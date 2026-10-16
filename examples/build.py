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
    # Stable LF bytes also make file-integrity examples portable across checkouts.
    path.write_bytes((json.dumps(data, indent=2, ensure_ascii=False) + '\n').encode('utf-8'))


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


def build(out, ffmpeg, font_path, example_set='all'):
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
    if example_set in ('montage', 'editorial'):
        (build_montage if example_set == 'montage' else build_editorial)(out, ffmpeg, font_path)
        record_media(out)
        return
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
    if example_set == 'all':
        build_montage(out, ffmpeg, font_path)
        build_editorial(out, ffmpeg, font_path)
    record_media(out)


def record_media(out):
    from PIL import Image
    media_meta = {}
    for p in sorted((out / 'media').iterdir()):
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


def build_montage(out, ffmpeg, font_path):
    """Five original filter/workflow proofs; no native Adobe or speech claims."""
    from PIL import Image, ImageDraw, ImageFont, __version__ as pillow_version
    media, outputs, work = out / 'media', out / 'outputs', out / 'work'
    qc = 'skills/montage/video-delivery-qc/scripts/media_qc.py'
    fonts = {}

    def text(im, xy, value, size=14, fill=PAPER):
        if size not in fonts:
            fonts[size] = ImageFont.truetype(font_path, size)
        ImageDraw.Draw(im).text(xy, value, font=fonts[size], fill=fill)

    def ff(args):
        return run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-nostdin', '-n', *args], out)

    def encode(pattern, fps, frames, target):
        ff(['-framerate', fps, '-i', pattern, '-frames:v', frames, '-an', '-c:v', 'libx264',
            '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', target])

    def extracted(source, indices, label):
        expression = '+'.join(f'eq(n\\,{n})' for n in indices)
        ff(['-i', source, '-vf', f'select={expression}', '-vsync', '0', f'work/{label}-%02d.png'])
        result = []
        for i in range(1, len(indices) + 1):
            with Image.open(work / f'{label}-{i:02}.png') as image:
                result.append(image.convert('RGB'))
        return result

    def sha(file):
        return hashlib.sha256(file.read_bytes()).hexdigest()

    # Known RGB arithmetic, NOT a camera log/LUT or HDR demonstration.
    reference = Image.new('RGB', (144, 144))
    patches = [(32, 32, 32), (80, 80, 80), (160, 160, 160), (180, 90, 70),
               (50, 150, 175), (145, 100, 165), (180, 165, 70), (65, 100, 170), (110, 145, 100)]
    d = ImageDraw.Draw(reference)
    for i, colour in enumerate(patches):
        x, y = (i % 3) * 48, (i // 3) * 48
        d.rectangle((x, y, x + 47, y + 47), fill=colour)
    reference.save(work / 'colour-reference.png')
    tinted = reference.copy()
    tinted.putdata([(round(r * 1.2), g, round(b * .8)) for r, g, b in reference.getdata()])
    tinted.save(work / 'colour-tinted.png')
    colour_filter = 'format=rgb24,colorchannelmixer=rr=0.833333333333:bb=1.25'
    ff(['-i', 'work/colour-tinted.png', '-vf', colour_filter, '-frames:v', '1',
        '-pix_fmt', 'rgb24', 'work/colour-corrected.png'])
    with Image.open(work / 'colour-corrected.png') as image:
        corrected = image.convert('RGB')

    def pixel_error(image):
        errors = [abs(a - b) for p, q in zip(reference.getdata(), image.getdata()) for a, b in zip(p, q)]
        return {'mean_absolute_error_8bit': round(sum(errors) / len(errors), 6), 'max_error_8bit': max(errors)}

    before, after = pixel_error(tinted), pixel_error(corrected)
    assert after['mean_absolute_error_8bit'] < before['mean_absolute_error_8bit']
    assert after['max_error_8bit'] <= 1
    board = Image.new('RGB', (480, 240), INK)
    text(board, (16, 12), 'COLOUR / KNOWN RGB GAIN ERROR', 17)
    for x, image, label in [(16, reference, 'Reference'), (168, tinted, 'Tinted'), (320, corrected, 'Corrected')]:
        text(board, (x, 42), label)
        board.paste(image, (x, 64))
    text(board, (16, 220), 'RGB math only - not a camera LUT or display calibration.', 12)
    board.save(media / 'colour-comparison.png')
    dump(outputs / 'colour-check.json', {'kind': 'measured-synthetic-rgb-test', 'filter': colour_filter,
         'before': before, 'after': after, 'native_grade': False,
         'not_verified': ['camera log or HDR transform', 'skin tones', 'calibrated monitor accuracy']})

    # Small source/proxy pair. H.264 chosen for gallery size, not universal editing performance.
    for n in range(90):
        im = Image.new('RGB', (640, 360), INK)
        d = ImageDraw.Draw(im)
        text(im, (24, 20), 'ORIGINAL SYNTHETIC SOURCE', 24)
        text(im, (24, 60), f'FRAME {n:03d} / 30 fps / 640 x 360', 18)
        for x in range(24, 617, 16):
            d.line((x, 115, x, 290), fill='#334958', width=1)
        cx = round(60 + 520 * n / 89)
        d.ellipse((cx - 28, 165, cx + 28, 221), fill=TEAL)
        d.rectangle((24, 290, 616, 294), fill=YELLOW)
        text(im, (24, 319), 'Same timing, lower raster - not a native attachment test', 16)
        im.save(work / f'proxy-source-{n:03}.png')
    encode('work/proxy-source-%03d.png', 30, 90, 'media/proxy-source.mp4')
    ff(['-i', 'media/proxy-source.mp4', '-vf', 'scale=320:180:flags=lanczos', '-an',
        '-c:v', 'libx264', '-crf', '26', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', 'media/proxy-small.mp4'])
    original_frame = extracted('media/proxy-source.mp4', [45], 'source-preview')[0]
    proxy_frame = extracted('media/proxy-small.mp4', [45], 'proxy-preview')[0]
    board = Image.new('RGB', (660, 250), INK)
    text(board, (8, 12), 'SOURCE / 640 x 360', 16)
    text(board, (338, 12), 'PROXY / 320 x 180', 16)
    board.paste(original_frame.resize((320, 180), Image.Resampling.LANCZOS), (8, 42))
    board.paste(proxy_frame, (338, 42))
    text(board, (8, 231), 'Decoded frame 45 in both files. Native attachment / relink not tested.', 13)
    board.save(media / 'proxy-comparison.png')

    # Calculator output and an actual zero-offset working preview from synthetic camera frames.
    anchor_script = 'skills/montage/montage-multicam-sync/scripts/sync_map.py'
    anchor_fixture = ROOT / 'skills/montage/montage-multicam-sync/assets/anchors.example.json'
    sync = tool(anchor_script, [anchor_fixture], out)
    assert sync['offset_fraction'] == '-1/5' and sync['scale_fraction'] == '1'
    dump(outputs / 'sync-map.json', sync)
    for camera, count in [('a', 90), ('b', 96)]:
        for n in range(count):
            world_frame = n if camera == 'a' else n - 6
            im = Image.new('RGB', (320, 180), INK)
            d = ImageDraw.Draw(im)
            text(im, (12, 10), 'REFERENCE A' if camera == 'a' else 'CAMERA B', 17)
            text(im, (12, 36), f'Source frame {n:03d}', 13)
            cx = round(40 + 240 * max(0, min(89, world_frame)) / 89)
            if camera == 'b':
                cx = 320 - cx
            colour = YELLOW if world_frame in (15, 75) else TEAL
            d.line((15, 133, 305, 133), fill='#60717e', width=2)
            d.ellipse((cx - 17, 88, cx + 17, 122), fill=colour)
            text(im, (12, 153), 'Synthetic event' if world_frame in (15, 75) else 'Known shared motion', 13, colour)
            im.save(work / f'camera-{camera}-{n:03}.png')
        encode(f'work/camera-{camera}-%03d.png', 30, count, f'work/camera-{camera}.mp4')
    offset_frames = -round(sync['offset_reference_frames'])
    sync_graph = (f'[0:v]trim=start_frame=0:end_frame=90,setpts=PTS-STARTPTS[a];'
                  f'[1:v]trim=start_frame={offset_frames}:end_frame={offset_frames + 90},setpts=PTS-STARTPTS[b];'
                  '[a][b]hstack=inputs=2[v]')
    ff(['-i', 'work/camera-a.mp4', '-i', 'work/camera-b.mp4', '-filter_complex', sync_graph,
        '-map', '[v]', '-an', '-r', '30', '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p',
        '-movflags', '+faststart', 'media/multicam-sync.mp4'])
    samples = extracted('media/multicam-sync.mp4', [15, 45, 75], 'sync-preview')
    board = Image.new('RGB', (640, 594), INK)
    for i, (frame, image) in enumerate(zip([15, 45, 75], samples)):
        text(board, (12, i * 198 + 2), f'OUTPUT FRAME {frame:02d} / B advanced by 6 frames', 12)
        board.paste(image, (0, i * 198 + 18))
    board.save(media / 'multicam-contact.png')
    dump(outputs / 'multicam-proof.json', {'kind': 'synthetic-anchor-driven-trim', 'filter_graph': sync_graph,
         'trimmed_camera_b_frames': offset_frames, 'output_frames': 90,
         'known_source_frame_pairs': [[15, 21], [45, 51], [75, 81]],
         'native_multicam_sequence': False, 'waveform_detection': False})

    # Real piecewise retiming: 3.5 seconds at 60 fps -> 3 seconds at 30 fps.
    segments = [(0, 60, 1), (60, 90, .5), (90, 210, 2)]
    for n in range(210):
        im = Image.new('RGB', (480, 270), INK)
        d = ImageDraw.Draw(im)
        speed = 1 if n < 60 else .5 if n < 90 else 2
        text(im, (20, 16), 'TIME REMAP / PIECEWISE SPEED', 20)
        text(im, (20, 58), f'{speed:g}x SPEED', 30, YELLOW)
        text(im, (20, 104), f'Source frame {n:03d} / captured at 60 fps', 16)
        d.line((35, 176, 445, 176), fill='#60717e', width=3)
        for x in range(35, 446, 41):
            d.line((x, 166, x, 186), fill='#60717e', width=2)
        cx = round(35 + 410 * n / 209)
        d.ellipse((cx - 16, 160, cx + 16, 192), fill=TEAL)
        text(im, (20, 228), 'Actual FFmpeg retime / no optical flow', 16)
        im.save(work / f'retime-source-{n:03}.png')
    encode('work/retime-source-%03d.png', 60, 210, 'work/retime-source.mp4')
    branches = []
    for i, (start, end, speed) in enumerate(segments):
        branches.append(f'[s{i}]trim=start_frame={start}:end_frame={end},'
                        f'setpts=(PTS-STARTPTS)/{speed:g},fps=30:round=up,setpts=N/(30*TB)[p{i}]')
    retime_graph = '[0:v]split=3[s0][s1][s2];' + ';'.join(branches) + ';[p0][p1][p2]concat=n=3:v=1:a=0[v]'
    # Verify source-frame identity BEFORE the final lossy encode. round=up
    # deliberately keeps each segment's first frame, including source frame 90.
    def frame_hashes(args):
        raw = ff([*args, '-an', '-vsync', '0', '-f', 'framehash', '-hash', 'sha256', '-'])
        return [line.split(',')[-1].strip() for line in raw.splitlines() if line and not line.startswith('#')]
    source_hashes = frame_hashes(['-i', 'work/retime-source.mp4', '-map', '0:v:0'])
    mapped_hashes = frame_hashes(['-i', 'work/retime-source.mp4', '-filter_complex', retime_graph, '-map', '[v]'])
    selected_frames = list(range(0, 60, 2)) + list(range(60, 90)) + list(range(90, 210, 4))
    assert len(source_hashes) == 210 and len(mapped_hashes) == 90
    assert mapped_hashes == [source_hashes[n] for n in selected_frames], 'Unexpected retime source-frame phase'
    # concat uses a neutral timebase; declare the encoder cadence so the final
    # packet also lasts 1/30 s instead of inheriting an effectively zero duration.
    ff(['-i', 'work/retime-source.mp4', '-filter_complex', retime_graph, '-map', '[v]', '-an', '-r', '30',
        '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', 'media/retime.mp4'])
    previews = extracted('media/retime.mp4', list(range(0, 90, 3)), 'retime-preview')
    palette = previews[15].quantize(colors=96)
    indexed = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in previews]
    indexed[0].save(media / 'retime.gif', save_all=True, append_images=indexed[1:], duration=100,
                    loop=0, optimize=True, disposal=2)
    dump(outputs / 'retime-map.json', {'kind': 'executed-piecewise-speed-test', 'source_fps': 60,
         'output_fps': 30, 'source_frames': 210, 'output_frames': 90,
         'segments': [{'source_frames': [a, b], 'speed': speed, 'output_frames': [i * 30, (i + 1) * 30]}
                      for i, (a, b, speed) in enumerate(segments)], 'filter_graph': retime_graph,
         'selected_source_frames': selected_frames,
         'mapping_verified_with': 'decoded-source-vs-filter-output-framehash-sha256-before-encoding',
         'smooth_ramp': False, 'optical_flow': False, 'native_nle_execution': False})

    # Generated bursts + hum + seeded noise, NOT human or synthesized speech.
    sr, sample_count = 48000, 144000
    rng = random.Random(41)
    dry = []
    for n in range(sample_count):
        t = n / sr
        envelope = sum(math.sin(math.pi * (t - a) / (b - a)) ** 2
                       for a, b in [(.5, .95), (1.2, 1.85), (2.1, 2.65)] if a <= t < b)
        tone = envelope * (.16 * math.sin(2 * math.pi * 220 * t) + .07 * math.sin(2 * math.pi * 440 * t)
                           + .04 * math.sin(2 * math.pi * 880 * t))
        noise = .045 * math.sin(2 * math.pi * 60 * t) + .016 * rng.uniform(-1, 1)
        dry.append(round((tone + noise) * 32767))
    with wave.open(str(media / 'dialogue-noisy.wav'), 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sr)
        wav.writeframes(struct.pack(f'<{len(dry)}h', *dry))
    repair_filter = 'highpass=f=80,afftdn=nr=6:nf=-35,apad=whole_len=144000,atrim=end_sample=144000'
    ff(['-i', 'media/dialogue-noisy.wav', '-af', repair_filter, '-c:a', 'pcm_s16le', 'media/dialogue-cleaned.wav'])
    with wave.open(str(media / 'dialogue-cleaned.wav'), 'rb') as wav:
        assert wav.getnframes() == sample_count and wav.getnchannels() == 1 and wav.getframerate() == sr
        clean = list(struct.unpack(f'<{sample_count}h', wav.readframes(sample_count)))

    def noise_rms(values):
        window = values[4800:16800]  # 0.10-0.35 s, known noise-only interval.
        return 20 * math.log10(math.sqrt(sum((v / 32768) ** 2 for v in window) / len(window)))

    noisy_db, clean_db = noise_rms(dry), noise_rms(clean)
    assert clean_db < noisy_db
    board = Image.new('RGB', (480, 306), INK)
    text(board, (18, 12), 'CLEANUP / SYNTHETIC FILTER TEST', 19)
    for row, values, label, colour in [(0, dry, 'BEFORE', YELLOW), (1, clean, 'AFTER', TEAL)]:
        center = 100 + row * 112
        text(board, (18, center - 47), f'{label} / noise-only RMS {noise_rms(values):.1f} dBFS', 14)
        d = ImageDraw.Draw(board)
        d.line((18, center, 462, center), fill='#60717e')
        for x in range(444):
            chunk = values[x * sample_count // 444:(x + 1) * sample_count // 444]
            d.line((18 + x, center - round(max(chunk) / 32768 * 110),
                    18 + x, center - round(min(chunk) / 32768 * 110)), fill=colour)
    text(board, (18, 270), 'No voice. Not loudness-matched. Not human-auditioned.', 12)
    text(board, (18, 288), 'Lower noise is not proof of natural speech quality.', 12)
    board.save(media / 'dialogue-waveform.png')
    dump(outputs / 'dialogue-check.json', {'kind': 'measured-synthetic-noise-test', 'filter': repair_filter,
         'sample_rate': sr, 'channels': 1, 'bits_per_sample': 16, 'samples_per_file': sample_count,
         'noise_window_s': [.1, .35], 'before_noise_rms_dbfs': round(noisy_db, 4),
         'after_noise_rms_dbfs': round(clean_db, 4), 'reduction_db': round(noisy_db - clean_db, 4),
         'before_sha256': sha(media / 'dialogue-noisy.wav'), 'after_sha256': sha(media / 'dialogue-cleaned.wav'),
         'contains_speech': False, 'human_audio_audition': False,
         'not_verified': ['speech intelligibility or identity', 'processing latency', 'loudness-matched listening']})

    reports = {}
    for name, width, height in [('proxy-source', 640, 360), ('proxy-small', 320, 180),
                               ('multicam-sync', 640, 180), ('retime', 480, 270)]:
        report = tool(qc, [f'media/{name}.mp4', '--expect-width', str(width), '--expect-height', str(height),
                          '--expect-fps', '30', '--expect-frames', '90', '--expect-duration', '3', '--expect-audio', 'no'], out)
        assert report['ok'], report['checks']
        reports[name + '.mp4'] = report
    for name in ('dialogue-noisy', 'dialogue-cleaned'):
        report = tool(qc, [f'media/{name}.wav', '--true-peak-max', '-1'], out)
        assert report['ok'], report['checks']
        # Also explicitly decode to EOF; measurements are not a playback audition.
        ff(['-xerror', '-i', f'media/{name}.wav', '-f', 'null', '-'])
        reports[name + '.wav'] = report
    dump(outputs / 'montage-qc.json', reports)
    dump(outputs / 'proxy-check.json', {'kind': 'measured-synthetic-proxy-pair',
         'source_sha256': reports['proxy-source.mp4']['sha256'], 'proxy_sha256': reports['proxy-small.mp4']['sha256'],
         'source_raster': [640, 360], 'proxy_raster': [320, 180], 'fps': 30, 'decoded_frames_each': 90,
         'silent': True, 'native_attachment_tested': False,
         'not_verified': ['reel/timecode retention', 'multichannel audio', 'VFR conform', 'native relink/export']})
    dump(outputs / 'montage-build-info.json', {'synthetic': True, 'set': 'montage', 'pillow': pillow_version,
         'font_family': fonts[14].getname()[0], 'ffmpeg': run([ffmpeg, '-version']).splitlines()[0],
         'native_ae_render': False, 'native_premiere_execution': False, 'upstream_pipeline_executed': False,
         'cloud_requests': 0, 'human_audio_audition': False, 'contains_recorded_or_generated_speech': False,
         'normalization': 'Only private/temporary file paths are omitted or made relative.'})


def build_editorial(out, ffmpeg, font_path):
    """Four original editorial examples plus explicit JSON-only proxy analysis."""
    import re
    from PIL import Image, ImageDraw, ImageFont, __version__ as pillow_version
    media, outputs, work = out / 'media', out / 'outputs', out / 'work'
    fonts = {}

    def text(im, xy, value, size=16, fill=INK):
        if size not in fonts:
            fonts[size] = ImageFont.truetype(font_path, size)
        ImageDraw.Draw(im).text(xy, value, font=fonts[size], fill=fill)

    def ff(args):
        return run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-nostdin', '-n', *args], out)

    def sha(file):
        return hashlib.sha256(file.read_bytes()).hexdigest()

    # Authored text, not transcription, speech alignment or an executed NLE edit.
    fixture = ROOT / 'examples/fixtures/transcript-selects.json'
    transcript = json.loads(fixture.read_text(encoding='utf-8'))
    mapping, cursor = [], 0
    for key in transcript['selected_ids']:
        segment = next(s for s in transcript['segments'] if s['id'] == key)
        length = segment['out_frame'] - segment['in_frame']
        mapping.append({'segment_id': key, 'source_frames': [segment['in_frame'], segment['out_frame']],
                        'output_frames': [cursor, cursor + length], 'text': segment['text']})
        cursor += length
    dump(outputs / 'paper-edit.json', {'kind': 'calculated-fictional-paper-edit', 'fixture_sha256': sha(fixture),
         'source_id': transcript['source_id'], 'fps': 30, 'ranges': 'start-inclusive/end-exclusive',
         'selected': mapping, 'output_frames': cursor, 'output_duration_s': cursor / 30,
         'asr_executed': False, 'recorded_speech': False, 'native_edit_executed': False,
         'human_context_review': False})
    board = Image.new('RGB', (640, 360), PAPER)
    d = ImageDraw.Draw(board)
    text(board, (20, 16), '20 / SOURCE-LINKED PAPER EDIT', 22)
    text(board, (20, 48), 'Fictional text. No speech recording. No NLE cut.', 14)
    for i, segment in enumerate(transcript['segments']):
        x = 20 + 205 * i
        selected = segment['id'] in transcript['selected_ids']
        d.rounded_rectangle((x, 90, x + 190, 205), radius=8, fill=YELLOW if selected else '#c8c7c1')
        text(board, (x + 10, 100), segment['id'] + (' / KEEP' if selected else ' / OMIT'), 16)
        text(board, (x + 10, 138), segment['text'], 16)
        text(board, (x + 10, 174), f"source [{segment['in_frame']},{segment['out_frame']})", 14)
    text(board, (20, 236), 'A01 -> output [0,30)     A03 -> output [30,60)', 20)
    text(board, (20, 274), '60 output frames / 30 fps = 2.0 seconds', 18)
    text(board, (20, 324), 'Calculation only. Meaning and listening review remain human tasks.', 13)
    board.save(media / 'transcript-plan.png')

    # Three original hard-cut shots; detection happens on the encoded MP4.
    for n in range(90):
        shot = n // 30
        bg, fg = [(TEAL, INK), (PAPER, INK), (INK, PAPER)][shot]
        im = Image.new('RGB', (480, 270), bg)
        draw = ImageDraw.Draw(im)
        text(im, (20, 16), f'SYNTHETIC SHOT {shot + 1}', 22, fg)
        if shot == 0:
            draw.ellipse((180, 78, 300, 198), fill=INK)
        elif shot == 1:
            draw.polygon([(240, 74), (316, 200), (164, 200)], fill=INK)
        else:
            draw.rectangle((178, 78, 302, 202), fill=YELLOW)
        text(im, (20, 236), f'source frame {n:02} / 30 fps / silent', 14, fg)
        im.save(work / f'scene-{n:03}.png')
    ff(['-framerate', '30', '-i', 'work/scene-%03d.png', '-frames:v', '90', '-r', '30', '-an',
        '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', 'media/scene-selects.mp4'])
    raw = ff(['-i', 'media/scene-selects.mp4', '-an', '-vf', 'scdet=t=12,metadata=mode=print:file=-', '-f', 'null', '-'])
    candidates, frame, score = [], None, None
    for line in raw.splitlines():
        match = re.match(r'frame:\s*(\d+)\s+.*pts_time:', line)
        if match:
            frame = int(match.group(1))
        if line.startswith('lavfi.scd.score='):
            score = float(line.split('=', 1)[1])
        if line.startswith('lavfi.scd.time='):
            candidates.append({'frame': frame, 'time_s': float(line.split('=', 1)[1]), 'score': score})
    assert [c['frame'] for c in candidates] == [30, 60], candidates
    assert [c['time_s'] for c in candidates] == [1, 2], candidates
    selected_frames = [15, 45, 75]
    expression = '+'.join(f'eq(n\\,{n})' for n in selected_frames)
    ff(['-i', 'media/scene-selects.mp4', '-vf', f'select={expression}', '-vsync', '0', 'work/scene-contact-%02d.png'])
    contact = Image.new('RGB', (720, 187), PAPER)
    for i, n in enumerate(selected_frames):
        with Image.open(work / f'scene-contact-{i + 1:02}.png') as im:
            contact.paste(im.convert('RGB').resize((240, 135), Image.Resampling.LANCZOS), (240 * i, 0))
        text(contact, (240 * i + 10, 141), f'SYNTH_A / frame {n}', 13)
    text(contact, (10, 166), 'Decoded representatives; candidates at frames 30 and 60 are not editorial approval.', 12)
    contact.save(media / 'scene-contact.png')
    dump(outputs / 'scene-candidates.json', {'kind': 'measured-synthetic-hard-cut-detection',
         'source': 'media/scene-selects.mp4', 'sha256': sha(media / 'scene-selects.mp4'), 'fps': 30,
         'filter': 'scdet=t=12,metadata=mode=print:file=-', 'threshold_scale': '0-100',
         'expected_boundary_frames': [30, 60], 'candidates': candidates,
         'representative_frames': selected_frames, 'human_editorial_review': False,
         'pyscenedetect_executed': False, 'not_tested': ['dissolves', 'flashes', 'camera motion', 'semantic scenes']})
    qc = tool('skills/montage/video-delivery-qc/scripts/media_qc.py',
              ['media/scene-selects.mp4', '--expect-width', '480', '--expect-height', '270', '--expect-fps', '30',
               '--expect-frames', '90', '--expect-duration', '3', '--expect-audio', 'no'], out)
    assert qc['ok'], qc['checks']
    dump(outputs / 'scene-qc.json', qc)

    # Labels are known by synthesis design, not speech recognition or audition.
    caption_reports = {}
    spans = [('00:00:00.300', '00:00:01.000'), ('00:00:01.000', '00:00:02.000'), ('00:00:02.000', '00:00:03.000')]
    for language, labels in [('en', ['[Sweep]', '[Impact]', '[Chime]']), ('fr', ['[Balayage]', '[Impact]', '[Carillon]'])]:
        blocks = [f'{i + 1}\n{start} --> {end}\n{label}\n' for i, ((start, end), label) in enumerate(zip(spans, labels))]
        srt_text = '\n'.join(blocks).replace('.', ',')
        vtt_text = 'WEBVTT\n\nNOTE Synthetic author-assigned sound labels; not ASR.\n\n' + '\n'.join(blocks)
        (outputs / f'captions-sounds-{language}.srt').write_bytes(srt_text.encode('utf-8'))
        (outputs / f'captions-sounds-{language}.vtt').write_bytes(vtt_text.encode('utf-8'))
        caption_reports[language] = tool('skills/montage/montage-editing-craft/scripts/srt_check.py',
             [f'outputs/captions-sounds-{language}.srt', '--preset', 'social-landscape',
              *(['--french', 'fr-CA'] if language == 'fr' else [])], out)
    dump(outputs / 'caption-access-check.json', {'kind': 'measured-sidecar-timing-with-authored-sound-labels',
         'audio_reference': 'examples/media/sfx-preview.mp4', 'audio_reference_sha256': sha(ROOT / 'examples/media/sfx-preview.mp4'),
         'srt_checks': caption_reports, 'spoken_dialogue': False, 'asr_executed': False,
         'human_audio_audition': False, 'human_translation_review': False, 'native_player_tested': False,
         'accessibility_certified': False, 'cue_start_seconds': [.3, 1, 2]})
    board = Image.new('RGB', (640, 300), INK)
    draw = ImageDraw.Draw(board)
    text(board, (20, 18), '22 / CAPTION SIDECARS + LOCALES', 22, PAPER)
    text(board, (20, 58), 'Authored labels for synthetic sounds; no spoken dialogue.', 15, PAPER)
    for x, language, label in [(20, 'EN', '[Chime]'), (330, 'FR-CA', '[Carillon]')]:
        draw.rounded_rectangle((x, 112, x + 290, 213), radius=10, fill=PAPER)
        text(board, (x + 15, 124), language + ' / 2.000-3.000 s', 16)
        text(board, (x + 15, 163), label, 27)
    text(board, (20, 247), 'Layout mockup. Not a player, RTL or accessibility certification test.', 14, PAPER)
    text(board, (20, 273), 'Separate UTF-8 SRT + WebVTT tracks; keep the unburned master.', 14, TEAL)
    board.save(media / 'caption-locales.png')

    # File-integrity proof with a real new-directory restore, no fake native file.
    note = b'SYNTHETIC HANDOFF NOTE - NOT AN NLE PROJECT\nMedia: media/scene-selects.mp4\nAnalysis: outputs/scene-candidates.json\nContact: media/scene-contact.png\nOnly byte integrity is tested. No native project has been opened.\n'
    (outputs / 'handoff-note.txt').write_bytes(note)
    files = ['outputs/handoff-note.txt', 'media/scene-selects.mp4', 'outputs/scene-candidates.json', 'media/scene-contact.png']
    manifest = {'canonical': files[0], 'canonical_sha256': sha(out / files[0]),
                'files': [{'path': name, 'size': (out / name).stat().st_size, 'sha256': sha(out / name)} for name in files]}
    dump(outputs / 'handoff-manifest.json', manifest)
    verifier = 'skills/after-effects/ae-production-workflow/scripts/verify-delivery-manifest.py'
    before = tool(verifier, ['outputs/handoff-manifest.json', '--root', '.'], out)
    before.update(manifest='outputs/handoff-manifest.json', root='.')
    restored = work / 'restored'
    restored.mkdir()
    for name in files:
        target = restored / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(out / name, target)
    shutil.copy2(outputs / 'handoff-manifest.json', restored / 'handoff-manifest.json')
    after = tool(verifier, ['handoff-manifest.json', '--root', '.'], restored)
    after.update(manifest='handoff-manifest.json', root='restored-copy')
    assert before['ok'] and after['ok']
    dump(outputs / 'handoff-restore-check.json', {'kind': 'measured-file-copy-and-integrity-check', 'before': before,
         'restored': after, 'restored_into_new_directory': True, 'source_deleted': False,
         'native_project_opened': False, 'dependency_discovery_performed': False})

    proxy = tool('skills/montage/montage-proxy-conform/scripts/proxy_audit.py',
                 ['json', ROOT / 'examples/fixtures/proxy-source-probe.json', ROOT / 'examples/fixtures/proxy-small-probe.json'],
                 out, expected=(3,))
    dump(outputs / 'proxy-audit.json', proxy)
    dump(outputs / 'editorial-build-info.json', {'synthetic': True, 'set': 'editorial', 'pillow': pillow_version,
         'font_family': fonts[16].getname()[0], 'ffmpeg': run([ffmpeg, '-version']).splitlines()[0],
         'native_premiere_execution': False, 'native_project_restore': False, 'asr_executed': False,
         'pyscenedetect_executed': False, 'cloud_requests': 0, 'human_audio_audition': False,
         'normalization': 'Temporary paths omitted or made relative; text artifacts use LF.'})


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', required=True, help='NEW output directory, preferably .local/examples-preview')
    ap.add_argument('--font', help='Licensed font available on this machine; not copied or embedded')
    ap.add_argument('--set', choices=('all', 'core', 'montage', 'editorial'), default='all',
                    help='all (default), original core, 0.4.0 montage, or 0.5.0 editorial examples')
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
        build(out, exe, chosen, args.set)
    except (ImportError, RuntimeError) as e:
        ap.exit(2, str(e) + '\n')


if __name__ == '__main__':
    main()
