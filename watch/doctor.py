#!/usr/bin/env python3.12
"""Read-only operational audit for the @qtecqot capture stack."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import xapi_client


ROOT = Path(__file__).resolve().parent
XDIR = ROOT / "x"
NOW = datetime.now(timezone.utc)


def age_minutes(value: str) -> float:
    then = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return (NOW - then).total_seconds() / 60


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    passes: list[str] = []

    try:
        state = json.loads((XDIR / "state.json").read_text())
        statuses = state["handles"]["qtecqot"]["statuses"]
        passes.append(f"state JSON valid: {len(statuses)} known status IDs")
        full = state["handles"]["qtecqot"].get("official_x", {}).get("backfilled_at")
        if not full or age_minutes(full) > 90:
            warnings.append(f"full X timeline enumeration stale or missing: {full}")
        else:
            passes.append(f"full X timeline enumeration current: {age_minutes(full):.1f} minutes")
    except Exception as exc:
        failures.append(f"state JSON unusable: {type(exc).__name__}: {exc}")

    try:
        health = json.loads((XDIR / "health.json").read_text())
        age = age_minutes(health["generated_at"])
        if age > 10:
            failures.append(f"watcher heartbeat stale: {age:.1f} minutes")
        else:
            passes.append(f"watcher heartbeat current: {age:.1f} minutes")
        for name, item in (health.get("legs") or {}).items():
            if item.get("status") in ("error", "unconfigured"):
                warnings.append(f"{name}: {item.get('status')} — {item.get('detail')}")
    except Exception as exc:
        failures.append(f"health JSON unusable: {type(exc).__name__}: {exc}")

    cron = subprocess.run(["/usr/bin/systemctl", "is-active", "cron"],
                          capture_output=True, text=True)
    if cron.returncode:
        failures.append("cron service is not active")
    else:
        passes.append("cron service active")
    schedule = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    if "watch/xwatch.py --quiet --commit" not in schedule.stdout:
        failures.append("two-minute xwatch crontab entry missing")
    else:
        passes.append("two-minute xwatch schedule installed")

    bad_json = []
    for directory in (XDIR / "raw", XDIR / "api_raw"):
        for path in directory.glob("*.json"):
            try:
                json.loads(path.read_text())
            except Exception:
                bad_json.append(str(path.relative_to(ROOT)))
    if bad_json:
        failures.append(f"unreadable archived JSON: {', '.join(bad_json[:5])}")
    else:
        passes.append("all local raw/API records parse as JSON")

    empty_media = [path.name for path in (XDIR / "media").iterdir()
                   if path.is_file() and path.stat().st_size == 0]
    if empty_media:
        failures.append(f"zero-byte media files: {', '.join(empty_media[:5])}")
    else:
        media = [path for path in (XDIR / "media").iterdir() if path.is_file()]
        passes.append(f"{len(media)} local media files are non-empty")

    try:
        with urllib.request.urlopen("http://127.0.0.1:8765/timeline/data.json", timeout=3) as response:
            viewer = json.loads(response.read())
        passes.append(f"localhost viewer responding: {viewer['counts']['entries']} entries")
        if age_minutes(viewer["generated_at"]) > 10:
            failures.append("viewer data is stale despite the server responding")
        missing = viewer["counts"].get("missing_media_assets", 0)
        if missing:
            warnings.append(f"viewer identifies {missing} expected attachments without local bytes")
    except Exception as exc:
        failures.append(f"localhost viewer unavailable: {type(exc).__name__}: {exc}")

    if xapi_client.bearer_token():
        passes.append("official X API bearer token configured (value not displayed)")
    else:
        warnings.append("official X API bearer token not configured; reply coverage is degraded")

    try:
        youtube = json.loads((ROOT / "youtube" / "index.json").read_text())
        if age_minutes(youtube["generated_at"]) > 120:
            failures.append("YouTube content capture is stale (>120 minutes)")
        else:
            passes.append(f"YouTube index current: {len(youtube['videos'])} videos")
        for vid, entry in youtube["videos"].items():
            if not entry.get("download", {}).get("files"):
                warnings.append(f"YouTube {vid}: no completed video download")
            for leg, detail in entry.get("errors", {}).items():
                warnings.append(f"YouTube {vid} {leg}: {detail}")
    except Exception as exc:
        warnings.append(f"YouTube content index unavailable: {type(exc).__name__}")

    free = shutil.disk_usage(ROOT).free / 1024**3
    if free < 1:
        failures.append(f"archive disk nearly full: {free:.1f} GiB free")
    elif free < 10:
        warnings.append(f"archive disk space low: {free:.1f} GiB free")

    for line in passes:
        print(f"PASS  {line}")
    for line in warnings:
        print(f"WARN  {line}")
    for line in failures:
        print(f"FAIL  {line}")
    print(f"\n{len(passes)} passed, {len(warnings)} warning(s), {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
