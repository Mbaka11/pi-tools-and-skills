#!/usr/bin/env python3
"""Decode-based QC for a delivered video file.

Measures the encoded file itself: stream summary, full video decode with frame
count and decode errors, black and frozen segments, audio loudness (EBU R128
integrated, LRA, true peak) and silence, an optional loop-seam score (SSIM of
last->first frame compared with normal frame-to-frame change), and an optional
contact sheet built from evenly spaced encoded frames.

Never modifies the input; refuses to overwrite reports or sheets unless
--overwrite. FFmpeg via $FFMPEG, PATH or the imageio-ffmpeg package; ffprobe is
optional. Exit 0 = all error-level checks pass, 1 = a check failed, 2 = usage.
"""
import argparse
import hashlib
import json
import math
import os
import re
import shutil
import statistics
import subprocess
import sys
from pathlib import Path


class UsageError(Exception):
    pass


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


_VERSION_CACHE = {}


def ffmpeg_version(ffmpeg):
    """(major, minor) of FFmpeg, or None when it cannot be parsed (git builds)."""
    if ffmpeg not in _VERSION_CACHE:
        r = subprocess.run([ffmpeg, "-hide_banner", "-version"], capture_output=True, text=True, encoding="utf-8", errors="replace")
        m = re.search(r"ffmpeg version n?(\d+)\.(\d+)", r.stdout or "")
        _VERSION_CACHE[ffmpeg] = (int(m.group(1)), int(m.group(2))) if m else None
    return _VERSION_CACHE[ffmpeg]


def fps_mode(ffmpeg, mode):
    """-fps_mode for FFmpeg >= 5.1, the older -vsync spelling otherwise."""
    version = ffmpeg_version(ffmpeg) if Path(str(ffmpeg)).exists() or shutil.which(str(ffmpeg)) else None
    if version is not None and version < (5, 1):
        return ["-vsync", mode]
    return ["-fps_mode", mode]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _fps(text):
    if not text or text in ("0/0", "N/A"):
        return None
    if "/" in text:
        num, den = text.split("/", 1)
        return float(num) / float(den) if float(den) else None
    return float(text)


def parse_banner(text):
    out = {"via": "ffmpeg-banner", "duration_s": 0.0, "video": None, "audio": []}
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", text)
    if m:
        out["duration_s"] = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    for line in text.splitlines():
        if "Stream #" in line and "Video:" in line and out["video"] is None:
            desc = line.split("Video:", 1)[1].strip()
            size = re.search(r"(?<![\dx])(\d{2,5})x(\d{2,5})(?![\dx])", desc)
            fps = re.search(r"([\d.]+)\s+fps", desc)
            pix = re.search(r"\),\s*([a-z0-9_]+)\(|,\s*(yuv[a-z0-9_]+|rgb[a-z0-9_]*|gbr[a-z0-9_]*|gray[a-z0-9_]*)", desc)
            out["video"] = {
                "codec": desc.split()[0].strip(","),
                "pix_fmt": (pix.group(1) or pix.group(2)) if pix else None,
                "width": int(size.group(1)) if size else None,
                "height": int(size.group(2)) if size else None,
                "fps": float(fps.group(1)) if fps else None,
                "color_space": "bt709" if "bt709" in desc else None,
            }
        elif "Stream #" in line and "Audio:" in line:
            desc = line.split("Audio:", 1)[1].strip()
            rate = re.search(r"(\d+)\s*Hz", desc)
            out["audio"].append({"codec": desc.split()[0].strip(","), "sample_rate": int(rate.group(1)) if rate else None,
                                 "layout": "stereo" if "stereo" in desc else ("mono" if "mono" in desc else None)})
    return out


def probe(path, ffmpeg):
    ffprobe = find_tool("ffprobe")
    if ffprobe:
        r = subprocess.run([ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode == 0:
            data = json.loads(r.stdout or "{}")
            streams = data.get("streams", [])
            v = next((s for s in streams if s.get("codec_type") == "video"), None)
            return {
                "via": "ffprobe",
                "duration_s": float(data.get("format", {}).get("duration", 0) or 0),
                "video": None if not v else {
                    "codec": v.get("codec_name"), "pix_fmt": v.get("pix_fmt"), "width": v.get("width"), "height": v.get("height"),
                    "fps": _fps(v.get("avg_frame_rate")) or _fps(v.get("r_frame_rate")), "color_space": v.get("color_space"),
                },
                "audio": [{"codec": s.get("codec_name"), "sample_rate": int(s.get("sample_rate") or 0) or None,
                           "layout": s.get("channel_layout")} for s in streams if s.get("codec_type") == "audio"],
            }
    r = subprocess.run([ffmpeg, "-hide_banner", "-nostdin", "-i", str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return parse_banner(r.stderr)


def run(args):
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")


# ---------------------------------------------------------------- passes
def video_pass_cmd(ffmpeg, path, black_pic_th=0.98, black_pix_th=0.10, freeze_noise="-60dB", freeze_d=1.0):
    vf = f"blackdetect=d=0.1:pic_th={black_pic_th}:pix_th={black_pix_th},freezedetect=n={freeze_noise}:d={freeze_d}"
    return [ffmpeg, "-hide_banner", "-nostdin", "-nostats", "-v", "info", "-i", str(path), "-map", "0:v:0",
            "-vf", vf, "-f", "null", "-", "-progress", "pipe:1"]


def parse_video_pass(stdout, stderr):
    frames = [int(x) for x in re.findall(r"^frame=(\d+)", stdout, re.M)]
    black = [{"start": float(a), "end": float(b), "duration": float(c)}
             for a, b, c in re.findall(r"black_start:\s*([\d.]+)\s+black_end:\s*([\d.]+)\s+black_duration:\s*([\d.]+)", stderr)]
    starts = [float(x) for x in re.findall(r"freeze_start:\s*([\d.]+)", stderr)]
    ends = [float(x) for x in re.findall(r"freeze_end:\s*([\d.]+)", stderr)]
    freezes = [{"start": s, "end": ends[i] if i < len(ends) else None} for i, s in enumerate(starts)]
    errors = [l.strip() for l in stderr.splitlines()
              if re.search(r"error while decoding|corrupt|Invalid data found|concealing|missing picture", l, re.I)]
    return {"decoded_frames": frames[-1] if frames else None, "black_segments": black, "freeze_segments": freezes,
            "decode_error_lines": len(errors), "decode_error_sample": errors[:5]}


def audio_pass_cmd(ffmpeg, path, silence_noise="-50dB", silence_d=1.0):
    return [ffmpeg, "-hide_banner", "-nostdin", "-nostats", "-v", "info", "-i", str(path), "-map", "0:a:0",
            "-af", f"ebur128=peak=true,silencedetect=n={silence_noise}:d={silence_d}", "-f", "null", "-"]


def _num(x):
    return None if x is None or x.endswith("inf") else float(x)


def parse_audio_pass(stderr):
    i = re.findall(r"I:\s*(-?[\d.]+|-inf)\s*LUFS", stderr)
    lra = re.findall(r"LRA:\s*(-?[\d.]+)\s*LU\b", stderr)
    peak = re.findall(r"Peak:\s*(-?[\d.]+|-inf)\s*dBFS", stderr)
    s_start = [float(x) for x in re.findall(r"silence_start:\s*(-?[\d.]+)", stderr)]
    s_end = re.findall(r"silence_end:\s*(-?[\d.]+)\s*\|\s*silence_duration:\s*([\d.]+)", stderr)
    silences = []
    for k, start in enumerate(s_start):
        end = float(s_end[k][0]) if k < len(s_end) else None
        silences.append({"start": max(0.0, start), "end": end})
    return {"integrated_lufs": _num(i[-1]) if i else None, "lra_lu": _num(lra[-1]) if lra else None,
            "true_peak_dbfs": _num(peak[-1]) if peak else None, "silence_segments": silences}


def seam_cmd(ffmpeg, path, frames):
    graph = (f"[0:v]select='eq(n\\,{frames - 1})',setpts=PTS-STARTPTS[a];"
             f"[1:v]select='eq(n\\,0)',setpts=PTS-STARTPTS[b];[a][b]ssim")
    return [ffmpeg, "-hide_banner", "-nostdin", "-nostats", "-v", "info", "-i", str(path), "-i", str(path),
            "-filter_complex", graph, *fps_mode(ffmpeg, "passthrough"), "-f", "null", "-"]


def consecutive_cmd(ffmpeg, path, frames):
    graph = (f"[0:v]trim=end_frame={frames - 1},setpts=PTS-STARTPTS[a];"
             f"[1:v]trim=start_frame=1,setpts=PTS-STARTPTS[b];[a][b]ssim=stats_file=-")
    return [ffmpeg, "-hide_banner", "-nostdin", "-nostats", "-v", "error", "-i", str(path), "-i", str(path),
            "-filter_complex", graph, "-f", "null", "-"]


def parse_ssim_summary(stderr):
    m = re.findall(r"SSIM .*?All:\s*([\d.]+)", stderr)
    return float(m[-1]) if m else None


def parse_ssim_stats(stdout):
    return [float(x) for x in re.findall(r"All:\s*([\d.]+)", stdout)]


def loop_verdict(seam, consecutive):
    if seam is None:
        return {"ok": False, "verdict": "seam could not be measured"}
    if not consecutive:
        return {"ok": seam >= 0.97, "seam_ssim": seam, "verdict": "no consecutive statistics; judged against 0.97"}
    ordered = sorted(consecutive)
    p5 = ordered[max(0, int(math.floor(0.05 * (len(ordered) - 1))))]
    med = statistics.median(ordered)
    ok = seam >= min(p5, 0.97)
    return {"ok": ok, "seam_ssim": round(seam, 5), "consecutive_median": round(med, 5), "consecutive_p5": round(p5, 5),
            "verdict": "seam behaves like a normal frame step" if ok else
            "seam is a visible jump compared with normal frame steps - confirm it is an intended cut"}


def contact_cmd(ffmpeg, path, frames, out, cols, rows, width):
    k = cols * rows
    idx = sorted({round(i * (frames - 1) / max(1, k - 1)) for i in range(k)})
    sel = "+".join(f"eq(n\\,{i})" for i in idx)
    vf = f"select='{sel}',scale={width}:-2,tile={cols}x{rows}:padding=4:margin=4:color=0x202020"
    return [ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-n", "-i", str(path), "-vf", vf,
            *fps_mode(ffmpeg, "vfr"), "-frames:v", "1", *(["-q:v", "3"] if out.suffix.lower() in (".jpg", ".jpeg") else []), str(out)], idx


# ----------------------------------------------------------------- checks
def build_checks(args, info, video, audio, loop):
    checks = []

    def add(name, ok, detail, severity="error"):
        checks.append({"check": name, "ok": bool(ok), "severity": severity, "detail": detail})

    v = info.get("video") or {}
    if not v and info.get("audio"):
        add("audio_only", True, "no video stream: audio-file checks only", "info")
        if args.expect_audio == "no":
            add("audio", False, "audio file but --expect-audio no")
        if audio and args.loudness_target is not None and audio.get("integrated_lufs") is not None:
            add("loudness", abs(audio["integrated_lufs"] - args.loudness_target) <= args.loudness_tolerance,
                f"{audio['integrated_lufs']} LUFS vs {args.loudness_target} \u00b1{args.loudness_tolerance}")
        if audio and args.true_peak_max is not None and audio.get("true_peak_dbfs") is not None:
            add("true_peak", audio["true_peak_dbfs"] <= args.true_peak_max, f"{audio['true_peak_dbfs']} dBTP vs max {args.true_peak_max}")
        return checks
    add("video_stream", bool(v), "video stream present")
    if args.expect_width or args.expect_height:
        add("size", (v.get("width"), v.get("height")) == (args.expect_width or v.get("width"), args.expect_height or v.get("height")),
            f"{v.get('width')}x{v.get('height')}")
    fps = v.get("fps")
    if args.expect_fps:
        add("fps", fps is not None and abs(fps - args.expect_fps) < 0.01, f"{fps} fps")
    frames = video.get("decoded_frames") if video else None
    add("full_decode", frames is not None and frames > 0 and video.get("decode_error_lines", 1) == 0,
        f"{frames} frames decoded, {video.get('decode_error_lines') if video else 'n/a'} decoder error line(s)")
    if frames and fps and info.get("duration_s"):
        expected = info["duration_s"] * fps
        add("frame_count_vs_duration", abs(frames - expected) <= max(1.5, 0.002 * expected),
            f"{frames} decoded vs ~{expected:.1f} from duration x fps", "warning")
    if args.expect_frames is not None:
        add("frames", frames == args.expect_frames, f"{frames} vs {args.expect_frames}")
    if args.expect_duration is not None:
        add("duration", abs(info.get("duration_s", 0) - args.expect_duration) <= (1.0 / fps if fps else 0.05),
            f"{info.get('duration_s')} s vs {args.expect_duration} s")
    n_audio = len(info.get("audio") or [])
    if args.expect_audio == "no":
        add("audio", n_audio == 0, f"{n_audio} audio stream(s), expected none")
    elif args.expect_audio == "yes":
        add("audio", n_audio >= 1, f"{n_audio} audio stream(s)")
    if video:
        dur = info.get("duration_s") or 0
        edge_black = [b for b in video["black_segments"] if b["start"] <= 0.05 or (dur and b["end"] >= dur - 0.05)]
        add("black_at_edges", not edge_black, f"{len(edge_black)} black segment(s) touching start/end", "warning")
        add("black_segments", True, f"{len(video['black_segments'])} black segment(s) >= 0.1 s (review list)", "info")
        add("freeze_segments", True, f"{len(video['freeze_segments'])} frozen segment(s) >= {args.freeze_seconds} s (holds are normal on LED)", "info")
    if audio:
        if args.loudness_target is not None and audio.get("integrated_lufs") is not None:
            add("loudness", abs(audio["integrated_lufs"] - args.loudness_target) <= args.loudness_tolerance,
                f"{audio['integrated_lufs']} LUFS vs {args.loudness_target} ±{args.loudness_tolerance}")
        if args.true_peak_max is not None and audio.get("true_peak_dbfs") is not None:
            add("true_peak", audio["true_peak_dbfs"] <= args.true_peak_max, f"{audio['true_peak_dbfs']} dBTP vs max {args.true_peak_max}")
    if loop is not None:
        add("loop_seam", loop.get("ok"), loop.get("verdict"))
    return checks


def _new_path(p, overwrite, src):
    if p is None:
        return None
    p = Path(p)
    if p.resolve() == Path(src).resolve():
        raise UsageError("Output must differ from the input.")
    if p.exists() and not overwrite:
        raise UsageError(f"Refusing to overwrite existing file: {p.name} (use --overwrite deliberately).")
    if not p.parent.exists():
        raise UsageError("Output folder does not exist.")
    return p


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("input")
    ap.add_argument("--report", help="write the JSON report here")
    ap.add_argument("--contact-sheet", help="write a contact sheet (.jpg/.png) of encoded frames")
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--rows", type=int, default=3)
    ap.add_argument("--tile-width", type=int, default=0, help="px per tile (default: 320 landscape, 200 portrait)")
    ap.add_argument("--expect-width", type=int)
    ap.add_argument("--expect-height", type=int)
    ap.add_argument("--expect-fps", type=float)
    ap.add_argument("--expect-frames", type=int)
    ap.add_argument("--expect-duration", type=float)
    ap.add_argument("--expect-audio", choices=["yes", "no"])
    ap.add_argument("--loop-check", action="store_true")
    ap.add_argument("--loudness-target", type=float, help="integrated LUFS target, e.g. -14 web, -24 Canadian broadcast")
    ap.add_argument("--loudness-tolerance", type=float, default=1.0)
    ap.add_argument("--true-peak-max", type=float, help="maximum true peak dBTP, e.g. -1")
    ap.add_argument("--freeze-seconds", type=float, default=1.0)
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="print the planned FFmpeg passes and exit")
    args = ap.parse_args(argv)
    try:
        if not (1 <= args.cols <= 10 and 1 <= args.rows <= 10):
            raise UsageError("cols/rows must be 1-10.")
        src = Path(args.input)
        if not src.is_file():
            raise UsageError("Input file not found.")
        report_path = _new_path(args.report, args.overwrite, src)
        sheet_path = _new_path(args.contact_sheet, args.overwrite, src)
        ffmpeg = find_tool("ffmpeg")
        if args.dry_run:
            exe = ffmpeg or "ffmpeg"
            plan = {"dry_run": True, "passes": {"video": video_pass_cmd(exe, src, freeze_d=args.freeze_seconds),
                                               "audio_if_present": audio_pass_cmd(exe, src)},
                    "loop_check": "seam SSIM (last->first) + consecutive SSIM statistics" if args.loop_check else None,
                    "contact_sheet": str(sheet_path) if sheet_path else None, "report": str(report_path) if report_path else None}
            print(json.dumps(plan, indent=2))
            return 0
        if not ffmpeg:
            raise UsageError("FFmpeg not found (set FFMPEG, add it to PATH, or pip install imageio-ffmpeg).")
        info = probe(src, ffmpeg)
        r = run(video_pass_cmd(ffmpeg, src, freeze_d=args.freeze_seconds))
        video = parse_video_pass(r.stdout, r.stderr) if info.get("video") else None
        if video is not None:
            video["ffmpeg_returncode"] = r.returncode
        audio = None
        if info.get("audio"):
            a = run(audio_pass_cmd(ffmpeg, src))
            audio = parse_audio_pass(a.stderr)
        frames = video.get("decoded_frames") if video else None
        loop = None
        if args.loop_check:
            if frames and frames >= 3:
                seam = parse_ssim_summary(run(seam_cmd(ffmpeg, src, frames)).stderr)
                consecutive = parse_ssim_stats(run(consecutive_cmd(ffmpeg, src, frames)).stdout) if frames <= 9000 else []
                loop = loop_verdict(seam, consecutive)
            else:
                loop = {"ok": False, "verdict": "not enough decoded frames for a loop check"}
        sheet = None
        if sheet_path and frames:
            v = info.get("video") or {}
            width = args.tile_width or (200 if (v.get("height") or 0) > (v.get("width") or 0) else 320)
            cmd, idx = contact_cmd(ffmpeg, src, frames, sheet_path, args.cols, args.rows, width)
            c = run(cmd)
            sheet = {"path": str(sheet_path), "frames": idx, "ok": c.returncode == 0 and sheet_path.exists()}
        checks = build_checks(args, info, video, audio, loop)
        ok = all(c["ok"] for c in checks if c["severity"] == "error")
        report = {"input": src.name, "size_bytes": src.stat().st_size, "sha256": sha256(src), "probe": info,
                  "video": video, "audio": audio, "loop": loop, "contact_sheet": sheet, "checks": checks, "ok": ok,
                  "not_verified": ["viewing on the target display", "human listening", "player compatibility"]}
        text = json.dumps(report, indent=2, ensure_ascii=False)
        if report_path:
            report_path.write_text(text + "\n", encoding="utf-8")
        print(text)
        return 0 if ok else 1
    except UsageError as error:
        print(json.dumps({"ok": False, "error": str(error)}, indent=2))
        return 2


if __name__ == "__main__":
    sys.exit(main())
