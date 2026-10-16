# Dialogue repair and review

| Problem | First action | Failure to listen for |
| --- | --- | --- |
| Isolated click | Local repair/crossfade on a duplicate | Lost consonant or new boundary click |
| Mains hum | Confirm fundamental/harmonics; narrow treatment | Hollow voice from overly broad cuts |
| Wind/plosive | Local attenuation/EQ, alternate mic/take | Whole voice thinned by global filtering |
| Steady hiss | Noise-only reference, modest spectral reduction | Metallic/watery tails, pumping |
| Clipped capture | Alternate take/mic; cautious restoration trial | Fabricated transients; no promise of recovery |
| Reverb/competing voice | Improve source choice; restrained enhancement | Missing words, altered timbre, unstable room |
| Uneven phrases | Clip gain and manual rides before compression | Breaths over-amplified, flattened emphasis |

## Local test recipe

For an approved short excerpt, after inspecting its actual noise floor:

```sh
ffmpeg -hide_banner -nostdin -n -i dry-excerpt.wav -af "highpass=f=80,afftdn=nr=6:nf=-35" -c:a pcm_s24le repaired-excerpt.wav
```

This is a **test**, not an all-voice preset. `nr` is reduction in dB; `nf` is
an assumed noise floor in dB. Tune from the real source and compare to bypass.
The command preserves input rate/channel count by default; inspect both.
Filters can change delay or tails, so compare duration and sync, and retain dry
handles. A quieter noise-only interval does not prove cleaner dialogue.

## Review note template

```text
Source ID / hash / channel: ...
Repair ranges and diagnosed issues: ...
Chain / settings / plugin versions: ...
Dry and processed A/B references: ...
Meaning, breaths, consonants, tails, channel/phase checks: pending / findings
Alignment and measured loudness/true peak: ...
Human listening: who, playback paths, result; or explicitly not performed
Remaining defects / alternate take needed: ...
```

The gallery uses generated harmonic bursts, hum and seeded noise, **not a voice**.
It measures a known noise-only interval and preserves the three-second sample
count. It does not demonstrate semantic fidelity, natural speech quality,
latency correction, loudness-matched audition or a native Enhance Speech run.

## Sources

Consulted 2026-10-16; Adobe guidance from indexed excerpts where direct fetching
returned 403. No upstream audio or plugin is copied.

- [Adobe — repair dialogue](https://helpx.adobe.com/premiere/desktop/add-audio-effects/adjust-volume-and-levels/repair-dialogue.html).
- [Adobe — Enhance Speech](https://helpx.adobe.com/in/premiere/desktop/add-audio-effects/adjust-volume-and-levels/enhance-speech.html).
- [Adobe — noise reduction and restoration](https://helpx.adobe.com/audition/desktop/effects-reference/noise-reduction-restoration-effects.html).
- [FFmpeg — afftdn](https://ffmpeg.org/ffmpeg-filters.html#afftdn).
