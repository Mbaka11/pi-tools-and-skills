# Generating and finding sounds

Order of preference: existing licensed library → quick self-recording →
generation. Generation is fast but costs credits and needs auditioning.

## Cloud providers (spend credits or money)

| Provider / model | Good for | Notes |
| --- | --- | --- |
| Higgsfield MCP audio models — Seed Audio 1.0 (default), Mirelo text-to-audio (SFX), Sonilo (music beds) | SFX, ambiences, Foley-like layers, short beds, when the Higgsfield MCP is connected | credits per generation; read the tool's current parameters (prompt, duration); commercial rights per plan |
| Higgsfield video models with audio (for example Seedance 2.0, Veo 3) | synchronized sound baked into generated clips | ask for Foley/ambience only, no music, when you plan your own score |
| ElevenLabs Sound Effects / Music API | precise SFX prompts, loops, durations; music with composition plans | needs `ELEVENLABS_API_KEY`; official agent skills: `elevenlabs/skills` (MIT) — install separately |

Prompting SFX: describe the physical source and texture, not the use:
"close-miked heavy rubber stamp hitting a wooden desk, short, dry, no reverb"
beats "impact for my logo". Ask for several short takes at once only when the
provider bills that cheaply; trim and fade every take.

## Local models (offline; check weight licences)

| Model | Use | Licence caution |
| --- | --- | --- |
| MMAudio | video-to-audio Foley from picture | code MIT, **weights CC BY-NC 4.0 → not for commercial deliverables** |
| HunyuanVideo-Foley | video/text-to-audio Foley | Tencent Hunyuan Community Licence: excludes EU, UK and South Korea; read all conditions before commercial use; heavy GPU needs |
| Stable Audio Open | text-to-audio SFX and textures | Stability AI Community Licence: commercial use allowed below its revenue threshold — verify current terms |

An 8 GB GPU limits model size and clip length; generate short one-shots and
layer them in the NLE.

## Searching a local library

- Name files descriptively (`stamp_thud_dry_01.wav`) and keep a `sources.csv`.
- Semantic search across a large library: `thedomid/sfx-finder` (MIT; CLAP
  embeddings locally, optional Freesound and ElevenLabs tiers) — install
  separately in its own Python environment; see the montage catalog.

## Audition checklist

- No clipping, clicks at start/end (add 2–10 ms fades), no baked reverb tail
  that fights the mix.
- Correct length for the picture event; tails do not cross the next cut unless
  intended.
- Consistent perspective: close sounds for close shots, distant for wide.
- Licence recorded.
