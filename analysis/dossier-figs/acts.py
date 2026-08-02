#!/usr/bin/env python3.12
"""Canonical act list for the qtecqot dossier figures, derived, not typed.

Why this exists. Every figure that needed qtecqot's posts carried its own hardcoded
list of timestamps. On 2026-08-02 he posted twice more, the watcher captured both, and
three figures silently kept saying "19 posts" while the raw directory held 21. Nothing
was wrong with any single script; the duplication was the bug. So the post list is read
off `raw/` at run time and there is one place to be wrong.

Two things this filters that a naive glob does not:

  * `watch/x/raw/` also holds posts by *other* accounts, captured because he reposted
    them. 2082824913815998748 is Eddie Abbott's "SKINNY BOB FACTS" thread. Counting it
    as his would have made 22.
  * The same status is often present in both raw directories. Dedupe by ID.

Import from a script in this directory, or add the repo root to sys.path.
"""
import glob
import json
import os
from datetime import datetime, timezone

HANDLE = "qtecqot"
RAW_DIRS = ("qtecqot-x-recovered/raw", "watch/x/raw")

# The repo root, found from this file rather than assumed to be the cwd.
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def snowflake_utc(status_id):
    """X status ID -> UTC datetime. (id >> 22) + the Twitter epoch, in ms."""
    return datetime.fromtimestamp(((int(status_id) >> 22) + 1288834974657) / 1000,
                                  timezone.utc).replace(tzinfo=None)


def _walk(obj, keys, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in keys and isinstance(v, str):
                out.add(v)
            _walk(v, keys, out)
    elif isinstance(obj, list):
        for v in obj:
            _walk(v, keys, out)


def _own_text(rec):
    """His text only.

    Do NOT take the longest "text" in the record. A reply record carries the text it
    replies to, and a repost record carries the whole reposted thread, both of which are
    longer than anything he writes. Taking the longest attributed Eddie Abbott's
    "SKINNY BOB FACTS" to him and put a stranger's reply in his row. Read the top-level
    node instead, and return "" rather than guess.
    """
    if not isinstance(rec, dict):
        return ""
    node = rec.get("tweet")                       # live fxtwitter shape
    if isinstance(node, dict) and isinstance(node.get("text"), str):
        return node["text"]
    node = rec.get("data")                        # archived Twitter API v2 shape
    if isinstance(node, dict) and isinstance(node.get("text"), str):
        return node["text"]
    if isinstance(rec.get("text"), str):          # bare record
        return rec["text"]
    return ""


def posts():
    """[(utc_datetime, status_id, text, is_live)], his own posts only, time-ordered.

    is_live is decided by which directory the record came from: anything present in
    `watch/x/raw/` was seen live by the daemon, anything only in the recovery set was
    pulled from Wayback after deletion. That is the same live/deleted split RECOVERED.md
    reports, derived rather than restated.
    """
    live_ids = {os.path.basename(p)[:-5]
                for p in glob.glob(os.path.join(ROOT, "watch/x/raw", "*.json"))}
    by_id = {}
    for d in RAW_DIRS:
        for path in glob.glob(os.path.join(ROOT, d, "*.json")):
            sid = os.path.basename(path)[:-5]
            if not sid.isdigit():
                continue
            try:
                rec = json.load(open(path, encoding="utf-8"))
            except Exception:
                continue
            names = set()
            _walk(rec, {"screen_name", "username"}, names)
            lowered = {n.lower() for n in names}
            # Reposts carry the original author's handle and not his. Require his.
            if HANDLE not in lowered:
                continue
            # A repost record names both. If another handle authored it, skip.
            if len(lowered) > 1 and not _authored_by_handle(rec):
                continue
            prev = by_id.get(sid)
            text = _own_text(rec)
            if prev is None or len(text) > len(prev[2]):
                by_id[sid] = (snowflake_utc(sid), sid, text, sid in live_ids)
    return sorted(by_id.values())


def _authored_by_handle(rec):
    """True if the top-level author of this record is the handle, not a reposted account."""
    for key in ("tweet", "data"):
        node = rec.get(key) if isinstance(rec, dict) else None
        if isinstance(node, dict):
            author = node.get("author") or node.get("user") or {}
            if isinstance(author, dict):
                sn = (author.get("screen_name") or author.get("username") or "")
                if sn:
                    return sn.lower() == HANDLE
    # Archived API v2 shape: includes.users[0] is the author of data.
    inc = rec.get("includes") if isinstance(rec, dict) else None
    if isinstance(inc, dict):
        users = inc.get("users") or []
        if users and isinstance(users[0], dict):
            sn = users[0].get("username", "")
            if sn:
                return sn.lower() == HANDLE
    return False


# A post with no record in raw/, and therefore invisible to posts() above.
#
# On the morning of 2026-08-02 he posted a YouTube link card captioned "Fake copycat
# channel" and deleted it within the hour. It has no status ID we ever learned, no Wayback
# capture, no fxtwitter record and no x_search hit. The only copy that exists anywhere is a
# browser screenshot taken while it was live, X-stamped "· 1h" at capture. See RECOVERED.md
# under "2026-08-02, ~09:00-11:00 UTC".
#
# It is listed separately because deriving from raw/ is only as complete as raw/, and this
# is the one act that shows where that floor is. Drawn hollow, like the YouTube comments,
# because its instant is a two-hour window rather than a timestamp.
SCREENSHOT_ONLY = [
    (datetime(2026, 8, 2, 10, 0, 0), "post-gone",
     "Post, since deleted — no record but a screenshot",
     "“◆ Fake copycat channel:” a link card for youtube.com/@qtecqot2, which now 404s",
     "~09:00–11:00 window"),
]

# Acts that are not X posts. These are machine-read from sources outside raw/, so they
# stay written down here with their provenance.
YT_CHANNEL_CREATED = datetime(2026, 4, 22, 5, 27, 55)    # YouTube channel RSS feed
X_ACCOUNT_CREATED = datetime(2026, 4, 28, 5, 24, 54)     # archived profile record
VIDEOS = [                                                # YouTube publish instants
    (datetime(2026, 5, 25, 9, 39, 42), "OpSTlDJWFFI", "video 5 of 8", 100),
    (datetime(2026, 6, 15, 4, 23, 35), "Oqw96jCOP7A", "video 6 of 8", 84),
    (datetime(2026, 7, 24, 9, 14, 5), "l9RAhmPHM_A", "video 7 of 8", 147),
]
DESC_EDIT = datetime(2026, 7, 28, 7, 7, 1)               # video 3 description edited

# ivan0135, 2011. Channel creation from YouTube's RSS feed (docs/SKINNY_BOB_DOSSIER.md
# section F); uploads decoded from the `timestamp` field of archive/ivan/*.info.json.
IVAN_2011 = [datetime(2011, 4, 14, 1, 8, 36), datetime(2011, 4, 14, 2, 4, 26),
             datetime(2011, 5, 2, 5, 21, 51), datetime(2011, 5, 9, 5, 9, 51),
             datetime(2011, 5, 18, 0, 35, 43)]


if __name__ == "__main__":
    ps = posts()
    live = sum(1 for p in ps if p[3])
    print(f"{len(ps)} posts by @{HANDLE}: {live} live, {len(ps) - live} deleted")
    for ts, sid, text, is_live in ps:
        flag = "live " if is_live else "DEL  "
        print(f"  {ts:%Y-%m-%dT%H:%M:%S} {flag} {sid}  {' '.join(text.split())[:72]}")
