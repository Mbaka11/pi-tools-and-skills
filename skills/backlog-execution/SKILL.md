---
name: backlog-execution
description: Execute a user-authorized set of project backlog tasks with visible progress, evidence-based completion, and explicit stop conditions. Use when asked to work through an existing plan, not to create unsolicited recurring work.
metadata:
  version: "1.0.0"
  origin: "Adapted from Mbaka11/Cowgorithm skills/cron-tasks"
---

# Backlog Execution

## Bound the work

Read the project's instructions and authoritative backlog. Establish which tasks,
phase, or milestone the user authorized, relevant dependencies, completion
criteria, and any time/resource budget. The presence of unfinished tasks is not
permission to execute all of them.

Do not start cron jobs, a recurring schedule, a long-running agent loop, or
subagents unless the user or applicable instructions authorize that mechanism.
The original skill's directory name did not mean that cron scheduling was enabled.

## Work loop

1. Select the next authorized, unblocked task whose prerequisites are satisfied.
2. Mark it in progress using the existing project tracker or available todo tool.
3. Read relevant sources; perform the bounded research or implementation.
4. Validate the real deliverable against the task's criteria.
5. Update the backlog and relevant source/test ledger with evidence and paths.
6. Report meaningful progress; continue only within the authorized scope.
7. Stop when done, blocked, cancelled, or when a material decision is needed.

Preserve unrelated edits and unsaved user work. A missing report does not prove
an operation made no changes: inspect actual state before retrying.

## Completion criteria

- Required output exists and is substantive, not a skeleton.
- Important factual claims have sources; estimates and assumptions are labeled.
- Code changes have appropriate validation, with failures and untested behavior
  stated explicitly.
- The tracker reflects what was actually completed.
- Follow-ups and unresolved questions are visible, not silently treated as done.

## Decision boundaries

Ask before making a consequential business/architecture choice not already
settled, changing scope, discarding user work, spending money, publishing private
data, or triggering an external action not covered by the request. Do not add
repeated approval gates for already-authorized routine steps.

Use available decision tools if supported, otherwise ask in the conversation.
Never invent answers to eligibility, signature, credential, legal, or financial
questions to keep the loop moving.

## Reporting

Conclude with completed tasks, changed paths, verification performed, and remaining
blockers. Draft external notifications but do not send without authorization.
Keep project artifacts in the project; the global skill is a workflow, not a
shared store for private results.

## Provenance

Generalized from [Cowgorithm's on-demand task reference](https://github.com/Mbaka11/Cowgorithm/blob/c3ccfce39969a9bab8a181c387c137b365457c6c/skills/cron-tasks/SKILL.md).
No domain-specific opportunity backlog, thresholds, or communication destination
is embedded here.
