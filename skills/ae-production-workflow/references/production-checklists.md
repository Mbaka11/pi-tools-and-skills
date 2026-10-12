# AE Production Checklists

Load this reference when executing or auditing a real After Effects build.

## 1. Suggested receipt tree

```text
_planning/<MODULE>_BUILD/
  preflight_live.json
  checkpoint_and_media.json
  media_edit_decision.json
  static_build_report.json
  motion_build_report.json
  native_audit.json
  render_report.json
  full_decode.log
  render_validation.json
  editability_test.json
  final_holds_contact.png
  motion_transition_contact_01.png
  video_contact_02.png
  render_decode_contact.jpg
  DELIVERY.md
  delivery_manifest.json
```

Use local project conventions when they already exist. Do not create a competing receipt tree.

## 2. Timestamp and naming convention

- Local timestamp: `YYYYMMDD_HHmmss`, e.g. `20260923_221037`.
- Also record an ISO timestamp with timezone in JSON receipts.
- Backup names:
  - `<Project>_before_<Module>_<timestamp>.aep`
  - `<Project>_<Module>_static_v01.aep`
  - `<Project>_<Module>_motion_v01.aep`
  - `<Project>_after_<Module>_final.aep`
- Preview names:
  - `<NN>_<MODULE>_v01.mp4`
  - increment only for meaningful render revisions.
- Temporary comps must begin `_QA_TEMP_` so audits can find them.

## 3. Preflight checklist

### Project state

- [ ] Correct AEP is open.
- [ ] Window title/project path captured.
- [ ] Dirty state captured.
- [ ] AE version captured.
- [ ] Cache Frames When Idle is off.
- [ ] Render queue is empty.
- [ ] Expected master and protected comps are present.
- [ ] Target module is absent or its exact existing state is understood.
- [ ] No `_QA_TEMP*` items remain.

### Project health

- [ ] Missing/substituted font count is zero.
- [ ] Required fonts resolve through font objects.
- [ ] Missing media count is zero.
- [ ] Expression errors are zero.
- [ ] Protected comp IDs, frames, durations, and layer counts recorded.

### Resources

- [ ] AE private RAM recorded.
- [ ] Windows free RAM recorded.
- [ ] No competing aerender/AME/second AE writer.
- [ ] One-controller rule established.

## 4. Static-pass checklist

- [ ] AEP folders use numbered semantic groups.
- [ ] Every scene/precomp name is semantic.
- [ ] Master, controls, background, rails, apertures, identities, and media are easy to locate.
- [ ] Official source assets are reused without editing originals.
- [ ] Text is native and editable.
- [ ] Shapes/mattes are native.
- [ ] Font substitution is checked after text creation.
- [ ] Visible text bounds measured in AE.
- [ ] Safe-area limits pass numerically.
- [ ] Each hold rendered from the master comp.
- [ ] Static checkpoint saved and hash recorded.

## 5. Motion-pass checklist

- [ ] Entrances, holds, and exits have explicit timing.
- [ ] Reading order matches reveal order.
- [ ] Position/Scale motion is BEZIER, not linear.
- [ ] Opacity and movement are not mechanically simultaneous unless intentional.
- [ ] Motion blur is applied only where useful.
- [ ] Continuous rails/lines do not jump laterally.
- [ ] Video aperture is inspected at start, midpoint, near-full, and full.
- [ ] Source subtitles are not materially hidden.
- [ ] Identity appears only on the correct person and shot.
- [ ] No overlay returns on the source outro.
- [ ] Motion checkpoint saved.

## 6. Media timing receipt

Record exact values, not prose-only estimates:

```json
{
  "source": "Assets/Video/interview.mp4",
  "source_sha256": "...",
  "source_timebase": "1/24000",
  "native_fps": "24000/1001",
  "source_frame_count": 1081,
  "source_duration_seconds": 45.086753,
  "source_in": {
    "frame_index_zero_based": 516,
    "pts_seconds": 21.5215
  },
  "source_out": {
    "policy": "native end",
    "last_valid_frame_index_zero_based": 1080,
    "last_valid_frame_pts_seconds": 45.045
  },
  "timeline": {
    "fps": 30,
    "aperture_start_frame": 972,
    "aperture_start_seconds": 32.4,
    "playback_start_frame": 986,
    "playback_start_seconds": 32.8666666667,
    "aperture_full_frame": 988,
    "aperture_full_seconds": 32.9333333333
  },
  "verification": {
    "frames": true,
    "subtitles": true,
    "waveform": true,
    "human_audio_audition": false
  }
}
```

Do not convert `human_audio_audition:false` into “audio-safe verified.” Say what was actually measured.

## 7. Native audit checklist

- [ ] Master width/height/fps/frame count exact.
- [ ] Protected modules unchanged.
- [ ] Complete mandatory copy present.
- [ ] No text exceeds safe bounds.
- [ ] Fonts exact and non-substituted.
- [ ] No missing media.
- [ ] No expression errors.
- [ ] Track mattes point to intended layers.
- [ ] Matte/precomp/background/media out-points cover the last used frame.
- [ ] Source fps/scale/stretch/audio state correct.
- [ ] Source final valid frame is visible in the master.
- [ ] Identity timing excludes colleagues/b-roll.
- [ ] No linear spatial keyframes on hero motion.
- [ ] No temp comps.
- [ ] Render queue empty.

## 8. Frame-review matrix

For every master, inspect at least:

| Beat | What to inspect |
|---|---|
| 0 | intended initial state; no accidental pop |
| entrance midpoint | mask direction, clipping, easing, readable partial state |
| settle | strongest final composition |
| hold | copy, hierarchy, safe bounds |
| exit midpoint | no ghosting or premature disappearance |
| transition midpoint | continuity, no uncovered background seam |
| first video frame | source IN, subtitle, framing |
| shot changes | identity/person correctness |
| identity start/full/end | face/hair/subtitles clear |
| source outro start | no duplicate brand overlay |
| final master frame | actual media still visible; no black/empty frame |

## 9. Render validation checklist

- [ ] Render report says complete.
- [ ] Output exists and has plausible size.
- [ ] Full decode exits 0.
- [ ] Decoded video frame count equals expected.
- [ ] Width/height/fps exact.
- [ ] Video codec/pixel format recorded.
- [ ] Audio stream/sample rate/channels recorded.
- [ ] Encoded-output contact sheet inspected.
- [ ] Final source outro and last frame inspected from encoded file.
- [ ] SHA-256 recorded.

## 10. Strict delivery-manifest contract

The verifier fails closed unless the manifest contains:

```json
{
  "canonical": "Adobe/Project.aep",
  "canonical_sha256": "<64 lowercase hex characters>",
  "files": [
    {
      "path": "Adobe/Project.aep",
      "size": 5093011,
      "sha256": "<64 lowercase hex characters>"
    }
  ]
}
```

Rules:

- `files` must be a non-empty array.
- Every path is relative to the project root, unique, and unable to escape it.
- `size` is the exact non-negative byte count.
- `sha256` is the exact 64-character digest.
- The canonical AEP must also appear in `files[]`.
- Empty, malformed, duplicate, absolute, or out-of-root entries fail verification.

Run from the skill directory or resolve the helper's absolute path:

```bash
python scripts/verify-delivery-manifest.py \
  <project>/_planning/<MODULE>_BUILD/delivery_manifest.json \
  --root <project>
```

## 11. Recovery decision tree

### Script returned an error

1. Stop.
2. Read the report and line number.
3. Inspect live items/layers and project dirty state.
4. Inspect disk outputs and timestamps.
5. Decide whether the pass was:
   - untouched;
   - partially applied but unsaved;
   - partially applied and saved;
   - complete despite a late report/check failure.
6. Recover with the least destructive option.

### Safe reload is allowed only when

- preflight captured `dirty=false` immediately before the pass;
- one known script was the only writer;
- every unsaved change belongs to the failed pass;
- the canonical saved file and backup are verified.

Otherwise ask the user before discarding anything.

### Render appears to time out

- Check whether the MP4 and report are still appearing.
- Check AE RAM and render queue.
- Do not launch a second render.
- Do not infer failure from a launcher process returning before disk flush.

## 12. Final delivery checklist

- [ ] Canonical project clean.
- [ ] Final backup byte/hash matches canonical.
- [ ] Preview full-decode passed.
- [ ] Native audit passed after editability cleanup.
- [ ] Manifest entries independently verified.
- [ ] Current project status documents updated.
- [ ] Residual risks stated.
- [ ] AE final state reported: open clean or gracefully closed.
