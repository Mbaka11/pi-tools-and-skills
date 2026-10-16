# Timing math and artifact review

## Constant-speed example

The gallery uses a synthetic 60 fps source and a 30 fps output:

| Source frame interval | Source seconds | Speed | Output seconds | Output frames |
| --- | --- | --- | --- | --- |
| [0,60) | [0,1) | 1× | [0,1) | [0,30) |
| [60,90) | [1,1.5) | 0.5× | [1,2) | [30,60) |
| [90,210) | [1.5,3.5) | 2× | [2,3) | [60,90) |

Total source consumption is 3.5 s; output is 3 s / 90 frames. This is a
**piecewise constant speed demonstration**, not a smooth Bezier speed ramp.
No optical flow or third-party model is used. The GIF is a 10 fps preview of
the actual encoded MP4, not a second independent animation. The selected source
frames are explicitly checked with decoded-frame SHA-256 before the final lossy
encode: 0,2,…,58; then 60,61,…,89; then 90,94,…,206. Output frames 0/30/60
therefore begin on source frames 0/60/90. The encoded file is checked separately
for frame count, duration and timestamps.

For output time `t`, source time is the accumulated integral of speed over
output time: `source(t) = source_start + integral(speed(u), u=0..t)`.
Positive speed maps forward; zero speed holds; negative speed reverses. Split
at cuts and reversals; endpoint and audio handling need explicit decisions.

## Timestamp proof recipe

For a confirmed constant-rate, video-only source:

```sh
# Twice as fast. Explicitly silent; do not discard client audio without approval.
ffmpeg -hide_banner -nostdin -n -i source.mp4 -an -vf "setpts=(PTS-STARTPTS)/2,fps=30" -c:v libx264 -pix_fmt yuv420p fast-review.mp4
```

Changing `-r` alone is not the same operation. For pitch-preserved audio,
`atempo=2` changes tempo, while `asetpts` alone changes timestamps rather than
creating a correctly stretched waveform. Validate the local filter's supported
range; chain supported factors when necessary and check tails/channel layouts.

A piecewise graph uses `split`, per-branch `trim` and `setpts`, an explicit
output cadence, then `concat`. `trim` end frames are exclusive. Count every
branch before trusting the total; avoid filling a mistake with a duplicated
last frame just to hit a duration. The generator records its actual graph.

## Review traps

- All frame-rate fractions must remain exact until a deliberate frame-grid
  rounding. 29.97 and 30000/1001 are not mathematically identical.
- At every speed boundary, inspect source continuity and output pacing. A hard
  speed step may be intentional; a skipped action peak usually is not.
- Optical flow must be checked on hands, faces, edges, reflections and flashes.
  Disable or switch methods locally when artifacts are worse than sampling.
- Reverse buffering can consume substantial RAM. Limit the source segment
  before reversing; do not casually buffer a feature-length clip.
- Interchange adapters often lose non-linear remaps. Provide a reference render,
  handles and native project; test the recipient's exact software version.

## Sources

Consulted 2026-10-16; Adobe guidance checked through indexed excerpts when direct
fetching returned 403, not through a connected application.

- [Adobe — speed and duration methods](https://helpx.adobe.com/uk/premiere/desktop/edit-projects/change-clip-speed/different-ways-to-change-clip-speed-and-duration.html).
- [Adobe — time interpolation](https://helpx.adobe.com/premiere/desktop/edit-projects/change-clip-speed/apply-time-interpolation-methods-to-adjust-clip-speed.html).
- [FFmpeg — setpts/asetpts](https://ffmpeg.org/ffmpeg-filters.html#setpts_002c-asetpts), [trim](https://ffmpeg.org/ffmpeg-filters.html#trim), [atempo](https://ffmpeg.org/ffmpeg-filters.html#atempo).
