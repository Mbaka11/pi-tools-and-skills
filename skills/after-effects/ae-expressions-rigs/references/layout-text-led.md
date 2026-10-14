# Layout, text and LED-safe expressions

## Measure a text layer in comp space

`sourceRectAtTime(t, includeExtents)` returns layer-space bounds
(`left`, `top`, `width`, `height`). Convert corners with `toComp()` so parent
scale, layer scale and anchor offsets are included. Point text is the most
predictable; verify paragraph (box) text on the installed version.

```js
var L = thisComp.layer("TXT_TITLE");
var r = L.sourceRectAtTime(time, false);
var tl = L.toComp([r.left, r.top]);
var br = L.toComp([r.left + r.width, r.top + r.height]);
// tl/br are comp-space corners (rotation ignored)
```

## Auto-sizing background box (plate, pill, banner)

Shape layer with one Rectangle at group position `[0,0]` and layer Anchor Point
`[0,0]`. Add Sliders renamed `Pad X` and `Pad Y` on the shape layer.

Rectangle › Size:

```js
var L = thisComp.layer("TXT_TITLE");
var r = L.sourceRectAtTime(time, false);
var tl = L.toComp([r.left, r.top]);
var br = L.toComp([r.left + r.width, r.top + r.height]);
[Math.abs(br[0] - tl[0]) + 2 * effect("Pad X")(1), Math.abs(br[1] - tl[1]) + 2 * effect("Pad Y")(1)];
```

Shape layer › Position (follows the text centre, unparented shape layer):

```js
var L = thisComp.layer("TXT_TITLE");
var r = L.sourceRectAtTime(time, false);
L.toComp([r.left + r.width / 2, r.top + r.height / 2]);
```

Keep the plate and its text in one precomp unit when the bridge doctrine asks
for it; the expression still references the text by name inside that precomp.
Add Round Corners on the shape for pills.

## Fit to width with a legibility floor

On the text layer's Scale. Shrinks long copy to `Max width` but never below
`Min scale`; if the floor is hit, the copy is too long for the screen and must
be split or rewritten (do not ship it smaller).

```js
var maxW = effect("Max width")(1);     // px in this layer's comp
var minS = effect("Min scale")(1);     // %, e.g. 85
var r = sourceRectAtTime(time, false);
var s = r.width > 0 ? Math.min(100, 100 * maxW / r.width) : 100;
s = Math.max(minS, s);
[s, s];
```

QA must confirm that no layer sits at its floor in the final copy.

## Pixel snapping for crisp holds on LED

Fractional positions blur thin strokes and small text across two LED pixels.
Snap only when the layer is not moving, so motion stays smooth.

```js
var v = velocity;   // pre-expression velocity of this Position
length(v) < 1 ? [Math.round(value[0]), Math.round(value[1])] : value;
```

Also round the Anchor Point of text and thin shapes, keep Scale at 100% on the
hold, and avoid odd-width elements centred on a half pixel. Check the result on
the real grid (ae-production-workflow native still at 100%).

## French / Québec numbers and prices (Source Text)

Control: a Slider renamed `Valeur` on `CTRL_<MODULE>`.

```js
var n = Math.round(thisComp.layer("CTRL_MODULE").effect("Valeur")(1));
var nbsp = "\u00A0";   // use "\u202F" only if the font has that glyph
var s = String(Math.abs(n)).replace(/\B(?=(\d{3})+(?!\d))/g, nbsp);
(n < 0 ? "\u2212" : "") + s + nbsp + "$";
```

Decimals (`12,5 %`):

```js
var x = thisComp.layer("CTRL_MODULE").effect("Taux")(1);
var s = x.toFixed(1).replace(".", ",");
s + "\u00A0%";
```

- Counters: animate the slider with ease-out; the final key must equal the
  approved figure exactly. Round in the expression, not by eye.
- Check the glyphs: some fonts lack U+202F, `−` (U+2212) or French quotes and
  AE silently substitutes or shows a box. Verify in a rendered still.

## Safe areas and minimum sizes

- Read the target's margins and minimum cap height from led-signage-content
  (LED) or the platform safe zones in video-delivery-qc (social).
- Keep a guide layer (`GUIDE_SAFE`, guide layer switch on so it never renders).
- After any copy change, re-measure every text layer's comp-space bounds against
  the safe rectangle in the **master** composition.

## Line breaks and hierarchy

- Break lines manually at semantic boundaries; do not rely on paragraph wrapping
  when copy must match an approved layout.
- One message per screen on LED; hierarchy by size and weight first, colour
  second.
- Avoid widows: a single short word alone on the last line.
