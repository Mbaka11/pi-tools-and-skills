---
name: montage-proxy-conform
description: Safe media ingest, proxies and online conform for editing - preserve card structure, verify copies, inventory frame rates/timecode/audio, distinguish proxy media from VFR-to-CFR working masters, attach and audit proxies, relink originals, and check interchange round trips. Use for ingest, rushes, proxies, offline/online editing, relink, missing media, phone VFR, mixed rates or conform. Never deletes camera cards or replaces originals automatically.
compatibility: Any NLE; Premiere proxy attachment is optional. FFmpeg/ffprobe and copy-verification tools are separate prerequisites, not installed by this skill.
metadata:
  version: "1.0.0"
  short-description: Verified ingest, proxy identity and original-media conform
---

# Montage proxy and conform

[Tiny example — a real source/proxy pair with decoded checks](../../../examples/README.md#montage-proxy-conform).

A proxy is an editing substitute tied to an original. It is not a new editorial
source, a review watermark export, or a license to discard camera media.

## Ingest safely

1. Inventory cards/drives, file counts, byte counts, camera IDs and recording
   notes. Preserve card folder structure and sidecars; duplicate names across
   cards must not collide.
2. Copy into a **new** project location. Verify destination files against source
   hashes with an appropriate copy tool; retain the verification report. Verify
   an independent backup before treating the card as expendable.
3. Never erase cards, move originals or rename source media automatically.
   Deletion needs separate explicit authorization, not an ingest checklist tick.
4. Record exact rational rates, durations, resolution, pixel aspect, rotation,
   field order, timecode/reel identity and audio stream/channel layouts. Unknown
   metadata stays unknown until checked; file creation time is not sync timecode.

## Decide the workflow before transcoding

| Need | Correct route |
| --- | --- |
| Heavy but well-behaved camera files | Attached proxies preserving the original time basis |
| VFR recording with sync/cadence problems | Reviewed CFR **working master**, then proxies from that master if needed |
| Mixed acquisition rates | Deliberate sequence-rate and retiming decision; do not force every source to one rate |
| Interlaced or telecined source | Identify field order/cadence first; do not blindly deinterlace |
| Slow-motion capture | Confirm capture versus playback metadata before proxy creation |

VFR cannot be established just by comparing `r_frame_rate` and `avg_frame_rate`.
Inspect decoded timestamps over the whole problematic clip. CFR conversion can
repeat/drop frames and changes source mapping; keep originals and a mapping
record. Recheck audio at the beginning, middle and end.

## Build and attach proxies

Prefer the NLE's matched proxy preset. Choose a divisible frame size and a codec
that improves editing on the actual machine (an intraframe proxy is often better
than another long-GOP H.264 file). Preserve duration, frame rate, fielding and
required audio-channel layout. Do not add `-r`, `-ac 2` or `-an` indiscriminately.

- Use a separate `PROXIES/` tree and stable original-to-proxy mapping.
- Test one clip from **every source/audio family** before batching.
- Attach as proxies, not as replacement originals. Avoid automatic relink by
  basename alone when camera cards reuse names.
- Toggle proxies and inspect first/middle/last frames, action and lip sync,
  rotation, reframing and colour interpretation.
- Keep source-media interpretation/audio mapping stable once attached; consult
  the installed Premiere version's restrictions before changing them.

## Online conform and delivery

Duplicate the sequence, bring originals online, verify source IDs/timecode and
check every offline item. Export from full-resolution media with proxy export
explicitly disabled. Spot-check source resolution and a detailed region in the
export; do not assume a monitor toggle controls every export path.

For XML/AAF/OTIO/EDL handoff, test a small round trip including transitions,
retimes, nested/multicam clips and audio channels. Supply a reference movie with
burned-in timeline timecode and a discrepancy list. Interchange does not promise
lossless effects or speed ramps; preserve the native project.

Finish with [video-delivery-qc](../video-delivery-qc/SKILL.md).
[Proxy audit and sources](references/proxy-audit.md).
