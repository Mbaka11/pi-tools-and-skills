---
name: reverse-api-investigation
description: Reconstruct an authorized web API from documentation and carefully reviewed network evidence, then design and test a client without hardcoded secrets. Use for API interoperability, endpoint mapping, and HAR-based investigation across projects.
compatibility: Uses pi's existing tools and model. The optional offline HAR summary helper requires Node.js 22.19+; no external Python agent or browser is installed automatically.
metadata:
  version: "1.0.0"
  inspiration: "https://github.com/kalil0321/reverse-api-engineer"
  reviewed-upstream-version: "0.14.0"
---

# Reverse API Investigation

A pi-native workflow inspired by Reverse API Engineer's network-evidence-to-client
approach. **This is not its CLI, a fork, or a compatibility claim.** Its autonomous
agent is not run by this skill. See [upstream evaluation](../../tools/reverse-api-engineer/README.md).

## 1. Define authorization and the useful question

Identify the exact service and environment, desired read/write operations, user
permission, authentication boundary, and output language. Prefer official public
APIs and documentation when available. A logged-in session does not itself
permit automation or give permission to extract credentials.

Stop at CAPTCHA, access denial, paywalls, login challenges, or rate limits. Do
not implement stealth fingerprints, session-cookie export, automatic account
reauthentication, or alternate routes to bypass these controls.

## 2. Choose the least invasive evidence

Prefer published docs, an owned test service, a synthetic fixture, or an existing
explicitly supplied capture. Capture new traffic only with clear authorization
covering the target and storage. Never attach to a general-purpose browser or
export its sessions implicitly. Use a separate test profile when appropriate;
never navigate or reload the user's existing forms.

HAR files can contain passwords, cookies, tokens, personal data, and full response
bodies. Keep originals local to the project, outside Git. Do not send a raw HAR
to the model, attach it to an issue, or paste it into a report.

The offline helper emits **only structural counts and opaque identifiers** by
default:

```bash
node scripts/har-summary.mjs /absolute/path/to/private.har --out /absolute/path/to/new-summary.json
```

Resolve the script path relative to this skill directory. It reads one file,
does not fetch URLs, and refuses to overwrite an output. It is a minimizer, not
a general-purpose HAR sanitizer, and does not modify the original.

If useful and authorized, `--include-routes` additionally exposes literal hosts
and paths, but never queries, headers, cookies, or bodies. Hosts and paths can
still contain secrets or personal identifiers. Review that output locally
before sharing it with a model or another person. Default output intentionally
cannot reconstruct endpoint semantics; supply a reviewed route/schema excerpt
for deeper analysis.

## 3. Map the API

Create a local endpoint ledger with method, reviewed route template, request and
response schemas, pagination, status/error handling, evidence reference, and
confidence. Document authentication **mechanisms**, never captured values.

Compare multiple examples; one response does not establish optionality, allowed
values, or completeness. Mark inferred contracts and unresolved behavior.
Inspect relevant client code only within scope. Use the REA skill when packaged
code or more detailed offline evidence analysis is needed.

## 4. Build a testable client

- Pass credentials through an explicit caller-owned auth adapter or environment
  variable, never source literals, fixtures, logs, command arguments, or Git.
- Do not implement password collection, session-cookie reuse, or token refresh
  inferred from a captured login. Use a documented authorized auth flow only
  when requested, keeping secret handling outside the generated example.
- Restrict the destination to the intended service; do not replay arbitrary URLs
  or follow credential-bearing redirects across hosts.
- Set deadlines, response-size limits, bounded pagination, and cancellation.
- Handle 401/403 as an auth/access boundary; respect 429/Retry-After and stop or
  ask before retrying. No unlimited retries or silent escalation of access.
- Read-only smoke tests first. Writes, purchases, messages, submissions, and
  account changes require separate authorization for their real-world effect.

## 5. Verify and deliver

Use synthetic tests for pagination, schema changes, malformed data, authentication
failures, cancellation, timeout, and rate limiting. Live validation is separate
and must be explicitly in scope. Do not claim a tested live connector based only
on a generated script or mocked test.

Deliver client code, setup with placeholder secrets, an endpoint map, evidence
and test results, limitations, and refresh instructions. Keep raw captures and
credentials private to the project. Use pi's current model without launching
another autonomous agent; provider usage and costs still apply.
