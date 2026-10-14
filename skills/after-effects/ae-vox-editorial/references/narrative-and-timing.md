# Narrative structure and timing

## The beat sheet comes first

Write it in the build-receipt folder before any AE work. One row per beat:

| # | On-screen text (exact) | VO line (if any) | Visual idea | Depth layers | Hold (s) | Transition out |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | — | "Ce prix ne devrait pas exister." | price tag cut-out slams on paper | ground / tag / hand | 3.2 | hard cut on "exister" |

Rules:

- One beat carries one idea. Two ideas in a sentence means two beats.
- Fewer scenes than beats: a held image while the next line lands reads as
  confidence. Roughly 7 scenes for 10 beats.
- Every on-screen number, date, price and quotation is copied from approved
  client material, with its source noted. Nothing is invented for layout.
- Never open a beat on an empty frame: the primary element is visible within
  about 3 frames of the cut.

## Hook and payoff (narrated explainers)

- The hook states something surprising or apparently wrong and withholds the
  subject (no brand, place or name in the first line when the format allows).
- The final beat answers the hook's exact question; it does not summarise.
- Test: can a viewer name the subject from the hook? If yes, rewrite. Does the
  last line pay the debt? If not, fix the hook or the ending.

Advertising briefs often require the brand early; then use the hook for the
problem and keep the reveal for the offer.

## Voice-over is the clock (when there is narration)

1. Write the script, then record or generate the VO **before** animating.
2. Measure each line (per-beat files are easier to re-time than one long file).
3. Derive beat lengths from the measured audio and put comp markers on the key
   words. Animation lands on markers, not on guessed frame numbers.
4. Budget: French or English narration at a calm explainer pace is about
   2.4–2.8 words per second; 60 s holds roughly 140–165 words.

Synthetic voices need licence checks for commercial use (see sound-design-sfx).

## Reading time is the clock (silent LED and signage)

LED roll-ups and walls usually play without sound in noisy halls. On-screen
text carries the message and the viewer is often walking.

Heuristic starting point, then verify:

```text
passers-by:      hold = max(2.5 s, words / 2.5 + 0.5 s)
seated audience: hold = max(2.0 s, words / 3.5 + 0.5 s)
```

- Count every word, including articles and numbers.
- Entrance animation time does not count as reading time; the hold starts when
  the line is fully legible and stable.
- Validation: read the line aloud twice at a normal pace; the stable hold must
  be longer than that. Client briefs that state a hold (for example "3–4 s per
  question") override the heuristic upward, never downward.
- Keep at most about 7–10 words per screen for passers-by; split longer copy
  into successive screens rather than shrinking type.

## LED loop structure

- Any moment can be a viewer's first frame. Make each message self-contained.
- Show the brand or logo at least every 8–10 s, or keep a small persistent mark
  if the brief allows.
- An offer or price that matters can stay visible while other lines change, at
  a lower hierarchy (decide explicitly with the client).
- Typical loop: 15–30 s, 3–5 messages, one identity moment. Longer programmes
  (event schedules) are chaptered with a consistent header.
- The last frame must hand off to the first: same ground, same camera, no flash.
  Check the seam with video-delivery-qc's loop check.

## Pacing references (30 fps)

| Element | Typical |
| --- | --- |
| Element entrance | 10–18 frames |
| Stagger between elements | 4–16 frames |
| Highlighter wipe | 8–14 frames |
| Draw-on annotation | 10–16 frames |
| Stamp slam | 3–4 frames + 2–4 frame shake |
| Camera push across a beat | 3–8% scale |
| Hard cut | on a word, a beat or a visual action |

## French copy on screen (fr-CA)

- Non-breaking space before `:` `;` `!` `?` `%` `$` and inside « guillemets »;
  use U+00A0 unless the font is verified to contain U+202F.
- Prices: `2 450 $` (space thousands separator, space before `$`).
- Keep line breaks semantic: never strand a single short word on the last line.
- Verify accents and ligatures in the chosen font (É, À, Ç, Œ, «»).
