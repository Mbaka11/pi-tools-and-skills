#!/usr/bin/env python3
"""Build tiny ORIGINAL synthetic examples into a NEW directory (never a client project).

Optional regeneration dependencies: Pillow >= 9.2 and FFmpeg with libx264.
No downloads, paid models, Adobe automation or third-party pipeline execution.
The committed gallery can be viewed without any of these dependencies.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import random
import shutil
import struct
import subprocess
import sys
import wave

ROOT = Path(__file__).resolve().parent.parent
FPS, SECONDS = 10, 3
W, H = 480, 270
PAPER, INK, YELLOW, TEAL = '#eee8db', '#1c2934', '#f6c945', '#63c6c4'


def dump(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def run(command, cwd=None, expected=(0,)):
    env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    r = subprocess.run([str(v) for v in command], cwd=cwd, env=env, capture_output=True,
                       text=True, encoding='utf-8', errors='replace', timeout=120)
    if r.returncode not in expected:
        raise RuntimeError(f'{Path(command[0]).name} failed ({r.returncode}): {r.stderr[-1200:]} {r.stdout[-1200:]}')
    return r.stdout


def tool(rel, args, cwd, expected=(0,)):
    return json.loads(run([sys.executable, ROOT / rel, *args], cwd, expected))


def ffmpeg_path():
    candidate = os.environ.get('FFMPEG') or shutil.which('ffmpeg')
    if candidate:
        return candidate
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        raise RuntimeError('FFmpeg unavailable; set FFMPEG or add ffmpeg to PATH. Nothing was installed.')


def build(out, ffmpeg, font_path):
    from PIL import Image, ImageDraw, ImageFont, __version__ as pillow_version
    fonts = {}

    def font(size):
        if size not in fonts:
            fonts[size] = ImageFont.truetype(font_path, size)
        return fonts[size]

    def text(im, xy, value, size=18, fill=INK, anchor=None):
        ImageDraw.Draw(im).text(xy, value, font=font(size), fill=fill, anchor=anchor)

    def ease(v):
        v = min(1, max(0, v))
        return v * v * (3 - 2 * v)

    def base(number, title, dark=False, native_mock=False):
        im = Image.new('RGB', (W, H), INK if dark else PAPER)
        d = ImageDraw.Draw(im)
        fg = PAPER if dark else INK
        d.line((24, 40, W - 24, 40), fill=fg, width=1)
        text(im, (24, 16), f'{number} / {title}', 12, fg)
        text(im, (24, 246), 'MAQUETTE - PAS UN RENDU AE' if native_mock else 'DEMO SYNTHETIQUE / 3 SECONDES', 10, fg)
        return im

    # Static procedural texture: no downloaded paper, photo, font file or logo.
    grain = Image.new('RGB', (W, H), PAPER)
    gd = ImageDraw.Draw(grain)
    rng = random.Random(42)
    for _ in range(900):
        x, y = rng.randrange(W), rng.randrange(H)
        gd.point((x, y), fill='#dcd6ca')

    def vox(t):
        im = grain.copy()
        d = ImageDraw.Draw(im)
        text(im, (24, 16), '01 / COLLAGE EDITORIAL', 12)
        d.line((24, 40, 456, 40), fill=INK)
        y = round(72 + 25 * (1 - ease(t / .5)))
        text(im, (24, y), 'UNE IDEE', 40)
        p = ease((t - .35) / .5)
        d.rectangle((24, 128, 24 + round(262 * p), 161), fill=YELLOW)
        text(im, (29, 129), 'PREND FORME', 29)
        text(im, (26, 195), 'Papier. Relief. Mouvement.', 15)
        card = Image.new('RGBA', (139, 161), (0, 0, 0, 0))
        c = ImageDraw.Draw(card)
        c.polygon([(3, 4), (132, 0), (137, 149), (127, 156), (113, 150), (99, 160), (80, 153), (61, 158), (3, 154)], fill='#fffaf0')
        c.polygon([(20, 105), (42, 55), (64, 82), (89, 32), (120, 105)], fill=TEAL)
        c.line([(20, 118), (53, 92), (80, 118), (117, 72)], fill=INK, width=4)
        for x, yy in [(20, 118), (53, 92), (80, 118), (117, 72)]:
            c.ellipse((x - 5, yy - 5, x + 5, yy + 5), fill=YELLOW, outline=INK, width=2)
        card = card.rotate(3 + (int(t * 5) % 2), resample=Image.Resampling.BICUBIC, expand=True)
        im.paste(card, (309, round(66 + 20 * (1 - ease((t - .1) / .6)))), card)
        text(im, (24, 246), 'MAQUETTE - PAS UN RENDU AE', 10)
        return im

    def rig(t):
        im = base('02', 'BOITE AUTO / TEXTE MODIFIABLE', True, True)
        d = ImageDraw.Draw(im)
        phrase = 'Bonjour' if t < 1.5 else 'Bonjour le monde'
        b = d.textbbox((0, 0), phrase, font=font(28))
        width = b[2] - b[0] + 36
        x = (W - width) // 2
        for xx in (24, W - 24):
            d.line((xx, 65, xx, 220), fill='#52616b')
        d.rounded_rectangle((x, 108, x + width, 170), radius=9, fill=TEAL)
        text(im, (W / 2, 139), phrase, 28, INK, 'mm')
        d.line((x, 190, x + width, 190), fill=YELLOW, width=2)
        for xx in (x, x + width):
            d.line((xx, 185, xx, 195), fill=YELLOW, width=2)
        text(im, (W / 2, 210), 'Largeur = texte + 36 px', 16, PAPER, 'mm')
        return im

    def vfx(t):
        im = base('03', 'REMPLACEMENT D\'ECRAN', False, True)
        d = ImageDraw.Draw(im)
        d.rectangle((24, 58, 456, 230), fill='#cbd0d0')
        d.polygon([(24, 180), (456, 175), (456, 230), (24, 230)], fill='#999f9d')
        d.ellipse((157, 205, 337, 222), fill='#777f7f')
        outer = [(181, 65), (309, 79), (303, 210), (175, 199)]
        inner = [(187, 72), (302, 85), (296, 203), (182, 194)]
        d.polygon(outer, fill=INK)
        d.polygon(inner, fill='#37414a')
        # A synthetic planar plate; no tracking or camera solve is claimed.
        insert = Image.new('RGB', (110, 120), '#123f4a')
        ii = ImageDraw.Draw(insert)
        ii.ellipse((55, -18, 135, 62), fill=TEAL)
        text(insert, (12, 54), 'IDEES', 24, PAPER)
        text(insert, (12, 82), 'EN VUE', 20, YELLOW)
        overlay = insert.transform((W, H), Image.Transform.AFFINE,
                                   (1, .043, -190, -.112, 1, -51), Image.Resampling.BICUBIC)
        mask = Image.new('L', (W, H), 0)
        ImageDraw.Draw(mask).polygon(inner, fill=255)
        reveal = Image.new('L', (W, H), 0)
        edge = int(170 + 145 * ease((t - .6) / 1.0))
        ImageDraw.Draw(reveal).rectangle((0, 0, edge, H), fill=255)
        from PIL import ImageChops
        im.paste(overlay, (0, 0), ImageChops.multiply(mask, reveal))
        text(im, (37, 70), 'AVANT' if t < .6 else 'APRES', 15)
        text(im, (328, 193), 'Plate fictif', 12)
        return im

    def edit(t):
        im = base('06', 'MONTAGE / LARGE > DETAIL > TITRE', True)
        d = ImageDraw.Draw(im)
        phase = min(2, int(t))
        if phase == 0:
            d.polygon([(30, 210), (145, 75), (255, 210)], fill=TEAL)
            d.ellipse((284, 77, 408, 201), fill=YELLOW)
            caption = '01 / CONTEXTE'
        elif phase == 1:
            d.ellipse((75, 65, 385, 375), fill=YELLOW)
            d.polygon([(225, 50), (440, 50), (440, 222)], fill=TEAL)
            caption = '02 / DETAIL'
        else:
            text(im, (240, 130), 'VOIR AUTREMENT', 34, PAPER, 'mm')
            d.rectangle((110, 160, 370, 166), fill=YELLOW)
            caption = '03 / CONCLUSION'
        d.rectangle((24, 214, 456, 238), fill=INK)
        text(im, (33, 219), caption, 12, PAPER)
        d.rectangle((0, 239, W, H), fill=INK)
        text(im, (24, 246), 'DEMO SYNTHETIQUE / 3 SECONDES', 10, PAPER)
        return im

    def pipeline(t):
        im = base('07', 'MICRO EXPLAINER / TROIS BEATS')
        d = ImageDraw.Draw(im)
        phase = min(2, int(t))
        titles = ['UNE QUESTION', 'UN INDICE', 'UNE REPONSE']
        text(im, (240, 85), titles[phase], 30, INK, 'mm')
        nodes = [(90, 169), (240, 169), (390, 169)]
        d.line([nodes[0], nodes[2]], fill=INK, width=3)
        for i, (x, y) in enumerate(nodes):
            r = 29 if i == phase else 19
            d.ellipse((x-r, y-r, x+r, y+r), fill=YELLOW if i == phase else TEAL, outline=INK, width=3)
            text(im, (x, y), str(i + 1), 22, INK, 'mm')
        text(im, (240, 218), 'Storyboard anime, sans voix generee', 14, INK, 'mm')
        return im

    media = out / 'media'
    outputs = out / 'outputs'
    scratch = out / 'work'
    for folder in (media, outputs, scratch):
        folder.mkdir(parents=True)
    for name, scene in [('ae-vox', vox), ('ae-rig', rig), ('ae-vfx', vfx), ('editing', edit), ('explainer', pipeline)]:
        frames = [scene(n / FPS) for n in range(FPS * SECONDS)]
        # Shared fixed palette avoids GIF colour flicker and keeps previews small.
        palette = frames[len(frames)//2].quantize(colors=96)
        indexed = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
        indexed[0].save(media / f'{name}.gif', save_all=True, append_images=indexed[1:],
                        duration=1000 // FPS, loop=0, optimize=True, disposal=2)
        frames[15].save(scratch / f'{name}-still.png')
    # A genuinely rendered/checked LED loop, authored at the reference pixel map.
    for n in range(90):
        im = Image.new('RGB', (516, 1032), INK)
        d = ImageDraw.Draw(im)
        d.rectangle((32, 44, 484, 50), fill=TEAL)
        text(im, (46, 90), 'UNE IDEE.', 64, PAPER)
        text(im, (46, 170), 'BIEN VISIBLE.', 49, YELLOW)
        text(im, (46, 269), 'Une boucle. Un message.', 29, PAPER)
        cx = round(258 + 58 * math.sin(2 * math.pi * n / 90))
        cy = round(536 + 25 * math.cos(2 * math.pi * n / 90))
        d.ellipse((cx-108, cy-108, cx+108, cy+108), fill=TEAL)
        d.rounded_rectangle((cx-55, cy-72, cx+55, cy+72), radius=12, fill=INK)
        d.line((cx-25, cy-10, cx, cy+20, cx+34, cy-32), fill=YELLOW, width=12)
        text(im, (258, 748), 'DEMO GENERIQUE', 32, PAPER, 'mm')
        text(im, (258, 817), '516 x 1032 / 30 fps / sans son', 22, PAPER, 'mm')
        im.save(scratch / f'led-{n:03}.png')
    run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-nostdin', '-n', '-framerate', '30',
         '-i', 'work/led-%03d.png', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', 'work/master.mp4'], out)
    led = 'skills/montage/led-signage-content/scripts/led_tool.py'
    qc = 'skills/montage/video-delivery-qc/scripts/media_qc.py'
    sfx = 'skills/montage/sound-design-sfx/scripts/sfx_place.py'
    srt = 'skills/montage/montage-editing-craft/scripts/srt_check.py'
    tool(led, ['export', '--profile', 'led-rollup-516x1032', '--input', 'work/master.mp4', '--output', 'media/led-loop.mp4'], out)
    report = tool(led, ['check', '--profile', 'led-rollup-516x1032', '--input', 'media/led-loop.mp4'], out)
    assert report['ok']
    dump(outputs / 'led-check.json', report)
    dump(outputs / 'text-size.json', tool(led, ['text-size', '--profile', 'led-rollup-516x1032', '--distance', '4'], out))
    tool(led, ['guides', '--profile', 'led-wall-3x-516x1032', '--out', 'media/led-guides.png'], out)
    tool(led, ['testcard', '--profile', 'led-rollup-516x1032', '--out-png', 'media/led-testcard.png'], out)
    # Lower-resolution browsing preview is explicitly NOT the delivery file.
    still = Image.open(scratch / 'led-015.png')
    still.resize((258, 516), Image.Resampling.LANCZOS).save(media / 'led-poster.png')
    report = tool(qc, ['media/led-loop.mp4', '--expect-width', '516', '--expect-height', '1032',
                      '--expect-fps', '30', '--expect-frames', '90', '--expect-audio', 'no', '--loop-check',
                      '--contact-sheet', 'media/qc-contact.png', '--cols', '3', '--rows', '1', '--tile-width', '150'], out)
    assert report['ok'], report['checks']
    dump(outputs / 'media-qc.json', report)
    # Three original sounds: noise sweep, low hit, two-note chime. No recordings.
    sr = 48000
    rng = random.Random(7)
    for name, duration in [('sweep', .5), ('hit', .35), ('chime', .65)]:
        samples = bytearray()
        for n in range(round(sr * duration)):
            t = n / sr
            if name == 'sweep':
                val = .22 * rng.uniform(-1, 1) * math.sin(math.pi * t / duration) ** 2
            elif name == 'hit':
                val = .55 * math.sin(2 * math.pi * (80 * t + 20 * (1-math.exp(-12*t)))) * math.exp(-15*t) * min(1, t/.003)
            else:
                val = .22 * (math.sin(2*math.pi*660*t) + .6*math.sin(2*math.pi*990*t)) * math.exp(-6*t) * min(1, t/.008)
            val *= min(1, (duration - t) / .015)
            samples.extend(struct.pack('<h', round(max(-1, min(1, val)) * 32767)))
        with wave.open(str(scratch / f'{name}.wav'), 'wb') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sr)
            wav.writeframes(samples)
    (scratch / 'cues.csv').write_text('time,file,gain_db,fade_in,fade_out,length,label\nf9,sweep.wav,-3,0.01,0.02,0.5,reveal\nf30,hit.wav,-3,0.005,0.03,0.35,cut\nf60,chime.wav,-3,0.01,0.03,0.65,resolve\n', encoding='utf-8')
    result = tool(sfx, ['--cues', 'work/cues.csv', '--duration', '3', '--fps', '30', '--out', 'media/sfx.wav'], out)
    assert result['returncode'] == 0
    dump(outputs / 'sfx-cues.json', {'kind': 'measured-excerpt', 'duration_s': result['duration_s'],
         'sample_rate': result['sample_rate'], 'cues': [{'time_s': c['time_s'], 'frame': c['frame'], 'label': c['label']} for c in result['cues']],
         'human_audio_audition': False, 'note': 'Command and temporary absolute input paths omitted.'})
    dump(outputs / 'sfx-qc.json', tool(qc, ['media/sfx.wav', '--true-peak-max', '-1'], out))
    run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-nostdin', '-n', '-i', 'media/editing.gif',
         '-i', 'media/sfx.wav', '-map', '0:v:0', '-map', '1:a:0', '-t', '3', '-vf', 'fps=30,format=yuv420p',
         '-c:v', 'libx264', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', 'media/sfx-preview.mp4'], out)
    # Real subtitle check/fix. The input errors are intentional.
    shutil.copyfile(ROOT / 'examples/fixtures/captions.srt', scratch / 'captions.srt')
    result = tool(srt, ['work/captions.srt', '--french', 'fr-CA', '--fix-french-out', 'outputs/captions-fixed.srt'], out, (1,))
    dump(outputs / 'captions-before.json', result)
    result = tool(srt, ['outputs/captions-fixed.srt', '--french', 'fr-CA'], out)
    assert result['errors'] == 0
    dump(outputs / 'captions-after.json', result)
    # The manifest helper verifies bytes; this fixture is deliberately not an AEP.
    shutil.copyfile(ROOT / 'examples/fixtures/canonical.txt', outputs / 'canonical.txt')
    fixture = (outputs / 'canonical.txt').read_bytes()
    digest = hashlib.sha256(fixture).hexdigest()
    dump(outputs / 'delivery-manifest.json', {'canonical': 'canonical.txt', 'canonical_sha256': digest,
         'files': [{'path': 'canonical.txt', 'size': len(fixture), 'sha256': digest}]})
    result = tool('skills/after-effects/ae-production-workflow/scripts/verify-delivery-manifest.py',
                  ['delivery-manifest.json', '--root', '.'], outputs)
    assert result['ok']
    # Paths are deliberately normalized; numerical results are unmodified.
    result.update(manifest='delivery-manifest.json', root='.')
    dump(outputs / 'delivery-check.json', result)
    api = json.loads(run(['node', ROOT / 'skills/reverse-api-investigation/scripts/har-summary.mjs',
                          ROOT / 'examples/fixtures/request-events.json'], out))
    dump(outputs / 'api-summary.json', api)
    dump(outputs / 'build-info.json', {'synthetic': True, 'pillow': pillow_version,
         'font_family': font(18).getname()[0], 'ffmpeg': run([ffmpeg, '-version']).splitlines()[0],
         'native_ae_render': False, 'upstream_pipeline_executed': False, 'cloud_requests': 0,
         'human_audio_audition': False, 'normalization': 'Only private/temporary file paths are omitted or made relative.'})
    media_meta = {}
    for p in sorted(media.iterdir()):
        data = p.read_bytes()
        item = {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data), 'origin': 'original-synthetic',
                'generator': 'examples/build.py', 'license': 'UNLICENSED'}
        if p.suffix in ('.gif', '.png'):
            with Image.open(p) as im:
                item.update(width=im.width, height=im.height)
                if p.suffix == '.gif':
                    duration = 0
                    for n in range(im.n_frames):
                        im.seek(n)
                        duration += im.info.get('duration', 0)
                    item.update(duration_s=duration/1000, frames=im.n_frames)
        elif p.suffix in ('.mp4', '.wav'):
            item['duration_s'] = 3
        media_meta['examples/media/' + p.name] = item
    dump(out / 'media-manifest.json', media_meta)
    print(json.dumps({'ok': True, 'output': str(out), 'media_files': len(media_meta),
                      'total_media_bytes': sum(v['bytes'] for v in media_meta.values())}))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', required=True, help='NEW output directory, preferably .local/examples-preview')
    ap.add_argument('--font', help='Licensed font available on this machine; not copied or embedded')
    args = ap.parse_args()
    out = Path(args.out).resolve()
    if out.exists():
        ap.error('Output already exists. Choose a new directory; nothing will be overwritten.')
    if ROOT in out.parents and ROOT / '.local' not in out.parents:
        ap.error('Inside this repository, generate only under .local; review before copying into examples/.')
    try:
        from PIL import ImageFont
        exe = ffmpeg_path()
        os.environ['FFMPEG'] = exe
        choices = [args.font] if args.font else ['DejaVuSans.ttf', 'arial.ttf']
        chosen = None
        for choice in choices:
            try:
                ImageFont.truetype(choice, 18)
                chosen = choice
                break
            except OSError:
                pass
        if not chosen:
            raise RuntimeError('No usable font. Pass --font with a licensed TTF available locally.')
        build(out, exe, chosen)
    except (ImportError, RuntimeError) as e:
        ap.exit(2, str(e) + '\n')


if __name__ == '__main__':
    main()
