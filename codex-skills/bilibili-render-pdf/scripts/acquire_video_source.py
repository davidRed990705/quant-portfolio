#!/usr/bin/env python3
"""
Acquire video, subtitles, and source metadata for bilibili-render-pdf.

This script is a mechanical helper. It does not summarize, translate, interpret,
or decide teaching content. It only downloads/probes media and normalizes files
into the layout expected by the skill workflow.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse


VIDEO_EXTS = {".mp4", ".mkv", ".webm", ".flv", ".mov", ".m4v"}
SUB_EXTS = {".srt", ".vtt", ".ass"}
THUMB_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
DEFAULT_SUB_LANGS = "zh-Hans,zh-CN,zh,zh-Hant,ai-zh,en.*,en"
SUB_PRIORITY = [
    "zh-hans",
    "zh-cn",
    "zh",
    "zh-hant",
    "ai-zh",
    "en",
]


@dataclass
class UrlItem:
    index: int
    url: str
    source_line: int | None
    key: str
    duplicate_of: int | None = None
    platform: str = "unknown"
    bilibili_part: str | None = None


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            "Command failed:\n"
            + " ".join(cmd)
            + "\n\nSTDOUT:\n"
            + result.stdout
            + "\n\nSTDERR:\n"
            + result.stderr
        )
    return result


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise SystemExit(f"Required tool not found on PATH: {name}")
    return path


def read_urls(inputs: list[str]) -> list[tuple[str, int | None]]:
    out: list[tuple[str, int | None]] = []
    url_re = re.compile(r"https?://\S+")
    for raw in inputs:
        p = Path(raw)
        if p.exists() and p.is_file():
            for line_no, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                match = url_re.search(line)
                if match:
                    out.append((match.group(0), line_no))
        else:
            match = url_re.search(raw)
            if match:
                out.append((match.group(0), None))
    return out


def detect_platform(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if "bilibili.com" in host or "b23.tv" in host:
        return "bilibili"
    if "youtube.com" in host or "youtu.be" in host:
        return "youtube"
    return "other"


def bilibili_part(url: str) -> str | None:
    query = parse_qs(urlparse(url).query)
    p = query.get("p", [None])[0]
    return p if p and p.isdigit() else None


def canonical_key(url: str, keep_query: bool = True) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    query_map = parse_qs(parsed.query)
    if "bilibili.com" in host:
        match = re.search(r"/video/(BV[A-Za-z0-9]+)", parsed.path)
        if match:
            return f"bilibili:{match.group(1)}:p={query_map.get('p', ['1'])[0]}"
    if "youtube.com" in host:
        video_id = query_map.get("v", [None])[0]
        if video_id:
            list_id = query_map.get("list", [""])[0]
            index = query_map.get("index", [""])[0]
            return f"youtube:{video_id}:list={list_id}:index={index}"
    if "youtu.be" in host:
        video_id = parsed.path.strip("/")
        return f"youtube:{video_id}"
    query = parsed.query if keep_query else ""
    return parsed._replace(query=query, fragment="").geturl()


def collect_url_items(inputs: list[str]) -> list[UrlItem]:
    seen: dict[str, int] = {}
    items: list[UrlItem] = []
    for url, line_no in read_urls(inputs):
        key = canonical_key(url, keep_query=True)
        duplicate_of = seen.get(key)
        if duplicate_of is None:
            seen[key] = len(items) + 1
        item = UrlItem(
            index=len(items) + 1,
            url=url,
            source_line=line_no,
            key=key,
            duplicate_of=duplicate_of,
            platform=detect_platform(url),
            bilibili_part=bilibili_part(url),
        )
        items.append(item)
    return items


def safe_json_loads(text: str) -> dict[str, Any]:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start : end + 1])
        raise


def yt_dlp_base_args(args: argparse.Namespace, item: UrlItem) -> list[str]:
    cmd = ["yt-dlp", "--no-warnings"]
    if args.cookies_from_browser:
        cmd += ["--cookies-from-browser", args.cookies_from_browser]
    if args.cookies:
        cmd += ["--cookies", str(args.cookies)]
    if item.platform == "bilibili" and item.bilibili_part:
        cmd += ["--playlist-items", item.bilibili_part]
    return cmd


def probe_metadata(args: argparse.Namespace, item: UrlItem) -> dict[str, Any]:
    cmd = yt_dlp_base_args(args, item) + ["--dump-single-json", "--skip-download", item.url]
    result = run(cmd, check=False)
    if result.returncode != 0:
        return {
            "probe_ok": False,
            "error": result.stderr.strip()[-2000:],
            "url": item.url,
            "platform": item.platform,
            "bilibili_part": item.bilibili_part,
        }
    info = safe_json_loads(result.stdout)
    return {
        "probe_ok": True,
        "id": info.get("id"),
        "title": info.get("title"),
        "fulltitle": info.get("fulltitle"),
        "duration": info.get("duration"),
        "webpage_url": info.get("webpage_url") or item.url,
        "extractor": info.get("extractor"),
        "playlist_count": info.get("playlist_count"),
        "playlist_index": info.get("playlist_index"),
        "thumbnail": info.get("thumbnail"),
        "chapters": info.get("chapters") or [],
        "subtitles": sorted((info.get("subtitles") or {}).keys()),
        "automatic_captions": sorted((info.get("automatic_captions") or {}).keys()),
        "formats": [
            {
                "format_id": f.get("format_id"),
                "ext": f.get("ext"),
                "height": f.get("height"),
                "width": f.get("width"),
                "vcodec": f.get("vcodec"),
                "acodec": f.get("acodec"),
                "format_note": f.get("format_note"),
            }
            for f in (info.get("formats") or [])[-20:]
        ],
    }


def download_item(args: argparse.Namespace, item: UrlItem, item_dir: Path) -> dict[str, Any]:
    raw_dir = item_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    outtmpl = str(raw_dir / "%(title).180B [%(id)s].%(ext)s")
    cmd = yt_dlp_base_args(args, item)
    cmd += [
        "--write-info-json",
        "--write-thumbnail",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs",
        args.sub_langs,
        "--convert-subs",
        "srt",
        "-f",
        args.format,
        "--merge-output-format",
        "mp4",
        "-o",
        outtmpl,
        item.url,
    ]
    result = run(cmd, check=False)
    return {
        "download_ok": result.returncode == 0,
        "command": redact_command(cmd),
        "stdout_tail": result.stdout[-3000:],
        "stderr_tail": result.stderr[-3000:],
    }


def redact_command(cmd: list[str]) -> list[str]:
    redacted = []
    skip_next = False
    for i, part in enumerate(cmd):
        if skip_next:
            redacted.append("<redacted>")
            skip_next = False
            continue
        redacted.append(part)
        if part == "--cookies":
            skip_next = True
    return redacted


def choose_largest(paths: list[Path]) -> Path | None:
    paths = [p for p in paths if p.exists() and p.is_file()]
    if not paths:
        return None
    return max(paths, key=lambda p: p.stat().st_size)


def choose_subtitle(paths: list[Path]) -> Path | None:
    candidates = [p for p in paths if p.suffix.lower() in SUB_EXTS]
    if not candidates:
        return None
    scored: list[tuple[int, int, Path]] = []
    for p in candidates:
        name = p.name.lower()
        lang_score = len(SUB_PRIORITY)
        for idx, lang in enumerate(SUB_PRIORITY):
            if f".{lang}." in name or name.endswith(f".{lang}{p.suffix.lower()}"):
                lang_score = idx
                break
        auto_penalty = 2 if ".auto." in name or "automatic" in name else 0
        scored.append((lang_score + auto_penalty, -p.stat().st_size, p))
    scored.sort()
    return scored[0][2]


def normalize_video(video: Path, dest: Path) -> dict[str, Any]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if video.suffix.lower() == ".mp4":
        shutil.copy2(video, dest)
        return {"video_normalized": True, "method": "copy", "source": str(video)}
    result = run(["ffmpeg", "-y", "-i", str(video), "-c", "copy", str(dest)], check=False)
    if result.returncode == 0 and dest.exists():
        return {"video_normalized": True, "method": "ffmpeg_remux", "source": str(video)}
    fallback = dest.with_suffix(video.suffix)
    shutil.copy2(video, fallback)
    return {
        "video_normalized": False,
        "method": "copy_original_ext",
        "source": str(video),
        "fallback_video": str(fallback),
        "ffmpeg_error": result.stderr[-2000:],
    }


def subtitle_to_transcript(srt_path: Path, transcript_path: Path) -> dict[str, Any]:
    transcript_path.parent.mkdir(parents=True, exist_ok=True)
    text = srt_path.read_text(encoding="utf-8", errors="replace")
    entries = re.split(r"\n\s*\n", text.strip(), flags=re.M)
    out: list[str] = []
    count = 0
    time_re = re.compile(r"(\d\d:\d\d:\d\d[,.]\d+)\s+-->\s+(\d\d:\d\d:\d\d[,.]\d+)")
    for block in entries:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if len(lines) < 2:
            continue
        match = None
        for line in lines:
            match = time_re.search(line)
            if match:
                break
        if not match:
            continue
        body = " ".join(line for line in lines if not line.isdigit() and "-->" not in line)
        body = re.sub(r"<[^>]+>", "", body).strip()
        if not body:
            continue
        count += 1
        start = match.group(1).replace(",", ".")
        end = match.group(2).replace(",", ".")
        out.append(f"字幕({start}--{end}): {body}")
    transcript_path.write_text("\n\n".join(out) + ("\n" if out else ""), encoding="utf-8")
    return {"transcript_entries": count, "transcript_file": str(transcript_path)}


def write_url_list(items: list[UrlItem], output_dir: Path) -> None:
    lines = []
    for item in items:
        dup = f" duplicate_of={item.duplicate_of}" if item.duplicate_of else ""
        part = f" p={item.bilibili_part}" if item.bilibili_part else ""
        lines.append(f"{item.index:03d} {item.platform}{part}{dup} {item.url}")
    (output_dir / "url_list_normalized.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def item_slug(index: int) -> str:
    return f"item_{index:03d}"


def normalize_thumbnail(thumbnail: Path, dest_jpg: Path) -> dict[str, Any]:
    dest_jpg.parent.mkdir(parents=True, exist_ok=True)
    if thumbnail.suffix.lower() in {".jpg", ".jpeg"}:
        shutil.copy2(thumbnail, dest_jpg)
        return {"cover_normalized": True, "method": "copy_jpg", "source": str(thumbnail), "cover": str(dest_jpg)}
    result = run(["ffmpeg", "-y", "-i", str(thumbnail), "-frames:v", "1", str(dest_jpg)], check=False)
    if result.returncode == 0 and dest_jpg.exists():
        return {"cover_normalized": True, "method": "ffmpeg_convert", "source": str(thumbnail), "cover": str(dest_jpg)}
    fallback = dest_jpg.with_suffix(thumbnail.suffix.lower())
    shutil.copy2(thumbnail, fallback)
    return {
        "cover_normalized": False,
        "method": "copy_original_ext",
        "source": str(thumbnail),
        "cover": str(fallback),
        "ffmpeg_error": result.stderr[-2000:],
    }


def process_item(args: argparse.Namespace, item: UrlItem, output_dir: Path) -> dict[str, Any]:
    item_dir = output_dir / "items" / item_slug(item.index)
    item_dir.mkdir(parents=True, exist_ok=True)
    record: dict[str, Any] = {
        "index": item.index,
        "url": item.url,
        "source_line": item.source_line,
        "duplicate_of": item.duplicate_of,
        "platform": item.platform,
        "bilibili_part": item.bilibili_part,
        "item_dir": str(item_dir),
    }

    if item.duplicate_of:
        record["status"] = "skipped_duplicate"
        return record
    if args.dry_run:
        record["status"] = "dry_run"
        return record

    source_dir = item_dir / "source"
    source_dir.mkdir(exist_ok=True)
    metadata = probe_metadata(args, item)
    record["metadata"] = metadata
    metadata_text = json.dumps(metadata, ensure_ascii=False, indent=2)
    (item_dir / "metadata_probe.json").write_text(metadata_text, encoding="utf-8")
    (source_dir / "source_metadata.json").write_text(metadata_text, encoding="utf-8")

    if args.metadata_only:
        record["status"] = "metadata_only" if metadata.get("probe_ok") else "metadata_failed"
        if not metadata.get("probe_ok"):
            record["needs_cookies_or_retry"] = item.platform == "bilibili"
        return record

    download = download_item(args, item, item_dir)
    record["download"] = download
    if not download["download_ok"]:
        record["status"] = "download_failed"
        return record

    raw_files = list((item_dir / "raw").glob("*"))
    video = choose_largest([p for p in raw_files if p.suffix.lower() in VIDEO_EXTS])
    subtitles = [p for p in raw_files if p.suffix.lower() in SUB_EXTS]
    subtitle = choose_subtitle(subtitles)
    thumbnail = choose_largest([p for p in raw_files if p.suffix.lower() in THUMB_EXTS])

    srt_dir = item_dir / "srt"
    srt_dir.mkdir(exist_ok=True)

    if video:
        record["video"] = normalize_video(video, source_dir / "source_video.mp4")
    else:
        record["video"] = {"video_normalized": False, "error": "no downloaded video file found"}

    if subtitle:
        source_srt = source_dir / "source_subtitle.srt"
        srt_copy = srt_dir / "source_subtitle.srt"
        shutil.copy2(subtitle, source_srt)
        shutil.copy2(subtitle, srt_copy)
        record["subtitle"] = {
            "subtitle_found": True,
            "selected_subtitle": str(subtitle),
            "source_subtitle": str(source_srt),
            "srt_copy": str(srt_copy),
        }
        record["transcript"] = subtitle_to_transcript(source_srt, source_dir / "source_transcript.txt")
    else:
        record["subtitle"] = {
            "subtitle_found": False,
            "needs_asr": True,
            "message": "No platform subtitle was downloaded. Run ASR/Whisper or provide a local transcript before visual localization.",
        }

    if thumbnail:
        record["cover"] = normalize_thumbnail(thumbnail, source_dir / "cover.jpg")

    record["status"] = "ready" if record.get("video", {}).get("video_normalized") and record.get("subtitle", {}).get("subtitle_found") else "needs_review"
    return record


def mirror_single_ready_item(output_dir: Path, records: list[dict[str, Any]]) -> None:
    ready = [r for r in records if r.get("status") in {"ready", "needs_review"} and not r.get("duplicate_of")]
    if len(ready) != 1:
        return
    src_item = Path(ready[0]["item_dir"])
    for name in ["source", "srt"]:
        src = src_item / name
        dst = output_dir / name
        if dst.exists():
            shutil.rmtree(dst)
        if src.exists():
            shutil.copytree(src, dst)


def file_sha256(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Download/probe Bilibili or YouTube video sources for bilibili-render-pdf.")
    parser.add_argument("inputs", nargs="+", help="URL(s), or text file(s) containing URLs.")
    parser.add_argument("--output-dir", required=True, type=Path, help="Run output directory.")
    parser.add_argument("--sub-langs", default=DEFAULT_SUB_LANGS, help="yt-dlp subtitle language preference.")
    parser.add_argument("--format", default="bv*[height<=1080]+ba/b[height<=1080]/bv*+ba/b", help="yt-dlp format selector.")
    parser.add_argument("--cookies-from-browser", default=None, help="Browser name for yt-dlp cookies, e.g. chrome or edge.")
    parser.add_argument("--cookies", type=Path, default=None, help="Netscape cookies.txt path.")
    parser.add_argument("--metadata-only", action="store_true", help="Only probe metadata; do not download media.")
    parser.add_argument("--dry-run", action="store_true", help="Only parse and deduplicate input URLs; do not call yt-dlp.")
    parser.add_argument("--max-items", type=int, default=None, help="Process only the first N URL entries after reading inputs.")
    args = parser.parse_args()

    if not args.dry_run:
        require_tool("yt-dlp")
    if not args.dry_run and not args.metadata_only:
        require_tool("ffmpeg")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    items = collect_url_items(args.inputs)
    if args.max_items is not None:
        items = items[: args.max_items]
    if not items:
        raise SystemExit("No URLs found in inputs.")

    write_url_list(items, args.output_dir)
    records = []
    for item in items:
        try:
            records.append(process_item(args, item, args.output_dir))
        except Exception as exc:
            records.append(
                {
                    "index": item.index,
                    "url": item.url,
                    "source_line": item.source_line,
                    "duplicate_of": item.duplicate_of,
                    "platform": item.platform,
                    "bilibili_part": item.bilibili_part,
                    "status": "error",
                    "error": str(exc),
                }
            )

    mirror_single_ready_item(args.output_dir, records)
    manifest = {
        "workflow": "bilibili-render-pdf-source-acquisition",
        "tool": "scripts/acquire_video_source.py",
        "codex_native_mode": True,
        "mechanical_only": True,
        "sub_langs": args.sub_langs,
        "format": args.format,
        "cookies_from_browser": args.cookies_from_browser,
        "cookies_file_used": bool(args.cookies),
        "metadata_only": args.metadata_only,
        "dry_run": args.dry_run,
        "item_root": str(args.output_dir / "items"),
        "input_count": len(items),
        "unique_count": len([i for i in items if not i.duplicate_of]),
        "duplicate_count": len([i for i in items if i.duplicate_of]),
        "items": records,
    }
    manifest["ready_count"] = len([r for r in records if r.get("status") == "ready"])
    manifest["metadata_failed_count"] = len([r for r in records if r.get("status") == "metadata_failed"])
    manifest["download_failed_count"] = len([r for r in records if r.get("status") == "download_failed"])
    manifest["needs_review_count"] = len([r for r in records if r.get("status") == "needs_review"])
    manifest["needs_cookies_or_retry_count"] = len([r for r in records if r.get("needs_cookies_or_retry")])
    single_video = args.output_dir / "source" / "source_video.mp4"
    single_sub = args.output_dir / "source" / "source_subtitle.srt"
    manifest["single_root_source_video"] = str(single_video) if single_video.exists() else None
    manifest["single_root_source_video_sha256"] = file_sha256(single_video)
    manifest["single_root_source_subtitle"] = str(single_sub) if single_sub.exists() else None
    manifest["single_root_source_subtitle_sha256"] = file_sha256(single_sub)
    (args.output_dir / "acquisition_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output_dir": str(args.output_dir), "items": len(items), "unique": manifest["unique_count"], "duplicates": manifest["duplicate_count"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
