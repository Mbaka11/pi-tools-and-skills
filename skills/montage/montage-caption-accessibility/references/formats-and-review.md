# Caption formats and review

## Format boundaries

| Output | Review |
| --- | --- |
| SRT | Time syntax, ordering, phrase breaks, reading policy; styling support varies |
| WebVTT | UTF-8, `WEBVTT` signature, valid increasing cue starts and end > start, supported cue settings |
| Embedded subtitle track | Container/codec and language labels, default/forced flags, actual player selection |
| Burned captions | Final encoded pixels, contrast, safe placement, legibility and complete glyphs |

WebVTT can represent overlapping cues and voice/language spans. A project's
no-overlap policy is a readability choice, not a claim that all overlaps violate
the format. Test voice markup and positioning in the intended player; do not
assume every platform renders them identically.

## Review checklist

- Words and necessary sounds match the final audio; speaker labels are supported.
- No missing negation, name, number, important music/sound cue or premature reveal.
- Cue timing and reading holds reviewed at normal speed, not only from an SRT.
- Language/locale names are correct and translations preserve meaning.
- Longest cues, language expansion, accents, RTL and fallback fonts checked.
- Closed-caption controls work in the actual player; burned captions do not
  obscure information. Captions and an accessible transcript serve different needs.
- Reviewers, remaining issues and delivery formats are recorded. No blanket
  accessibility/legal certification is inferred from these checks.

## Gallery boundary

The sidecars label three deliberately synthesized sounds from the existing
three-second SFX preview. Labels were authored by the demo designer, **not**
recognized by ASR or confirmed by human listening. English/French files exercise
sidecar timing and layout; there is no spoken dialogue or translation service.
The preview is a synthetic layout, not a browser/player accessibility test.

## Sources

W3C pages retrieved 2026-10-16; these notes paraphrase the guidance and do not
reproduce the specifications.

- [W3C — understanding captions, prerecorded, SC 1.2.2](https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html).
- [W3C — WebVTT specification](https://www.w3.org/TR/webvtt1/).
- [Existing French SRT guidance](../../montage-editing-craft/references/captions-fr.md).

No provider upload, voice cloning, font redistribution or unreviewed automatic
translation is authorized by loading this skill.
