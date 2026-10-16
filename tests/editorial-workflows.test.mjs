import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, writeFile, mkdtemp, mkdir, copyFile, rm, access } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { ROOT } from '../scripts/upstreams.mjs';

const PY = process.env.PYTHON || 'python';
const env = { ...process.env, PYTHONDONTWRITEBYTECODE: '1', PYTHONIOENCODING: 'utf-8' };
const examples = path.join(ROOT, 'examples');
const json = async file => JSON.parse(await readFile(path.join(examples, file), 'utf8'));
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
function py(args, options = {}) {
  const r = spawnSync(PY, args, { encoding: 'utf8', env, timeout: 30000, ...options });
  assert.ifError(r.error);
  return r;
}
async function temporary(t) {
  const dir = await mkdtemp(path.join(tmpdir(), 'toolbox-editorial-'));
  t.after(() => rm(dir, { recursive: true, force: true }));
  return dir;
}

test('fictional paper edit preserves source ranges and has no invented execution claims', async () => {
  const source = await json('fixtures/transcript-selects.json'), report = await json('outputs/paper-edit.json');
  let cursor = 0;
  for (const [index, id] of source.selected_ids.entries()) {
    const segment = source.segments.find(s => s.id === id), selected = report.selected[index];
    const length = segment.out_frame - segment.in_frame;
    assert.deepEqual(selected.source_frames, [segment.in_frame, segment.out_frame]);
    assert.deepEqual(selected.output_frames, [cursor, cursor + length]);
    assert.equal(selected.text, segment.text);
    cursor += length;
  }
  assert.equal(report.output_frames, cursor);
  assert.equal(report.output_duration_s, cursor / Number(source.source_rate));
  assert.equal(report.output_duration_s, 2);
  assert.equal(report.fixture_sha256, sha(await readFile(path.join(examples, 'fixtures/transcript-selects.json'))));
  for (const key of ['asr_executed', 'recorded_speech', 'native_edit_executed', 'human_context_review']) assert.equal(report[key], false);
});

test('scene candidates and QC bind the actual short encoded source', async () => {
  const report = await json('outputs/scene-candidates.json'), qc = await json('outputs/scene-qc.json');
  const bytes = await readFile(path.join(examples, report.source));
  assert.equal(report.sha256, sha(bytes));
  assert.equal(qc.sha256, report.sha256);
  assert.equal(qc.ok, true);
  assert.equal(qc.video.decoded_frames, 90);
  assert.equal(qc.probe.duration_s, 3);
  assert.deepEqual(report.candidates.map(c => c.frame), [30, 60]);
  assert.deepEqual(report.candidates.map(c => c.time_s), [1, 2]);
  assert.ok(report.candidates.every(c => c.score >= 12));
  assert.equal(report.human_editorial_review, false);
  assert.equal(report.pyscenedetect_executed, false);
});

test('English/French SRT checks reproduce and WebVTT uses matching UTF-8 cues', async () => {
  const report = await json('outputs/caption-access-check.json');
  const helper = path.join(ROOT, 'skills/montage/montage-editing-craft/scripts/srt_check.py');
  for (const language of ['en', 'fr']) {
    const filename = path.join(examples, `outputs/captions-sounds-${language}.srt`);
    const r = py([helper, filename, '--preset', 'social-landscape', ...(language === 'fr' ? ['--french', 'fr-CA'] : [])]);
    assert.equal(r.status, 0, r.stderr);
    assert.deepEqual(JSON.parse(r.stdout), report.srt_checks[language]);
    const srt = (await readFile(filename, 'utf8')).replace(/\r\n/g, '\n');
    const vtt = (await readFile(filename.replace(/\.srt$/, '.vtt'), 'utf8')).replace(/\r\n/g, '\n');
    assert.ok(vtt.startsWith('WEBVTT\n\nNOTE '));
    assert.ok(vtt.endsWith(srt.replace(/,/g, '.')));
    assert.equal([...vtt.matchAll(/-->/g)].length, 3);
  }
  assert.equal(report.audio_reference_sha256, sha(await readFile(path.join(ROOT, report.audio_reference))));
  for (const key of ['spoken_dialogue', 'asr_executed', 'human_audio_audition', 'human_translation_review', 'native_player_tested', 'accessibility_certified']) assert.equal(report[key], false);
});

test('handoff restores listed bytes and detects tampering without touching originals', async t => {
  const dir = await temporary(t), manifest = await json('outputs/handoff-manifest.json');
  const helper = path.join(ROOT, 'skills/after-effects/ae-production-workflow/scripts/verify-delivery-manifest.py');
  const published = await json('outputs/handoff-restore-check.json');
  assert.equal(published.before.ok, true);
  assert.equal(published.restored.ok, true);
  assert.equal(published.native_project_opened, false);
  assert.equal(published.dependency_discovery_performed, false);
  assert.equal(published.source_deleted, false);
  const sourceManifest = path.join(examples, 'outputs/handoff-manifest.json');
  assert.equal(py([helper, sourceManifest, '--root', examples]).status, 0);
  for (const record of manifest.files) {
    const target = path.join(dir, record.path);
    const bytes = await readFile(path.join(examples, record.path));
    assert.equal(record.sha256, sha(bytes));
    assert.equal(record.size, bytes.length);
    await mkdir(path.dirname(target), { recursive: true });
    await copyFile(path.join(examples, record.path), target);
  }
  const savedManifest = path.join(dir, 'manifest.json');
  await copyFile(sourceManifest, savedManifest);
  let result = py([helper, savedManifest, '--root', dir]);
  assert.equal(result.status, 0, result.stdout);
  assert.equal(JSON.parse(result.stdout).entriesChecked, 4);
  await writeFile(path.join(dir, manifest.canonical), 'intentional test-only corruption\n');
  result = py([helper, savedManifest, '--root', dir]);
  assert.equal(result.status, 1);
  assert.equal(JSON.parse(result.stdout).canonicalOk, false);
  assert.equal(sha(await readFile(path.join(examples, manifest.canonical))), manifest.canonical_sha256);
});

const lookup = py(['-c', [
  'import os,shutil,importlib.util,json',
  'p=os.environ.get("FFMPEG") or shutil.which("ffmpeg")',
  'if not p and importlib.util.find_spec("imageio_ffmpeg"):',
  ' import imageio_ffmpeg; p=imageio_ffmpeg.get_ffmpeg_exe()',
  'font=None',
  'if importlib.util.find_spec("PIL"):',
  ' from PIL import ImageFont',
  ' for f in ([os.environ["TOOLBOX_FONT"]] if os.environ.get("TOOLBOX_FONT") else ["DejaVuSans.ttf","arial.ttf"]):',
  '  try: ImageFont.truetype(f,18); font=f; break',
  '  except OSError: pass',
  'print(json.dumps({"ffmpeg":p,"font":font}))',
].join('\n')]);
const deps = lookup.status === 0 ? JSON.parse(lookup.stdout) : {};
if (process.env.REQUIRE_MEDIA_TESTS === '1') assert.ok(deps.ffmpeg && deps.font, 'Mandatory editorial generation requires FFmpeg/Pillow/font');

test('scene candidates reproduce from the published encoding (optional FFmpeg)', { skip: !deps.ffmpeg && 'FFmpeg unavailable' }, () => {
  const r = spawnSync(deps.ffmpeg, ['-hide_banner', '-loglevel', 'error', '-nostdin', '-i', path.join(examples, 'media/scene-selects.mp4'),
    '-an', '-vf', 'scdet=t=12,metadata=mode=print:file=-', '-f', 'null', '-'], { encoding: 'utf8', timeout: 30000 });
  assert.ifError(r.error);
  assert.equal(r.status, 0, r.stderr);
  assert.deepEqual([...r.stdout.matchAll(/lavfi\.scd\.time=([\d.]+)/g)].map(m => Number(m[1])), [1, 2]);
});

test('editorial examples regenerate alone with optional media dependencies', { skip: !(deps.ffmpeg && deps.font) && 'FFmpeg/Pillow/font unavailable' }, async t => {
  const dir = await temporary(t), target = path.join(dir, 'new');
  const r = py([path.join(examples, 'build.py'), '--set', 'editorial', '--out', target, '--font', deps.font],
    { env: { ...env, FFMPEG: deps.ffmpeg }, timeout: 180000 });
  assert.equal(r.status, 0, r.stderr);
  assert.equal(JSON.parse(r.stdout).media_files, 4);
  assert.ok(JSON.parse(r.stdout).total_media_bytes < 1024 * 1024);
  const fresh = JSON.parse(await readFile(path.join(target, 'outputs/handoff-restore-check.json'), 'utf8'));
  assert.equal(fresh.restored.ok, true);
  assert.equal(fresh.native_project_opened, false);
  await assert.rejects(access(path.join(target, 'outputs/api-summary.json')));
  await assert.rejects(access(path.join(target, 'media/proxy-source.mp4')));
  assert.equal(py([path.join(examples, 'build.py'), '--set', 'editorial', '--out', target]).status, 2);
});
