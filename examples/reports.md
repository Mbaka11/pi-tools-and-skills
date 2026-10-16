# Report examples — a few lines each

**All scenarios and figures below are fictitious.** They illustrate deliverable
formats, not market research, certification or an executed investigation.
No real client, account, binary or service is targeted.

## market-research

> **Question:** is there an opportunity for a fictitious rental service?
> **Demo assumption:** 100 venues × 2 purchases/year × €300 = €60,000/year.
> **Illustrative range:** 50–150 venues → €30,000–€90,000/year.
> **To verify:** venue count, purchase frequency and budget using primary sources.
> **Decision:** do not treat this simulation as a measured market.

## research-reporting

> **Decision brief — fictitious project**
> Modeled potential: €60,000/year; unverified data.
> Main sensitivity: the number of purchasing venues.
> Proposed next step: validate demand before setting a price.
> Source: [demo assumptions above](#market-research).

## backlog-execution

> **Fictitious authorized scope:** two tasks, no automatic publication.
> ✓ Prepare a brief — expected evidence: reviewed `brief.md`.
> ☐ Produce the animation — blocked: final copy not approved.
> **Illustrative status:** 1/2; no invented production-completion percentage.

## rea-investigation

> **Sample report, REA not executed:**
> `open file → importDocument() → parseDocument() → preview`
> Assumed artifact: a test application owned by the operator.
> Evidence to collect: module, offset/line and authorized capture reference.
> Hypothesis: decoding is local; no network conclusion without observation.

This invented flow shows the expected level of concision. It is not REA engine
output and does not justify bypassing access controls.

## reverse-api-investigation

> **Fictitious contract map:** `GET /v1/items?page=N` → paginated collection.
> **To confirm:** response schema, final-page behavior and errors.
> **Intended client:** environment-based configuration, never embedded secrets.
> **Status:** no network request executed, no client validated.

The [actual structural summary](outputs/api-summary.json) was produced with
`har-summary.mjs` from [two synthetic events](fixtures/request-events.json).
It contains one opaque host, one endpoint and two HTTP 200 responses. It does
**not** establish the contract semantics above: those are fictitious and would
require additional authorized evidence.

## Reference tools

- **REA 6.4.0**: [sample flow](#rea-investigation), a text illustration,
  not a REA session. [Integration](../tools/rea/README.md).
- **Reverse API Engineer 0.14.0**: [fictitious contract](#reverse-api-investigation),
  through our adaptation; no upstream-agent execution or hardcoded secrets.
  [Evaluation](../tools/reverse-api-engineer/README.md).

[Back to the gallery](README.md)
