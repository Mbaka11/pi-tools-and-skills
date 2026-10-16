---
name: montage-time-remapping
description: Plan and review slow motion, speed ramps, freezes and reverse edits - distinguish capture rate from playback rate, map source to timeline frames, budget handles, choose frame sampling/blending/optical flow, keep audio and captions aligned, and inspect retime artifacts. Use for speed ramp, time remap, slow motion, rate stretch, freeze frame, reverse, velocity edits or a hit that must land on an exact frame.
compatibility: Any NLE with retiming; Premiere and After Effects optional. FFmpeg examples require separately available filters. Optical-flow models/plugins are not installed or authorized automatically.
metadata:
  version: "1.0.0"
  short-description: Frame-accounted speed changes without hidden sync or interpolation errors
---

# Montage time remapping

[Tiny example — actual 1× → 0.5× → 2× retiming](../../../examples/README.md#montage-time-remapping).

Name the event and its target frame before touching the speed curve. A ramp
serves an action; it is not a cure for footage with no usable motion or handles.

## Preflight and map

1. Preserve the source and duplicate the sequence/clip. Confirm exact capture,
   encoded playback and timeline rates; a slow-motion camera file may already
   be conformed. Do not slow it twice by guessing from its filename.
2. Mark the source event frame and required output event frame. Budget real
   source handles before/after it, including transitions.
3. Record source ranges as **start-inclusive/end-exclusive** frame intervals.
   For constant speed `s`, output duration = source duration / `s`.
4. For a variable ramp, calculate cumulative source consumption from the speed
   curve; average endpoint speeds alone do not determine the result. Inspect
   the remap graph and event landing in the host.
5. Decide audio behavior explicitly: linked retime, separate music/SFX bed,
   deliberate mute, pitch-preserved time stretch or stylized pitch change.
   Ordinary speech should remain natural unless the brief explicitly says otherwise.

## Choose interpolation deliberately

| Method | Appropriate use | Risk |
| --- | --- | --- |
| Frame sampling | Adequate captured frames; clean edges | Repeated frames/judder below available temporal resolution |
| Frame blending | Some softer motion, modest retime | Ghosted edges and double images |
| Optical flow | Suitable motion where intermediate frames are genuinely needed | Warped limbs, occlusions, text, reflections and cut boundaries |
| Freeze/reverse | Intentional editorial punctuation | Duplicate endpoint frames, impossible motion, audio discontinuity |

60 fps capture played at 50% on a 30 fps timeline can use one captured frame per
output frame; 30 fps at 50% cannot. Optical flow invents estimates, not recovered
camera detail. Check rights/build/model requirements before enabling an external
interpolator. Never interpolate across an unrelated shot cut.

## Native workflow

In Premiere, compare Speed/Duration, Rate Stretch and Time Remapping for the
actual need. Time Remapping is not an automatic guarantee of audio following
video. Make a duplicate and explicitly verify linked audio behavior. In AE,
use a source precomp and source-time keys; remove unintended end holds and
check the last valid source frame. Keep editable versions before baking.

Discover the real connected host/tool capabilities. A local FFmpeg proof is
not evidence that a Premiere ramp or AE expression was built.

## QA and handoff

- Confirm total frames, exact event landing and source endpoints in the encoded
  output, not only the editor's preview.
- Review at normal speed, then inspect frame-by-frame around slope changes,
  occlusions and high-motion edges. Check reverse/freeze boundaries for clicks.
- Re-time or regenerate captions, cue sheets and overlays that followed the old
  timeline. Keep unretimed reference and a source-to-output timing note.
- Export from originals, not low-quality proxies; decode with
  [video-delivery-qc](../video-delivery-qc/SKILL.md).
- See [timing math and FFmpeg proof](references/timing-and-artifacts.md).
