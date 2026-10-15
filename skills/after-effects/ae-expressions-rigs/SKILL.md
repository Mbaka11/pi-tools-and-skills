---
name: ae-expressions-rigs
description: Vetted After Effects expressions and control rigs for editable client work - overshoot/settle, stepped stop-motion boil, seamless looping wiggle and noise for LED loops, delays and cascades, marker-triggered animation, auto-sizing text boxes from sourceRectAtTime, fit-to-width with a legibility floor, pixel snapping, French/Quebec number and price formatting, multiplane scale compensation, 2D parallax, path links and brand colour controls. Use when writing, debugging or rigging AE expressions, building a CTRL null, Essential Graphics/MOGRT controls, or making templates that survive language and copy changes.
compatibility: Adobe After Effects with the JavaScript expression engine (default since AE 16). Works through the Higgsfield bridge (ae_set_expression, ae_set_effect_expression, ae_add_expression_control, ae_link_properties) or by hand.
metadata:
  version: "1.0.0"
  short-description: Reliable AE expressions and control rigs
---

# After Effects expressions and rigs

[Tiny example — 3 s auto-box mockup and expression snippet](../../../examples/README.md#ae-expressions-rigs).

Use expressions to make client projects **editable and robust**, not to show off.
Every expression here is written for the JavaScript engine and avoids
language-dependent names.

## Rules that prevent most breakage

1. **Language-independent references.** Effect and property display names are
   localized (a French AE calls the slider property "Curseur"). Rename each
   control effect yourself (`Compteur`, `Drift X`, `Accent`) and read its value
   by index: `effect("Compteur")(1)`. Transform paths (`transform.position`,
   `text.sourceText`) are language-independent.
2. **Always return a value.** In the JavaScript engine an `if` without `else`
   can return nothing and raise a dimension error. Every branch ends in a value.
3. **Deterministic randomness.** Seed every `random()` (`seedRandom(seed, true)`)
   so renders, previews and re-renders match frame for frame.
4. **Keep `value` in the result** when the keyframes must stay editable; an
   expression that ignores `value` silently disables the animator's keys.
5. **One control null per module.** `CTRL_<MODULE>` holds sliders, checkboxes
   and colour controls. Clients change the control, never the expression.
6. **Measure, do not guess.** Layout expressions read `sourceRectAtTime()` and
   convert corners with `toComp()`; QA re-measures the result in the master.
7. **Performance.** Cross-layer `sourceRectAtTime`, long `valueAtTime` loops and
   per-frame text expressions are expensive. Posterize where possible; convert
   expressions to keyframes only when the module is final and the brief allows.

## Where things are

- [Expression library](references/expression-library.md) — motion, loops,
  timing, markers, randomness, camera/depth, paths.
- [Layout, text and LED](references/layout-text-led.md) — auto boxes,
  fit-to-width with a floor, pixel snapping, French formatting, safe areas.
- [Control rigs and templates](references/control-rigs.md) — CTRL nulls, brand
  colours, toggles, Essential Properties and MOGRT for Premiere.

## Applying through the Higgsfield bridge

- Add controls with `ae_add_expression_control`, then set expressions with
  `ae_set_expression` (layer properties) or `ae_set_effect_expression` (effect
  parameters). Link simple values with `ae_link_properties`.
- Re-read the layer after setting an expression and run the bridge audit:
  expression errors must be zero before the motion pass is called done.
- The bridge's `ae_finalize_build` repairs linear/default easing on keyframes;
  expressions are not keyframes, so ease them inside the expression
  (`ease()`, `easeOut()`) where it matters.

## Debug checklist

1. Read the error text in the expression error bar (or the audit report):
   dimension mismatch, undefined property, or reference to a renamed layer.
2. Check the layer and effect names referenced; a duplicate layer name makes
   `thisComp.layer("X")` ambiguous — names must be unique in the comp.
3. Check the engine: *File › Project Settings › Expressions* should be
   JavaScript. Legacy ExtendScript projects may need syntax changes.
4. Isolate: replace the last line with `value` and re-add pieces until it fails.
5. For text, test with a longer and a shorter copy, accents and a price —
   the editability test in ae-production-workflow should exercise the rig.
