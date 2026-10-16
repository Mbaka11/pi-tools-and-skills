---
name: montage-multicam-sync
description: Synchronize multicamera video and double-system sound before editing - choose timecode, slate or waveform anchors, distinguish fixed offset from clock drift, map camera time to a reference with scripts/sync_map.py, verify beginning/middle/end sync, preserve channel layouts and continuous master audio, and build reversible multicam sequences. Use for multicam, multi-camera interviews, podcasts, concerts, external recorders, sync offsets or drifting lip sync.
compatibility: Python 3.9+ standard library for the anchor calculator; no media engine needed. Native multicam editing requires a separately available NLE. The helper does not detect audio events or modify media.
metadata:
  version: "1.0.0"
  short-description: Evidence-based multicam offsets, drift and audio routing
---

# Montage multicamera synchronization

[Tiny example — calculate and apply a six-frame offset](../../../examples/README.md#montage-multicam-sync).

Sync first, cut second. Camera timestamps, timecode, genlock and matching frame
rates solve different problems; none alone proves that sound and picture align.

## Establish the reference

Inventory camera IDs, exact rates, recording breaks, timecode mode, audio tracks
and the best continuous recorder. Preserve original channels and files. Choose
a common reference timeline and document its zero; do not normalize every clip's
timecode independently and then pretend they share a clock.

Choose evidence in order of suitability, not prestige:

1. Trusted shared timecode with confirmed frame-rate/drop-frame interpretation.
2. A visible slate/transient paired with the same recorded sound.
3. Shared scratch audio aligned by the NLE, then checked manually.
4. Manually identified common events when no reliable shared audio exists.

Do not sync by filesystem date. Similar music patterns, applause and echoes can
produce false waveform matches. Timecode is not genlock; clocks can drift after
a successful start alignment. Drop-frame changes labels, not playback speed.

## Measure offset and drift

Mark one common event for a constant-offset estimate; use a second event far
later for a two-point linear drift estimate. Source positions must be measured
from each clip's first decoded frame/sample, not its timeline placement.

```sh
# Run from this skill folder; copy/edit the template in your project first.
python scripts/sync_map.py assets/anchors.example.json
python scripts/sync_map.py project-anchors.json --out sync-plan.json
```

The helper outputs `reference_seconds = scale * camera_seconds + offset` using
exact rational arithmetic. Positive offset places camera start later; negative
offset puts it before reference zero. The example yields **−0.2 s / −6 frames**.
It accepts decimal seconds or `fN` source-frame indices at each declared rate,
not SMPTE/drop-frame labels. See [the contract](references/sync-contract.md).

This is a **calculator**, not automated synchronization. It cannot assess event
identity, confidence, nonlinear clock drift, latency or missing frames. One
anchor cannot estimate drift. Two anchors are not a substitute for a third
independent check in the middle and checks across all recording breaks.

## Build and review the multicam source

- Duplicate the edit/project; preserve angle names and source references.
- In Premiere, use **Create Multi-Camera Source Sequence** with the chosen
  sync method. Discover installed controls/tools rather than inventing APIs.
- Preserve a continuous master dialogue/music track. Switch **picture only**
  unless an explicit audio-follow-video decision is required.
- Check channel order, phase/polarity and microphone delay. Do not sum duplicate
  scratch tracks with the master or flatten everything to stereo automatically.
- Test lip sync/transients at beginning, middle, end and every recording break.
  For drift, check the clock/rate explanation before any stretch or resampling.
- Apply only an approved correction on a copy. Retime linked video/audio
  consistently; sound quality and motion artifacts require playback review.

Keep multicam/nested sources editable. Flatten only a duplicate for a tested
handoff. Route story/pacing to [montage-editing-craft](../montage-editing-craft/SKILL.md),
cleanup to [montage-dialogue-cleanup](../montage-dialogue-cleanup/SKILL.md), and
exports to [video-delivery-qc](../video-delivery-qc/SKILL.md).
