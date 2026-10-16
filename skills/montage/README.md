# Montage skills

Category folder (not a skill). pi discovers the skill folders below
recursively.

| Skill | Use | Helper |
| --- | --- | --- |
| [led-signage-content](led-signage-content/SKILL.md) | Generic digital roll-ups and walls, LED posters: profiles, text sizes, guides, exports, splits, test cards | `scripts/led_tool.py` |
| [video-delivery-qc](video-delivery-qc/SKILL.md) | decode-based QC, loudness, loop seam, contact sheets, platform specs, FFmpeg recipes | `scripts/media_qc.py` |
| [sound-design-sfx](sound-design-sfx/SKILL.md) | spotting, licensed SFX/music, generation options, cue placement, mix targets | `scripts/sfx_place.py` |
| [montage-editing-craft](montage-editing-craft/SKILL.md) | edit workflow, pacing, Premiere via the bridge, reframes, versions, French captions and client notes | `scripts/srt_check.py` |
| [vox-explainer-pipelines](vox-explainer-pipelines/SKILL.md) | pinned Remotion/Python Vox pipelines and hosted options, with Windows and LED adaptations | vendored upstream scripts |
| [montage-colour-finishing](montage-colour-finishing/SKILL.md) | input/working/output colour spaces, shot matching, scopes, export consistency | workflow + synthetic RGB test |
| [montage-proxy-conform](montage-proxy-conform/SKILL.md) | verified ingest, proxies, VFR decisions, original-media relink and interchange | `scripts/proxy_audit.py` + decoded source/proxy pair |
| [montage-multicam-sync](montage-multicam-sync/SKILL.md) | reviewed anchors, fixed offset/drift, reversible multicam and audio routing | `scripts/sync_map.py` |
| [montage-dialogue-cleanup](montage-dialogue-cleanup/SKILL.md) | conservative noise repair, gain, room tone, listening gates and aligned DX stems | workflow + synthetic filter test |
| [montage-time-remapping](montage-time-remapping/SKILL.md) | source/output mapping, slow motion, ramps, interpolation and artifact review | workflow + actual speed-change example |
| [montage-transcript-editing](montage-transcript-editing/SKILL.md) | reviewed words, source-linked paper edits, radio cuts and context preservation | fictional cut-map example |
| [montage-scene-selects](montage-scene-selects/SKILL.md) | cut candidates, representative frames and reviewed selects | actual FFmpeg `scdet` example |
| [montage-caption-accessibility](montage-caption-accessibility/SKILL.md) | meaningful sounds, speaker labels, localization and player checks | existing SRT checker + SRT/WebVTT examples |
| [montage-archive-handoff](montage-archive-handoff/SKILL.md) | dependency inventory, reversible collection and isolated restoration | existing manifest verifier + actual byte restore |

Helpers use only the Python standard library. FFmpeg is located through
`$FFMPEG`, `PATH`, or the `imageio-ffmpeg` package; nothing is installed by the
toolbox. `sync_map.py` needs no media engine and only calculates a plan.
`proxy_audit.py media` requires separate ffprobe (`--ffprobe`, `$FFPROBE` or PATH);
its `json` mode needs no engine and does not inspect media. Incomplete metadata
is not approval to attach or conform.

[Short examples for every skill](../../examples/README.md).
