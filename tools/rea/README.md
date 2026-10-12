# REA integration

Source: https://github.com/morluto/rea

Pinned package: `rea-agents@6.4.0` · source commit:
`a56f7bb668ab23fec8d33f7af353ac7ed2fe1895`.

The original skill and references in [vendor/rea](../../vendor/rea/skills/reverse-engineer-anything/SKILL.md)
were extracted from the verified npm release archive, not copied from a newer
`main`. Archive integrity and file digests are recorded in [the lock](../upstreams.lock.json).
The local wrapper is [rea-investigation](../../skills/rea-investigation/SKILL.md).

## Optional installation

Installing this pi package only registers the curated skills. To run REA after
review and explicit tool-install authorization, choose either scoped execution
or a separately installed exact version:

```bash
npx -y rea-agents@6.4.0 analyze-javascript-application /absolute/path/to/owned-app --json
# Or, as an explicit separate global installation:
npm install --global rea-agents@6.4.0
```

These commands download and run third-party code. The initial toolbox setup does
not execute them. REA dependencies are managed by its package; this repository's
pin is not a lock of its entire transitive installation environment.

REA requires Node `^22.19.0 || ^24.11.0 || >=26.0.0`. Optional native engines have
separate operating-system, installation, authorization, and license requirements.
Windows support is not identical to Linux/macOS; consult the pinned release's
platform documentation. Do not install every engine merely to satisfy a broad
readiness report.

## Optional MCP connection

[mcp.example.json](mcp.example.json) contains an intentionally disabled server.
Merge only the `rea` entry into the **active MCP configuration**, after review.
Do not replace the whole file or copy private server entries into this repo.
Enable it only when wanted, then reload/reconnect pi and inspect actual schemas.

Alternatively, REA provides an explicit setup plan:

```bash
npx -y rea-agents@6.4.0 setup --client pi --dry-run --json
```

That plan may install another copy of the original skill and edit global MCP
configuration. Review duplicate skill names, destinations, and backups before
applying it; this repository does not apply the plan automatically.

pi's built-in MCP normally uses `~/.pi/agent/mcp.json`. An installed
`pi-mcp-adapter` replaces built-in session MCP and has its own configuration
precedence (including compatibility imports). Inspect the active configuration
rather than assuming a successful built-in `pi mcp list` proves the adapter is
using that entry. Do not disable unrelated MCP integrations.

## Capabilities and limits

- Static packaged JavaScript/Electron analysis, native/managed artifact workflows,
  and selected offline capture analysis, depending on available engines.
- Passive browser observations are not general browser automation or permission
  to access an account. No browser attachment is configured here.
- REA performs local analysis; returned evidence may reach pi's provider.
- Tool availability comes from the connected release, not the latest website.
- This release of the toolbox verifies packaging and offline helpers. It does
  not claim a live REA/browser or native-engine integration test.

Source-only retrieval is available through `node scripts/fetch-source.mjs rea --fetch`
from the toolbox root. That does not build or install the engine.
