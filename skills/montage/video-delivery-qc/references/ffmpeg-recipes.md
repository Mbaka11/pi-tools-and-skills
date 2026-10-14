# Vetted FFmpeg recipes

All commands read a high-quality master and never overwrite (`-n`). Replace
`ffmpeg` with the path from `$FFMPEG` or `imageio_ffmpeg.get_ffmpeg_exe()` when
it is not on PATH. When converting RGB masters (ProRes 4444, PNG) to 4:2:0,
specify the BT.709 matrix in the scale filter to avoid a colour shift.

## H.264 web master (1080p, 30 fps)

```bash
ffmpeg -n -i master.mov -map 0:v:0 -map 0:a:0? \
  -vf "scale=1920:1080:flags=lanczos:out_color_matrix=bt709:out_range=tv,setsar=1,format=yuv420p" \
  -c:v libx264 -preset slow -crf 18 -maxrate 12M -bufsize 24M -profile:v high -level:v 4.1 \
  -g 15 -bf 2 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv \
  -c:a aac -b:a 320k -ar 48000 -ac 2 -movflags +faststart out_1920x1080_30p.mp4
```

`-g 15` gives a closed GOP of half the frame rate as YouTube recommends; use a
value equal to half the fps for other rates.

## ProRes intermediates

```bash
# ProRes 422 HQ (editor handoff)
ffmpeg -n -i in.mov -c:v prores_ks -profile:v 3 -pix_fmt yuv422p10le -c:a pcm_s24le out_hq.mov
# ProRes 4444 with alpha (overlays, lower thirds)
ffmpeg -n -i in_rgba.mov -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le -alpha_bits 16 out_4444.mov
```

## Transparent video for the web (VP9 WebM with alpha)

```bash
ffmpeg -n -i in_rgba.mov -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 30 -row-mt 1 -an out_alpha.webm
```

H.264/MP4 cannot carry alpha: a transparent comp exported to H.264 always gets
a solid background.

## Image sequence ↔ video

```bash
ffmpeg -n -framerate 30 -i frames/frame_%05d.png -c:v prores_ks -profile:v 3 -pix_fmt yuv422p10le seq.mov
ffmpeg -n -i in.mov -vf "select=eq(n\,0)" -frames:v 1 first_frame.png
```

## Loudness normalisation (two-pass loudnorm)

```bash
# 1) measure
ffmpeg -hide_banner -i mix.wav -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null -
# 2) apply with the measured values (measured_I, measured_TP, measured_LRA, measured_thresh, offset)
ffmpeg -n -i mix.wav -af loudnorm=I=-14:TP=-1:LRA=11:measured_I=<..>:measured_TP=<..>:measured_LRA=<..>:measured_thresh=<..>:offset=<..>:linear=true \
  -ar 48000 -c:a pcm_s24le mix_-14LUFS.wav
```

Prefer normalising the **mix** before muxing; re-measure the final file with
media_qc.py. For broadcast use the broadcaster's target (−24 LKFS in Canada).

## Replace or add audio without re-encoding video

```bash
ffmpeg -n -i picture.mp4 -i mix.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart out.mp4
```

## Remove audio (LED, website backgrounds)

```bash
ffmpeg -n -i in.mp4 -map 0:v:0 -c:v copy -an -movflags +faststart out_silent.mp4
```

## High-quality GIF

```bash
ffmpeg -n -i in.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4" out.gif
```

## Burn subtitles (when libass is available)

```bash
ffmpeg -n -i in.mp4 -vf "subtitles=subs.srt:force_style='FontName=Arial,FontSize=28,Outline=2'" -c:a copy out_subtitled.mp4
```

Check `ffmpeg -filters` for `subtitles`/`drawtext`; many minimal builds lack
libass or freetype. Captions designed in AE/Premiere avoid that dependency.

## Trim exactly by frames

```bash
# frames 120..419 (300 frames) at 30 fps, re-encoded for frame accuracy
ffmpeg -n -i in.mov -vf "trim=start_frame=120:end_frame=420,setpts=PTS-STARTPTS" -af "atrim=start=4:end=14,asetpts=PTS-STARTPTS" -c:v prores_ks -profile:v 3 -c:a pcm_s24le cut.mov
```

Stream copy (`-c copy`) cuts only on keyframes; use it for speed, not accuracy.
