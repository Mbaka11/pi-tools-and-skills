---
name: rea-investigation
description: Investigate authorized binaries, packaged JavaScript or Electron apps, and passive runtime or saved network evidence using pinned REA tools. Use for reverse engineering, not ordinary source-code review or general browser automation.
compatibility: REA 6.4.0 is optional and must be installed or connected separately. Node.js must satisfy REA's engine range; native engines and platform support vary by target.
metadata:
  version: "1.0.0"
  upstream: "https://github.com/morluto/rea"
  upstream-version: "6.4.0"
---

# REA Investigation

[Tiny example — illustrative import-flow report, REA not executed](../../examples/README.md#rea-investigation).

This is a personal integration guide, not a replacement engine or a promise of
support for every target. The original MIT-licensed REA skill and references are
preserved unchanged in [the versioned snapshot](../../vendor/rea/skills/reverse-engineer-anything/SKILL.md).

## Scope and privacy first

- Establish the exact target, question, and authorized actions. Ask if ownership
  or authorization for runtime access is unclear. Source-code analysis alone
  normally needs standard repository tools, not REA.
- Prefer static or already-recorded evidence. Do not launch a binary, attach to a
  browser, enable remote debugging, record traffic, or broaden access implicitly.
- Never export session cookies or credentials. Do not bypass access controls,
  CAPTCHA, login requirements, paid access, or service limits.
- Do not connect to an unrelated browser profile or navigate an existing user
  form. Browser observation is not permission to automate the site's account.
- Store evidence under the current project's ignored private directory, not in
  this shared toolbox. Tool results may reach pi's configured model provider;
  local analysis is not a guarantee of offline processing.
- REA's exclusions are not a complete secret scrub: URLs, source code, screenshots,
  and visible text may contain sensitive values. For sensitive targets, prefer
  local CLI output and reviewed minimal excerpts rather than returning raw
  evidence to the model. Establish that boundary before collecting evidence.
- Delegation still requires user or applicable project authorization; upstream
  guidance about parallel workers does not itself grant it.

## Resolve the tool

Read [REA setup](../../tools/rea/README.md) only if the tool is absent or its
version is unknown. Use the pinned `rea-agents@6.4.0`; never silently substitute
`@latest` or upgrade the installed CLI. Check the actual connected server's
schemas rather than assuming every upstream-main feature is available.

A package install loads these instructions only. It does not register MCP,
install REA, or install Ghidra, Hopper, IDA, Java, or a browser. Show a setup plan
and obtain authorization before changing global tool configuration. Preserve
unrelated MCP servers and skills. Prefer scoped CLI use when persistent MCP is
unnecessary.

## Investigation

1. Read the bundled upstream skill linked above, then only its relevant reference.
   Keep this guide's pinning and authorization boundaries in force.
2. Record target digest, tool version, and analysis scope. Distinguish the runtime
   engine's version from this skill's version.
3. Choose the smallest appropriate static/recorded analysis. Use summary-first
   evidence and page large results instead of repeating the same analysis.
4. Follow evidence-backed hypotheses. Corroborate static inferences with runtime
   observations only if needed and explicitly in scope.
5. Preserve evidence IDs and limitations. "Not found in this search" is not proof
   of absence. Decompiled code is not the original source.
6. If constructing an implementation, separate observed behavior from design
   choices and test it with synthetic fixtures before any live replay.
7. Close only the sessions/processes owned by this investigation. Never close or
   restart an unrelated application to resolve a tool issue.

Report findings, sources, verified behavior, unknowns, and remaining risks.
For API reconstruction, also use [reverse-api-investigation](../reverse-api-investigation/SKILL.md).
