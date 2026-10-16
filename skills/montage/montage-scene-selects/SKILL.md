---
name: montage-scene-selects
description: Find and review shot-boundary candidates, create source-linked contact sheets and selects logs, and turn approved ranges into an edit brief. Covers FFmpeg scene-change scores, optional PySceneDetect, false positives from flashes/pans, fades and dissolves, source timebases and representative-frame review. Use for scene detection, shot logs, rushes, B-roll selects, contact sheets or finding cuts in a long recording. Candidates are not semantic scene labels or automatic editorial approval.
compatibility: FFmpeg 4.4+ for the simple local analysis recipe; PySceneDetect is an optional separately reviewed BSD-3-Clause tool, not installed or bundled. Python/Pillow only for gallery regeneration.
metadata:
  version: "1.0.0"
  short-description: Reviewed shot boundaries, contact sheets and selects logs
---

# Scene detection and selects

[Tiny example — actual local cut candidates and decoded contact sheet](../../../examples/README.md#montage-scene-selects).

A visual change detector proposes boundaries. It cannot decide whether a shot
is useful, whether a flash is a cut, or whether a claim shown in it is true.

## Prepare the analysis

Preserve the source, record its hash and exact time basis, and establish the
editorial objective. Decide whether you need hard cuts, fades, action peaks or
speaker turns; these are different detection problems. Put logs and thumbnails
in a new private analysis directory, not in the source folder or this toolbox.

## Candidate pass

For a local FFmpeg starting point:

```sh
ffmpeg -hide_banner -nostdin -i input.mp4 -an -vf "scdet=t=12,metadata=print" -f null -
```

`scdet` reports scores and crossing times in diagnostic output. Its threshold
uses **0–100**, not the 0–1 scale of `select`'s `scene` expression. Twelve is a
synthetic-example setting, not a production default. This command analyzes the
video but creates no cut files; diagnostics may contain private source paths.

For harder motion, consider separately installed PySceneDetect's adaptive
method. Record its exact version, detector settings and output; do not assume
all versions share CLI flags or default thresholds. See [methods and review](references/detectors-and-review.md).

## Review before making selects

1. Inspect frames immediately before/after each candidate at the source timebase.
2. Reject flashes, whip pans, exposure changes and screen animations mistaken
   for cuts. Add missed dissolves or subtle cuts manually.
3. Use start-inclusive/end-exclusive ranges. Preserve gaps and handles; never
   confuse a source timestamp with a timestamp in a trimmed proxy.
4. Pick representative frames inside each shot, avoiding black transition
   frames and occluded subjects. Show source ID plus time/frame on the sheet.
5. Log purpose, quality, rights, framing and keep/maybe/reject. A contact sheet
   does not replace motion, focus, audio or consent review.

## Handoff

Deliver a candidate list separately from the **approved** selects list, plus
thumbnails and unresolved issues. Keep source hashes and analysis settings so
that replacing media invalidates old findings. Route the approved ranges to
[montage-editing-craft](../montage-editing-craft/SKILL.md) or
[transcript editing](../montage-transcript-editing/SKILL.md).

Do not automatically split/delete original media, assign emotional meaning,
publish private thumbnails or turn detector scores into unsupported confidence
percentages. Decode-based QC remains separate from editorial review.
