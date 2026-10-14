---
name: ae-production-workflow
description: Disciplined professional After Effects production workflow for building, revising, rendering, and delivering editable AEP modules. Use for canonical-project preflight, organized AEP folders, one-writer control, timestamped backups, cache/RAM safeguards, exact media timecodes, staged static-to-motion construction, native QA, full render decoding, reversible editability tests, and delivery manifests.
compatibility: Pi on Windows with Adobe After Effects. PowerShell 5+ and Python 3 support bundled helpers; FFmpeg and the Higgsfield AE bridge are optional but recommended.
metadata:
  short-description: Safe, organized, auditable After Effects production
  version: "1.0.2"
---

# After Effects Production Workflow

Use this skill to make AE work **organized, reversible, measurable, and deliverable**. Match the project's creative brief; do not impose a visual style. This skill governs production discipline, not design taste.

## Core contract

1. **One canonical AEP.** Determine the authoritative project before editing. Never fork into parallel standalone AEPs unless the user explicitly asks.
2. **One AE writer/controller.** Reviewers may inspect files, plans, or rendered outputs, but only one agent/process may mutate the live AEP.
3. **Preserve user work.** Inspect the live project and dirty state before backup, reload, close, undo, or script execution.
4. **Work in reversible passes.** Preflight → backup → media package → static build → static QA → motion → native QA → preview → full decode → editability test → final backup/manifest.
5. **Measure, do not assume.** Record comp dimensions, fps, frames, source fps, source IN/OUT, last valid media frame, text bounds, fonts, RAM, hashes, and output decode results.
6. **Never claim verification that did not happen.** Distinguish visual/subtitle checks, waveform analysis, automated decode, and human audio audition.

## Activation sequence

When this skill activates:

1. Find the project root and its instructions, brief, storyboards, prior delivery receipts, and canonical AEP.
2. Create or reuse a build-receipt directory such as:

```text
_planning/<MODULE>_BUILD/
```

3. Start a visible todo list for preflight, media, static, motion, QA, render, editability, and delivery.
4. If using the Higgsfield AE bridge, query host status first. Load its `ae-clean-rig` skill before any other AE skill, then load only the routed modules needed.
5. If scope, canonical AEP, destructive recovery, or final creative direction is ambiguous, ask one focused user question. Do not add approval gates when the user already clearly authorized the work.

## Bundled helpers

Resolve these paths relative to this skill directory:

```powershell
# Read-only RAM gate. Exit 0=safe, 1=warning, 2=pause. Thresholds auto-scale;
# on a 32 GB system the defaults resolve to 18/20/6 GB.
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/ram-snapshot.ps1

# Exact checkpoint. Run only after live AE reports project.dirty=false.
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/checkpoint-aep.ps1 `
  -ProjectPath "Adobe/Project.aep" -Label "before_Module04" -ConfirmedSaved

# Strict final manifest verification from the project root.
python scripts/verify-delivery-manifest.py _planning/MODULE_BUILD/delivery_manifest.json --root .
```

The checkpoint helper refuses unconfirmed saves, existing outputs, non-JSON receipts, and receipt paths that could collide with AEP files. The manifest verifier requires a non-empty strict manifest and fails closed.

## Phase A — live preflight

Perform a read-only preflight before any mutation. Write `_planning/<MODULE>_BUILD/preflight_live.json` containing at least:

- local timestamp and timezone;
- AE version and exact open-project path;
- project dirty state;
- expected master/precomp existence;
- dimensions, fps, duration, frames, layer counts and item IDs for protected comps;
- exact font objects and substitution state;
- missing media and expression errors;
- render-queue item count;
- `_QA_TEMP*` or prior partial-build artifacts;
- Cache Frames When Idle state;
- AE private RAM and Windows free RAM.

### Cache and RAM rules

- Keep **Cache Frames When Idle disabled** unless the user explicitly requests otherwise.
- Determine total physical memory before using thresholds.
- On a 32 GB workstation, use these defaults:
  - warn near **18 GB AE private RAM**;
  - stop new previews/renders at **20 GB**;
  - stop when Windows free RAM is below **6 GB**.
- On other systems, preserve roughly 20% free physical RAM and pause before AE consumes about 65% of total RAM.
- `scripts/ram-snapshot.ps1` derives those thresholds from installed RAM when parameters are omitted; pass explicit positive overrides only for a documented workstation profile.
- Never solve pressure with repeated purges, blind retries, a larger disk cache, or forced restarts.
- If a completed render crosses the threshold: launch no further render, save, quit AE gracefully, then validate externally.

If the project is dirty, preserve the user's unsaved edits. Do not reload or close without explicit alignment.

## Phase B — baseline and checkpoint

Before structural work:

1. Record the canonical AEP SHA-256 and byte size.
2. Record protected comp invariants: ID, duration, frame count, layer count, source media, and any critical matte/control names.
3. Create a timestamped exact backup only after confirming the live project is saved:

```text
<Project>_before_<Module>_YYYYMMDD_HHmmss.aep
```

4. Verify backup hash equals canonical hash.
5. Save the receipt as `checkpoint_and_media.json`.

Use `scripts/checkpoint-aep.ps1` after the saved-state check. Never use the helper as a substitute for checking AE's dirty state.

## Phase C — package media without damaging originals

- Never edit client/source-delivery files in place.
- Copy selected media losslessly into the project asset tree.
- Verify source and packaged SHA-256 hashes match.
- Probe dimensions, codec, fps, audio, duration, frame count, and the final valid video PTS.
- Preserve native source speed and cadence unless reinterpretation is explicitly approved.
- Record source IN/OUT and timeline mapping in a decision receipt, for example:

```json
{
  "source_timebase": "1/24000",
  "source_fps": "24000/1001",
  "source_in_seconds": 21.5215,
  "source_in_frame": 516,
  "timeline_fps": 30,
  "timeline_start_frame": 986,
  "timeline_start_seconds": 32.8666666667,
  "source_out_policy": "native end",
  "last_valid_frame": 1080,
  "verification": ["frame", "subtitle", "waveform"],
  "human_audio_audition": false
}
```

For interviews, inspect the edit around IN/OUT frame-by-frame. Preserve J/L cuts, subtitles, colleagues, and authentic source outros. If human listening did not occur, keep it as a named residual risk.

## Phase D — organize the AEP

Use semantic, independent module folders. A recommended pattern is:

```text
<PROJECT>_<MODULE>_v01/
  01_COMPOSANTS/
    COM_00_LOGO
    COM_01_<SCENE>
    COM_02_<SCENE>
    ...
  02_ASSETS/
  03_CONTROLES/       # only when useful
<MASTER_MODULE_COMP>
```

Rules:

- Reuse official **source assets**, not hidden shared precomp dependencies.
- New module precomps and controls must be independent from protected modules.
- Use a clearly named `CTRL_<MODULE>` null/control layer.
- Prefer native editable text, shapes, mattes, masks, and effects.
- Do not import planning boards as final artwork.
- Use semantic layer names; never leave production layers named `Shape Layer 1`, `Text 4`, or `Untitled`.
- Keep backgrounds, rails, apertures, text, identities, and media structurally obvious.
- Add named comp markers at semantic beats and source-video starts.

## Phase E — static pass first

Build target hold frames before motion:

1. Create folders/comps and place final text, logo, rail, accents, media, mattes, and identity.
2. Measure actual AE `sourceRectAtTime()` bounds; do not trust external mockup metrics. These bounds are layer-space: transform all four corners into comp space with `toComp()` or an equivalent full transform before asserting safety, including parenting, anchor, scale, and rotation.
3. Verify safe areas and maximum right/bottom bounds numerically in the final master coordinate space.
4. Verify fonts through `fontObject.isSubstitute`, not only PostScript names.
5. Save the canonical AEP and create a static checkpoint:

```text
<Project>_<Module>_static_v01.aep
```

6. Render one native still for every hold plus identity/video/outro states.
7. Inspect the **master composition**, not only nested precomps.

Write `static_build_report.json`. A builder must be guarded against existing or partially-created items and must not be blindly rerun.

## Phase F — motion pass

Only after static holds pass:

- Apply masked reveals, deliberate stagger, stable reading holds, and project-approved easing.
- Avoid linear Position/Scale motion. Use settle-weighted BEZIER entrances and restrained exits.
- Keep motion subordinate to hierarchy; do not add generic presets merely to create activity.
- Maintain continuous elements, such as rails, as one master layer when continuity is part of the design.
- Ensure all precomps, media, mattes, backgrounds, and overlays extend through the actual final frame.
- Keep source videos at native speed unless approved otherwise.
- Save and create a motion checkpoint:

```text
<Project>_<Module>_motion_v01.aep
```

Write `motion_build_report.json` with every animated layer, timing, easing, and special variation.

## Phase G — native QA before full render

Audit the final master and protected modules. The audit must cover:

- dimensions, fps, exact duration and frame count;
- protected comp IDs/durations/layer counts;
- complete required copy;
- text bounds and safe areas;
- fonts and substitution state;
- missing media;
- expression errors;
- track-matte links;
- source fps, stretch, audio state, IN/OUT and last-frame visibility;
- rail/control positions at all holds;
- linear spatial keyframes;
- residual `_QA_TEMP*` items;
- render queue is empty.

Render and inspect:

- frame 0;
- each entrance midpoint;
- each settle/hold;
- each exit and transition midpoint;
- video first frame, shot changes, identity start/end, colleagues, outro start, and final frame.

Save `native_audit.json` and contact sheets under the build-receipt folder.

## Phase H — render safely and decode fully

Before a full render, re-check RAM and render queue. Render only one chain at a time.

For preview delivery:

- use the exact master time span;
- include source audio when required;
- write `render_report.json` before/during the long operation so an absent final report is not mistaken for no mutation;
- after render, externally decode the complete file with FFmpeg;
- verify codec, dimensions, fps, decoded frame count, audio stream, duration, first meaningful content, source outro, and final frame;
- generate a contact sheet from the actual encoded output, not only AE stills.

Write `render_validation.json`. Decoded frame count is more authoritative than rounded container-duration text.

## Phase I — reversible editability test

Prove the project is editable:

1. Duplicate one semantic scene into `_QA_TEMP_<MODULE>_EDITABILITY`.
2. Change a real text or control value to a longer but safe test value.
3. Measure bounds and render one native image.
4. Remove the temporary comp.
5. Confirm the original text/control is unchanged.
6. Re-run the native audit.

Do not rely on an immediate `saveFrameToPng()` file-size check; the file may appear just after script return. Check the disk externally before declaring failure or retrying.

Write `editability_test.json`.

## Phase J — final delivery receipt

After the last cleanup and save:

1. Create the exact final backup:

```text
<Project>_after_<Module>_final.aep
```

2. Verify final backup hash equals canonical hash.
3. Write:
   - `DELIVERY.md`;
   - `delivery_manifest.json` using the strict schema in `references/production-checklists.md` (`canonical`, `canonical_sha256`, and a non-empty `files[]` of relative `path`, integer `size`, and SHA-256);
   - updated project context/coverage/status documents.
4. Verify every manifest entry with `scripts/verify-delivery-manifest.py`.
5. State residual risks explicitly: human audition, player codec, physical display, color, audio policy, sync, or unbuilt modules.
6. Leave AE either open and clean or save/quit gracefully; report which state was left.

Use [the detailed checklists](references/production-checklists.md) and [the delivery template](assets/delivery-template.md).

## Error and recovery discipline

- **No blind retry.** First inspect live AE state, report files, disk outputs, render queue, and RAM.
- A missing report does not prove a script made no changes.
- If a one-undo-group builder fails while the preflight proved `project.dirty=false`, reload the saved canonical only after confirming every unsaved change came from that failed pass.
- Do not close without saving when any user edit may exist.
- ExtendScript must remain compatible with AE's older JavaScript engine: avoid unsupported modern syntax and unquoted reserved object keys.
- Unlock only the layer being changed, then restore its lock state.
- Write phase reports before long renders or fragile operations.
- Prefer idempotent scripts or explicit guards that abort on partial state.

## Definition of done

Do not say “finished” until all applicable statements are true:

- canonical AEP saved and final backup hash-matched;
- required copy and media preserved;
- static and motion holds visually inspected;
- fonts/media/expressions/mattes pass native audit;
- full preview decoded to the expected frame count;
- source outro/final frame verified;
- reversible editability test cleaned up;
- no temp comps or render-queue items remain;
- delivery receipt and manifest verified;
- residual risks are stated without exaggerating verification.

## Related toolbox skills

This skill governs discipline, not look or format. Pair it with:

- [ae-vox-editorial](../ae-vox-editorial/SKILL.md) for the editorial collage look;
- [ae-expressions-rigs](../ae-expressions-rigs/SKILL.md) for controls and robust expressions;
- [ae-vfx-compositing](../ae-vfx-compositing/SKILL.md) for keying, tracking and integration;
- [led-signage-content](../../montage/led-signage-content/SKILL.md) for LED roll-ups and walls;
- [video-delivery-qc](../../montage/video-delivery-qc/SKILL.md) for decode-based QC of encoded files.
