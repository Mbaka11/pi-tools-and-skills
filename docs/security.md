# Privacy and execution boundaries

## This is not a profile backup

Never commit pi settings/authentication, MCP secrets, model credentials, browser
profiles, network captures, generated clients containing secrets, application
records, customer files, or production media. Do not export all of `~/.pi/agent`
to restore a few skills. The Git ignore rules are a precaution, not a data-loss
prevention system: review `git diff --cached` before every push.

Use the target project's ignored private directory for evidence and generated
outputs. The toolbox's `.local/` is only for local maintenance/checkouts/tests.
If a project does not ignore its private evidence directory, establish that
exclusion before writing a capture there. File names and paths can themselves
contain personal or business-sensitive information.

## HAR handling

A HAR can contain request/response bodies, Authorization headers, cookies,
passwords, search queries, and identity data. Redacting obvious header names is
not sufficient. Do not send a raw capture to a model just because analysis is
initiated locally.

The bundled helper is offline and allowlist-based:

- Default output: opaque host/endpoint IDs, known HTTP methods, status counts,
  path depth, query count, known MIME categories, and a source digest.
- Default output contains no literal URLs, headers, cookie values, request or
  response bodies, query names/values, timestamps, titles, or input path.
- `--include-routes` adds only literal origin/path, **which can still contain
  secrets and personal identifiers**. It is a review preview, not sanitized data.
- Unknown HAR extension fields are dropped. Malformed URLs and userinfo-bearing
  URLs are skipped. No recorded URL is requested or replayed.
- Input is limited to 25 MiB and 50000 entries; existing output files are refused.
- Originals are not modified. A digest and derived usage statistics may still
  be sensitive; review all outputs for the intended recipient.

This minimizer does not replace a comprehensive redaction process. It deliberately
omits most details needed for full API inference. Add a separately reviewed,
minimal route/schema excerpt only when necessary and authorized.

## Tool acquisition and live access

Installing the pi skills does not install analysis engines or authorize runtime
access. Optional source retrieval is separate from installation and execution.
Review external code and dependencies before running them. A source checkout is
not a sandbox; Git's ordinary local configuration and checkout behavior still
apply. The retrieval helper does not run repository scripts or dependency
installers and refuses to overwrite an existing destination.

Before live work, establish target identity, authorization, data boundaries,
read/write scope, output location, cancellation, and cleanup. Use owned test
services and fixtures where possible. Do not extract cookies from an existing
session, bypass security challenges or service limits, or infer authorization
from a user's successful login. Do not modify or close unrelated browser tabs.

pi and external programs retain the operating-system permissions of their user.
A skill, project-trust decision, or prompt instruction is not a security sandbox.
Use an isolated environment for untrusted artifacts. No new scheduled tasks,
background agents, telemetry services, or auto-updaters are configured here.

## Synthetic gallery exception

`examples/` contains purpose-built fixtures and original media, never client
assets or saved browser evidence. The only permitted committed media are exact
paths declared in `examples/manifest.json`, with provenance, a size limit and
SHA-256. GIF/PNG/MP4/WAV signatures are checked; each file is limited to 1 MiB,
the collection to 8 MiB, and animated/audio examples to four seconds. Tests
fully decode animations/audio when FFmpeg is present; the separate mandatory
media CI fails when its declared prerequisites are absent. This narrow exception is
not permission to add other project media. Review paths and generated reports
before publication. A digest proves byte identity, not copyright or privacy.

Mockups and illustrative reports must be labelled as such: they are not proof
of native Adobe execution, a tested external pipeline or a live investigation.
No external media was copied into this gallery. The dialogue test uses generated
tone/noise, not a voice recording; no enhancement provider receives audio. The
sync calculator only maps user-supplied anchors and never reads or changes media.
Full client ffprobe reports, camera metadata, proxy maps and transcripts belong
in private projects, even when the tools that create them run locally.

`proxy_audit.py` only reads inputs; its optional report uses exclusive creation.
JSON mode handles supplied metadata and never opens media. Media mode invokes a
separately available ffprobe with a timeout and file-only protocol whitelist;
it is **not a decoder sandbox**. Isolate unfamiliar/malicious media. Raw input
paths, timecode/reel strings and arbitrary tags are not emitted; hashes and
numeric metadata can still be sensitive. A metadata-compatible verdict is not
proof of cadence, picture/audio identity, rights or native attachment.

The transcript example is fictional, and caption labels were authored rather
than transcribed or human-auditioned. Archive copying uses a new destination and
never deletes originals. Collection/trim/transcode, provider uploads, paid ASR,
font/plugin redistribution and source deletion still require deliberate scope
and authorization. Checksums do not discover missing dependencies or prove that
an NLE project opens.

## Publishing

Run tests and inspect both staged names and contents. Confirm no evidence,
credentials, personal absolute paths, or client data are included. Preserve
third-party notices. If a secret is ever exposed, revoke/rotate it; deleting the
current file does not remove it from Git history or copies already obtained.
