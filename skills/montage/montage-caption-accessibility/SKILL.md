---
name: montage-caption-accessibility
description: Accessible captions and multilingual subtitle delivery - distinguish dialogue subtitles from captions, include necessary speaker and non-speech audio information, review timing/readability and safe placement, localize without changing meaning, verify fonts/RTL and language tracks, and test sidecars and burned versions in the actual player. Use for accessibility captions, SDH, closed captions, WebVTT, multilingual subtitles or caption localization. Complements the existing SRT checker without claiming automatic WCAG certification.
compatibility: Any NLE/caption editor and target player. Existing srt_check.py requires standard-library Python; fonts, translation/transcription providers and subtitle renderers are separate prerequisites.
metadata:
  version: "1.0.0"
  short-description: Reviewed accessible captions and language-track delivery
---

# Caption accessibility and localization

[Tiny example — English/French sound-caption sidecars and layout preview](../../../examples/README.md#montage-caption-accessibility).

Dialogue subtitles translate or transcribe speech. Accessible captions also
convey necessary speaker identity and meaningful non-speech audio. Captions are
not a replacement for audio description of important visual information.

## Establish requirements

Confirm target platforms/players, audience, languages/locales, accessibility
requirements, sidecar versus embedded versus burned-in output, and a reviewed
source transcript. WCAG 1.2.2 addresses prerecorded synchronized media; passing
an SRT linter does not certify WCAG or a jurisdiction's legal requirements.

## Author against the locked timeline

- Verify words, names, numbers and speaker changes against the actual recording.
- Identify off-screen/ambiguous speakers when necessary, without guessing an
  identity or announcing information before the picture reveals it.
- Caption meaningful sound effects, music or reactions concisely. Do not label
  every incidental sound or invent emotion that is not supported by the source.
- Synchronize cue starts and ends, preserve sensible phrase breaks and avoid
  covering faces, lower thirds, demonstrations or important text.
- Set a project-specific reading-speed/line-length policy. Character counting
  differs by language and writing system; one numeric threshold is not universal.

## Localize and reflow

Translate meaning and register, not just words. Keep a glossary and approved
names/units; do not silently change a quotation, price or factual claim. Use a
qualified language reviewer for important content and log unresolved passages.
Translation can expand text, so re-segment and retime within the actual speech
rather than shrinking typography below a readable size.

Check Unicode, accents, punctuation, glyph coverage, line breaking, bidirectional
text and font licences. RTL/shaping support must be tested in the actual renderer
and player; a Latin-only Pillow mockup does not prove it.

## Validate and deliver

Use the existing helper from the repository root:

```sh
python skills/montage/montage-editing-craft/scripts/srt_check.py captions.srt --preset broadcast
python skills/montage/montage-editing-craft/scripts/srt_check.py captions-fr.srt --french fr-CA
```

Keep originals; fixes go to a new copy. Export UTF-8 SRT/WebVTT as required and
verify language labels, track selection, cue timing and rendered placement in
the actual player. Do not assume SRT styling survives WebVTT or MP4 conversion.
For burns, inspect pixels from the final encode, not only the editor preview.

Deliver the unburned master when requested, one clearly named sidecar per
language, any required burn, glossary/review note and known limitations.
Follow [format and accessibility checks](references/formats-and-review.md) and
[video-delivery-qc](../video-delivery-qc/SKILL.md). State human language/listening
review separately from automatic timing checks.
