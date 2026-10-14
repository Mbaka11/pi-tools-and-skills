# Platform delivery specs

Specs change; treat these as defaults verified during the toolbox's 2026
research and confirm against the platform's current help page or the client's
technical sheet for anything contractual.

## Web and social

| Target | Frame | Video | Audio | Loudness | Notes |
| --- | --- | --- | --- | --- | --- |
| YouTube (SDR) | 1920×1080 or 3840×2160, native fps | H.264 High, 4:2:0, progressive, closed GOP ≈ half the frame rate, MP4 with moov at the front; ~8 Mbit/s at 24–30 fps 1080p, ~12 Mbit/s at 48–60 fps | AAC-LC 48 kHz stereo, 384 kbit/s | about −14 LUFS integrated, TP ≤ −1 dBTP | YouTube normalises playback loudness downward |
| Instagram Reels / Facebook Reels | 1080×1920 (9:16) | H.264, 30 fps typical | AAC 48 kHz | about −14 LUFS | UI covers top and bottom: keep text out of roughly the top 250 px and bottom 420–670 px, and the right ~120 px (icons) |
| TikTok | 1080×1920 | H.264 | AAC | about −14 LUFS | similar overlays to Reels; captions recommended (sound-off viewing) |
| LinkedIn feed | 1920×1080, 1080×1080 or 1080×1350 | H.264 | AAC | about −14 LUFS | square or 4:5 takes more feed space; captions recommended |
| Website hero / background | 1920×1080 (or 1280×720) | H.264, no audio, short loop, small file | none | — | `-an`, faststart, consider a WebM VP9 alternative |

Safe zones for vertical video vary by placement and app version: upload a test
with a guide overlay or compare with a current screenshot of the interface.

## Broadcast and events

| Target | Typical spec | Loudness |
| --- | --- | --- |
| Canadian TV | per broadcaster sheet; commonly 1920×1080, 29.97 fps (interlaced or progressive per sheet), ProRes 422 HQ or XDCAM HD 50 | **−24 LKFS** (ATSC A/85 — the CRTC requires it for commercials and broadcasters' sheets apply it to programs), true peak typically ≤ −2 dBTP |
| European broadcast | per sheet | −23 LUFS (EBU R128), TP ≤ −1 dBTP |
| Event playback from a laptop or media server | native resolution and frame rate of the show system; ProRes 422 HQ or high-bitrate H.264; constant frame rate | −16…−14 LUFS with headroom; confirm with the AV technician |
| LED roll-ups and walls | see led-signage-content profiles; exact pixel map, H.264 High yuv420p 30 fps CFR, no audio | none |

## Audio-only

| Target | Loudness |
| --- | --- |
| Podcasts | about −16 LUFS integrated, TP ≤ −1 dBTP |
| Music streaming references | about −14 LUFS integrated |

## Checks before any upload

- Exact frame size and pixel aspect 1:1 (`setsar=1`).
- Constant frame rate matching the master.
- BT.709 colour tags for HD/4K SDR.
- Progressive unless the broadcaster sheet requires interlaced.
- Burned-in captions only when the brief asks; otherwise a separate SRT.
- Loudness measured on the final file, not on the timeline.
