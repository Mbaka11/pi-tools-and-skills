---
name: montage-editing-craft
description: Editing craft and workflow for client montages from brief to delivery - ingest and bins, selects, transcript-based speech cuts, cut plans, pacing by format (ads, testimonials, event recaps, social, LED loops), J/L cuts, music editing on bars, B-roll coverage, transitions ladder, reframing 16:9 to 9:16/1:1/4:5/1:2 LED, colour normalisation, French captions with scripts/srt_check.py, versioning, French client review notes and deliverable matrices. Works with Premiere through the Higgsfield bridge (pr_* tools) or by hand. Use for "montage", "edit", "cut", "reel", "recap", "testimonial", "captions/sous-titres", "versions", or client revision rounds.
compatibility: Premiere Pro through the Higgsfield bridge is optional; any NLE works. Python 3.9+ for scripts/srt_check.py (standard library).
metadata:
  version: "1.0.2"
  short-description: Professional edit workflow, pacing, captions and client versions
---

# Montage editing craft

[Tiny example — 3 s editing mockup and real subtitle correction](../../../examples/README.md#montage-editing-craft).

The edit decides what the audience understands. Software is the easy part;
choices about what to keep, how long to hold and where to cut are the job.

## Route by deliverable

| Deliverable | Also load |
| --- | --- |
| LED roll-up / wall loop | [led-signage-content](../led-signage-content/SKILL.md) (silent, reading holds, exact pixels) |
| Motion graphics, titles, editorial collage | [ae-vox-editorial](../../after-effects/ae-vox-editorial/SKILL.md), [ae-production-workflow](../../after-effects/ae-production-workflow/SKILL.md) |
| Interview paper edits and source-linked radio cuts | [montage-transcript-editing](../montage-transcript-editing/SKILL.md) |
| Shot boundaries, contact sheets and selects | [montage-scene-selects](../montage-scene-selects/SKILL.md) |
| Accessible captions and language versions | [montage-caption-accessibility](../montage-caption-accessibility/SKILL.md) |
| Archive, collect and restoration testing | [montage-archive-handoff](../montage-archive-handoff/SKILL.md) |
| Ingest, proxies, relink, online conform | [montage-proxy-conform](../montage-proxy-conform/SKILL.md) |
| Multicam or external recorder synchronization | [montage-multicam-sync](../montage-multicam-sync/SKILL.md) |
| Dialogue repair and voice balancing | [montage-dialogue-cleanup](../montage-dialogue-cleanup/SKILL.md) |
| Colour management and shot matching | [montage-colour-finishing](../montage-colour-finishing/SKILL.md) |
| Slow motion, speed ramps, freezes | [montage-time-remapping](../montage-time-remapping/SKILL.md) |
| Sound design, music, mix | [sound-design-sfx](../sound-design-sfx/SKILL.md) |
| Final file checks | [video-delivery-qc](../video-delivery-qc/SKILL.md) |

## Workflow

1. **Brief**: objective, audience, platform(s), durations, aspect ratios,
   mandatory messages, brand rules, music/voice, deadline, revision rounds.
   Ask once for missing high-leverage inputs with options and a default.
2. **Ingest**: copy media into the project tree, keep originals untouched,
   bins by type (`01_RUSHES`, `02_AUDIO`, `03_GRAPHICS`, `04_MUSIC`, `05_EXPORTS`).
   Note frame rates; mixed rates need a decision, not an accident.
3. **Selects**: watch everything once. For speech, get a transcript first and
   mark usable sentences; for B-roll, mark moments (action peaks, reveals).
4. **Cut plan**: an ordered list of clips with in/out timecodes and purpose
   (`references/editing-grammar.md`). With the Higgsfield bridge the plan is the
   argument to `pr_assemble_edit` / `pr_apply_cut_plan`, not a prose deliverable.
5. **Assemble → rough → fine**: structure first, then rhythm, then frames.
   Speech cuts land on sentence or phrase boundaries (transcript), snapped to
   pauses (`pr_detect_silence`). Beat-synced cutting (`pr_detect_beats`) is for
   B-roll and music montages only — never chop someone mid-sentence.
6. **Picture lock**, then sound, colour, graphics and captions. Changes after
   lock are re-scoped explicitly.
7. **Versions**: reframes and durations per `references/reframe-and-versions.md`.
8. **QC and delivery**: decode-based QC on every file; French delivery note
   (`references/client-review-fr.md`).

## Premiere through the Higgsfield bridge

- Happy path: `get_host_status` → `pr_import_media` (only if needed) →
  `pr_assemble_edit` with the full cut plan (one call; sequence settings match
  footage; optional reframe such as 1080×1920).
- For speech edits, load `pr_get_skill('radio-edit-craft')`; for the tool
  contract, `premiere-api-realities`.
- Run at most 2–3 media-analysis calls (probe, silence, beats, renders) at once.
- Verify with two signals: a fresh `pr_get_active_sequence` and a viewed
  `pr_export_sequence_frame`. The editor may have changed the timeline between
  turns — re-read before mutating.
- Transitions ladder: hard cut first; then `pr_add_transition` by exact name;
  then a .mogrt; generated bridges only for hero moments (credits).

## Captions

Check every SRT before burning or delivering it:

```bash
python scripts/srt_check.py captions_fr.srt --preset social-vertical --french fr-CA
python scripts/srt_check.py captions_fr.srt --french fr-CA --fix-french-out captions_fr_fixed.srt
```

Rules, presets and transcription options: `references/captions-fr.md`.

## Ethics and accuracy

- Testimonials and interviews: never assemble words into a statement the person
  did not make. Keep meaning intact; mark condensed quotes if the brief allows.
- Prices, dates and claims on screen come from approved client copy.
- Music, footage and fonts: licences recorded before delivery.
