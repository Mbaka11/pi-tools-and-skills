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

## Helper contract

`proxy_audit.py media source proxy` invokes ffprobe with `-count_frames`, stream
and format metadata, a file-only protocol whitelist and a per-input timeout
(default 300 seconds, configurable from 1 to 3600). It hashes each regular input
and checks for changes during its probe/hash pass. It is not a sandbox for
untrusted decoders or malicious local playlists; isolate unfamiliar media.

`json source-probe.json proxy-probe.json` compares supplied snapshots only.
Their hashes identify **JSON bytes**, not media. Inputs are capped at 1 MiB and
64 streams each; duplicate fields, malformed/nonfinite JSON and empty inputs
are rejected. Raw paths, tags, reel names and timecode strings are not printed.
Basic numeric metadata is reported; a digest may still be sensitive.

Exit codes and verdicts:

- **0 / metadata-compatible** — every supported metadata comparison passed.
- **1 / mismatch** — at least one comparison failed; inspect unknowns too.
- **3 / incomplete** — no known mismatch, but required metadata is absent or
  ambiguous. **This is not a pass.** Missing values do not compare equal.
- **2** — invalid input, missing/failed ffprobe, timeout or output conflict.

Decoded counts use `nb_read_frames`, not container-declared `nb_frames`. Frame
rates are exact fractions. Raster policy requires equal-size or uniform integer
reduction, matching SAR and declared rotation; unusual proxy strategies need
manual review. Stream duration may use its own ticks/timebase, **not another
stream's container duration**. Duration tolerance is at most half a frame and
10 ms; start offsets use 1 ms. Audio compares stream order/count, rate, channel
count/layout, start and duration, not samples or speech.

`--report` exclusively creates a new JSON file in an existing parent directory.
No media is written. Full cadence/VFR, image correspondence, channel content,
subframe sync, complete integrity and native attach/export remain unverified.
The result is a bounded metadata audit, never an approval receipt.

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
and VFR conversion were not tested by this example. The additional JSON-mode
example uses **hand-authored illustrative probe snapshots**, not an actual
ffprobe capture. It demonstrates an incomplete verdict when timecode/reel IDs
are absent. The dedicated media CI separately exercises media mode with ffprobe.

## Sources

Consulted 2026-10-16; Adobe pages were checked through indexed excerpts where
HTTP 403 prevented a direct fetch. Menu names and limits are version-dependent.

- [Adobe — ingest and proxy workflow](https://helpx.adobe.com/premiere/desktop/organize-media/ingest-proxy-workflow/ingest-and-proxy-workflow.html).
- [Adobe — attach proxies](https://helpx.adobe.com/uk/premiere/desktop/organize-media/ingest-proxy-workflow/attach-proxies-to-full-resolution-media.html).
- [FFmpeg — documentation](https://ffmpeg.org/ffmpeg.html).
- [OpenTimelineIO — adapters](https://opentimelineio.readthedocs.io/en/latest/api/python/opentimelineio.adapters.html). Apache-2.0; optional, not installed. Verify the exact adapter/version's capabilities.
