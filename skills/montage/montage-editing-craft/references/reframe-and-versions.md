# Reframing and version management

## Aspect ratio matrix

| Version | Size | Use | Composition notes |
| --- | --- | --- | --- |
| 16:9 | 1920×1080 | YouTube, web, presentations, TV | master for most shoots |
| 9:16 | 1080×1920 | Reels, Shorts, TikTok, Stories | subject centred; text in the central safe zone |
| 1:1 | 1080×1080 | feeds | tighter framing |
| 4:5 | 1080×1350 | Instagram/LinkedIn feed | more vertical space than 1:1 |
| 1:2 LED | e.g. 516×1032 per screen (confirm hardware) | roll-ups | rebuild graphics at device size |
| 1:1 LED wall | 1032×1032 | two roll-ups | seam at x = 516 |
| 3:2 LED wall | 1548×1032 | three roll-ups | seams at x = 516 and 1032 |

## Reframing rules

- Reframe shot by shot (keyframed position/scale or the bridge's reframe on
  sequence creation); a single centre crop loses subjects.
- Re-lay out text and graphics per format; never scale a 16:9 title into 9:16.
- Shoot or select with vertical crops in mind when vertical is a main
  deliverable (wide framing with headroom).
- LED versions come from graphics rebuilt at device size, not from a downscaled
  1080×1920 export.
- After reframing, re-check every caption and lower third against the format's
  safe zone.

## Durations

Cut-downs (60 → 30 → 15 → 6 s) are new edits: re-pick the strongest moments
and keep the brand and call to action; do not just trim the end.

## Naming and version log

`CLIENT_PROJECT_FORMAT_WxH_FPSp_vNN.ext`, for example
`CLIENT_RECAP_9x16_1080x1920_30p_v02.mp4`.

Keep `VERSIONS.md` in the project:

| Version | Date | Changes | Files | QC | Sent |
| --- | --- | --- | --- | --- | --- |
| v01 | 2026-10-14 | first cut | 16x9, 9x16 | media_qc ok | yes (preview link) |
| v02 | 2026-10-16 | client notes round 1 (items 1–7) | 16x9, 9x16, LED 516x1032 | media_qc ok | — |

Never overwrite a sent version; increment. Archive the project with media,
fonts, music licences and the final QC reports.

## Deliverable matrix (fill per project)

| Deliverable | Size | fps | Duration | Audio | Captions | Codec | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Master 16:9 | 1920×1080 | 30 | 30 s | mix −14 LUFS | SRT sidecar | H.264 | |
| Reel 9:16 | 1080×1920 | 30 | 30 s | mix −14 LUFS | burned | H.264 | |
| LED roll-up | 516×1032 | 30 | 20 s loop | none | none | H.264 | |
