# Mix targets and practice

## Loudness targets (integrated, measured on the final file)

| Destination | Target | True peak |
| --- | --- | --- |
| Web, social, YouTube | about −14 LUFS | ≤ −1 dBTP |
| Podcasts | about −16 LUFS | ≤ −1 dBTP |
| Canadian broadcast (ATSC A/85; CRTC rule for commercials, broadcaster sheets for programs) | −24 LKFS | per sheet, commonly ≤ −2 dBTP |
| European broadcast (EBU R128) | −23 LUFS | ≤ −1 dBTP |
| Event playback (PA) | −16 to −14 LUFS, confirm with the AV team | ≤ −1 dBTP |
| LED roll-ups | no audio | — |

Measure with `media_qc.py` (EBU R128 integrated, LRA, true peak). Normalise the
mix with two-pass `loudnorm` (video-delivery-qc recipes) rather than limiting
everything to the ceiling.

## Balance

- Voice is the reference: dialogue/narration sits around −16 to −14 LUFS short
  term for web; everything else is placed relative to it.
- Music under voice: start 12–20 dB below the voice and duck 6–12 dB while the
  voice speaks; let it swell in gaps. Judge on a small speaker: music living
  mostly below 250 Hz disappears on phones.
- SFX: present but not louder than the voice; impacts may peak briefly above.
- Ambience: low, continuous, hides edits; fade at scene boundaries.

## Voice-over polish (typical chain)

High-pass ~80 Hz → gentle cut around 300–400 Hz if boxy → presence lift around
3 kHz → de-ess 5–8 kHz → 2:1–3:1 compression → limiter at the true-peak target.
Apply per voice and listen; numbers are starting points.

## Sync and editing

- Cut music on bar lines; make edits under a hit or a transient.
- Use real endings (the track's ending or a final hit), not fades, for
  confident outros.
- J/L cuts: let audio lead or follow the picture cut by 4–12 frames to smooth
  transitions.
- Keep SFX aligned to frames (`sfx_place.py --snap --fps`).

## Deliverables

- Review: MP4 with AAC 48 kHz stereo.
- Masters on request: stereo mix WAV 48 kHz/24-bit; stems DX/MX/SFX/AMB all
  zero-aligned and equal length; M&E (music and effects without dialogue) for
  localisation.
- Notes: loudness measured, human listening done or not, licence list.
