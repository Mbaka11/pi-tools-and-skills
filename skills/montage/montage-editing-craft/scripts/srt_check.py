#!/usr/bin/env python3
"""Check SRT subtitles: timing, overlaps, reading speed, line length and
French typography; optionally write a corrected copy of the French spacing.

Presets follow common professional guidance (42 characters per line and 17
characters per second resemble widely used French broadcast/streaming style
guides); adjust with options when a client's style sheet differs.

Never modifies the input. Exit 0 = no errors, 1 = errors found, 2 = usage.
"""
import argparse
import json
import re
import sys
from pathlib import Path

PRESETS = {
    "broadcast": {"max_chars": 42, "max_lines": 2, "max_cps": 17.0, "min_dur": 0.833, "max_dur": 7.0, "min_gap": 0.083},
    "social-landscape": {"max_chars": 42, "max_lines": 2, "max_cps": 17.0, "min_dur": 0.7, "max_dur": 6.0, "min_gap": 0.0},
    "social-vertical": {"max_chars": 32, "max_lines": 2, "max_cps": 17.0, "min_dur": 0.7, "max_dur": 5.0, "min_gap": 0.0},
}
TC = re.compile(r"(\d{1,2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{1,2}):(\d{2}):(\d{2})[,.](\d{3})")
TAGS = re.compile(r"<[^>]+>|\{\\[^}]*\}")
NBSP, NNBSP = "\u00a0", "\u202f"


class UsageError(Exception):
    pass


def seconds(h, m, s, ms):
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def parse_srt(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    cues = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [l for l in block.split("\n")]
        if not any(l.strip() for l in lines):
            continue
        tc_line = next((i for i, l in enumerate(lines) if TC.search(l)), None)
        if tc_line is None:
            raise UsageError(f"Block without a timecode near: {lines[0][:40]!r}")
        m = TC.search(lines[tc_line])
        idx = lines[0].strip() if tc_line == 1 else None
        cues.append({"index": idx, "start": seconds(*m.groups()[:4]), "end": seconds(*m.groups()[4:]),
                     "lines": [l for l in lines[tc_line + 1:]], "tc": lines[tc_line].strip()})
    if not cues:
        raise UsageError("No subtitles found.")
    return cues


def visible(line):
    return TAGS.sub("", line)


def french_issues(line, style):
    issues = []
    plain = visible(line)
    for m in re.finditer(r" ([:;!?»%$€])", plain):
        issues.append(("error", "breakable-space-before-punctuation", f"regular space before '{m.group(1)}' can wrap; use a no-break space"))
    for m in re.finditer(r"\d \d{3}(?!\d)", plain):
        issues.append(("error", "breakable-space-in-number", f"'{m.group(0)}' can split across lines; use a no-break space as thousands separator"))
    for m in re.finditer(r"« ", plain):
        issues.append(("error", "breakable-space-after-guillemet", "regular space after '«'; use a no-break space"))
    for m in re.finditer(r"(?<![\s\u00a0\u202f\d:/])(:)(?!\d|//)", plain):
        issues.append(("warning", "missing-space-before-colon", "French requires a no-break space before ':'"))
    if style == "fr-FR":
        for m in re.finditer(r"(?<![\s\u00a0\u202f!?;])([;!?])", plain):
            issues.append(("warning", "missing-space-before-punctuation", f"fr-FR style expects a narrow no-break space before '{m.group(1)}'"))
    if re.search(r"«(?![\u00a0\u202f ])", plain) or re.search(r"(?<![\u00a0\u202f ])»", plain):
        issues.append(("warning", "guillemet-spacing", "« and » need no-break spaces inside"))
    if "..." in plain:
        issues.append(("info", "ellipsis", "consider the single character '…'"))
    return issues


def fix_french(line, style, space):
    out = re.sub(r" ([:;!?»%$€])", space + r"\1", line)
    out = re.sub(r"(?<=\d) (?=\d{3}(?!\d))", space, out)
    out = re.sub(r"« ", "«" + space, out)
    out = re.sub(r"«(?![\u00a0\u202f ])", "«" + space, out)
    out = re.sub(r"(?<![\u00a0\u202f ])»", space + "»", out)
    out = re.sub(r"(?<![\s\u00a0\u202f\d:/<])(:)(?!\d|//)", space + r"\1", out)
    if style == "fr-FR":
        out = re.sub(r"(?<![\s\u00a0\u202f!?;<])([;!?])", space + r"\1", out)
    return out


def check(cues, rules, french=None):
    issues = []

    def add(cue_no, cue, severity, rule, detail):
        issues.append({"cue": cue_no, "index": cue["index"], "start": round(cue["start"], 3), "severity": severity, "rule": rule, "detail": detail})

    prev_end = None
    for n, c in enumerate(cues, start=1):
        dur = c["end"] - c["start"]
        text_lines = [visible(l) for l in c["lines"] if l.strip()]
        chars = sum(len(l) for l in text_lines)
        if dur <= 0:
            add(n, c, "error", "non-positive-duration", f"{c['tc']}")
            continue
        if prev_end is not None:
            if c["start"] < prev_end - 1e-6:
                add(n, c, "error", "overlap", f"starts {prev_end - c['start']:.3f}s before the previous subtitle ends")
            elif 0 < c["start"] - prev_end < rules["min_gap"] - 1e-6:
                add(n, c, "warning", "short-gap", f"gap {c['start'] - prev_end:.3f}s < {rules['min_gap']}s")
        prev_end = c["end"]
        if not text_lines:
            add(n, c, "warning", "empty", "no text")
            continue
        if len(text_lines) > rules["max_lines"]:
            add(n, c, "error", "too-many-lines", f"{len(text_lines)} lines > {rules['max_lines']}")
        for l in text_lines:
            if len(l) > rules["max_chars"]:
                add(n, c, "error", "line-too-long", f"{len(l)} chars > {rules['max_chars']}: {l[:60]!r}")
        if dur < rules["min_dur"] - 1e-6:
            add(n, c, "warning", "too-short", f"{dur:.3f}s < {rules['min_dur']}s")
        if dur > rules["max_dur"] + 1e-6:
            add(n, c, "warning", "too-long", f"{dur:.3f}s > {rules['max_dur']}s")
        cps = chars / dur
        if cps > rules["max_cps"] + 1e-6:
            add(n, c, "error" if cps > rules["max_cps"] * 1.25 else "warning", "reading-speed", f"{cps:.1f} cps > {rules['max_cps']}")
        if french:
            for l in c["lines"]:
                for severity, rule, detail in french_issues(l, french):
                    add(n, c, severity, rule, detail)
    return issues


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("srt")
    ap.add_argument("--preset", choices=sorted(PRESETS), default="broadcast")
    ap.add_argument("--max-chars", type=int)
    ap.add_argument("--max-lines", type=int)
    ap.add_argument("--max-cps", type=float)
    ap.add_argument("--french", choices=["fr-CA", "fr-FR"], help="check French typography (fr-CA accepts no space before ; ! ?)")
    ap.add_argument("--fix-french-out", help="write a copy with French spacing fixed (needs --french)")
    ap.add_argument("--space", choices=["nbsp", "narrow"], default="nbsp", help="U+00A0 (safe in most fonts) or U+202F")
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args(argv)
    try:
        src = Path(args.srt)
        if not src.is_file():
            raise UsageError("SRT file not found.")
        rules = dict(PRESETS[args.preset])
        for key in ("max_chars", "max_lines", "max_cps"):
            if getattr(args, key) is not None:
                rules[key] = getattr(args, key)
        text = src.read_text(encoding="utf-8-sig")
        cues = parse_srt(text)
        issues = check(cues, rules, args.french)
        fixed = None
        if args.fix_french_out:
            if not args.french:
                raise UsageError("--fix-french-out needs --french.")
            out = Path(args.fix_french_out)
            if out.resolve() == src.resolve():
                raise UsageError("Write the fixed copy to a new file.")
            if out.exists() and not args.overwrite:
                raise UsageError(f"Refusing to overwrite existing file: {out.name}")
            space = NNBSP if args.space == "narrow" else NBSP
            lines = text.replace("\r\n", "\n").split("\n")
            new = [l if (TC.search(l) or re.fullmatch(r"\s*\d+\s*", l)) else fix_french(l, args.french, space) for l in lines]
            out.write_text("\n".join(new), encoding="utf-8")
            fixed = {"path": str(out), "remaining": len([i for i in check(parse_srt("\n".join(new)), rules, args.french) if i["rule"].startswith(("breakable", "missing", "guillemet"))])}
        errors = sum(1 for i in issues if i["severity"] == "error")
        report = {"file": src.name, "preset": args.preset, "rules": rules, "french": args.french, "subtitles": len(cues),
                  "errors": errors, "warnings": sum(1 for i in issues if i["severity"] == "warning"), "issues": issues, "fixed_copy": fixed}
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 1 if errors else 0
    except (UsageError, UnicodeDecodeError) as error:
        print(json.dumps({"ok": False, "error": str(error)}, indent=2))
        return 2


if __name__ == "__main__":
    sys.exit(main())
