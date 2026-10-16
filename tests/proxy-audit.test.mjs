import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, writeFile, mkdtemp, rm, access } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { ROOT } from '../scripts/upstreams.mjs';

const PY = process.env.PYTHON || 'python';
const env = { ...process.env, PYTHONDONTWRITEBYTECODE: '1', PYTHONIOENCODING: 'utf-8' };
const helper = path.join(ROOT, 'skills/montage/montage-proxy-conform/scripts/proxy_audit.py');
const fixture = name => path.join(ROOT, 'examples/fixtures', name);
const hash = data => createHash('sha256').update(data).digest('hex');
function py(args, options = {}) {
  const result = spawnSync(PY, args, { encoding: 'utf8', env, timeout: 30000, ...options });
  assert.ifError(result.error);
  return result;
}
async function temporary(t) {
  const dir = await mkdtemp(path.join(tmpdir(), 'toolbox-proxy-audit-'));
  t.after(() => rm(dir, { recursive: true, force: true }));
  return dir;
}
const base = JSON.parse(await readFile(fixture('proxy-source-probe.json'), 'utf8'));
const small = JSON.parse(await readFile(fixture('proxy-small-probe.json'), 'utf8'));
function complete(data) {
  const d = structuredClone(data);
  d.streams[0].tags = { timecode: '00:00:00:00', reel_name: 'SYNTH_A' };
  return d;
}
let serial = 0;
async function compare(dir, a, b, args = []) {
  const files = ['a', 'b'].map(n => path.join(dir, `${n}-${serial}.json`)); serial++;
  for (const [index, data] of [a, b].entries()) await writeFile(files[index], typeof data === 'string' ? data : JSON.stringify(data));
  return py([helper, 'json', ...files, ...args]);
}
const row = (report, name) => report.checks.find(c => c.check === name);

test('proxy snapshots reproduce incomplete metadata, never an attachment pass', async () => {
  const a = fixture('proxy-source-probe.json'), b = fixture('proxy-small-probe.json');
  const before = [await readFile(a), await readFile(b)];
  const result = py([helper, 'json', a, b]);
  assert.equal(result.status, 3, result.stderr);
  const report = JSON.parse(result.stdout);
  assert.equal(report.verdict, 'incomplete');
  assert.equal(report.unknowns, 2);
  assert.equal(report.failures, 0);
  assert.equal(report.native_attachment_tested, false);
  assert.equal(report.media_inspected, false);
  assert.equal(report.inputs.source.sha256, hash(before[0]));
  const published = JSON.parse(await readFile(path.join(ROOT, 'examples/outputs/proxy-audit.json'), 'utf8'));
  // A nonstandard checkout may change JSON line endings; semantics do not change.
  delete report.inputs; delete published.inputs;
  assert.deepEqual(report, published);
  assert.deepEqual([await readFile(a), await readFile(b)], before);
});

test('complete metadata passes while exact rational rates and mismatches stay strict', async t => {
  const dir = await temporary(t), a = complete(base), b = complete(small);
  let r = await compare(dir, a, b);
  assert.equal(r.status, 0, r.stderr);
  assert.equal(JSON.parse(r.stdout).verdict, 'metadata-compatible');
  const cases = [
    ['avg_frame_rate', '29.97', 'video.average_frame_rate'],
    ['nb_read_frames', '89', 'video.decoded_frame_count'],
    ['duration', '2.900', 'video.duration'],
    ['start_time', '0.1', 'video.start_time'],
    ['height', 179, 'video.uniform_integer_downscale'],
    ['sample_aspect_ratio', '4:3', 'video.sample_aspect_ratio'],
    ['field_order', 'tt', 'video.field_order'],
    ['side_data_list', [{ rotation: 90 }], 'video.declared_rotation'],
    ['tags', { timecode: '00:00:00:01', reel_name: 'SYNTH_A' }, 'video.timecode'],
    ['tags', { timecode: '00:00:00:00', reel_name: 'SYNTH_B' }, 'video.reel_id'],
  ];
  for (const [field, value, check] of cases) {
    const changed = structuredClone(b); changed.streams[0][field] = value;
    r = await compare(dir, a, changed);
    assert.equal(r.status, 1, r.stderr);
    assert.equal(row(JSON.parse(r.stdout), check).status, 'fail', check);
  }
  a.streams[0].avg_frame_rate = '30000/1001';
  b.streams[0].avg_frame_rate = '30000/1001';
  assert.equal((await compare(dir, a, b)).status, 0);
  b.streams[0].avg_frame_rate = '29.97';
  assert.equal((await compare(dir, a, b)).status, 1); // Rounded display rate is not exact.
});

test('missing, malformed and ambiguous metadata remain unknown, not equal', async t => {
  const dir = await temporary(t);
  const a = complete(base), b = complete(small);
  for (const doc of [a, b]) {
    delete doc.streams[0].nb_read_frames; doc.streams[0].nb_frames = '90';
    delete doc.streams[0].duration; // Matching format durations cannot substitute for streams.
    doc.streams[0].field_order = [];
    doc.streams[0].sample_aspect_ratio = '0:1';
    doc.streams[0].side_data_list = 'invalid';
    doc.format.tags = { timecode: '00:01:00:00' }; // Conflicts with video tag.
  }
  const r = await compare(dir, a, b);
  assert.equal(r.status, 3, r.stderr);
  const report = JSON.parse(r.stdout);
  for (const key of ['decoded_frame_count', 'duration', 'field_order', 'sample_aspect_ratio', 'declared_rotation', 'timecode']) {
    assert.equal(row(report, 'video.' + key).status, 'unknown');
  }
  assert.doesNotMatch(r.stderr, /Traceback/);
});

test('audio topology is compared and cover-art video is excluded', async t => {
  const dir = await temporary(t), a = complete(base), b = complete(small);
  const audio = { codec_type: 'audio', sample_rate: '48000', channels: 2, channel_layout: 'stereo', start_time: '0', duration: '3' };
  a.streams.push(audio, { codec_type: 'video', disposition: { attached_pic: 1 }, width: 100, height: 100 });
  b.streams.push(structuredClone(audio));
  assert.equal((await compare(dir, a, b)).status, 0);
  b.streams[1].channels = 1; b.streams[1].channel_layout = 'mono';
  const r = await compare(dir, a, b);
  assert.equal(r.status, 1);
  assert.equal(row(JSON.parse(r.stdout), 'audio[0].channels').status, 'fail');
  assert.equal(row(JSON.parse(r.stdout), 'audio[0].channel_layout').status, 'fail');
  b.streams.pop();
  assert.equal(row(JSON.parse((await compare(dir, a, b)).stdout), 'audio.stream_count').status, 'fail');
});

test('bounded JSON parsing rejects malformed/oversized data and omits private tags', async t => {
  const dir = await temporary(t);
  for (const bad of ['null', '[]', '{}', '{"streams":[],"streams":[]}', '{"streams":[],"x":NaN}',
    { streams: [null] }, { streams: Array.from({ length: 65 }, () => ({})) }, { streams: [], format: [] },
    ' '.repeat(1024 * 1024 + 1) + '{}']) {
    const r = await compare(dir, bad, small);
    assert.equal(r.status, 2);
    assert.equal(r.stdout, '');
    assert.doesNotMatch(r.stderr, /Traceback/);
  }
  const a = complete(base), b = complete(small);
  for (const doc of [a, b]) {
    doc.format.filename = 'private-path-sentinel';
    doc.format.tags = { comment: 'private-tag-sentinel' };
    doc.streams[0].tags.reel_name = 'private-reel-sentinel';
  }
  const r = await compare(dir, a, b);
  assert.equal(r.status, 0);
  assert.doesNotMatch(r.stdout + r.stderr, /private-.*-sentinel/);
});

test('proxy report creation is exclusive and inputs/missing parents are preserved', async t => {
  const dir = await temporary(t), target = path.join(dir, 'report.json');
  const a = path.join(dir, 'source.json'), b = path.join(dir, 'proxy.json');
  await writeFile(a, JSON.stringify(base)); await writeFile(b, JSON.stringify(small));
  const before = await readFile(a);
  let r = py([helper, 'json', a, b, '--report', target]);
  assert.equal(r.status, 3);
  const saved = await readFile(target);
  assert.deepEqual(JSON.parse(saved), JSON.parse(r.stdout));
  assert.equal(py([helper, 'json', a, b, '--report', target]).status, 2);
  assert.deepEqual(await readFile(target), saved);
  assert.equal(py([helper, 'json', a, b, '--report', a]).status, 2);
  assert.deepEqual(await readFile(a), before);
  assert.equal(py([helper, 'json', a, a]).status, 2);
  const missing = path.join(dir, 'missing', 'report.json');
  assert.equal(py([helper, 'json', a, b, '--report', missing]).status, 2);
  await assert.rejects(access(path.dirname(missing)));
});

test('missing media prerequisites fail explicitly without installation or fallback', () => {
  const absent = path.join(ROOT, '.local', 'no-such-ffprobe-for-test');
  const r = py([helper, 'media', fixture('proxy-source-probe.json'), fixture('proxy-small-probe.json'), '--ffprobe', absent]);
  assert.equal(r.status, 2);
  assert.match(r.stderr, /ffprobe unavailable/);
  const preflight = spawnSync(process.execPath, [path.join(ROOT, 'scripts/test-media.mjs'), '--preflight-only'],
    { encoding: 'utf8', timeout: 30000, env: { ...env, FFPROBE: absent } });
  assert.ifError(preflight.error);
  assert.equal(preflight.status, 2);
  assert.match(preflight.stderr, /required|preflight/);
  assert.doesNotMatch(preflight.stdout, /mandatoryMediaTests/);
});

const lookup = py(['-c', 'import os,shutil; print(os.environ.get("FFPROBE") or shutil.which("ffprobe") or "")']);
const ffprobe = lookup.status === 0 ? lookup.stdout.trim() : '';
if (process.env.REQUIRE_MEDIA_TESTS === '1') assert.ok(ffprobe, 'Mandatory proxy integration requires ffprobe');
test('actual proxy media is probed and bound to media hashes (optional ffprobe)', { skip: !ffprobe && 'ffprobe unavailable' }, async () => {
  const a = path.join(ROOT, 'examples/media/proxy-source.mp4'), b = path.join(ROOT, 'examples/media/proxy-small.mp4');
  const before = [await readFile(a), await readFile(b)];
  const r = py([helper, 'media', a, b, '--ffprobe', ffprobe], { timeout: 60000 });
  assert.equal(r.status, 3, r.stderr); // Missing synthetic camera identifiers, not a pass.
  const report = JSON.parse(r.stdout);
  assert.equal(report.media_inspected, true);
  assert.equal(report.failures, 0);
  assert.ok(report.unknowns >= 2);
  assert.equal(row(report, 'video.decoded_frame_count').source, 90);
  assert.equal(row(report, 'video.decoded_frame_count').proxy, 90);
  assert.equal(report.inputs.source.sha256, hash(before[0]));
  assert.equal(report.inputs.proxy.sha256, hash(before[1]));
  assert.deepEqual([await readFile(a), await readFile(b)], before);
});
