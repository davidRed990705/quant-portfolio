# Source Acquisition From Video URLs

Use this reference when the input is a Bilibili/YouTube URL, a BV number, a b23 short link, or a text file containing multiple video URLs.

This stage is mechanical. It downloads or probes media and subtitles so Codex can later perform transcript understanding, visual-question design, frame interpretation, and writing. The acquisition script must not summarize, classify knowledge, choose teaching points, or make visual claims.

## What We Absorb From The Reference Project

The wdkns workflow is useful here because it treats platform metadata, subtitles, cover images, and downloadable video as first-class source artifacts before writing begins. Keep these platform lessons:

- Prefer platform subtitles before ASR.
- Preserve subtitle timestamps because later keyframe search depends on subtitle-aligned intervals.
- Probe available formats and download the highest usable video in the current environment.
- For Bilibili, expect subtitle scarcity, login-gated high resolution, and multi-part `p=` videos.
- Use cookies only as a download credential path, never as teaching content.
- Do not use danmaku as transcript evidence.

## Accepted Inputs

Accepted source inputs:

- one Bilibili URL, BV URL, or b23 short link
- one YouTube URL
- a text file containing one URL per line
- mixed URL text where URLs can be extracted from surrounding notes

For Bilibili multi-part videos:

- If the URL contains `p=N`, process that exact part by passing `--playlist-items N` to `yt-dlp`.
- If the URL does not contain `p=`, treat it as part 1 unless the metadata clearly shows a playlist and the user asked for multiple parts.
- If a URL file contains repeated URLs, deduplicate by video identity and part, not by tracking parameters such as `spm_id_from` or `vd_source`.

## Standard Command

Use `scripts/acquire_video_source.py` as the default entry point.

Dry-run a URL file without network/download:

```powershell
python C:\Users\david\.codex\skills\bilibili-render-pdf\scripts\acquire_video_source.py `
  C:\path\to\视频地址.txt `
  --output-dir C:\path\to\output `
  --dry-run
```

Probe metadata and subtitles for one or more items without downloading video:

```powershell
python C:\Users\david\.codex\skills\bilibili-render-pdf\scripts\acquire_video_source.py `
  C:\path\to\视频地址.txt `
  --output-dir C:\path\to\output `
  --metadata-only `
  --max-items 1
```

Download video, subtitles, metadata, and cover:

```powershell
python C:\Users\david\.codex\skills\bilibili-render-pdf\scripts\acquire_video_source.py `
  "https://www.bilibili.com/video/BVxxxx?p=2" `
  --output-dir C:\path\to\output
```

If higher Bilibili quality is login-gated, use browser cookies only when the user wants that quality:

```powershell
python C:\Users\david\.codex\skills\bilibili-render-pdf\scripts\acquire_video_source.py `
  "https://www.bilibili.com/video/BVxxxx?p=2" `
  --output-dir C:\path\to\output `
  --cookies-from-browser chrome
```

The manifest may record that browser cookies were requested, but it must not record cookie values or cookie file contents.

## Subtitle Priority

The acquisition stage should request:

```text
zh-Hans, zh-CN, zh, zh-Hant, ai-zh, en.*, en
```

Selection priority:

1. Chinese manual subtitles when available
2. Chinese auto subtitles
3. English subtitles only when Chinese is unavailable
4. ASR/Whisper fallback when no platform subtitles exist and the user approves or asks for ASR
5. visual-only mode only when neither subtitle nor ASR is available

Keep the selected subtitle as SRT and create a timestamped text view for Codex reading. Do not flatten timestamps away before visual localization is complete.

## Output Layout

The acquisition stage writes:

```text
output/
  acquisition_manifest.json
  url_list_normalized.txt
  items/
    item_001/
      metadata_probe.json
      raw/
      source/
        source_video.mp4
        source_subtitle.srt
        source_transcript.txt
        source_metadata.json
        cover.jpg
      srt/
        source_subtitle.srt
```

When exactly one unique item is ready, the script also mirrors `items/item_001/source/` and `items/item_001/srt/` to:

```text
output/
  source/
  srt/
```

This keeps the rest of the skill workflow compatible with both single-video and batch URL acquisition.

## Manifest Requirements

`acquisition_manifest.json` must record:

- input URL count, unique count, duplicate count
- normalized URL list and source line numbers when input came from a file
- platform and Bilibili part number
- whether metadata probing, download, subtitle extraction, video normalization, and cover normalization succeeded
- whether platform subtitles were missing and ASR is needed
- whether browser cookies or a cookies file were requested, without exposing secrets
- paths to normalized source files and SHA-256 hashes for root single-item source files when present

## Hand-Off Gate

Do not start `knowledge_points.json` until one of these is true:

- `source/source_video.mp4` and `source/source_subtitle.srt` exist for a single-video run;
- or each intended item under `items/` has a ready video and subtitle;
- or the manifest explicitly marks `needs_asr=true` and the next step is ASR/transcript repair;
- or the user deliberately chooses visual-only mode.

If only metadata was probed, treat the run as a source preview, not a full teaching-note run.
