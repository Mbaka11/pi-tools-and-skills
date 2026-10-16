---
name: montage-colour-finishing
description: Colour-managed finishing for video edits - identify camera log, SDR or HDR inputs, choose working and output spaces, prevent double transforms, normalize exposure and white balance, match shots with scopes and reference frames, apply creative looks separately, and verify exports. Use for colour/color grading, Lumetri, shot matching, LUTs, Rec.709, washed-out exports or mixed-camera footage. Complements montage-editing-craft and video-delivery-qc, not a replacement for calibrated monitoring.
compatibility: Any colour-managed NLE; Premiere Pro and Lumetri are optional. FFmpeg examples require a separately available build. No LUTs, plugins or calibration hardware are bundled.
metadata:
  version: "1.0.0"
  short-description: Colour management, shot matching and export consistency
---

# Montage colour finishing

[Tiny example — actual RGB correction on a synthetic chart](../../../examples/README.md#montage-colour-finishing).

Make the pipeline correct before making the image attractive. A LUT cannot
repair an incorrectly identified camera transfer function or clipped capture.

## Establish the colour contract

Record in a project-local grade note:

- camera/profile and trusted input space for each source group; metadata can be
  absent or wrong, so confirm with the operator or camera documentation;
- project/sequence working space, output space and SDR/HDR delivery intent;
- display transform, calibrated monitoring conditions and any limitations;
- exact technical LUT/transform, version/hash and permitted usage, if required;
- whether an automatic input conversion or tone map is already active.

Do not infer a camera log curve from a flat-looking thumbnail. Ask for missing
capture information. Do not change the working space halfway through a grade
without duplicating the sequence and rechecking every correction.

## Work in this order

1. **Duplicate and reference.** Save a versioned sequence; choose a representative
   hero frame and inspect shots before/after it at normal playback speed.
2. **Input conversion.** Assign the right input interpretation. Choose a managed
   conversion OR the appropriate technical LUT path; do not accidentally apply
   two log-to-display conversions. Separate input, creative and output transforms.
3. **Primary balance.** Correct exposure and white balance with waveform, RGB
   parade and vectorscope. Inspect neutrals and plausible skin, not just average
   histogram values. Protect highlights; no transform recovers clipped channels.
4. **Shot matching.** Match the same subject under comparable lighting, then
   contrast, saturation and black level. Compare through cuts, not only stills.
   Preserve intentional changes in scene or time of day.
5. **Creative look.** Apply a restrained look after balancing. Keep shot-specific
   corrections separate from a sequence-wide look so revisions stay reversible.
6. **Secondaries and texture.** Check qualifiers on moving faces/hands, noise,
   banding, gradients and compression. Avoid sharpening noise or plastic skin.
7. **Export and re-import.** Check the encoded file's tags, scopes and appearance
   through the same managed pipeline. Then inspect the target playback path.
   Do not compensate blindly for a single unmanaged player's gamma difference.

## Premiere route

Check the installed version's colour controls. Source-clip input assignments,
sequence working/output settings and automatic tone mapping vary by version.
Use Lumetri **Comparison View** and **Apply Match** only as a starting point;
refine manually and compare multiple frames. A shared adjustment layer is useful
for a look, not for hiding incompatible input interpretations.

If using a bridge, discover the actual available tool contracts before editing.
Do not invent a colour-grading API or claim that a disconnected host was tested.
Keep one writer and a recoverable project copy.

## Acceptance and handoff

- Input/working/output spaces and all LUTs are documented.
- No unexplained brightness/white-balance jump across adjacent shots.
- Export tags agree with the intended transform; **tagging is not conversion**.
- SDR and HDR versions are separately authored and reviewed, not relabelled.
- [Decode QC](../video-delivery-qc/SKILL.md) passes; human and calibrated-display
  review are recorded separately, including anything not performed.

Read [colour pipeline checks and sources](references/colour-pipeline.md).
