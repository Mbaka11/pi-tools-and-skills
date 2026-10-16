import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, writeFile, readFile, rm, stat } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { ROOT } from '../scripts/upstreams.mjs';

const PY = process.env.PYTHON || 'python';
const LED = path.join(ROOT, 'skills/montage/led-signage-content/scripts/led_tool.py');
const QC = path.join(ROOT, 'skills/montage/video-delivery-qc/scripts/media_qc.py');
const SFX = path.join(ROOT, 'skills/montage/sound-design-sfx/scripts/sfx_place.py');
const SRT = path.join(ROOT, 'skills/montage/montage-editing-craft/scripts/srt_check.py');
const env = { ...process.env, PYTHONIOENCODING: 'utf-8' };

function py(script, args, options = {}) {
  const result = spawnSync(PY, [script, ...args], { encoding: 'utf8', timeout: 120000, env, ...options });
  assert.ifError(result.error);
  return result;
}
const out = result => JSON.parse(result.stdout);

async function temp(t) {
  const dir = await mkdtemp(path.join(tmpdir(), 'pi-toolbox-montage-'));
  t.after(() => rm(dir, { recursive: true, force: true }));
  return dir;
}

function ffmpegPath() {
  if (process.env.FFMPEG) return process.env.FFMPEG;
  const which = spawnSync(process.platform === 'win32' ? 'where' : 'which', ['ffmpeg'], { encoding: 'utf8' });
  if (which.status === 0 && which.stdout.trim()) return which.stdout.split(/\r?\n/)[0].trim();
  const viaPy = spawnSync(PY, ['-c', 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())'], { encoding: 'utf8' });
  return viaPy.status === 0 ? viaPy.stdout.trim() : null;
}
const FFMPEG = ffmpegPath();
if (process.env.REQUIRE_MEDIA_TESTS === '1') assert.ok(FFMPEG, 'Mandatory media integration requires FFmpeg');

async function wav(file, seconds, channels = 1, rate = 48000) {
  const code = `import wave,struct,math,sys\nw=wave.open(sys.argv[1],'wb');w.setnchannels(${channels});w.setsampwidth(2);w.setframerate(${rate})\n` +
    `w.writeframes(b''.join(struct.pack('<'+'h'*${channels},*([int(9000*math.sin(i/7))]*${channels})) for i in range(int(${rate}*${seconds}))));w.close()`;
  const r = spawnSync(PY, ['-c', code, file], { encoding: 'utf8' });
  assert.equal(r.status, 0, r.stderr);
}

// ------------------------------------------------------------- led_tool.py
test('LED profiles expose generic pixel maps and divide into screens', () => {
  const r = py(LED, ['profiles']);
  assert.equal(r.status, 0, r.stderr);
  const { profiles } = out(r);
  assert.deepEqual([profiles['led-rollup-516x1032'].width, profiles['led-rollup-516x1032'].height], [516, 1032]);
  assert.deepEqual([profiles['led-wall-2x-516x1032'].width, profiles['led-wall-2x-516x1032'].height], [1032, 1032]);
  assert.deepEqual([profiles['led-wall-3x-516x1032'].width, profiles['led-wall-3x-516x1032'].height], [1548, 1032]);
  for (const [name, p] of Object.entries(profiles)) {
    assert.equal(p.width % p.screens[0], 0, name);
    assert.equal(p.height % p.screens[1], 0, name);
    assert.equal(p.width % 2, 0, name);
  }
});

test('LED text sizes follow the distance/150 x movement method', () => {
  const generic = out(py(LED, ['text-size', '--pitch', '4', '--distance', '6', '--movement', 'pedestrian']));
  assert.equal(generic.tiers.detail.cap_height_mm, 48);
  assert.equal(generic.tiers.detail.cap_height_px, 12);
  const rollup = out(py(LED, ['text-size', '--profile', 'led-rollup-516x1032', '--distance', '4']));
  assert.deepEqual(Object.values(rollup.tiers).map(t => t.cap_height_px), [18, 26, 44]);
  assert.deepEqual(rollup.screen_mm, [960, 1920]);
  const bad = py(LED, ['text-size', '--pitch', '0', '--distance', '4']);
  assert.equal(bad.status, 2);
});

test('LED guides and test card are valid PNGs at the device size and are never overwritten', async t => {
  const dir = await temp(t);
  const file = path.join(dir, 'guides.png');
  assert.equal(py(LED, ['guides', '--profile', 'led-wall-3x-516x1032', '--out', file]).status, 0);
  const png = await readFile(file);
  assert.equal(png.subarray(1, 4).toString(), 'PNG');
  assert.equal(png.readUInt32BE(16), 1548);
  assert.equal(png.readUInt32BE(20), 1032);
  const again = py(LED, ['guides', '--profile', 'led-wall-3x-516x1032', '--out', file]);
  assert.equal(again.status, 2);
  assert.deepEqual(await readFile(file), png);
  const card = path.join(dir, 'card.png');
  assert.equal(py(LED, ['testcard', '--profile', 'led-rollup-516x1032', '--out-png', card]).status, 0);
  const cardPng = await readFile(card);
  assert.equal(cardPng.readUInt32BE(16), 516);
  assert.equal(cardPng.readUInt32BE(20), 1032);
});

test('LED export plan is pixel-exact, silent, BT.709, CFR and refuses unsafe outputs', async t => {
  const dir = await temp(t);
  const input = path.join(dir, 'master.mov');
  await writeFile(input, 'not a real video - dry run only');
  const plan = out(py(LED, ['export', '--profile', 'led-rollup-516x1032', '--input', input, '--output', path.join(dir, 'out.mp4'), '--dry-run']));
  const cmd = plan.command.join(' ');
  for (const part of ['scale=516:1032', 'out_color_matrix=bt709', 'fps=30', 'libx264', 'yuv420p', '-an', '+faststart', '-map_metadata -1']) assert.ok(cmd.includes(part), part);
  assert.ok(plan.command.includes('-n'));
  const cover = out(py(LED, ['export', '--profile', 'led-rollup-516x1032', '--input', input, '--output', path.join(dir, 'c.mp4'), '--fit', 'cover', '--dry-run']));
  assert.ok(cover.command.join(' ').includes('force_original_aspect_ratio=increase'));
  assert.equal(py(LED, ['export', '--profile', 'led-rollup-516x1032', '--input', input, '--output', input, '--dry-run']).status, 2);
  await writeFile(path.join(dir, 'exists.mp4'), 'x');
  assert.equal(py(LED, ['export', '--profile', 'led-rollup-516x1032', '--input', input, '--output', path.join(dir, 'exists.mp4'), '--dry-run']).status, 2);
  assert.equal(py(LED, ['export', '--profile', 'nope', '--input', input, '--output', path.join(dir, 'o.mp4'), '--dry-run']).status, 2);
});

test('LED wall split crops one decode into per-screen files', async t => {
  const dir = await temp(t);
  const input = path.join(dir, 'wall.mov');
  await writeFile(input, 'dry run');
  const plan = out(py(LED, ['split', '--profile', 'led-wall-3x-516x1032', '--input', input, '--outdir', path.join(dir, 'deliver'), '--dry-run']));
  assert.deepEqual(plan.screen_size, [516, 1032]);
  assert.deepEqual(plan.outputs.map(o => o.crop[2]), [0, 516, 1032]);
  assert.ok(plan.command.join(' ').includes('split=3'));
  assert.equal(py(LED, ['split', '--profile', 'led-rollup-516x1032', '--input', input, '--outdir', dir, '--dry-run']).status, 2);
});

// ------------------------------------------------------------- media_qc.py
test('media QC parses FFmpeg banners and plans passes without touching the input', async t => {
  const dir = await temp(t);
  const input = path.join(dir, 'in.mp4');
  await writeFile(input, 'dry run');
  const plan = out(py(QC, [input, '--loop-check', '--dry-run']));
  assert.equal(plan.dry_run, true);
  assert.ok(plan.passes.video.join(' ').includes('blackdetect'));
  const code = [
    'import json, media_qc',
    'b = "  Duration: 00:00:24.00, start: 0.000000, bitrate: 807 kb/s\\n    Stream #0:0[0x1](und): Video: h264 (High) (avc1 / 0x31637661), yuv420p(tv, bt709, progressive), 516x1032 [SAR 1:1 DAR 1:2], 803 kb/s, 30 fps, 30 tbr, 15360 tbn (default)\\n    Stream #0:1[0x2](eng): Audio: aac (LC) (mp4a / 0x6134706D), 48000 Hz, stereo, fltp, 316 kb/s"',
    'print(json.dumps(media_qc.parse_banner(b)))',
  ].join('\n');
  const r = spawnSync(PY, ['-c', code], { cwd: path.dirname(QC), encoding: 'utf8', env });
  assert.equal(r.status, 0, r.stderr);
  const parsed = JSON.parse(r.stdout);
  assert.equal(parsed.duration_s, 24);
  assert.deepEqual([parsed.video.codec, parsed.video.width, parsed.video.height, parsed.video.fps, parsed.video.pix_fmt], ['h264', 516, 1032, 30, 'yuv420p']);
  assert.equal(parsed.audio.length, 1);
  const verdict = spawnSync(PY, ['-c', 'import json, media_qc; print(json.dumps([media_qc.loop_verdict(0.95, [0.99]*50)["ok"], media_qc.loop_verdict(0.995, [0.99]*50)["ok"]]))'], { cwd: path.dirname(QC), encoding: 'utf8', env });
  assert.deepEqual(JSON.parse(verdict.stdout), [false, true]);
});

// ------------------------------------------------------------ sfx_place.py
test('SFX cue sheet plans frame-accurate delays and rejects cues after the end', async t => {
  const dir = await temp(t);
  await wav(path.join(dir, 'whoosh.wav'), 0.5);
  await writeFile(path.join(dir, 'cues.csv'), 'time,file,gain_db,fade_in,length,label\n0.5,whoosh.wav,-6,0.05,0.5,first\nf60,whoosh.wav,,,,second\n00:00:03:15,whoosh.wav,-3,,,third\n');
  const plan = out(py(SFX, ['--cues', path.join(dir, 'cues.csv'), '--duration', '5', '--fps', '30', '--out', path.join(dir, 'stem.wav'), '--dry-run']));
  assert.deepEqual(plan.cues.map(c => c.time_s), [0.5, 2, 3.5]);
  const graph = plan.command[plan.command.indexOf('-filter_complex') + 1];
  for (const part of ['adelay=delays=500:all=1', 'adelay=delays=2000:all=1', 'adelay=delays=3500:all=1', 'amix=inputs=3:normalize=0', 'apad=whole_dur=5']) assert.ok(graph.includes(part), part);
  await writeFile(path.join(dir, 'late.csv'), 'time,file\n9,whoosh.wav\n');
  assert.equal(py(SFX, ['--cues', path.join(dir, 'late.csv'), '--duration', '5', '--out', path.join(dir, 'x.wav'), '--dry-run']).status, 2);
  await writeFile(path.join(dir, 'frames.csv'), 'time,file\nf10,whoosh.wav\n');
  assert.equal(py(SFX, ['--cues', path.join(dir, 'frames.csv'), '--duration', '5', '--out', path.join(dir, 'y.wav'), '--dry-run']).status, 2);
});

// ------------------------------------------------------------- srt_check.py
test('SRT checker flags timing, length and French spacing, and fixes into a new file only', async t => {
  const dir = await temp(t);
  const srt = path.join(dir, 'fr.srt');
  const source = '1\n00:00:01,000 --> 00:00:03,000\nBonjour : notre offre !\nDès 2 450 $\n\n2\n00:00:02,900 --> 00:00:04,000\nUne ligne beaucoup trop longue pour un seul sous-titre de diffusion\n\n3\n00:00:05,000 --> 00:00:06,500\nRendez-vous à 10:30.\n';
  await writeFile(srt, source, 'utf8');
  const r = py(SRT, [srt, '--french', 'fr-CA']);
  assert.equal(r.status, 1);
  const rules = new Set(out(r).issues.map(i => i.rule));
  for (const rule of ['overlap', 'line-too-long', 'breakable-space-before-punctuation', 'breakable-space-in-number']) assert.ok(rules.has(rule), rule);
  assert.ok(!out(r).issues.some(i => i.cue === 3 && i.rule === 'missing-space-before-colon'), 'times like 10:30 are not punctuation');
  const fixed = path.join(dir, 'fr_fixed.srt');
  const f = py(SRT, [srt, '--french', 'fr-CA', '--fix-french-out', fixed]);
  assert.equal(out(f).fixed_copy.remaining, 0);
  const text = await readFile(fixed, 'utf8');
  assert.ok(text.includes('Bonjour\u00a0: notre offre\u00a0!'));
  assert.ok(text.includes('2\u00a0450\u00a0$'));
  assert.equal(await readFile(srt, 'utf8'), source);
  assert.equal(py(SRT, [srt, '--french', 'fr-CA', '--fix-french-out', srt]).status, 2);
});

// ------------------------------------------------- FFmpeg integration tests
test('LED export, check, media QC and SFX render work end to end', { skip: !FFMPEG && 'FFmpeg unavailable' }, async t => {
  const dir = await temp(t);
  const master = path.join(dir, 'master.mp4');
  const gen = spawnSync(FFMPEG, ['-hide_banner', '-loglevel', 'error', '-f', 'lavfi', '-i', 'testsrc2=size=1032x2064:rate=30:duration=2', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', master], { encoding: 'utf8', timeout: 120000 });
  assert.equal(gen.status, 0, gen.stderr);
  const exported = path.join(dir, 'CLIENT_MSG_516x1032_30p_v01.mp4');
  const e = py(LED, ['export', '--profile', 'led-rollup-516x1032', '--input', master, '--output', exported], { env: { ...env, FFMPEG } });
  assert.equal(e.status, 0, e.stdout);
  const c = out(py(LED, ['check', '--profile', 'led-rollup-516x1032', '--input', exported], { env: { ...env, FFMPEG } }));
  assert.equal(c.ok, true, JSON.stringify(c.checks));
  const sheet = path.join(dir, 'sheet.jpg');
  const q = py(QC, [exported, '--expect-width', '516', '--expect-height', '1032', '--expect-fps', '30', '--expect-frames', '60', '--expect-audio', 'no', '--contact-sheet', sheet], { env: { ...env, FFMPEG } });
  assert.equal(q.status, 0, q.stdout);
  assert.equal(out(q).video.decoded_frames, 60);
  assert.ok((await stat(sheet)).size > 0);
  await wav(path.join(dir, 'hit.wav'), 0.3, 2);
  await writeFile(path.join(dir, 'cues.csv'), 'time,file\nf15,hit.wav\n');
  const stem = path.join(dir, 'stem.wav');
  const s = py(SFX, ['--cues', path.join(dir, 'cues.csv'), '--duration', '2', '--fps', '30', '--out', stem], { env: { ...env, FFMPEG } });
  assert.equal(s.status, 0, s.stdout);
  const bytes = await readFile(stem);
  assert.equal(bytes.subarray(0, 4).toString(), 'RIFF');
  const expected = 2 * 48000 * 2 * 3;   // seconds x rate x channels x 24-bit
  assert.ok(Math.abs(bytes.length - expected) < 4096, `${bytes.length} vs ${expected}`);
});
