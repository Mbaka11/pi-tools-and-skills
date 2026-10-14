# Composite integration QA

Run on the master composition, at 100% and 200%, on the frames listed in the
shot plan (first, last, fastest motion, closest subject, every cut).

## Checklist

| Check | Pass condition | How |
| --- | --- | --- |
| Matte core | no holes, no transparency inside the subject | alpha view, levels pushed |
| Matte edge | no hard cut-out line, no dark or coloured halo | 200% on hair, fingers, motion-blurred edges |
| Spill | no green/blue/magenta cast on skin and edges | vectorscope or Info panel samples |
| Temporal stability | no edge chatter or boiling between frames | play at full rate, step frame by frame |
| Black point | darkest foreground values match the plate's darkest | Info panel on shadows |
| White point | highlights clip like the plate (or not at all) | Info panel on brights |
| Colour temperature | foreground light matches the plate's key light | compare neutral areas |
| Light direction | shadows and highlights agree with the plate | visual, frame by frame |
| Grain | element grain size and amount match the plate | zoom on a flat area of both |
| Focus | element sharpness matches its depth | compare to plate objects at the same distance |
| Motion blur | element blur matches plate blur on fast frames | step through the fastest motion |
| Contact | objects touching the ground have contact shadows | visual |
| Track | no sliding against the plate | scrub with a test grid enabled |
| Screen mockups | content proportions equal the device's pixel size; emissive blacks | measure corner pin aspect |
| Duration | elements extend through the last frame | check the final frame |
| Licences | every AI/model output has a licence basis recorded | receipt |

## Measuring instead of eyeballing

- Sample RGB values on matched areas (plate vs element) in the Info panel at
  the same frame; record them in `integration_qa.json`.
- Render A/B stills (composite vs plate-only) and a 200% crop sheet of edges.
- After encoding, decode the full file and extract frames from the encoded output
  (video-delivery-qc) — compression can reveal banding and edge artifacts hidden
  in AE previews.

## Residual risks to state

Human review on the final display, the client's rights to the plate and to any
generated element, model licence status, and anything inspected only at preview
resolution.
