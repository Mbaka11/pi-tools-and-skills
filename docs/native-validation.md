# Native Premiere validation — separate evidence gate

This is a **procedure, not an execution receipt**. FFmpeg examples and CI do not
prove Premiere attachment, effects, timeline behavior or project restoration.
A disconnected host means pending, never passed.

## Safe setup

1. Discover current bridge/host availability and the installed Premiere version.
   Load its current tool contracts; do not assume remembered APIs exist.
2. Read live project/sequence identity, path, dirty state and media status before
   any mutation. Do not close, replace or save an unrelated open client project.
   If a new project cannot be created safely, ask for a safe workspace first.
3. Use a new private synthetic project directory. Copy only the intended original
   gallery assets or regenerate test sources there; never edit the toolbox's
   published media or a managed Pi installation.
4. Record a baseline, perform one bounded test, inspect live state and exported
   evidence, then save a separate reversible checkpoint. Keep one project writer.

## Test matrix

| Test | Evidence required | Remaining limitation |
| --- | --- | --- |
| Proxy attachment / online relink | Attach source/proxy pair; inspect native attachment status; toggle; export using originals and compare checked frames | Silent synthetic pair does not prove camera timecode, VFR or multichannel behavior |
| Multicam offset / audio routing | Independent synthetic camera files, known event offsets, native start/middle/end review and routing inspection | Anchors alone do not prove lip sync or nonlinear drift |
| Colour / Lumetri | Recorded input/sequence/output settings; known chart correction; exported frame measurements | Not calibrated-display or real skin-tone validation |
| Dialogue processing | Bypass/processed comparison, duration/start alignment, native settings and output measurements | Tone/noise is not speech; human intelligibility/listening remains separate |
| Time remapping | Explicit source capture/playback/timeline rates, sampling mode and checked source/output boundaries | Piecewise timing is not optical flow or a smooth Bezier ramp test |
| Collection / restore | New collected folder; separately opened restored project that cannot fall back to original paths; dependency inspection and reference render | Hash equality alone is insufficient |

Transcript and language/accessibility review need suitable consented test content
and qualified human review; do not substitute a generated receipt. Never upload
recordings or install missing plugins/models without explicit authorization.

## Private receipt

For each test record: tested/not tested/failed, actual host/version, project and
sequence identity, settings, source/output hashes, exact frames checked, native
screenshots/export paths, observed result, unresolved limits and rollback path.
Keep private absolute paths and host captures in the project's ignored evidence
directory, not this public repository. Publish only reviewed synthetic evidence.

Related: [proxy workflow](../skills/montage/montage-proxy-conform/SKILL.md),
[multicam](../skills/montage/montage-multicam-sync/SKILL.md),
[colour](../skills/montage/montage-colour-finishing/SKILL.md),
[dialogue](../skills/montage/montage-dialogue-cleanup/SKILL.md),
[retiming](../skills/montage/montage-time-remapping/SKILL.md),
[handoff](../skills/montage/montage-archive-handoff/SKILL.md).
