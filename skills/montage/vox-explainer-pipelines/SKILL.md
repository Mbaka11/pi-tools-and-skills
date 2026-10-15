---
name: vox-explainer-pipelines
description: Choose and run code-rendered or generated Vox-style explainer pipelines - the pinned MIT vox-skill (Remotion paper-collage film re-timed from the voice-over, code-drawn charts, halftone cut-outs, music bed and ducking scripts) and vox-editorial (vertical cut-paper multiplane films with Python + FFmpeg and Higgsfield sprites), plus hosted Higgsfield workflows (/vox-mixed-media, /paper-collage) and other community pipelines - with Windows, licensing, credit and LED-format adaptations. Use for one-topic-to-film explainers, narrated documentary shorts, or when an editable AEP is not required; use ae-vox-editorial for native After Effects builds.
compatibility: Route B needs Node.js 22+, npm and Python 3 (Remotion is installed per project, never by this toolbox). Route C needs Python 3 with numpy and Pillow plus FFmpeg; sprite generation uses the Higgsfield CLI or other Higgsfield tools and spends credits. macOS-only cut-out helpers have Windows substitutes listed below.
metadata:
  version: "1.0.0"
  upstream: "https://github.com/jaredcassoutt/vox-editorial"
  upstream-commit: "f394e925f7ccbd6df3e6b3403fcb260194bbece3"
---

# Vox explainer pipelines (code and generated)

[Tiny example — 3 s beat-sheet mockup, not an upstream pipeline render](../../../examples/README.md#vox-explainer-pipelines).

This is a routing and adaptation guide. The two upstream skills are preserved
unchanged (MIT) in the pinned snapshot:

- [vox-skill — Remotion paper B-roll](../../../vendor/vox-editorial/skills/vox-skill/SKILL.md)
- [vox-editorial — Python/FFmpeg multiplane](../../../vendor/vox-editorial/skills/vox-editorial/SKILL.md)
- [overview of both](../../../vendor/vox-editorial/README.md)

For an editable After Effects project, use
[ae-vox-editorial](../../after-effects/ae-vox-editorial/SKILL.md) instead.

## Choose the route

| Route | Output | Strength | Cost / limits |
| --- | --- | --- | --- |
| **B. vox-skill (Remotion)** | 1920×1080 or 1080×1920 MP4; React project | narration drives every cue; code-drawn maps, charts, documents; tunable props in Remotion Studio | Remotion licence terms; Node project per film; client edits need a developer or Studio |
| **C. vox-editorial (Python)** | vertical 1080×1920 MP4 | generated subject sprites composed across depth planes; local assembly | sprite generation spends Higgsfield credits; less editable than AE |
| **D. Hosted** | MP4 from a provider | fastest from one prompt | least control; credits; check output rights |
| **A. Native AE** (other skill) | editable AEP + MP4 | exact client copy, revisions, LED formats | most build effort |

Hosted and community options (catalogued, not vendored):

- Higgsfield MCP workflows: `/vox-mixed-media` (Editorial Motion Graphics),
  `/paper-collage` and `/use-after-effects`, `/faceless-paper-diorama`.
  Require the Higgsfield MCP connection (`https://mcp.higgsfield.ai/mcp`),
  spend credits.
- `EricTechPro/vox` — `/vox-style` on the Higgsfield MCP (no licence file in the
  repository: use it from upstream, do not copy it here).
- Pipelines on other paid APIs: `CK42BB/vox-explainer-skill`,
  `Alisa0808/vox-director` (Atlas Cloud), `Anil-matcha/vox-ai-motion-graphics-generator`
  (muapi), `sadekxD/vox-style-collage-video-skill` (Unsora MCP).
See the [montage tools catalog](../../../docs/montage-catalog.md) for pins and notes.

## Before running a vendored pipeline

1. **Copy, do not run in place.** Copy the chosen upstream folder into the
   project (for example `<project>/_pipeline/vox-skill/`). vox-editorial's
   `library/library.py` writes its manifest and sprites into its own folder;
   running it inside the installed toolbox would modify the pinned snapshot.
2. **Path substitution.** Upstream text uses `~/.claude/skills/vox-skill/`;
   read it as the copied folder. On Windows use `python` instead of `python3`
   and `.venv\Scripts\python` instead of `./.venv/bin/python`; run `.sh`
   scripts from Git Bash.
3. **Rights review.**
   - Narration: upstream defaults to `edge-tts`, an unofficial client of
     Microsoft Edge's Read Aloud service with unclear commercial rights. Use it
     for drafts and timing; for client delivery use a licensed voice (for
     example ElevenLabs through Higgsfield credits or a direct plan) or a human
     voice, then re-run the timing step.
   - Remotion is free for individuals and organisations of up to three people;
     larger for-profit organisations need a company licence — confirm who
     renders the film.
   - Portraits and archive images: public-domain or licensed only; record each
     source.
4. **Credits.** vox-editorial's `sprite_sheets.py` calls `higgsfield generate
   create …`. Quote the number of sheets and expected credits before running
   and get consent unless the user already authorised that batch.

## Windows substitutes

| Upstream piece | Status on Windows | Substitute |
| --- | --- | --- |
| `cutout.swift`, `subject_cutout.swift` (Apple Vision) | macOS only | Higgsfield Remove Background (credits), Photoshop Remove Background, or a local BiRefNet/SAM 2 workflow (see ae-vfx-compositing licences) |
| `scaffold.sh`, `mix_audio.sh` | need bash + FFmpeg | Git Bash; FFmpeg on PATH (or `$FFMPEG`) |
| `gen_vo.py` | Python + `edge-tts` package | install in a project virtual environment only after the rights decision |
| `halftone.py`, `score.py`, `pick_thumbnail.py`, `captions.py` | Python + Pillow/numpy | project virtual environment |

Install dependencies inside the project (virtual environment, local
`node_modules`), never globally from this toolbox.

## LED and other formats

- A 516×1032 roll-up is **1:2**, not 9:16. Confirm the actual device format.
  A 1080×1920 render cannot
  be scaled to 516×1032 without distortion or cropping.
- Route B: after scaffolding, set the composition to 516×1032 (or 1032×2064 and
  reduce exactly 2:1 with `led_tool.py export`), and recompute the dead zones —
  the TikTok safe areas do not apply; use the LED guides instead.
- Route C: change `W, H` in the copied `multiplane.py` and `scene_graph.py`
  to the device size (or an exact multiple) and re-check layouts.
- LED loops are silent: drop narration and music; on-screen text and reading
  holds carry the story (ae-vox-editorial narrative reference).
- Always finish with `led_tool.py check` and `media_qc.py --loop-check`.

## Quality gates (all routes)

- One checkable idea, hook and payoff, beats written before visuals.
- Numbers, quotes and claims verified and sourced; nothing invented for layout.
- Contact sheet of stills before the full render.
- Decode-based QC on the final file (video-delivery-qc); audio measured and
  auditioned when present.
