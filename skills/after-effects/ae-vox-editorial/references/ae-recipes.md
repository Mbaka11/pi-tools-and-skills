# Native AE recipes for the editorial collage look

Each recipe lists the layer stack, the effects (display name and match name for
scripted or bridge calls), the values worth tuning and the LED caveat. Values
assume 1920×1080; scale pixel values by `target width / 1920` and then apply
the LED minimums. Verify match names with `ae_list_effects` (or the Effects &
Presets panel) on the installed AE version before scripting; third-party
plug-ins are never assumed.

Name every layer semantically (`PAPER_GROUND`, `CUT_portrait_main`,
`HL_line02`, `CTRL_VOX`). Keep one `CTRL_VOX` null holding shared sliders.

---

## 1. Paper ground (continuous across the film)

**Preferred:** a licensed or CC0 paper scan, at least comp size, imported once,
placed in the master comp under every beat precomp. Keep it one layer for the
whole duration so beats read as one film.

**Procedural fallback:**

| Layer | Effect | Notes |
| --- | --- | --- |
| `PAPER_BASE` solid, paper colour from the passport | — | `#DAD9D5`-like warm grey or client cream |
| `PAPER_TEXTURE` solid | Fractal Noise (`ADBE Fractal Noise`) | Contrast 60–90, Brightness −10…0, Scale 250–500, Complexity 6–8; blend Multiply or Overlay at 8–20% |
| `PAPER_FIBRE` solid | Fractal Noise, Fractal Type *Dynamic*, Scale 40–80, stretched width 300–600% | blend Soft Light 5–12%; drop on LED if it shimmers |

Do not animate Evolution on the ground unless the brief wants "boiling" paper;
static paper reads as a physical sheet.

**LED:** fine fibres under ~3 px disappear or flicker on P1.86. Prefer a scan
with large, soft variation, or omit the fibre layer.

## 2. Torn paper shapes and banners

| Layer | Effect | Tune |
| --- | --- | --- |
| `TEAR_<name>` shape or solid with mask | Roughen Edges (`ADBE Roughen Edges`) | Edge Type *Roughen*, Border 6–20, Edge Sharpness 1–2, Scale 30–60, Complexity 2–4 |
| optional white fibre edge: duplicate below, slightly larger | Roughen Edges with a higher Border | white or paper-light colour |
| — | Drop Shadow (`ADBE Drop Shadow`) | Opacity 20–35%, Direction 135–160°, Distance 4–12, Softness 12–30 |

Headlines set into torn stock: native text layer above the torn shape, both in
one precomp (`BANNER_<slug>`) so the unit animates together while the text stays
editable. Never rasterise the headline.

## 3. Sticker border and offset marker stroke (alpha cut-outs)

For a PNG/footage layer with clean alpha (`CUT_<subject>`), inside a precomp:

1. `CUT_<subject>` — the image (top).
2. `CUT_<subject>_BORDER` — duplicate below: Fill (`ADBE Fill`) white, then
   Minimax (`ADBE Minimax`) Operation *Maximum*, Channel *Alpha and Color*,
   Radius 6–14 px (dilates the silhouette). Optional light Roughen Edges for a
   scissored feel.
3. `CUT_<subject>_STROKE` — another duplicate below: Fill accent red from the
   passport, Minimax Radius slightly larger than the border, Position offset
   about +20…+26 px X and +6…+10 px Y (mirror the X sign for subjects on the
   left of frame so the stroke points outward).
4. Paper Drop Shadow on the precomp layer in the beat comp.

Small expansions (≤10 px) can use Simple Choker (`ADBE Simple Choker`) with a
negative choke instead of Minimax. Check the edge at 200% on hair and fingers;
a coloured fringe means the source alpha needs work (see the VFX skill).

**LED:** border ≥ 4 px and stroke offset ≥ 4 px at 516 px width or they merge
into a blur.

## 4. Halftone and duotone

**Stills (preferred):** treat in Photoshop as a Smart Object (Black & White →
Levels contrast → Filter › Pixelate › Color Halftone with one channel angle, or
a bitmap halftone), export PNG, keep the untreated original beside it. The
Photoshop MCP or the vendored `halftone.py` (see vox-explainer-pipelines) can do
this. Treated stills stay crisp and render fast.

**Footage or animated halftone (native, luma-threshold method):**

1. Precomp the shot; inside: Black & White (`ADBE Black&White`) then Curves
   (`ADBE CurvesCustom`) or Levels (`ADBE Easy Levels2`) for contrast.
2. Build a dot grid: a cell-sized precomp (for example 12×12 px) holding a
   radial Gradient Ramp (`ADBE Ramp`), tiled to comp size with CC RepeTile
   (`CC RepeTile`, tiling Repeat, large expansions).
3. Combine the dot grid with the luminance in the shot precomp and apply
   Threshold (`ADBE Threshold2`) on an adjustment layer above both. The blend
   between grid and luminance decides whether dark areas grow dots; test the
   stack on a black-to-white gradient test card first and keep the version that
   produces larger dots in shadows.
4. Colour the result with Tint (`ADBE Tint`) or Tritone (`ADBE Tritone`):
   ink colour on map-to-black, paper on map-to-white. Set the precomp layer to
   Multiply over the paper ground.

Prove the stack on the test card before applying it to client footage, and
record the chosen cell size in the style passport.

**LED:** cell size ≥ 6 px on a 516 px wide screen, otherwise dots alias into
moiré. Large duotone areas without dots are often the better LED choice.

## 5. Highlighter wipe behind words

- `HL_<line>` rectangle shape sized to the measured text bounds (use
  `sourceRectAtTime()`; see ae-expressions-rigs), placed **below** the text,
  blend Multiply, accent colour at 60–85% opacity.
- Reveal: Linear Wipe (`ADBE Linear Wipe`) Transition Completion 100→0% over
  8–14 frames with settle easing, Feather 2–6 px. With those keys a Wipe Angle of
  270° (−90°) reveals left to right and 90° reveals right to left — check one
  mid-wipe frame before copying the setup to other lines.
  Alternative: anchor at the left edge and animate Scale X 0→100%.
- Marker texture: Turbulent Displace (`ADBE Turbulent Displace`) Amount 5–15,
  Size 20–40 on the highlight only.
- Stagger multiple lines by 4–8 frames; land the wipe on the spoken or key word.

## 6. Hand-drawn circle, underline, arrow

- Draw with the Pen tool, deliberately imperfect: an open loop that overshoots
  its start reads as hand-made; a perfect ellipse reads as UI.
- Stroke 6–10 px (LED ≥ 4 px), round caps and joins, accent colour.
- Trim Paths (`ADBE Vector Filter - Trim`) End 0→100% over 10–16 frames with
  an ease-out; arrows: draw the shaft, then the head 2–4 frames later.
- Boil: Wiggle Paths (`ADBE Vector Filter - Roughen`) Size 1–2, Detail 2–4,
  Wiggles/Second 0 for a fixed wobble, or keyed/stepped for a boiling line.
- Anchor the annotation to the element it marks by parenting, or with the
  expressions in ae-expressions-rigs. Never type absolute coordinates.

## 7. Stepped collage motion

Collage elements move at 8–12 steps per second while the camera and the ground
stay smooth at the comp frame rate. Options, cheapest first:

1. Posterize Time (`ADBE Posterize Time`) on the element's precomp layer
   (affects everything inside the precomp).
2. The stepped-motion expression from ae-expressions-rigs on Position/Rotation
   (affects one property, adds deterministic boil).
3. Hold keyframes for deliberate pose-to-pose moves.

Do not posterize the master comp: the camera push and texture would stutter.

## 8. Multiplane depth

**3D (best parallax):** make beat elements 3D layers at depth tiers, add one
camera `CAM_MAIN` (one-node is enough), and push in or drift slowly (3–8% per
beat). Suggested tiers relative to the subject plane (z = 0 at 100% apparent
size; positive z is farther from the default camera):

| Plane | z | Role |
| --- | --- | --- |
| Ground | +1500…+2500 | paper and backdrop, barely moves |
| Clippings, maps | +600…+1000 | context |
| Secondary subject | +200…+400 | supporting cut-outs |
| Primary subject | 0 | the beat's subject |
| Foreground occluder | −300…−600 | crops the subject, sells depth |
| Headline | −600…−900 | damp its response or it leaves frame |

Use the scale-compensation expression from ae-expressions-rigs so layers keep
their designed size at rest. Enable Depth of Field only if the look needs it;
it multiplies render time.

**2D parallax rig (fast):** keep layers 2D; give each a `Depth` slider (0 far,
1 near) and add the parallax expression driven by a `Parallax Drift` point
control on `CTRL_VOX`. Animate only the control.

## 9. Maps and routes

- Shapes: public-domain vector data (for example Natural Earth) or the client's
  map, imported via Illustrator → *Create Shapes from Vector Layer*.
- Precomp the map with **Collapse Transformations / Continuous Rasterize** on so
  it stays sharp while scaling.
- Route: open path, stroke 6–12 px (LED ≥ 4), Trim Paths draw-on; optional
  dashes; a pin/dot pops at the destination 2–4 frames after the line lands.
- Zoom: animate the camera or the map precomp scale with ease, holding long
  enough to read labels. Labels are native text, never baked.

## 10. Documents, clippings and type

- Clipping: paper rectangle (torn on one or two edges) + native text layers in a
  serif face; slight rotation ±2–4°; paper drop shadow; halftone photo inside.
- Use the client's real copy or clearly generic mastheads. Do not imitate a real
  publication's masthead or attribute invented headlines to real outlets.
- Typewriter reveal: text animator Opacity 0% with a Range Selector, Units
  *Index* or Percentage, Based On *Characters*, Smoothness 0%; animate Start
  0→100%. About 2 frames per character at 30 fps reads as typing.
- Stamp slam: scale 140→100% in 3–4 frames with a hold, rotation −6…−10°,
  Multiply blend, grunge via Fractal Noise + Set Matte (`ADBE Set Matte3`) or
  Roughen Edges; optional 2–4 frame camera shake on the beat null.

## 11. Charts and counters

- Bars/lines as shape layers; draw lines with Trim Paths; bars grow from a
  baseline (anchor at the base, Scale Y).
- Counters: a Slider on `CTRL_VOX` animated with ease-out, read by a Source
  Text expression with locale formatting (ae-expressions-rigs). Numbers must
  come from the client's validated data.

## 12. Archival footage treatment

| Step | Effect |
| --- | --- |
| Desaturate | Black & White (`ADBE Black&White`) or Hue/Saturation (`ADBE HUE SATURATION`) |
| Crush and age | Curves (`ADBE CurvesCustom`), Tint (`ADBE Tint`) towards warm paper |
| Grain | Add Grain (`VISINF Grain Implant`) or Noise (`ADBE Noise`) at master level |
| Flicker | an exposure/brightness wiggle held per 2 frames (ae-expressions-rigs) |
| Gate weave | stepped 0.5–1.5 px position jitter on the footage precomp |
| Frame | torn-paper alpha as a track matte, plus a white border via Minimax |

Keep source speed native and record IN/OUT per ae-production-workflow.

## 13. Red string between pinned items

A shape layer path driven by two pin layers (expression in ae-expressions-rigs),
stroke 2–4 px in accent red (LED ≥ 3 px), slight sag via a midpoint, pins as
small shape circles with a drop shadow. Animate the string with Trim Paths after
both pins have landed.

## 14. Transitions between beats

- Paper slide/flip: the next beat's ground enters as a torn sheet (fast in,
  soft settle) — hide the cut under motion.
- Match cut on a shape: a circle annotation becomes the next beat's map pin.
- Camera whip on the master null with motion blur, 6–10 frames.
- Hard cut on a word is often the best editorial transition; do not decorate
  every cut.

Every transition element must extend to the actual last frame of its beat and
leave no gap in the ground.
