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

Assets are downloaded from whatever shape the record happens to be in, because we
hold two: the live fxtwitter body and the archived Twitter API v2 bodies recovered
from the Wayback Machine. The shape-specific reader this started with saw nothing
in the second kind, so the 2026-06-14 deleted post's attached video sat unfetched
for seven weeks. `--backfill-media` sweeps every record we hold, including
qtecqot-x-recovered/raw/, and logs which assets the CDN has already purged.

Usage:  python3.12 watch/xwatch.py           # one pass
        python3.12 watch/xwatch.py --quiet   # print only on change (for cron)
        python3.12 watch/xwatch.py --backfill 2049004250995507595 ...   # add known IDs
        python3.12 watch/xwatch.py --backfill-media   # sweep held records for assets
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


def leg_b2(handle):
    """Status IDs including REPLIES, via xAI x_search. Returns (ids, note).

    Leg B is blind to replies. Nitter's profile RSS carries only standalone posts;
    /with_replies/rss returns empty and the search endpoint is dead on every mirror
    we have. That was not a problem while he posted announcements. On 2026-08-02 he
    began answering people, and three consecutive replies -- including a dated
    prediction about the next release -- were invisible to every leg except the
    tweets counter in leg A, which could only say "one more post exists somewhere".

    Needs XAI_API_KEY. Absent, this returns a recorded skip, never a silent zero.
    """
    key = os.environ.get("XAI_API_KEY") or ""
    if not key:
        for p in (os.path.expanduser("~/.config/last30days/.env"),):
            try:
                for ln in open(p):
                    if ln.startswith("XAI_API_KEY="):
                        key = ln.split("=", 1)[1].strip()
            except Exception:
                pass
    if not key:
        return [], "SKIPPED (no XAI_API_KEY) -- replies are not being enumerated"
    body = json.dumps({
        "model": "grok-4",
        "input": f"List every post from the X account @{handle} from the last 7 days, "
                 f"including replies. Give the full numeric status ID of each.",
        "tools": [{"type": "x_search"}],
    }).encode()
    try:
        req = urllib.request.Request(
            "https://api.x.ai/v1/responses", data=body,
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
        raw = urllib.request.urlopen(req, timeout=120).read().decode("utf-8", "replace")
    except Exception as e:
        return [], f"x_search FAILED: {type(e).__name__} {getattr(e, 'code', '')}"
    # Snowflake IDs for this account are 19 digits starting 20; anything else in the
    # prose is not a status id. Validate by decoding to a plausible date.
    ids = []
    for m in re.finditer(r"\b(2[0-9]{18})\b", raw):
        sid = m.group(1)
        ts = (int(sid) >> 22) + 1288834974657
        if 1735689600000 < ts < time.time() * 1000 + 86400000:   # 2025-01-01 .. tomorrow
            ids.append(sid)
    ids = sorted(set(ids))
    return ids, f"ok via x_search ({len(ids)} ids, replies included)"


# ---------------------------------------------------------------- leg C
def fetch_status(handle, sid):
    """(record|None, http_status). 404 means deleted/never-existed."""
    try:
        return get(f"https://api.fxtwitter.com/{handle}/status/{sid}"), 200
    except urllib.error.HTTPError as e:
        return None, e.code
    except Exception:
        return None, -1


CDN = ("pbs.twimg.com", "video.twimg.com")


def media_urls(obj):
    """Every twimg asset URL anywhere in a record, whatever the record's shape.

    Deliberately shape-agnostic. The live fxtwitter body nests assets under
    tweet.media.all[].url, but the archived Twitter API v2 bodies in
    qtecqot-x-recovered/raw/ use includes.media[].media_url_https and a
    variants[] list, and the 2026-06-14 deleted post kept its video only in the
    latter. A shape-specific reader silently returned nothing for those and the
    assets went un-downloaded for months. Walk the whole tree instead.
    """
    found = set()

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, str) and any(d in v for d in CDN) and v.startswith("http"):
                    # news_img/* is the link-preview thumbnail for an article he linked
                    # to, not media he attached. Tracking it as a loss is a false alarm.
                    if k in ("url", "media_url", "media_url_https", "preview_image_url") \
                            and "/news_img/" not in v:
                        found.add(v)
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(obj)
    # Keep only the largest rendition per video: the variants list carries the same
    # clip at 480x270 through 1920x1080 and we want the one with the most signal.
    best = {}
    keep = set()
    for u in found:
        m = re.search(r"/amplify_video/(\d+)/vid/[^/]+/(\d+)x(\d+)/", u)
        if m:
            vid, px = m.group(1), int(m.group(2)) * int(m.group(3))
            if px > best.get(vid, (0, None))[0]:
                best[vid] = (px, u)
        else:
            keep.add(u)
    return sorted(keep | {u for _, u in best.values()})


def save_media(rec, sid, log=None):
    """Download every attached asset at full resolution. Returns list of local names."""
    out = []
    for i, url in enumerate(media_urls(rec), 1):
        fetch = url
        # Images: ask for the original, not the timeline-resized variant.
        if "pbs.twimg.com/media/" in url and "name=" not in url:
            ext0 = url.rsplit(".", 1)[-1]
            fetch = url.split("?")[0] + "?format=" + ext0 + "&name=orig"
        ext = re.sub(r"[?&].*$", "", url).rsplit(".", 1)[-1][:4] or "bin"
        path = os.path.join(MEDIA, f"{sid}_{i}.{ext}")
        if os.path.exists(path) and os.path.getsize(path) > 0:
            out.append(os.path.basename(path)); continue
        try:
            body = get(fetch, timeout=90, raw=True)
            if not body:
                raise ValueError("empty body")
            open(path, "wb").write(body)
            out.append(os.path.basename(path))
        except Exception as e:
            # A 404 here is itself a finding: X purges assets on delete, but not
            # always and not immediately. Record which ones we lost and when.
            code = getattr(e, "code", type(e).__name__)
            out.append(f"GONE {os.path.basename(path)} ({code}) {url}")
            if log is not None:
                log.append(f"    media GONE {sid}_{i} {code} {url}")
    return out


def backfill_media(extra_dirs, log):
    """Sweep every record we already hold and download any asset we never fetched.

    Leg C only ever downloaded media at the moment it captured a status. Records
    recovered by other means -- the Wayback API v2 bodies under
    qtecqot-x-recovered/raw/ -- were never swept, so their assets were never
    pulled even while the CDN was still serving them. This closes that.
    """
    # Assets X has already purged stay purged. Remember which, so the hourly pass
    # reports a NEW loss as an error and stays quiet about the standing ones.
    gone_path = os.path.join(XDIR, "media_gone.json")
    try:
        known_gone = set(json.load(open(gone_path)))
    except Exception:
        known_gone = set()
    fresh_gone = []
    n_ok = n_gone = 0
    for d in extra_dirs:
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".json"):
                continue
            sid = fn[:-5]
            try:
                rec = json.load(open(os.path.join(d, fn)))
            except Exception:
                continue
            for name in save_media(rec, sid, None):
                if name.startswith("GONE"):
                    n_gone += 1
                    url = name.rsplit(" ", 1)[-1]
                    if url not in known_gone:
                        fresh_gone.append(name)
                        known_gone.add(url)
                else:
                    n_ok += 1
    try:
        json.dump(sorted(known_gone), open(gone_path, "w"), indent=1)
    except Exception:
        pass
    for name in fresh_gone:
        log.append(f"    media NEWLY {name}")
    log.append(f"    backfill media: {n_ok} held, {n_gone} purged "
               f"({len(fresh_gone)} newly)")
    return n_ok, len(fresh_gone)


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

    # Sweep every record we hold for assets we never downloaded. Cheap after the
    # first pass (existing files are skipped), and it runs before the legs so a
    # newly recovered record gets its media on the very next tick.
    if "--backfill-media" in sys.argv or "--full" in sys.argv:
        ok, gone = backfill_media(
            [RAW, os.path.join(os.path.dirname(ROOT), "qtecqot-x-recovered", "raw")], lines)
        if gone:
            errors.append(f"{gone} asset(s) purged from the twimg CDN since the last sweep")

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

        # --- leg B2: replies, which leg B structurally cannot see.
        #
        # Cadence, not every tick: x_search is metered. The obvious trigger -- leg A's
        # tweets counter running ahead of the IDs we hold -- DOES NOT WORK, and the
        # measurement is worth recording: after capturing his two 2026-08-02 replies we
        # held 11 live statuses while the profile counter read 10. Replies do not
        # increment it. So the counter can never signal a new reply, and a fixed cadence
        # is the only honest option. Ten minutes bounds reply latency to ten minutes,
        # costs 144 calls/day, and is inside the ~1 h window in which he deletes.
        live_n = sum(1 for v in hs["statuses"].values() if v.get("state") == "live")
        counter_ahead = bool(prof) and prof.get("tweets", 0) > max(live_n, len(ids))
        if "--full" in sys.argv or counter_ahead or (now.minute % 10) < 2:
            ids2, note2 = leg_b2(handle)
            if not ids2:
                errors.append(f"@{handle} leg B2 (replies): {note2}")
            elif counter_ahead:
                lines.append(f"    leg B2 fired: counter {prof.get('tweets')} > "
                             f"{max(live_n, len(ids))} known -- {note2}")
            ids = sorted(set(ids) | set(ids2))

        # Numbers already proven not to be statuses. Without this the same bogus id is
        # re-harvested by leg B2, re-fetched, re-dropped and re-logged every ten minutes.
        ids = [i for i in ids if i not in hs.get("not_statuses", {})]
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
                    saved = save_media(rec, sid, lines)
                    lines.append(f"★★★ @{handle}: CAPTURED {sid} ({tw.get('created_at')}) "
                                 f"— {txt!r}" + (f" [media: {', '.join(saved)}]" if saved else ""))
                    lines.append(f"    {wayback_save(sid)} for {sid}")
                meta["state"] = "live"
                meta["last_live"] = now.isoformat()
            elif code == 404:
                # An id we have NEVER fetched successfully is not a deletion. leg B2
                # harvests 19-digit numbers out of grok's prose, and the account's own
                # user id (2048996761101078528) is itself a snowflake in a plausible
                # date range, so it passed the filter, entered state as "new", 404ed as
                # a status and fired "★★★ DELETED — !! NO LOCAL BODY, this one got
                # away". A false alarm at the loudest level is worse than no alarm: it
                # is the one line in this log that is supposed to mean drop everything.
                if prev == "new" and not os.path.exists(os.path.join(RAW, f"{sid}.json")):
                    lines.append(f"    not a status, dropping {sid} "
                                 f"(404 on first fetch, no body ever held)")
                    hs["statuses"].pop(sid, None)
                    hs.setdefault("not_statuses", {})[sid] = now.isoformat()
                    continue
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
