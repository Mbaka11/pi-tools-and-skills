# Control rigs and templates

## The CTRL null

One null per module, `CTRL_<MODULE>`, guide layer off (it does not render
anyway), locked after setup. Typical controls (rename each effect; read by index):

| Control | Effect type | Used by |
| --- | --- | --- |
| `Accent`, `Ink`, `Paper`, `Brand 1…n` | Color Control | shape fills/strokes, text fill via expression |
| `Valeur`, `Taux` | Slider | counters and prices (Source Text) |
| `Afficher prix`, `Afficher logo` | Checkbox | opacity toggles for variants |
| `Drift X`, `Drift Y` | Slider | 2D parallax |
| `Stagger (f)` | Slider | frame offsets in cascades |
| `Langue` | Dropdown Menu Control | FR/EN copy switching |

## Brand colours from one place

Fill › Color (shape) or a Fill effect's Color:

```js
thisComp.layer("CTRL_MODULE").effect("Accent")(1);
```

In a precomp, reference the master's control with `comp("MASTER").layer(...)`
only when the precomp is never reused elsewhere; otherwise expose an Essential
Property (below) so each instance can differ.

## Toggles for variants

Opacity:

```js
thisComp.layer("CTRL_MODULE").effect("Afficher prix")(1) == 1 ? value : 0;
```

Keep `value` so the layer's own fade keys still work when visible.

## Language switch (FR/EN) without duplicating comps

Dropdown Menu Control renamed `Langue` with items `FR`, `EN` (menu values are
1-based). Source Text:

```js
var lang = thisComp.layer("CTRL_MODULE").effect("Langue")(1);
var fr = "Aller à l\u2019expo";
var en = "See you at the show";
lang == 1 ? fr : en;
```

For more than a few strings, keep two text layers (`TXT_FR_*`, `TXT_EN_*`)
toggled by the dropdown instead of long expression strings, so translators edit
text layers, not code. Re-run layout QA for each language: English and French
lengths differ.

## Essential Properties (per-instance precomp overrides)

To reuse one beat template with different copy, colour or image per instance:

1. In the template comp open *Essential Graphics*, set the comp as primary and
   drag the text Source Text, colour controls and checkboxes into the panel.
2. Each instance of that precomp in the master exposes those properties under
   *Essential Properties*; override per instance without duplicating comps.
3. Name properties for the client (`Titre`, `Prix`, `Couleur accent`).

This keeps one template authoritative for animation while instances change
content — ideal for multi-client or multi-price LED loops.

## MOGRT for Premiere editors

Export the template as a Motion Graphics Template when an editor will change
text in Premiere. Through the bridge, Premiere can then use `pr_import_mogrt`
and `pr_set_mogrt_text`. Constraints:

- Only properties added to Essential Graphics are editable downstream.
- Fonts must be installed on the editor's machine (or use Adobe Fonts).
- Test the MOGRT with the longest expected copy before handing it over.

## Rig hygiene

- Lock the CTRL null and the rigged layers after setup; unlock only the layer
  being changed, then restore the lock (ae-production-workflow).
- Document every control in the module's `DELIVERY.md`: name, purpose, safe
  range (for example `Pad X` 16–60 px).
- The reversible editability test must change a real control (longer copy,
  another colour) and confirm the layout and the original are restored.
