#!/usr/bin/env python3.12
"""
Feed watcher for the skinny-bob investigation.

YouTube's channel RSS endpoint (youtube.com/feeds/videos.xml?channel_id=UC...) is
reachable from this sandbox even though the rest of YouTube is IP-blocked. It needs no
API key and no cookies. It exposes, per video: title, published, **updated** (i.e. a
metadata-edit detector), view count and like count -- plus the channel's own creation
timestamp to the second.

Each run writes a timestamped snapshot and appends any CHANGE to watch/CHANGELOG.md.
Detects: new uploads, title edits, metadata edits (updated bumps), view/like deltas,
and videos that DISAPPEAR (deleted or made private) -- which for this subject would
itself be a significant event.

Usage:  python3.12 watch/watch.py            # fetch, snapshot, diff, log
        python3.12 watch/watch.py --quiet    # only print when something changed
Exit code 10 = something changed (useful for cron/alerting).
"""
import json, os, sys, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.abspath(__file__))
SNAPS = os.path.join(ROOT, "snapshots")
CHANGELOG = os.path.join(ROOT, "CHANGELOG.md")
NS = {'a':'http://www.w3.org/2005/Atom','yt':'http://www.youtube.com/xml/schemas/2015',
      'media':'http://search.yahoo.com/mrss/'}

CHANNELS = {
    "qtecqot":      "UCw1EA-KJud9OmMA5p7_MWgw",   # the 2026 channel under investigation
    "ivan0135":     "UCC5AjFfZHRvILhJfWw5UcDw",   # the 2011 channel -- any activity here is major
    "m21-b5q":      "UCRI2fYCRUkvxgmGaGqivqdA",   # the commenter qtecqot replied to
}

def fetch(cid):
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

def parse(xml):
    r = ET.fromstring(xml)
    out = {"channel_title": r.findtext('a:title', namespaces=NS),
           "channel_published": r.findtext('a:published', namespaces=NS),
           "videos": {}}
    for e in r.findall('a:entry', NS):
        vid = e.findtext('yt:videoId', namespaces=NS)
        rec = {"title": e.findtext('a:title', namespaces=NS),
               "published": e.findtext('a:published', namespaces=NS),
               "updated": e.findtext('a:updated', namespaces=NS)}
        g = e.find('media:group', NS)
        if g is not None:
            c = g.find('media:community', NS)
            if c is not None:
                st = c.find('media:statistics', NS); sr = c.find('media:starRating', NS)
                if st is not None: rec["views"] = int(st.get('views', 0))
                if sr is not None: rec["likes"] = int(sr.get('count', 0))
        out["videos"][vid] = rec
    return out

def diff(name, old, new):
    """Return a list of human-readable change lines."""
    ch = []
    if old is None:
        ch.append(f"BASELINE established for {name}: {len(new['videos'])} videos, "
                  f"channel created {new['channel_published']}")
        return ch
    if old.get("channel_title") != new.get("channel_title"):
        ch.append(f"★ {name}: CHANNEL RENAMED {old.get('channel_title')!r} -> {new.get('channel_title')!r}")
    ov, nv = old["videos"], new["videos"]
    for vid in nv.keys() - ov.keys():
        ch.append(f"★★★ {name}: NEW VIDEO {vid} — {nv[vid]['title']!r} published {nv[vid]['published']}")
    for vid in ov.keys() - nv.keys():
        ch.append(f"★★★ {name}: VIDEO GONE (deleted/private/aged out of feed) {vid} — {ov[vid]['title']!r}")
    for vid in ov.keys() & nv.keys():
        o, n = ov[vid], nv[vid]
        if o["title"] != n["title"]:
            ch.append(f"★★ {name}/{vid}: TITLE CHANGED {o['title']!r} -> {n['title']!r}")
        if o["updated"] != n["updated"]:
            ch.append(f"★★ {name}/{vid}: METADATA EDITED (updated {o['updated']} -> {n['updated']}) "
                      f"— check the description")
        if o["published"] != n["published"]:
            ch.append(f"★★ {name}/{vid}: PUBLISHED TIME CHANGED {o['published']} -> {n['published']}")
        for k in ("views", "likes"):
            if k in o and k in n and o[k] != n[k]:
                ch.append(f"    {name}/{vid}: {k} {o[k]} -> {n[k]} ({n[k]-o[k]:+d})")
    return ch

def latest_snapshot():
    """The last state we saw. latest.json is written every run; snapshots/ holds only
    the runs where something changed, so compare against latest.json."""
    p = os.path.join(ROOT, "latest.json")
    if os.path.exists(p):
        return json.load(open(p))
    files = sorted(f for f in os.listdir(SNAPS) if f.endswith(".json"))
    return json.load(open(os.path.join(SNAPS, files[-1]))) if files else None

def main():
    quiet = "--quiet" in sys.argv
    os.makedirs(SNAPS, exist_ok=True)
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y-%m-%dT%H%M%SZ")
    prev = latest_snapshot()
    cur = {"fetched_utc": now.isoformat(), "channels": {}, "errors": {}}
    for name, cid in CHANNELS.items():
        try:
            cur["channels"][name] = parse(fetch(cid))
        except Exception as e:
            # A fetch failure is NOT evidence of absence -- record it as an error.
            cur["errors"][name] = f"{type(e).__name__}: {e}"

    lines = []
    for name in CHANNELS:
        if name in cur["errors"]:
            lines.append(f"    ! {name}: FETCH FAILED ({cur['errors'][name]}) — "
                         f"this is an instrument failure, not an absence of change")
            continue
        old = (prev or {}).get("channels", {}).get(name) if prev else None
        lines += diff(name, old, cur["channels"][name])

    real = [l for l in lines if not l.startswith("    ") or "FETCH FAILED" in l]
    # Keep a snapshot file only when something changed; otherwise just record the check.
    # Avoids accumulating ~48 identical 2 KB files a day.
    if lines:
        json.dump(cur, open(os.path.join(SNAPS, f"{stamp}.json"), "w"), indent=1)
    json.dump(cur, open(os.path.join(ROOT, "latest.json"), "w"), indent=1)
    with open(os.path.join(ROOT, "checks.log"), "a") as w:
        w.write(f"{now.isoformat()} changes={len(lines)} errors={len(cur['errors'])}\n")
    if lines:
        with open(CHANGELOG, "a") as w:
            w.write(f"\n## {now.isoformat()}\n\n")
            for l in lines: w.write(f"- {l}\n")
    if lines and (not quiet or real):
        print(f"[{now.isoformat()}] {len(lines)} change line(s):")
        for l in lines: print("  " + l)
    elif not quiet:
        print(f"[{now.isoformat()}] no changes")
    return 10 if real else 0

if __name__ == "__main__":
    sys.exit(main())
