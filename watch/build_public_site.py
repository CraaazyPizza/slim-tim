#!/usr/bin/env python3.12
"""Build the reviewed, self-contained GitHub Pages edition of the timeline.

Publication is fail-closed: timeline entries and media hashes must be explicitly
listed in timeline/publication.json. New captures therefore remain local until a
person reviews them and adds them to the inclusion manifest.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import build_timeline


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
CONFIG = ROOT / "timeline" / "publication.json"
ALLOWED_MEDIA_ROOTS = ((ROOT / "x" / "media").resolve(),
                       (REPO / "qtecqot-x-recovered" / "media").resolve())
PUBLIC_SOURCE_HOSTS = {"web.archive.org"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def output_directory(value: str) -> Path:
    path = Path(value).expanduser().resolve()
    forbidden = {Path("/").resolve(), Path.home().resolve(), ROOT.resolve(), REPO.resolve()}
    if path in forbidden:
        raise argparse.ArgumentTypeError(f"refusing broad output directory: {path}")
    return path


def make_output(path: Path) -> None:
    if path.exists() and any(path.iterdir()):
        raise RuntimeError(f"output directory is not empty: {path}")
    path.mkdir(parents=True, exist_ok=True)
    (path / "media").mkdir()


def public_source_links(entry: dict) -> list[dict]:
    links = []
    for link in entry.get("source_links") or []:
        href = link.get("href") or ""
        if urlparse(href).hostname in PUBLIC_SOURCE_HOSTS:
            links.append({"label": link.get("label") or "Archived source", "href": href})
    return links


def copy_reviewed_media(entry: dict, output: Path, reviewed_hashes: set[str],
                        assets: dict[str, dict]) -> None:
    for media in entry.get("media") or []:
        source_ref = media.get("src")
        if not source_ref:
            continue
        source = (ROOT / "timeline" / source_ref).resolve()
        if not any(source.is_relative_to(root) for root in ALLOWED_MEDIA_ROOTS):
            raise RuntimeError(f"media path escapes reviewed roots: {source}")
        if not source.is_file():
            raise RuntimeError(f"reviewed media is missing: {source}")
        digest = sha256(source)
        if digest not in reviewed_hashes:
            raise RuntimeError(f"unreviewed media hash for {entry['id']}: {digest} ({source.name})")
        suffix = source.suffix.lower()
        target_name = f"{digest[:24]}{suffix}"
        target = output / "media" / target_name
        if target.exists() and sha256(target) != digest:
            raise RuntimeError(f"publication media-name collision: {target_name}")
        if not target.exists():
            shutil.copyfile(source, target)
        media["src"] = f"media/{target_name}"
        assets[target_name] = {
            "path": f"media/{target_name}",
            "sha256": digest,
            "bytes": target.stat().st_size,
        }


def sanitize_entry(entry: dict, output: Path, reviewed_hashes: set[str],
                   assets: dict[str, dict]) -> dict:
    result = copy.deepcopy(entry)
    author = result.get("author") or {}
    handle = author.get("handle") or "unknown"
    # Handles are timeline context. Remote avatars and real-name display fields are
    # not part of the reviewed public bundle.
    result["author"] = {"handle": handle, "name": handle, "avatar": None}
    result["source_links"] = public_source_links(result)
    copy_reviewed_media(result, output, reviewed_hashes, assets)
    return result


def recalculate_counts(data: dict) -> None:
    entries = data["entries"]
    counts = data["counts"]
    counts.update({
        "entries": len(entries),
        "posts": sum(e.get("kind") == "post" for e in entries),
        "replies": sum(e.get("kind") == "reply" for e in entries),
        "reposts": sum(e.get("kind") in ("repost", "timeline_item") for e in entries),
        "deleted": sum(e.get("state") == "deleted" for e in entries),
        "with_media": sum(any(m.get("src") for m in e.get("media") or []) for e in entries),
        "missing_media_entries": sum(any(m.get("kind") == "missing"
                                             for m in e.get("media") or []) for e in entries),
        "missing_media_assets": sum(m.get("kind") == "missing" for e in entries
                                    for m in e.get("media") or []),
    })


def build(output: Path) -> dict:
    make_output(output)
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    included_ids = config["include_entry_ids"]
    if len(included_ids) != len(set(included_ids)):
        raise RuntimeError("publication entry allowlist contains duplicates")
    reviewed_hashes = set(config["include_asset_sha256"])

    data = build_timeline.build_data()
    held = {entry["id"]: entry for entry in data["entries"]}
    missing = [status_id for status_id in included_ids if status_id not in held]
    if missing:
        raise RuntimeError(f"reviewed timeline entries are no longer available: {missing}")

    assets: dict[str, dict] = {}
    data["entries"] = [sanitize_entry(held[status_id], output, reviewed_hashes, assets)
                       for status_id in included_ids]
    data["entries"].sort(key=lambda entry: entry.get("timeline_at") or "", reverse=True)
    data["generated_at"] = datetime.now(timezone.utc).isoformat()
    recalculate_counts(data)

    structured = (data.get("health") or {}).get("structured") or {}
    structured.pop("pid", None)
    structured.pop("reported_errors", None)
    data["publication"] = {
        "mode": "reviewed public snapshot",
        "reviewed_at": config["reviewed_at"],
        "entry_count": len(data["entries"]),
        "asset_count": len(assets),
        "asset_bytes": sum(item["bytes"] for item in assets.values()),
        "note": ("This static copy is built only from individually reviewed timeline entries "
                 "and media. The continuously updated watcher remains local."),
    }

    manifest = {
        "schema": 1,
        "generated_at": data["generated_at"],
        "account": "qtecqot",
        "included_entry_ids": [entry["id"] for entry in data["entries"]],
        "included_entry_fields": sorted({key for entry in data["entries"] for key in entry}),
        "included_assets": sorted(assets.values(), key=lambda item: item["path"]),
        "included_site_files": [".nojekyll", "data.json", "index.html", "publication-manifest.json"],
    }

    json_text = json.dumps(data, ensure_ascii=False, indent=2)
    embedded = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    embedded = embedded.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    html = build_timeline.HTML.replace("__TIMELINE_DATA__", embedded)
    html = html.replace("@qtecqot offline timeline", "@qtecqot public timeline archive")
    html = html.replace("@qtecqot · reconstructed timeline",
                        "@qtecqot · reviewed public archive snapshot")
    notice = ("<section class=\"system\"><strong>Public snapshot.</strong> "
              "Every included entry and media asset was reviewed before publication. "
              "The local watcher continues updating separately.</section>")
    html = html.replace("<main>", "<main>" + notice, 1)

    (output / ".nojekyll").write_text("", encoding="utf-8")
    (output / "data.json").write_text(json_text + "\n", encoding="utf-8")
    (output / "index.html").write_text(html, encoding="utf-8")
    (output / "publication-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # These invariants catch the two most damaging publication regressions: local
    # raw-record links and an accidentally inherited credential.
    complete = "\n".join(path.read_text(encoding="utf-8", errors="replace")
                         for path in (output / "index.html", output / "data.json",
                                      output / "publication-manifest.json"))
    forbidden = ("../x/", "qtecqot-x-recovered/raw", "Bearer Token", "AAAAAAAA")
    leaked = [needle for needle in forbidden if needle in complete]
    if leaked:
        raise RuntimeError(f"public output contains forbidden local/credential material: {leaked}")
    return data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=output_directory,
                        help="new or empty directory for the reviewed static site")
    args = parser.parse_args()
    data = build(args.output)
    publication = data["publication"]
    print(f"wrote {args.output}")
    print(f"entries={publication['entry_count']} assets={publication['asset_count']} "
          f"bytes={publication['asset_bytes']}")


if __name__ == "__main__":
    main()
