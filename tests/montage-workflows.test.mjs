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
const sync = path.join(ROOT, 'skills/montage/montage-multicam-sync/scripts/sync_map.py');
const fixture = path.join(ROOT, 'skills/montage/montage-multicam-sync/assets/anchors.example.json');
const examples = path.join(ROOT, 'examples');
const json = async file => JSON.parse(await readFile(path.join(examples, file), 'utf8'));
function py(args, options = {}) {
  const r = spawnSync(PY, args, { encoding: 'utf8', env, timeout: 120000, ...options });
  assert.ifError(r.error);
  return r;
}
async function temporary(t) {
  const dir = await mkdtemp(path.join(tmpdir(), 'toolbox-montage-'));
  t.after(() => rm(dir, { recursive: true, force: true }));
  return dir;
}
let serial = 0;
async function calculate(dir, data, args = []) {
  const file = path.join(dir, `anchors-${serial++}.json`);
  await writeFile(file, typeof data === 'string' ? data : JSON.stringify(data));
  return py([sync, file, ...args]);
}
const config = anchors => ({ schema: 1, reference_rate: '30', camera_rate: '30', anchors });

// Pure stdlib tests always run; engines are never installed by the test suite.
test('sync fixture reproduces the published rational six-frame offset', async () => {
  const before = await readFile(fixture);
  const result = py([sync, fixture]);
  assert.equal(result.status, 0, result.stderr);
  const report = JSON.parse(result.stdout);
  assert.deepEqual(report, await json('outputs/sync-map.json'));
  assert.equal(report.scale_fraction, '1');
  assert.equal(report.offset_fraction, '-1/5');
  assert.equal(report.offset_reference_frames, -6);
  assert.equal(report.duration_scale_ppm, 0);
  assert.equal(report.kind, 'anchor-calculation-not-sync-certification');
  assert.deepEqual(await readFile(fixture), before);
});

test('sync sign, one-anchor unknown drift and exact mixed-rate frame conversion', async t => {
  const dir = await temporary(t);
  let result = await calculate(dir, config([{ reference: '0.7', camera: '0.5' }]));
  assert.equal(result.status, 0, result.stderr);
  let report = JSON.parse(result.stdout);
  assert.equal(report.offset_fraction, '1/5');
  assert.equal(report.offset_reference_frames, 6);
  assert.equal(report.drift_estimated, false);
  assert.equal(report.duration_scale_ppm, null);
  assert.match(report.warnings.join(' '), /unknown/);
  result = await calculate(dir, { schema: 1, reference_rate: '30000/1001', camera_rate: '25',
    anchors: [{ reference: 'f300', camera: 'f250' }] });
  assert.equal(result.status, 0, result.stderr);
  report = JSON.parse(result.stdout);
  assert.equal(report.offset_fraction, '1/100');
  assert.equal(report.reference_rate, '30000/1001');
  assert.equal(report.anchors[0].reference_s, 10.01);
  assert.equal(report.anchors[0].camera_s, 10);
});

test('two-anchor duration scaling uses the inverse playback speed and flags drift', async t => {
  const dir = await temporary(t);
  const result = await calculate(dir, config([{ reference: 0, camera: 0 }, { reference: 10, camera: 10.001 }]), ['--max-drift-ppm', '50']);
  assert.equal(result.status, 0, result.stderr);
  const report = JSON.parse(result.stdout);
  assert.equal(report.scale_fraction, '10000/10001');
  assert.equal(report.required_playback_speed_percent, 100.01);
  assert.ok(Math.abs(report.duration_scale_ppm + 99.990001) < 0.000001);
  assert.match(report.warnings.join(' '), /threshold/);
  assert.ok(report.anchors.every(a => a.fit_residual_s === 0));
  assert.ok(report.limitations.some(l => l.includes('not independent validation')));
});

test('sync rejects malformed, ambiguous, nonfinite and out-of-bounds input', async t => {
  const dir = await temporary(t);
  const good = config([{ reference: 'f15', camera: 'f21' }]);
  const cases = [
    'null', '[]', '{"schema":1,"schema":1}', '{"schema":NaN}',
    { ...good, schema: true }, { ...good, schema: 2 }, { ...good, extra: 'unknown' },
    { ...good, anchors: [] }, { ...good, anchors: [good.anchors[0], good.anchors[0], good.anchors[0]] },
    { ...good, reference_rate: '1/0' }, { ...good, reference_rate: 0 }, { ...good, camera_rate: true },
    { ...good, camera_rate: 241 }, { ...good, camera_rate: 'Infinity' },
    config([{ reference: -1, camera: 0 }]), config([{ reference: 'f1.5', camera: 0 }]),
    config([{ reference: '00:00:01:00', camera: 0 }]), config([{ reference: '86400.1', camera: 0 }]),
    config([{ reference: '1'.repeat(49), camera: 0 }]), config([{ reference: true, camera: 0 }]),
    config([{ reference: 0, camera: 0, extra: 1 }]),
    config([{ reference: 1, camera: 0 }, { reference: 0, camera: 1 }]),
    config([{ reference: 0, camera: 1 }, { reference: 1, camera: 1 }]),
    ' '.repeat(65537) + '{}',
  ];
  for (const data of cases) {
    const result = await calculate(dir, data);
    assert.equal(result.status, 2, result.stdout);
    assert.equal(result.stdout, '');
    assert.doesNotMatch(result.stderr, /Traceback/);
  }
  for (const value of ['nan', 'inf', '-1', '1000001']) {
    assert.equal((await calculate(dir, good, ['--max-drift-ppm', value])).status, 2);
  }
});

test('sync output is exclusive, preserves input and does not create missing parents', async t => {
  const dir = await temporary(t);
  const target = path.join(dir, 'result.json');
  const before = await readFile(fixture);
  const first = py([sync, fixture, '--out', target]);
  assert.equal(first.status, 0, first.stderr);
  const saved = await readFile(target);
  assert.deepEqual(JSON.parse(saved), JSON.parse(first.stdout));
  assert.equal(py([sync, fixture, '--out', target]).status, 2);
  assert.deepEqual(await readFile(target), saved);
  const input = path.join(dir, 'source.json');
  await writeFile(input, before);
  assert.equal(py([sync, input, '--out', input]).status, 2);
  assert.deepEqual(await readFile(input), before);
  const missing = path.join(dir, 'missing', 'out.json');
  assert.equal(py([sync, fixture, '--out', missing]).status, 2);
  await assert.rejects(access(path.dirname(missing)));
});

test('new reports bind real media and state unperformed native/audio work', async () => {
  const reports = await json('outputs/montage-qc.json');
  assert.equal(Object.keys(reports).length, 6);
  for (const [name, report] of Object.entries(reports)) {
    const data = await readFile(path.join(examples, 'media', name));
    assert.equal(report.sha256, createHash('sha256').update(data).digest('hex'), name);
    assert.equal(report.size_bytes, data.length, name);
    assert.equal(report.ok, true, name);
    if (name.endsWith('.mp4')) {
      assert.equal(report.video.decoded_frames, 90, name);
      assert.equal(report.probe.video.fps, 30, name);
      assert.equal(report.probe.duration_s, 3, name);
    }
  }
  const build = await json('outputs/montage-build-info.json');
  for (const key of ['native_ae_render', 'native_premiere_execution', 'human_audio_audition', 'upstream_pipeline_executed', 'contains_recorded_or_generated_speech']) assert.equal(build[key], false);
  assert.equal(build.cloud_requests, 0);
  const colour = await json('outputs/colour-check.json');
  assert.ok(colour.after.mean_absolute_error_8bit < colour.before.mean_absolute_error_8bit);
  assert.ok(colour.after.max_error_8bit <= 1);
  assert.equal((await json('outputs/proxy-check.json')).native_attachment_tested, false);
  const retime = await json('outputs/retime-map.json');
  assert.equal(retime.smooth_ramp, false);
  assert.equal(retime.optical_flow, false);
  assert.deepEqual(retime.selected_source_frames, [
    ...Array.from({ length: 30 }, (_, n) => n * 2),
    ...Array.from({ length: 30 }, (_, n) => 60 + n),
    ...Array.from({ length: 30 }, (_, n) => 90 + n * 4),
  ]);
  assert.equal(retime.mapping_verified_with, 'decoded-source-vs-filter-output-framehash-sha256-before-encoding');
  assert.deepEqual(retime.segments.map(s => (s.source_frames[1] - s.source_frames[0]) / retime.source_fps / s.speed), [1, 1, 1]);
});

test('synthetic cleanup measurements reproduce from PCM without claiming speech quality', async () => {
  const report = await json('outputs/dialogue-check.json');
  const result = py(['-c', [
    'import json, math, struct, sys, wave',
    'out = []',
    'for p in sys.argv[1:]:',
    ' with wave.open(p, "rb") as w:',
    '  assert (w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()) == (1, 2, 48000, 144000)',
    '  values = struct.unpack("<144000h", w.readframes(144000))[4800:16800]',
    '  out.append(20 * math.log10(math.sqrt(sum((v / 32768)**2 for v in values) / len(values))))',
    'print(json.dumps(out))',
  ].join('\n'), path.join(examples, 'media/dialogue-noisy.wav'), path.join(examples, 'media/dialogue-cleaned.wav')]);
  assert.equal(result.status, 0, result.stderr);
  const [before, after] = JSON.parse(result.stdout);
  assert.ok(after < before);
  assert.ok(Math.abs(before - report.before_noise_rms_dbfs) < .0001);
  assert.ok(Math.abs(after - report.after_noise_rms_dbfs) < .0001);
  assert.equal(report.contains_speech, false);
  assert.equal(report.human_audio_audition, false);
});

const lookup = py(['-c', [
  'import os, shutil, importlib.util',
  'p = os.environ.get("FFMPEG") or shutil.which("ffmpeg")',
  'if not p and importlib.util.find_spec("imageio_ffmpeg"):',
  ' import imageio_ffmpeg; p = imageio_ffmpeg.get_ffmpeg_exe()',
  'print(p or "")',
].join('\n')]);
const ffmpeg = lookup.status === 0 ? lookup.stdout.trim() : '';

test('new MP4s have 90 monotonic 30-fps decoded timestamps (optional FFmpeg)', { skip: !ffmpeg && 'FFmpeg unavailable' }, () => {
  for (const name of ['proxy-source', 'proxy-small', 'multicam-sync', 'retime']) {
    const r = spawnSync(ffmpeg, ['-hide_banner', '-nostdin', '-i', path.join(examples, 'media', name + '.mp4'), '-vf', 'showinfo', '-vsync', '0', '-f', 'null', '-'], { encoding: 'utf8', timeout: 60000 });
    assert.ifError(r.error);
    assert.equal(r.status, 0, r.stderr);
    const times = [...r.stderr.matchAll(/n:\s*\d+.*?pts_time:([\d.-]+)/g)].map(m => Number(m[1]));
    assert.equal(times.length, 90, name);
    times.forEach((time, index) => assert.ok(Math.abs(time - index / 30) < .00002, `${name} frame ${index}: ${time}`));
  }
});

const renderDeps = py(['-c', [
  'from PIL import Image, ImageFont',
  'for font in ("DejaVuSans.ttf", "arial.ttf"):',
  ' try:',
  '  ImageFont.truetype(font, 18); print(font); break',
  ' except OSError: pass',
].join('\n')]);
const font = renderDeps.status === 0 ? renderDeps.stdout.trim() : '';

test('montage examples regenerate in isolation when optional rendering dependencies exist', { skip: !(ffmpeg && font) && 'FFmpeg/Pillow/local font unavailable' }, async t => {
  const dir = await temporary(t);
  const target = path.join(dir, 'new');
  const result = py([path.join(examples, 'build.py'), '--set', 'montage', '--out', target, '--font', font], { env: { ...env, FFMPEG: ffmpeg }, timeout: 240000 });
  assert.equal(result.status, 0, result.stderr);
  const summary = JSON.parse(result.stdout);
  assert.equal(summary.media_files, 11);
  assert.ok(summary.total_media_bytes < 3 * 1024 * 1024);
  const fresh = JSON.parse(await readFile(path.join(target, 'outputs/sync-map.json'), 'utf8'));
  assert.deepEqual(fresh, await json('outputs/sync-map.json'));
  // This set must not execute the core gallery's Node/REA helper or rewrite its outputs.
  await assert.rejects(access(path.join(target, 'outputs/api-summary.json')));
  assert.equal(py([path.join(examples, 'build.py'), '--set', 'montage', '--out', target]).status, 2);
});
