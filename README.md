# Pi Tools & Skills

[![Version](https://img.shields.io/badge/version-0.5.0-blue)](https://github.com/Mbaka11/pi-tools-and-skills/releases/latest)
[![Checks](https://github.com/Mbaka11/pi-tools-and-skills/actions/workflows/check.yml/badge.svg)](https://github.com/Mbaka11/pi-tools-and-skills/actions/workflows/check.yml)

A personal, cross-project collection of reusable [pi](https://github.com/earendil-works/pi) skills, small offline helpers, pinned reverse-engineering tool references, and an After Effects / montage toolbox for LED-signage and video work.

**Twenty-three skills · No automatic tool installation · No credentials or project data**

**[Browse the short-example gallery](examples/README.md)** — 3-second animations,
audio, actual helper outputs and fictitious mini-reports. Every included skill
and tool has an example with clearly stated limitations.

Documentation is written in English. Quoted source text and language-specific
examples retain their original wording.

This is a toolbox, not an ApplyPilot dependency and not a backup of an entire pi
profile. It contains reusable instructions and helpers, not browser sessions,
model authentication, private captures, or previous project deliverables.

## Included skills

Skills live in `skills/`; related skills are grouped in category folders
(`skills/after-effects/`, `skills/montage/`), which pi discovers recursively.

### After Effects — `skills/after-effects/`

| Skill | Use | Origin |
| --- | --- | --- |
| `ae-production-workflow` | Reversible After Effects production, checkpoints, RAM gates, native QA, delivery verification | Existing personal skill, with its scripts and templates |
| `ae-vox-editorial` | Vox-style editorial collage (paper, cut-outs, halftone, highlights, maps, multiplane) built natively and editably in AE | New personal skill |
| `ae-expressions-rigs` | Vetted expressions, CTRL rigs, auto-sizing boxes, French price formatting, LED-safe layout, Essential Properties/MOGRT | New personal skill |
| `ae-vfx-compositing` | Keying, roto, cleanup, tracking, screen/LED mockups, integration QA, AI options with licence checks | New personal skill |

### Montage — `skills/montage/`

| Skill | Use | Origin |
| --- | --- | --- |
| `led-signage-content` | Generic LED roll-ups (e.g. 516×1032) and walls: profiles, text size from pitch and distance, guides, exports, per-screen splits, test cards | New personal skill + `led_tool.py` |
| `video-delivery-qc` | Decode-based QC: frames, black/freeze, loudness, loop seam, contact sheets; platform specs; FFmpeg recipes | New personal skill + `media_qc.py` |
| `sound-design-sfx` | Spotting, licensed SFX/music, generation options, frame-accurate cue stems, mix targets | New personal skill + `sfx_place.py`; routes to a vendored score-to-picture workflow |
| `montage-editing-craft` | Edit workflow, pacing, Premiere via the Higgsfield bridge, reframes, versions, French captions and client notes | New personal skill + `srt_check.py` |
| `vox-explainer-pipelines` | Pinned Remotion and Python Vox pipelines plus hosted options, with Windows, licence and LED adaptations | Personal adapter + unchanged MIT upstream snapshot |
| `montage-colour-finishing` | Colour management, input/output transforms, scopes, shot matching and export consistency | Original workflow + synthetic RGB correction example |
| `montage-proxy-conform` | Verified ingest, proxies, VFR decisions, relink and online/interchange checks | Original workflow + read-only `proxy_audit.py` |
| `montage-multicam-sync` | Reviewed anchors, fixed offset/drift, reversible multicam and continuous master audio | Original workflow + `sync_map.py` |
| `montage-dialogue-cleanup` | Conservative repair, gain, room tone, enhancement limits and dialogue-stem QA | Original workflow + actual synthetic noise filter test |
| `montage-time-remapping` | Source/output timing, slow motion, speed ramps, interpolation and artifact review | Original workflow + actual piecewise-speed example |
| `montage-transcript-editing` | Source-linked paper edits, radio cuts and meaning preservation | Original workflow + fictional cut map |
| `montage-scene-selects` | Shot-boundary candidates, contact sheets and reviewed selects | Original workflow + actual local cut detection |
| `montage-caption-accessibility` | Meaningful sound/speaker captions, localization and player checks | Original workflow + English/French SRT/WebVTT examples |
| `montage-archive-handoff` | Dependency inventory, collection, hashes and isolated restoration | Original workflow + actual four-file restore |

### Research and investigation — `skills/`

| Skill | Use | Origin |
| --- | --- | --- |
| `market-research` | Sourced market sizing, competition, regulations, and opportunity comparisons | Generalized from personal Cowgorithm research skill |
| `research-reporting` | Briefs, executive summaries, full reports, and reviewed PDF exports | Generalized from personal Cowgorithm report skill |
| `backlog-execution` | Bounded on-demand task execution and evidence-based completion | Generalized from personal Cowgorithm task reference |
| `rea-investigation` | Authorized artifact and passive runtime investigation using REA | Personal adapter + unchanged matching upstream skill snapshot |
| `reverse-api-investigation` | Reviewed network evidence → endpoint map → testable client, without embedded secrets | pi-native workflow inspired by Reverse API Engineer |

Original sources and exact revisions: [SOURCES.md](SOURCES.md).
Other installed third-party skills are listed in [the external catalog](docs/external-skills.md), not copied or presented as personal creations.
Researched After Effects, Vox, motion, SFX, VFX and editing tools (with pins, licences and verdicts) are in [the montage tools catalog](docs/montage-catalog.md).

## Short examples

[![Original editorial-collage mockup, 3 seconds](examples/media/ae-vox.gif)](examples/README.md#ae-vox-editorial)

[Full gallery: all 23 skills](examples/README.md) ·
[One micro-example per included tool](examples/tools.md).
Original synthetic media only. AE previews are explicitly labelled mockups;
LED, QC, SFX, subtitle, sync and manifest examples include actual helper outputs.
The new colour, proxy, cleanup and retiming examples execute local filters;
they do not claim native Adobe tests, calibrated colour or human voice quality.
Editorial examples add real cut candidates, caption timing and byte restoration;
the transcript is fictional and accessibility/native restoration are not certified.

## Recover on another machine

Requires pi and Git. For an immutable version:

```bash
pi install git:github.com/Mbaka11/pi-tools-and-skills@v0.5.0
```

Restart pi or run `/reload`. Skills are registered at **user scope**, so they are
available across projects. Dependencies such as REA, After Effects, Python,
FFmpeg, or browser tooling are **not** installed or activated by this command.

Alternatively, clone an editable copy:

```bash
git clone https://github.com/Mbaka11/pi-tools-and-skills.git
cd pi-tools-and-skills
npm test
pi install .
```

`npm test` requires Node.js 22.19+ and Python 3.9+; it installs nothing. Node 24 LTS
is recommended. Windows-specific checkpoint tests also use PowerShell. There are
no npm dependencies and no package install hooks. Optional media tests may skip
in this lightweight suite. `npm run test:media` instead **requires** FFmpeg,
ffprobe, Pillow and a local font; missing prerequisites fail immediately. The
separate Ubuntu media CI installs its declared dependencies explicitly, not on
your machine. See [the test matrix](docs/maintenance.md#test-matrix).

If `ae-production-workflow` already exists as a standalone personal skill, review
which copy should stay enabled with `pi config`. Disable the old resource before
loading the package copy; do not keep two skills with the same name active.
Keep a backup outside pi's scanned skill directories before any migration.

This repository's creation does not modify any current pi installation.

## Use a skill

Ask pi normally, or select a workflow explicitly:

```text
/skill:market-research Compare the market for this product in the agreed region.
/skill:research-reporting Create an executive summary from these reviewed findings.
/skill:backlog-execution Complete the three authorized tasks in this project plan.
/skill:rea-investigation Explain this owned Electron package's import flow.
/skill:reverse-api-investigation Map the API from this reviewed test capture.
/skill:ae-production-workflow Preflight the current AE project without changing it.
/skill:ae-vox-editorial Build a 20 s Vox-style loop for a 516x1032 roll-up from this brief.
/skill:led-signage-content Check this export for a three-screen LED wall.
/skill:video-delivery-qc Verify the final MP4 before sending it to the client.
/skill:sound-design-sfx Spot this cut and place whooshes and hits on the cuts.
/skill:montage-colour-finishing Match the two cameras without double-applying a LUT.
/skill:montage-proxy-conform Prepare proxies and audit the original-media relink.
/skill:montage-multicam-sync Calculate the offset from these two reviewed slates.
/skill:montage-dialogue-cleanup Make a reversible dialogue repair test, preserving words.
/skill:montage-time-remapping Land this action at frame 60 with reviewed source handles.
/skill:montage-transcript-editing Build a source-linked paper edit without changing meaning.
/skill:montage-scene-selects Find cut candidates and make a reviewed contact sheet.
/skill:montage-caption-accessibility Review English/French captions for meaningful sounds.
/skill:montage-archive-handoff Package a project copy and test an isolated restore.
```

Skills are instructions, not access grants. Unavailable host tools and engines
remain unavailable. Targets, live actions, credentials, and output directories
must be established for each project.

If your pi settings narrow this package with a `skills` filter, add the new
paths explicitly (for example `skills/montage/led-signage-content/SKILL.md` or
`skills/after-effects/ae-vox-editorial/SKILL.md`), or remove the filter to load
all twenty-three. Run `/reload` afterwards. Publishing a new release does not
upgrade an existing pinned installation or expand its resource filter.

## After Effects and montage toolbox

Built for LED-signage work (digital roll-ups and walls) and general
client montages. The helpers use only the Python standard library; FFmpeg is
found through `$FFMPEG`, `PATH`, or the `imageio-ffmpeg` Python package. Each
media-rendering helper supports a JSON plan with `--dry-run`. Helpers preserve
inputs and refuse output overwrite. The subtitle checker and `sync_map.py`
produce analysis/calculation JSON directly; the sync helper never opens media.
`proxy_audit.py` performs a read-only metadata audit. Its `media` mode needs
ffprobe (`--ffprobe`, `$FFPROBE` or PATH); `json` mode only compares provided
snapshots. Exit 3 means incomplete evidence, not a pass. No mode tests native
proxy attachment or certifies matching picture/audio.

```bash
# LED: text sizes, guide overlay, pixel-exact export, wall split, device test card
python skills/montage/led-signage-content/scripts/led_tool.py text-size --profile led-rollup-516x1032 --distance 4
python skills/montage/led-signage-content/scripts/led_tool.py guides --profile led-wall-3x-516x1032 --out guides.png
python skills/montage/led-signage-content/scripts/led_tool.py export --profile led-rollup-516x1032 --input master.mov --output out.mp4 --dry-run
python skills/montage/led-signage-content/scripts/led_tool.py split --profile led-wall-3x-516x1032 --input wall.mov --outdir deliver/
python skills/montage/led-signage-content/scripts/led_tool.py testcard --profile led-rollup-516x1032 --out-png card.png --out-mp4 card.mp4

# QC of any encoded file: full decode, frames, black/freeze, loudness, loop seam, contact sheet
python skills/montage/video-delivery-qc/scripts/media_qc.py out.mp4 --expect-width 516 --expect-height 1032 --expect-fps 30 --expect-audio no --loop-check --contact-sheet sheet.jpg

# SFX cue sheet -> zero-aligned WAV stem; French caption checks
python skills/montage/sound-design-sfx/scripts/sfx_place.py --cues cues.csv --video cut.mp4 --fps 30 --snap --out sfx_stem.wav
python skills/montage/montage-editing-craft/scripts/srt_check.py captions.srt --preset social-vertical --french fr-CA

# Reviewed source anchors -> rational camera-to-reference map; no media mutation
python skills/montage/montage-multicam-sync/scripts/sync_map.py skills/montage/montage-multicam-sync/assets/anchors.example.json

# Read-only source/proxy audit; new report only, no relink or media changes
python skills/montage/montage-proxy-conform/scripts/proxy_audit.py media original.mov proxy.mov --report audit.json
```

Two MIT-licensed upstream skill sets are vendored unchanged at pinned commits
and reached through adapters: Jared Cassoutt's Vox pipelines (Remotion and
Python) via `vox-explainer-pipelines`, and the score-to-picture workflow via
`sound-design-sfx`. Copy a vendored pipeline into the project before running
its scripts. Full upstream sources can be retrieved separately with
`node scripts/fetch-source.mjs vox-editorial` (plan) and `--fetch`. Higgsfield-hosted workflows and other researched tools are listed,
not installed, in [the montage tools catalog](docs/montage-catalog.md).

## Reverse-engineering tools

### REA — optional CLI / MCP

[REA by morluto](https://github.com/morluto/rea) is pinned to **6.4.0**.
The matching original skill and its six references are included under `vendor/`;
the actual engine is not bundled. Read [setup and limitations](tools/rea/README.md)
before installing or connecting it. A disabled, credential-free MCP example is
provided; no user MCP configuration is replaced automatically.

### Reverse API Engineer — reviewed reference

[Reverse API Engineer by kalil0321](https://github.com/kalil0321/reverse-api-engineer)
is recorded at **0.14.0**. Its autonomous CLI is **not installed or run**. That
version's prompts explicitly instruct generated clients to hardcode captured
credentials, cookies, and tokens. Our [adapted workflow](skills/reverse-api-investigation/SKILL.md)
deliberately does not follow that policy and instead uses pi's existing tools and
model. See [the evaluation](tools/reverse-api-engineer/README.md).

Both repositories can be retrieved as exact, separate source checkouts:

```bash
# Print plans only; no downloads or configuration changes.
node scripts/fetch-source.mjs rea
node scripts/fetch-source.mjs reverse-api-engineer

# Explicit opt-in downloads into ignored .local/upstreams/; no dependency installs.
node scripts/fetch-source.mjs rea --fetch
node scripts/fetch-source.mjs reverse-api-engineer --fetch
```

The published repo contains the reusable integrations, pins, and selected upstream
references—not two full forks. Source checkout is optional; GitHub and npm must
remain reachable to retrieve external sources or engines.

## Privacy and safety

- Keep raw HARs, browser profiles, secrets, and analysis outputs in the relevant
  project's ignored private directory, never this repository.
- The HAR helper outputs only structural counts and opaque identifiers by
  default. Literal route previews require an explicit flag and human review.
- No cookie export, credential harvesting, CAPTCHA bypass, account automation,
  submission, or external messaging is authorized by installing a skill.
- Use official APIs where available. Technical access to a service is not
  permission to automate it or bypass its commercial/access conditions.
- Local tools can produce evidence that reaches pi's model provider. This is not
  an offline-AI guarantee or a promise of free model usage.
- Skills and these checks are not a sandbox or a complete secret scanner.

More: [privacy and execution boundaries](docs/security.md).

## Updates and maintenance

```bash
npm test
npm run updates:check
```

The update check only reads public release metadata (or, for unreleased
snapshots, the tracked branch's latest commit). It never pulls, installs,
changes pins, or rewrites skills. No scheduled task is created. Run it periodically
or before an investigation; review changes and tests before a deliberate update.

Pins, source commits, npm archive integrity, and vendored file hashes live in
[tools/upstreams.lock.json](tools/upstreams.lock.json). Keep REA's engine and skill
snapshot aligned. Git tags are immutable; restoring a pinned version does not
silently upgrade it. See [the update/rollback procedure](docs/maintenance.md) and
[the changelog](CHANGELOG.md).

## Rights

**No license is granted for the original personal skills and helpers at this time.**
A public GitHub repository is not by itself an open-source license. See
[RIGHTS.md](RIGHTS.md). The npm `private` flag prevents accidental npm publication;
it does not make this GitHub repository private.

Third-party material retains its existing MIT license and attribution. See
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Adobe, Higgsfield and
other product names identify compatible products only; no affiliation or
endorsement is implied.
