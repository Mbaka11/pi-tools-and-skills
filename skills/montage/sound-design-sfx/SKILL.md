---
name: sound-design-sfx
description: Sound design for montages and motion graphics - decide whether a piece has sound (LED loops usually do not), spot sync events, build an SFX/ambience/music plan, source or generate effects with commercial-licence checks (Sonniss, Freesound CC0, Pixabay, BBC limits, Higgsfield audio models, ElevenLabs, local models), place cues frame-accurately into a zero-aligned stem with scripts/sfx_place.py, duck music under voice, hit loudness targets (web -14 LUFS, Canadian broadcast -24 LKFS) and deliver mixes and stems. Use for "SFX", "sound effects", "whoosh", "bruitage", "sound design", "music bed", "mix", "foley", or scoring a cut; for full original score-to-picture work it routes to the vendored cinematic-score-and-sfx workflow.
compatibility: Python 3.9+ and FFmpeg 5+ for scripts/sfx_place.py (FFmpeg via $FFMPEG, PATH or imageio-ffmpeg). Optional providers (Higgsfield credits, ElevenLabs API key) and local models are installed and authorised separately.
metadata:
  version: "1.0.0"
  short-description: Licensed, frame-accurate SFX and mixes for client montages
---

# Sound design and SFX

[Tiny example — original 3 s sweep, impact and chime, with cue report](../../../examples/README.md#sound-design-sfx).

Sound sells motion — when it exists. Decide first whether the deliverable
plays with sound, then design only the sounds that carry meaning.

## 0. Does it have sound?

| Deliverable | Default |
| --- | --- |
| LED roll-ups and walls at events | **silent**, no audio track (`-an`) unless the device has speakers and the brief asks |
| Social vertical video | designed for sound-off first (captions), sound adds punch |
| Web/YouTube, presentations | full mix: voice, music, SFX |
| Broadcast | to the broadcaster's sheet (−24 LKFS in Canada) |

For a silent LED piece, stop here: put the effort into motion timing and
reading holds instead.

## 1. Spot the picture

Watch the locked (or clearly provisional) cut and list events with frame
numbers. Copy `assets/cues.template.csv` into the project and fill it:

- **hard sync**: cuts, slams, impacts, text arrivals, logo hits, stamps;
- **soft events**: mood changes, reveals, section changes;
- **protected audio**: dialogue, interviews, approved music — never altered by
  the SFX pass.

Rules of thumb: a whoosh *peaks on* the cut (starts 5–10 frames before); an
impact lands on the contact frame; a riser ends on the downbeat or the cut; one
designed sound per meaningful event — not on every cut.

## 2. Source sounds with rights you can prove

Read `references/sources-and-licenses.md` before using any library or model
output in client work. Record every file's source, licence and URL in the cue
sheet or a `sfx_sources.csv` beside it. Avoid non-commercial licences (CC BY-NC,
BBC RemArc) for client deliverables.

Generation options (Higgsfield audio models, ElevenLabs, local models) and
their caveats: `references/generation-options.md`. Search an existing local
library first; generate last.

## 3. Place cues and render a stem

```bash
python scripts/sfx_place.py --cues sfx_cues.csv --video picture.mp4 --fps 30 --snap \
  --out SFX_stem_48k.wav --preview-out preview_sfx.mp4 --with-original --dry-run
python scripts/sfx_place.py --cues sfx_cues.csv --video picture.mp4 --fps 30 --snap \
  --out SFX_stem_48k.wav --preview-out preview_sfx.mp4 --with-original
```

The stem starts at 0, lasts exactly the programme length, 48 kHz/24-bit stereo
— drop it on a track in Premiere/AE at the head. Times accept seconds,
`HH:MM:SS.mmm`, `HH:MM:SS:FF` or `f375` frames.

## 4. Mix

- Levels and targets: `references/mix-targets.md` (web −14 LUFS integrated,
  true peak ≤ −1 dBTP; Canadian broadcast −24 LKFS).
- Music under voice: duck 6–12 dB while the voice speaks (Premiere through the
  bridge: `pr_duck_music`; otherwise sidechain or keyframes).
- Measure the final file: `python ../video-delivery-qc/scripts/media_qc.py
  final.mp4 --loudness-target -14 --true-peak-max -1`.
- Listen on headphones *and* a phone/laptop speaker. State whether human
  listening happened; a measurement is not an audition.

## 5. Deliver

Review mix in the MP4, plus on request: stereo mix WAV 48 kHz/24-bit, stems
(`DX`, `MX`, `SFX`, `AMB`), and a music/SFX source list. Broadcast music may
need a cue sheet for performing-rights reporting (SOCAN in Canada).

## Full score-to-picture jobs

For an original score with cue architecture, lock ledgers and NLE stem
handoff, read the vendored workflow
[cinematic-score-and-sfx](../../../vendor/cinematic-score-and-sfx/SKILL.md)
(MIT, pinned). Keep this skill's licence and loudness rules in force; the
vendored workflow's provider suggestions are not authorisations to spend.

## Editorial collage (Vox-style) palette

Paper rustle and slide, tape rip, scissors snip, marker squeak, pencil scribble,
typewriter keys and bell, stamp thud, camera shutter, page turn, map pin pop,
soft whoosh on camera pushes, low riser into the reveal. Keep them dry and
close-miked; the music bed carries the space.
