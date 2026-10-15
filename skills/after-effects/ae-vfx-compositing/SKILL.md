---
name: ae-vfx-compositing
description: Plan, build and QA believable VFX composites in After Effects - keying, rotoscoping, cleanup and object removal, planar/3D tracking, screen replacement and LED roll-up mockups, sky/background swaps, light wrap, colour/grain/black-level matching, depth, shadows and motion-blur integration - using native AE tools first, then Higgsfield or local ComfyUI models with licence checks. Use for green screen, remove background, roto, tracking, corner pin, "put our content on the screen in this photo", cleanup, or when a composite looks pasted.
compatibility: Adobe After Effects 2024 or newer (Keylight, Roto Brush, Content-Aware Fill, 3D Camera Tracker, Mocha AE are bundled). Optional Higgsfield bridge (credits) and a local ComfyUI install (GPU-dependent). FFmpeg optional for QA.
metadata:
  version: "1.0.0"
  short-description: Native-first AE compositing with measured integration QA
---

# VFX compositing in After Effects

[Tiny example — 3 s synthetic screen-replacement mockup](../../../examples/README.md#ae-vfx-compositing).

A composite is finished when nobody notices it. That is measured, not hoped:
edges, black levels, grain, light direction, motion blur and temporal stability
must match the plate.

Production discipline comes from [ae-production-workflow](../ae-production-workflow/SKILL.md)
(canonical AEP, originals untouched, checkpoints, native audit, full decode).
With the Higgsfield bridge, load `ae-clean-rig` first.

## Route by task

| Task | Native AE first | Then, if needed |
| --- | --- | --- |
| Green/blue screen | Keylight + Key Cleaner + Advanced Spill Suppressor | garbage mattes, core/edge split |
| Isolate a subject without a screen | Roto Brush, masks with tracking | Higgsfield Remove Background (credits) or a local segmentation/matting model (licence check) |
| Remove an object / logo / rig | Content-Aware Fill, clone with tracked masks | Higgsfield `/Shot-Cleanup` hosted workflow |
| Put content on a screen, poster, roll-up | Mocha AE planar track → Corner Pin | 3D Camera Tracker for parallax shots |
| Sky or background replacement | Keylight/Linear key on sky, roto edges, tracked plate | depth map for haze and defocus |
| Missing plate or element | — | generate a plate (Higgsfield video models) as a layer, never as the place copy lives |
| Upscale / reframe / interpolate | Detail-preserving Upscale, Warp Stabilizer, Frame Blending off | Higgsfield Upscale/Reframe, local RIFE/ESRGAN (licence check) |

Details: [native recipes](references/native-ae-vfx.md),
[AI-assisted options and licences](references/ai-assisted-vfx.md),
[integration QA](references/integration-qa.md).

## Workflow

1. **Analyse the plate.** fps, resolution, codec, bit depth, noise/grain size,
   motion blur amount, lens distortion, light direction and colour, black and
   white points, camera motion. Write `plate_analysis.json` in the build folder.
2. **Plan the matte.** Hero subject, core matte, edge matte (hair, motion
   blur), garbage matte, holdouts. Decide what is keyed, rotoscoped or tracked.
3. **Pre-compose by role.** `PLATE_<shot>` (untouched), `MATTE_<subject>`,
   `FG_<subject>`, `BG_<replacement>`, `FX_<element>`, `GRADE_<shot>`. The
   original plate layer stays available for A/B at any time.
4. **Build the matte**, judged on the alpha channel view and at 200%.
5. **Integrate** in this order: geometry and track, colour (blacks, whites,
   midtones, saturation), light wrap and edge colour, defocus and depth, motion
   blur, shadows and contact, atmosphere, grain last.
6. **QA** with the checklist in `references/integration-qa.md`, including a
   temporal check (edge chatter) and the final frame.
7. **Deliver** per ae-production-workflow; list generated or model-processed
   elements and their licences in the delivery receipt.

## Hard rules

- Never modify the source plate in place; packaged copies only, hashed.
- Mattes stay editable: no baked "final" alpha without the source matte comp.
- Credits and cloud uploads require consent: say what will be processed, on
  which layer and range, and the cost; trim to the used range first.
- Client footage is not sent to a cloud model unless the user agrees for that
  footage. Local models are preferred for confidential material.
- Check model licences before using outputs commercially; several popular
  matting/background-removal/depth weights are non-commercial.
- Grain is added last and matched to the plate; a clean element on a grainy
  plate is the most common "pasted" tell.
