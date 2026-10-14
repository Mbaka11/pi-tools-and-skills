# Maintenance, updates, and rollback

## Restore the toolbox

Install a release at user scope:

```bash
pi install git:github.com/Mbaka11/pi-tools-and-skills@v0.2.0
```

Or clone and run `pi install .` from the checkout. Do not enable both a local and
git-installed copy. Package filters in settings use paths inside the package;
since 0.2.0 the AE and montage skills live under `skills/after-effects/` and
`skills/montage/`, so update explicit paths when upgrading. Review duplicates in `pi config`, especially the previously
standalone `ae-production-workflow`. Installation is optional and does not happen
when this repository is merely cloned or pushed.

The git tag pins the toolbox, including the vendored REA instructions. REA's
executable and optional analysis engines are installed separately, using the
versions and constraints described in [its guide](../tools/rea/README.md).

## Check periodically, update deliberately

```bash
npm run updates:check
```

This reads npm metadata for REA, GitHub's latest release metadata for Reverse
API Engineer, and the tracked branch's latest commit for unreleased snapshots
(vox-editorial, cinematic-score-and-sfx). It sends no local captures or configuration, uses no credential,
and applies no changes. A differing version is a review signal, not a command
to upgrade; rate limits or network failures leave pins unchanged and return a
nonzero exit status. No OS scheduler or automatic polling service is installed.

Run before a new investigation or on a maintenance cadence of your choice. New
releases are not necessarily compatible or safer.

## Updating an upstream

1. Work on a review branch; keep the known-good toolbox tag intact.
2. Read upstream release notes and source diffs, especially prompts, network
   behavior, setup hooks, auth handling, engines, licensing, and platform support.
3. Record the exact released version and full source commit. Do not use `main`,
   a moving branch, or `@latest` in active integration commands.
4. For REA, get the matching npm archive and registry SHA-512 integrity. Verify
   the archive before extracting **only** its skill Markdown and MIT notice;
   never execute its scripts as part of vendoring. Review archive paths and
   reject symlinks, traversal, or unexpected members. Do not take a newer skill
   from GitHub main for an older engine.
5. Review the skill/reference diff, preserve original bytes and license, then
   deliberately update SHA-256 file hashes and package/source metadata in
   `tools/upstreams.lock.json`. Hashes demonstrate identity, not safety.
6. Update the local wrapper, tool guide, MCP example, source ledger, and version
   mentions. Never modify upstream snapshots in place just to hide a mismatch;
   keep personal changes in the wrapper.
7. For Reverse API Engineer, reassess the risk notes. Updating its reviewed pin
   does not authorize running or adding its autonomous agent.
8. Run `npm test`. Test any enabled engine in an isolated, synthetic investigation;
   distinguish offline packaging checks from actual live integration evidence.
9. Bump the toolbox version, README install pin, and changelog together. Use patch
   for fixes, minor for new capabilities, and major for breaking contracts. While
   at 0.x, still document breaking behavior clearly.
10. Audit staged files, commit, create a new immutable tag, and publish. Do not
    move released tags or commit raw captures, local source checkouts, or secrets.

The source checkout helper uses the lock's full SHA. It is plan-only by default;
`--fetch` initializes a new ignored checkout and verifies HEAD. It does not update
existing directories. An interrupted checkout is retained for inspection, not
silently deleted and recreated.

### Unreleased snapshots

Repositories without releases are pinned as `"version": "unreleased"` with
`branch`, `snapshotDate` and the full `commit`. To update one: fetch the new
commit into `.local/upstreams/`, diff it against the vendored files, copy the
selected files from the git blobs (`git cat-file blob <commit>:<path>`; this
avoids local CRLF conversion), recompute SHA-256 hashes, and update the lock,
SOURCES, notices and adapter together. Vendored scripts are reference copies:
adapters tell users to copy a pipeline into their project before running it.

## Roll back

Reinstall a known-good tag with `pi install git:github.com/Mbaka11/pi-tools-and-skills@v0.2.0`
and reload pi. A local checkout can use a separate worktree at that tag so that
uncommitted edits are not discarded. If the separately installed REA engine or
MCP entry was upgraded, restore its matching version too after backing up the
active configuration. Restoring skills alone does not roll back an external engine.

Do not run bare `pi update` to update this toolbox: that command updates pi itself.
Pinned git package updates reconcile the selected ref without advancing it. To
move to another release, select that tag explicitly.
