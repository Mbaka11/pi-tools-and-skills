# On-site and device tests

Generate the test card and moving-bar video for the exact profile:

```bash
python scripts/led_tool.py testcard --profile led-rollup-516x1032 --out-png card_516x1032.png --out-mp4 card_516x1032.mp4 --seconds 20
```

## What to check on the device

| Element | Pass | Failure means |
| --- | --- | --- |
| Red 1 px border | visible on all four edges | the player crops, overscans or offsets the image |
| White corner marks | all four corners intact | wrong pixel map or rotation |
| 1 px lines / 2 px lines / checkerboard | crisp, no beating | the player or publishing tool rescales the file |
| Colour patches | clean primaries and secondaries | colour mode or calibration issue |
| 11 grey steps | each step distinguishable, darkest still black | brightness/gamma settings |
| Smooth ramp | no strong bands | low bit depth or aggressive re-encoding |
| Text-size bars | readable equivalents at the real distance | text tiers too small for this venue |
| Moving bars (video) | smooth motion, no jump at screen seams | frame drops or unsynchronised players |

Then play the real deliverable:

1. Start-up: does the loop start on the intended first frame?
2. Loop seam: watch three loops; no flash, jump or black frame at the seam.
3. Reading test: someone unfamiliar reads each message at the real distance
   while walking; if they cannot finish, lengthen the hold or cut words.
4. Brightness: check in the real ambient light; reduce brightness if whites
   glare (comfort and power draw).
5. Camera test: film the screen with a phone; severe moiré on fine textures
   means simplifying the pattern.

Record results (date, device, player/firmware if visible, file names, issues)
in the project's delivery notes. A screen test on one roll-up does not prove
sync across a wall.
