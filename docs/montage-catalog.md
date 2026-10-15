# Montage, After Effects, VFX and SFX tools: reviewed catalog

Research snapshot from **2026-10-14** for LED work (roll-ups, walls)
and general montage. Listing a project here is **not** an installation,
endorsement or licence grant. Commits are the revisions that were looked at;
review again before installing anything, and prefer that exact commit.

Legend — **Vendored**: pinned copy inside this toolbox (see
[SOURCES](../SOURCES.md)). **Recommended**: worth installing separately after
review. **Reference**: useful to read or for ideas. **Caution**: licence,
rights or conflict issue.

## Already in this setup

| Tool | What it adds | Notes |
| --- | --- | --- |
| Higgsfield bridge (`https://bridge.higgsfield.ai/mcp`) | `ae_*`, `pr_*`, `bl_*` tools; AE skills via `ae_get_skill` (`ae-clean-rig`, `ae-animation-principles`, `ae-depth-space`, `ae-transition-kit`…); Premiere skills via `pr_get_skill` | load `ae-clean-rig` first for AE; generation spends credits |
| Higgsfield MCP (`https://mcp.higgsfield.ai/mcp`, connect separately) | hosted workflows: `/vox-mixed-media`, `/paper-collage`, `/use-after-effects`, `/Shot-Composer`, `/Shot-Cleanup`, `/color-grading`, `/faceless-paper-diorama`…; image, video and audio models (Seed Audio, Mirelo, Sonilo) | credits; output rights per plan; less control over project structure |
| Photoshop MCP | still treatments (halftone, cleanup) for AE assets | — |

## Vox / editorial explainer pipelines

| Project | Commit | Licence | Engine | Verdict |
| --- | --- | --- | --- | --- |
| [jaredcassoutt/vox-editorial](https://github.com/jaredcassoutt/vox-editorial) — `vox-skill`, `vox-editorial` | `f394e925f7cc` | MIT (per skill) | Remotion; Python + FFmpeg; Higgsfield sprites | **Vendored** → [vox-explainer-pipelines](../skills/montage/vox-explainer-pipelines/SKILL.md) |
| [EricTechPro/vox](https://github.com/EricTechPro/vox) — `/vox-style` | `ecbeb32fc5d7` | none published | Higgsfield MCP end to end (~200–250 credits/min per its README) | **Reference** — no licence file, use from upstream only |
| [Alisa0808/vox-director](https://github.com/Alisa0808/vox-director) | `6a85a7c34161` | MIT | Atlas Cloud API + FFmpeg | Reference (paid API) |
| [CK42BB/vox-explainer-skill](https://github.com/CK42BB/vox-explainer-skill) | `7003225dc3ed` | MIT | Atlas Cloud (Seedream, Gemini, xAI TTS, MiniMax) | Reference (paid API) |
| [pyang5166/gbro-collage-broll](https://github.com/pyang5166/gbro-collage-broll) | `a1a4ee2e2abf` | MIT | halftone collage B-roll, Gemini generation | Reference |
| [Anil-matcha/vox-ai-motion-graphics-generator](https://github.com/Anil-matcha/vox-ai-motion-graphics-generator) | `c6856442a457` | none published | muapi, Veo | **Caution** — no licence |

The native After Effects route is the toolbox's own
[ae-vox-editorial](../skills/after-effects/ae-vox-editorial/SKILL.md).

## After Effects bridges and skills (alternatives to Higgsfield)

Run only **one** AE controller at a time (ae-production-workflow one-writer rule).

| Project | Commit | Licence | Notes | Verdict |
| --- | --- | --- | --- | --- |
| [JUNKDOGE-JOE/after-effects-mcp](https://github.com/JUNKDOGE-JOE/after-effects-mcp) | `3577303fc6bf` | MIT | CEP panel + MCP, previews, recovery | Reference |
| [yumehiko/ae-agent-skills](https://github.com/yumehiko/ae-agent-skills) | `760cc5b135a0` | MIT | AE extension + `ae-cli` + declarative scene skill | Reference |
| [Engine-Room-Games/after-effects-mcp](https://github.com/Engine-Room-Games/after-effects-mcp) | `97ec53c6e774` | MIT | MCP + bundled AE skill | Reference |
| [Arman-Luthra/aftr](https://github.com/Arman-Luthra/aftr) | `628397d700d6` | MIT | WebSocket CEP controller, render-review loop | Reference |
| [TheLlamainator/after-effects-mcp](https://github.com/TheLlamainator/after-effects-mcp) | `e4a462098d28` | MIT | bridge panel + JSX | Reference |
| [LobzyJay/motion-design-with-claude](https://github.com/LobzyJay/motion-design-with-claude) | `a4d48c55ccb5` | MIT | `motion-design`, `aftereffects-motion`, critique skills | **Reference, not vendored** — written for a different MCP; conflicts with the Higgsfield bridge's build doctrine and has dated render advice |
| [iart-ai/motion-design-skills](https://github.com/iart-ai/motion-design-skills) | `3c129f769d90` | MIT | AE hub: expressions, export, performance | **Reference, not vendored** — claims H.264 is absent from AE's Render Queue, which is outdated for current AE |

## Code-rendered motion and templates

| Project | Commit | Licence | Use | Verdict |
| --- | --- | --- | --- | --- |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | `8f0bcadcd328` | Apache-2.0 | HTML/CSS/GSAP → deterministic MP4, agent skills | Recommended for code-built promos |
| [remotion-dev/skills](https://github.com/remotion-dev/skills) | `7ba4dcf8ebe1` | no licence file; Remotion's own licence for the engine | official Remotion best-practice skills | Recommended with Remotion projects (check company licence) |
| [diffusionstudio/lottie](https://github.com/diffusionstudio/lottie) (`text-to-lottie`) | `3c72912fad54` | MIT | Lottie JSON authoring with a Skottie player | Recommended — pairs with the bridge's `ae_build_scene_from_lottie` |
| [digitalsamba/claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit) | `959e0fc6c202` | MIT | Remotion-based production toolkit | Reference |
| [Barty-Bart/motion-graphics](https://github.com/Barty-Bart/motion-graphics) | `3d83d987d658` | NOASSERTION | talking-head B-roll, SAM 2 object separation, measured sound pass | Caution — licence unclear |
| [imMamdouhaboammar/motion-graphics-skills](https://github.com/imMamdouhaboammar/motion-graphics-skills) | `29919c1ff91d` | NOASSERTION | 53 HyperFrames skills, SFX picker | Caution — licence unclear, 869 MB repo |
| [zhuyansen/awesome-claude-video-skills](https://github.com/zhuyansen/awesome-claude-video-skills) | `15e2f4bba750` | NOASSERTION | index of ~295 video skills with test results | Reference index |

## Sound and music

| Project | Commit | Licence | Use | Verdict |
| --- | --- | --- | --- | --- |
| [thenpceo/cinematic-score-and-sfx-skill](https://github.com/thenpceo/cinematic-score-and-sfx-skill) | `d48bb343ce08` | MIT | score-to-picture workflow, lock ledger, stems | **Vendored** → [sound-design-sfx](../skills/montage/sound-design-sfx/SKILL.md) |
| [elevenlabs/skills](https://github.com/elevenlabs/skills) | `32f48f6ebf4a` | MIT | official SFX, music, TTS, STT, voice isolator skills | Recommended if an ElevenLabs plan exists |
| [thedomid/sfx-finder](https://github.com/thedomid/sfx-finder) | `37a921817afe` | MIT | CLAP search of a local library, Freesound, ElevenLabs fallback | Recommended for large libraries (heavy Python deps) |
| [hkchengrex/MMAudio](https://github.com/hkchengrex/MMAudio) | `974010a026c7` | code MIT, **weights CC BY-NC** | video-to-audio Foley | Caution — not for commercial deliverables |
| [Tencent-Hunyuan/HunyuanVideo-Foley](https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley) | `df7b005b5023` | Tencent Hunyuan Community Licence | video-to-audio Foley | Caution — territory exclusions (EU/UK/KR) and conditions |
| Sonniss #GameAudioGDC bundles | — | royalty-free EULA | SFX library | Recommended (no AI training use) |

## VFX and AI assistance

| Project | Commit | Licence | Use | Verdict |
| --- | --- | --- | --- | --- |
| [Comfy-Org/comfy-mcp](https://github.com/Comfy-Org/comfy-mcp) | `1bbf3bb4487c` | NOASSERTION on GitHub | official MCP for local ComfyUI or Comfy Cloud | Recommended to drive the local ComfyUI — read its licence first |
| [sideshowroberto/vfx-agent-toolkit](https://github.com/sideshowroberto/vfx-agent-toolkit) | `9063d47135ce` | MIT | Nuke, Houdini, Unreal, Blender, ComfyUI plugins | Reference |

Model-weight licences (BiRefNet, RMBG-2.0, SAM 2, MatAnyone, Depth Anything V2,
RIFE, Real-ESRGAN, Wan) are summarised in
[ae-vfx-compositing](../skills/after-effects/ae-vfx-compositing/references/ai-assisted-vfx.md).

## Editing and Premiere

| Project | Commit | Licence | Use | Verdict |
| --- | --- | --- | --- | --- |
| [hetpatel-11/Adobe_Premiere_Pro_MCP](https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP) | `4ad1d9515ed8` | MIT | Premiere MCP | Reference (the bridge already covers Premiere) |
| [muhammaddadu/ffmpeg-skill](https://github.com/muhammaddadu/ffmpeg-skill) | `f6482b65e7cc` | MIT | FFmpeg recipes and production pipeline | Reference |

## LED signage references

- Nummax, *How to create effective content for your LED display* (text height =
  distance / 150 × movement coefficient) — basis of `led_tool.py text-size`.
- Q-lite, *Layout guidelines for graphic LED displays* (exact resolution, full
  pixels, light-on-dark, H.264, 25/30/60 fps progressive).
- NovaStar Taurus and Huidu A-series player specifications (H.264 decoding far
  above roll-up sizes; publishing tools may transcode).
- Generic reference pixel maps: 516×1032 per vertical panel, 1032×1032 or
  1548×1032 for two/three panels. These are examples, not universal standards;
  confirm the actual pixel pitch, cabinet size, mapping and player.

## Micro-examples for catalog-only tools

These are **illustrative output briefs**, not samples rendered by those tools.
They do not establish installation, runtime compatibility or commercial rights.
Actual original media and measured toolbox-helper results are in the
[short-example gallery](../examples/README.md). Follow each project's linked
README above for its own demonstrations; no external demo media is copied here.

| Catalog item | Very short example of the intended result |
| --- | --- |
| Higgsfield bridge | Editable 3 s AE title reveal or a Premiere three-shot cut. |
| Higgsfield MCP workflows | 3 s paper-collage clip from one brief, with separately approved credits. |
| Photoshop MCP | One still treated with two-colour halftone for a collage. |
| jaredcassoutt/vox-editorial | Question → evidence card → answer, timed to narration. |
| EricTechPro/vox | One hosted editorial shot mixing a cutout and caption. |
| Alisa0808/vox-director | One narrated explainer beat assembled from generated elements. |
| CK42BB/vox-explainer-skill | One cut-paper scene with a synchronised voice line. |
| pyang5166/gbro-collage-broll | 3 s halftone collage insert over a talking-head edit. |
| Anil-matcha/vox-ai-motion-graphics-generator | One generated documentary-style motion shot. |
| JUNKDOGE-JOE/after-effects-mcp | Create a title layer and inspect a preview frame. |
| yumehiko/ae-agent-skills | Declarative title card with editable layers. |
| Engine-Room-Games/after-effects-mcp | Short AE shape-and-text animation. |
| Arman-Luthra/aftr | Render-review-adjust cycle on a 3 s title. |
| TheLlamainator/after-effects-mcp | JSX-driven text reveal with a local preview. |
| LobzyJay/motion-design-with-claude | Three-second lower third plus a design critique. |
| iart-ai/motion-design-skills | Reusable title rig and a delivery checklist. |
| heygen-com/hyperframes | HTML/CSS card turns into a 3 s MP4 promo. |
| remotion-dev/skills | Typed composition with three timed title beats. |
| diffusionstudio/lottie | Tiny looping checkmark in Lottie JSON. |
| digitalsamba/claude-code-video-toolkit | Code-built montage with a title and captions. |
| Barty-Bart/motion-graphics | Subject cutout in front of an editorial title. |
| imMamdouhaboammar/motion-graphics-skills | HTML motion card with a selected transition sound. |
| zhuyansen/awesome-claude-video-skills | Shortlist of three skills for a given visual task; index, not renderer. |
| thenpceo/cinematic-score-and-sfx-skill | Three-event cue plan, stems and a handoff note. |
| elevenlabs/skills | One approved 1 s whoosh or a short music cue. |
| thedomid/sfx-finder | Top three locally matched sounds for “soft paper slide”. |
| hkchengrex/MMAudio | Short Foley bed for a test video, non-commercial weights caveat. |
| Tencent-Hunyuan/HunyuanVideo-Foley | Foley timed to one test action, subject to territory/licence limits. |
| Sonniss bundles | One licensed impact selected for a cut; no standalone sample redistribution. |
| Comfy-Org/comfy-mcp | Run an approved local matting workflow on one test frame. |
| sideshowroberto/vfx-agent-toolkit | Prepare a one-shot compositing scene in a supported host. |
| hetpatel-11/Adobe_Premiere_Pro_MCP | Three clips assembled with one J-cut. |
| muhammaddadu/ffmpeg-skill | Three-second clip encoded to the requested dimensions. |
| Nummax text-height method | At 4 m and P1.86, compute an 18 px minimum detail cap height. |
| Q-lite layout guidance | One high-contrast message, exact pixel map, no fractional-pixel strokes. |
| NovaStar Taurus / Huidu player references | On-device playback check of a 3 s test card; no device certification implied. |

## Installing a catalog item in pi (after review)

1. Clone or download the exact commit into a reviewed folder outside this
   repository.
2. Add the skill folder to pi's `skills` setting, or copy a single reviewed
   skill folder into `~/.pi/agent/skills/`. Use `pi config` to check names do
   not collide.
3. Install runtime dependencies inside that tool's own environment, never
   globally from a skill's instructions.
4. MCP servers: add them through the MCP adapter configuration with approvals
   kept on; never paste tokens into skills or repositories.
