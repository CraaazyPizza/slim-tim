#!/usr/bin/env python3.12
"""
X/Twitter capture daemon for @qtecqot (and any other handle in HANDLES).

Why this exists: on 2026-08-02 the account posted a "Fake copycat channel" tweet
linking youtube.com/@qtecqot2 and deleted it inside ~1 hour. Nothing archived it.
The only surviving copy is a browser screenshot a human happened to take. The
2026-05-25 purge (three posts erased eleven minutes after video 1 went public) was
recovered only because a stranger's Twitter API v2 lookups happened to be in the
Wayback Machine. Neither is a method. This is.

Independent legs, so no single blocked endpoint means silent data loss:

  A. COUNTER TRIPWIRE - api.fxtwitter.com/<handle>. Cheap, never blocked, and the
     counters move the instant anything happens: tweets +/-, media_count, following
     (a follow/unfollow), likes (he liked something), followers, name, bio, avatar.
     A tweets increment followed by a decrement IS a post-and-delete, bounded to the
     poll interval even if every other leg failed to catch the body.

  B. TIMELINE ENUMERATION - nitter RSS mirrors, tried in order until one parses.
     Yields status IDs. New ID -> leg C archives it.

  B2. REPLIES + EXACT API RECORD - the official X user-post timeline. Unlike RSS,
      it includes replies by default and returns structured IDs, referenced posts,
      edit metadata, engagement and media. The first successful call backfills the
      current account timeline; later calls keep checking the newest five posts.

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
import fcntl, json, os, re, shutil, subprocess, sys, tempfile, time, urllib.request, urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

import xapi_client

ROOT = os.path.dirname(os.path.abspath(__file__))
XDIR = os.path.join(ROOT, "x")
RAW = os.path.join(XDIR, "raw")
API_RAW = os.path.join(XDIR, "api_raw")
MEDIA = os.path.join(XDIR, "media")
REVISIONS = os.path.join(XDIR, "revisions")
METRICS = os.path.join(XDIR, "metrics")
STATE = os.path.join(XDIR, "state.json")
HEALTH = os.path.join(XDIR, "health.json")
CHANGELOG = os.path.join(XDIR, "CHANGELOG.md")
CHECKLOG = os.path.join(XDIR, "check.log")
LOCK = os.path.join(XDIR, ".xwatch.lock")

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


def write_state_atomic(state):
    """Replace state only after a complete JSON file is safely on disk."""
    fd, tmp = tempfile.mkstemp(prefix=".state.", suffix=".tmp", dir=XDIR)
    try:
        with os.fdopen(fd, "w") as w:
            json.dump(state, w, indent=1, ensure_ascii=False)
            w.flush()
            os.fsync(w.fileno())
        if os.path.exists(STATE) and os.path.getsize(STATE) > 0:
            shutil.copy2(STATE, STATE + ".bak")
        os.replace(tmp, STATE)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def write_json_atomic(path, value):
    """Atomically write any JSON evidence/health file."""
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".json.", suffix=".tmp", dir=directory)
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(value, stream, indent=1, ensure_ascii=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def load_health():
    """Load durable per-leg health without ever confusing damage with health."""
    try:
        value = json.load(open(HEALTH))
        if isinstance(value, dict) and isinstance(value.get("legs"), dict):
            return value
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass
    return {"schema": 1, "legs": {}}


def set_leg_health(health, name, status, now, detail, **extra):
    """Update a leg while retaining the last time it actually succeeded."""
    previous = health.setdefault("legs", {}).get(name) or {}
    item = {
        "status": status,
        "last_attempt": now.isoformat(),
        "last_success": now.isoformat() if status == "ok" else previous.get("last_success"),
        "detail": detail,
        "last_error": (detail if status in ("error", "unconfigured")
                       else previous.get("last_error")),
        "last_error_at": (now.isoformat() if status in ("error", "unconfigured")
                          else previous.get("last_error_at")),
    }
    item.update(extra)
    health["legs"][name] = item
    return item


VOLATILE_RECORD_KEYS = {
    "bookmarks", "bookmark_count", "captured_at", "followers", "following",
    "impression_count", "like_count", "likes", "media_count", "non_public_metrics",
    "organic_metrics", "promoted_metrics", "public_metrics", "quote_count", "quotes",
    "replies", "reply_count", "repost_count", "retweet_count", "retweets", "views",
}


def semantic_record(value):
    """Strip engagement/capture-time drift, retaining content and attribution."""
    if isinstance(value, dict):
        return {key: semantic_record(item) for key, item in value.items()
                if key not in VOLATILE_RECORD_KEYS}
    if isinstance(value, list):
        return [semantic_record(item) for item in value]
    return value


def write_revisioned(path, value, sid, now, source):
    """Update the current record only after preserving every semantic revision."""
    try:
        with open(path) as stream:
            old = json.load(stream)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        write_json_atomic(path, value)
        return True, False
    if semantic_record(old) == semantic_record(value):
        return False, False
    directory = os.path.join(REVISIONS, sid)
    os.makedirs(directory, exist_ok=True)
    initial = os.path.join(directory, f"initial-{source}.json")
    if not os.path.exists(initial):
        write_json_atomic(initial, old)
    stamp = now.strftime("%Y%m%dT%H%M%S.%fZ")
    write_json_atomic(os.path.join(directory, f"{stamp}-{source}.json"), value)
    write_json_atomic(path, value)
    return False, True


def record_metrics(sid, now, source, values, minimum_interval=1800):
    """Keep useful engagement history without committing two-minute heartbeat noise."""
    values = {key: value for key, value in values.items() if value is not None}
    if not values:
        return False
    path = os.path.join(METRICS, f"{sid}.json")
    try:
        with open(path) as stream:
            history = json.load(stream)
        if not isinstance(history, list):
            history = []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        history = []
    prior = next((item for item in reversed(history) if item.get("source") == source), None)
    if prior and prior.get("values") == values:
        return False
    if prior and minimum_interval:
        try:
            then = datetime.fromisoformat(prior["at"].replace("Z", "+00:00"))
            if (now - then).total_seconds() < minimum_interval:
                return False
        except (KeyError, TypeError, ValueError):
            pass
    history.append({"at": now.isoformat(), "source": source, "values": values})
    write_json_atomic(path, history)
    return True


def load_state():
    """Load the primary state, falling back to the last atomic-write backup."""
    for path in (STATE, STATE + ".bak"):
        try:
            with open(path) as r:
                state = json.load(r)
            if isinstance(state, dict) and isinstance(state.get("handles"), dict):
                return state
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            pass
    if not os.path.exists(STATE):
        return {"handles": {}}
    raise RuntimeError(f"xwatch state is corrupt and no valid backup exists: {STATE}")


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


def official_media_record(record):
    """Limit media download to this post, or the original item it reposts.

    Official reply expansions can include the parent's media. We preserve that
    context in api_raw but do not mislabel/download it as the reply's attachment.
    """
    data = record.get("data") or {}
    includes = record.get("includes") or {}
    target = data
    refs = xapi_client.referenced_items(data)
    repost = next((ref for ref in refs if ref.get("type") in ("retweeted", "reposted")), None)
    if repost:
        target = next((tweet for tweet in xapi_client.included_posts(includes)
                       if str(tweet.get("id")) == str(repost.get("id"))), data)
    keys = set((target.get("attachments") or {}).get("media_keys") or [])
    media = [item for item in includes.get("media") or [] if item.get("media_key") in keys]
    return {"data": target, "includes": {"media": media}}


def archive_official_records(records, now, log):
    """Persist exact API v2 records before any secondary mirror is consulted."""
    fresh_ids = []
    for sid, record in sorted(records.items()):
        path = os.path.join(API_RAW, f"{sid}.json")
        fresh, revised = write_revisioned(path, record, sid, now, "official-x")
        saved = save_media(official_media_record(record), sid, log)
        tweet = record.get("data") or {}
        record_metrics(sid, now, "official-x", tweet.get("public_metrics") or {})
        if fresh:
            refs = xapi_client.referenced_items(tweet)
            kind = "reply" if any(ref.get("type") in ("replied_to", "replied") for ref in refs) else \
                   "repost" if any(ref.get("type") in ("retweeted", "reposted") for ref in refs) else "post"
            text = (tweet.get("text") or "").replace("\n", " / ")[:220]
            log.append(f"★★★ @qtecqot: OFFICIAL API CAPTURED {sid} {kind} "
                       f"({tweet.get('created_at')}) — {text!r}" +
                       (f" [media: {', '.join(saved)}]" if saved else ""))
            fresh_ids.append(sid)
        elif revised:
            text = (tweet.get("text") or "").replace("\n", " / ")[:220]
            log.append(f"★★★ @qtecqot: OFFICIAL API CONTENT UPDATED {sid} — {text!r} "
                       f"[prior and new versions archived]")
    return fresh_ids


def leg_official_x(handle_state, now, log):
    """Fetch the official user timeline, including replies, and archive it."""
    token = xapi_client.bearer_token()
    if not token:
        return [], None, "not configured: X_BEARER_TOKEN is absent"
    user_id = str((handle_state.get("profile") or {}).get("id") or "2048996761101078528")
    source_state = handle_state.setdefault("official_x", {})
    full_backfill = not source_state.get("backfill_complete", False)
    try:
        if full_backfill:
            results = [xapi_client.get_user_posts(
                user_id, token, now.isoformat(), full_backfill=True, max_results=100)]
            mode = "full backfill"
        else:
            newest = source_state.get("newest_id")
            results = [xapi_client.get_user_posts(
                user_id, token, now.isoformat(), full_backfill=False, max_results=100,
                since_id=newest)]
            mode = "new-since-last poll"
            # since_id deliberately does not return older items that were edited.
            # Re-read five recent items every ten minutes to preserve semantic edits.
            if (now.minute % 10) < 2:
                results.append(xapi_client.get_user_posts(
                    user_id, token, now.isoformat(), full_backfill=False, max_results=5))
                mode += " + edit probe"
    except xapi_client.XApiError as exc:
        return [], None, str(exc)
    records = {}
    for result in results:
        records.update(result.records)
    archive_official_records(records, now, log)
    if full_backfill and results[0].complete:
        source_state["backfill_complete"] = True
        source_state["backfilled_at"] = now.isoformat()
    newest_ids = [result.newest_id for result in results if result.newest_id]
    oldest_ids = [result.oldest_id for result in results if result.oldest_id]
    if newest_ids:
        source_state["newest_id"] = max(newest_ids, key=int)
    if oldest_ids:
        oldest = min(oldest_ids, key=int)
        previous_oldest = source_state.get("oldest_id")
        source_state["oldest_id"] = min([oldest, previous_oldest], key=int) \
            if previous_oldest else oldest
    note = (f"ok ({len(records)} unique posts, {sum(item.pages for item in results)} page(s), "
            f"{mode})")
    return sorted(records), note, None


def leg_xai_fallback(handle):
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
                    # news_img/* and card_img/* are link-preview thumbnails, not media
                    # he attached. Tracking either as a lost attachment is a false alarm.
                    if k in ("url", "media_url", "media_url_https", "preview_image_url") \
                            and "/news_img/" not in v and "/card_img/" not in v:
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
            # A killed process used to leave a non-empty partial file which every
            # later pass then treated as complete. Publish only a fully received,
            # fsynced response.
            fd, tmp = tempfile.mkstemp(prefix=f".{sid}_{i}.", suffix=".tmp", dir=MEDIA)
            try:
                with os.fdopen(fd, "wb") as stream:
                    stream.write(body)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(tmp, path)
            finally:
                if os.path.exists(tmp):
                    os.unlink(tmp)
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
        write_json_atomic(gone_path, sorted(known_gone))
    except Exception:
        pass
    for name in fresh_gone:
        log.append(f"    media NEWLY {name}")
    log.append(f"    backfill media: {n_ok} held, {n_gone} purged "
               f"({len(fresh_gone)} newly)")
    return n_ok, n_gone, len(fresh_gone)


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
    for d in (XDIR, RAW, API_RAW, MEDIA, REVISIONS, METRICS):
        os.makedirs(d, exist_ok=True)
    lock_file = open(LOCK, "w")
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return 0
    state = load_state()

    if "--backfill" in sys.argv:
        ids = [a for a in sys.argv[sys.argv.index("--backfill") + 1:] if a.isdigit()]
        h = state["handles"].setdefault(HANDLES[0], {"profile": None, "statuses": {}})
        for sid in ids:
            h["statuses"].setdefault(sid, {"first_seen": None, "state": "unknown"})
        print(f"backfilled {len(ids)} ids")

    now = datetime.now(timezone.utc)
    lines, errors = [], []
    health = load_health()
    health.update({"schema": 1, "generated_at": now.isoformat(), "pid": os.getpid()})

    # Sweep every record we hold for assets we never downloaded. Cheap after the
    # first pass (existing files are skipped), and it runs before the legs so a
    # newly recovered record gets its media on the very next tick.
    if "--backfill-media" in sys.argv or "--full" in sys.argv:
        ok, standing_gone, gone = backfill_media(
            [RAW, API_RAW, os.path.join(os.path.dirname(ROOT), "qtecqot-x-recovered", "raw")], lines)
        set_leg_health(health, "media_archive", "error" if gone else "ok", now,
                       f"{ok} asset references resolved locally; {standing_gone} historical "
                       f"attached URLs unavailable; {gone} newly unavailable",
                       held_references=ok, unavailable_references=standing_gone,
                       newly_unavailable=gone)
        if gone:
            errors.append(f"{gone} asset(s) purged from the twimg CDN since the last sweep")
    else:
        set_leg_health(health, "media_archive", "standby", now,
                       "Full local/remote media sweep runs hourly; immediate downloads still run per capture")

    for handle in HANDLES:
        hs = state["handles"].setdefault(handle, {"profile": None, "statuses": {}})

        # --- leg A
        prof, err = leg_a(handle)
        if err:
            set_leg_health(health, "profile_counters", "error", now, err)
            errors.append(f"@{handle} leg A (counters): {err}")
        elif hs["profile"] is None:
            set_leg_health(health, "profile_counters", "ok", now,
                           f"profile and counters fetched for @{handle}")
            lines.append(f"BASELINE @{handle}: {prof['tweets']} posts, "
                         f"{prof['followers']} followers, {prof['following']} following, "
                         f"{prof['likes']} likes, {prof['media_count']} media")
            hs["profile"] = prof
        else:
            set_leg_health(health, "profile_counters", "ok", now,
                           f"profile and counters fetched for @{handle}")
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
            set_leg_health(health, "timeline_rss", "error", now, note)
            errors.append(f"@{handle} leg B (timeline): {note}")
        else:
            set_leg_health(health, "timeline_rss", "ok", now, note, ids=len(ids))

        # --- leg B2: exact structured user timeline, including replies.
        official_ids, official_note, official_error = leg_official_x(hs, now, lines)
        if official_error:
            official_status = "unconfigured" if official_error.startswith("not configured:") else "error"
            set_leg_health(health, "official_x_api", official_status, now, official_error,
                           configured=official_status != "unconfigured")
            errors.append(f"@{handle} leg B2 (official replies): {official_error}")
        else:
            set_leg_health(health, "official_x_api", "ok", now, official_note,
                           configured=True, ids=len(official_ids), replies_included=True)
            lines.append(f"    official X API: {official_note}")
            ids = sorted(set(ids) | set(official_ids))

        # xAI is only an emergency fallback. It is non-deterministic and previously
        # returned the account's user id as though it were a status. Never invoke it
        # every two minutes, and never prefer it over the official timeline.
        if official_error and ("--full" in sys.argv or (now.minute % 10) < 2):
            fallback_ids, fallback_note = leg_xai_fallback(handle)
            if not fallback_ids:
                set_leg_health(health, "xai_reply_fallback", "error", now, fallback_note)
                errors.append(f"@{handle} leg B3 (xAI reply fallback): {fallback_note}")
            else:
                set_leg_health(health, "xai_reply_fallback", "ok", now, fallback_note,
                               ids=len(fallback_ids))
                lines.append(f"    xAI reply fallback: {fallback_note}")
                ids = sorted(set(ids) | set(fallback_ids))
        elif not official_error:
            set_leg_health(health, "xai_reply_fallback", "standby", now,
                           "Not needed because the official X API succeeded")
        else:
            previous_xai = health.get("legs", {}).get("xai_reply_fallback") or {}
            set_leg_health(health, "xai_reply_fallback", "standby", now,
                           "Fallback is attempted every 10 minutes while official X is unavailable",
                           last_success=previous_xai.get("last_success"))

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
        capture_errors_before = len(errors)
        checked = 0
        for sid, meta in sorted(hs["statuses"].items()):
            if sid not in new_ids:
                if not sweep:
                    continue
                if meta.get("state") == "deleted" and not full:
                    continue  # deletions do not reverse; --full re-checks anyway
            rec, code = fetch_status(handle, sid)
            checked += 1
            prev = meta.get("state")
            if code == 200 and rec:
                path = os.path.join(RAW, f"{sid}.json")
                fresh, revised = write_revisioned(path, rec, sid, now, "fxtwitter")
                tw = rec.get("tweet") or {}
                record_metrics(sid, now, "fxtwitter", {
                    key: tw.get(key) for key in
                    ("replies", "retweets", "likes", "bookmarks", "quotes", "views")
                })
                if fresh:
                    txt = (tw.get("text") or "").replace("\n", " / ")[:220]
                    saved = save_media(rec, sid, lines)
                    lines.append(f"★★★ @{handle}: CAPTURED {sid} ({tw.get('created_at')}) "
                                 f"— {txt!r}" + (f" [media: {', '.join(saved)}]" if saved else ""))
                    lines.append(f"    {wayback_save(sid)} for {sid}")
                elif revised:
                    txt = (tw.get("text") or "").replace("\n", " / ")[:220]
                    saved = save_media(rec, sid, lines)
                    lines.append(f"★★★ @{handle}: CONTENT UPDATED {sid} — {txt!r} "
                                 f"[prior and new versions archived]" +
                                 (f" [media: {', '.join(saved)}]" if saved else ""))
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
                held_body = (os.path.exists(os.path.join(RAW, f"{sid}.json")) or
                             os.path.exists(os.path.join(API_RAW, f"{sid}.json")))
                if prev == "new" and not held_body:
                    lines.append(f"    not a status, dropping {sid} "
                                 f"(404 on first fetch, no body ever held)")
                    hs["statuses"].pop(sid, None)
                    hs.setdefault("not_statuses", {})[sid] = now.isoformat()
                    continue
                if prev in ("live", "new"):
                    if os.path.exists(os.path.join(RAW, f"{sid}.json")):
                        have = f"body archived at x/raw/{sid}.json"
                    elif os.path.exists(os.path.join(API_RAW, f"{sid}.json")):
                        have = f"official body archived at x/api_raw/{sid}.json"
                    else:
                        have = "!! NO LOCAL BODY -- this one got away"
                    lines.append(f"★★★ @{handle}: DELETED {sid} "
                                 f"(last seen live {meta.get('last_live','?')}) — {have}")
                meta["state"] = "deleted"
                meta.setdefault("deleted_noticed", now.isoformat())
            else:
                errors.append(f"@{handle} leg C: status {sid} returned {code}")

        capture_failed = len(errors) > capture_errors_before
        set_leg_health(
            health, "status_capture", "error" if capture_failed else "ok", now,
            (f"checked {checked} status(es); full liveness sweep={'yes' if sweep else 'no'}; "
             f"{len(new_ids)} newly enumerated"), checked=checked, full_sweep=sweep,
            known_statuses=len(hs["statuses"]), newly_enumerated=len(new_ids))

    real = [l for l in lines if not l.startswith("    ")]
    os.makedirs(XDIR, exist_ok=True)
    write_state_atomic(state)
    degraded = [name for name, item in health.get("legs", {}).items()
                if item.get("status") in ("error", "unconfigured")]
    health["overall"] = "degraded" if degraded else "healthy"
    health["degraded_legs"] = degraded
    health["counts"] = {
        "errors_this_pass": len(errors),
        "changes_this_pass": len(real),
        "known_statuses": sum(len(h.get("statuses") or {})
                              for h in state.get("handles", {}).values()),
        "local_raw_records": len([name for name in os.listdir(RAW) if name.endswith(".json")]),
        "official_raw_records": len([name for name in os.listdir(API_RAW) if name.endswith(".json")]),
        "media_files": len([name for name in os.listdir(MEDIA) if os.path.isfile(os.path.join(MEDIA, name))]),
        "revision_sets": len([name for name in os.listdir(REVISIONS)
                              if os.path.isdir(os.path.join(REVISIONS, name))]),
        "metric_histories": len([name for name in os.listdir(METRICS) if name.endswith(".json")]),
    }
    # Keep persistent degradation visible in health/check.log without appending the
    # same paragraph to CHANGELOG and cron.log every two minutes. Re-announce a
    # standing error daily so it never disappears indefinitely.
    reported = health.setdefault("reported_errors", {})
    reportable_errors = []
    for message in errors:
        item = reported.get(message) or {}
        should_report = not item.get("last_reported")
        if not should_report:
            try:
                last = datetime.fromisoformat(item["last_reported"].replace("Z", "+00:00"))
                should_report = (now - last).total_seconds() >= 86400
            except (TypeError, ValueError):
                should_report = True
        item["last_seen"] = now.isoformat()
        if should_report:
            item["last_reported"] = now.isoformat()
            reportable_errors.append(message)
        reported[message] = item
    write_json_atomic(HEALTH, health)
    with open(CHECKLOG, "a") as w:
        w.write(f"{now.isoformat()} changes={len(real)} notes={len(lines)-len(real)} "
                f"errors={len(errors)}\n")
    if lines or reportable_errors:
        with open(CHANGELOG, "a") as w:
            w.write(f"\n## {now.isoformat()}\n\n")
            for l in lines:
                w.write(f"- {l}\n")
            for e in reportable_errors:
                w.write(f"- ! ERROR (instrument failure, NOT an absence of change): {e}\n")

    # Keep the offline viewer synchronized with the evidence and health state. A
    # failure is visible in health.json and the next successful cron pass retries.
    try:
        built = subprocess.run([sys.executable, os.path.join(ROOT, "build_timeline.py")],
                               cwd=ROOT, capture_output=True, text=True, timeout=60)
        if built.returncode:
            set_leg_health(health, "offline_viewer", "error", now,
                           (built.stderr or built.stdout).strip()[:500])
        else:
            set_leg_health(health, "offline_viewer", "ok", now,
                           (built.stdout.strip().splitlines()[-1] if built.stdout.strip()
                            else "viewer rebuilt"))
    except Exception as exc:
        set_leg_health(health, "offline_viewer", "error", now,
                       f"{type(exc).__name__}: {exc}")
    degraded = [name for name, item in health.get("legs", {}).items()
                if item.get("status") in ("error", "unconfigured")]
    health["overall"] = "degraded" if degraded else "healthy"
    health["degraded_legs"] = degraded
    write_json_atomic(HEALTH, health)
    if real and "--commit" in sys.argv:
        print("  git: " + git_commit(f"xwatch: {len(real)} change(s) at {now.isoformat()}"))
    if not quiet or real or reportable_errors:
        print(f"[{now.isoformat()}] {len(real)} change(s), {len(errors)} error(s)")
        for l in lines:
            print("  " + l)
        for e in (errors if not quiet else reportable_errors):
            print("  ! " + e)
    return 10 if real else 0


if __name__ == "__main__":
    sys.exit(main())
