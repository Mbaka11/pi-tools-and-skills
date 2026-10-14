#!/usr/bin/env python3
"""Place sound effects on a timeline from a cue sheet and render one
zero-aligned SFX stem (WAV) for an NLE, AE or a final mix.

Cue sheet CSV columns (header required; only time and file are mandatory):
  time        seconds (12.5), timecode (00:00:12.500 or 00:00:12:15 with --fps), or frames (f375)
  file        audio file, relative to the CSV folder or absolute
  gain_db     default 0
  fade_in     seconds, default 0
  fade_out    seconds, default 0
  trim_start  seconds into the source file, default 0
  length      seconds of source to use (default: to the end)
  label       free text for the report

Never overwrites outputs unless --overwrite; --dry-run prints the plan only.
FFmpeg 5+ via $FFMPEG, PATH or the imageio-ffmpeg package.
"""
import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

MAX_CUES = 100


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


def parse_time(text, fps=None):
    t = (text or "").strip()
    if not t:
        raise UsageError("Empty time value.")
    if re.fullmatch(r"f\d+", t):
        if not fps:
            raise UsageError(f"Frame time '{t}' needs --fps.")
        return int(t[1:]) / fps
    m = re.fullmatch(r"(\d+):(\d{2}):(\d{2})([.,]\d+)?", t)
    if m:
        frac = float(m.group(4).replace(",", ".")) if m.group(4) else 0.0
        return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3)) + frac
    m = re.fullmatch(r"(\d+):(\d{2}):(\d{2}):(\d{2})", t)
    if m:
        if not fps:
            raise UsageError(f"Timecode '{t}' with frames needs --fps.")
        ff = int(m.group(4))
        if ff >= fps:
            raise UsageError(f"Frame field in '{t}' exceeds fps.")
        return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3)) + ff / fps
    try:
        value = float(t)
    except ValueError:
        raise UsageError(f"Unrecognised time '{t}'.")
    if value < 0:
        raise UsageError("Times must be >= 0.")
    return value


def _num(row, key, default, lo, hi):
    raw = (row.get(key) or "").strip()
    if not raw:
        return default
    try:
        value = float(raw.replace(",", "."))
    except ValueError:
        raise UsageError(f"Column {key}: '{raw}' is not a number.")
    if not (lo <= value <= hi):
        raise UsageError(f"Column {key}: {value} outside {lo}..{hi}.")
    return value


def media_duration(path, ffmpeg):
    ffprobe = find_tool("ffprobe")
    if ffprobe:
        r = subprocess.run([ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        try:
            return float(r.stdout.strip())
        except ValueError:
            pass
    if ffmpeg:
        r = subprocess.run([ffmpeg, "-hide_banner", "-nostdin", "-i", str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace")
        m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", r.stderr)
        if m:
            return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    return None


def load_cues(csv_path, total, fps=None, snap=False, ffmpeg=None):
    base = Path(csv_path).resolve().parent
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not {"time", "file"} <= {h.strip() for h in reader.fieldnames}:
            raise UsageError("CSV needs a header with at least 'time' and 'file'.")
        rows = [{(k or "").strip(): (v or "") for k, v in row.items()} for row in reader]
    if not rows:
        raise UsageError("The cue sheet has no cues.")
    if len(rows) > MAX_CUES:
        raise UsageError(f"More than {MAX_CUES} cues: split them into several stems (for example SFX_A, SFX_B).")
    cues, warnings = [], []
    for n, row in enumerate(rows, start=2):
        try:
            t = parse_time(row["time"], fps)
            if snap:
                if not fps:
                    raise UsageError("--snap needs --fps.")
                t = round(t * fps) / fps
            if t >= total:
                raise UsageError(f"time {t:.3f}s is at or after the end ({total}s).")
            src = Path(row["file"].strip())
            src = src if src.is_absolute() else base / src
            if not src.is_file():
                raise UsageError(f"audio file not found: {row['file'].strip()}")
            cue = {
                "line": n, "label": row.get("label", "").strip(), "file": str(src), "time_s": round(t, 6),
                "gain_db": _num(row, "gain_db", 0.0, -60, 12), "fade_in": _num(row, "fade_in", 0.0, 0, 30),
                "fade_out": _num(row, "fade_out", 0.0, 0, 30), "trim_start": _num(row, "trim_start", 0.0, 0, 36000),
                "length": _num(row, "length", None, 0.01, 36000),
            }
        except UsageError as error:
            raise UsageError(f"Cue sheet line {n}: {error}")
        if fps:
            cue["frame"] = round(cue["time_s"] * fps, 3)
        if cue["fade_out"] and cue["length"] is None:
            d = media_duration(src, ffmpeg)
            if d is None:
                warnings.append(f"line {n}: fade-out skipped (source length unknown; add a 'length' column)")
                cue["fade_out"] = 0.0
            else:
                cue["length"] = max(0.01, d - cue["trim_start"])
        if cue["length"] is not None and cue["fade_in"] + cue["fade_out"] > cue["length"]:
            warnings.append(f"line {n}: fades longer than the clip; shortened")
            scale = cue["length"] / (cue["fade_in"] + cue["fade_out"])
            cue["fade_in"], cue["fade_out"] = cue["fade_in"] * scale, cue["fade_out"] * scale
        end = cue["time_s"] + (cue["length"] or 0)
        if cue["length"] is not None and end > total:
            warnings.append(f"line {n}: cue runs past the end and will be cut at {total}s")
        cues.append(cue)
    return cues, warnings


def build_command(ffmpeg, cues, total, out, sr=48000, overwrite=False):
    args = [ffmpeg, "-hide_banner", "-nostdin", "-y" if overwrite else "-n"]
    for c in cues:
        args += ["-i", c["file"]]
    parts = []
    for i, c in enumerate(cues):
        chain = [f"atrim=start={c['trim_start']:g}" + (f":duration={c['length']:g}" if c["length"] is not None else ""),
                 "asetpts=PTS-STARTPTS", f"aresample={sr}", f"aformat=sample_fmts=fltp:sample_rates={sr}:channel_layouts=stereo"]
        if c["fade_in"]:
            chain.append(f"afade=t=in:st=0:d={c['fade_in']:g}")
        if c["fade_out"] and c["length"] is not None:
            chain.append(f"afade=t=out:st={max(0.0, c['length'] - c['fade_out']):g}:d={c['fade_out']:g}")
        if c["gain_db"]:
            chain.append(f"volume={c['gain_db']:g}dB")
        chain.append(f"adelay=delays={round(c['time_s'] * 1000)}:all=1")
        parts.append(f"[{i}:a]{','.join(chain)}[c{i}]")
    labels = "".join(f"[c{i}]" for i in range(len(cues)))
    mix = f"{labels}amix=inputs={len(cues)}:normalize=0:dropout_transition=0," if len(cues) > 1 else f"{labels}anull,"
    parts.append(f"{mix}apad=whole_dur={total:g},atrim=end={total:g}[mix]")
    args += ["-filter_complex", ";".join(parts), "-map", "[mix]", "-c:a", "pcm_s24le", "-ar", str(sr), str(out)]
    if sum(len(a) + 3 for a in args) > 30000:
        raise UsageError("Command line too long for Windows: split the cue sheet into several stems.")
    return args


def preview_command(ffmpeg, video, stem, out, with_original=False, overwrite=False):
    args = [ffmpeg, "-hide_banner", "-nostdin", "-y" if overwrite else "-n", "-i", str(video), "-i", str(stem)]
    if with_original:
        args += ["-filter_complex", "[0:a][1:a]amix=inputs=2:normalize=0:duration=first[a]", "-map", "0:v:0", "-map", "[a]"]
    else:
        args += ["-map", "0:v:0", "-map", "1:a:0", "-shortest"]
    return args + ["-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", str(out)]


def _new(path, overwrite):
    p = Path(path)
    if p.exists() and not overwrite:
        raise UsageError(f"Refusing to overwrite existing file: {p.name} (use --overwrite deliberately).")
    if not p.parent.exists():
        raise UsageError("Output folder does not exist.")
    return p


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--cues", required=True, help="cue sheet CSV")
    ap.add_argument("--duration", type=float, help="program length in seconds (or use --video)")
    ap.add_argument("--video", help="picture file; its duration sets the stem length")
    ap.add_argument("--out", required=True, help="output WAV stem")
    ap.add_argument("--fps", type=float, help="needed for frame times, HH:MM:SS:FF and --snap")
    ap.add_argument("--snap", action="store_true", help="snap cue times to whole frames")
    ap.add_argument("--sr", type=int, default=48000, choices=[44100, 48000, 96000])
    ap.add_argument("--preview-out", help="also write a review MP4 (needs --video)")
    ap.add_argument("--with-original", action="store_true", help="preview mixes the picture's own audio with the stem")
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    try:
        ffmpeg = find_tool("ffmpeg")
        if args.fps is not None and not (1 <= args.fps <= 120):
            raise UsageError("--fps must be between 1 and 120.")
        total = args.duration
        if total is None and args.video:
            if not Path(args.video).is_file():
                raise UsageError("Video file not found.")
            total = media_duration(args.video, ffmpeg)
        if not total or total <= 0:
            raise UsageError("Give --duration in seconds, or a readable --video.")
        if args.preview_out and not args.video:
            raise UsageError("--preview-out needs --video.")
        out = _new(args.out, args.overwrite)
        preview = _new(args.preview_out, args.overwrite) if args.preview_out else None
        cues, warnings = load_cues(args.cues, total, args.fps, args.snap, ffmpeg)
        exe = ffmpeg or "ffmpeg"
        command = build_command(exe, cues, total, out, args.sr, args.overwrite)
        result = {"stem": str(out), "duration_s": total, "sample_rate": args.sr, "cues": cues, "warnings": warnings,
                  "command": command, "preview": None}
        if preview:
            result["preview"] = {"path": str(preview), "command": preview_command(exe, args.video, out, preview, args.with_original, args.overwrite)}
        if args.dry_run:
            result["dry_run"] = True
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 0
        if not ffmpeg:
            raise UsageError("FFmpeg not found (set FFMPEG, add it to PATH, or pip install imageio-ffmpeg).")
        r = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
        result["returncode"] = r.returncode
        if r.returncode:
            result["stderr_tail"] = r.stderr[-1500:]
        elif preview:
            p = subprocess.run(result["preview"]["command"], capture_output=True, text=True, encoding="utf-8", errors="replace")
            result["preview"]["returncode"] = p.returncode
            if p.returncode:
                result["preview"]["stderr_tail"] = p.stderr[-1500:]
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if not r.returncode and not (preview and result["preview"].get("returncode")) else 1
    except UsageError as error:
        print(json.dumps({"ok": False, "error": str(error)}, indent=2))
        return 2


if __name__ == "__main__":
    sys.exit(main())
