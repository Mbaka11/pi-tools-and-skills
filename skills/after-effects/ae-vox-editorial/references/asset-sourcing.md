# Asset sourcing: draw, source, generate

Classify every asset before building. The classification decides who owns
editability and rights.

| Class | Examples | How |
| --- | --- | --- |
| `DRAW` | paper ground, tears, banners, highlights, circles, arrows, charts, maps, documents, stamps, **all text, prices, logos' layout** | native AE layers |
| `SOURCE` | client photos and logos, public-domain archives, licensed stock, client footage | packaged copies with rights evidence |
| `GEN` | wordless illustrated subjects: a hand, a phone, a crowd, an object, a vintage-style prop | image generation as isolated elements |

## Elements, not posters

Do not generate a finished composition and animate pieces of it: the original
image stays underneath, nothing can move behind anything, and the result looks
flat. Generate **one subject per element** (or several well-separated subjects
on one sheet) and compose the frame natively.

Prompt skeleton (prepend the passport's style descriptor verbatim to every
generation in the task, so all assets share one style):

```text
<STYLE DESCRIPTOR FROM THE PASSPORT>
Single isolated <subject>, vintage print illustration with halftone shading,
cut-out paper look, centered with a wide empty margin, flat solid #FF00FF
background, even lighting, no text, no letters, no numbers, no logo,
no watermark, not a 3D render.
```

- Keep the subject count small (about 4–6 generated assets per task) and
  regenerate any result that drifts off-style instead of mixing styles.
- Never generate text, prices, logos, real people's likenesses, or anything the
  client has to approve word for word.
- Cut out on a flat field: key the magenta (Keylight `Keylight 906` with the
  screen colour picked from the border, then Simple/Matte Choker 1–2 px and a
  magenta spill correction), or use a background-removal tool (Higgsfield
  Remove Background spends credits; a local model works offline — see
  ae-vfx-compositing). Inspect edges at 200% for a coloured halo.
- Generated stills that need halftone can be treated afterwards (Photoshop or
  the vendored `halftone.py`), keeping the untreated file too.

## Higgsfield generation contract

Generation spends the user's credits.

1. List what will be generated (subject, size, count) and the estimate before
   the first call when the user has not already authorised that batch.
2. One style descriptor for the whole batch; one subject per request unless a
   sheet of separated subjects is deliberately cheaper.
3. Use the tools actually present in the session (for example a Higgsfield
   image-generation tool returning a result URL, then `ae_import_image`). Check
   each tool's description for host requirements before relying on it.
4. Download every accepted result into the project asset tree
   (for example `Assets/06_Working/gen/`), import it by local path, and record
   its SHA-256. A remote URL is not a durable project asset.
5. Keep a ledger, `_planning/<MODULE>_BUILD/generation_ledger.json`:

```json
{
  "style_descriptor": "…verbatim…",
  "items": [
    {
      "id": "GEN_hand_pointing_01",
      "prompt": "…",
      "tool": "…",
      "job_id": "…",
      "credits": 0,
      "local_path": "Assets/06_Working/gen/GEN_hand_pointing_01.png",
      "sha256": "…",
      "status": "accepted | rejected-off-style | rejected-defect",
      "rights_note": "commercial use per the account's plan; confirm for client delivery"
    }
  ]
}
```

Commercial rights for generated media depend on the provider plan. Flag it once
for client work and record the answer.

## Public-domain and open sources

Licences change and are per item: record the item URL, the licence or rights
statement, and the date checked, in the media receipt.

| Source | Typical status | Notes |
| --- | --- | --- |
| Smithsonian Open Access | CC0 items flagged as such | filter by CC0 |
| The Met Open Access | CC0 for flagged public-domain works | check the item badge |
| Rijksmuseum | many items public domain | check per item |
| Library of Congress | many items with "no known restrictions" | rights statement per item |
| NYPL Digital Collections | public-domain filter available | check per item |
| Wikimedia Commons | per-file licences | attribution licences complicate reposts |
| Natural Earth | public domain map data | good for map shapes |
| BAnQ (Québec) | mixed rights | many items restricted; read each notice |

Prefer CC0/public domain for client work: attribution licences rarely survive
reposting. Avoid violent or distressing archival material unless the brief
requires it. Identifiable people in commercial work need consent or a release
even when the photograph itself is free to use.

## Client assets

- Logos: use the official vector or high-resolution files, in separate layers
  if the identity animation needs parts. Never redraw a logo from a screenshot.
- Fonts: package licensed font files with licence text in `Assets/03_Fonts/`
  and verify `fontObject.isSubstitute === false` in AE.
- Photos and footage: copy, hash, and keep originals untouched
  (ae-production-workflow, Phase C).
