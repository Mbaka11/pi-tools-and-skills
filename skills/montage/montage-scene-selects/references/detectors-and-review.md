# Detector choices and boundary review

| Method | Useful for | Important limitation |
| --- | --- | --- |
| FFmpeg `scdet` | Quick hard-change candidates without a model | Brightness changes and flashes can trigger; subtle cuts can be missed |
| PySceneDetect content detector | Hard cuts with configurable content metrics | Fast camera movement can resemble a cut |
| PySceneDetect adaptive detector | Relative change against neighboring-frame activity | Reduces some motion false positives, not semantic proof |
| Threshold/fade analysis | Dark fades and intensity changes | Does not identify every dissolve or editorial transition |
| Manual marker/log | Context, action peaks, speaker/content decisions | Requires source review and a recorded rationale |

PySceneDetect's adaptive method uses a rolling average of adjacent content
changes. Tune against known boundaries and false positives, then inspect the
result. Do not install it just to reproduce the small FFmpeg-only gallery.
Its BSD-3-Clause source licence does not license the footage being analyzed.

## Selects CSV example

```csv
source_id,in_frame,out_frame,decision,purpose,review_status
SYNTH_A,0,30,keep,establish shape,fictional-example
SYNTH_A,30,60,maybe,detail,fictional-example
SYNTH_A,60,90,keep,resolve,fictional-example
```

These rows illustrate structure, not real editorial approval. For VFR media,
retain exact decoded PTS and a rational timebase instead of inventing a nominal
frame number. A low-resolution proxy may suppress subtle changes; inspect
questionable candidates against original-resolution frames.

## Gallery proof

The generator creates three original one-second shots at 30 fps, runs `scdet`,
records the observed candidate times/scores and checks that they occur at 1 s
and 2 s. A contact sheet comes from the encoded MP4. This controlled hard-cut
case is not a benchmark for documentaries, fades or camera motion.

## Sources

Reviewed 2026-10-16. No upstream code, weights or demo media are copied.

- [FFmpeg — scdet](https://ffmpeg.org/ffmpeg-filters.html#scdet-1); filter options also checked against local FFmpeg 7.1.
- [PySceneDetect — detector documentation](https://www.scenedetect.com/docs/latest/api/detectors.html).
- [Reviewed PySceneDetect source and licence finding](../../../../docs/montage-catalog.md#additional-editing-references-2026-10-16).
