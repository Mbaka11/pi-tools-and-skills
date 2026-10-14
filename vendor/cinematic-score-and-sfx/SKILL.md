---
name: cinematic-score-and-sfx
description: "Design, generate, synchronize, revise, mix, and deliver an original score, cinematic sound effects, ambience, and editable audio stems for an existing picture edit. Use when picture is the timing authority and the user needs spotting, cue architecture, music-generation prompts, SFX placement, hard-sync accents, dialogue-safe mixing, or an NLE handoff."
---

# Cinematic score and SFX

Use this skill when the picture already exists and the user wants original music, cinematic sound effects, ambience, synchronization, revisions, a final mix, or editable stems.

The picture is the timing authority. The goal is not to cover every second with sound. The goal is to make one coherent musical and sonic argument whose changes sharpen the story.

## Route boundary

This skill owns:

- spotting an edited video;
- designing a score architecture;
- translating creative direction into original music-generation prompts;
- placing causal and cinematic SFX;
- preserving production audio, dialogue, and approved cues;
- aligning generated transitions to exact picture events;
- mixing added audio non-destructively;
- exporting a review mix and editable NLE stems.

This skill does not own picture editing, dialogue generation, lip sync, or fully automatic Foley creation. Use companion tools or skills for those jobs, then bring their outputs into this workflow as protected or independently editable material.

## Inputs

Required:

- a picture-locked or clearly provisional video edit;
- its duration, frame rate, dimensions, and audio-stream inventory;
- a clear statement of which existing audio must be preserved.

Strongly recommended:

- dialogue and production audio already in place;
- a usable Foley/ambience baseline with **no music**;
- references described as musical traits rather than a request to imitate a specific living artist;
- an NLE or deterministic timeline/compositor for final placement and export.

## Non-negotiable principles

1. **Separate story structure from musical identity.** Timing, emotional arc, instrumentation, harmony, groove, mix, and content are separate revision axes. Freeze approved axes.
2. **Generate dependent elements together.** A motif, bass line, drums, riser, impact, and continuation that must sound related should normally be one continuous generation.
3. **Keep independent sounds independent.** Foley, ambience, dialogue, user recordings, and replaceable one-shots should stay on separate tracks unless a sound must literally transform into the score.
4. **Translate taste into traits.** Specify tonal language, lead-instrument role, articulation, rhythmic pocket, recording texture, arrangement density, emotional temperature, and exclusions. Do not ask a model to copy a living artist or recognizable song.
5. **Picture time beats prompt time.** Model timestamps are approximate. Measure the returned cue and conform its own continuous material to picture.
6. **Protect approvals.** Never regenerate an accepted cue because a neighboring cue changed. Preserve it by path and checksum.
7. **Deliver editability.** A good preview is not the editorial handoff. Consolidate zero-aligned stems, document automation, and verify the package.

## Phase 0 — Establish authority and locks

Inspect the current project, video, audio streams, frame rate, duration, existing timeline, and accepted cues. Do not infer acceptance from the existence of a file.

Create a lock ledger:

| Element | State | May change? | Evidence |
|---|---|---:|---|
| Picture edit | locked / provisional | yes/no | source path + duration |
| Dialogue/production audio | protected / replaceable | yes/no | source stream/path |
| Foley/ambience | approved / provisional | yes/no | source stream/path |
| Cue timing | approved / provisional | yes/no | review note |
| Cue identity | approved / provisional | yes/no | review note |
| Cue mix | approved / provisional | yes/no | review note |
| Cinematic SFX | approved / provisional | yes/no | review note |

Record a SHA-256 checksum for every locked audio file. Recheck it at handoff.

**Gate:** picture duration and frame rate are verified; protected audio and approved cue axes are explicit.

## Phase 1 — Spot the picture

Watch the full video before generating music. Build a spotting map from actual visible events, not round-number guesses. Inspect frames around uncertain moments.

For every state change, record:

- absolute picture time;
- cue-local time;
- frame/timecode;
- visible story event;
- desired viewer feeling;
- current musical state;
- next musical state;
- sync strength: hard or soft;
- dialogue/production-sound constraints;
- intended handoff or tail.

### Hard and soft sync

**Hard sync** lands on a frame or within roughly one frame: a jump, reveal, impact, footfall, sudden look, door slam, logo, or cut that explicitly motivates sound.

**Soft sync** emerges across a window: unease growing, wonder widening, a groove thinning, or ambience becoming musical.

Do not hard-sync everything. One or two strong accents are more cinematic than constant punctuation.

### Cause precedes reaction

When sound causes a visible reaction, place the causal onset just before the first reaction frame. Verify the first actual movement frame, not merely the cut containing it. Record the offset.

### Dialogue pockets

Mark dialogue starts and ends. Decide whether music should duck, thin its midrange, reduce transient density, simplify its melody, or stop. Arrangement space is usually better than brute-force volume reduction.

**Gate:** the spotting map distinguishes hard-sync points, soft transitions, dialogue pockets, causal offsets, and protected silence.

## Phase 2 — Design one musical argument

Think in musical states, not a pile of songs. Short films usually need fewer internally evolving cues, not a new track for every scene.

For each cue define:

- narrative job;
- starting state;
- transformation states;
- climax or drop;
- exit and tail;
- tonal center or pitch collection;
- motif ownership;
- groove family and tempo feel;
- lead voice and supporting roles;
- recording/production texture;
- forbidden substitutes;
- dialogue strategy.

### What belongs in one generation

Use one continuous generation when:

- an introductory texture becomes a melody;
- that melody continues across a beat drop;
- bass and drums must share one pocket;
- tension resolves into an impact and groove;
- an impact's resonance becomes the bass or kick;
- a motif must remain recognizable across changing energy.

Use separate assets when:

- the sound is diegetic or editorially replaceable;
- the user supplied the recording;
- it needs independent placement or level control;
- it is Foley, ambience, dialogue, or a one-shot not fused to the harmony.

Do not stack separately generated melody, bass, and drums merely because it seems controllable. If they must feel like one composition, generate them together.

## Phase 3 — Write the generative brief

When the user names a genre, culture, era, soundtrack, artist, or instrument, extract the traits instead of copying the label.

Specify:

1. **Emotional temperature:** sunlit, intimate, mischievous, anxious, grounded, tender, or similar.
2. **Tonal language:** major, minor, modal, pentatonic, ambiguous, consonant, or dissonant; say whether key changes are allowed.
3. **Lead role:** which instrument family owns the hook and whether it persists through later sections.
4. **Articulation:** plucked, bowed, breathy, muted, tremolo, slides, harmonics, staccato, legato, close-miked, dry, or roomy.
5. **Groove:** tempo feel, swing, kick/snare character, humanization, density, and relationship between melody and drums.
6. **Arrangement relationship:** bass, motif, and drums share one tonal center and rhythmic pocket; the rhythm section answers spaces in the lead phrase.
7. **Production texture:** dusty sampler, acoustic room, tape saturation, vinyl grain, field-recorded tactility, pristine modern mix, or similar.
8. **Exclusions:** competing leads, unwanted genre defaults, vocals, trailer devices, trap hats, orchestral bombast, glossy synth risers, unrelated countermelodies, or a resolved ending.

If a particular instrument is essential, make it the **foreground hook**, keep it as the only lead, require it to remain audible after the beat enters, and forbid generic substitutes.

### Timecoded prompt template

```text
Create ONE seamless original instrumental cue, exactly <duration>.

GLOBAL IDENTITY
- one tonal family throughout;
- one recurring motif;
- define the lead role, articulation, groove, and production texture;
- no restart, key change, imitation, or separate-song feeling.

0:00–A — STATE 1
Describe only what is present. Explicitly forbid elements that must not arrive yet.

EXACTLY A — STATE 2
Name the new foreground element and what continues unchanged.

EXACTLY B — HARD SYNC
Name the visible event and exact musical change. Reassert that motif, tonal center, and groove remain related.

EXACTLY C — HANDOFF
Describe what disappears, what rings out, and whether the ending is resolved or suspended.

NEGATIVE CONTRACT
List likely wrong defaults and competing lead voices.
```

Prompts use cue-local time. The production manifest records both cue-local and absolute picture time.

## Phase 4 — Generate economically and preserve evidence

Before a paid generation:

- lock duration, model, provider, prompt, seed if available, and expected cost;
- save the prompt and plan to a manifest;
- generate only the unresolved cue;
- never write credentials into prompts, logs, or the repository;
- keep raw provider output separate from normalized and aligned derivatives.

Use stable names:

```text
raw/<cue_id>_<revision>.<provider_format>
music/<cue_id>_<revision>.wav
music/<cue_id>_<revision>_aligned.wav
generation-log.json
```

Never overwrite an approved raw output.

## Phase 5 — Diagnose before revising

Review independent axes:

| Axis | Question | Typical fix |
|---|---|---|
| Structure | Are the right states present in the right order? | Rewrite architecture or regenerate |
| Identity | Is the lead voice, tonal language, articulation, and production aesthetic correct? | Strengthen role/exclusions; regenerate only this cue |
| Cohesion | Do melody, bass, drums, and transitions feel like one composition? | Generate dependent elements together |
| Sync | Do transitions hit picture? | Conform the same cue internally |
| Mix | Are dialogue, Foley, and music balanced? | Gain, automation, EQ, or arrangement duck |
| Content | Is a specific SFX or motif wrong? | Replace only that asset or section |

Feedback such as “timing and vibe are perfect; instruments are wrong” locks structure and sync. “The ending is perfect” locks that asset; do not regenerate it.

Avoid semantic prompt traps. Words such as “epic,” “dark,” “cinematic,” “riser,” and “impact” can trigger generic trailer scoring. Qualify them with material, scale, texture, rhythm, and exclusions.

## Phase 6 — Conform the continuous cue

Generated timestamps drift. Measure the return:

1. verify duration, sample rate, and channels;
2. inspect waveform and onset energy around intended landmarks;
3. listen for actual state changes;
4. record actual cue-local transition times;
5. map actual segments to desired picture segments;
6. time-stretch segments from the **same generation** with pitch preservation;
7. concatenate seamlessly and apply only the intended tail or fade;
8. verify duration and transition times again.

This preserves shared harmony, motif, players, room, and production texture. If a segment requires extreme stretching, regenerate it with clearer duration instructions.

**Gate:** every hard sync is frame-accurate; every soft transition is inside its approved window; tails do not invade protected dialogue or silence.

## Phase 7 — Place SFX and mix non-destructively

Keep protected source audio separate from added music and effects. Use stable track names and IDs.

Mix in this order:

1. protected dialogue and production sound;
2. score architecture;
3. ambience continuity;
4. hero Foley and causal SFX;
5. cinematic accents such as risers, impacts, tonal thuds, drones, reverses, and swells;
6. technology/diegetic accents;
7. dialogue ducking and final automation.

Use cinematic SFX selectively. A riser should prepare a real transition. An impact should land on a motivated event. Ambience should connect cuts and establish space, not become an anonymous wash. Do not use loud effects to hide a weak musical transition.

## Phase 8 — Review and lock

Review in this order:

1. narrative and emotional arc;
2. musical identity;
3. hard sync;
4. continuity across transitions;
5. dialogue intelligibility;
6. Foley causality;
7. tail and final frame.

The review handoff must state what changed and what remained protected. When the user approves a region, update the lock ledger and checksum it immediately.

Do not render the final video merely because the preview looks complete. Verify the actual artifact after explicit approval or under the active autonomy contract.

## Phase 9 — Deliver editable stems

For Resolve, Premiere, or Final Cut, deliver editability rather than only a mixed WAV.

### Individual consolidated stems

- one file per music cue, ambience bed, Foley cue, and cinematic/diegetic cue;
- every file starts at timeline `00:00:00:00`;
- every file equals the full picture duration;
- preserve placement with leading and trailing silence;
- use lossless PCM WAV, normally 48 kHz/24-bit stereo unless the project says otherwise;
- bake documented gain and automation when the goal is to match the approved preview;
- alternatively provide raw-level stems plus an automation sheet for maximum remix control.

### Convenience buses

Optionally deliver Music, Ambience, SFX/Foley/Tech, and All-Added-Audio buses. Put them in a folder labeled `DO NOT DOUBLE`; they duplicate individual stems.

### Documents

Include:

- cue-sheet CSV with filenames, category, cue ID, picture start seconds, timecode, source duration, gain, and automation;
- manifest JSON with technical format and exclusions;
- import README;
- optional FCP7 XML or equivalent NLE timeline;
- checksummed ZIP archive.

State explicitly whether original video, dialogue, and production audio are excluded.

### Verification

Programmatically verify:

- expected stem and bus counts;
- identical full duration for every consolidated WAV;
- codec, sample rate, bit depth, and channels;
- no video streams in stem files;
- pre-cue silence and alignment;
- XML validity and track count if included;
- archive integrity and checksum;
- locked-source identity after documented gain and automation.

## Final acceptance criteria

- Picture timing, duration, and frame rate were inspected rather than assumed.
- Existing dialogue, production audio, Foley, and approved cues were explicitly protected.
- A spotting map identifies hard sync, soft transitions, dialogue pockets, causal offsets, and silence.
- The score behaves as one musical argument rather than unrelated songs.
- Correlated elements were generated together.
- Generated timestamps were measured and conformed to picture.
- SFX are motivated, sparse, independently editable where useful, and do not hide musical problems.
- The final mix was decoded end-to-end and inspected.
- Editorial stems are zero-aligned, full-duration, documented, and verified.
