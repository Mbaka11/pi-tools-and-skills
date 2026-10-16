#!/usr/bin/env node
// Explicit integration entry point. Checks prerequisites; never installs them.
import { spawnSync } from 'node:child_process';
import { readdirSync } from 'node:fs';
import path from 'node:path';
import { ROOT } from './upstreams.mjs';

const args = process.argv.slice(2);
if (args.some(a => a !== '--preflight-only') || args.length > 1) {
  console.error('Usage: node scripts/test-media.mjs [--preflight-only]');
  process.exit(2);
}
const python = process.env.PYTHON || 'python';
const preflight = String.raw`
import importlib.util, json, os, shutil, subprocess, sys
try:
 from PIL import Image, ImageFont, __version__ as pillow_version
except ImportError:
 raise SystemExit('Pillow is required for mandatory media tests; nothing was installed.')
ffmpeg = os.environ.get('FFMPEG') or shutil.which('ffmpeg')
if not ffmpeg and importlib.util.find_spec('imageio_ffmpeg'):
 import imageio_ffmpeg
 ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
ffprobe = os.environ.get('FFPROBE') or shutil.which('ffprobe')
for name, exe in [('FFmpeg', ffmpeg), ('ffprobe', ffprobe)]:
 if not exe or not shutil.which(exe):
  raise SystemExit(name + ' is required for mandatory media tests; nothing was installed.')
def call(exe, args):
 r = subprocess.run([exe, *args], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=20)
 if r.returncode:
  raise SystemExit('A required media-engine preflight failed.')
 return r.stdout + r.stderr
filters = call(ffmpeg, ['-hide_banner', '-filters'])
for name in ['afftdn', 'colorchannelmixer', 'scdet', 'metadata', 'fps', 'hstack', 'concat', 'setpts', 'ebur128']:
 if name not in filters:
  raise SystemExit('Missing required FFmpeg filter: ' + name)
if 'libx264' not in call(ffmpeg, ['-hide_banner', '-encoders']):
 raise SystemExit('FFmpeg libx264 encoder is required.')
if 'framehash' not in call(ffmpeg, ['-hide_banner', '-muxers']):
 raise SystemExit('FFmpeg framehash muxer is required.')
if not hasattr(Image, 'Resampling'):
 raise SystemExit('Pillow >= 9.2 is required.')
font = None
for candidate in ([os.environ['TOOLBOX_FONT']] if os.environ.get('TOOLBOX_FONT') else ['DejaVuSans.ttf', 'arial.ttf']):
 try:
  ImageFont.truetype(candidate, 18); font = candidate; break
 except OSError: pass
if not font:
 raise SystemExit('A licensed local TrueType font is required; set TOOLBOX_FONT.')
print(json.dumps({'ffmpeg': ffmpeg, 'ffprobe': ffprobe, 'font': font, 'pillow': pillow_version,
 'ffmpeg_version': call(ffmpeg, ['-version']).splitlines()[0], 'ffprobe_version': call(ffprobe, ['-version']).splitlines()[0]}))
`;
const probe = spawnSync(python, ['-c', preflight], { encoding: 'utf8', timeout: 120000, env: { ...process.env, PYTHONIOENCODING: 'utf-8' } });
if (probe.error || probe.status !== 0) {
  console.error(probe.error ? 'Python/media preflight could not start.' : probe.stderr.trim());
  process.exit(2);
}
let info;
try { info = JSON.parse(probe.stdout); }
catch { console.error('Invalid media preflight response.'); process.exit(2); }
console.log(JSON.stringify({ mandatoryMediaTests: true, ffmpeg: info.ffmpeg_version, ffprobe: info.ffprobe_version, pillow: info.pillow, font: path.basename(info.font), installsDependencies: false }));
if (!args.includes('--preflight-only')) {
  const env = { ...process.env, REQUIRE_MEDIA_TESTS: '1', FFMPEG: info.ffmpeg, FFPROBE: info.ffprobe,
    TOOLBOX_FONT: info.font, PYTHONDONTWRITEBYTECODE: '1', PYTHONIOENCODING: 'utf-8' };
  const tests = readdirSync(path.join(ROOT, 'tests')).filter(f => f.endsWith('.test.mjs')).sort().map(f => `tests/${f}`);
  for (const command of [['scripts/check.mjs'], ['--test', ...tests]]) {
    const result = spawnSync(process.execPath, command, { cwd: ROOT, env, stdio: 'inherit', timeout: 600000 });
    if (result.error || result.status !== 0) process.exit(result.status || 1);
  }
}
