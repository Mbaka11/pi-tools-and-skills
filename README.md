# Pi Tools & Skills

[![Version](https://img.shields.io/badge/version-0.1.0-blue)](https://github.com/Mbaka11/pi-tools-and-skills/releases/latest)
[![Checks](https://github.com/Mbaka11/pi-tools-and-skills/actions/workflows/check.yml/badge.svg)](https://github.com/Mbaka11/pi-tools-and-skills/actions/workflows/check.yml)

A personal, cross-project collection of reusable [pi](https://github.com/earendil-works/pi) skills, small offline helpers, and pinned reverse-engineering tool references.

**Six skills · No automatic tool installation · No credentials or project data**

This is a toolbox, not an ApplyPilot dependency and not a backup of an entire pi
profile. It contains reusable instructions and helpers, not browser sessions,
model authentication, private captures, or previous project deliverables.

## Included skills

| Skill | Use | Origin |
| --- | --- | --- |
| `ae-production-workflow` | Reversible After Effects production, checkpoints, RAM gates, native QA, delivery verification | Existing personal skill, with its scripts and templates |
| `market-research` | Sourced market sizing, competition, regulations, and opportunity comparisons | Generalized from personal Cowgorithm research skill |
| `research-reporting` | Briefs, executive summaries, full reports, and reviewed PDF exports | Generalized from personal Cowgorithm report skill |
| `backlog-execution` | Bounded on-demand task execution and evidence-based completion | Generalized from personal Cowgorithm task reference |
| `rea-investigation` | Authorized artifact and passive runtime investigation using REA | Personal adapter + unchanged matching upstream skill snapshot |
| `reverse-api-investigation` | Reviewed network evidence → endpoint map → testable client, without embedded secrets | pi-native workflow inspired by Reverse API Engineer |

Original sources and exact revisions: [SOURCES.md](SOURCES.md).
Other installed third-party skills are listed in [the external catalog](docs/external-skills.md), not copied or presented as personal creations.

## Recover on another machine

Requires pi and Git. For an immutable version:

```bash
pi install git:github.com/Mbaka11/pi-tools-and-skills@v0.1.0
```

Restart pi or run `/reload`. Skills are registered at **user scope**, so they are
available across projects. Dependencies such as REA, After Effects, Python,
FFmpeg, or browser tooling are **not** installed or activated by this command.

Alternatively, clone an editable copy:

```bash
git clone https://github.com/Mbaka11/pi-tools-and-skills.git
cd pi-tools-and-skills
npm test
pi install .
```

`npm test` requires Node.js 22.19+ and Python 3.9+; it installs nothing. Node 24 LTS
is recommended. Windows-specific checkpoint tests also use PowerShell. There are
no npm dependencies and no package install hooks.

If `ae-production-workflow` already exists as a standalone personal skill, review
which copy should stay enabled with `pi config`. Disable the old resource before
loading the package copy; do not keep two skills with the same name active.
Keep a backup outside pi's scanned skill directories before any migration.

This repository's creation does not modify any current pi installation.

## Use a skill

Ask pi normally, or select a workflow explicitly:

```text
/skill:market-research Compare the market for this product in the agreed region.
/skill:research-reporting Create an executive summary from these reviewed findings.
/skill:backlog-execution Complete the three authorized tasks in this project plan.
/skill:rea-investigation Explain this owned Electron package's import flow.
/skill:reverse-api-investigation Map the API from this reviewed test capture.
/skill:ae-production-workflow Preflight the current AE project without changing it.
```

Skills are instructions, not access grants. Unavailable host tools and engines
remain unavailable. Targets, live actions, credentials, and output directories
must be established for each project.

## Reverse-engineering tools

### REA — optional CLI / MCP

[REA by morluto](https://github.com/morluto/rea) is pinned to **6.4.0**.
The matching original skill and its six references are included under `vendor/`;
the actual engine is not bundled. Read [setup and limitations](tools/rea/README.md)
before installing or connecting it. A disabled, credential-free MCP example is
provided; no user MCP configuration is replaced automatically.

### Reverse API Engineer — reviewed reference

[Reverse API Engineer by kalil0321](https://github.com/kalil0321/reverse-api-engineer)
is recorded at **0.14.0**. Its autonomous CLI is **not installed or run**. That
version's prompts explicitly instruct generated clients to hardcode captured
credentials, cookies, and tokens. Our [adapted workflow](skills/reverse-api-investigation/SKILL.md)
deliberately does not follow that policy and instead uses pi's existing tools and
model. See [the evaluation](tools/reverse-api-engineer/README.md).

Both repositories can be retrieved as exact, separate source checkouts:

```bash
# Print plans only; no downloads or configuration changes.
node scripts/fetch-source.mjs rea
node scripts/fetch-source.mjs reverse-api-engineer

# Explicit opt-in downloads into ignored .local/upstreams/; no dependency installs.
node scripts/fetch-source.mjs rea --fetch
node scripts/fetch-source.mjs reverse-api-engineer --fetch
```

The published repo contains the reusable integrations, pins, and selected upstream
references—not two full forks. Source checkout is optional; GitHub and npm must
remain reachable to retrieve external sources or engines.

## Privacy and safety

- Keep raw HARs, browser profiles, secrets, and analysis outputs in the relevant
  project's ignored private directory, never this repository.
- The HAR helper outputs only structural counts and opaque identifiers by
  default. Literal route previews require an explicit flag and human review.
- No cookie export, credential harvesting, CAPTCHA bypass, account automation,
  submission, or external messaging is authorized by installing a skill.
- Use official APIs where available. Technical access to a service is not
  permission to automate it or bypass its commercial/access conditions.
- Local tools can produce evidence that reaches pi's model provider. This is not
  an offline-AI guarantee or a promise of free model usage.
- Skills and these checks are not a sandbox or a complete secret scanner.

More: [privacy and execution boundaries](docs/security.md).

## Updates and maintenance

```bash
npm test
npm run updates:check
```

The update check only reads public release metadata. It never pulls, installs,
changes pins, or rewrites skills. No scheduled task is created. Run it periodically
or before an investigation; review changes and tests before a deliberate update.

Pins, source commits, npm archive integrity, and vendored file hashes live in
[tools/upstreams.lock.json](tools/upstreams.lock.json). Keep REA's engine and skill
snapshot aligned. Git tags are immutable; restoring a pinned version does not
silently upgrade it. See [the update/rollback procedure](docs/maintenance.md) and
[the changelog](CHANGELOG.md).

## Rights

**No license is granted for the original personal skills and helpers at this time.**
A public GitHub repository is not by itself an open-source license. See
[RIGHTS.md](RIGHTS.md). The npm `private` flag prevents accidental npm publication;
it does not make this GitHub repository private.

Third-party material retains its existing MIT license and attribution. See
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
