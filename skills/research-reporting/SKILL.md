---
name: research-reporting
description: Turn existing research into concise briefs, executive summaries, full reports, or reviewed PDF exports. Use when synthesizing sourced findings for a specified audience without inventing evidence or sending messages automatically.
metadata:
  version: "1.0.0"
  origin: "Adapted from Mbaka11/Cowgorithm skills/report-gen"
---

# Research Reporting

[Tiny example — a four-line fictitious decision brief](../../examples/README.md#research-reporting).

Read the project's instructions and the selected source documents. Establish the
audience, purpose, output language, length, format, and destination. Preserve
source-language quotations where necessary; do not translate user data or change
units/currencies silently.

## Synthesis

- Organize by the audience's decisions, not by the order of input files.
- Retain citations, dates, assumptions, uncertainties, and conflicting evidence.
- Distinguish a sourced fact from an estimate or recommendation.
- Never fabricate a percentage complete or convert a draft into a verified result.
- Avoid quoting confidential source material into a public deliverable.

## Short brief

Use one topic and normally no more than 250 words:

```text
Topic — Date
Key findings: up to three evidence-backed points
What changed: one or two sentences
Action needed: one focused decision, if any
Full report: project-relative path
```

Prepare a message draft only. Sending to WhatsApp, email, Slack, or any other
recipient requires authorization covering that recipient and content.

## Executive summary

Aim for one or two pages with:

1. Bottom line.
2. Key numbers (value, unit/currency, reference date, source).
3. Opportunities and evidence.
4. Risks and unresolved questions.
5. Concrete next steps.

## Full report

Read the actual source set, synthesize across findings, and explain cross-cutting
trade-offs rather than concatenating documents. Use numbered sections, consistent
terminology, accessible charts/tables, an executive summary, and a bibliography.
Reuse project conventions for filenames and folders.

## PDF export

Use an already available, appropriate document pipeline. Check dependencies
before exporting; do not install a converter or invoke a paid service implicitly.
A possible Pandoc/WeasyPrint invocation is:

```bash
pandoc report.md --standalone --toc --pdf-engine=weasyprint -o report.pdf
```

Run only on trusted/reviewed input in an appropriate environment. Document
converters can access local resources; do not enable arbitrary scripts or remote
asset fetching for untrusted documents.

Open or render the produced PDF and check page count, clipping, typography,
charts, links, and missing glyphs. A successful exit code does not establish
visual quality. If export is unavailable, deliver Markdown and state the limit.

## Progress reports

Cover completed work, ongoing work, blockers, decisions needed, and next steps.
Use an explicit denominator before reporting a completion percentage. This skill
does not create a schedule or send recurring messages.

## Provenance

Generalized from [Cowgorithm's report skill](https://github.com/Mbaka11/Cowgorithm/blob/c3ccfce39969a9bab8a181c387c137b365457c6c/skills/report-gen/SKILL.md).
Automatic messaging, fixed project directories, and scheduling assumptions were
removed.
