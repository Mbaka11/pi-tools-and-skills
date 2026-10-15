---
name: video-delivery-qc
description: Verify and package video deliverables by measuring the encoded file - full decode and frame count, size/fps/audio expectations, black and frozen segments, EBU R128 loudness and true peak, silence, LED loop-seam scoring, contact sheets from encoded frames, checksums - plus platform delivery specs (YouTube, Reels/TikTok, LinkedIn, Canadian broadcast, event playback, LED) and vetted FFmpeg recipes (H.264 web masters, ProRes, alpha WebM/ProRes 4444, GIF, loudness normalization). Use before sending any video to a client, uploading, or declaring a render finished.
compatibility: Python 3.9+ (standard library only). FFmpeg 4.4+ (5.1+ recommended) via $FFMPEG, PATH or the imageio-ffmpeg package; ffprobe optional.
metadata:
  version: "1.0.0"
  short-description: Decode-based QC and delivery specs for any montage
---

# Video delivery QC

[Tiny example — real decode report and contact sheet](../../../examples/README.md#video-delivery-qc).

The encoded file is the deliverable. AE or Premiere previews, render logs and
container durations are not proof. Decode the whole file, count frames, look at
frames extracted from the file, and measure the audio.

## Quick start

```bash
# Full QC with expectations, loop seam and a contact sheet
python scripts/media_qc.py deliver/CLIENT_PROMO_1920x1080_30p_v03.mp4 \
  --expect-width 1920 --expect-height 1080 --expect-fps 30 --expect-audio yes \
  --loudness-target -14 --true-peak-max -1 \
  --contact-sheet qc/sheet_v03.jpg --report qc/qc_v03.json

# LED loop: silent, exact size, seamless loop
python scripts/media_qc.py deliver/CLIENT_MSG_516x1032_30p_v01.mp4 \
  --expect-width 516 --expect-height 1032 --expect-fps 30 --expect-audio no --loop-check
```

`--dry-run` prints the FFmpeg passes without running them. Exit code 0 means
every error-level check passed; warnings and info entries still need a look.

## What the report proves (and what it does not)

| Proven by the report | Not proven |
| --- | --- |
| the file decodes end to end, with N frames and zero decoder errors | how it looks on the client's display or LED player |
| size, fps, audio stream presence match expectations | colour accuracy on an uncalibrated screen |
| black and frozen segments (timestamps) | that a frozen segment is unintended (holds are normal) |
| integrated loudness, LRA, true peak, silences | how the mix sounds — human listening is separate |
| loop seam behaves like a normal frame step | that the player loops without a gap |
| SHA-256 of the delivered bytes | rights and approvals |

Report the second column honestly as residual risk.

## Delivery workflow

1. **Specs first.** Pick the target in `references/platform-specs.md` (or the
   LED profile) and write the expectations down before encoding.
2. **Encode from a high-quality master** (ProRes/PNG/lossless from AE or
   Premiere) with a recipe from `references/ffmpeg-recipes.md`, or the LED tool.
3. **Run media_qc.py** with expectations; fix every failed error-level check.
4. **Look at the contact sheet** made from the encoded file; check first
   meaningful frame, text holds, the final frame.
5. **Listen** on headphones and on a small speaker when there is audio; state
   whether human listening happened.
6. **Name and checksum.** `CLIENT_PROJECT_FORMAT_WxH_FPSp_vNN.ext`; keep the QC
   JSON beside the file; for AE modules, also run ae-production-workflow's
   manifest verifier.
7. **Deliver** with a short note: what was verified, what was not, how to play
   it (loop, sound, aspect).

## Typical failures this catches

- One frame short (rounded durations, wrong frame rate interpretation).
- Black flash at the start or end of an LED loop (render range, transitions).
- Silent video delivered with an empty audio track (LED players may complain).
- Web delivery at −24 LUFS (broadcast mix) that sounds quiet on phones.
- Upscaled or letterboxed output from a wrong master size.
- Decoder errors from a broken render that the editor's preview hid.
