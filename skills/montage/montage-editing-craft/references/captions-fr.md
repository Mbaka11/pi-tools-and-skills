# Captions and subtitles (French focus)

## Presets in srt_check.py

| Preset | Max chars/line | Max lines | Max CPS | Min / max duration | Min gap |
| --- | --- | --- | --- | --- | --- |
| `broadcast` | 42 | 2 | 17 | 0.833 s / 7 s | 0.083 s |
| `social-landscape` | 42 | 2 | 17 | 0.7 s / 6 s | 0 |
| `social-vertical` | 32 | 2 | 17 | 0.7 s / 5 s | 0 |

CPS counts every visible character including spaces and punctuation. Client or
broadcaster style sheets override these values (`--max-chars`, `--max-cps`).

## French typography

- Colon: no-break space before (`Bonjour : …` with U+00A0).
- `;` `!` `?`: fr-FR uses a narrow no-break space before; fr-CA commonly uses
  none (or a narrow no-break space in careful typography). Never a regular
  space — it can wrap the mark onto the next line. Use `--french fr-CA` or
  `--french fr-FR` accordingly.
- Guillemets « » with no-break spaces inside; numbers with a no-break space as
  thousands separator (`2 450 $`), and a no-break space before `$` and `%`.
- U+202F (narrow no-break space) is typographically ideal but missing from some
  fonts and some players; `--space nbsp` (U+00A0) is the safe default.
- Prefer `…` over `...`, and typographic apostrophes `’` if the font has them.

## Line breaking

- Break at natural linguistic units: after punctuation, before conjunctions and
  prepositions; never split an article from its noun or a number from its unit.
- Bottom line usually longer than the top (pyramid) for readability; for burned
  social captions keep one idea per caption.
- Keep captions out of platform UI zones (video-delivery-qc platform specs).

## Timing

- Start when the speech starts (or up to 2–3 frames earlier); end with the
  speech plus a short linger; respect shot changes (avoid captions straddling a
  cut by a few frames).
- Reading speed above the limit: condense the text faithfully rather than
  shortening the display time.

## Transcription options

| Option | Notes |
| --- | --- |
| Higgsfield connector speech-to-text | per the bridge instructions; send compact audio (for example `pr_render_audio_edl` MP3) |
| Local Whisper family (faster-whisper, whisperX) | open-source, runs on GPU; word timestamps; good French; check model size vs VRAM |
| ElevenLabs speech-to-text | API key; word timestamps and diarization |

Always review names, brands, numbers and Québec terms by a human; automatic
transcripts mis-hear proper nouns.

## Burn-in vs sidecar

- Sidecar SRT/VTT: accessible, editable, platform-dependent styling.
- Burned (open) captions: guaranteed look on social; design them in the NLE/AE
  so fonts and safe zones are controlled. Premiere through the bridge:
  `pr_create_caption_track`.
- Deliver the SRT too, even when burned, for accessibility uploads.
