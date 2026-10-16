import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, mkdtemp, writeFile, rm, access, readdir } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { ROOT } from '../scripts/upstreams.mjs';
import { EXPECTED_SKILLS } from '../scripts/check.mjs';
import { checkMediaRecord, readGifTiming, validateExamples, MAX_EXAMPLE_BYTES, MAX_GALLERY_BYTES } from '../scripts/check-examples.mjs';

const PY = process.env.PYTHON || 'python';
const env = { ...process.env, PYTHONIOENCODING: 'utf-8', PYTHONDONTWRITEBYTECODE: '1' };
const examples = path.join(ROOT, 'examples');
const manifest = JSON.parse(await readFile(path.join(examples, 'manifest.json'), 'utf8'));
const led = path.join(ROOT, 'skills/montage/led-signage-content/scripts/led_tool.py');
const srt = path.join(ROOT, 'skills/montage/montage-editing-craft/scripts/srt_check.py');
function py(script, args) {
  const r = spawnSync(PY, [script, ...args], { encoding: 'utf8', env, timeout: 120000 });
  assert.ifError(r.error);
  return r;
}
async function temporary(t) {
  const dir = await mkdtemp(path.join(tmpdir(), 'toolbox-examples-'));
  t.after(() => rm(dir, { recursive: true, force: true }));
  return dir;
}
const json = async p => JSON.parse(await readFile(path.join(examples, p), 'utf8'));
const lf = text => text.replace(/\r\n/g, '\n');

test('gallery covers all 23 skills and every included helper/reference with valid links', async () => {
  const result = await validateExamples(ROOT, EXPECTED_SKILLS);
  assert.deepEqual(result.errors, []);
  assert.equal(manifest.entries.length, 23);
  assert.equal(result.mediaPaths.size, 27);
  assert.ok(Object.values(manifest.media).reduce((n, m) => n + m.bytes, 0) <= MAX_GALLERY_BYTES);
  for (const entry of manifest.entries) {
    const skill = await readFile(path.join(ROOT, entry.skill), 'utf8');
    assert.ok(skill.includes(`examples/README.md#${entry.id}`), `${entry.id} needs a discoverable example`);
  }
  const pkg = JSON.parse(await readFile(path.join(ROOT, 'package.json'), 'utf8'));
  assert.ok(pkg.files.includes('examples/'));
});

test('media exception is exact, hash-pinned, format checked and size/duration bounded', async () => {
  const name = 'examples/media/ae-rig.gif';
  const data = await readFile(path.join(ROOT, name));
  const meta = manifest.media[name];
  assert.deepEqual(checkMediaRecord(name, meta, data), []);
  assert.ok(checkMediaRecord('examples/../client.mp4', meta, data).some(e => /path/.test(e)));
  assert.ok(checkMediaRecord('examples/media/secret.key', meta, data).some(e => /path/.test(e)));
  assert.ok(checkMediaRecord(name, { ...meta, sha256: '0'.repeat(64) }, data).some(e => /hash/.test(e)));
  assert.ok(checkMediaRecord(name, { ...meta, bytes: MAX_EXAMPLE_BYTES + 1 }, data).some(e => /size/.test(e)));
  assert.ok(checkMediaRecord(name, { ...meta, duration_s: 60 }, data).some(e => /four seconds/.test(e)));
  assert.ok(checkMediaRecord(name, { ...meta, origin: 'client-footage' }, data).some(e => /provenance/.test(e)));
  const bad = Buffer.from(data);
  bad.write('NOTGIF', 0);
  assert.ok(checkMediaRecord(name, { ...meta, sha256: createHash('sha256').update(bad).digest('hex') }, bad).some(e => /signature/.test(e)));
  assert.ok(checkMediaRecord(name, { ...meta, width: 123 }, data).some(e => /dimensions/.test(e)));
});

test('GIF timing comes from encoded frame delays, not a decoder progress endpoint', async () => {
  const name = 'examples/media/retime.gif';
  const bytes = await readFile(path.join(ROOT, name));
  assert.deepEqual(readGifTiming(bytes), { frames: 30, duration_s: 3 });
  assert.ok(checkMediaRecord(name, { ...manifest.media[name], duration_s: 2.9 }, bytes).some(e => /encoded delays/.test(e)));
  assert.ok(checkMediaRecord(name, { ...manifest.media[name], frames: 29 }, bytes).some(e => /encoded delays/.test(e)));
  assert.throws(() => readGifTiming(bytes.subarray(0, 20)), /Truncated/);
  assert.throws(() => readGifTiming(bytes.subarray(0, bytes.length - 1)), /trailer/);
  assert.throws(() => readGifTiming(Buffer.from('not a GIF')), /header/);
  assert.ok(checkMediaRecord(name, null, bytes).length > 0);
  const paletteEnd = 13 + ((bytes[10] & 0x80) ? 3 * (1 << ((bytes[10] & 7) + 1)) : 0);
  const firstControl = bytes.indexOf(Buffer.from([0x21, 0xf9, 0x04]), paletteEnd);
  assert.ok(firstControl >= paletteEnd); // First control precedes any compressed pixels.
  const longer = Buffer.from(bytes);
  longer.writeUInt16LE(20, firstControl + 4); // First frame now holds 200 ms, not 100.
  assert.deepEqual(readGifTiming(longer), { frames: 30, duration_s: 3.1 });
  const changed = { ...manifest.media[name], sha256: createHash('sha256').update(longer).digest('hex') };
  assert.ok(checkMediaRecord(name, changed, longer).some(e => /encoded delays/.test(e)));
  assert.deepEqual(checkMediaRecord(name, { ...changed, duration_s: 3.1 }, longer), []);
  longer.writeUInt16LE(0, firstControl + 4);
  assert.throws(() => readGifTiming(longer), /positive delays/);
});

test('LED calculator, guides and test-card examples reproduce with standard-library Python', async t => {
  const dir = await temporary(t);
  const text = py(led, ['text-size', '--profile', 'led-rollup-516x1032', '--distance', '4']);
  assert.equal(text.status, 0, text.stderr);
  assert.deepEqual(JSON.parse(text.stdout), await json('outputs/text-size.json'));
  for (const [command, profile, output, flag] of [
    ['guides', 'led-wall-3x-516x1032', 'led-guides.png', '--out'],
    ['testcard', 'led-rollup-516x1032', 'led-testcard.png', '--out-png'],
  ]) {
    const dest = path.join(dir, output);
    const r = py(led, [command, '--profile', profile, flag, dest]);
    assert.equal(r.status, 0, r.stdout);
    assert.deepEqual(await readFile(dest), await readFile(path.join(examples, 'media', output)));
  }
});

test('subtitle example is a real reproducible correction and preserves the source', async t => {
  const dir = await temporary(t);
  const source = path.join(examples, 'fixtures/captions.srt');
  const before = await readFile(source);
  const dest = path.join(dir, 'fixed.srt');
  const r = py(srt, [source, '--french', 'fr-CA', '--fix-french-out', dest]);
  assert.equal(r.status, 1, r.stdout); // Deliberately bad input, not a generation failure.
  assert.equal(JSON.parse(r.stdout).fixed_copy.remaining, 0);
  assert.equal(lf(await readFile(dest, 'utf8')), lf(await readFile(path.join(examples, 'outputs/captions-fixed.srt'), 'utf8')));
  assert.deepEqual(await readFile(source), before);
  assert.equal(py(srt, [dest, '--french', 'fr-CA']).status, 0);
});

test('manifest example verifies real fixture bytes without claiming an AEP', async () => {
  const verify = path.join(ROOT, 'skills/after-effects/ae-production-workflow/scripts/verify-delivery-manifest.py');
  const r = py(verify, [path.join(examples, 'outputs/delivery-manifest.json'), '--root', path.join(examples, 'outputs')]);
  assert.equal(r.status, 0, r.stdout);
  assert.equal(JSON.parse(r.stdout).entriesChecked, 1);
  const report = await json('outputs/build-info.json');
  assert.equal(report.native_ae_render, false);
  assert.equal(report.cloud_requests, 0);
  assert.equal(report.human_audio_audition, false);
});

test('API summary is reproduced from synthetic events, with no routes or secrets', async () => {
  const helper = path.join(ROOT, 'skills/reverse-api-investigation/scripts/har-summary.mjs');
  const source = path.join(examples, 'fixtures/request-events.json');
  const r = spawnSync(process.execPath, [helper, source], { encoding: 'utf8', timeout: 30000 });
  assert.equal(r.status, 0, r.stderr);
  const current = JSON.parse(r.stdout), saved = await json('outputs/api-summary.json');
  // Fixture line endings can change in a user's nonstandard checkout; counts cannot.
  delete current.sourceSha256;
  delete saved.sourceSha256;
  assert.deepEqual(current, saved);
  assert.equal(current.totalEntries, 2);
  assert.equal(current.endpoints[0].requests, 2);
  assert.equal(current.endpoints[0].route, undefined);
});

test('gallery generator refuses existing directories and direct writes into published examples', async t => {
  const dir = await temporary(t);
  await writeFile(path.join(dir, 'keep.txt'), 'keep');
  const script = path.join(examples, 'build.py');
  const existing = py(script, ['--out', dir]);
  assert.equal(existing.status, 2);
  assert.match(existing.stderr, /already exists/);
  assert.equal(await readFile(path.join(dir, 'keep.txt'), 'utf8'), 'keep');
  const bad = path.join(examples, 'must-not-be-created-by-test');
  assert.equal(py(script, ['--out', bad]).status, 2);
  await assert.rejects(access(bad));
});

test('current distributable text uses generic device names only', async () => {
  const excluded = new Set(['.git', '.local', 'node_modules', '__pycache__']);
  const retired = ['pixa', 'nova'].join('');
  async function scan(dir) {
    for (const entry of await readdir(dir, { withFileTypes: true })) {
      if (excluded.has(entry.name)) continue;
      const file = path.join(dir, entry.name);
      if (entry.isDirectory()) await scan(file);
      else if (/\.(?:md|json|py|ps1|mjs|csv|srt|txt)$/.test(entry.name)) {
        assert.ok(!(await readFile(file, 'utf8')).toLowerCase().includes(retired), path.relative(ROOT, file));
      }
    }
  }
  await scan(ROOT);
});

const lookup = spawnSync(PY, ['-c', [
  'import os, shutil, importlib.util',
  'p = os.environ.get("FFMPEG") or shutil.which("ffmpeg")',
  'if not p and importlib.util.find_spec("imageio_ffmpeg"):',
  ' import imageio_ffmpeg; p = imageio_ffmpeg.get_ffmpeg_exe()',
  'print(p or "")',
].join('\n')], { encoding: 'utf8', timeout: 30000 });
const ffmpeg = lookup.status === 0 ? lookup.stdout.trim() : '';
if (process.env.REQUIRE_MEDIA_TESTS === '1') assert.ok(ffmpeg, 'Mandatory gallery decoding requires FFmpeg');

test('every gallery animation and audio file fully decodes (optional FFmpeg)', { skip: !ffmpeg && 'FFmpeg unavailable' }, async () => {
  for (const name of Object.keys(manifest.media).filter(p => /\.(?:gif|mp4|wav)$/.test(p))) {
    const r = spawnSync(ffmpeg, ['-hide_banner', '-nostdin', '-nostats', '-v', 'error', '-xerror', '-i', path.join(ROOT, name), '-f', 'null', '-', '-progress', 'pipe:1'], { encoding: 'utf8', timeout: 120000 });
    assert.ifError(r.error);
    assert.equal(r.status, 0, `${name}: ${r.stderr}`);
    const times = [...r.stdout.matchAll(/^out_time_us=(\d+)$/gm)];
    assert.ok(times.length, `No decoded duration for ${name}`);
    const seconds = Number(times.at(-1)[1]) / 1e6;
    const counts = [...r.stdout.matchAll(/^frame=(\d+)$/gm)];
    if (name.endsWith('.gif')) {
      // FFmpeg 6 reports the last PTS (2.9 s), while 7 reports its end (3 s).
      // Require every frame to decode and independently verify actual GIF delays.
      const timing = readGifTiming(await readFile(path.join(ROOT, name)));
      assert.equal(Number(counts.at(-1)?.[1]), timing.frames, name);
      assert.equal(timing.frames, manifest.media[name].frames, name);
      assert.equal(timing.duration_s, manifest.media[name].duration_s, name);
      assert.ok(timing.duration_s <= 4, name);
    } else {
      assert.ok(seconds <= 4 && Math.abs(seconds - manifest.media[name].duration_s) <= 0.06, `${name}: ${seconds} s`);
      if (name.endsWith('.mp4')) assert.equal(Number(counts.at(-1)?.[1]), 90, name);
    }
  }
});
