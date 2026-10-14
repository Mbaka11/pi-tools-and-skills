# LED design rules

## Pixels, pitch and size

- **Pixel pitch** (mm between LED centres) fixes the pixel map:
  `pixels = physical size (mm) / pitch (mm)`. PixaNova roll-ups are P1.86:
  960 × 1920 mm active area → 516 × 1032 px per screen.
- **Author at the pixel map.** A 1080×1920 design downscaled to 516×1032 loses
  half its detail and blurs thin type. If a higher-resolution master is useful
  for other deliverables, build the LED version separately.
- **Pixel-snap** static text and thin shapes (ae-expressions-rigs) so edges do
  not straddle two LED pixels.

## Minimum text size

`led_tool.py text-size` implements the published Nummax method:

```text
minimum character height (cm) = reading distance (cm) / 150 × movement coefficient
minimum height (px) = minimum height (mm) / pitch (mm)
```

Movement coefficients: static 1.0, pedestrian 1.2, parking 1.6, quiet street
2.0, normal traffic 2.6. This minimum is for the smallest *detail* line; the
toolbox recommends ×1.5 for information and ×2.5 for the hook. Example at P1.86,
4 m, pedestrians: detail ≥ 18 px cap height, information ≥ 26 px, hook ≥ 44 px.

Convert cap height to an AE font size with the font's cap-height ratio (about
0.7 for many sans-serifs; measure it). Prefer sturdy sans-serif families with
open counters; avoid script, hairline, condensed-light and thin serif styles.

## Hierarchy and copy

- One message per screen; at most about 7–10 words for passers-by.
- Hook → information → detail; never three equally loud lines.
- Prime zone: the upper third of a floor-standing roll-up is at eye level.
  Keep the key line there; the logo can sit high or low but not in the bottom
  occlusion band.
- Prices and legal mentions follow the client's approved wording exactly
  (for example "À partir de 2 450 $, taxes en sus").

## Contrast, brightness and colour

- Dark or saturated grounds with light text read best and draw less power.
- Avoid large pure-white fields: at event brightness they glare, wash out
  neighbouring text and look like a lamp. Keep big areas below about 85% white
  and limit full-white surfaces.
- Black is "off" on LED: true black backgrounds disappear into the frame, which
  can be desirable for floating elements.
- Very saturated reds and blues can bloom; test small red text on the device.
- Gradients: smooth, wide gradients can band after H.264; add subtle noise in AE
  or widen the gradient, and check the encoded file.

## Thin lines, patterns and moiré

- Lines and strokes at least 3–4 px at 516 px width; 1 px details vanish or
  shimmer.
- Avoid fine stripes, checkerboards, small halftone dots and dense textures:
  they beat against the LED grid and against phone cameras filming the booth.
- Paper grain, film grain and noise: larger and subtler than for web, or none.

## Motion

- Motion should help reading: entrances settle, then text holds still.
- Slow pans of text cause judder on low-resolution grids; prefer cuts, slides
  that settle, and scale/fade arrivals.
- Avoid strobing, rapid full-frame flashes and high-contrast flicker (comfort
  and photosensitivity).
- Constant frame rate (30 fps default). No variable frame rate sources.

## Loops and programmes

- Any frame may be a viewer's first: make each message self-contained, show the
  brand at least every 8–10 s.
- Typical loop 15–30 s, 3–5 messages. Event programmes (schedules) can be longer
  with a stable header.
- The loop seam must be invisible: same ground and camera state at first and
  last frame; verify with `media_qc.py --loop-check`.
- No audio track unless the device has sound and the brief asks for it.

## Multi-screen walls

- Ask whether one processor drives the full wall (one file) or each roll-up has
  its own player (one file per screen, `led_tool.py split`).
- Independent players can start a few frames apart. Do not run fast motion or
  key text across seams unless sync has been verified with the test video.
- Design each screen to read alone as well as together (people see one screen
  at a time from close range).

## File delivery

- Default: MP4, H.264 High, yuv420p, BT.709 tags, 30 fps CFR, CRF ~16–18 with a
  12 Mbit/s cap, no audio, faststart, exact pixel size.
- Players such as NovaStar Taurus and Huidu A-series decode H.264 well above
  these sizes and bitrates; the limiting factor is usually upload, storage or a
  conversion step in the publishing software. If the publishing tool converts
  files, test the converted result.
- Naming: `CLIENT_MESSAGE_WIDTHxHEIGHT_FPSp_vNN.mp4`
  (for example `CLIENT_PROMO_516x1032_30p_v02.mp4`), plus `_S1`, `_S2`… per
  screen for split walls.
