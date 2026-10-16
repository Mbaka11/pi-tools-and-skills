---
name: montage-dialogue-cleanup
description: Conservative dialogue and voice-over post-production - choose and sync microphones, repair clicks/hum/noise, preserve breaths and room tone, balance clip gain, apply restrained EQ/de-essing/compression, review enhancement artifacts and export aligned dialogue stems. Use for noisy interviews, podcast cleanup, voice-over repair, hiss, hum, plosives, reverb or uneven speech. Complements sound-design-sfx without changing a speaker's words or identity.
compatibility: Any audio-capable NLE/DAW; Premiere Essential Sound and Audition optional. FFmpeg filters are local optional examples. Cloud enhancement, models and voice generation require separate authorization and rights checks.
metadata:
  version: "1.0.0"
  short-description: Intelligible speech with reversible cleanup and honest QA
---

# Montage dialogue cleanup

[Tiny example — actual filtering of synthetic noise and tone bursts](../../../examples/README.md#montage-dialogue-cleanup).

Intelligibility before loudness. Remove distraction without erasing consonants,
changing words, inventing speech or making the room disappear between phrases.

## Diagnose before processing

Work on a duplicate or non-destructive effect chain. Keep the unprocessed files
and channel mapping. Listen to loud speech, quiet speech, breaths, pauses and
noisy transitions; mark representative time ranges. If listening is unavailable,
state that clearly and produce a provisional test, not an approved dialogue mix.

1. Choose the best mic/channel. Fix synchronization first with
   [montage-multicam-sync](../montage-multicam-sync/SKILL.md).
2. Distinguish clipping, hum, steady hiss, wind/plosives, clicks, reverberation
   and competing speakers. A single denoise preset does not solve all of them.
3. Capture clean room tone from the same setup, not a phrase containing speech.
   Keep pauses meaningful; do not automatically delete all low-level regions.
4. Check phase/comb filtering before mixing boom/lav/scratch tracks together.

## Conservative chain

- **Edit/clip gain first:** repair isolated clicks and abrupt boundaries, use
  short appropriate crossfades, level obvious take-to-take differences.
- **Targeted repair:** narrow hum treatment or a voice-appropriate high-pass
  only when justified. Do not assume 80 Hz is right for every voice.
- **Light denoise:** short preview, modest reduction, compare bypass at similar
  loudness. Listen for watery tails, pumping and consonant loss. Stop earlier
  than the point where the noise disappears but speech becomes synthetic.
- **EQ/de-ess/compress:** correct an actual problem, not a preset checklist.
  Control sibilance and dynamics without lisping or flattening emphasis.
- **Room tone and transitions:** keep acoustic continuity between takes.
- **Final gain/limiting:** after editing and repair; measure the final programme
  against its delivery spec, not a universal podcast LUFS rule.

See [repair decision table and test recipe](references/repair-and-review.md).

## Native and generated enhancement

Premiere's Essential Sound repair and Enhance Speech controls can provide a
starting point; use the mix amount and audition the exact processed result.
Audition spectral tools can target local defects instead of processing a whole
interview. Menus and capabilities depend on the installed version.

Do not silently upload private recordings. Confirm the provider, content rights,
retention policy, spend and authorization before external processing. Do not
clone a voice or generate replacement words as a "cleanup" operation. Verify
names, negatives and numbers against the original after any generative enhancer.

## Acceptance and deliverables

- Speech meaning, identity, timing and channel intent are intact.
- Start/middle/end sync and transitions checked after processing; compensate
  plugin latency only after measuring it, not by guessing.
- Normal-speed human listening completed on headphones and a small speaker,
  or explicitly marked pending. A waveform/noise metric cannot certify speech.
- Deliver a zero-aligned 48 kHz/24-bit DX stem when requested, preserving the
  agreed mono/stereo/multichannel layout, plus a dry alternate and repair note.
- Route music/SFX/ducking to [sound-design-sfx](../sound-design-sfx/SKILL.md),
  then measure the encoded mix with [video-delivery-qc](../video-delivery-qc/SKILL.md).
