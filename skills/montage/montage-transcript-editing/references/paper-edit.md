# Source-linked paper edits

## Minimal record

| Field | Meaning |
| --- | --- |
| source_id / segment_id | Stable identities, not a fragile filename alone |
| source_rate / origin | Exact rational rate and whether time is source-relative or timecode |
| in_frame / out_frame | Zero-based, start-inclusive/end-exclusive source interval |
| original_text | Reviewed source words; never a rewritten sentence labelled as a quote |
| context / purpose | Question, surrounding qualifiers and editorial reason |
| decision / reviewer | Keep, omit, uncertain; approval belongs to a real reviewer |
| output_in / output_out | Final placement after editorial ordering |

Frame zero is the first decoded source frame, not necessarily timecode 00:00:00:00.
For VFR, use timestamps and the reviewed working-master mapping; frame number
at an assumed rate is not reliable. Word-level timestamps need listening review.

## Short fictional example

At 30 fps, keep source `[0,30)` and `[60,90)`. At normal speed they map to output
`[0,30)` and `[30,60)`: two seconds total. The unused middle sentence stays in the
source. The gallery calculates this map but does **not** execute an NLE cut or
claim that the text came from a recording.

## Review around every seam

Listen to several seconds on both sides, not just the join. Check the omitted
question, negations, tense, chronology and conditions. Review the assembled
passage as a whole; a sequence of individually accurate words can still mislead.
Preserve a dry source alternate and keep changes reversible.

## Transcription choices

Use the NLE's source transcription when available and appropriate. An external
ASR engine must be selected by language, speaker overlap, hardware, privacy,
model licence and deployment constraints. This skill does not bundle weights,
choose an account, upload recordings or automatically install Whisper variants.
Human correction remains necessary even with word-level alignment.

## Sources

Adobe indexed guidance checked 2026-10-16; native Premiere was not connected.
Confirm controls and ripple behavior in the installed version.

- [Adobe — transcribe individual source files](https://helpx.adobe.com/premiere/desktop/edit-projects/edit-video-using-text-based-editing/transcribe-individual-source-files.html).
- [Adobe — edit sequences using Text-Based Editing](https://helpx.adobe.com/ie/premiere/desktop/edit-projects/edit-video-using-text-based-editing/edit-sequences-using-text-based-editing.html).
- [Adobe — detect and delete pauses](https://helpx.adobe.com/ie/premiere/desktop/edit-projects/edit-video-using-text-based-editing/detect-and-delete-pauses-in-transcripts.html).

The workflow and fictional example are original; no transcript or third-party
editing implementation is copied.
