# Proxy audit and conform record

## Required comparison

| Property | Review |
| --- | --- |
| Identity | Original full path/relative project ID, card/reel ID and hash; proxy association recorded |
| Time basis | Exact rational frame rate and decoded timestamps; duration and decoded frame count |
| Picture | Divisible raster, same display aspect, rotation, fielding and action on corresponding frames |
| Audio | Same required stream/channel layout and order; sample rate, start offset and end sync checked |
| Metadata | Required source timecode/reel tags retained or association documented and verified in NLE |
| Original untouched | Original hash after the operation matches the ingest record |
| Conform | Original online, proxy export off, detailed output inspected, native project saved |

A matching frame count alone proves neither attachment nor source identity.
Container duration is only a hint. Long-GOP seeking can land on a keyframe;
use decoded frame numbers for identity checks rather than an approximate seek.

## Inspection command

```sh
ffprobe -v error -count_frames -show_streams -show_format -of json proxy-review.mov
```

The report may expose full paths, recording times, device tags or locations.
Keep it in the private project, not in this public toolbox. Missing fields are
not passes; inspect them in the NLE or mark the limitation explicitly.

## Optional simple transcode

For a confirmed progressive, even-sized, square-pixel source, this is only a
**starting recipe**, not a universal Premiere proxy preset:

```sh
ffmpeg -hide_banner -nostdin -n -i original.mov -map 0:v:0 -map "0:a?" -map_metadata 0 -vf "scale=iw/2:ih/2" -c:v prores_ks -profile:v 0 -pix_fmt yuv422p10le -c:a pcm_s24le proxy.mov
```

Check that half-size dimensions are valid. Metadata mapping does not guarantee
preservation of every timecode/data stream; verify the actual output and native
attachment before batching. No frame-rate change, channel collapse or deletion
is authorized by this recipe. ProRes encoding support depends on the local build.

## Gallery boundary

The tiny H.264 pair demonstrates 640×360 → 320×180, unchanged 30 fps and 90
fully decoded frames. H.264 keeps this public download small; it is **not** the
preferred editing codec for every machine. The synthetic pair is silent and has
no camera/reel/timecode metadata. Native attachment, relink, multi-channel audio
and VFR conversion were not tested by this example.

## Sources

Consulted 2026-10-16; Adobe pages were checked through indexed excerpts where
HTTP 403 prevented a direct fetch. Menu names and limits are version-dependent.

- [Adobe — ingest and proxy workflow](https://helpx.adobe.com/premiere/desktop/organize-media/ingest-proxy-workflow/ingest-and-proxy-workflow.html).
- [Adobe — attach proxies](https://helpx.adobe.com/uk/premiere/desktop/organize-media/ingest-proxy-workflow/attach-proxies-to-full-resolution-media.html).
- [FFmpeg — documentation](https://ffmpeg.org/ffmpeg.html).
- [OpenTimelineIO — adapters](https://opentimelineio.readthedocs.io/en/latest/api/python/opentimelineio.adapters.html). Apache-2.0; optional, not installed. Verify the exact adapter/version's capabilities.
