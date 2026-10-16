#!/usr/bin/env python3
"""Calculate a camera-to-reference timing map from one or two reviewed anchors.

Standard library only. Does not inspect or modify media. JSON stdout; --out
creates a new file exclusively. A successful calculation is not verified sync.
"""
import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import re

MAX_BYTES = 64 * 1024
MAX_SECONDS = 24 * 60 * 60
DECIMAL = re.compile(r"\d+(?:\.\d+)?\Z", re.ASCII)
RATE = re.compile(r"\d+(?:\.\d+|/\d+)?\Z", re.ASCII)
FRAMES = re.compile(r"f(\d+)\Z", re.ASCII)


def strict_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON field")
        result[key] = value
    return result


def invalid_constant(_value):
    raise ValueError("Nonfinite JSON number")


def scalar(value, field):
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ValueError(f"{field} must be a number or numeric string")
    text = str(value)
    if len(text) > 48:
        raise ValueError(f"{field} is too long")
    return text


def rate(value, field):
    text = scalar(value, field)
    if not RATE.fullmatch(text):
        raise ValueError(f"{field} must be a positive decimal or fraction")
    try:
        number = Fraction(text)
    except (ValueError, ZeroDivisionError):
        raise ValueError(f"{field} is not a valid rate") from None
    if not 1 <= number <= 240:
        raise ValueError(f"{field} must be between 1 and 240 fps")
    return number


def seconds(value, fps, field):
    text = scalar(value, field)
    frame = FRAMES.fullmatch(text)
    if frame:
        number = Fraction(int(frame.group(1)), 1) / fps
    elif DECIMAL.fullmatch(text):
        number = Fraction(text)
    else:
        raise ValueError(f"{field} must be nonnegative decimal seconds or fN frames")
    if number > MAX_SECONDS:
        raise ValueError(f"{field} exceeds the 24-hour limit")
    return number


def fields(value, expected, label):
    if not isinstance(value, dict) or set(value) != set(expected):
        raise ValueError(f"{label} requires exactly these fields: {', '.join(expected)}")


def display(value):
    return round(float(value), 10)


def calculate(data, max_drift_ppm=1000):
    if (isinstance(max_drift_ppm, bool) or not isinstance(max_drift_ppm, (int, float))
            or not math.isfinite(max_drift_ppm) or not 0 <= max_drift_ppm <= 1_000_000):
        raise ValueError("max-drift-ppm must be finite and between 0 and 1000000")
    fields(data, ("schema", "reference_rate", "camera_rate", "anchors"), "Document")
    if type(data["schema"]) is not int or data["schema"] != 1:
        raise ValueError("Only schema 1 is supported")
    reference_rate = rate(data["reference_rate"], "reference_rate")
    camera_rate = rate(data["camera_rate"], "camera_rate")
    anchors = data["anchors"]
    if not isinstance(anchors, list) or len(anchors) not in (1, 2):
        raise ValueError("Provide one or two anchors")
    points = []
    for anchor in anchors:
        fields(anchor, ("reference", "camera"), "Anchor")
        points.append((seconds(anchor["reference"], reference_rate, "reference"),
                       seconds(anchor["camera"], camera_rate, "camera")))
    scale = Fraction(1)
    warnings = []
    estimated = len(points) == 2
    if estimated:
        dr, dc = points[1][0] - points[0][0], points[1][1] - points[0][1]
        if dr <= 0 or dc <= 0:
            raise ValueError("Both source positions must increase strictly between anchors")
        scale = dr / dc
    else:
        warnings.append("One anchor: scale assumed to be 1; drift is unknown.")
    offset = points[0][0] - scale * points[0][1]
    ppm = (scale - 1) * 1_000_000 if estimated else None
    if ppm is not None and abs(ppm) > Fraction(str(max_drift_ppm)):
        warnings.append("Drift exceeds the review threshold; verify anchors, rates and recording breaks.")
    return {
        "schema": 1,
        "ok": True,
        "kind": "anchor-calculation-not-sync-certification",
        "reference_rate": str(reference_rate),
        "camera_rate": str(camera_rate),
        "equation": "reference_seconds = scale * camera_seconds + offset_seconds",
        "scale_fraction": str(scale),
        "offset_fraction": str(offset),
        "scale": display(scale),
        "offset_seconds": display(offset),
        "offset_reference_frames": display(offset * reference_rate),
        "required_playback_speed_percent": display(100 / scale),
        "drift_estimated": estimated,
        "duration_scale_ppm": display(ppm) if ppm is not None else None,
        "review_threshold_ppm": max_drift_ppm,
        "anchors": [{"reference_s": display(r), "camera_s": display(c),
                     "mapped_reference_s": display(scale * c + offset),
                     "fit_residual_s": display(r - (scale * c + offset))} for r, c in points],
        "warnings": warnings,
        "limitations": [
            "Anchors are supplied by the operator; event identity and confidence are not measured.",
            "A zero fitting residual is construction, not independent validation.",
            "Check a separate middle event and every recording break; nonlinear drift is not modeled.",
            "No media, waveform, lip-sync, channel layout or plugin latency was inspected.",
            "No media was modified. Review timing, motion and sound before applying any correction.",
        ],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("anchors", type=Path, help="Local schema-1 anchor JSON, at most 64 KiB")
    ap.add_argument("--out", type=Path, help="NEW JSON output; parent directory must already exist")
    ap.add_argument("--max-drift-ppm", type=float, default=1000, help="Absolute duration-scale review threshold")
    args = ap.parse_args()
    try:
        with args.anchors.open("rb") as source:
            raw = source.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("Input exceeds the 64 KiB limit")
        data = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=strict_object,
                          parse_constant=invalid_constant, parse_float=str)
        result = calculate(data, args.max_drift_ppm)
        rendered = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
        if args.out:
            with args.out.open("x", encoding="utf-8", newline="\n") as output:
                output.write(rendered)
        print(rendered, end="")
    except (OSError, ValueError, UnicodeError, RecursionError) as error:
        ap.exit(2, f"sync_map: {error}\n")


if __name__ == "__main__":
    main()
