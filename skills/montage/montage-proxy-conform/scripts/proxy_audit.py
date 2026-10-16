#!/usr/bin/env python3
"""Read-only source/proxy metadata audit. No relink, conversion or media changes.

media mode requires separately installed ffprobe. json mode compares supplied
ffprobe-shaped snapshots and does not inspect media. Exit 0=metadata-compatible,
1=mismatch, 2=usage/probe error, 3=incomplete metadata. Never certifies attachment.
"""
import argparse
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

MAX_JSON = 1024 * 1024
MAX_STREAMS = 64
NUMBER = re.compile(r"[+-]?\d+(?:\.\d+|/\d+)?\Z", re.ASCII)


class AuditError(Exception):
    pass


def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise AuditError("Duplicate JSON field")
        result[key] = value
    return result


def nonfinite(_value):
    raise AuditError("Nonfinite JSON number")


def parse(raw):
    if len(raw) > MAX_JSON:
        raise AuditError("Probe JSON exceeds 1 MiB")
    try:
        data = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=pairs,
                          parse_constant=nonfinite, parse_float=str)
    except (ValueError, UnicodeError, RecursionError):
        raise AuditError("Invalid probe JSON") from None
    if not isinstance(data, dict) or not isinstance(data.get("streams"), list):
        raise AuditError("Probe JSON requires a streams array")
    if len(data["streams"]) > MAX_STREAMS or any(not isinstance(s, dict) for s in data["streams"]):
        raise AuditError("Invalid stream list or more than 64 streams")
    if "format" in data and not isinstance(data["format"], dict):
        raise AuditError("format must be an object")
    return data


def number(value, positive=False):
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        return None
    text = str(value)
    if len(text) > 64 or not NUMBER.fullmatch(text):
        return None
    try:
        n = Fraction(text)
    except (ValueError, ZeroDivisionError):
        return None
    if abs(n) > 10 ** 12 or (positive and n <= 0):
        return None
    return n


def integer(value):
    n = number(value, True)
    return int(n) if n is not None and n.denominator == 1 else None


def known(value):
    return value if isinstance(value, str) and value.strip() and value.lower() not in ("unknown", "n/a", "unspecified") else None


def duration(stream, document):
    direct = number(stream.get("duration"), True)
    if direct is not None:
        return direct
    ticks, base = integer(stream.get("duration_ts")), number(stream.get("time_base"), True)
    if ticks is not None and base is not None:
        return ticks * base
    # A container's duration can belong to another stream; do not substitute it.
    return None


def identifier(document, stream, names):
    values = set()
    for obj in (stream, document.get("format", {})):
        tags = obj.get("tags", {})
        if isinstance(tags, dict):
            for key, value in tags.items():
                if key.lower() in names and known(value) is not None:
                    values.add(value.strip())
    if len(values) != 1:
        return None
    value = next(iter(values))
    if names == {"timecode"} and not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d[:;]\d{2}", value, re.ASCII):
        return None
    return value


def rotation(stream):
    values = []
    tags = stream.get("tags", {})
    if isinstance(tags, dict) and "rotate" in tags:
        values.append(number(tags["rotate"]))
    side = stream.get("side_data_list", [])
    if not isinstance(side, list):
        return None
    for item in side:
        if isinstance(item, dict) and "rotation" in item:
            values.append(number(item["rotation"]))
    if not values:
        return Fraction(0)  # No declared rotation, not proof of pixel orientation.
    if any(v is None for v in values):
        return None
    values = {v % 360 for v in values}
    return next(iter(values)) if len(values) == 1 else None


def compare(source, proxy):
    checks = []

    def add(name, a, b, comparator=None, disclose=True):
        status = "unknown" if a is None or b is None else "pass" if (comparator(a, b) if comparator else a == b) else "fail"
        item = {"check": name, "status": status}
        if disclose:
            item.update(source=str(a) if isinstance(a, Fraction) else a,
                        proxy=str(b) if isinstance(b, Fraction) else b)
        else:
            item.update(source_known=a is not None, proxy_known=b is not None)
        checks.append(item)

    def streams(doc, kind):
        # Thumbnail/cover-art video streams are not the main picture.
        return [s for s in doc["streams"] if s.get("codec_type") == kind
                and not (kind == "video" and isinstance(s.get("disposition"), dict)
                         and s["disposition"].get("attached_pic") == 1)]

    av, bv = streams(source, "video"), streams(proxy, "video")
    checks.append({"check": "one_video_stream_each", "status": "pass" if len(av) == len(bv) == 1 else "fail",
                   "source": len(av), "proxy": len(bv)})
    if len(av) == len(bv) == 1:
        a, b = av[0], bv[0]
        ar, br = number(a.get("avg_frame_rate"), True), number(b.get("avg_frame_rate"), True)
        add("video.average_frame_rate", ar, br)
        add("video.decoded_frame_count", integer(a.get("nb_read_frames")), integer(b.get("nb_read_frames")))
        # Metadata durations are rounded. Counts still require exact equality.
        tolerance = min(Fraction(1, 100), Fraction(1, 2) / ar) if ar else Fraction(1, 1000)
        add("video.duration", duration(a, source), duration(b, proxy), lambda x, y: abs(x - y) <= tolerance)
        add("video.start_time", number(a.get("start_time")), number(b.get("start_time")), lambda x, y: abs(x - y) <= Fraction(1, 1000))
        aw, ah, bw, bh = [integer(s.get(k)) for s, k in [(a, "width"), (a, "height"), (b, "width"), (b, "height")]]
        raster_a, raster_b = ([aw, ah], [bw, bh]) if all((aw, ah, bw, bh)) else (None, None)
        add("video.uniform_integer_downscale", raster_a, raster_b,
            lambda x, y: Fraction(x[0], y[0]) == Fraction(x[1], y[1]) and x[0] >= y[0] and x[0] % y[0] == 0)
        add("video.sample_aspect_ratio", number(str(a.get("sample_aspect_ratio", "")).replace(":", "/"), True),
            number(str(b.get("sample_aspect_ratio", "")).replace(":", "/"), True))
        orders = {"progressive", "tt", "bb", "tb", "bt"}
        ao, bo = known(a.get("field_order")), known(b.get("field_order"))
        add("video.field_order", ao if ao in orders else None, bo if bo in orders else None, disclose=False)
        add("video.declared_rotation", rotation(a), rotation(b))
        add("video.timecode", identifier(source, a, {"timecode"}), identifier(proxy, b, {"timecode"}), disclose=False)
        add("video.reel_id", identifier(source, a, {"reel_name", "reel", "tape"}),
            identifier(proxy, b, {"reel_name", "reel", "tape"}), disclose=False)
    aa, ba = streams(source, "audio"), streams(proxy, "audio")
    add("audio.stream_count", len(aa), len(ba))
    for i, (a, b) in enumerate(zip(aa, ba)):
        for key in ("sample_rate", "channels"):
            add(f"audio[{i}].{key}", integer(a.get(key)), integer(b.get(key)))
        add(f"audio[{i}].channel_layout", known(a.get("channel_layout")), known(b.get("channel_layout")), disclose=False)
        add(f"audio[{i}].start_time", number(a.get("start_time")), number(b.get("start_time")), lambda x, y: abs(x - y) <= Fraction(1, 1000))
        add(f"audio[{i}].duration", duration(a, source), duration(b, proxy), lambda x, y: abs(x - y) <= Fraction(1, 100))
    failures = sum(c["status"] == "fail" for c in checks)
    unknowns = sum(c["status"] == "unknown" for c in checks)
    verdict = "mismatch" if failures else "incomplete" if unknowns else "metadata-compatible"
    return {"schema": 1, "verdict": verdict, "failures": failures, "unknowns": unknowns, "checks": checks,
            "policy": "Exact decoded counts/rates; uniform integer raster reduction; conservative metadata comparison.",
            "native_attachment_tested": False,
            "not_verified": ["frame-by-frame cadence/VFR", "visual content correspondence or pre-rotated pixels",
                             "audio content, sample-level sync or human listening", "native attachment/relink/export",
                             "rights, complete media integrity or all decoder errors"]}


def fingerprint(path):
    s = path.stat()
    return s.st_size, s.st_mtime_ns, s.st_ctime_ns


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_file(file, mode, exe, timeout):
    path = Path(file).resolve(strict=True)
    if not path.is_file() or path.stat().st_size == 0:
        raise AuditError("Input must be a nonempty regular file")
    before = fingerprint(path)
    if mode == "json":
        with path.open("rb") as f:
            raw = f.read(MAX_JSON + 1)
    else:
        with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
            command = [exe, "-v", "error", "-protocol_whitelist", "file", "-count_frames", "-show_streams",
                       "-show_format", "-of", "json", str(path)]
            result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, timeout=timeout)
            if result.returncode or stderr.tell():
                raise AuditError("ffprobe reported a probe/decode error; inspect the input privately")
            stdout.seek(0)
            raw = stdout.read(MAX_JSON + 1)
    data = parse(raw)
    info = {"kind": "provided-probe-json" if mode == "json" else "local-media", "bytes": before[0], "sha256": digest(path)}
    if fingerprint(path) != before:
        raise AuditError("Input changed during the audit")
    return data, info


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mode", choices=("media", "json"))
    ap.add_argument("source")
    ap.add_argument("proxy")
    ap.add_argument("--ffprobe", help="Explicit local executable; otherwise FFPROBE or PATH")
    ap.add_argument("--timeout", type=int, default=300, help="Per-probe timeout, 1..3600 seconds")
    ap.add_argument("--report", type=Path, help="NEW JSON file; existing files are never overwritten")
    args = ap.parse_args()
    try:
        if not 1 <= args.timeout <= 3600:
            raise AuditError("timeout must be between 1 and 3600 seconds")
        if args.report and (args.report.exists() or args.report.is_symlink()):
            raise AuditError("Report already exists")
        if Path(args.source).resolve() == Path(args.proxy).resolve():
            raise AuditError("Source and proxy must be separate inputs")
        exe = args.ffprobe or os.environ.get("FFPROBE") or shutil.which("ffprobe")
        if args.mode == "media" and (not exe or not shutil.which(exe)):
            raise AuditError("ffprobe unavailable; supply it separately or use explicit json mode. Nothing was installed.")
        source, si = load_file(args.source, args.mode, exe, args.timeout)
        proxy, pi = load_file(args.proxy, args.mode, exe, args.timeout)
        report = compare(source, proxy)
        report.update(mode=args.mode, media_inspected=args.mode == "media", inputs={"source": si, "proxy": pi})
        rendered = json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
        if args.report:
            with args.report.open("x", encoding="utf-8", newline="\n") as f:
                f.write(rendered)
        print(rendered, end="")
        return {"metadata-compatible": 0, "mismatch": 1, "incomplete": 3}[report["verdict"]]
    except AuditError as error:
        ap.exit(2, f"proxy_audit: {error}; no media was changed.\n")
    except (OSError, ValueError, subprocess.TimeoutExpired):
        # Do not echo raw probe errors, tags, paths or malformed input into logs.
        ap.exit(2, "proxy_audit: input/output unavailable or probe timed out; no media was changed.\n")


if __name__ == "__main__":
    raise SystemExit(main())
