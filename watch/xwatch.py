#!/usr/bin/env python3.12
"""
X/Twitter capture daemon for @qtecqot (and any other handle in HANDLES).

Why this exists: on 2026-08-02 the account posted a "Fake copycat channel" tweet
linking youtube.com/@qtecqot2 and deleted it inside ~1 hour. Nothing archived it.
The only surviving copy is a browser screenshot a human happened to take. The
2026-05-25 purge (three posts erased eleven minutes after video 1 went public) was
recovered only because a stranger's Twitter API v2 lookups happened to be in the
Wayback Machine. Neither is a method. This is.

Four independent legs, so no single blocked endpoint means silent data loss:

  A. COUNTER TRIPWIRE - api.fxtwitter.com/<handle>. Cheap, never blocked, and the
     counters move the instant anything happens: tweets +/-, media_count, following
     (a follow/unfollow), likes (he liked something), followers, name, bio, avatar.
     A tweets increment followed by a decrement IS a post-and-delete, bounded to the
     poll interval even if every other leg failed to catch the body.

  B. TIMELINE ENUMERATION - nitter RSS mirrors, tried in order until one parses.
     Yields status IDs. New ID -> leg C archives it.

  C. FULL CAPTURE - for every ID ever seen: fetch the complete record from
     api.fxtwitter.com/<handle>/status/<id>, write x/raw/<id>.json, download every
     attached image/video at :orig into x/media/, and record it. Re-checked each run;
     a 404 on a previously-200 ID is a DELETION, and we already hold the body.

  D. THIRD-PARTY ARCHIVE - fire web.archive.org/save/ for each newly seen status, so
     a copy exists outside this repo and outside our control. Best effort, rate-limited.

Absence rule (AGENTS.md): a fetch failure is recorded as an ERROR, never as "nothing
happened". The changelog distinguishes the two, and check.log carries per-leg outcomes.

Usage:  python3.12 watch/xwatch.py           # one pass
        python3.12 watch/xwatch.py --quiet   # print only on change (for cron)
        python3.12 watch/xwatch.py --backfill 2049004250995507595 ...   # add known IDs
Exit 10 = something changed.
"""
import json, os, re, sys, time, urllib.request, urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.abspath(__file__))
XDIR = os.path.join(ROOT, "x")
RAW = os.path.join(XDIR, "raw")
MEDIA = os.path.join(XDIR, "media")
STATE = os.path.join(XDIR, "state.json")
CHANGELOG = os.path.join(XDIR, "CHANGELOG.md")
CHECKLOG = os.path.join(XDIR, "check.log")

HANDLES = ["qtecqot"]

# Tried in order; first one that parses as RSS with >=1 item wins.
NITTER = [
    "https://nitter.net/{h}/rss",
    "https://nitter.poast.org/{h}/rss",
    "https://xcancel.com/{h}/rss",
    "https://nitter.privacyredirect.com/{h}/rss",
    "https://nitter.tiekoetter.com/{h}/rss",
]

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

# Counters worth shouting about. following/likes changes are how we caught that an
# account was followed and unfollowed inside the May window.
# A screen_name change is loud: the account has exactly one on record (April 2026, prior
# handle unrecoverable) and it is an open item in the dossier. A second one gets caught here.
LOUD = {"tweets": "★★★", "media_count": "★★", "following": "★★★", "likes": "★★",
        "name": "★★★", "screen_name": "★★★", "description": "★★★", "avatar_url": "★★",
        "protected": "★★★", "location": "★★", "website": "★★"}


def get(url, timeout=25, raw=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        b = r.read()
    return b if raw else json.loads(b)


# ---------------------------------------------------------------- leg A
def leg_a(handle):
    """Profile counters. Returns (snapshot, error)."""
    try:
        d = get(f"https://api.fxtwitter.com/{handle}")
        u = d.get("user") or {}
        if not u:
            return None, f"fxtwitter returned no user object (code={d.get('code')})"
        keep = ("screen_name", "id", "name", "description", "location", "website",
                "followers", "following", "likes", "tweets", "media_count",
                "avatar_url", "banner_url", "protected", "joined")
        return {k: u.get(k) for k in keep}, None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


# ---------------------------------------------------------------- leg B
def leg_b(handle):
    """Timeline status IDs from whichever nitter mirror answers. Returns (ids, note)."""
    tried = []
    for tpl in NITTER:
        url = tpl.format(h=handle)
        try:
            body = get(url, timeout=20, raw=True)
            root = ET.fromstring(body)
            items = root.find("channel").findall("item")
            ids = []
            for it in items:
                m = re.search(r"/status/(\d+)", it.findtext("link") or "")
                if m:
                    ids.append(m.group(1))
            if ids:
                return ids, f"ok via {url} ({len(ids)} items)"
            tried.append(f"{url}: parsed but 0 items")
        except Exception as e:
            tried.append(f"{url}: {type(e).__name__}")
    return [], "ALL MIRRORS FAILED -- " + "; ".join(tried)


# ---------------------------------------------------------------- leg C
def fetch_status(handle, sid):
    """(record|None, http_status). 404 means deleted/never-existed."""
    try:
        return get(f"https://api.fxtwitter.com/{handle}/status/{sid}"), 200
    except urllib.error.HTTPError as e:
        return None, e.code
    except Exception:
        return None, -1


def save_media(rec, sid):
    """Download every attached asset at full resolution. Returns list of local paths."""
    out = []
    tw = (rec or {}).get("tweet") or {}
    media = (tw.get("media") or {}).get("all") or []
    for i, m in enumerate(media, 1):
        url = m.get("url")
        if not url:
            continue
        # Images: ask for the original, not the timeline-resized variant.
        if m.get("type") == "photo" and "?" not in url:
            url = url + "?format=" + url.rsplit(".", 1)[-1] + "&name=orig"
        ext = re.sub(r"[?&].*$", "", url).rsplit(".", 1)[-1][:4] or "bin"
        path = os.path.join(MEDIA, f"{sid}_{i}.{ext}")
        if os.path.exists(path):
            out.append(os.path.basename(path)); continue
        try:
            open(path, "wb").write(get(url, timeout=60, raw=True))
            out.append(os.path.basename(path))
        except Exception as e:
            out.append(f"FAILED {os.path.basename(path)}: {type(e).__name__}")
    return out


# ---------------------------------------------------------------- leg D
def wayback_save(sid):
    """Best effort third-party copy.

    Save Page Now without an archive.org S3 key is unreliable -- it commonly answers
    523, and archive.today rate-limits hard. We try anyway because when it lands it is
    a copy outside our control, but the honest outcome is logged either way. The real
    durability guarantee is leg C's local body plus --commit below, not this.
    """
    url = f"https://twitter.com/qtecqot/status/{sid}"
    try:
        req = urllib.request.Request("https://web.archive.org/save/" + url,
                                     headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=45) as r:
            return f"wayback save accepted (HTTP {r.status})"
    except urllib.error.HTTPError as e:
        return f"wayback save unavailable (HTTP {e.code}) — local body is the copy"
    except Exception as e:
        return f"wayback save unavailable ({type(e).__name__}) — local body is the copy"


def git_commit(msg):
    """Get the capture off this box. Only touches watch/x/."""
    import subprocess
    try:
        subprocess.run(["git", "-C", os.path.dirname(ROOT), "add", "watch/x"],
                       check=True, capture_output=True, timeout=60)
        r = subprocess.run(["git", "-C", os.path.dirname(ROOT), "commit", "-m", msg],
                           capture_output=True, timeout=60, text=True)
        return "committed" if r.returncode == 0 else f"nothing to commit ({r.stdout.strip()[:60]})"
    except Exception as e:
        return f"commit failed: {type(e).__name__}"


# ---------------------------------------------------------------- main
def main():
    quiet = "--quiet" in sys.argv
    for d in (XDIR, RAW, MEDIA):
        os.makedirs(d, exist_ok=True)
    state = json.load(open(STATE)) if os.path.exists(STATE) else {"handles": {}}

    if "--backfill" in sys.argv:
        ids = [a for a in sys.argv[sys.argv.index("--backfill") + 1:] if a.isdigit()]
        h = state["handles"].setdefault(HANDLES[0], {"profile": None, "statuses": {}})
        for sid in ids:
            h["statuses"].setdefault(sid, {"first_seen": None, "state": "unknown"})
        print(f"backfilled {len(ids)} ids")

    now = datetime.now(timezone.utc)
    lines, errors = [], []

    for handle in HANDLES:
        hs = state["handles"].setdefault(handle, {"profile": None, "statuses": {}})

        # --- leg A
        prof, err = leg_a(handle)
        if err:
            errors.append(f"@{handle} leg A (counters): {err}")
        elif hs["profile"] is None:
            lines.append(f"BASELINE @{handle}: {prof['tweets']} posts, "
                         f"{prof['followers']} followers, {prof['following']} following, "
                         f"{prof['likes']} likes, {prof['media_count']} media")
            hs["profile"] = prof
        else:
            old = hs["profile"]
            for k, v in prof.items():
                if old.get(k) != v and k in LOUD:
                    lines.append(f"{LOUD[k]} @{handle}: {k} {old.get(k)!r} -> {v!r}")
                elif old.get(k) != v:
                    lines.append(f"    @{handle}: {k} {old.get(k)!r} -> {v!r}")
            hs["profile"] = prof

        # --- leg B
        ids, note = leg_b(handle)
        if not ids:
            errors.append(f"@{handle} leg B (timeline): {note}")
        new_ids = [i for i in ids if i not in hs["statuses"]]
        for sid in new_ids:
            hs["statuses"][sid] = {"first_seen": now.isoformat(), "state": "new"}

        # --- leg C: capture new ones, re-check known ones.
        #
        # Budget matters here. Re-checking all 20 known IDs every 2 minutes is ~8k
        # requests/day at a free public mirror, which invites a block -- and a block
        # would blind legs A and C at the same time, which is the one failure mode
        # this whole file exists to prevent. So the sweep is conditional:
        #
        #   - a NEW id from leg B is always captured immediately (that is the point);
        #   - a full liveness sweep runs when leg A's counters moved (a deletion shows
        #     up there first, as tweets going down), or on --full, or every ~30 min;
        #   - otherwise leg C is skipped and the pass costs 2 requests total.
        #
        # Detection latency is therefore the cron interval, not the sweep interval.
        full = "--full" in sys.argv
        counters_moved = any(l.startswith(("★", "BASELINE")) for l in lines)
        periodic = (now.minute % 30) < 2
        sweep = full or counters_moved or periodic
        for sid, meta in sorted(hs["statuses"].items()):
            if sid not in new_ids:
                if not sweep:
                    continue
                if meta.get("state") == "deleted" and not full:
                    continue  # deletions do not reverse; --full re-checks anyway
            rec, code = fetch_status(handle, sid)
            prev = meta.get("state")
            if code == 200 and rec:
                path = os.path.join(RAW, f"{sid}.json")
                fresh = not os.path.exists(path)
                if fresh:
                    json.dump(rec, open(path, "w"), indent=1, ensure_ascii=False)
                    tw = rec.get("tweet") or {}
                    txt = (tw.get("text") or "").replace("\n", " / ")[:220]
                    saved = save_media(rec, sid)
                    lines.append(f"★★★ @{handle}: CAPTURED {sid} ({tw.get('created_at')}) "
                                 f"— {txt!r}" + (f" [media: {', '.join(saved)}]" if saved else ""))
                    lines.append(f"    {wayback_save(sid)} for {sid}")
                meta["state"] = "live"
                meta["last_live"] = now.isoformat()
            elif code == 404:
                if prev in ("live", "new"):
                    have = "body archived at x/raw/%s.json" % sid if \
                        os.path.exists(os.path.join(RAW, f"{sid}.json")) else \
                        "!! NO LOCAL BODY -- this one got away"
                    lines.append(f"★★★ @{handle}: DELETED {sid} "
                                 f"(last seen live {meta.get('last_live','?')}) — {have}")
                meta["state"] = "deleted"
                meta.setdefault("deleted_noticed", now.isoformat())
            else:
                errors.append(f"@{handle} leg C: status {sid} returned {code}")

    real = [l for l in lines if not l.startswith("    ")]
    os.makedirs(XDIR, exist_ok=True)
    json.dump(state, open(STATE, "w"), indent=1, ensure_ascii=False)
    with open(CHECKLOG, "a") as w:
        w.write(f"{now.isoformat()} changes={len(real)} notes={len(lines)-len(real)} "
                f"errors={len(errors)}\n")
    if lines or errors:
        with open(CHANGELOG, "a") as w:
            w.write(f"\n## {now.isoformat()}\n\n")
            for l in lines:
                w.write(f"- {l}\n")
            for e in errors:
                w.write(f"- ! ERROR (instrument failure, NOT an absence of change): {e}\n")
    if real and "--commit" in sys.argv:
        print("  git: " + git_commit(f"xwatch: {len(real)} change(s) at {now.isoformat()}"))
    if not quiet or real or errors:
        print(f"[{now.isoformat()}] {len(real)} change(s), {len(errors)} error(s)")
        for l in lines:
            print("  " + l)
        for e in errors:
            print("  ! " + e)
    return 10 if real else 0


if __name__ == "__main__":
    sys.exit(main())
