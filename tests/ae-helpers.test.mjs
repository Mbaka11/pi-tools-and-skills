import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, writeFile, readFile, rm, readdir } from 'node:fs/promises';
import path from 'node:path';
import { tmpdir } from 'node:os';
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { ROOT } from '../scripts/upstreams.mjs';

const verifier = path.join(ROOT, 'skills/after-effects/ae-production-workflow/scripts/verify-delivery-manifest.py');
const checkpoint = path.join(ROOT, 'skills/after-effects/ae-production-workflow/scripts/checkpoint-aep.ps1');
const ram = path.join(ROOT, 'skills/after-effects/ae-production-workflow/scripts/ram-snapshot.ps1');
const sha = data => createHash('sha256').update(data).digest('hex');
async function fixture(t) {
  const dir = await mkdtemp(path.join(tmpdir(), 'pi-toolbox-ae-'));
  t.after(() => rm(dir, { recursive: true, force: true }));
  const bytes = Buffer.from('SYNTHETIC AEP BYTES - no Adobe process or project is opened');
  const project = path.join(dir, 'Fixture.aep');
  await writeFile(project, bytes);
  return { dir, project, bytes, manifest: { canonical: 'Fixture.aep', canonical_sha256: sha(bytes), files: [{ path: 'Fixture.aep', size: bytes.length, sha256: sha(bytes) }] } };
}
async function verify(dir, manifest) {
  const file = path.join(dir, 'manifest.json');
  await writeFile(file, JSON.stringify(manifest));
  const result = spawnSync(process.env.PYTHON || 'python', [verifier, file, '--root', dir], { encoding: 'utf8', timeout: 10000 });
  assert.ifError(result.error);
  return { result, report: JSON.parse(result.stdout) };
}
function ps(script, args, overrides = {}) {
  // Hosted CI starts npm from PowerShell 7. Windows PowerShell 5 must rebuild
  // its own module path rather than inherit incompatible pwsh module entries.
  const env = { ...process.env, ...overrides };
  for (const key of Object.keys(env)) if (key.toLowerCase() === 'psmodulepath') delete env[key];
  return spawnSync('powershell.exe', ['-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-File', script, ...args], { env, encoding: 'utf8', timeout: 20000 });
}

test('AE manifest verifier accepts exact canonical bytes without opening After Effects', async t => {
  const f = await fixture(t);
  const { result, report } = await verify(f.dir, f.manifest);
  assert.equal(result.status, 0, result.stderr);
  assert.equal(report.ok, true);
  assert.equal(report.canonicalOk, true);
  assert.equal(report.entriesChecked, 1);
});

test('AE manifest verifier rejects invalid root, missing fields, empty files and bool sizes', async t => {
  const f = await fixture(t);
  const cases = [null, [], {}, { ...f.manifest, files: [] }, { ...f.manifest, canonical_sha256: 'bad' }, { ...f.manifest, files: [{ ...f.manifest.files[0], size: true }] }];
  for (const manifest of cases) {
    const { result, report } = await verify(f.dir, manifest);
    assert.equal(result.status, 1);
    assert.equal(report.ok, false);
  }
});

test('AE manifest verifier rejects hash/size mismatch, missing canonical entry and duplicate paths', async t => {
  const f = await fixture(t);
  const cases = [
    { ...f.manifest, files: [{ ...f.manifest.files[0], size: 0 }] },
    { ...f.manifest, files: [{ ...f.manifest.files[0], sha256: '0'.repeat(64) }] },
    { ...f.manifest, files: [{ ...f.manifest.files[0], path: 'missing.aep' }] },
    { ...f.manifest, files: [f.manifest.files[0], f.manifest.files[0]] },
  ];
  for (const manifest of cases) {
    const { result, report } = await verify(f.dir, manifest);
    assert.equal(result.status, 1);
    assert.equal(report.ok, false);
  }
});

test('AE manifest verifier refuses out-of-root and absolute entries', async t => {
  const f = await fixture(t);
  for (const escaped of ['../outside.aep', f.project]) {
    const manifest = { ...f.manifest, files: [{ ...f.manifest.files[0], path: escaped }] };
    const { result, report } = await verify(f.dir, manifest);
    assert.equal(result.status, 1);
    assert.equal(report.ok, false);
  }
});

test('AE checkpoint refuses an unconfirmed save and leaves the source untouched', { skip: process.platform !== 'win32' }, async t => {
  const f = await fixture(t);
  const result = ps(checkpoint, ['-ProjectPath', f.project, '-Label', 'test']);
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /ConfirmedSaved/);
  assert.deepEqual(await readFile(f.project), f.bytes);
  assert.deepEqual(await readdir(f.dir), ['Fixture.aep']);
});

test('AE checkpoint isolates parent module paths, copies exact bytes and refuses receipt overwrite', { skip: process.platform !== 'win32' }, async t => {
  const f = await fixture(t);
  const receipt = path.join(f.dir, 'receipt.json');
  const result = ps(checkpoint, ['-ProjectPath', f.project, '-Label', 'fixture', '-ReceiptPath', receipt, '-ConfirmedSaved'], { PSModulePath: path.join(f.dir, 'not-a-module-directory') });
  assert.equal(result.status, 0, result.stderr);
  const report = JSON.parse((await readFile(receipt, 'utf8')).replace(/^\uFEFF/, ''));
  assert.equal(report.ok, true);
  assert.equal(report.sourceSha256, sha(f.bytes));
  assert.equal(report.backupSha256, sha(f.bytes));
  assert.deepEqual(await readFile(report.backup), f.bytes);
  const repeat = ps(checkpoint, ['-ProjectPath', f.project, '-Label', 'different', '-ReceiptPath', receipt, '-ConfirmedSaved']);
  assert.notEqual(repeat.status, 0);
  assert.match(repeat.stderr, /overwrite an existing receipt/);
  assert.deepEqual(await readFile(f.project), f.bytes);
});

test('AE RAM helper rejects contradictory thresholds without starting or stopping an app', { skip: process.platform !== 'win32' }, () => {
  const result = ps(ram, ['-WarnAEGB', '2', '-StopAEGB', '1']);
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /WarnAEGB must be lower than StopAEGB/);
});
