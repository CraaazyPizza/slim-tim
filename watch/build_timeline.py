#!/usr/bin/env python3.12
"""Build the offline @qtecqot timeline viewer from the held archive.

The output has no network dependencies. It links to media and raw records already
held in this repository, and it keeps authored posts, replies, explicit reposts,
and observed third-party timeline items distinct.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
XDIR = ROOT / "x"
API_RAW = XDIR / "api_raw"
RECOVERED = REPO / "qtecqot-x-recovered"
OUT = ROOT / "timeline"
ACCOUNT = "qtecqot"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def iso_time(value: str | None) -> str | None:
    if not value:
        return None
    try:
        if re.match(r"^[A-Z][a-z]{2} ", value):
            dt = parsedate_to_datetime(value)
        else:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except (TypeError, ValueError, OverflowError):
        return value


def metrics_from(mapping: dict) -> dict:
    aliases = {
        "replies": ("replies", "reply_count"),
        "reposts": ("reposts", "retweets", "repost_count", "retweet_count"),
        "quotes": ("quotes", "quote_count"),
        "likes": ("likes", "like_count"),
        "bookmarks": ("bookmarks", "bookmark_count"),
        "views": ("views", "impression_count"),
    }
    result = {}
    for label, keys in aliases.items():
        for key in keys:
            if mapping.get(key) is not None:
                result[label] = mapping[key]
                break
    return result


def v2_parts(doc: dict) -> tuple[dict, dict, dict[str, dict], dict[str, dict]]:
    data = doc.get("data") or {}
    includes = doc.get("includes") or {}
    users = {str(user.get("id")): user for user in includes.get("users") or []}
    tweets = {str(tweet.get("id")): tweet
              for tweet in (includes.get("posts") or includes.get("tweets") or [])}
    return data, includes, users, tweets


def best_text(tweet: dict) -> str:
    note = tweet.get("note_post") or tweet.get("note_tweet") or {}
    return note.get("text") or tweet.get("text") or ""


def expanded_text(tweet: dict) -> str:
    """Use the readable destination behind t.co whenever the API supplied it."""
    text = best_text(tweet)
    note = tweet.get("note_post") or tweet.get("note_tweet") or {}
    entities = note.get("entities") or tweet.get("entities") or {}
    for item in entities.get("urls") or []:
        short = item.get("url")
        destination = item.get("unwound_url") or item.get("expanded_url")
        if short and destination:
            text = text.replace(short, destination)
    return text


def referenced_media(v2: dict, kind: str) -> list[dict]:
    """Return only media belonging to this post, or to the post it reposts.

    Included media on replies can belong to the parent. Treating every included
    object as an attachment caused a documented false attribution in this repo.
    """
    data, includes, _, tweets = v2_parts(v2)
    target = data
    origin = "attached media"
    if kind == "repost":
        refs = data.get("referenced_posts") or data.get("referenced_tweets") or []
        ref = next((r for r in refs if r.get("type") in ("retweeted", "reposted")), None)
        if ref and str(ref.get("id")) in tweets:
            target = tweets[str(ref["id"])]
            origin = "media from reposted item"
    keys = set((target.get("attachments") or {}).get("media_keys") or [])
    found = []
    for media in includes.get("media") or []:
        if media.get("media_key") not in keys:
            continue
        url = media.get("url") or media.get("preview_image_url")
        if media.get("type") in ("video", "animated_gif"):
            variants = [v for v in media.get("variants") or []
                        if v.get("content_type") == "video/mp4"]
            variants.sort(key=lambda v: v.get("bit_rate") or 0, reverse=True)
            if variants:
                url = variants[0].get("url")
        found.append({"kind": media.get("type") or "media", "url": url,
                      "label": origin})
    return found


def local_media(status_id: str, allow: bool) -> list[dict]:
    if not allow:
        return []
    files = []
    for path in sorted((XDIR / "media").glob(f"{status_id}_*")):
        suffix = path.suffix.lower()
        if suffix in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
            kind = "image"
        elif suffix in (".mp4", ".webm", ".mov"):
            kind = "video"
        else:
            continue
        files.append({"kind": kind, "src": f"../x/media/{path.name}",
                      "label": "Locally archived media", "bytes": path.stat().st_size})
    return files


def first_b2_failure() -> str | None:
    path = XDIR / "CHANGELOG.md"
    if not path.exists():
        return None
    current = None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
        if "leg B2 (replies): x_search FAILED: HTTPError 403" in line:
            return iso_time(current)
    return None


def latest_check() -> dict:
    path = XDIR / "check.log"
    if not path.exists():
        return {}
    lines = [line for line in path.read_text().splitlines() if line.strip()]
    if not lines:
        return {}
    line = lines[-1]
    result = {"raw": line, "at": iso_time(line.split()[0])}
    for key in ("changes", "notes", "errors"):
        match = re.search(rf"\b{key}=(\d+)", line)
        if match:
            result[key] = int(match.group(1))
    return result


def normalize(status_id: str, state_meta: dict, current: dict | None,
              official: dict | None, recovered: dict | None,
              referenced_ids: set[str], gone_urls: set[str]) -> dict | None:
    fx = (current or {}).get("tweet") or {}
    fx_author = fx.get("author") or {}
    fx_handle = fx_author.get("screen_name") or ""

    v2 = official or recovered or {}
    v2_data, v2_includes, v2_users, v2_tweets = v2_parts(v2)
    refs = v2_data.get("referenced_posts") or v2_data.get("referenced_tweets") or []
    ref_type = refs[0].get("type") if refs else None

    # A separately held original that already appears through explicit retweet
    # wrappers is supporting evidence, not a third timeline event.
    if not v2 and fx_handle.lower() != ACCOUNT and status_id in referenced_ids:
        return None

    if ref_type in ("retweeted", "reposted"):
        kind = "repost"
    elif ref_type in ("replied_to", "replied") or fx.get("replying_to"):
        kind = "reply"
    elif fx_handle and fx_handle.lower() != ACCOUNT:
        kind = "timeline_item"
    else:
        kind = "post"

    original_tweet = None
    original_author = None
    if kind == "repost" and refs:
        original_tweet = v2_tweets.get(str(refs[0].get("id")))
        if original_tweet:
            original_author = v2_users.get(str(original_tweet.get("author_id")))

    if kind in ("repost", "timeline_item") and fx_handle and fx_handle.lower() != ACCOUNT:
        author = {"handle": fx_handle, "name": fx_author.get("name") or fx_handle,
                  "avatar": fx_author.get("avatar_url")}
        text = fx.get("text") or ""
        metric_source = fx
    elif kind == "repost" and original_tweet:
        original_author = original_author or {}
        author = {"handle": original_author.get("username") or "unknown",
                  "name": original_author.get("name") or original_author.get("username") or "Unknown"}
        text = expanded_text(original_tweet)
        metric_source = original_tweet.get("public_metrics") or {}
    else:
        v2_author = v2_users.get(str(v2_data.get("author_id"))) or {}
        author = {"handle": fx_handle or v2_author.get("username") or ACCOUNT,
                  "name": fx_author.get("name") or v2_author.get("name") or ACCOUNT,
                  "avatar": fx_author.get("avatar_url") or v2_author.get("profile_image_url")}
        text = fx.get("text") or expanded_text(v2_data)
        metric_source = fx or v2_data.get("public_metrics") or {}

    wrapper_at = iso_time(v2_data.get("created_at"))
    original_at = iso_time(fx.get("created_at"))
    observed_at = iso_time(state_meta.get("first_seen"))
    if wrapper_at:
        timeline_at = wrapper_at
    elif fx_handle.lower() == ACCOUNT:
        timeline_at = original_at or observed_at
    else:
        timeline_at = observed_at or original_at

    is_explicit_timeline_record = bool(v2 or fx_handle.lower() == ACCOUNT or
                                       (fx.get("reposted_by") or {}).get("screen_name") == ACCOUNT)
    allow_media = bool(current) or kind == "repost"
    media = local_media(status_id, allow_media)
    remote_media = referenced_media(v2, kind) if v2 else []
    if current:
        all_media = ((fx.get("media") or {}).get("all") or [])
        remote_media = [{"kind": item.get("type") or "media", "url": item.get("url"),
                         "label": "media URL in captured record"} for item in all_media]

    missing = []
    if len(media) < len(remote_media):
        for item in remote_media[len(media):]:
            missing.append({"kind": "missing", "url": item.get("url"),
                            "label": "Asset unavailable locally",
                            "gone": item.get("url") in gone_urls})
    media.extend(missing)

    if state_meta.get("state") == "deleted":
        if state_meta.get("last_live"):
            deletion_label = (f"Last verified live {state_meta['last_live']}; deletion noticed "
                              f"{state_meta.get('deleted_noticed', 'at an unknown time')}.")
        else:
            deletion_label = (f"Deletion confirmed {state_meta.get('deleted_noticed', 'during recovery')}; "
                              "the exact deletion time is unknown.")
    else:
        deletion_label = None

    source_links = []
    if current:
        source_links.append({"label": "Captured JSON", "href": f"../x/raw/{status_id}.json"})
    if official:
        source_links.append({"label": "Official X API record",
                             "href": f"../x/api_raw/{status_id}.json"})
    if recovered:
        source_links.append({"label": "Recovered API record",
                             "href": f"../../qtecqot-x-recovered/raw/{status_id}.json"})
        stamp = re.sub(r"\D", "", v2_data.get("created_at") or "")[:14]
        if stamp:
            source_links.append({"label": "Wayback capture",
                                 "href": (f"https://web.archive.org/web/{stamp}id_/"
                                          f"https://twitter.com/{ACCOUNT}/status/{status_id}")})

    parent_id = None
    parent_handle = None
    if kind == "reply":
        parent_id = str(refs[0].get("id")) if refs else fx.get("replying_to_status")
        parent_handle = fx.get("replying_to")
        if not parent_handle:
            mentions = (v2_data.get("entities") or {}).get("mentions") or []
            parent_handle = mentions[0].get("username") if mentions else None

    profile_at_post = None
    if v2:
        u = v2_users.get(str(v2_data.get("author_id"))) or {}
        profile_at_post = metrics_from(u.get("public_metrics") or {})
        raw_profile = u.get("public_metrics") or {}
        profile_at_post.update({
            "followers": raw_profile.get("followers_count"),
            "following": raw_profile.get("following_count"),
            "posts": raw_profile.get("post_count", raw_profile.get("tweet_count")),
            "media": raw_profile.get("media_count"),
        })
        profile_at_post = {k: v for k, v in profile_at_post.items() if v is not None}

    if kind == "timeline_item":
        provenance = ("Third-party status observed by the watcher while enumerating @qtecqot's "
                      "timeline. It is presented as a repost/timeline item, not as his authorship. "
                      "Current presence of the repost itself is not independently verified.")
    elif official and current:
        provenance = "Official X API record plus a secondary live watcher capture."
    elif official:
        provenance = "Captured from the official X API user timeline."
    elif recovered and current:
        provenance = "Recovered API record plus a later live watcher capture."
    elif recovered:
        provenance = "Recovered from an archived Twitter API v2 lookup."
    else:
        provenance = "Captured by the local watcher while available."

    canonical_url = fx.get("url") or f"https://x.com/{ACCOUNT}/status/{status_id}"
    if kind in ("post", "reply", "repost"):
        canonical_url = f"https://x.com/{ACCOUNT}/status/{status_id}"

    return {
        "id": status_id,
        "status_id": status_id,
        "kind": kind,
        "state": state_meta.get("state") or "unknown",
        "timeline_at": timeline_at,
        "original_at": original_at if kind == "timeline_item" else None,
        "observed_at": observed_at,
        "author": author,
        "text": text,
        "metrics": metrics_from(metric_source),
        "metrics_context": "original post engagement" if kind in ("repost", "timeline_item") else "engagement at capture",
        "parent_id": parent_id,
        "parent_handle": parent_handle,
        "deleted_noticed": iso_time(state_meta.get("deleted_noticed")),
        "last_live": iso_time(state_meta.get("last_live")),
        "deletion_label": deletion_label,
        "first_seen": observed_at,
        "profile_at_post": profile_at_post,
        "conversation_id": v2_data.get("conversation_id") or fx.get("conversation_id"),
        "language": v2_data.get("lang") or fx.get("lang"),
        "source": v2_data.get("source") or fx.get("source"),
        "possibly_sensitive": v2_data.get("possibly_sensitive", fx.get("possibly_sensitive")),
        "reply_settings": v2_data.get("reply_settings"),
        "edit_history_ids": (v2_data.get("edit_history_post_ids") or
                             v2_data.get("edit_history_tweet_ids") or []),
        "edit_controls": v2_data.get("edit_controls") or {},
        "media": media,
        "has_local_media": any(item.get("src") for item in media),
        "provenance": provenance,
        "source_links": source_links,
        "canonical_url": canonical_url,
        "explicit_timeline_record": is_explicit_timeline_record,
    }


def build_data() -> dict:
    state = read_json(XDIR / "state.json")
    handle_state = state["handles"][ACCOUNT]
    statuses = handle_state.get("statuses") or {}
    gone_path = XDIR / "media_gone.json"
    gone_urls = set(read_json(gone_path)) if gone_path.exists() else set()

    current_paths = {p.stem: p for p in (XDIR / "raw").glob("*.json")}
    official_paths = {p.stem: p for p in API_RAW.glob("*.json")}
    recovered_paths = {p.stem: p for p in (RECOVERED / "raw").glob("*.json")
                       if not p.name.startswith("_")}
    current_docs = {sid: read_json(path) for sid, path in current_paths.items()}
    official_docs = {sid: read_json(path) for sid, path in official_paths.items()}
    recovered_docs = {sid: read_json(path) for sid, path in recovered_paths.items()}

    referenced_ids = set()
    for doc in list(recovered_docs.values()) + list(official_docs.values()):
        data = doc.get("data") or {}
        for ref in data.get("referenced_posts") or data.get("referenced_tweets") or []:
            if ref.get("type") in ("retweeted", "reposted"):
                referenced_ids.add(str(ref.get("id")))

    entries = []
    for status_id in sorted(set(statuses) | set(current_docs) | set(official_docs) |
                            set(recovered_docs)):
        entry = normalize(status_id, statuses.get(status_id, {}), current_docs.get(status_id),
                          official_docs.get(status_id), recovered_docs.get(status_id),
                          referenced_ids, gone_urls)
        if entry:
            metrics_path = XDIR / "metrics" / f"{status_id}.json"
            if metrics_path.exists():
                history = read_json(metrics_path)
                if history:
                    entry["metrics"] = metrics_from(history[-1].get("values") or {})
                    entry["metrics_history_count"] = len(history)
                    entry["metrics_history_first"] = history[0].get("at")
                    entry["metrics_history_last"] = history[-1].get("at")
            revisions_dir = XDIR / "revisions" / status_id
            if revisions_dir.exists():
                revisions = sorted(revisions_dir.glob("*.json"))
                entry["revision_count"] = len(revisions)
                entry["source_links"].append({
                    "label": f"Content revisions ({len(revisions)})",
                    "href": f"../x/revisions/{status_id}/",
                })
            entries.append(entry)

    manual_path = OUT / "manual_entries.json"
    if manual_path.exists():
        entries.extend(read_json(manual_path))

    annotations_path = OUT / "annotations.json"
    if annotations_path.exists():
        annotations = read_json(annotations_path)
        for entry in entries:
            entry.update(annotations.get(entry["id"], {}))

    entries.sort(key=lambda entry: entry.get("timeline_at") or "", reverse=True)
    profile = handle_state.get("profile") or {}
    checks = latest_check()
    b2_failure = first_b2_failure()
    health_path = XDIR / "health.json"
    structured_health = read_json(health_path) if health_path.exists() else {}
    official_status = ((structured_health.get("legs") or {}).get("official_x_api") or {}).get("status")
    reply_degraded = official_status not in (None, "ok") if structured_health else \
        bool(b2_failure and checks.get("errors", 0))

    media_files = [path for path in (XDIR / "media").iterdir() if path.is_file()]
    missing_assets = sum(media.get("kind") == "missing" for entry in entries
                         for media in entry.get("media") or [])
    missing_entries = sum(any(media.get("kind") == "missing" for media in entry.get("media") or [])
                          for entry in entries)

    latencies = []
    for entry in entries:
        if not entry.get("first_seen") or not entry.get("timeline_at"):
            continue
        try:
            seen = datetime.fromisoformat(entry["first_seen"].replace("Z", "+00:00"))
            posted = datetime.fromisoformat(entry["timeline_at"].replace("Z", "+00:00"))
            seconds = (seen - posted).total_seconds()
            if 0 <= seconds <= 86400 * 7:
                latencies.append(seconds)
        except (TypeError, ValueError):
            pass
    latencies.sort()
    median_latency = latencies[len(latencies) // 2] if latencies else None

    counts = {
        "entries": len(entries),
        "posts": sum(e["kind"] == "post" for e in entries),
        "replies": sum(e["kind"] == "reply" for e in entries),
        "reposts": sum(e["kind"] in ("repost", "timeline_item") for e in entries),
        "deleted": sum(e["state"] == "deleted" for e in entries),
        "with_media": sum(e.get("has_local_media") or any(m.get("src") for m in e.get("media", []))
                          for e in entries),
        "missing_media_entries": missing_entries,
        "missing_media_assets": missing_assets,
        "local_media_files": len(media_files),
        "local_media_bytes": sum(path.stat().st_size for path in media_files),
        "official_api_records": len(official_docs),
        "revision_files": sum(1 for path in (XDIR / "revisions").glob("*/*.json")),
        "metric_snapshots": sum(len(read_json(path)) for path in (XDIR / "metrics").glob("*.json")),
    }
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "account": {
            "handle": ACCOUNT,
            "name": profile.get("name") or ACCOUNT,
            "joined": profile.get("joined"),
            "followers": profile.get("followers"),
            "following": profile.get("following"),
            "likes": profile.get("likes"),
            "posts": profile.get("tweets"),
            "media_count": profile.get("media_count"),
        },
        "counts": counts,
        "health": {
            "structured": structured_health,
            "last_check": checks,
            "reply_discovery_degraded": reply_degraded,
            "reply_discovery_failure_since": b2_failure,
            "coverage_note": ("Reply discovery is degraded; new replies can be missed. "
                              "Standalone timeline polling and known-status deletion checks continue."
                              if reply_degraded else
                              "Latest watcher check has no recorded reply-discovery failure."),
            "coverage_gaps": [
                {
                    "start": None,
                    "end": "2026-08-02T19:20:00+00:00",
                    "label": "Before automatic watcher installation",
                    "detail": ("Coverage is reconstructed from surviving/recovered records. "
                               "It cannot establish that no other posts or replies existed."),
                },
                {
                    "start": "2026-08-07T12:56:00+00:00",
                    "end": "2026-08-09T18:52:00+00:00",
                    "label": "Watcher outage",
                    "detail": ("State-file corruption stopped successful passes for 53h56m. "
                               "RSS/API recovery constrains this gap but does not prove completeness."),
                },
            ],
            "capture_latency": {
                "sample_size": len(latencies),
                "median_seconds": median_latency,
                "maximum_seconds": max(latencies) if latencies else None,
                "floor": ("Calculated only for records observed within seven days of their authored time; "
                          "recovered historical records are excluded."),
            },
            "detection_floor": (
                "The schedule runs every 2 minutes. With official X configured, each delta poll "
                "can enumerate up to 100 new posts/replies since the prior ID; a five-item edit "
                "probe runs every 10 minutes. Known statuses are swept at least every 30 minutes "
                "and immediately when profile counters move. A post created and deleted entirely "
                "between polls can still evade body capture, and no source can prove that such an "
                "event did not occur."
            ),
        },
        "entries": entries,
    }


HTML = r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>@qtecqot offline timeline</title>
  <style>
    :root{color-scheme:dark;--bg:#000;--panel:#080808;--soft:#151515;--line:#2f3336;--text:#e7e9ea;--muted:#71767b;--blue:#1d9bf0;--red:#f4212e;--amber:#ffb000;--green:#00ba7c}
    *{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
    a{color:var(--blue);text-decoration:none}a:hover{text-decoration:underline}button,input,select{font:inherit}
    .shell{width:min(760px,100%);margin:0 auto;border-left:1px solid var(--line);border-right:1px solid var(--line);min-height:100vh}
    .hero{padding:26px 22px 18px;border-bottom:1px solid var(--line);background:linear-gradient(160deg,#0c1923 0,#000 60%)}
    .eyebrow{color:var(--blue);font-weight:800;letter-spacing:.08em;text-transform:uppercase;font-size:12px}.hero h1{font-size:30px;margin:5px 0 0}.handle{color:var(--muted);font-size:16px}.bio-line{display:flex;flex-wrap:wrap;gap:15px;margin-top:14px;color:var(--muted)}.bio-line strong{color:var(--text)}
    .summary{display:grid;grid-template-columns:repeat(5,1fr);border-bottom:1px solid var(--line)}.stat{padding:13px 8px;text-align:center;border-right:1px solid var(--line)}.stat:last-child{border:0}.stat b{font-size:18px;display:block}.stat span{color:var(--muted);font-size:12px}
    .system{padding:14px 16px;border-bottom:1px solid var(--line);background:#050505}.system-head{display:flex;justify-content:space-between;gap:12px;align-items:center}.system h2{font-size:16px;margin:0}.overall{font-size:11px;font-weight:900;text-transform:uppercase;letter-spacing:.06em;padding:4px 8px;border-radius:999px}.overall.healthy,.leg.ok{color:#67e6b8;background:#08251b}.overall.degraded,.leg.error,.leg.unconfigured{color:#ff9ca3;background:#2e0d11}.leg.standby{color:#ffd36a;background:#241d08}.health-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px;margin-top:10px}.leg{border:1px solid var(--line);border-radius:9px;padding:8px 9px;background:#0a0a0a}.leg-top{display:flex;justify-content:space-between;gap:8px}.leg-name{font-weight:750}.leg-status{font-size:10px;font-weight:900;text-transform:uppercase}.leg-detail{color:var(--muted);font-size:12px;margin-top:3px}.coverage{margin-top:9px}.coverage summary{font-size:13px;color:#c7c9cb}.gap{font-size:12px;color:var(--muted);padding:7px 0;border-top:1px solid #1d1d1d}.gap strong{color:var(--text)}
    .warning{margin:15px 0 0;padding:11px 13px;border:1px solid #5d4500;border-radius:10px;background:#1e1700;color:#ffd36a}.warning strong{color:#fff0bd}
    .controls{position:sticky;top:0;z-index:20;padding:12px;background:rgba(0,0,0,.94);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
    .control-row{display:flex;gap:8px}.search{width:100%;border:1px solid var(--line);background:var(--soft);color:var(--text);padding:10px 12px;border-radius:999px;outline:none}.search:focus{border-color:var(--blue)}select{border:1px solid var(--line);background:var(--soft);color:var(--text);border-radius:10px;padding:0 9px}
    .filters{display:flex;gap:7px;overflow:auto;padding-top:10px;scrollbar-width:none}.filters::-webkit-scrollbar{display:none}.chip{white-space:nowrap;border:1px solid var(--line);background:transparent;color:var(--text);padding:6px 10px;border-radius:999px;cursor:pointer}.chip.active{background:var(--text);color:#000;border-color:var(--text);font-weight:700}.result-count{padding-top:8px;color:var(--muted);font-size:12px}
    .entry{display:grid;grid-template-columns:42px 1fr;gap:11px;padding:16px 18px;border-bottom:1px solid var(--line);position:relative}.entry:target{background:#07131c}.entry.deleted{background:linear-gradient(90deg,rgba(244,33,46,.08),transparent 42%)}.entry.deleted:before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--red)}
    .avatar{width:42px;height:42px;border-radius:50%;display:grid;place-items:center;background:#1c1f23;color:#fff;font-size:18px;font-weight:900;border:1px solid var(--line)}.entry-main{min-width:0}.head{display:flex;gap:6px;align-items:baseline;min-width:0}.name{font-weight:800;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.user,.dot,.date{color:var(--muted);white-space:nowrap}.date{overflow:hidden;text-overflow:ellipsis}.badges{display:flex;flex-wrap:wrap;gap:6px;margin:7px 0}.badge{font-size:11px;font-weight:800;padding:3px 7px;border-radius:999px;background:#16202a;color:#8ecdf7;text-transform:uppercase;letter-spacing:.03em}.badge.deleted{background:#2e0d11;color:#ff8b94}.badge.reply{background:#241d08;color:#ffd36a}.badge.repost,.badge.timeline_item{background:#08251b;color:#67e6b8}.reply-context{padding:7px 9px;margin:7px 0;border-left:2px solid var(--line);color:var(--muted);background:#090909}.text{white-space:pre-wrap;overflow-wrap:anywhere;font-size:16px;line-height:1.48;margin:5px 0 11px}.text a{overflow-wrap:anywhere}
    .media-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2px;border:1px solid var(--line);border-radius:14px;overflow:hidden;margin:10px 0;background:#111}.media-grid.single{grid-template-columns:1fr}.media-grid img,.media-grid video{width:100%;height:100%;max-height:560px;object-fit:contain;background:#080808;display:block}.media-link{display:block;min-height:140px}.missing{padding:22px;min-height:120px;display:grid;place-items:center;text-align:center;color:#dca2a6;background:#210a0c}.media-label{font-size:11px;color:var(--muted);margin-top:5px}
    .metrics{display:flex;justify-content:space-between;max-width:480px;color:var(--muted);margin:10px 0 2px}.metric{display:flex;gap:5px;align-items:center}.deleted-note{border:1px solid #5a161c;background:#1c080a;color:#ffb3b8;border-radius:9px;padding:9px 10px;margin:10px 0}.deleted-note strong{color:#fff}.archive-note{border:1px solid #31546c;background:#071722;color:#b9dff7;border-radius:9px;padding:9px 10px;margin:10px 0}.archive-note strong{color:#e6f5ff}.archive-note a{margin-left:5px}
    details{margin-top:10px;color:var(--muted)}summary{cursor:pointer;user-select:none}details .detail-box{font-size:13px;margin-top:7px;padding:10px;background:#090909;border:1px solid var(--line);border-radius:9px;overflow-wrap:anywhere}.detail-grid{display:grid;grid-template-columns:max-content 1fr;gap:4px 10px}.detail-grid b{color:#b8bdc1}.source-links{display:flex;gap:12px;flex-wrap:wrap;margin-top:9px}.permalink{margin-left:auto;color:var(--muted)}
    .empty{padding:60px 20px;text-align:center;color:var(--muted)}footer{padding:25px 20px 45px;color:var(--muted);font-size:13px;text-align:center}.hidden{display:none!important}
    @media(max-width:560px){.shell{border:0}.hero{padding:20px 15px}.summary{grid-template-columns:repeat(3,1fr)}.stat:nth-child(3){border-right:0}.health-grid{grid-template-columns:1fr}.entry{padding:14px 12px;grid-template-columns:36px 1fr}.avatar{width:36px;height:36px}.head{flex-wrap:wrap}.date{width:100%}.media-grid{grid-template-columns:1fr}.control-row{flex-direction:column}select{height:40px}}
  </style>
</head>
<body>
<main class="shell">
  <header class="hero">
    <div class="eyebrow">Offline archive</div>
    <h1 id="profileName">qtecqot</h1>
    <div class="handle">@qtecqot · reconstructed timeline</div>
    <div class="bio-line" id="profileStats"></div>
    <div class="warning hidden" id="healthWarning"></div>
  </header>
  <section class="summary" id="summary"></section>
  <section class="system" id="systemHealth"></section>
  <section class="controls" aria-label="Timeline controls">
    <div class="control-row">
      <input class="search" id="search" type="search" placeholder="Search posts, people, IDs…" autocomplete="off">
      <select id="sort" aria-label="Sort order"><option value="newest">Newest first</option><option value="oldest">Oldest first</option></select>
    </div>
    <div class="filters" id="filters"></div>
    <div class="result-count" id="resultCount"></div>
  </section>
  <section id="timeline" aria-live="polite"></section>
  <footer id="footer"></footer>
</main>
<script>
const DATA = __TIMELINE_DATA__;
const fmt = new Intl.DateTimeFormat(undefined,{dateStyle:'medium',timeStyle:'short',timeZone:'UTC'});
const compact = new Intl.NumberFormat(undefined,{notation:'compact',maximumFractionDigits:1});
const timeline = document.querySelector('#timeline');
const search = document.querySelector('#search');
const sort = document.querySelector('#sort');
const filters = document.querySelector('#filters');
let active = 'all';

function el(tag, cls, text){const node=document.createElement(tag);if(cls)node.className=cls;if(text!==undefined)node.textContent=text;return node}
function time(value){if(!value)return 'time unknown';try{return fmt.format(new Date(value))+' UTC'}catch{return value}}
function num(value){return value===undefined||value===null?'—':compact.format(value)}
function bytes(value){if(value===undefined||value===null)return '—';const units=['B','KB','MB','GB'];let n=value,i=0;while(n>=1024&&i<units.length-1){n/=1024;i++}return n.toFixed(i?1:0)+' '+units[i]}
function appendLinkedText(container,text){
  const pattern=/(https?:\/\/[^\s]+|@[A-Za-z0-9_]+|#[\p{L}\p{N}_]+)/gu;let at=0;
  for(const match of text.matchAll(pattern)){container.append(document.createTextNode(text.slice(at,match.index)));const token=match[0];const a=el('a');
    if(token.startsWith('http')){a.href=token.replace(/[),.;]+$/,'');a.target='_blank';a.rel='noreferrer'}else{a.href='#';a.addEventListener('click',ev=>{ev.preventDefault();search.value=token;render()})}
    a.textContent=token;container.append(a);at=match.index+token.length}
  container.append(document.createTextNode(text.slice(at)));
}
function kindLabel(entry){return {post:'Post',reply:'Reply',repost:'Repost',timeline_item:'Repost observed'}[entry.kind]||entry.kind}
function entryDate(entry){if(entry.time_label)return entry.time_label;if(entry.kind==='timeline_item'&&entry.observed_at)return 'Observed '+time(entry.observed_at);return time(entry.timeline_at)}
function metricIcon(name){return {replies:'↩',reposts:'⟳',quotes:'❞',likes:'♥',bookmarks:'⌑',views:'◉'}[name]||'•'}
function renderMedia(entry,host){if(!entry.media?.length)return;const grid=el('div','media-grid'+(entry.media.length===1?' single':''));
  for(const media of entry.media){if(media.kind==='image'){const a=el('a','media-link');a.href=media.src;a.target='_blank';const img=el('img');img.src=media.src;img.loading='lazy';img.alt=media.label||'Archived image';a.append(img);grid.append(a)}
    else if(media.kind==='video'){const video=el('video');video.src=media.src;video.controls=true;video.preload='metadata';grid.append(video)}
    else{const box=el('div','missing');const historical=media.gone&&entry.provenance?.startsWith('Recovered');box.append(el('div','',historical?'Historical attached-media URL was already 404 when this record was recovered':media.gone?'Media purged before it could be archived':'Media is not held locally'));grid.append(box)}}
  host.append(grid);const labels=[...new Set(entry.media.map(m=>m.label).filter(Boolean))];if(labels.length)host.append(el('div','media-label',labels.join(' · ')))}
function renderEntry(entry){const article=el('article','entry'+(entry.state==='deleted'?' deleted':''));article.id='status-'+entry.id;article.dataset.kind=entry.kind;
  const avatar=el('div','avatar',(entry.author?.name||'?').slice(0,1).toUpperCase());const main=el('div','entry-main');const head=el('div','head');
  head.append(el('span','name',entry.author?.name||'Unknown'),el('span','user','@'+(entry.author?.handle||'unknown')),el('span','dot','·'),el('span','date',entryDate(entry)));
  const anchor=el('a','permalink','↗');anchor.href='#status-'+entry.id;anchor.title='Permalink';head.append(anchor);main.append(head);
  const badges=el('div','badges');badges.append(el('span','badge '+entry.kind,kindLabel(entry)));if(entry.state==='deleted')badges.append(el('span','badge deleted','Deleted'));else if(entry.kind==='timeline_item')badges.append(el('span','badge','Original '+entry.state));else badges.append(el('span','badge',entry.state));main.append(badges);
  if(entry.kind==='reply'){const ctx=el('div','reply-context');ctx.append(document.createTextNode('Replying to '+(entry.parent_handle?'@'+entry.parent_handle:'status')));if(entry.parent_id){const p=el('a','', ' '+entry.parent_id);p.href='#status-'+entry.parent_id;ctx.append(p)}main.append(ctx)}
  if(entry.kind==='repost'||entry.kind==='timeline_item')main.append(el('div','reply-context','Reposted/timeline content originally by @'+(entry.author?.handle||'unknown')+'. Engagement below belongs to the original post.'));
  const text=el('div','text');appendLinkedText(text,entry.text||'[No text; media-only post]');main.append(text);renderMedia(entry,main);
  if(entry.archive_note){const note=el('div','archive-note');note.append(el('strong','','Archive note: '),document.createTextNode(entry.archive_note));if(entry.related_status_id){const related=el('a','',entry.related_status_label||'Related status');related.href='#status-'+entry.related_status_id;note.append(related)}main.append(note)}
  const metrics=el('div','metrics');for(const [name,value] of Object.entries(entry.metrics||{})){const m=el('span','metric');m.title=name;m.append(el('span','',metricIcon(name)),el('span','',num(value)));metrics.append(m)}if(metrics.children.length)main.append(metrics);
  if(entry.state==='deleted'){const note=el('div','deleted-note');note.append(el('strong','',entry.status_id?'Deleted status. ':'Deleted screenshot-only status. '),document.createTextNode(entry.deletion_label||'Deletion time unknown.'));main.append(note)}
  const details=el('details');details.append(el('summary','', 'Archive details'));const box=el('div','detail-box');const grid=el('div','detail-grid');
  const profile=entry.profile_at_post?Object.entries(entry.profile_at_post).map(([k,v])=>k+' '+num(v)).join(' · '):null;const edits=entry.edit_history_ids?.length>1?entry.edit_history_ids.join(', '):null;
  const metricHistory=entry.metrics_history_count?entry.metrics_history_count+' snapshots, '+time(entry.metrics_history_first)+' → '+time(entry.metrics_history_last):null;
  const rows=[['Status ID',entry.status_id||'unknown'],['Conversation ID',entry.conversation_id],['Timeline time',entry.time_label||time(entry.timeline_at)],['Original post time',entry.original_at?time(entry.original_at):null],['First observed',time(entry.first_seen||entry.observed_at)],['Last verified live',time(entry.last_live)],['Deletion noticed',time(entry.deleted_noticed)],['Language',entry.language],['Client/source',entry.source],['Reply settings',entry.reply_settings],['Sensitive flag',entry.possibly_sensitive===true?'yes':null],['Edit history IDs',edits],['Preserved revisions',entry.revision_count],['Account snapshot',profile],['Metrics history',metricHistory],['Metrics context',entry.metrics_context],['Provenance',entry.provenance]];
  for(const [label,value] of rows){if(!value||value==='time unknown')continue;grid.append(el('b','',label),el('span','',value))}box.append(grid);
  const links=el('div','source-links');for(const link of entry.source_links||[]){const a=el('a','',link.label);a.href=link.href;if(link.href.startsWith('http')){a.target='_blank';a.rel='noreferrer'}links.append(a)}if(entry.canonical_url){const a=el('a','','Open on X');a.href=entry.canonical_url;a.target='_blank';a.rel='noreferrer';links.append(a)}box.append(links);details.append(box);main.append(details);
  article.append(avatar,main);return article}
function matches(entry,query){if(!query)return true;const hay=[entry.text,entry.archive_note,entry.id,entry.kind,entry.state,entry.author?.handle,entry.author?.name,entry.parent_handle].join(' ').toLowerCase();return query.split(/\s+/).every(term=>hay.includes(term))}
function inFilter(entry){if(active==='all')return true;if(active==='deleted')return entry.state==='deleted';if(active==='media')return entry.media?.some(m=>m.src);if(active==='missing')return entry.media?.some(m=>m.kind==='missing');if(active==='reposts')return ['repost','timeline_item'].includes(entry.kind);return entry.kind===active}
function render(){const query=search.value.trim().toLowerCase();let entries=DATA.entries.filter(e=>inFilter(e)&&matches(e,query));entries.sort((a,b)=>(a.timeline_at||'').localeCompare(b.timeline_at||'')*(sort.value==='oldest'?1:-1));timeline.replaceChildren(...entries.map(renderEntry));if(!entries.length)timeline.append(el('div','empty','No archived entries match.'));document.querySelector('#resultCount').textContent=entries.length+' of '+DATA.entries.length+' entries shown'}

document.querySelector('#profileName').textContent=DATA.account.name;const ps=document.querySelector('#profileStats');for(const [label,value] of [['followers',DATA.account.followers],['following',DATA.account.following],['posts now',DATA.account.posts],['likes given',DATA.account.likes]]){const span=el('span');span.append(el('strong','',num(value)),' '+label);ps.append(span)}
const summaryItems=[['entries',DATA.counts.entries],['deleted',DATA.counts.deleted],['replies',DATA.counts.replies],['reposts',DATA.counts.reposts],['with media',DATA.counts.with_media]];const summary=document.querySelector('#summary');for(const [label,value] of summaryItems){const s=el('div','stat');s.append(el('b','',String(value)),el('span','',label));summary.append(s)}
if(DATA.health.reply_discovery_degraded){const warning=document.querySelector('#healthWarning');warning.classList.remove('hidden');warning.append(el('strong','','Coverage warning: '),document.createTextNode(DATA.health.coverage_note+(DATA.health.reply_discovery_failure_since?' Failure recorded since '+time(DATA.health.reply_discovery_failure_since)+'.':'')))}
const sh=DATA.health.structured||{};const system=document.querySelector('#systemHealth');const shead=el('div','system-head');shead.append(el('h2','','Capture system'));const overall=el('span','overall '+(sh.overall||'degraded'),sh.overall||'health file pending');shead.append(overall);system.append(shead);
const hg=el('div','health-grid');const legNames={profile_counters:'Profile counters',timeline_rss:'Standalone timeline RSS',official_x_api:'Official X API + replies',xai_reply_fallback:'xAI reply fallback',status_capture:'Status/deletion checks',media_archive:'Media archive',offline_viewer:'Offline viewer'};for(const [key,item] of Object.entries(sh.legs||{})){const card=el('div','leg '+item.status);const top=el('div','leg-top');top.append(el('span','leg-name',legNames[key]||key),el('span','leg-status',item.status));let detail=(item.detail||'')+(item.last_success?' · success '+time(item.last_success):'');if(item.last_error&&item.last_error!==item.detail)detail+=' · last error '+time(item.last_error_at)+': '+item.last_error;card.append(top,el('div','leg-detail',detail));hg.append(card)}system.append(hg);
const cov=el('details','coverage');cov.append(el('summary','','Known coverage limits, media audit, and detection floor'));const cb=el('div');for(const gap of DATA.health.coverage_gaps||[]){const g=el('div','gap');g.append(el('strong','',gap.label+': '),document.createTextNode((gap.start?time(gap.start):'archive start')+' → '+time(gap.end)+'. '+gap.detail));cb.append(g)}const c=DATA.counts;const audit=el('div','gap');audit.append(el('strong','','Media held: '),document.createTextNode(c.local_media_files+' files / '+bytes(c.local_media_bytes)+'. '+c.missing_media_assets+' attached asset(s) unavailable across '+c.missing_media_entries+' entries.'));cb.append(audit);const preservation=el('div','gap');preservation.append(el('strong','','Change history: '),document.createTextNode(c.revision_files+' semantic revision files and '+c.metric_snapshots+' engagement snapshots are held.'));cb.append(preservation);const latency=DATA.health.capture_latency||{};const floor=el('div','gap');floor.append(el('strong','','Capture latency sample: '),document.createTextNode(latency.sample_size+' records; median '+(latency.median_seconds===null?'—':Math.round(latency.median_seconds/60)+' min')+', maximum '+(latency.maximum_seconds===null?'—':Math.round(latency.maximum_seconds/60)+' min')+'. '+latency.floor));cb.append(floor);const detect=el('div','gap');detect.append(el('strong','','Detection floor: '),document.createTextNode(DATA.health.detection_floor));cb.append(detect);cov.append(cb);system.append(cov);
const filterDefs=[['all','All'],['post','Posts'],['reply','Replies'],['reposts','Reposts'],['deleted','Deleted'],['media','Media'],['missing','Missing media']];for(const [key,label] of filterDefs){const b=el('button','chip'+(key==='all'?' active':''),label);b.dataset.filter=key;b.addEventListener('click',()=>{active=key;for(const c of filters.children)c.classList.toggle('active',c===b);render()});filters.append(b)}
search.addEventListener('input',render);sort.addEventListener('change',render);document.querySelector('#footer').append(document.createTextNode('Generated '+time(DATA.generated_at)+' from local watcher and recovered API records · '),(()=>{const a=el('a','','data.json');a.href='data.json';return a})());render();
</script>
</body>
</html>
'''


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    data = build_data()
    json_text = json.dumps(data, ensure_ascii=False, indent=2)
    (OUT / "data.json").write_text(json_text + "\n", encoding="utf-8")
    embedded = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    embedded = embedded.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    (OUT / "index.html").write_text(HTML.replace("__TIMELINE_DATA__", embedded), encoding="utf-8")
    counts = data["counts"]
    print(f"wrote {OUT / 'index.html'}")
    print(f"entries={counts['entries']} deleted={counts['deleted']} replies={counts['replies']} "
          f"reposts={counts['reposts']} with_media={counts['with_media']}")


if __name__ == "__main__":
    main()
