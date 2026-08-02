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

## Attached media: what survives, what the CDN has purged

Added 2026-08-02, after noticing that nothing had ever swept the *recovered* records for
attached assets. Leg C of `watch/xwatch.py` downloaded media at the moment it captured a
status, but the archived Twitter API v2 bodies came in by a different route and use a
different JSON shape, so the reader saw nothing in them. The URLs had been sitting in
`raw/*.json` unfetched. `xwatch.py --backfill-media` now walks any record shape and sweeps
every record we hold; it runs automatically on the hourly `--full` pass.

X purges `pbs.twimg.com` assets when a post is deleted, but **not reliably and not always**.
Of 19 asset URLs across the 20 records:

| | |
|---|---|
| **12 still served** | downloaded to `watch/x/media/`, sha256 in this repo |
| **7 already purged (404)** | URL recorded, asset gone |

**Purged, and these are the losses that matter:**

- `2052271474304750075_1` — the **Valerijs Černohajev photograph**, 2026-05-07. Gone.
- `2066148832728207700_1`, `2066151685723169249_1` — the two 2026-06-14 "rel. 6 / 8" cards.
- `2083134567695925347_1/2` — a deleted 2026-07-31 pair.

**Held, and one of them is not what it looked like at first.** Deleted post
`2066149533432807512` (2026-06-14 13:23:30, a reply reading *"he is confirmed real.
continuation of series on my Youtube. There are others survivors"*) carried a **19.48 s
1920×1080 H.264 video**, `watch/x/media/2066149533432807512_4.mp4`,
sha256 `4f2beb5f96680714541b3de55b0e51463e61306464452e1896f5a2879f65000f`. Burned-in
timecodes read `25 00:00:45` and `25 00:27:39`–`27:42`.

It is **not new footage.** Sampled at 2 fps, mean-subtracted, normalised 32×32 greyscale
cross-correlation against every 2026 and 2011 video in `videos/`:

| compared against | frames | median best NCC | frames > 0.97 |
|---|---|---|---|
| the three 2026 videos | 660 | 0.72–0.77 | **0 of 38** |
| the four 2011 videos | 610 | **0.991** | **36 of 38** |

Best matches are all to **`RsQCXN4o4Ps`**, ivan0135's 2011 upload — the same video his two
YouTube comments sit under. So the deleted post attached a re-encode of 2011 material while
asserting the subject is "confirmed real", and was then removed.

Two caveats on that table, both real. The 2 fps sampling and 32×32 downscale make this a
*shot-level* identity test, not a frame-level one: it establishes the clip is drawn from
`RsQCXN4o4Ps`, not that it is bit-identical or that no frame was altered. And the near-black
cut frame at 10.0 s matches near-black frames in all seven videos at NCC 1.000, which is an
artefact of comparing low-variance frames and was excluded from the counts above.

The X copy runs **831 kbps**, against 932–1424 kbps for `videos/2026-avc/` and 310–439 kbps
for `videos/2026/`. It is an independent X transcode of whatever the uploader supplied, so it
is useful as a **cross-encoder control** in the sense of `FINDINGS.md` §17, and useless as a
quality upgrade. Check `CORPUS_QUALITY.md` before drawing an absence from it.
