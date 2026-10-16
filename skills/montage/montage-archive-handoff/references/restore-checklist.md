# Manifest and restoration checklist

## Generic manifest shape

```json
{
  "canonical": "project.ext",
  "canonical_sha256": "<actual 64-character SHA-256>",
  "files": [
    {"path": "project.ext", "size": 123, "sha256": "<actual SHA-256>"}
  ]
}
```

This is illustrative syntax, not a valid receipt. Compute hashes and sizes from
the actual files, include every intended dependency, and keep paths relative to
the package root. The verifier checks only listed paths; an omitted dependency
will not magically become a failing entry. Do not use symbolic links to make an
archive appear self-contained when the media still lives elsewhere.

## Handoff README

Record: canonical file, selected sequence(s), software/version, frame rate and
colour spaces, render/reference files, media-root layout, included/excluded items,
required separately licensed fonts/plugins, handles, relink steps, captions,
known differences, rights notes and the person responsible for acceptance.
No passwords, API keys or activation codes belong in this document.

## Restoration evidence

| Test | What it establishes |
| --- | --- |
| Manifest verification before transfer | Listed bytes match the intended package |
| Verify after copy/restore | Those bytes survived the transfer |
| Open in native app | Project can load in that specific environment |
| Dependency/native audit | Checked media/fonts/plugins/sequences resolve correctly |
| Render and compare | Checked outputs remain visually/aurally consistent |

A byte-identical restore alone does not prove the last three rows. Automated
measurements do not replace a normal-speed human audio/visual review.

## Gallery boundary

The demo's canonical file is an explicit **project note**, not a fake `.prproj`
or `.aep`. A real synthetic MP4, cut-candidate report and contact sheet are
listed, copied into a new restoration directory and verified with the existing helper. It demonstrates
file integrity only. No production project, native restore or dependency scan
is claimed.

## Sources

Adobe indexed documentation checked 2026-10-16; native tests require a connected
host and a safe synthetic project.

- [Adobe — copy projects](https://helpx.adobe.com/premiere/desktop/organize-media/create-projects/copy-project.html).
- [Adobe — consolidate and archive](https://helpx.adobe.com/premiere/desktop/organize-media/create-projects/consolidate-and-archive-projects.html).
- [Adobe — move projects to another computer](https://helpx.adobe.com/premiere/desktop/organize-media/create-projects/move-project-to-another-computer.html).
