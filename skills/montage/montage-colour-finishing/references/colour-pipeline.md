# Colour pipeline checks

## Troubleshooting by symptom

| Symptom | Check before changing the grade |
| --- | --- |
| Log footage looks flat | Input identification and technical conversion; not an arbitrary contrast LUT |
| Image is crushed or over-saturated | Duplicate input LUT/automatic transform, wrong range interpretation |
| HDR clip looks wrong in SDR | Correct HLG/PQ interpretation and deliberate tone mapping |
| Export differs from timeline | Output transform, transfer/primaries/matrix/range tags, player/display management |
| Two cameras never quite match | Different light/sensors, exposure, white balance and gamut before a creative look |
| Skin changes during a shot | Moving qualifier, mixed illumination, automatic exposure/white balance |

## Inspect, do not assume

With separately installed ffprobe, inspect a video stream without modifying it:

```sh
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,pix_fmt,color_range,color_space,color_transfer,color_primaries -of json grade-review.mp4
```

Missing tags mean unknown, not Rec.709. A `-color_trc`/`-colorspace` output flag
labels a stream; it does not by itself perform a pixel conversion. FFmpeg
`colorspace`, `zscale`, `tonemap` and `lut3d` require correct input assumptions,
build support and an agreed output target. Do not use one universal HDR recipe.

## Minimal grade note

```text
Input: camera A / confirmed capture profile; camera B / confirmed capture profile
Working space: recorded from the actual sequence
Output: agreed SDR Rec.709 or specified HDR delivery
Transforms: input conversion -> shot balance -> look -> output conversion
Reference: source ID + exact source frame
Review: scopes checked; exported-file comparison checked; calibrated display pending
```

## Synthetic example boundary

The gallery introduces a known RGB channel gain error and reverses it using
FFmpeg `colorchannelmixer`. Pixel error is measured against the original chart.
This is an **8-bit RGB arithmetic demonstration**, not a camera log transform,
HDR tone-map test, skin-tone grade or monitor calibration. No LUT is distributed.

## Sources

Consulted 2026-10-16; Adobe guidance was available through indexed excerpts when
direct page fetches returned HTTP 403. Confirm UI/version details in the host.

- [Adobe — configure clips for colour management](https://helpx.adobe.com/premiere/desktop/correct-color/set-up-color-management/color-management-using-clip-modify.html).
- [Adobe — tone mapping](https://helpx.adobe.com/premiere/desktop/correct-color/set-up-color-management/tone-mapping-in-premiere.html).
- [Adobe — match colour between shots](https://helpx.adobe.com/premiere/desktop/correct-color/add-color-effects/match-color-between-shots.html).
- [FFmpeg — filter reference](https://ffmpeg.org/ffmpeg-filters.html#colorchannelmixer).

These are references, not copied documentation or permission to redistribute LUTs.
