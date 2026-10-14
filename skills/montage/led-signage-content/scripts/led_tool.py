#!/usr/bin/env python3
"""LED signage helper for roll-ups, posters and walls.

Subcommands (all print JSON):
  profiles    list device profiles
  text-size   minimum text heights in mm, LED pixels and AE font size
  guides      write a transparent PNG guide overlay (no dependencies)
  export      pixel-exact H.264 MP4 for a profile (plan with --dry-run)
  split       one decode -> one file per screen of a multi-screen wall
  check       verify an encoded file against a profile

Safety: inputs are never modified, existing outputs are refused, nothing is
installed. FFmpeg is found via $FFMPEG, PATH, or the imageio-ffmpeg package;
ffprobe is optional ($FFPROBE or PATH).
"""
import argparse
import json
import math
import os
import re
import shutil
import struct
import subprocess
import sys
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_PROFILES = HERE / "led_profiles.json"
# Movement coefficients from Nummax's published LED text-height method:
# text height = reading distance / 150 x coefficient.
MOVEMENT = {"static": 1.0, "pedestrian": 1.2, "parking": 1.6, "quiet-street": 2.0, "traffic": 2.6}
# Toolbox heuristics: the formula gives the smallest *detail* line.
TIERS = (("detail", 1.0), ("information", 1.5), ("hook", 2.5))
H264_LEVELS = (("4.1", 245760, 8192), ("4.2", 522240, 8704), ("5.1", 983040, 36864), ("5.2", 2073600, 36864))


class UsageError(Exception):
    pass


# ---------------------------------------------------------------- profiles
def load_profiles(path=None):
    file = Path(path) if path else DEFAULT_PROFILES
    try:
        data = json.loads(file.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise UsageError(f"Cannot read profiles file: {error.__class__.__name__}")
    if data.get("schema") != 1 or not isinstance(data.get("profiles"), dict):
        raise UsageError("Invalid profiles file (schema 1 with a 'profiles' object expected).")
    return data["profiles"]


def get_profile(name, path=None):
    profiles = load_profiles(path)
    if name not in profiles:
        raise UsageError(f"Unknown profile '{name}'. Known: {', '.join(sorted(profiles))}")
    prof = dict(profiles[name])
    prof["name"] = name
    w, h = prof.get("width"), prof.get("height")
    if not (isinstance(w, int) and isinstance(h, int) and not isinstance(w, bool) and w >= 16 and h >= 16):
        raise UsageError("Profile width/height must be integers >= 16.")
    cols, rows = prof.get("screens", [1, 1])
    if not (isinstance(cols, int) and isinstance(rows, int) and cols >= 1 and rows >= 1 and w % cols == 0 and h % rows == 0):
        raise UsageError("Profile 'screens' must divide the pixel size exactly.")
    fps = prof.get("fps", 30)
    if not (isinstance(fps, (int, float)) and 1 <= fps <= 120):
        raise UsageError("Profile fps must be between 1 and 120.")
    return prof


# --------------------------------------------------------------- text size
def text_size(pitch_mm, distance_m, coefficient, cap_ratio=0.70):
    if not (pitch_mm and pitch_mm > 0 and distance_m > 0 and coefficient > 0 and 0.3 <= cap_ratio <= 1.0):
        raise UsageError("pitch, distance and coefficient must be > 0; cap ratio between 0.3 and 1.0.")
    base_mm = distance_m * 1000.0 / 150.0 * coefficient
    tiers = {}
    for tier, mult in TIERS:
        mm = base_mm * mult
        px = max(1, math.ceil(mm / pitch_mm - 1e-9))
        tiers[tier] = {
            "cap_height_mm": round(mm, 1),
            "cap_height_px": px,
            "ae_font_size_px": math.ceil(px / cap_ratio - 1e-9),
        }
    return {
        "pitch_mm": pitch_mm,
        "distance_m": distance_m,
        "movement_coefficient": coefficient,
        "cap_ratio": cap_ratio,
        "tiers": tiers,
        "method": "detail line = distance/150 x movement coefficient (Nummax); information x1.5 and hook x2.5 are toolbox heuristics",
        "verify": "Measure the cap height of the chosen font in AE (sourceRectAtTime of 'H') and test on the real screen at the real distance.",
    }


# ------------------------------------------------------------------ guides
class Canvas:
    def __init__(self, width, height):
        self.w, self.h = width, height
        self.buf = bytearray(width * height * 4)

    def rect(self, x0, y0, x1, y1, rgba):
        x0, x1 = max(0, min(self.w, int(x0))), max(0, min(self.w, int(x1)))
        y0, y1 = max(0, min(self.h, int(y0))), max(0, min(self.h, int(y1)))
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(rgba) * (x1 - x0)
        for y in range(y0, y1):
            start = (y * self.w + x0) * 4
            self.buf[start:start + len(row)] = row

    def outline(self, x0, y0, x1, y1, rgba, t=1):
        self.rect(x0, y0, x1, y0 + t, rgba)
        self.rect(x0, y1 - t, x1, y1, rgba)
        self.rect(x0, y0, x0 + t, y1, rgba)
        self.rect(x1 - t, y0, x1, y1, rgba)

    def png(self):
        stride = self.w * 4
        raw = b"".join(b"\x00" + bytes(self.buf[y * stride:(y + 1) * stride]) for y in range(self.h))

        def chunk(tag, data):
            return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

        return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", self.w, self.h, 8, 6, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def guide_plan(prof, distance_m=None, movement=None, cap_ratio=0.70):
    w, h = prof["width"], prof["height"]
    margin = int(prof.get("safe_margin_px", 0))
    cols, rows = prof.get("screens", [1, 1])
    plan = {
        "size": [w, h],
        "safe_rect": [margin, margin, w - margin, h - margin],
        "prime_zone": [0, 0, w, round(h / 3)] if prof.get("prime_zone") else None,
        "occlusion_zone": None,
        "seams_x": [w // cols * i for i in range(1, cols)],
        "seams_y": [h // rows * i for i in range(1, rows)],
        "text_bars": None,
    }
    pct = prof.get("occlusion_risk_bottom_pct")
    if pct:
        plan["occlusion_zone"] = [0, h - round(h * pct / 100.0), w, h]
    if prof.get("pitch_mm"):
        dist = distance_m or max(prof.get("typical_viewing_distance_m", [3])[-1], 0.5)
        coef = MOVEMENT.get(movement or prof.get("movement", "pedestrian"), 1.2)
        sizes = text_size(prof["pitch_mm"], dist, coef, cap_ratio)
        plan["text_bars"] = {"distance_m": dist, "heights_px": {k: v["cap_height_px"] for k, v in sizes["tiers"].items()}}
    return plan


def draw_guides(plan):
    w, h = plan["size"]
    c = Canvas(w, h)
    if plan["prime_zone"]:
        c.rect(*plan["prime_zone"], (40, 200, 90, 34))
    if plan["occlusion_zone"]:
        c.rect(*plan["occlusion_zone"], (230, 50, 50, 40))
    c.outline(*plan["safe_rect"], (0, 220, 255, 200))
    c.rect(w // 2, 0, w // 2 + 1, h, (255, 0, 200, 110))
    c.rect(0, h // 2, w, h // 2 + 1, (255, 0, 200, 110))
    for x in plan["seams_x"]:
        c.rect(x - 1, 0, x + 1, h, (255, 210, 0, 230))
    for y in plan["seams_y"]:
        c.rect(0, y - 1, w, y + 1, (255, 210, 0, 230))
    if plan["text_bars"]:
        x = plan["safe_rect"][0] + 4
        y = plan["safe_rect"][1] + 8
        for tier in ("hook", "information", "detail"):
            px = plan["text_bars"]["heights_px"][tier]
            c.rect(x, y, x + 10, y + px, (255, 255, 255, 200))
            x += 18
    return c.png()


def draw_testcard(prof, distance_m=None, movement=None):
    """Opaque test card: edge border, grid, patches, grey steps, gradient,
    fine-line patterns (reveal player scaling) and text-size bars."""
    w, h = prof["width"], prof["height"]
    c = Canvas(w, h)
    c.rect(0, 0, w, h, (0, 0, 0, 255))
    for x in range(0, w, 50):
        c.rect(x, 0, x + 1, h, (60, 60, 60, 255))
    for y in range(0, h, 50):
        c.rect(0, y, w, y + 1, (60, 60, 60, 255))
    c.outline(0, 0, w, h, (255, 0, 0, 255))            # outermost pixels: must all be visible
    arm = max(8, min(w, h) // 12)
    for (x, y, dx, dy) in ((1, 1, 1, 1), (w - 1, 1, -1, 1), (1, h - 1, 1, -1), (w - 1, h - 1, -1, -1)):
        c.rect(min(x, x + dx * arm), y - (0 if dy > 0 else 3), max(x, x + dx * arm), y + (3 if dy > 0 else 0), (255, 255, 255, 255))
        c.rect(x - (0 if dx > 0 else 3), min(y, y + dy * arm), x + (3 if dx > 0 else 0), max(y, y + dy * arm), (255, 255, 255, 255))
    m = max(8, w // 20)
    band = max(12, h // 16)
    y = m * 2
    patches = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255), (255, 255, 0), (255, 255, 255), (128, 128, 128)]
    pw = (w - 2 * m) / len(patches)
    for i, col in enumerate(patches):
        c.rect(m + i * pw, y, m + (i + 1) * pw, y + band, (*col, 255))
    y += band + m
    for i in range(11):                                  # 0..100% grey steps
        v = round(255 * i / 10)
        c.rect(m + i * (w - 2 * m) / 11, y, m + (i + 1) * (w - 2 * m) / 11, y + band, (v, v, v, 255))
    y += band + m
    for x in range(m, w - m):                            # smooth ramp: banding check
        v = round(255 * (x - m) / max(1, w - 2 * m - 1))
        c.rect(x, y, x + 1, y + band, (v, v, v, 255))
    y += band + m
    third = (w - 2 * m) // 3
    for x in range(m, m + third, 2):                     # 1 px lines
        c.rect(x, y, x + 1, y + band, (255, 255, 255, 255))
    for x in range(m + third, m + 2 * third, 4):         # 2 px lines
        c.rect(x, y, x + 2, y + band, (255, 255, 255, 255))
    for yy in range(y, y + band):                        # 1 px checkerboard
        for x in range(m + 2 * third + (yy % 2), w - m, 2):
            c.rect(x, yy, x + 1, yy + 1, (255, 255, 255, 255))
    y += band + m
    if prof.get("pitch_mm"):
        dist = distance_m or max(prof.get("typical_viewing_distance_m", [3])[-1], 0.5)
        sizes = text_size(prof["pitch_mm"], dist, MOVEMENT.get(movement or prof.get("movement", "pedestrian"), 1.2))
        x = m
        for tier in ("hook", "information", "detail"):
            px = sizes["tiers"][tier]["cap_height_px"]
            c.rect(x, y, x + max(4, px // 2), y + px, (255, 255, 255, 255))
            x += max(4, px // 2) + m
    cols, rows = prof.get("screens", [1, 1])
    for i in range(1, cols):
        c.rect(w // cols * i - 1, 0, w // cols * i + 1, h, (255, 210, 0, 255))
    for i in range(1, rows):
        c.rect(0, h // rows * i - 1, w, h // rows * i + 1, (255, 210, 0, 255))
    return c.png()


def testcard_video_plan(prof, png, out, seconds=10, overwrite=False):
    w, h = prof["width"], prof["height"]
    fps = prof.get("fps", 30)
    if not (2 <= seconds <= 120):
        raise UsageError("Test video duration must be 2-120 s.")
    out = _require_new(out, overwrite)
    step = max(1, w // int(round(fps * 2)))              # vertical bar crosses the frame in ~2 s
    vstep = max(1, h // int(round(fps * 3)))             # horizontal bar in ~3 s
    ffmpeg = find_tool("ffmpeg") or "ffmpeg"
    graph = (f"[0:v]fps={fps:g},format=rgb24[card];"
             f"[1:v]format=rgb24[vb];[2:v]format=rgb24[hb];"
             f"[card][vb]overlay=x='mod(n*{step},W)':y=0[a];"
             f"[a][hb]overlay=x=0:y='mod(n*{vstep},H)',"
             f"scale={w}:{h}:out_color_matrix=bt709:out_range=tv,setsar=1,format=yuv420p[v]")
    args = [ffmpeg, "-hide_banner", "-nostdin", "-y" if overwrite else "-n",
            "-loop", "1", "-framerate", f"{fps:g}", "-i", str(png),
            "-f", "lavfi", "-i", f"color=c=white:s=6x{h}:r={fps:g}",
            "-f", "lavfi", "-i", f"color=c=0x00FFFF:s={w}x4:r={fps:g}",
            "-filter_complex", graph, "-map", "[v]", "-t", f"{seconds:g}",
            *encode_args(w, h, fps, 16, 12.0, "drop"), str(out)]
    return {"action": "testcard-video", "profile": prof["name"], "seconds": seconds, "command": args, "output": str(out),
            "how_to_read": ["Red 1 px border must be visible on all four edges (no crop/overscan).",
                            "1 px lines and checkerboard must stay crisp; blur or beating means the player rescales.",
                            "Grey steps: all 11 distinguishable; ramp: no strong bands.",
                            "Moving bars must cross screen seams without jumping (multi-screen sync)."]}


# ------------------------------------------------------------------ ffmpeg
def find_tool(name):
    env = os.environ.get(name.upper())
    if env and Path(env).is_file():
        return env
    found = shutil.which(name)
    if found:
        return found
    if name == "ffmpeg":
        try:
            import imageio_ffmpeg  # optional
            return imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            return None
    return None


def _fps(text):
    if not text or text in ("0/0", "N/A"):
        return None
    if "/" in text:
        num, den = text.split("/", 1)
        return float(num) / float(den) if float(den) else None
    return float(text)


def probe(path):
    """Return a small stream summary, using ffprobe when present, else ffmpeg -i."""
    ffprobe = find_tool("ffprobe")
    if ffprobe:
        r = subprocess.run([ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode == 0:
            data = json.loads(r.stdout or "{}")
            v = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
            a = [s for s in data.get("streams", []) if s.get("codec_type") == "audio"]
            return {
                "via": "ffprobe",
                "duration_s": float(data.get("format", {}).get("duration", 0) or 0),
                "video": None if not v else {
                    "codec": v.get("codec_name"), "profile": v.get("profile"), "pix_fmt": v.get("pix_fmt"),
                    "width": v.get("width"), "height": v.get("height"),
                    "fps": _fps(v.get("avg_frame_rate")) or _fps(v.get("r_frame_rate")),
                    "color_space": v.get("color_space"),
                },
                "audio_streams": len(a),
            }
    ffmpeg = find_tool("ffmpeg")
    if not ffmpeg:
        raise UsageError("FFmpeg not found (set FFMPEG, add it to PATH, or pip install imageio-ffmpeg).")
    r = subprocess.run([ffmpeg, "-hide_banner", "-i", str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return parse_ffmpeg_banner(r.stderr)


def parse_ffmpeg_banner(text):
    out = {"via": "ffmpeg-banner", "duration_s": 0.0, "video": None, "audio_streams": 0}
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", text)
    if m:
        out["duration_s"] = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    for line in text.splitlines():
        if "Stream #" in line and "Video:" in line and out["video"] is None:
            desc = line.split("Video:", 1)[1].strip()
            codec = desc.split()[0].strip(",")
            prof = re.search(r"^\S+\s+\(([^)]+)\)", desc)
            size = re.search(r"(?<![\dx])(\d{2,5})x(\d{2,5})(?![\dx])", desc)
            fps = re.search(r"([\d.]+)\s+fps", desc)
            pix = re.search(r"\),\s*([a-z0-9_]+)\(|,\s*(yuv[a-z0-9_]+|rgb[a-z0-9_]*|gbr[a-z0-9_]*|gray[a-z0-9_]*)", desc)
            out["video"] = {
                "codec": codec,
                "profile": prof.group(1) if prof and not prof.group(1).startswith(("avc1", "hvc1", "mp4v")) else None,
                "pix_fmt": (pix.group(1) or pix.group(2)) if pix else None,
                "width": int(size.group(1)) if size else None,
                "height": int(size.group(2)) if size else None,
                "fps": float(fps.group(1)) if fps else None,
                "color_space": "bt709" if "bt709" in desc else None,
            }
        elif "Stream #" in line and "Audio:" in line:
            out["audio_streams"] += 1
    return out


def h264_level(w, h, fps):
    mbs = math.ceil(w / 16) * math.ceil(h / 16)
    for name, max_rate, max_frame in H264_LEVELS:
        if mbs <= max_frame and mbs * fps <= max_rate:
            return name
    raise UsageError("Frame size x fps exceeds H.264 level 5.2; use a smaller size or frame rate.")


def video_filters(w, h, fit, fps):
    colour = "flags=lanczos:out_color_matrix=bt709:out_range=tv"
    if fit == "exact":
        chain = [f"scale={w}:{h}:{colour}"]
    elif fit == "contain":
        chain = [f"scale={w}:{h}:force_original_aspect_ratio=decrease:{colour}", f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black"]
    elif fit == "cover":
        chain = [f"scale={w}:{h}:force_original_aspect_ratio=increase:{colour}", f"crop={w}:{h}"]
    else:
        raise UsageError("fit must be exact, contain or cover.")
    return [f"fps={fps:g}"] + chain + ["setsar=1", "format=yuv420p"]


def encode_args(w, h, fps, crf, maxrate_mbps, audio):
    if w % 2 or h % 2:
        raise UsageError("H.264 4:2:0 needs even width and height.")
    if not (0 <= crf <= 30) or not (0.5 <= maxrate_mbps <= 80):
        raise UsageError("crf must be 0-30 and maxrate 0.5-80 Mbps.")
    args = ["-c:v", "libx264", "-preset", "slow", "-crf", f"{crf:g}",
            "-maxrate", f"{maxrate_mbps:g}M", "-bufsize", f"{maxrate_mbps * 2:g}M",
            "-profile:v", "high", "-level:v", h264_level(w, h, fps), "-pix_fmt", "yuv420p",
            "-g", str(int(round(fps * 2))), "-r", f"{fps:g}",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
    args += ["-an"] if audio == "drop" else ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
    return args + ["-movflags", "+faststart", "-map_metadata", "-1"]


def _require_input(path):
    p = Path(path)
    if not p.is_file():
        raise UsageError("Input file not found.")
    return p


def _require_new(path, overwrite, src=None):
    p = Path(path)
    if src is not None and p.resolve() == Path(src).resolve():
        raise UsageError("Output must differ from input.")
    if p.exists() and not overwrite:
        raise UsageError(f"Refusing to overwrite existing file: {p.name} (use --overwrite deliberately).")
    if not p.parent.exists():
        raise UsageError("Output folder does not exist.")
    return p


def export_plan(prof, src, out, fit="exact", fps=None, crf=18, maxrate=12.0, audio=None, overwrite=False, probe_input=True):
    src = _require_input(src)
    out = _require_new(out, overwrite, src)
    w, h = prof["width"], prof["height"]
    fps = fps or prof.get("fps", 30)
    audio = audio or prof.get("audio", "drop")
    warnings = []
    info = None
    if probe_input:
        try:
            info = probe(src)
        except UsageError as error:
            warnings.append(str(error))
    if info and info.get("video"):
        v = info["video"]
        if v.get("width") and v.get("height"):
            if fit == "exact" and abs(v["width"] / v["height"] - w / h) > 0.002:
                warnings.append("Source aspect differs from the profile: 'exact' will distort; use contain/cover or re-author at device size.")
            if v["width"] < w or v["height"] < h:
                warnings.append("Source is smaller than the device: it will be upscaled; re-render at device size instead.")
            if (v["width"], v["height"]) != (w, h):
                warnings.append("Best practice: author at the exact device pixel size; scaling softens text and thin strokes.")
        if v.get("fps") and abs(v["fps"] - fps) > 0.01:
            warnings.append(f"Source is {v['fps']:g} fps; output will be resampled to {fps:g} fps.")
        if audio == "keep" and not info.get("audio_streams"):
            warnings.append("Audio 'keep' requested but the source has no audio stream.")
    ffmpeg = find_tool("ffmpeg") or "ffmpeg"
    maps = ["-map", "0:v:0"] + (["-map", "0:a:0?"] if audio == "keep" else [])
    args = [ffmpeg, "-hide_banner", "-nostdin", "-y" if overwrite else "-n", "-i", str(src), *maps,
            "-vf", ",".join(video_filters(w, h, fit, fps)), *encode_args(w, h, fps, crf, maxrate, audio), str(out)]
    return {"action": "export", "profile": prof["name"], "size": [w, h], "fps": fps, "fit": fit, "audio": audio,
            "input_probe": info, "warnings": warnings, "command": args, "output": str(out)}


def split_plan(prof, src, outdir, fit="exact", fps=None, crf=18, maxrate=12.0, overwrite=False):
    src = _require_input(src)
    cols, rows = prof.get("screens", [1, 1])
    if cols * rows < 2:
        raise UsageError("This profile is a single screen; use export.")
    w, h = prof["width"], prof["height"]
    sw, sh = w // cols, h // rows
    fps = fps or prof.get("fps", 30)
    outdir = Path(outdir)
    if outdir.exists() and not outdir.is_dir():
        raise UsageError("--outdir exists and is not a folder.")
    outputs = []
    for r in range(rows):
        for c in range(cols):
            n = r * cols + c + 1
            path = outdir / f"{Path(src).stem}_{prof['name']}_S{n}.mp4"
            if path.exists() and not overwrite:
                raise UsageError(f"Refusing to overwrite existing file: {path.name} (use --overwrite deliberately).")
            outputs.append({"screen": n, "crop": [sw, sh, c * sw, r * sh], "path": str(path)})
    labels = "".join(f"[s{i}]" for i in range(len(outputs)))
    graph = f"[0:v]{','.join(video_filters(w, h, fit, fps))},split={len(outputs)}{labels}"
    for i, o in enumerate(outputs):
        cw, ch, cx, cy = o["crop"]
        graph += f";[s{i}]crop={cw}:{ch}:{cx}:{cy}[o{i}]"
    ffmpeg = find_tool("ffmpeg") or "ffmpeg"
    args = [ffmpeg, "-hide_banner", "-nostdin", "-y" if overwrite else "-n", "-i", str(src), "-filter_complex", graph]
    for i, o in enumerate(outputs):
        args += ["-map", f"[o{i}]", *encode_args(sw, sh, fps, crf, maxrate, "drop"), o["path"]]
    return {"action": "split", "profile": prof["name"], "screen_size": [sw, sh], "fps": fps, "outputs": outputs,
            "outdir": str(outdir), "overwrite": overwrite, "command": args,
            "notes": ["One decode feeds every screen, so all files share the same frames and duration.",
                      "Synchronised start still depends on the players (sync/NTP/genlock) - test on site."]}


def check_file(prof, path, audio=None):
    info = probe(_require_input(path))
    v = info.get("video") or {}
    audio = audio or prof.get("audio", "drop")
    checks = []

    def add(name, ok, detail, severity="error"):
        checks.append({"check": name, "ok": bool(ok), "severity": severity, "detail": detail})

    add("video_stream", bool(v), "video stream present")
    add("size", (v.get("width"), v.get("height")) == (prof["width"], prof["height"]),
        f"{v.get('width')}x{v.get('height')} vs {prof['width']}x{prof['height']}")
    add("codec", v.get("codec") == "h264", f"codec {v.get('codec')}")
    add("pix_fmt", (v.get("pix_fmt") or "").startswith("yuv420p"), f"pix_fmt {v.get('pix_fmt')}")
    fps = v.get("fps")
    add("fps", fps is not None and abs(fps - prof.get("fps", 30)) < 0.01, f"fps {fps} vs {prof.get('fps', 30)}")
    if audio == "drop":
        add("audio", info.get("audio_streams", 0) == 0, f"{info.get('audio_streams', 0)} audio stream(s); LED profile expects none", "warning")
    else:
        add("audio", info.get("audio_streams", 0) >= 1, f"{info.get('audio_streams', 0)} audio stream(s)")
    add("colour_tags", v.get("color_space") in ("bt709", None), f"colour space {v.get('color_space')}", "warning")
    add("duration", info.get("duration_s", 0) > 0, f"{info.get('duration_s')} s")
    ok = all(c["ok"] for c in checks if c["severity"] == "error")
    return {"action": "check", "profile": prof["name"], "file": Path(path).name, "probe": info, "checks": checks, "ok": ok,
            "next": "Run video-delivery-qc media_qc.py for full decode, black/freeze detection and loop seam."}


def run(plan):
    r = subprocess.run(plan["command"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    plan = dict(plan)
    plan["returncode"] = r.returncode
    if r.returncode:
        plan["stderr_tail"] = r.stderr[-1500:]
    return plan


# --------------------------------------------------------------------- CLI
def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--profiles-file", help="alternative profiles JSON (same schema)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("profiles")
    t = sub.add_parser("text-size")
    t.add_argument("--profile")
    t.add_argument("--pitch", type=float, help="pixel pitch in mm (instead of --profile)")
    t.add_argument("--distance", type=float, help="reading distance in metres")
    t.add_argument("--movement", choices=sorted(MOVEMENT))
    t.add_argument("--coefficient", type=float)
    t.add_argument("--cap-ratio", type=float, default=0.70)
    g = sub.add_parser("guides")
    g.add_argument("--profile", required=True)
    g.add_argument("--out", required=True)
    g.add_argument("--distance", type=float)
    g.add_argument("--movement", choices=sorted(MOVEMENT))
    g.add_argument("--overwrite", action="store_true")
    g.add_argument("--dry-run", action="store_true")
    for name in ("export", "split"):
        e = sub.add_parser(name)
        e.add_argument("--profile", required=True)
        e.add_argument("--input", required=True)
        if name == "export":
            e.add_argument("--output", required=True)
            e.add_argument("--audio", choices=["drop", "keep"])
        else:
            e.add_argument("--outdir", required=True)
        e.add_argument("--fit", choices=["exact", "contain", "cover"], default="exact")
        e.add_argument("--fps", type=float)
        e.add_argument("--crf", type=float, default=18)
        e.add_argument("--maxrate", type=float, default=12.0, help="Mbps")
        e.add_argument("--overwrite", action="store_true")
        e.add_argument("--dry-run", action="store_true")
    c = sub.add_parser("check")
    c.add_argument("--profile", required=True)
    c.add_argument("--input", required=True)
    c.add_argument("--audio", choices=["drop", "keep"])
    tc = sub.add_parser("testcard")
    tc.add_argument("--profile", required=True)
    tc.add_argument("--out-png", required=True)
    tc.add_argument("--out-mp4", help="optional moving-bar test video for players and multi-screen sync")
    tc.add_argument("--seconds", type=float, default=10)
    tc.add_argument("--distance", type=float)
    tc.add_argument("--movement", choices=sorted(MOVEMENT))
    tc.add_argument("--overwrite", action="store_true")
    tc.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    try:
        if args.cmd == "profiles":
            result = {"profiles": load_profiles(args.profiles_file)}
        elif args.cmd == "text-size":
            prof = get_profile(args.profile, args.profiles_file) if args.profile else {}
            pitch = args.pitch or prof.get("pitch_mm")
            if not pitch:
                raise UsageError("Give --pitch or a profile with pitch_mm.")
            dist = args.distance or (prof.get("typical_viewing_distance_m") or [None])[-1]
            if not dist:
                raise UsageError("Give --distance in metres.")
            coef = args.coefficient or MOVEMENT[args.movement or prof.get("movement", "pedestrian")]
            result = text_size(pitch, dist, coef, args.cap_ratio)
            if prof:
                result["profile"] = args.profile
                result["screen_mm"] = [round(prof["width"] * pitch), round(prof["height"] * pitch)]
        elif args.cmd == "guides":
            prof = get_profile(args.profile, args.profiles_file)
            plan = guide_plan(prof, args.distance, args.movement)
            result = {"action": "guides", "profile": args.profile, "plan": plan, "output": args.out}
            if not args.dry_run:
                out = _require_new(args.out, args.overwrite)
                out.write_bytes(draw_guides(plan))
                result["written"] = True
        elif args.cmd == "export":
            prof = get_profile(args.profile, args.profiles_file)
            result = export_plan(prof, args.input, args.output, args.fit, args.fps, args.crf, args.maxrate,
                                 args.audio, args.overwrite, probe_input=True)
            if not args.dry_run:
                result = run(result)
        elif args.cmd == "split":
            prof = get_profile(args.profile, args.profiles_file)
            result = split_plan(prof, args.input, args.outdir, args.fit, args.fps, args.crf, args.maxrate, args.overwrite)
            if not args.dry_run:
                Path(args.outdir).mkdir(parents=True, exist_ok=True)
                result = run(result)
        elif args.cmd == "testcard":
            prof = get_profile(args.profile, args.profiles_file)
            png = _require_new(args.out_png, args.overwrite)
            result = {"action": "testcard", "profile": args.profile, "png": str(png)}
            video = testcard_video_plan(prof, png, args.out_mp4, args.seconds, args.overwrite) if args.out_mp4 else None
            if not args.dry_run:
                png.write_bytes(draw_testcard(prof, args.distance, args.movement))
                result["written"] = True
                if video:
                    video = run(video)
            if video:
                result["video"] = video
                result["returncode"] = video.get("returncode", 0)
        else:
            result = check_file(get_profile(args.profile, args.profiles_file), args.input, args.audio)
    except UsageError as error:
        print(json.dumps({"ok": False, "error": str(error)}, indent=2))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result.get("returncode"):
        return 1
    if result.get("action") == "check" and not result["ok"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
