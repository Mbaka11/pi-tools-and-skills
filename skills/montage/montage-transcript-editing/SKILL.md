---
name: montage-transcript-editing
description: Transcript-led interview and documentary editing - map reviewed words to source IDs and exact time ranges, build a paper edit, preserve context and speaker meaning, assemble a reversible radio edit, retain breaths and handles, then cover picture cuts and regenerate captions. Use for text-based editing, interview selects, podcast excerpts, radio edits, paper edits or cutting from a transcript. Does not authorize cloud transcription, voice cloning or invented quotes.
compatibility: Any NLE; Premiere Text-Based Editing optional. Transcription engines, language models and cloud services are separate prerequisites and require consent for private recordings.
metadata:
  version: "1.0.0"
  short-description: Source-linked paper edits and truthful interview assembly
---

# Transcript-based editing

[Tiny example — fictional transcript and source-linked paper edit](../../../examples/README.md#montage-transcript-editing).

A transcript is a navigation aid, not proof of what was said. Edit the actual
recording and context, not just the apparent fluency of a generated paragraph.

## Establish source truth

1. Preserve originals and assign stable source/take/speaker IDs. Record exact
   rational source rates, timecode origin and any VFR-to-working-master mapping.
2. Obtain a source transcript with timestamps. Confirm permission before sending
   recordings to a provider; local execution still needs model/licence review.
3. Listen and correct names, numbers, negations, speaker changes and ambiguous
   phrases against the source. Mark inaudible text rather than inventing it.
4. Preserve the uncorrected transcript separately and record corrections. An ASR
   confidence value is not an editorial approval or identity verification.

## Paper edit before timeline edits

For each proposed excerpt record source ID, source IN/OUT, original wording,
context, purpose and keep/omit decision. Keep sentence boundaries and surrounding
handles. A practical review table is in [the paper-edit reference](references/paper-edit.md).

- Build a beginning, evidence and conclusion from authentic statements.
- Do not join words to reverse a meaning, hide a condition or manufacture an
  endorsement. Reordering requires context review, not just smooth audio.
- Protect negatives, uncertainty, qualifiers and the question being answered.
- Distinguish a quote, paraphrase, narration and editorial on-screen summary.
- Resolve rights, sensitive disclosures and speaker consent before publishing.

## Assemble the radio edit

Duplicate the sequence, then assemble approved source ranges. Keep original
media links and a source-to-output map. Inspect cuts around consonants, breaths,
pauses and room tone at normal speed; add appropriate handles/crossfades rather
than deleting every pause. Keep continuous master audio from multicam sources.

In Premiere, distinguish **source transcription** from the **sequence transcript**.
Source text helps select footage; editing the sequence transcript can ripple
actual timeline clips. Never run a bulk pause/filler-word deletion without a
preview, scope limit and review of the resulting cut. Tool names and behavior
must be discovered in the connected version, not assumed from this document.

## Picture, captions and revisions

Cover unavoidable jump cuts with relevant, licensed B-roll; coverage must not
suggest a different location, action or chronology without explanation. Finish
picture and [dialogue cleanup](../montage-dialogue-cleanup/SKILL.md), then create
captions from the **final** timeline, not the old source transcript.

For each revision keep source references, changed ranges and the reason. Check
that captions, graphics, SFX and sequence duration follow ripple changes.

## Acceptance

- Every quoted passage can be located in the preserved source.
- Human meaning/context review and normal-speed audio review are recorded, or
  explicitly pending. A cut-plan JSON is not evidence of either.
- Delivery includes the editable sequence, source-linked selects and unresolved
  issues; run [video-delivery-qc](../video-delivery-qc/SKILL.md) on exports.
- No private transcript, voice sample or generated client project enters this
  toolbox. The gallery uses authored fictional text, not ASR output.
