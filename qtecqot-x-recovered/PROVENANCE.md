# Provenance — recovered @qtecqot X posts

Captured **2026-08-02** into the working directory. Loose in the repo root on purpose; move it
into `archive/` when its home is decided.

## What is here

| path | what |
|---|---|
| `RECOVERED.md` | all 19 posts rendered in order, with live/deleted state and a Wayback link per post |
| `CERNOHAJEV_LEAD.md` | the one deleted post that names a real outside archive, and what follows from it |
| `SERPO_LEAD.md` | the first post named Project SERPO; SERPO Release 26a is headed "RETIRED KGB MAJOR IVAN WRITES" |
| `raw/<status_id>.json` | the primary evidence: one Twitter API v2 lookup per status |
| `raw/_cdx_listing.json` | the Wayback CDX query result the set was enumerated from |
| `media/0731_live_*.jpg` | the only two surviving images, from status `2083135181737914543` |
| `media/2026-08-02_deleted_*.png` | screenshot of a post deleted within ~1 h; the only copy that exists |

## Where it came from

X exposes no logged-out route to this timeline any more — the syndication profile endpoint
returns `entries: []`, every nitter mirror is behind Cloudflare or Anubis, and `x.com/qtecqot`
serves a JS shell. The set came instead from the Wayback Machine, which holds **Twitter API v2
tweet lookups** archived under the canonical tweet URL:

```bash
curl -s 'http://web.archive.org/cdx/search/cdx?url=twitter.com/qtecqot*&output=json&fl=timestamp,original'
curl -s 'https://web.archive.org/web/<ts>id_/https://twitter.com/qtecqot/status/<id>'
```

Who ran those API calls and archived them is **not established**. It is not this project.

## Why the set is trusted

1. The two posts already in the record (`2082002737362039094`, `2082380299598753907`) appear here
   with text and timestamps matching `reports/agent_qtecqot_dossier.md` §4.5 exactly.
2. A snowflake decode of every status ID — `(id >> 22) + 1288834974657 ms` — agrees with that
   record's own `created_at` to the second, 19 times out of 19.
3. Live-checking each ID against `api.fxtwitter.com` returns **8 live, 11 deleted (404)**, and the
   account's public post counter reads **8**. The live subset matches the public count exactly.
4. The `includes.users[0].public_metrics.tweet_count` carried in each record — the author's post
   counter at the instant of posting — moves consistently with the deletions, resetting to 1 on
   2026-05-25 09:50 and again on 2026-07-28 07:18.

## Limits

- **Completeness is guaranteed for live posts only.** Point 3 pins the live set. For deleted posts
  the archive only holds what its operator happened to look up, so **11 deleted is a lower bound**.
- **Going forward this is fixed.** `watch/xwatch.py` (installed to cron 2026-08-02, every 2 min)
  captures each new status and its media within minutes of posting, and logs deletions against a
  body we already hold. Everything above was recovered after the fact; nothing after 2026-08-02
  12:17 UTC has to be.
- Media for deleted posts is unrecoverable. X purges it on delete, `pbs.twimg.com` returns 404 for
  all four, and neither the Wayback Machine nor archive.today holds a copy.
- One deleted post (`2052271474304750075`, 2026-05-07) consists of a **personal name** and an image.
  Redaction-critical: it must not reach anything published. See `AGENTS.md`, and the precedent in
  `reports/agent_zip_toolkit.md`.

## What it changes in the record

Not yet folded into `FINDINGS.md`, the dossier, or `CORRECTIONS.md`. Outstanding:

- **§2, §23** — the X account was not dormant from April to July. It posted 30 minutes after
  registration and was **wiped before 2026-07-28 07:18:28**, inside or before the eleven-minute
  activation window. Relaunch, not activation.
- **§4.5** — "the two tweets" is 19, of which 11 deleted.
- **§9** — "replies to anyone, ever: 1" is wrong; at least three replies to third parties plus two
  retweets, one of them deleted and reposted.
- **§3, the clock** — needs redoing from scratch against all 19 instants. The clean CEST
  06:23–11:39 morning band does not survive: counting acts outside 07:00–24:00 local gives
  **Moscow 5, CEST 7, US Pacific 10, US Eastern 11**. This one needs new analysis, not new text.
- **§6.2** — his 2026-08-02 reply to `@CytHyper` asserts "Case 28 belongs to tape 5, not tape 4",
  which agrees with our own ledger.

## Bonus: the username change is now bounded to 29½ minutes

The dossier (§9, and `docs/TIMELINE.md` line 211) carries an open item: X's "About this account"
panel records **one username change, last in April 2026**, prior handle not recoverable.

Every one of the 19 archived records carries `includes.users[0].username` **and** a
`public_metrics.tweet_count` that matches the post's own position in the sequence (1, 2, 3, 1, 2 …).
The counters being at-post-time means each lookup was made at or near the moment of posting, so the
username in each record is the username as it stood then. All 19 read `qtecqot`, the earliest at
**2026-04-28 05:54:16**.

The account was created **2026-04-28 05:24:54**. The rename therefore happened inside a window of
**29 minutes 22 seconds**, during which the account had zero posts and one follower.

That is the signature of the ordinary signup flow — X auto-assigns a handle and the user changes it
minutes later. **The open item can be closed as carrying no information**, rather than left standing
as an unexplained rename. The prior handle stays unrecoverable and is now also uninteresting.

A *second* rename would be a different matter, and `watch/xwatch.py` now flags `screen_name` changes
at the loudest level.
