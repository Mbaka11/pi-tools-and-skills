# Sound sources and licences for client work

Licences differ per library and sometimes per file. For each sound used, record:
source, file name or ID, licence, attribution text if required, date checked.
When in doubt, do not ship it.

| Source | Typical terms (checked 2026-10) | Client use |
| --- | --- | --- |
| Sonniss #GameAudioGDC bundles | royalty-free, commercial use, no attribution; licensed for media production; AI/ML training prohibited | yes — keep the bundle licence with the project archive |
| Freesound — CC0 items | public domain dedication | yes |
| Freesound — CC BY items | commercial allowed with attribution | only if attribution can be shown (credits, description) |
| Freesound — CC BY-NC items | non-commercial only | **no** |
| Pixabay sound effects/music | Pixabay Content License: free commercial use, no attribution; restrictions on standalone redistribution | yes, after checking the item page |
| BBC Sound Effects (RemArc licence) | personal, educational, research — **not commercial** | **no**; commercial licences are sold separately (Pro Sound Effects) |
| Subscription libraries (Epidemic, Artlist, Soundstripe…) | coverage depends on the plan and on whose channel/client is covered | only if the subscription covers this client and use |
| Client-supplied audio | client warrants rights | yes, keep their written confirmation |
| Self-recorded Foley | yours | yes — the safest option for signature sounds |

## Music specifically

- Do not use commercial songs without sync and master licences.
- "Royalty-free" is not "rights-free": read territory, media, duration and
  client-transfer clauses.
- Broadcast use may require performing-rights reporting (cue sheet).
- Keep the licence PDF or page capture with the project archive.

## Generated audio

- Commercial use follows the provider's terms for the account's plan; record
  the plan and date.
- Avoid prompts naming living artists or recognisable songs; check the output
  does not resemble a known melody.
- Keep prompts, model, job IDs and file hashes in a generation ledger.
- Model weights' licences matter for local models (see generation-options.md).

## Synthetic voices

- Licensed TTS (for example ElevenLabs on a paid plan, or Azure Speech under a
  subscription) or a human voice for client deliverables.
- `edge-tts` (used by some open-source pipelines) calls Microsoft Edge's Read
  Aloud service through an unofficial client; commercial-use rights are unclear —
  use it for drafts and timing only unless rights are confirmed.
- Voice cloning of a real person requires that person's explicit consent.
