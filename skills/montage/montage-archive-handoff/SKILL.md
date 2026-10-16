---
name: montage-archive-handoff
description: Package editable video projects for handoff and restoration - inventory dependencies and rights, collect into a new location, distinguish full copies from trimmed/transcoded consolidation, preserve handles and native projects, hash listed files, test an isolated restore and document missing plugins/fonts/Dynamic Link items. Use for project archive, handoff, delivery package, collect files, moving machines or restore verification. Never deletes originals or claims that hashes prove a project opens.
compatibility: Any NLE; Premiere Project Manager optional. The existing delivery-manifest verifier uses standard-library Python and can verify arbitrary listed files; it does not parse an NLE project or discover dependencies.
metadata:
  version: "1.0.0"
  short-description: Portable project packages with measured restoration evidence
---

# Project archiving and handoff

[Tiny example — real manifest verification and byte-for-byte restore](../../../examples/README.md#montage-archive-handoff).

An archive is useful only if the intended recipient can restore the intended
work. A folder full of media and a matching checksum are necessary evidence,
not proof of complete dependencies or a working editable project.

## Agree on the handoff contract

Confirm software/version, native project, selected sequences, source versus
consolidated media, handles, proxies, fonts/plugins, colour transforms, captions,
licences and storage destination. Establish whether the recipient needs full
editorial flexibility or a smaller finish-only package. Do not guess a retention
period or delete source drives/cards as part of packaging.

## Inventory and collect

1. Save and checkpoint the canonical project after checking its dirty state.
2. Inventory used footage/audio/stills, nested/multicam sequences, Dynamic Link
   projects, graphics/templates, LUTs, captions, fonts and third-party effects.
3. Separate redistributable dependencies from items the recipient must license
   or install. A font/plugin licence rarely permits copying its installer.
4. Use the NLE's collect/copy function into a **new** destination. For Premiere,
   distinguish Collect Files from Consolidate and Transcode; review selected
   sequences, nested dependencies and exclude-unused options before applying.
5. If trimming/transcoding, document codec, colour/timebase decisions and handles.
   Retime/freeze/nested effects can require media beyond obvious cut boundaries.
   Keep originals separately until an approved restore and retention decision.
6. Include an encoded reference, source/timecode notes, captions, known issues,
   software/plugin versions and a manifest of the intended package.

## Verify listed bytes

From the repository root, use the existing verifier:

```sh
python skills/after-effects/ae-production-workflow/scripts/verify-delivery-manifest.py handoff/delivery-manifest.json --root handoff
```

Its generic file/hash checks also work for non-AE archives. The manifest must
name a nonempty canonical project/record and list it in `files[]`, with relative
paths, byte sizes and SHA-256. See [manifest and restoration checks](references/restore-checklist.md).
The verifier does **not** discover missing dependencies, inspect project contents,
prove ownership or test an application's ability to open the package.

## Isolated restoration test

Restore into a new directory on the recipient's machine or a clearly isolated
workspace. Verify hashes again. Open the copied native project without changing
the original; ensure it resolves the restored media rather than falling back to
old absolute paths. Do not rename/unmount/delete a live production media tree
just to force this test. Use a separate machine or controlled sandbox instead.

Check missing media, fonts, plugins, captions, nested sequences and selected
frames; render a short reference comparison and inspect sound/sync. Record byte
verification and native restoration as separate results. If the host is absent,
report native restoration as pending, not passed.

Deliver a concise README and the archive manifest; keep credentials, caches,
private captures and unnecessary personal metadata out of the package.
