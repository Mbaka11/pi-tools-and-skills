# Expression library

JavaScript engine. Copy the block, adjust the parameters at the top, and keep
control names unique. Controls are read by index `(1)` so the expressions work
in any AE interface language.

---

## Overshoot and settle after each keyframe

Apply to Position, Scale or Rotation. The last keyframe is the resting value;
the expression adds a decaying oscillation using the velocity arriving at it.

```js
var amp = 0.06;    // overshoot strength (0.03–0.12)
var freq = 2.2;    // oscillations per second (2–4)
var decay = 6.5;   // settle speed (4–8 snappy, 2–4 soft)
var n = 0;
if (numKeys > 0) {
  n = nearestKey(time).index;
  if (key(n).time > time) { n--; }
}
if (n > 0) {
  var t = time - key(n).time;
  var v = velocityAtTime(key(n).time - thisComp.frameDuration / 10);
  value + v * amp * Math.sin(freq * 2 * Math.PI * t) / Math.exp(decay * t);
} else {
  value;
}
```

Use it on entrances that should feel physical (cut-outs landing, stamps). Do not
stack it on top of hand-keyed overshoot keys.

## Stepped stop-motion with boil

Stepped timing at `fps` steps per second plus a small deterministic jitter.
Works on 2D or 3D Position.

```js
var fps = 12;      // steps per second (8–12 for collage)
var amp = 1.5;     // jitter in px (≥ 1 px on LED or it disappears)
var t = Math.floor(time * fps) / fps;
seedRandom(index * 1000 + Math.round(t * fps), true);
var v = valueAtTime(t);
var j = [random(-amp, amp), random(-amp, amp)];
v.length == 3 ? v + [j[0], j[1], 0] : v + j;
```

Rotation variant:

```js
var fps = 12, amp = 0.6;   // degrees
var t = Math.floor(time * fps) / fps;
seedRandom(index * 733 + Math.round(t * fps), true);
valueAtTime(t) + random(-amp, amp);
```

Set `amp = 0` to get pure stepped timing of the keyframed motion.

## Seamless looping wiggle (LED loops)

Cross-fades two wiggles so the motion at the loop end equals the loop start.

```js
var freq = 0.8;                    // wiggles per second
var amp = 10;                      // property units
var loopTime = thisComp.duration;  // or a slider for a shorter cycle
var t = time % loopTime;
var w1 = wiggle(freq, amp, 1, 0.5, t);
var w2 = wiggle(freq, amp, 1, 0.5, t - loopTime);
linear(t, 0, loopTime, w1, w2);
```

## Seamless Fractal Noise for loops

In Fractal Noise › Evolution Options enable **Cycle Evolution** and set
**Cycle (in Revolutions)** to `N`. Then on Evolution:

```js
var N = 2;   // must equal Cycle (in Revolutions)
linear(time, 0, thisComp.duration, 0, 360 * N);
```

The last frame equals the first. Check the seam with video-delivery-qc.

## Loops of keyframes

```js
loopOut("cycle");      // repeat first→last key
loopOut("pingpong");   // forward, then backward
loopOut("offset");     // repeat while accumulating the delta
loopOut("continue");   // keep the last velocity
```

For a looping precomp: enable Time Remap on its layer, place keys at the loop
range, and apply `loopOut("cycle")` to Time Remap.

## Follow the leader (cascade by index)

```js
var leader = thisComp.layer("LEAD");
var step = 0.08;   // seconds per layer
leader.transform.position.valueAtTime(time - step * (index - leader.index));
```

Place followers directly below the leader in the layer stack.

## Start on a named comp marker

Name comp markers in their comment field (`B03`, `PRIX`). Shift a keyframed
animation so it starts at that marker without moving keys by hand:

```js
var m = thisComp.marker.key("B03").time;   // marker whose comment is "B03"
var first = numKeys > 0 ? key(1).time : 0;
valueAtTime(first + Math.max(0, time - m));
```

## Replay an animation at every layer marker

Author the animation once from the property's first key; it restarts at each
layer marker (pulses on beats, repeated stamps).

```js
var n = 0;
if (marker.numKeys > 0) {
  n = marker.nearestKey(time).index;
  if (marker.key(n).time > time) { n--; }
}
if (n > 0 && numKeys > 0) {
  valueAtTime(key(1).time + (time - marker.key(n).time));
} else {
  valueAtTime(numKeys > 0 ? key(1).time : time);
}
```

## Flicker and gate weave (archival look)

Exposure (Exposure effect, property in stops) — held flicker:

```js
var fps = 12, amp = 0.08;
var t = Math.floor(time * fps) / fps;
seedRandom(index * 97 + Math.round(t * fps), true);
value + random(-amp, amp);
```

Gate weave on the footage precomp's Position: use the stepped-boil expression
with `amp` 0.5–1.5.

## Multiplane scale compensation

For **unparented** 3D layers seen by `CAM_MAIN` looking down +Z (default
orientation). Keeps each layer at its designed apparent size at the camera's
rest position while the camera moves.

```js
var cam = thisComp.layer("CAM_MAIN");
var zoom = cam.cameraOption.zoom.valueAtTime(cam.inPoint);
var camZ = cam.transform.position.valueAtTime(cam.inPoint)[2];
var k = (transform.position[2] - camZ) / zoom;
value * k;
```

At z = 0 with the default camera (z = −zoom) the factor is 1. If the camera is
rotated or the layer is parented, measure instead of relying on this shortcut.

## 2D parallax rig

Fast alternative to 3D. On `CTRL_VOX` add two Slider controls renamed
`Drift X` and `Drift Y` (pixels at depth 1). On each layer add a Slider renamed
`Depth` (0 = far, 1 = near). Position:

```js
var ctrl = thisComp.layer("CTRL_VOX");
var d = effect("Depth")(1);
value + [ctrl.effect("Drift X")(1), ctrl.effect("Drift Y")(1)] * d;
```

Animate only the two drift sliders.

## A path that follows two layers (red string, connector)

On the shape layer's Path property; add a Slider renamed `Sag` on that layer.
For 2D layers.

```js
var A = thisComp.layer("PIN_A"), B = thisComp.layer("PIN_B");
var pa = fromComp(A.toComp(A.transform.anchorPoint));
var pb = fromComp(B.toComp(B.transform.anchorPoint));
var mid = (pa + pb) / 2 + [0, effect("Sag")(1)];
var d = (pb[0] - pa[0]) / 4;
createPath([pa, mid, pb], [[0, 0], [-d, 0], [0, 0]], [[0, 0], [d, 0], [0, 0]], false);
```

Add Trim Paths to draw it on after both pins land.

## Typewriter via Source Text (alternative to a text animator)

Prefer the text animator (Opacity 0% + Range Selector Start 0→100%, Smoothness
0%) because it keeps per-character styling. Expression version:

```js
var cps = 15;                  // characters per second
var start = inPoint + 0.2;     // seconds
var n = Math.max(0, Math.floor((time - start) * cps));
value.substr(0, n);
```

## Ease a value between two times without keyframes

```js
var t0 = thisComp.marker.key("B05").time, dur = 0.5;
ease(time, t0, t0 + dur, 0, 100);   // or easeOut()/easeIn(); arrays work too
```
