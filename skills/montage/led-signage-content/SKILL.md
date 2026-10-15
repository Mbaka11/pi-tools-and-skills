---
name: led-signage-content
description: Plan, design, export and verify content for LED signage - generic digital roll-ups (for example 516x1032 per screen, P1.86), two- and three-screen walls (1032x1032, 1548x1032), LED posters and event screens. Covers device profiles, pixel-exact authoring, minimum text size from pixel pitch and viewing distance, readable loops for passers-by, contrast/brightness/moire rules, silent-loop structure, H.264 exports for LED players, per-screen splits for walls, test cards for on-site checks, and French client intake. Use for any "écran LED", "roll-up numérique", affichage dynamique, digital signage or trade-show screen deliverable.
compatibility: Python 3.9+ for scripts/led_tool.py (no packages required). FFmpeg on PATH, via $FFMPEG, or the imageio-ffmpeg Python package for export/split/check/test videos. Works with any editor; After Effects skills in this toolbox apply for builds.
metadata:
  version: "1.1.0"
  short-description: LED roll-up and wall content that reads and plays correctly
---

# LED signage content (digital roll-ups and walls)

[Tiny example — real 3 s LED export, test card and guides](../../../examples/README.md#led-signage-content).

LED screens show every pixel, have true blacks, and are read by people walking
past a noisy booth. Content that looks fine on a laptop fails on the device
when it is scaled, too small, too thin, too bright or too long.

## Start every LED job with five facts

1. **Device and pixel map** — profile from `scripts/led_profiles.json`
   (`led-rollup-516x1032`, `led-wall-2x-516x1032`, `led-wall-3x-516x1032`)
   or a new measured profile. These are generic examples, not certified hardware
   specifications. Confirm pixel map, pitch and whether each screen has its own player.
2. **Context** — trade show, conference, retail; viewing distance range;
   moving or seated audience; what may block the bottom of the screen.
3. **Player and file rules** — player brand/model if known, accepted container
   and codec, frame rate, loop behaviour, scheduling, USB/Wi-Fi/cloud upload.
   Default when unknown: H.264 High, yuv420p, 30 fps CFR, MP4 with faststart,
   no audio — then test on the device.
4. **Messages and mentions** — exact approved copy, prices with taxes wording,
   legal mentions, logo files, fonts with licences (intake sheet:
   `references/client-intake-fr.md`).
5. **Loop** — total length, number of messages, how often the brand appears,
   whether an offer stays visible.

## Workflow

1. **Profile and guides.** Generate a guide overlay at the exact size and import
   it into AE as a guide layer:

   ```bash
   python scripts/led_tool.py guides --profile led-rollup-516x1032 --distance 4 --out guides_516x1032.png
   ```

   It marks the safe margin, the upper-third prime zone (eye level on a 1.92 m
   screen), the bottom occlusion-risk band (tables, people), screen seams for
   walls, and bars showing minimum text heights.
2. **Text sizes.** Compute the tiers for the real reading distance:

   ```bash
   python scripts/led_tool.py text-size --profile led-rollup-516x1032 --distance 4 --movement pedestrian
   ```

   Use `detail` only for the smallest secondary line; messages use
   `information` or `hook`. Measure the font's actual cap height in AE.
3. **Design** with `references/led-design-rules.md`: one message per screen,
   strong contrast on dark grounds, thick strokes, no hairlines, controlled
   white areas, slow readable motion, loop seam planned.
4. **Build** at the exact device size (After Effects: ae-production-workflow,
   and ae-vox-editorial for editorial looks). Silent unless the brief says
   otherwise. For walls, decide whether critical text may cross seams (only
   when one processor drives the whole wall in sync).
5. **Export** pixel-exact (a master from AE at device size is the input):

   ```bash
   python scripts/led_tool.py export --profile led-rollup-516x1032 --input master.mov --output CLIENT_MSG_516x1032_30p_v01.mp4 --dry-run
   python scripts/led_tool.py export --profile led-rollup-516x1032 --input master.mov --output CLIENT_MSG_516x1032_30p_v01.mp4
   ```

   For walls fed by one player per screen, split from one decode so all files
   share identical frames:

   ```bash
   python scripts/led_tool.py split --profile led-wall-3x-516x1032 --input wall_master.mov --outdir deliver/
   ```
6. **Verify** the encoded files, not the AE comp:

   ```bash
   python scripts/led_tool.py check --profile led-rollup-516x1032 --input CLIENT_MSG_516x1032_30p_v01.mp4
   python ../video-delivery-qc/scripts/media_qc.py CLIENT_MSG_516x1032_30p_v01.mp4 --expect-width 516 --expect-height 1032 --expect-fps 30 --expect-audio no --loop-check --contact-sheet sheet.jpg
   ```
7. **On-site test** with the test card before the event when the player or wall
   is new (`references/on-site-test.md`):

   ```bash
   python scripts/led_tool.py testcard --profile led-wall-3x-516x1032 --out-png card.png --out-mp4 card_sync.mp4 --seconds 20
   ```
8. **Deliver** with a short French note (format, duration, loop, no audio,
   what was verified and what must be tested on the device).

## Non-negotiables

- Author at the exact pixel map or an exact integer multiple reduced by
  `led_tool.py`. Never rely on the player to rescale.
- No critical information in the bottom ~15% of a floor-standing roll-up.
- Every message holds long enough to read (reading-time rule in
  ae-vox-editorial `references/narrative-and-timing.md`).
- The loop's last frame hands off cleanly to the first.
- State what was verified (decode, frame count, loop seam, readability on a
  monitor at 100%) and what was not (real screen, brightness, player, sync).
