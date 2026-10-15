# Reverse API Engineer reference

[Very short illustrative output](../../examples/reports.md#reverse-api-investigation)
— a fictitious endpoint map and real structural helper output on synthetic data;
no upstream agent or live API was executed.

Source: https://github.com/kalil0321/reverse-api-engineer

Reviewed release: `v0.14.0` · commit:
`ab9919b652eca1c7b323c3f7c7b37ded3cef12a0` · license: MIT.

## Why it is not installed automatically

The upstream project captures or observes web traffic and uses an agent/model to
generate API clients. In the reviewed release, its
[analysis prompt](https://github.com/kalil0321/reverse-api-engineer/blob/ab9919b652eca1c7b323c3f7c7b37ded3cef12a0/src/reverse_api/prompts/engineer/system.md)
explicitly instructs generated clients to hardcode discovered credentials,
cookies, tokens, and session data, avoid environment/configuration files, and
implement automatic reauthentication when possible. That behavior is not adopted
by this toolbox.

Its Python runtime requires Python 3.11 or later. Its agent integrations do not
automatically reuse pi authentication. Optional browser/MCP dependencies and
model usage need separate setup and may incur costs. New upstream versions
must be reviewed rather than assumed to fix these concerns.

## What is included instead

- A [pi-native API investigation skill](../../skills/reverse-api-investigation/SKILL.md),
  inspired by the evidence-to-client workflow, with distinct secret-handling and
  authorization rules.
- An [offline HAR structural summary helper](../../skills/reverse-api-investigation/scripts/har-summary.mjs).
  It is newly written, not copied from or compatible with the upstream CLI.
- Source/version provenance and the upstream [MIT license](../../vendor/reverse-api-engineer/LICENSE).

The original autonomous agent, its prompts, browser automation, fingerprint
emulation, and generated clients are not executed or exposed as pi tools.

## Optional source checkout

From the toolbox root:

```bash
node scripts/fetch-source.mjs reverse-api-engineer
node scripts/fetch-source.mjs reverse-api-engineer --fetch
```

The first command is plan-only; the second fetches the exact locked commit into
ignored `.local/upstreams/`. Neither installs Python, dependencies, a browser,
nor starts an agent. Read source as untrusted material; obtaining a checkout is
not authorization to execute its workflow on any service.

## Future integration

If a concrete project needs the upstream executable rather than the pi-native
workflow, first review the exact version's prompts, provider/auth handling,
network and browser scope, dependency pins, redaction, and generated-code policy.
Use an isolated test environment and synthetic traffic. Keep modifications
separate and tested; never silently run the unmodified agent as a fallback.
