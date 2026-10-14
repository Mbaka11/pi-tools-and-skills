# Cinematic Score & SFX Skill

An agent skill for adding an original score, cinematic sound effects, ambience, and editable audio stems to an existing video edit.

This is a **score-to-picture** workflow: the video is the timing authority, and the audio is designed around its cuts, performances, reveals, dialogue, and emotional arc.

The skill is deliberately provider-agnostic. It does not contain API keys, private project files, generated audio, third-party model weights, or a bundled audio engine. Bring the music/SFX providers and editing tools you prefer.

## What this skill does

The skill teaches an AI coding/production agent how to:

- inspect a video and identify protected source audio;
- perform a cinematic spotting pass;
- distinguish hard-sync events from soft emotional transitions;
- build one coherent score architecture instead of stacking unrelated songs;
- turn aesthetic direction into precise, original music-generation prompts;
- generate harmonically dependent elements together;
- conform generated cue transitions to exact picture events;
- add risers, impacts, drones, reverses, swells, ambience, and diegetic effects selectively;
- preserve dialogue, Foley, approved cues, and locked regions across revisions;
- mix non-destructively;
- export a review mix plus zero-aligned stems for DaVinci Resolve, Premiere Pro, or Final Cut Pro.

## What it does not do

This is not:

- a video-generation model;
- an automatic picture editor;
- a dialogue or lip-sync system;
- a replacement for a human mix review;
- a model-weight bundle;
- a generic “add random music everywhere” prompt.

It is specifically for **adding a score and cinematic audio accents to an existing video**.

## Start with Foley, not music

The best input is a video that already has believable production audio, Foley, and ambience—but **no music yet**.

Why? Foley gives the scene physical reality. The score can then shape emotion without being forced to invent every footstep, cloth movement, wind bed, door sound, or environmental cue at the same time.

### If your footage is AI-generated

Tell the video model explicitly:

> Generate synchronized dialogue/production sound, ambience, and Foley only. Do not generate music, score, songs, melodic underscore, or rhythmic background music.

If the video model cannot produce usable Foley, create it separately before scoring. You can experiment with [Tencent HunyuanVideo-Foley](https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley), but audition the result carefully: in our practical workflow it was not consistently strong enough to treat as a finished professional Foley pass. It is a starting point, not an approval.

If you use HunyuanVideo-Foley, review its own model license and system requirements separately. This repository does not include it.

### If your footage is live action or traditionally animated

Use the cleanest available production audio and Foley edit. Do not lay in temp music unless it is clearly separated and removable. If temp music is already baked into the only audio stream, source separation may damage dialogue and effects; obtaining clean stems is much better.

## Recommended companion skills and tools

This skill is the creative and editorial decision layer. It becomes more useful when paired with the following capabilities.

### Strongly recommended

| Capability | Why you need it | Example |
|---|---|---|
| Media inspection | Verify streams, duration, frame rate, channels, and codecs | `ffprobe`, `ffmpeg` |
| Timeline/compositor | Place cues, automate gains, preview, and render deterministically | HyperFrames or an NLE |
| Music/SFX generation | Produce original cues and one-shots from the briefs | ElevenLabs or another licensed provider |
| Audio editing | Stretch, trim, crossfade, normalize, and export PCM WAV | `ffmpeg`, DAW, or NLE |
| Human listening review | Validate taste, cohesion, sync, and dialogue clarity | Headphones + speakers |

### Useful agent skills

- **HyperFrames / general-video** — timeline assembly, deterministic placement, preview, render, and verification.
- **Media-use** — provider setup, authenticated generation, downloads, provenance, and media normalization.
- **ElevenLabs** — original music and sound-effect generation when ElevenLabs is the chosen provider.
- **AI-film-production-pipeline** — shot/asset continuity and broader film-production orchestration.
- **Seedance or another video-model skill** — picture generation; explicitly request Foley/ambience without music when the model supports audio.

The skill works without these exact names. Substitute equivalent tools as long as the workflow preserves timing authority, protected audio, generation evidence, and editability.

## Requirements

Minimum:

- an agent that can read Markdown skills;
- a video file;
- a way to inspect and render audio/video;
- a licensed source of original music and effects, or human-created audio;
- enough disk space for lossless stems.

Recommended command-line tools:

```bash
ffmpeg -version
ffprobe -version
```

For Python- or model-based audio analysis, use an isolated environment and pin dependencies. This repository itself has no runtime dependencies and makes no network calls.

## Installation

### Option 1: install as a local agent skill

Clone the repository, then copy or symlink its folder into your agent's skill directory.

```bash
git clone https://github.com/thenpceo/cinematic-score-and-sfx-skill.git
mkdir -p ~/.agents/skills
cp -R cinematic-score-and-sfx-skill ~/.agents/skills/cinematic-score-and-sfx
```

If your agent uses a different skill directory, place the repository there instead. Keep `SKILL.md` at the root of the installed skill.

### Option 2: use it directly in a project

Clone it into a repository-level skills directory supported by your agent, then instruct the agent to use `cinematic-score-and-sfx` for score-to-picture tasks.

### Provider setup

This skill does not prescribe a provider and never stores credentials.

- Authenticate through the provider's standard credential flow.
- Keep secrets in your system keychain, provider CLI, or uncommitted environment configuration.
- Never paste API keys into `SKILL.md`, a prompt manifest, generation log, shell history, or a public repository.
- Confirm commercial rights and output terms for the provider/model you select.

## Quick start

Give your agent:

1. the video path;
2. a statement of what audio must be preserved;
3. whether the picture is locked;
4. creative direction for the score;
5. the desired final deliverables.

Example request:

```text
Use the cinematic-score-and-sfx skill on ./picture-lock.mp4.

Protect all dialogue, production sound, and Foley already in the source.
The picture is locked at 24 fps. Spot the full film before generating anything.

Create one cohesive score whose motif evolves across the piece. Use only a few
motivated cinematic accents: a soft riser into the reveal, one low impact on the
doorway entrance, and an ambience transition between the exterior and interior.

Show me the spotting map, lock ledger, cue architecture, prompts, and expected
generation cost before paid calls. After approval, generate and assemble a review
mix. Deliver the final MP4 plus zero-aligned 48 kHz/24-bit WAV stems and a cue sheet.
```

## Best practices

### 1. Lock picture or name what is provisional

Scoring a moving edit creates avoidable rework. Confirm the duration, frame rate, and cut points. If the edit is provisional, label it honestly and avoid expensive micro-sync work until it stabilizes.

### 2. Spot before generating

Watch the complete piece. Record actual visible events and dialogue pockets. Do not write prompts from a verbal summary alone.

### 3. Use fewer, evolving cues

The most common failure is too many different songs. Prefer one cue that changes state—ambient opening, motif arrival, beat drop, thinning, suspended tail—over unrelated tracks at every scene.

### 4. Generate correlated music together

If melody, bass, drums, riser, impact, and continuation must agree in key and groove, put them in one generation. Separate generations that merely name the same key frequently clash in tuning, voicing, swing, room, or phrase shape.

### 5. Keep Foley and replaceable effects separate

Footsteps, cloth, doors, wildlife, machines, room tone, user recordings, and diegetic sounds benefit from independent placement and gain control. Keep them as separate assets unless they intentionally transform into the music.

### 6. Use hard sync sparingly

A jump, reveal, impact, footstep, or sudden look may deserve frame-accurate sync. Most emotional transitions should breathe across a window. Constant punctuation feels like a trailer or game UI.

### 7. Let cause precede reaction

If a sound startles a character, its onset should normally arrive just before the first visible reaction frame—not after the reaction has begun.

### 8. Describe musical mechanics, not only references

Do not rely on “cinematic,” “Asian,” “lo-fi,” “dark,” or an artist name. Define:

- tonal language;
- lead instrument and articulation;
- groove and swing;
- bass/drum relationship;
- recording texture;
- emotional temperature;
- density;
- forbidden substitutes.

Ask for an original work. Do not request imitation of a living artist or reproduction of a recognizable song.

### 9. Measure generated transitions

Music models treat timestamps as guidance. Listen to the returned cue, identify where its sections really change, then conform that same continuous cue to picture with conservative pitch-preserving stretch.

### 10. Revise one axis at a time

If timing and structure work but instrumentation is wrong, lock timing and structure. If an ending is approved, checksum and freeze it. Regenerate only the unresolved cue or axis.

### 11. Mix around dialogue with arrangement first

Before simply turning music down, reduce midrange competition, transient density, countermelodies, and rhythmic clutter. Then automate gain if needed.

### 12. Deliver stems, not just a preview

For NLE handoff, every consolidated WAV should begin at `00:00:00:00`, equal the full picture duration, and preserve placement with silence. Separate Music, Ambience, Foley, Cinematic SFX, and Tech/Diegetic categories.

## Suggested folder structure

```text
project/
  picture/
    picture-lock.mp4
  source-audio/
    dialogue.wav
    production-foley.wav
  raw/
    cue_a_v01_provider-output.mp3
  music/
    cue_a_v01.wav
    cue_a_v01_aligned.wav
  sfx/
    reveal-riser.wav
    doorway-impact.wav
  manifests/
    lock-ledger.md
    spotting-map.csv
    generation-log.json
    cue-sheet.csv
    mix-automation.csv
  stems/
    Music_Cue_A.wav
    Ambience.wav
    Foley.wav
    Cinematic_SFX.wav
  renders/
    review-mix.mp4
    final-mix.mp4
```

## Review checklist

Before final render:

- [ ] Picture duration and frame rate were verified.
- [ ] Protected audio and locked cues are listed and checksummed.
- [ ] The whole video was spotted.
- [ ] Hard sync, soft transitions, dialogue pockets, causal offsets, and silence are documented.
- [ ] The score feels like one musical argument.
- [ ] Correlated musical elements were generated together.
- [ ] Actual returned transition times were measured.
- [ ] Cinematic SFX are motivated and not overused.
- [ ] Dialogue remains intelligible.
- [ ] Approved regions were not regenerated.
- [ ] The final video decodes end-to-end without errors.
- [ ] Stems are full-duration, zero-aligned, lossless, and documented.

## Security and privacy

This repository contains only Markdown guidance.

It contains no:

- API keys or tokens;
- personal filesystem paths;
- customer or production assets;
- generated music or sound effects;
- video files;
- model weights;
- executable scripts;
- vendored third-party code.

Generated prompts and manifests can still leak project names, unreleased story details, filenames, or provider IDs. Review them before committing a production project publicly.

## Limitations

- Generative music timing is approximate.
- Model output quality and licensing vary by provider.
- Automatic Foley is still inconsistent and must be auditioned.
- A waveform can validate timing and dynamics, not taste.
- Final approval requires listening on more than one playback system.
- This workflow cannot restore clean dialogue/Foley perfectly when music is baked into the only source mix.

## License

MIT. See [LICENSE](LICENSE).

## Acknowledgment

This workflow was developed through iterative production on a short narrative film, then generalized so the public package contains no project-specific characters, assets, prompts, audio, or private paths.
