# Native AE compositing recipes

Effect match names are given for scripted or bridge calls; verify them with
`ae_list_effects` on the installed version.

## Keying (green/blue screen)

1. **Garbage matte** first: a loose tracked mask removing rigs and screen edges.
2. **Keylight** (`Keylight 906`): pick Screen Colour from a mid-tone of the
   screen near the subject. View *Screen Matte*. Raise Clip Black until the
   background is solid black, lower Clip White until the core is solid white;
   keep Screen Shrink/Grow and Softness small (−2…+1, 0–2). Do not crush edges
   to fix a noisy screen — split the work instead:
   - **core matte**: aggressive key, choked, holds the interior;
   - **edge matte**: soft key for hair and motion blur;
   - combine (core over edge) in a matte precomp.
3. **Key Cleaner** to recover edge detail, then **Advanced Spill Suppressor**
   for colour spill (look up their match names with `ae_list_effects` before
   scripting). Check skin tones after despill.
4. Refine with Matte Choker / Simple Choker 0.5–1.5 px only after the edge looks
   right in context, not on black.

Uneven screens: key in sections with separate masks, or use a clean-plate
difference where a clean plate exists.

## Rotoscoping

- **Roto Brush** for organic subjects: strokes on key frames, propagate, use
  Refine Edge on hair; freeze the result once approved to avoid recomputation.
- **Masks** for hard surfaces: fewer points, track with the mask tracker or
  Mocha, feather per vertex where motion blur varies.
- Roto the subject a little inside the edge, then build the edge with a
  feathered/blurred version — never one hard mask for both.

## Cleanup and object removal

- **Content-Aware Fill** (*Window › Content-Aware Fill*): mask the object (with
  tracking), choose Object, Surface or Edge Blend fill, add reference frames for
  hard shots. Render the fill layer, then review every frame in motion.
- **Clone/patch**: a tracked patch from a clean area, feathered, with grain
  matched afterwards. Best for small static areas (logos on walls, signs).
- Logos or trademarks visible by accident in client footage: remove or blur per
  the client's rights instructions.

## Tracking

| Need | Tool |
| --- | --- |
| Flat surface (screen, poster, roll-up, wall) | **Mocha AE** planar track → export corner pin to a Corner Pin (`ADBE Corner Pin`) |
| Points in 2D | Tracker panel (position/rotation/scale) applied to a null, parent elements to it |
| Camera moving through space | **3D Camera Tracker** → camera + nulls/solids on the ground plane |
| Shaky footage | Warp Stabilizer (do not stack under a tracked composite; track the stabilized plate) |

Always track on the plate's native frame rate and resolution; solve, then
verify with a test grid layer before placing hero content.

## Screen replacement and LED roll-up mockups

Common for proposals: show the client's content on a digital roll-up in a venue
photo or video.

1. Track the screen's four corners (Mocha planar or a still photo's corners).
2. Content precomp at the **device's pixel size** (for example 516×1032) so the
   proportions are true; Corner Pin it to the tracked corners.
3. Emissive look: the screen does not receive room light. Keep its blacks deep,
   add a subtle glow (Glow `ADBE Glo2`, low intensity) and a faint reflection
   pass from the plate (Screen/Add blend, 5–15%) for glass.
4. Edge: a 1–2 px dark bezel and slight defocus matching the plate's focus.
5. Optional realism for close-ups: a pixel-grid overlay at the pitch scale; omit
   it for wide shots (it creates moiré at small sizes).
6. Label mockups as mockups; never present them as photographs of a real event.

## Integration techniques

- **Colour match**: match black point, white point and midtone colour of the
  foreground to the plate using Curves/Levels per channel or Lumetri
  (`ADBE Lumetri`); compare with Info panel readings on dark and bright areas.
- **Light wrap** (no native effect): duplicate the background, blur it, keep it
  only inside a thin band of the foreground edge (foreground alpha minus a choked
  copy), blend Screen/Add at low opacity above the foreground.
- **Edge colour**: slight spill of environment colour on edges, not a clean
  white or green rim.
- **Defocus**: Camera Lens Blur (`ADBE Camera Lens Blur`) matched to the plate's
  depth of field; a depth map can drive it.
- **Motion blur**: layer motion blur with shutter angle matching the footage
  (often 180°); for footage-based elements use Pixel Motion Blur or CC Force
  Motion Blur sparingly.
- **Shadows and contact**: duplicate the matte, fill black, Corner Pin/skew onto
  the ground plane, blur with distance, Multiply at 30–60%; add a tight contact
  shadow where the object touches the ground.
- **Atmosphere**: haze proportional to distance (depth map or gradients).
- **Grain**: match with Match Grain or Add Grain (`VISINF Grain Implant`)
  analysed on a flat area of the plate; apply once, on top of the composite
  elements, not on the plate.

## Sky and background replacement

Key or roto the sky, keep the edge soft, colour-match the foreground to the new
sky's light (direction and temperature), add haze on distant elements, track
the new sky to the camera move, add grain. Reflections in windows and water
must change too, or the swap reads as fake.
