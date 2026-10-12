import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, writeFile, readFile, rm, symlink } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { validate, frontmatter } from '../scripts/check.mjs';
import { readLock, rejectSymlinks, ROOT, LOCK_PATH } from '../scripts/upstreams.mjs';
import { latestVersions } from '../scripts/check-updates.mjs';
import { sourcePlan } from '../scripts/fetch-source.mjs';

test('package, all six skills, local links, rights and vendored digests validate', async () => {
  const report = await validate();
  assert.deepEqual(report.errors, []);
  assert.equal(report.ok, true);
  assert.equal(report.skills.length, 6);
});

test('frontmatter rejects missing descriptions and malformed names', () => {
  assert.throws(() => frontmatter('# Not a skill'));
  assert.throws(() => frontmatter('---\nname: bad--name\ndescription: Useful\n---\n'));
  assert.throws(() => frontmatter('---\nname: valid\n---\n'));
  assert.equal(frontmatter('---\nname: good\ndescription: "Useful task"\n---\n').description, 'Useful task');
});

test('release check compares metadata without sending auth or changing pins', async () => {
  const before = await readFile(LOCK_PATH, 'utf8');
  const seen = [];
  const reports = await latestVersions(await readLock(), async (url, options) => {
    seen.push({ url, options });
    return { ok: true, json: async () => url.includes('registry.npmjs.org') ? { version: '6.5.0' } : { tag_name: 'v0.14.0' } };
  });
  assert.equal(reports[0].differs, true);
  assert.equal(reports[0].action, 'review-before-changing-pins');
  assert.equal(reports[1].differs, false);
  assert.equal(seen.length, 2);
  for (const { options } of seen) {
    assert.equal(options.headers.Authorization, undefined);
    assert.equal(options.redirect, 'error');
    assert.ok(options.signal instanceof AbortSignal);
  }
  assert.equal(await readFile(LOCK_PATH, 'utf8'), before);
});

test('rate limits, bad metadata and offline failures are reported without remote-body leakage', async () => {
  const lock = await readLock();
  for (const fetcher of [async () => ({ ok: false, status: 429 }), async () => ({ ok: true, json: async () => ({ version: 'bad-secret-value' }) }), async () => { throw new Error('network-secret-value'); }]) {
    const report = await latestVersions(lock, fetcher);
    assert.ok(report.every(item => item.error));
    assert.ok(!JSON.stringify(report).includes('secret-value'));
  }
});

test('source plans name exact commits and never imply activation', async () => {
  const lock = await readLock();
  for (const name of Object.keys(lock.upstreams)) {
    const plan = sourcePlan(lock, name);
    assert.match(plan.commit, /^[a-f0-9]{40}$/);
    assert.ok(plan.destination.startsWith('.local/upstreams/'));
    assert.equal(plan.installsDependencies, false);
    assert.equal(plan.executesUpstreamPrograms, false);
  }
  assert.throws(() => sourcePlan(lock, '../escape'));
  assert.throws(() => sourcePlan(lock, '__proto__'));
});

test('fetch CLI is plan-only by default and rejects unknown options', () => {
  const script = path.join(ROOT, 'scripts/fetch-source.mjs');
  const result = spawnSync(process.execPath, [script, 'rea'], { encoding: 'utf8', timeout: 5000 });
  assert.equal(result.status, 0, result.stderr);
  assert.equal(JSON.parse(result.stdout).mode, 'plan-only');
  const invalid = spawnSync(process.execPath, [script, 'rea', '--force'], { encoding: 'utf8', timeout: 5000 });
  assert.equal(invalid.status, 1);
});

test('relative file guards reject traversal and symlink escapes', async t => {
  const dir = await mkdtemp(path.join(tmpdir(), 'pi-toolbox-path-'));
  t.after(() => rm(dir, { recursive: true, force: true }));
  for (const rel of ['../outside', '/absolute', 'a/../b', 'a//b', 'C:/absolute', 'a\\b']) await assert.rejects(rejectSymlinks(dir, rel));
  await writeFile(path.join(dir, 'real.txt'), 'fixture');
  assert.equal(await rejectSymlinks(dir, 'real.txt'), path.join(dir, 'real.txt'));
  try { await symlink(dir, path.join(dir, 'linked'), process.platform === 'win32' ? 'junction' : 'dir'); }
  catch (error) { if (error.code === 'EPERM') return t.skip('Symlink creation unavailable.'); throw error; }
  await assert.rejects(rejectSymlinks(dir, 'linked/escape'));
});
