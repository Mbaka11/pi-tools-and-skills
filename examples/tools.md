# One very short example per included tool

Links below point to genuinely generated synthetic outputs, or are explicitly
marked **illustrative / not executed**. These examples do not install
third-party engines.

## Editing helpers

| Tool | Example result |
| --- | --- |
| [`led_tool.py`](../skills/montage/led-signage-content/scripts/led_tool.py) | [3 s loop](media/led-loop.mp4), [test card](media/led-testcard.png), [guides](media/led-guides.png); at 4 m/P1.86, cap heights of **18 / 26 / 44 px** ([calculation](outputs/text-size.json)). |
| [`media_qc.py`](../skills/montage/video-delivery-qc/scripts/media_qc.py) | [90 decoded frames, no audio, measured seam](outputs/media-qc.json) + [contact sheet](media/qc-contact.png). |
| [`sfx_place.py`](../skills/montage/sound-design-sfx/scripts/sfx_place.py) | [3 s stem](media/sfx.wav), three cues at **0.3 / 1 / 2 s** ([result excerpt](outputs/sfx-cues.json)). |
| [`srt_check.py`](../skills/montage/montage-editing-craft/scripts/srt_check.py) | [Corrected copy](outputs/captions-fixed.srt); [0 errors after correction](outputs/captions-after.json). |
| [`sync_map.py`](../skills/montage/montage-multicam-sync/scripts/sync_map.py) | [Two reviewed synthetic anchors](../skills/montage/montage-multicam-sync/assets/anchors.example.json) → [−0.2 s / −6 frames](outputs/sync-map.json); calculation only, no event detection or media changes. |

## AE helpers

| Tool | Example result |
| --- | --- |
| [`verify-delivery-manifest.py`](../skills/after-effects/ae-production-workflow/scripts/verify-delivery-manifest.py) | [Actual result](outputs/delivery-check.json): `ok=true`, one text file checked, no AEP involved. |
| [`checkpoint-aep.ps1`](../skills/after-effects/ae-production-workflow/scripts/checkpoint-aep.ps1) | **Illustrative, not executed**: `Demo_before_title_YYYYMMDD_HHmmss.aep`, a timestamped copy whose hash must match the saved project. No fake AEP is published. |
| [`ram-snapshot.ps1`](../skills/after-effects/ae-production-workflow/scripts/ram-snapshot.ps1) | **Illustrative, not executed**: “Free memory below threshold → pause, no new render.” No diagnostics from this machine are published. |

## Investigation tools and engines

| Tool | Example result |
| --- | --- |
| [`har-summary.mjs`](../skills/reverse-api-investigation/scripts/har-summary.mjs) | [Actual summary of two fictitious events](outputs/api-summary.json): `host_1`, `endpoint_1`, `requests=2`, without URLs/cookies/tokens. |
| [REA](../tools/rea/README.md) | [Fictitious import chain](reports.md#rea-investigation); engine not executed. |
| [Reverse API Engineer](../tools/reverse-api-engineer/README.md) | [Fictitious mini API map](reports.md#reverse-api-investigation); upstream agent not executed, no hardcoded secrets. |
| [Vox editorial / Remotion and Python](../vendor/vox-editorial/README.md) | [Original three-beat mockup](README.md#vox-explainer-pipelines), not an upstream-script render. |
| [Cinematic score and SFX](../vendor/cinematic-score-and-sfx/README.md) | **Illustrative**: `reveal → sweep; cut → impact; conclusion → chime`. [Original audio](media/sfx.wav) produced by our helper, not an upstream provider. |

## Maintenance utilities

| Tool | Very short example |
| --- | --- |
| [`check.mjs`](../scripts/check.mjs) | `node scripts/check.mjs` → sample response shape `{"ok":true,"skills":["…"],"errors":[]}`; the actual result depends on the inspected files. |
| [`check-examples.mjs`](../scripts/check-examples.mjs) | Checks that media is declared, size-bounded and matches its SHA-256; rejects a video added outside the manifest. |
| [`check-updates.mjs`](../scripts/check-updates.mjs) | **Illustrative**: “Pinned version unchanged / update available”; no simulated network check is presented as current evidence. |
| [`fetch-source.mjs`](../scripts/fetch-source.mjs) | `node scripts/fetch-source.mjs vox-editorial` → retrieval plan for the pinned commit; no download without `--fetch`. |
| [`upstreams.mjs`](../scripts/upstreams.mjs) | Internal library: reads `tools/upstreams.lock.json`, validates pins and safely resolves source paths. |
| [`examples/build.py`](build.py) | `--set montage` produces the [five new examples](README.md#montage-colour-finishing); `all`/`core` include the original gallery. New directories only, no cloud use or implicit installation. |

[Back to the gallery](README.md)
