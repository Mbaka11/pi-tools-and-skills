---
name: market-research
description: Research market size, competitors, regulations, and adjacent opportunities using sourced assumptions and explicit uncertainty. Use for evidence-based market studies and opportunity comparisons in any project.
metadata:
  version: "1.0.0"
  origin: "Adapted from Mbaka11/Cowgorithm skills/research"
---

# Market Research

[Tiny example — fictitious bottom-up calculation, not market evidence](../../examples/README.md#market-research).

## Establish the scope

Read the current project's instructions and existing research first. Determine the
product, customer, geography, time horizon, currency, audience, and requested
deliverable. Ask only for missing decisions that materially change the analysis.
Do not assume a Canadian market, CAD, hardware product, or a particular company.

Use available research tools; a skill does not provide web access. Do not invent
sources when browsing is unavailable. Separate current observations, dated
historical evidence, estimates, and unresolved claims.

## Market sizing

Prefer a bottom-up calculation:

```text
TAM = addressable customers or units × annual revenue per customer or unit
SAM = TAM × justified geographic and product-fit filters
SOM = serviceable opportunity × defensible near-term capture assumptions
```

- Show units, reference dates, sources, math, and each filter's assumptions.
- Avoid double-counting overlapping segments or multiplying dependent filters.
- Give conservative, base, and optimistic scenarios rather than false precision.
- Triangulate important inputs with independent sources where available. Two
  pages repeating the same study are not independent evidence.
- Distinguish measured market revenue from a modeled potential market.

## Competition and regulation

For each relevant competitor, record product, customers, geography, pricing date,
currency, pricing model, capabilities, funding when verified, strengths, gaps,
and source links. Treat "not found" as a search limitation, not proof of absence.

Prefer primary sources: official statistics, regulatory text, published pricing,
company filings, and original studies. Note jurisdiction and effective date for
regulations. Do not turn a research summary into legal advice or a compliance
certification.

## Opportunity scoring

Choose factors and weights appropriate to the user's objective. A possible
starting point is market size 25%, unmet need 25%, technical fit 20%, regulatory
fit 15%, strategic fit 15%. These are examples, not universal decision rules.

Define anchored scales, explain every score, show the weighted calculation and
sensitivity, and flag missing evidence. Do not use arbitrary thresholds to make
an investment or pricing decision on the user's behalf.

For adjacent opportunities, start from confirmed product capabilities, inspect
previous investigations, compare alternatives, and document why each is or is
not worth further validation. Do not silently expand the authorized backlog.

## Deliverable

Use the project's established output directory. If none exists, propose a simple
`research/` folder and a source ledger rather than imposing a large structure.
Include:

1. Key findings and decision implications.
2. Tables and calculations with inline source URLs and dates.
3. Explicit assumptions, estimates, contradictions, and limitations.
4. Recommended next validation steps, not unsupported certainty.
5. A source ledger with claim, source, date accessed, and verification status.

Keep confidential business material in its project, not in the global skill
repository. Drafting a report does not authorize sending it to anyone.

## Provenance

Generalized from [Cowgorithm's research skill](https://github.com/Mbaka11/Cowgorithm/blob/c3ccfce39969a9bab8a181c387c137b365457c6c/skills/research/SKILL.md).
The original project's market facts, fixed thresholds, and business assumptions
are intentionally not carried over.
