# Anchor calculator contract

`sync_map.py` reads a local JSON document, at most 64 KiB, with one or two
anchors. It never opens media, runs an engine, downloads or changes originals.

```json
{
  "schema": 1,
  "reference_rate": "30",
  "camera_rate": "30",
  "anchors": [
    {"reference": "f15", "camera": "f21"},
    {"reference": "f75", "camera": "f81"}
  ]
}
```

Rates accept exact fractions such as `30000/1001`, from 1 to 240 fps. Decimal
seconds and frame indices must be nonnegative and no more than 24 hours from
source zero. `f0` means the first decoded frame. Use exact rational rate strings,
not rounded `29.97`, when the source is actually `30000/1001`.

## Equation and sign

For anchors `(c1,r1)` and `(c2,r2)`:

```text
scale = (r2 - r1) / (c2 - c1)
offset = r1 - scale*c1
reference_time = scale*camera_time + offset
source playback speed percent = 100/scale
duration correction ppm = (scale - 1)*1,000,000
```

With one anchor, scale is assumed to be 1 and drift is **unknown**. Two anchors
must advance strictly in both sources. A configurable absolute drift threshold
(default 1,000 ppm) adds a warning; it does not approve or apply a correction.
The ppm sign describes **duration scaling**, not a recorder's oscillator error.

A negative offset means camera start falls before reference zero; keep negative
pre-roll if the NLE supports it, shift the common origin, or deliberately trim a
working copy. Do not trim original media. A positive offset creates a leading
gap on the reference timeline. Round only when placing on the target timeline;
keep the fractional result for subframe audio decisions.

## Output and failures

JSON includes the exact scale/offset fractions, decimal display values, mapped
anchor residuals, the drift assumption and explicit limits. `ok=true` means valid
arithmetic, not verified sync. `--out` creates a **new** file exclusively and
refuses overwrite; stdout also contains the same result. It does not create
missing parent directories. Exit 0 means a valid plan (warnings may remain);
exit 2 means malformed data, invalid ranges, missing input or output conflict.

The parser rejects unknown/duplicate fields, nonfinite values, invalid frame
indices, unsupported schema, overlarge inputs and non-increasing anchors.
No source paths or raw media metadata are embedded in the output.

## Sources

- [Adobe — multi-camera source sequences](https://helpx.adobe.com/uk/premiere/desktop/edit-projects/set-up-multi-camera-sequences-for-editing/create-a-multi-camera-source-sequence.html), indexed guidance checked 2026-10-16; native execution not performed.
- [FFmpeg — trim and timestamp filters](https://ffmpeg.org/ffmpeg-filters.html#trim). `trim` selects frames but does not reset timestamps; follow with `setpts` when building a zero-aligned working copy.

The helper and equations were written for this toolbox; no third-party sync
implementation is copied. The demo uses known synthetic anchors, not a waveform
correlator or a confidence score fabricated from two points.
