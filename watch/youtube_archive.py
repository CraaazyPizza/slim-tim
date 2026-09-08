#!/usr/bin/env python3.12
"""Preserve qtecqot watch pages, player responses, descriptions and downloadable media.

Raw captures remain local. This module deliberately does not equate RSS absence
or a downloader error with a deletion. yt-dlp is an external uv-managed tool.
"""
from __future__ import annotations

import gzip
import hashlib
import http.cookiejar
import html
import json
import re
import os
import shutil
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from archive_assets import atomic_bytes, atomic_json, capture

ROOT = Path(__file__).resolve().parent / "youtube"
CHANNEL_ID = "UCw1EA-KJud9OmMA5p7_MWgw"


def cookies_file():
    path = Path(os.environ.get("YOUTUBE_COOKIES_FILE") or
                "~/.config/qtecqot-watch/youtube-cookies.txt").expanduser()
    return path if path.is_file() else None


def cookie_args():
    path = cookies_file()
    return ["--cookies", str(path)] if path else []


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    opener = urllib.request.build_opener()
    if cookies_file():
        jar = http.cookiejar.MozillaCookieJar(str(cookies_file()))
        jar.load(ignore_discard=True)
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    with opener.open(request, timeout=45) as response:
        return response.read()


def player_response(body):
    text = body.decode("utf-8", "replace")
    match = re.search(r"(?:var\s+)?ytInitialPlayerResponse\s*=\s*", text)
    if not match:
        raise ValueError("watch page has no initial player response")
    value, _ = json.JSONDecoder().raw_decode(text[match.end():])
    return value


def capture_video(vid, now):
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", vid):
        raise ValueError("invalid YouTube video ID")
    directory = ROOT / "videos" / vid
    body = fetch(f"https://www.youtube.com/watch?v={vid}")
    digest = hashlib.sha256(body).hexdigest()
    atomic_bytes(directory / "pages" / f"{now:%Y%m%dT%H%M%SZ}-{digest[:16]}.html.gz",
                 gzip.compress(body, mtime=0))
    player = player_response(body)
    details = player.get("videoDetails") or {}
    raw = json.dumps(player, sort_keys=True).encode()
    fingerprint = hashlib.sha256(raw).hexdigest()
    atomic_json(directory / "players" / f"{fingerprint}.json", player)
    if details.get("videoId") != vid or details.get("channelId") != CHANNEL_ID:
        reason = (player.get("playabilityStatus") or {}).get("reason")
        raise ValueError(reason or "player does not identify the expected video and channel")
    metadata = {key: details.get(key) for key in (
        "videoId", "channelId", "author", "title", "shortDescription", "lengthSeconds",
        "keywords", "isLiveContent", "isCrawlable", "allowRatings")}
    metadata["microformat"] = player.get("microformat") or {}
    renderer = metadata["microformat"].get("playerMicroformatRenderer") or {}
    renderer.pop("viewCount", None)
    renderer.pop("likeCount", None)
    encoded = json.dumps(metadata, sort_keys=True).encode()
    revision = hashlib.sha256(encoded).hexdigest()
    old_path = directory / "latest.json"
    old = json.loads(old_path.read_text()) if old_path.exists() else {}
    snapshot = {"captured_at": now.isoformat(), "metadata": metadata,
                "revision": revision, "watch_page_sha256": digest,
                "player_sha256": fingerprint}
    revision_path = directory / "revisions" / f"{revision}.json"
    if not revision_path.exists():
        atomic_json(revision_path, snapshot)
    atomic_json(old_path, snapshot)
    # Plain text makes description changes diffable without parsing player JSON.
    atomic_bytes(directory / "description.txt", (details.get("shortDescription") or "").encode())
    thumbnails = (details.get("thumbnail") or {}).get("thumbnails") or []
    assets = capture(ROOT / "media", vid, [t["url"] for t in thumbnails if t.get("url")], fetch,
                     now=now.isoformat())
    return snapshot, old.get("revision") != revision, assets


def download_video(vid, now):
    """Retry failures on the next run; only verified completed bytes count as held."""
    directory = ROOT / "videos" / vid / "download"
    manifest_path = directory / "manifest.json"
    # Reuse the already held AVC corpus by an immutable hard link. It is a
    # historical capture, not a claim that today's remote download succeeded.
    existing = ROOT.parent.parent / "videos" / "2026-avc" / f"{vid}.mkv"
    if not manifest_path.exists() and existing.is_file():
        directory.mkdir(parents=True, exist_ok=True)
        target = directory / existing.name
        if not target.exists():
            try:
                os.link(existing, target)
            except OSError:
                shutil.copyfile(existing, target)
        manifest = {"indexed_at": now.isoformat(), "source": "existing videos/2026-avc corpus",
                    "captured_at": None, "files": [{"file": target.name,
                        "bytes": target.stat().st_size,
                        "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}]}
        atomic_json(manifest_path, manifest)
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        if all((directory / item["file"]).is_file()
               and hashlib.sha256((directory / item["file"]).read_bytes()).hexdigest() == item["sha256"]
               for item in manifest.get("files", [])) and manifest.get("files"):
            return manifest
    command = shutil.which("yt-dlp")
    if not command:
        raise RuntimeError("yt-dlp is missing; install with uv tool install yt-dlp")
    directory.mkdir(parents=True, exist_ok=True)
    result = subprocess.run([
        command, "--ignore-config", *cookie_args(), "--no-playlist", "--no-progress", "--no-overwrites",
        "--socket-timeout", "30", "--retries", "2", "--write-info-json", "--write-description",
        "--write-thumbnail", "--write-subs", "--write-auto-subs", "--sub-langs", "all",
        "-f", "bv*[vcodec^=avc1]+ba/b[vcodec^=avc1]/bv*+ba/b",
        "--merge-output-format", "mkv", "-o", str(directory / "%(id)s.%(ext)s"),
        f"https://www.youtube.com/watch?v={vid}"], capture_output=True, text=True, timeout=900)
    atomic_bytes(directory / "download.log", (result.stdout + result.stderr).encode())
    if result.returncode:
        raise RuntimeError(f"yt-dlp exited {result.returncode}; see videos/{vid}/download/download.log")
    files = [{"file": path.name, "bytes": path.stat().st_size,
              "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
             for path in directory.iterdir() if path.suffix in (".mp4", ".mkv", ".webm")]
    if not files:
        raise RuntimeError("downloader returned success without a completed video file")
    manifest = {"captured_at": now.isoformat(), "files": files,
                "format_policy": "best available AVC video + audio, fallback best available"}
    atomic_json(manifest_path, manifest)
    return manifest


def capture_comments(vid, now):
    """Daily full comment extraction, including replies when exposed by YouTube."""
    directory = ROOT / "videos" / vid / "comments" / f"{now:%Y-%m-%d}"
    complete = directory / "complete.json"
    if complete.exists():
        return json.loads(complete.read_text())
    command = shutil.which("yt-dlp")
    if not command:
        raise RuntimeError("yt-dlp unavailable for comments")
    directory.mkdir(parents=True, exist_ok=True)
    result = subprocess.run([
        command, "--ignore-config", *cookie_args(), "--no-playlist", "--no-progress", "--skip-download",
        "--socket-timeout", "30", "--retries", "2", "--write-info-json", "--write-comments",
        "-o", str(directory / "%(id)s.%(ext)s"), f"https://www.youtube.com/watch?v={vid}"],
        capture_output=True, text=True, timeout=900)
    atomic_bytes(directory / "capture.log", (result.stdout + result.stderr).encode())
    info_path = directory / f"{vid}.info.json"
    if result.returncode or not info_path.exists():
        raise RuntimeError(f"comment extraction failed; see videos/{vid}/comments/{now:%Y-%m-%d}/capture.log")
    info = json.loads(info_path.read_text())
    comments = info.get("comments")
    # Empty or partial extraction has no measured detection floor. Retain output
    # but do not advertise it as successful enumeration.
    if not isinstance(comments, list) or not comments or "WARNING:" in result.stderr:
        raise RuntimeError(f"comments incomplete/empty or extractor warning; inspect videos/{vid}/comments")
    summary = {"captured_at": now.isoformat(), "comments_held": len(comments),
               "reported_comment_count": info.get("comment_count"),
               "completeness": "extractor finished; deleted/filtered/unexposed comments may be absent"}
    atomic_json(complete, summary)
    return summary


def build_comment_page(vid, summary):
    day = summary["captured_at"][:10]
    directory = ROOT / "videos" / vid / "comments" / day
    info = json.loads((directory / f"{vid}.info.json").read_text())
    escape = lambda value: html.escape(str(value or ""), quote=True)
    parts = ["<!doctype html><meta charset='utf-8'><title>Archived YouTube comments</title>",
             "<style>body{max-width:850px;margin:30px auto;background:#111;color:#eee;font:16px system-ui}article{border-bottom:1px solid #444;padding:12px}p{white-space:pre-wrap}a{color:#69bfff}.reply{margin-left:30px}</style>",
             f"<h1>Archived comments · {escape(vid)}</h1><p>Captured {escape(summary['captured_at'])}. "
             "Replies link to their parent. This is a local snapshot; deleted or filtered comments may be absent.</p>"]
    for comment in info.get("comments") or []:
        parent = comment.get("parent")
        parts.append(f"<article id='{escape(comment.get('id'))}' class='{'reply' if parent != 'root' else ''}'>"
                     f"<b>{escape(comment.get('author'))}</b> · {escape(comment.get('timestamp'))}")
        if parent and parent != "root":
            parts.append(f" · <a href='#{escape(parent)}'>Parent comment</a>")
        parts.append(f"<p>{escape(comment.get('text'))}</p></article>")
    atomic_bytes(directory / "index.html", "\n".join(parts).encode())


def run(video_ids, retry=False):
    now = datetime.now(timezone.utc)
    previous_path = ROOT / "index.json"
    previous = json.loads(previous_path.read_text()) if previous_path.exists() else {}
    videos = dict(previous.get("videos") or {})
    errors, events = {}, []
    feed = video_ids if isinstance(video_ids, dict) else {}
    # Recheck everything ever seen, even after it ages out of the channel RSS.
    for vid in sorted(set(video_ids) | set(videos)):
        entry = dict(videos.get(vid) or {})
        prior_errors = entry.get("errors") or {}
        entry["last_attempt"] = now.isoformat()
        entry["errors"] = {}
        try:
            snapshot, changed, thumbnails = capture_video(vid, now)
            entry.update(title=snapshot["metadata"].get("title"),
                         captured_at=now.isoformat(), revision=snapshot["revision"])
            if changed:
                events.append(f"YouTube {vid}: watch page, player and description revision archived")
            if any(a["status"] != "held" for a in thumbnails):
                entry["errors"]["thumbnails"] = "one or more thumbnail requests failed"
        except Exception as exc:
            entry["errors"]["page"] = f"{type(exc).__name__}: {exc}"
            if vid in feed:
                item = feed[vid]
                entry["title"] = item.get("title")
                directory = ROOT / "videos" / vid
                rss = {"captured_at": now.isoformat(), "source": "channel RSS",
                       "metadata": {"videoId": vid, "channelId": CHANNEL_ID, **item}}
                atomic_json(directory / "rss-latest.json", rss)
                # Keep a readable current description even when the player is
                # gated. Its source is explicitly recorded alongside it.
                atomic_bytes(directory / "description.txt", (item.get("description") or "").encode())
        for leg, method in (("download", download_video), ("comments", capture_comments)):
            last_failed = entry.get("retry_after", {}).get(leg)
            if last_failed and not retry and now.timestamp() < last_failed:
                entry["errors"][leg] = prior_errors.get(leg, "retry deferred")
                continue
            try:
                entry[leg] = method(vid, now)
                if leg == "comments":
                    build_comment_page(vid, entry[leg])
                entry.setdefault("retry_after", {}).pop(leg, None)
            except Exception as exc:
                entry["errors"][leg] = f"{type(exc).__name__}: {exc}"
                entry.setdefault("retry_after", {})[leg] = now.timestamp() + 21600
        videos[vid] = entry
        if entry["errors"]:
            errors[vid] = entry["errors"]
        # A later download timeout must not lose already captured progress.
        atomic_json(previous_path, {"generated_at": now.isoformat(), "videos": videos, "errors": errors})
    try:
        page = fetch("https://www.youtube.com/@qtecqot/about")
        atomic_bytes(ROOT / "channel" / f"{now:%Y%m%dT%H%M%SZ}.html.gz", gzip.compress(page, mtime=0))
    except Exception as exc:
        errors["channel"] = f"{type(exc).__name__}: {exc}"
    atomic_json(previous_path, {"generated_at": now.isoformat(), "videos": videos, "errors": errors})
    return events, errors
