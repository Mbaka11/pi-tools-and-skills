# Changelog

Versioned releases use Semantic Versioning. Published tags are not moved.

## 0.2.0

- Add an After Effects and montage toolbox: eight new skills in category folders
  `skills/after-effects/` and `skills/montage/` (fourteen skills in total).
- After Effects: `ae-vox-editorial` (native Vox-style editorial collage),
  `ae-expressions-rigs` (language-independent expressions and control rigs),
  `ae-vfx-compositing` (native-first compositing with licence-checked AI options).
- Montage: `led-signage-content` with `led_tool.py` (PixaNova roll-up and wall
  profiles, text-size calculator, guide overlays, pixel-exact exports, per-screen
  splits, device test cards), `video-delivery-qc` with `media_qc.py` (full decode,
  black/freeze, loudness, loop seam, contact sheets), `sound-design-sfx` with
  `sfx_place.py` (frame-accurate cue stems), `montage-editing-craft` with
  `srt_check.py` (French caption checks and fixes), and the
  `vox-explainer-pipelines` adapter.
- Vendor two MIT upstreams byte-for-byte at pinned commits with SHA-256 hashes:
  jaredcassoutt/vox-editorial and thenpceo/cinematic-score-and-sfx-skill.
- Add a reviewed catalog of AE bridges, Vox pipelines, motion frameworks, SFX,
  VFX and editing tools with licences and verdicts (`docs/montage-catalog.md`).
- Move `ae-production-workflow` to `skills/after-effects/` (content 1.0.2 adds a
  related-skills section; helpers unchanged). Filters that referenced the old
  path must be updated.
- Checks: recursive category discovery with an explicit skill inventory;
  unreleased upstream snapshots pinned by branch, commit and date; the update
  check compares their branch head read-only; tests for every new helper.

## 0.1.0

- Initial cross-project pi package with six curated skills.
- Preserve the personal After Effects workflow, helpers, and delivery templates.
- Generalize Cowgorithm's research, reporting, and on-demand task workflows.
- Add the REA integration guide with the exact 6.4.0 upstream skill snapshot,
  MIT notice, package integrity, file hashes, and disabled MCP example.
- Add a pi-native API investigation workflow inspired by Reverse API Engineer
  0.14.0, excluding embedded secrets and autonomous account access.
- Include a bounded offline HAR structural summary helper, read-only release
  checking, optional pinned source retrieval, tests, and maintenance guidance.
- Keep original personal material unlicensed and preserve third-party licenses.
- No engine installation, browser connection, pi profile migration, or ApplyPilot
  modification occurs as part of this release.
