# Montage skills

Category folder (not a skill). pi discovers the skill folders below
recursively.

| Skill | Use | Helper |
| --- | --- | --- |
| [led-signage-content](led-signage-content/SKILL.md) | PixaNova roll-ups and walls, LED posters: profiles, text sizes, guides, exports, splits, test cards | `scripts/led_tool.py` |
| [video-delivery-qc](video-delivery-qc/SKILL.md) | decode-based QC, loudness, loop seam, contact sheets, platform specs, FFmpeg recipes | `scripts/media_qc.py` |
| [sound-design-sfx](sound-design-sfx/SKILL.md) | spotting, licensed SFX/music, generation options, cue placement, mix targets | `scripts/sfx_place.py` |
| [montage-editing-craft](montage-editing-craft/SKILL.md) | edit workflow, pacing, Premiere via the bridge, reframes, versions, French captions and client notes | `scripts/srt_check.py` |
| [vox-explainer-pipelines](vox-explainer-pipelines/SKILL.md) | pinned Remotion/Python Vox pipelines and hosted options, with Windows and LED adaptations | vendored upstream scripts |

Helpers use only the Python standard library. FFmpeg is located through
`$FFMPEG`, `PATH`, or the `imageio-ffmpeg` package; nothing is installed by the
toolbox.
