# Sources and provenance

## Personal skills

| Included path | Original source | Changes |
| --- | --- | --- |
| `skills/after-effects/ae-production-workflow/` | Existing personal `ae-production-workflow` skill, version 1.0.0 | Included all six files; replaced a project-specific example prefix with `<PROJECT>` (1.0.1). Moved under `skills/after-effects/` and added a related-skills section in 0.2.0 (1.0.2). Helper scripts unchanged. |
| `skills/market-research/` | [Cowgorithm research](https://github.com/Mbaka11/Cowgorithm/blob/c3ccfce39969a9bab8a181c387c137b365457c6c/skills/research/SKILL.md) | Added pi metadata; removed fixed geography, currency, hardware assumptions, and decision thresholds. |
| `skills/research-reporting/` | [Cowgorithm report-gen](https://github.com/Mbaka11/Cowgorithm/blob/c3ccfce39969a9bab8a181c387c137b365457c6c/skills/report-gen/SKILL.md) | Added pi metadata; generalized folders/audiences; no automatic message sending or scheduling. |
| `skills/backlog-execution/` | [Cowgorithm cron-tasks](https://github.com/Mbaka11/Cowgorithm/blob/c3ccfce39969a9bab8a181c387c137b365457c6c/skills/cron-tasks/SKILL.md) | Added pi metadata; clarified bounded on-demand scope; removed domain-specific backlog and messaging assumptions. |

The original personal skill and Cowgorithm files are not changed by this import.

### New personal skills (0.2.0)

Written for this toolbox from the owner's After Effects/LED production practice
and the 2026-10 research recorded in [the montage catalog](docs/montage-catalog.md).
No client names, project files or media are included.

| Included path | Notes |
| --- | --- |
| `skills/after-effects/ae-vox-editorial/` | Native AE recipes for the editorial collage look; palette defaults mirror common community practice |
| `skills/after-effects/ae-expressions-rigs/` | Expressions written for the AE JavaScript engine with index-based control access |
| `skills/after-effects/ae-vfx-compositing/` | Native-first compositing; model licences checked 2026-10 |
| `skills/montage/led-signage-content/` | Generic reference pixel maps, not device certification; confirm hardware dimensions and pitch before use. Text-size method from Nummax's published guide; `led_tool.py` is original |
| `skills/montage/video-delivery-qc/` | `media_qc.py` is original; platform figures from public platform/broadcast guidance |
| `skills/montage/sound-design-sfx/` | `sfx_place.py` is original; licence table from each provider's public terms |
| `skills/montage/montage-editing-craft/` | `srt_check.py` is original; presets resemble common French subtitle style guides |
| `skills/montage/vox-explainer-pipelines/` | Adapter for the vendored Vox snapshot below |

The collection is not an exhaustive backup of every agent package or historic
session; it includes the personal skills found in the inspected local locations.

### Additional personal montage skills (0.4.0)

Written for this toolbox, with public Adobe/FFmpeg documentation reviewed on
2026-10-16. Each skill links to its sources and distinguishes native workflows
from locally executed synthetic tests. Adobe direct fetches returned HTTP 403;
indexed documentation excerpts informed the version-dependent guidance.

| Included path | Scope and origin |
| --- | --- |
| `skills/montage/montage-colour-finishing/` | Original colour-pipeline and shot-matching workflow; synthetic RGB correction, not a log/HDR LUT |
| `skills/montage/montage-proxy-conform/` | Original ingest/proxy/conform workflow; no camera cards or client metadata |
| `skills/montage/montage-multicam-sync/` | Original `sync_map.py` rational anchor calculator; no waveform detection or third-party sync code |
| `skills/montage/montage-dialogue-cleanup/` | Original dialogue repair workflow; synthetic tone/noise test, no voice recording or cloning |
| `skills/montage/montage-time-remapping/` | Original timing and interpolation guidance; actual local FFmpeg speed changes |

PySceneDetect and OpenTimelineIO were reviewed as optional references, not
vendored or executed. The unlicensed `maxazure/video-editing-skill` remains a
catalog-only caution; none of its code, instructions or media is copied.
Full commits, licence findings and limits: [montage catalog](docs/montage-catalog.md).

### Editorial workflows and proxy audit (0.5.0)

Four original workflows: `montage-transcript-editing`, `montage-scene-selects`,
`montage-caption-accessibility` and `montage-archive-handoff`. Their references
link Adobe indexed documentation, FFmpeg, PySceneDetect and W3C guidance reviewed
2026-10-16. No upstream workflow text, detector implementation or recordings were
copied. `proxy_audit.py` is original standard-library code; it does not certify
native attachment, content identity or cadence. Supplied probe fixtures are
explicitly hand-authored illustrations, not captured ffprobe reports.

The separate CI media job uses distribution FFmpeg/ffprobe, DejaVu fonts and a
[PyPI Pillow 12.3.0](https://pypi.org/project/pillow/12.3.0/) CPython 3.11 Linux
x86_64 wheel (SHA-256 in `.github/media-requirements.txt`, licence MIT-CMU).
These are installed only in the explicitly configured CI environment, not
vendored or installed by package hooks. GitHub checkout/setup-node/setup-python
Node-24 actions are pinned by reviewed commits in the workflow.

## Original synthetic examples (0.3.0 through 0.5.0)

[examples/](examples/README.md) contains original procedural graphics, synthetic
sounds and fictitious reports, not imported client or upstream demo media.
`examples/build.py` uses local Pillow/FFmpeg and the toolbox's own helpers.
The [manifest](examples/manifest.json) records coverage, sizes and SHA-256 hashes;
[build info](examples/outputs/build-info.json) records the actual engine/font
versions. Font files are neither copied nor embedded. Native AE/Premiere, REA,
Remotion and cloud execution are not claimed. The examples retain the original
material's UNLICENSED policy; vendored MIT files remain byte-identical.
The 0.4.0 additions have a separate [build receipt](examples/outputs/montage-build-info.json)
and [decoded-media report](examples/outputs/montage-qc.json); existing 0.3.0
media and reports remain unchanged. Noise-interval measurements do not establish
natural speech quality, and the anchor calculator does not certify real-world sync.
The 0.5.0 [editorial build receipt](examples/outputs/editorial-build-info.json)
records a separate four-media-file batch. Transcript copy is fictional; scene
scores are measured from the actual encode; caption labels are authored, not
ASR/listening results. Archive restoration checks listed bytes, not an NLE
project. Older media, fixtures and reports are not replaced by this batch.

## Reverse-engineering sources

### REA

- Repository: https://github.com/morluto/rea
- Pinned npm version: `6.4.0`.
- Source commit: `a56f7bb668ab23fec8d33f7af353ac7ed2fe1895`.
- Package: https://registry.npmjs.org/rea-agents/-/rea-agents-6.4.0.tgz
- `vendor/rea/` contains only the release's original skill, six references, and
  MIT license. The published npm skill has metadata version **37**; it is not the
  newer main-branch skill observed during initial research.
- The archive's SHA-512 integrity was verified before extraction. Each included
  file has a SHA-256 in [tools/upstreams.lock.json](tools/upstreams.lock.json).
- `skills/rea-investigation/` is our separate pinning/privacy integration layer.

### Reverse API Engineer

- Repository: https://github.com/kalil0321/reverse-api-engineer
- Pinned reviewed release: `v0.14.0`.
- Commit: `ab9919b652eca1c7b323c3f7c7b37ded3cef12a0`.
- Inspiration: observe authorized traffic, infer the API contract, generate and
  verify a client. The upstream secret-hardcoding and reauthentication policy is
  expressly excluded. See [the review](tools/reverse-api-engineer/README.md).
- `skills/reverse-api-investigation/` and its helper are newly written, not an
  upstream code copy or an installed Python agent.

## Montage sources (vendored, unreleased snapshots)

### Vox editorial pipelines (Jared Cassoutt)

- Repository: https://github.com/jaredcassoutt/vox-editorial
- Snapshot of `main` at commit `f394e925f7ccbd6df3e6b3403fcb260194bbece3`
  (2026-09-02); no releases exist, so the commit is the pin.
- `vendor/vox-editorial/` holds the repository README and both skills'
  instructions, references, scripts, LICENSE and NOTICE, byte-identical to the
  upstream blobs. Excluded: demo media (`docs/`), the sample Remotion film
  (`example/`), and 24 MB of generated sprite PNGs with their manifest.
- `vox-editorial` itself records that it began as a fork of
  CK42BB/vox-explainer-skill (MIT) and was rewritten; see its NOTICE.
- Adapter: `skills/montage/vox-explainer-pipelines/`.

### Cinematic score and SFX (thenpceo)

- Repository: https://github.com/thenpceo/cinematic-score-and-sfx-skill
- Snapshot of `main` at commit `d48bb343ce087a76e04183a1344b915f269401ee`
  (2026-08-13).
- `vendor/cinematic-score-and-sfx/` holds SKILL.md, README.md and LICENSE,
  byte-identical. Excluded: SECURITY.md and `.gitignore`.
- Adapter: `skills/montage/sound-design-sfx/`.

File hashes for both are in [tools/upstreams.lock.json](tools/upstreams.lock.json).

Full source checkouts remain optional, separate, ignored, and pinned. Version
checking is read-only. See [maintenance](docs/maintenance.md).
