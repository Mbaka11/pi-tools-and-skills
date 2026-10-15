---
name: ae-vox-editorial
description: Build Vox-style editorial explainer motion natively and editably in After Effects - paper-collage grounds, cut-out subjects with sticker borders and offset marker strokes, halftone/archival treatments, highlighter and hand-drawn annotations, document clippings, maps and route lines, stepped collage motion and multiplane camera depth. Use for "Vox style", editorial/documentary motion graphics, paper-collage or mixed-media explainers, animated clippings, or highlight/scribble reveals in AE, in 16:9, 9:16 or LED roll-up formats. For code-rendered or fully generated pipelines use vox-explainer-pipelines.
compatibility: Adobe After Effects 2024 or newer. The Higgsfield AE bridge is recommended for live builds; image generation spends Higgsfield credits. Photoshop is optional for still halftone treatment. FFmpeg is optional for QA.
metadata:
  version: "1.0.0"
  short-description: Editable Vox-style editorial collage in After Effects
---

# Vox-style editorial motion in After Effects

[Tiny example — 3 s original collage mockup, not a native AE render](../../../examples/README.md#ae-vox-editorial).

This skill supplies the **visual grammar and native AE recipes** for the
editorial "Vox" look. It does not replace the production discipline or the
bridge doctrine:

1. Follow [ae-production-workflow](../ae-production-workflow/SKILL.md) for the
   canonical AEP, backups, static-before-motion, native QA and delivery receipts.
2. With the Higgsfield bridge, load its `ae-clean-rig` skill first. Where it
   conflicts with this skill about tools, building, auditing or finalizing, the
   bridge doctrine wins; this skill only decides *what the frame looks like*.
3. For LED roll-ups and walls, also apply [led-signage-content](../../montage/led-signage-content/SKILL.md)
   before locking type sizes, strokes, textures and loop timing.

## Pick the route first

| Need | Route |
| --- | --- |
| Client-editable AEP, exact copy, brand fonts, LED formats, revisions | **This skill (native AE)** |
| Narrated film rendered from code, re-timed from the voice-over | [vox-explainer-pipelines](../../montage/vox-explainer-pipelines/SKILL.md) route B (Remotion) |
| Vertical cut-paper film assembled locally with Python + FFmpeg | [vox-explainer-pipelines](../../montage/vox-explainer-pipelines/SKILL.md) route C |
| One-prompt hosted generation, low editability, credits accepted | Higgsfield hosted workflows (`/vox-mixed-media`, `/paper-collage`) — see the catalog in that skill |

Default to the native route when the client will ask for text, price, logo or
timing changes. Generated video can feed a native build as a plate, never as
the place where copy lives.

## What makes the look (in priority order)

1. **One checkable idea per beat.** Editorial motion earns attention by being
   interesting. A hook that withholds the subject, a payoff that answers it.
2. **The clock.** With narration, the voice-over is the clock. On silent LED
   screens, reading time is the clock (see `references/narrative-and-timing.md`).
3. **Depth.** Ground, subject and foreground move against each other. A frame
   with two flat layers reads as a slide.
4. **Hand-made texture.** Paper, halftone, torn edges, marker strokes, stepped
   motion. Restraint: two or three colours plus paper and ink.
5. Everything else.

## Build sequence

1. **Brief and format.** Record aspect, pixel size, fps, duration, loop or not,
   sound or silent, language, required copy and legal mentions, brand assets
   and font licences. Ask once if a high-leverage input is missing.
2. **Beat sheet.** Write the beats table (`references/narrative-and-timing.md`)
   before opening AE: on-screen text, VO line, visual idea, depth layers,
   duration, transition. Fewer scenes than beats; hold images while text changes.
3. **Style passport.** Copy `assets/vox-style-passport.template.json` to the
   build-receipt folder and fill it: palette, paper source, stroke offsets,
   halftone, grain, stepped rate, typefaces with licence evidence. Every scene
   reuses it. Change it only by an explicit decision.
4. **Classify assets.** `DRAW` (paper, tears, highlights, arrows, charts, maps,
   documents, stamps, all text) is built natively. `SOURCE` (client photos,
   public-domain archives) is packaged with rights evidence. `GEN` is limited
   to wordless subjects generated as *elements, not posters* — see
   `references/asset-sourcing.md`. Never bake text, prices or logos into a
   generated image.
5. **Static pass.** One precomp per beat (`VOX_B01_<slug>`). One continuous
   paper ground in the master, not one per beat. Build every hold frame, measure
   text bounds, check safe areas, render stills, inspect the master.
6. **Motion pass.** Elements *arrive* (rise, scale-settle, slam, draw-on); they
   rarely just fade. Stagger entrances; settle-weighted easing; stepped collage
   motion on elements while the camera stays smooth. Recipes:
   `references/ae-recipes.md`. Expressions: [ae-expressions-rigs](../ae-expressions-rigs/SKILL.md).
7. **Texture pass.** Grain, paper fibres, vignette, subtle gate weave, applied
   once at master level. Re-check legibility afterwards — texture is the usual
   reason small text fails on LED.
8. **QA and delivery.** Native audit, contact sheet of every hold, readability
   on the real pixel grid, loop seam if looping, full decode. Use
   [video-delivery-qc](../../montage/video-delivery-qc/SKILL.md) for the
   encoded file.

## Native recipe index

Full layer stacks, effect match names and tuning live in `references/ae-recipes.md`:

- paper ground (scan or procedural), torn edges, paper drop shadow;
- white sticker border and offset colour stroke around alpha cut-outs;
- halftone/duotone for stills (Photoshop or pre-treatment) and for footage;
- highlighter wipe, hand-drawn circle, underline, arrow, scribble boil;
- stepped "stop-motion" motion and line boil;
- multiplane 3D depth with scale compensation, or a cheap 2D parallax rig;
- maps (vector shapes, route draw-on, pins), charts drawn on, counters;
- document/newspaper clippings, typewriter reveal, stamp slam;
- archival footage treatment (B&W, grain, flicker, weave, torn frame matte);
- red-string connections that follow pinned layers.

## LED and vertical adaptations

- Build at the exact device pixel size (for example 516×1032 per
  screen on a compatible 1:2 panel; confirm the device). Never design at 1080×1920 and hope the player downsizes cleanly.
- Halftone dots, paper fibres and grain below about 3 px shimmer or vanish on a
  P1.86 grid. Enlarge the pattern or drop it on the smallest elements.
- Strokes and underlines at least 3–4 px; text sizes from the LED skill's
  calculator; avoid large pure-white paper fields at full brightness.
- Silent loops: the last frame must return to the first state. Keep the paper
  ground and camera continuous across the loop point.

## Red flags

- A generated "finished poster" animated by sliding parts over itself.
- Copy, prices, dates or logos inside generated or flattened images.
- Every element fading in, or several elements landing on the same frame.
- The paper ground changing between beats, or each beat using another palette.
- Archival images without a recorded licence, or real outlets' mastheads on
  invented headlines.
- Halftone or grain making text unreadable at 100% on the target grid.
- Declaring the build done before the native audit and a decoded render.
