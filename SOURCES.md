# Sources and provenance

## Personal skills

| Included path | Original source | Changes |
| --- | --- | --- |
| `skills/ae-production-workflow/` | Existing personal `ae-production-workflow` skill, version 1.0.0 | Included all six files; replaced a project-specific example prefix with `<PROJECT>`; skill version 1.0.1. Helper scripts unchanged. |
| `skills/market-research/` | [Cowgorithm research](https://github.com/Mbaka11/Cowgorithm/blob/c3ccfce39969a9bab8a181c387c137b365457c6c/skills/research/SKILL.md) | Added pi metadata; removed fixed geography, currency, hardware assumptions, and decision thresholds. |
| `skills/research-reporting/` | [Cowgorithm report-gen](https://github.com/Mbaka11/Cowgorithm/blob/c3ccfce39969a9bab8a181c387c137b365457c6c/skills/report-gen/SKILL.md) | Added pi metadata; generalized folders/audiences; no automatic message sending or scheduling. |
| `skills/backlog-execution/` | [Cowgorithm cron-tasks](https://github.com/Mbaka11/Cowgorithm/blob/c3ccfce39969a9bab8a181c387c137b365457c6c/skills/cron-tasks/SKILL.md) | Added pi metadata; clarified bounded on-demand scope; removed domain-specific backlog and messaging assumptions. |

The original personal skill and Cowgorithm files are not changed by this import.
The collection is not an exhaustive backup of every agent package or historic
session; it includes the personal skills found in the inspected local locations.

## Reverse-engineering sources

### REA

- Repository: https://github.com/morluto/rea
- Pinned npm version: `6.4.0`.
- Source commit: `a56f7bb668ab23fec8d33f7af353ac7ed2fe1895`.
- Package: https://registry.npmjs.org/rea-agents/-/rea-agents-6.4.0.tgz
- `vendor/rea/` contains only the release's original skill, six references, and
  MIT license. The published npm skill has metadata version **37**; it is not the
  newer main-branch skill observed during initial research.
- The archive's SHA-512 integrity was verified before extraction. Each included
  file has a SHA-256 in [tools/upstreams.lock.json](tools/upstreams.lock.json).
- `skills/rea-investigation/` is our separate pinning/privacy integration layer.

### Reverse API Engineer

- Repository: https://github.com/kalil0321/reverse-api-engineer
- Pinned reviewed release: `v0.14.0`.
- Commit: `ab9919b652eca1c7b323c3f7c7b37ded3cef12a0`.
- Inspiration: observe authorized traffic, infer the API contract, generate and
  verify a client. The upstream secret-hardcoding and reauthentication policy is
  expressly excluded. See [the review](tools/reverse-api-engineer/README.md).
- `skills/reverse-api-investigation/` and its helper are newly written, not an
  upstream code copy or an installed Python agent.

Full source checkouts remain optional, separate, ignored, and pinned. Version
checking is read-only. See [maintenance](docs/maintenance.md).
