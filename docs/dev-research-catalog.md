# Research, ML, health-AI and Flutter tools: reviewed catalog

Research snapshot from **2026-10-29**, made for a health-AI mobile project (ECG photo
interpretation, Flutter app, FastAPI backend) but reusable across projects. Listing a
project here is **not** an installation, endorsement or licence grant. Commits are the
revisions that were reviewed; review again before installing anything, and prefer that
exact commit.

Legend — **Use now**: reviewed and in use in at least one project. **Later**: useful for a
future phase. **Reference**: worth reading. **Caution**: licence, rights or security issue.

## How to install a pinned skill package

Third-party skills are not copied into this toolbox. Add them per project (or in personal
settings) as pinned git packages with a skill filter, for example in `.pi/settings.json`:

```json
{
  "packages": [
    {
      "source": "git:github.com/anthropics/skills@ca45fc496a3436251f191354091d557da31c15b5",
      "skills": ["skills/skill-creator/SKILL.md"],
      "extensions": [], "prompts": [], "themes": []
    }
  ]
}
```

Very large repositories (for example K-Dense, ~470 MB) are better vendored selectively into
the project's `.agents/skills/` with their licence, as done in
[ECG-AI-KG](https://github.com/Mbaka11/ECG-AI-KG/tree/main/.agents/skills).

## Agent skills

| Skills | Source and commit | Licence | Verdict |
| --- | --- | --- | --- |
| `literature-review`, `citation-management`, `scientific-writing`, `neurokit2`, `pytorch-lightning` (selected from 100+) | [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) `5f2bc0341354` | MIT (repo; `pytorch-lightning` metadata says Apache-2.0) | **Use now** (vendored in ECG-AI-KG). Scripts call public scholarly APIs; the literature-review schematic scripts use OpenRouter only if `OPENROUTER_API_KEY` is set. README says biosignal skills are research-only. |
| `skill-creator`, `frontend-design`, `webapp-testing` | [anthropics/skills](https://github.com/anthropics/skills) `ca45fc496a34` | Apache-2.0 (per-folder `LICENSE.txt`) | **Use now** as a pinned package. `frontend-design` is web-oriented, not Flutter. |
| `docx`, `pdf`, `pptx`, `xlsx` | same | **Source-available, all rights reserved** (not open source) | **Caution** — load from upstream only, never copy. |
| `flutter-setup-localization`, `flutter-apply-architecture-best-practices`, `flutter-build-responsive-layout`, `flutter-fix-layout-issues`, `flutter-add-widget-test`, `flutter-add-integration-test` (+ other `flutter-*`, `dart-*`) | [flutter/agent-plugins](https://github.com/flutter/agent-plugins) `90fa51dc9d1b` (`flutter/skills` redirects here) | BSD-3-Clause | **Use now** as a pinned package for Flutter projects; official Flutter team. |
| `paper-search` skill + MCP/CLI (arXiv, PubMed, Semantic Scholar, Crossref…) | [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp) `cab1b5cc276a` (skill at `dsh/skills/paper-search/`) | MIT | **Later** — needs a Python install; **never enable its optional Sci-Hub source**. |
| `hf-cli`, `huggingface-datasets`, trainers | [huggingface/skills](https://github.com/huggingface/skills) | Apache-2.0 | **Later** (model/dataset hosting). |
| Software process skills (TDD, plans, subagent development) | [obra/superpowers](https://github.com/obra/superpowers) | MIT | **Reference** — opinionated; try on a branch first. |
| ~40 community Flutter skills | [zakariaf/Flutter-Skills](https://github.com/zakariaf/Flutter-Skills) | not checked | **Reference** only until reviewed. |

## MCP servers

| Server | Licence | Verdict |
| --- | --- | --- |
| Dart & Flutter MCP (`dart mcp-server`, ships with the Dart SDK) — [docs](https://docs.flutter.dev/ai/get-started) | Dart SDK (BSD-style) | **Later** — install when Flutter work starts: `{"command": "dart", "args": ["mcp-server"]}` |
| [mobile-dev-inc/maestro](https://github.com/mobile-dev-inc/maestro) (`maestro mcp`) — mobile E2E tests, Flutter supported | Apache-2.0 | **Later** (app testing) |
| [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) | Apache-2.0 | **Later** (web admin panels) |
| [datalayer/jupyter-mcp-server](https://github.com/datalayer/jupyter-mcp-server) | not checked | **Reference** |
| Figma MCP (hosted) | Figma terms | Skip unless designs live in Figma; output is web-biased |

## ECG / biosignal Python libraries

| Library | Licence | Notes |
| --- | --- | --- |
| [wfdb](https://pypi.org/project/wfdb/) | MIT | PhysioNet record I/O |
| [neurokit2](https://pypi.org/project/neurokit2/) | MIT | Cleaning, R-peaks, delineation, HRV |
| [ecg-image-kit](https://github.com/alphanumericslab/ecg-image-kit) | BSD-3-Clause | Synthetic paper-ECG images from signals |
| [torch_ecg](https://github.com/DeepPSP/torch_ecg) | MIT | PyTorch ECG models and utilities |
| [ecglib](https://pypi.org/project/ecglib/) | Apache-2.0 | Pretrained models — check weight/data licences |
| [Ahus-AIM/Open-ECG-Digitizer](https://github.com/Ahus-AIM/Open-ECG-Digitizer) | **CC BY-SA 4.0** (code and weights) | **Caution** — share-alike; best published phone-photo results |
| Ultralytics YOLO | **AGPL-3.0** / Enterprise | **Caution** — avoid in products handed to third parties |

## Flutter packages (as reviewed 2026-10)

Prefer: `riverpod`, `drift`, `flutter_localizations` + `intl` (Kyrgyz `ky` is supported by
Material localisations), `flutter_litert` (LiteRT runtime, Apache-2.0),
`google_mlkit_document_scanner` (Android, beta) or `cunning_document_scanner`, `pdf` +
`printing`, `CustomPainter` for dense signal plots. Avoid for new work: `isar`, original
`hive` (stale), `tflite_flutter` (marked work-in-progress), Syncfusion charts (community
licence limits).

## Security notes

Skills and MCP servers can execute code and steer an agent; recent audits found
malicious or flawed skills in public marketplaces. Pin every source to a commit, read the
`SKILL.md` and scripts before enabling, give MCP servers least privilege, and never give
an agent patient data or secrets. See [security](security.md).
