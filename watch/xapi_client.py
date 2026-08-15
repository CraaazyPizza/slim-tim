#!/usr/bin/env python3.12
"""Small stdlib-only client for the official X API user-post timeline.

The user timeline includes replies unless ``exclude=replies`` is explicitly
requested.  Keeping this client separate makes the paid/deterministic source
testable without touching watcher state or making live calls in tests.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


API_BASE = "https://api.x.com/2"
DEFAULT_CREDENTIAL_FILES = (
    Path("~/.config/qtecqot-watch.env").expanduser(),
    Path("~/.config/qtecqot-watch/x.env").expanduser(),
)

POST_FIELDS = (
    "article,article_title,attachments,card_uri,community_id,context_annotations,"
    "conversation_id,created_at,display_text_range,edit_controls,entities,geo,lang,"
    "matched_media_notes,media_metadata,note_post,paid_partnership,possibly_sensitive,"
    "public_metrics,reply_settings,source,suggested_source_links,"
    "suggested_source_links_with_counts,withheld"
)
EXPANSIONS = (
    "attachments.media_keys,attachments.media_source_tweet,attachments.poll_ids,author_id,"
    "edit_history_post_ids,entities.mentions.username,geo.place_id,in_reply_to_user_id,"
    "referenced_posts,username"
)
MEDIA_FIELDS = (
    "alt_text,duration_ms,height,media_key,preview_image_url,public_metrics,type,url,variants,width"
)
USER_FIELDS = (
    "created_at,description,entities,id,is_identity_verified,location,name,parody,"
    "profile_banner_url,profile_image_url,protected,public_metrics,url,username,verified,"
    "verified_followers_count,verified_type,withheld"
)
POLL_FIELDS = "duration_minutes,end_datetime,id,options,voting_status"
PLACE_FIELDS = "contained_within,country,country_code,full_name,geo,id,name,place_type"


class XApiError(RuntimeError):
    """An official X API request failed without exposing credentials."""

    def __init__(self, message: str, status: int | None = None):
        super().__init__(message)
        self.status = status


@dataclass
class TimelineResult:
    records: dict[str, dict]
    pages: int
    result_count: int
    newest_id: str | None
    oldest_id: str | None
    complete: bool


def load_env_value(name: str, files: tuple[Path, ...] = DEFAULT_CREDENTIAL_FILES) -> str:
    value = os.environ.get(name, "").strip()
    if value:
        return value
    for path in files:
        try:
            for raw_line in path.read_text(encoding="utf-8").splitlines():
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, candidate = line.split("=", 1)
                if key.strip() == name:
                    return candidate.strip().strip("\"").strip("'")
        except OSError:
            continue
    return ""


def bearer_token() -> str:
    return load_env_value("X_BEARER_TOKEN") or load_env_value("TWITTER_BEARER_TOKEN")


def referenced_items(post: dict) -> list[dict]:
    return post.get("referenced_posts") or post.get("referenced_tweets") or []


def included_posts(includes: dict) -> list[dict]:
    return includes.get("posts") or includes.get("tweets") or []


def _included_ids(tweet: dict, includes: dict) -> tuple[set[str], set[str]]:
    """Return media and user ids directly relevant to a timeline post.

    Referenced post objects are retained as context. Their attached media is also
    retained, but the viewer independently checks attachment keys before assigning
    any of it to the qtecqot post.
    """
    media_keys = set((tweet.get("attachments") or {}).get("media_keys") or [])
    user_ids = {str(tweet.get("author_id") or ""), str(tweet.get("in_reply_to_user_id") or "")}
    ref_ids = {str(ref.get("id")) for ref in referenced_items(tweet) if ref.get("id")}
    for ref in included_posts(includes):
        if str(ref.get("id")) not in ref_ids:
            continue
        media_keys.update((ref.get("attachments") or {}).get("media_keys") or [])
        if ref.get("author_id"):
            user_ids.add(str(ref["author_id"]))
    user_ids.discard("")
    return media_keys, user_ids


def slice_record(tweet: dict, response: dict, captured_at: str) -> dict:
    """Make a self-contained per-post API v2 record from a timeline page."""
    includes = response.get("includes") or {}
    ref_ids = {str(ref.get("id")) for ref in referenced_items(tweet) if ref.get("id")}
    media_keys, user_ids = _included_ids(tweet, includes)
    posts_key = "posts" if "posts" in includes else "tweets"
    kept_tweets = [item for item in included_posts(includes) if str(item.get("id")) in ref_ids]
    kept_media = [item for item in includes.get("media") or []
                  if item.get("media_key") in media_keys]
    kept_users = [item for item in includes.get("users") or []
                  if str(item.get("id")) in user_ids]
    result = {
        "data": tweet,
        "includes": {
            posts_key: kept_tweets,
            "media": kept_media,
            "users": kept_users,
            "polls": includes.get("polls") or [],
            "places": includes.get("places") or [],
        },
        "_archive": {
            "source": "official X API GET /2/users/:id/tweets",
            "captured_at": captured_at,
        },
    }
    if response.get("errors"):
        result["errors"] = response["errors"]
    return result


def _request_json(url: str, token: str, timeout: int,
                  opener: Callable = urllib.request.urlopen) -> dict:
    request = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}", "User-Agent": "qtecqot-archive/1.0"},
    )
    try:
        with opener(request, timeout=timeout) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        detail = ""
        try:
            payload = json.loads(exc.read())
            detail = payload.get("detail") or payload.get("title") or ""
        except Exception:
            pass
        suffix = f": {detail}" if detail else ""
        raise XApiError(f"HTTP {exc.code}{suffix}", exc.code) from exc
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise XApiError(f"{type(exc).__name__}: {exc}") from exc


def get_user_posts(user_id: str, token: str, captured_at: str, *,
                   full_backfill: bool, max_results: int = 100, timeout: int = 30,
                   since_id: str | None = None,
                   opener: Callable = urllib.request.urlopen) -> TimelineResult:
    """Fetch replies and posts, optionally paginating the full current timeline."""
    if not token:
        raise XApiError("not configured: X_BEARER_TOKEN is absent")
    records: dict[str, dict] = {}
    pages = 0
    newest_id = oldest_id = None
    pagination_token = None
    complete = False
    while True:
        params = {
            "max_results": str(max_results),
            "post.fields": POST_FIELDS,
            "expansions": EXPANSIONS,
            "media.fields": MEDIA_FIELDS,
            "user.fields": USER_FIELDS,
            "poll.fields": POLL_FIELDS,
            "place.fields": PLACE_FIELDS,
        }
        if pagination_token:
            params["pagination_token"] = pagination_token
        if since_id:
            params["since_id"] = since_id
        url = f"{API_BASE}/users/{user_id}/tweets?{urllib.parse.urlencode(params)}"
        payload = _request_json(url, token, timeout, opener)
        pages += 1
        for tweet in payload.get("data") or []:
            sid = str(tweet.get("id") or "")
            if sid:
                records[sid] = slice_record(tweet, payload, captured_at)
        meta = payload.get("meta") or {}
        newest_id = newest_id or meta.get("newest_id")
        oldest_id = meta.get("oldest_id") or oldest_id
        pagination_token = meta.get("next_token")
        if not full_backfill or not pagination_token:
            complete = not pagination_token
            break
    return TimelineResult(
        records=records,
        pages=pages,
        result_count=len(records),
        newest_id=str(newest_id) if newest_id else None,
        oldest_id=str(oldest_id) if oldest_id else None,
        complete=complete,
    )
