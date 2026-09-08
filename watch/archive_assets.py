"""URL-indexed, hash-verified local assets; originals and failures remain inspectable."""
from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit


def atomic_bytes(path: Path, body: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".capture-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(body)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def atomic_json(path: Path, value):
    atomic_bytes(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode())


def canonical_url(url: str) -> str:
    parts = urlsplit(url)
    if parts.hostname == "pbs.twimg.com" and parts.path.startswith("/media/"):
        query = parse_qs(parts.query)
        suffix = Path(parts.path).suffix.lstrip(".")
        fmt = (query.get("format") or [suffix or "jpg"])[0]
        path = parts.path[:-len(suffix)-1] if suffix in ("jpg", "jpeg", "png", "webp") else parts.path
        return urlunsplit((parts.scheme, parts.netloc, path,
                           urlencode({"format": fmt, "name": "orig"}), ""))
    return url


def manifest_path(media: Path, owner: str) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9_-]+", owner):
        raise ValueError("invalid asset owner")
    return media.parent / "assets" / f"{owner}.json"


def read_manifest(media: Path, owner: str) -> dict:
    path = manifest_path(media, owner)
    return json.loads(path.read_text()) if path.exists() else {"schema": 1, "owner": owner, "assets": {}}


def capture(media: Path, owner: str, urls: list[str], fetch, *, now=None) -> list[dict]:
    """Never infer a URL-to-file mapping from the legacy enumeration filenames.

    Stored bytes are immutable and content-addressed. Successful assets are reused
    only after length and SHA-256 verification. Failed requests remain retryable.
    """
    now = now or datetime.now(timezone.utc).isoformat()
    manifest = read_manifest(media, owner)
    before = json.dumps(manifest, sort_keys=True)
    items = []
    for source in sorted(set(urls)):
        url = canonical_url(source)
        old = manifest["assets"].get(url) or {}
        item = dict(old)
        item.update({"url": url, "source_urls": sorted(set(old.get("source_urls", [])) | {source}),
                     "first_seen": old.get("first_seen") or now})
        held = media / old.get("file", ".missing")
        valid = (old.get("status") == "held" and held.is_file()
                 and held.stat().st_size == old.get("bytes")
                 and hashlib.sha256(held.read_bytes()).hexdigest() == old.get("sha256"))
        if not valid:
            try:
                body = fetch(url)
                if not body:
                    raise ValueError("empty response")
                digest = hashlib.sha256(body).hexdigest()
                parts = urlsplit(url)
                ext = (parse_qs(parts.query).get("format") or [Path(parts.path).suffix.lstrip(".")])[0]
                ext = ext if re.fullmatch(r"[A-Za-z0-9]{1,5}", ext or "") else "bin"
                filename = f"{owner}_{digest}.{ext}"
                atomic_bytes(media / filename, body)
                item.update(status="held", file=filename, sha256=digest, bytes=len(body), retrieved_at=now)
                for key in ("error", "http_status", "last_failed_at"):
                    item.pop(key, None)
            except Exception as exc:
                code = getattr(exc, "code", None)
                item.update(status="unavailable" if code in (404, 410) else "retry",
                            http_status=code, error=type(exc).__name__, last_failed_at=now)
        manifest["assets"][url] = item
        items.append(item)
    if json.dumps(manifest, sort_keys=True) != before:
        atomic_json(manifest_path(media, owner), manifest)
    return items
