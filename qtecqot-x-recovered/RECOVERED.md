# @qtecqot — every recovered X post, 2026-04-28 → 2026-08-02

Recovered 2026-08-02, extended the same day by the watcher. **12 of 22 are deleted** (marked
DELETED). The header read "11 of 19" until 2026-08-02 16:00 UTC; three posts have been added
since — the screenshot-only copycat card and the two 13:0x replies at the foot of this file.

**Composition, because a reader asked whether replies were in here at all:** 13 originals,
7 replies (3 on his own thread, 4 to another account) and 2 reposts. Every entry carries a
`type:` line — `original`, `replied_to → <id>`, or `retweeted → <id>` — and always has. The
dossier is where they were missing; see `CORRECTIONS.md`, 2026-08-02 (later).

`tweet_count` is the author's post counter *at the moment that tweet was posted* — it is the
evidence for the deletions: it resets to 1 on 2026-05-25 09:50 and again on 2026-07-28 07:18.


## Provenance — how each post below was obtained

X exposes no logged-out route to this timeline (syndication returns `entries: []`, nitter mirrors
are behind Cloudflare/Anubis, x.com serves a JS shell). Every post below comes from a **Wayback
Machine capture of a Twitter API v2 tweet lookup**, archived under the canonical tweet URL.

**Enumeration** — the complete set of archived statuses:

```bash
curl -s 'http://web.archive.org/cdx/search/cdx?url=twitter.com/qtecqot*&output=json&fl=timestamp,original'
```

**Retrieval** — each post's `Archived:` link below is the exact capture used. The `id_` suffix
requests the raw archived bytes with no Wayback rewriting.

**Live/deleted state** — each ID was checked against `api.fxtwitter.com`, which reads live X:
404 = deleted. Independently, an xAI Agent Tools `x_search` over `@qtecqot` (2026-04-01 → 2026-08-02,
replies and retweets included) returned **exactly the 8 LIVE ids and nothing before 2026-07-28**,
matching X's own public post counter of 8.

**Not established:** who ran the API calls that the Wayback Machine archived. It was not this project.

**Completeness:** guaranteed for LIVE posts (pinned twice over). For deleted posts the archive holds
only what its operator happened to look up, so **12 deleted is a lower bound**.

**Replies specifically.** The `x_search` pass above ran with replies and retweets included, and the
CDX enumeration is by status URL, so neither route treats a reply differently from an original.
There is no known reply-shaped gap. But note the floor is lower here than for originals: X's
logged-out profile timeline omits replies entirely and `x.com/qtecqot/with_replies` is login-walled,
so a deleted reply that no one ever looked up leaves less trace than a deleted original. One post is
already known to have left no trace at all — the copycat card below, which survives only as a
screenshot.


---


## 2026-04-28 05:54:16 UTC — DELETED

`2049004250995507595`  ·  https://x.com/qtecqot/status/2049004250995507595

- type: original
- conversation: `2049004250995507595`
- author at post time: 1 posts · 0 followers · 2 following · 0 likes given · 0 media
- **Archived:** https://web.archive.org/web/20260428055416id_/https://twitter.com/qtecqot/status/2049004250995507595
- **Local copy:** `raw/2049004250995507595.json`
- **Live check:** `curl -s https://api.fxtwitter.com/qtecqot/status/2049004250995507595` → 404 (deleted)

```
ivan   compromised, UNK cond.
2026-04-21  15:30:12 UTC

release 5 -8 is triggered

Иван
СЕРПО
раскрытие
```

## 2026-05-07 06:17:03 UTC — DELETED

`2052271474304750075`  ·  https://x.com/qtecqot/status/2052271474304750075

- type: replied_to → 2049004250995507595  (@qtecqot)
- conversation: `2049004250995507595`
- author at post time: 2 posts · 0 followers · 4 following · 0 likes given · 1 media
- media: photo 595×449 https://pbs.twimg.com/media/HHsh_cxaUAAtlAf.png **(404 — X purges media on delete)**
- link: https://t.co/skYhOP6KkU → https://x.com/qtecqot/status/2052271474304750075/photo/1
- **Archived:** https://web.archive.org/web/20260507061703id_/https://twitter.com/qtecqot/status/2052271474304750075
- **Local copy:** `raw/2052271474304750075.json`
- **Live check:** `curl -s https://api.fxtwitter.com/qtecqot/status/2052271474304750075` → 404 (deleted)

```
Valerijs Černohajev https://t.co/skYhOP6KkU
```

## 2026-05-25 09:46:14 UTC — DELETED

`2058847096904855681`  ·  https://x.com/qtecqot/status/2058847096904855681

- type: original
- conversation: `2058847096904855681`
- author at post time: 3 posts · 0 followers · 3 following · 1 likes given · 1 media
- **Archived:** https://web.archive.org/web/20260525094614id_/https://twitter.com/qtecqot/status/2058847096904855681
- **Local copy:** `raw/2058847096904855681.json`
- **Live check:** `curl -s https://api.fxtwitter.com/qtecqot/status/2058847096904855681` → 404 (deleted)

```
Disclosure footage release upload No.1 complete.
2026/05/25, YT.  ufo-ebe.
```

## 2026-05-25 09:50:36 UTC — DELETED

`2058848196907200562`  ·  https://x.com/qtecqot/status/2058848196907200562

- type: original
- conversation: `2058848196907200562`
- author at post time: 1 posts · 0 followers · 3 following · 1 likes given · 0 media
- **Archived:** https://web.archive.org/web/20260525095036id_/https://twitter.com/qtecqot/status/2058848196907200562
- **Local copy:** `raw/2058848196907200562.json`
- **Live check:** `curl -s https://api.fxtwitter.com/qtecqot/status/2058848196907200562` → 404 (deleted)

```
Disclosure footage upload No.1 complete 
2026/05/25  YT
ufo-ebe material resumption of transparency
```

## 2026-06-14 13:20:43 UTC — DELETED

`2066148832728207700`  ·  https://x.com/qtecqot/status/2066148832728207700

- type: original
- conversation: `2066148832728207700`
- author at post time: 2 posts · 0 followers · 3 following · 2 likes given · 1 media
- media: photo 1920×1080 https://pbs.twimg.com/media/HKxvPawbEAAuEqP.png **(404 — X purges media on delete)**
- link: https://t.co/ZRP0BoQ8da → https://x.com/qtecqot/status/2066148832728207700/photo/1
- **Archived:** https://web.archive.org/web/20260614132043id_/https://twitter.com/qtecqot/status/2066148832728207700
- **Local copy:** `raw/2066148832728207700.json`
- **Live check:** `curl -s https://api.fxtwitter.com/qtecqot/status/2066148832728207700` → 404 (deleted)

```
Next drop imminent: rel. 6 / 8.  subscribe to the YT channel. #skinnybob https://t.co/ZRP0BoQ8da
```

## 2026-06-14 13:23:30 UTC — DELETED

`2066149533432807512`  ·  https://x.com/qtecqot/status/2066149533432807512

- type: replied_to → 2059688614695670011  (@_halkyofu_)
- conversation: `2059688614695670011`
- author at post time: 3 posts · 0 followers · 3 following · 2 likes given · 1 media
- media: **none of his own.** `data.attachments` is empty. The video 1920×1080 and photo
  1480×912 that the API returned with this record belong to the tweet he replied to, whose
  `attachments.media_keys` carry them; both still serve 200 because that tweet is still up.
  They are held at `watch/x/media/2066149533432807512_*` under his ID, which is our filing
  artefact and not his authorship — see `PROVENANCE.md`
- **Archived:** https://web.archive.org/web/20260614132330id_/https://twitter.com/qtecqot/status/2066149533432807512
- **Local copy:** `raw/2066149533432807512.json`
- **Live check:** `curl -s https://api.fxtwitter.com/qtecqot/status/2066149533432807512` → 404 (deleted)

```
@_halkyofu_ he is confirmed real. continuation of series on my Youtube.  There are others survivors
```

## 2026-06-14 13:32:03 UTC — DELETED

`2066151685723169249`  ·  https://x.com/qtecqot/status/2066151685723169249

- type: original
- conversation: `2066151685723169249`
- author at post time: 3 posts · 0 followers · 3 following · 3 likes given · 1 media
- media: photo 1920×1080 https://pbs.twimg.com/media/HKxx2aDa4AA1GT2.png **(404 — X purges media on delete)**
- link: https://t.co/dTNV7NZbnt → https://x.com/qtecqot/status/2066151685723169249/photo/1
- **Archived:** https://web.archive.org/web/20260614133203id_/https://twitter.com/qtecqot/status/2066151685723169249
- **Local copy:** `raw/2066151685723169249.json`
- **Live check:** `curl -s https://api.fxtwitter.com/qtecqot/status/2066151685723169249` → 404 (deleted)

```
Next drop imminent: rel. 6 /8.   the YT channel for official release. #skinnybob qtecqot https://t.co/dTNV7NZbnt
```

## 2026-06-15 04:53:33 UTC — DELETED

`2066383587763769681`  ·  https://x.com/qtecqot/status/2066383587763769681

- type: original
- conversation: `2066383587763769681`
- author at post time: 4 posts · 0 followers · 3 following · 3 likes given · 2 media
- link: https://t.co/wurTpAvirv → https://www.youtube.com/watch?v=OpSTlDJWFFI
- **Archived:** https://web.archive.org/web/20260615045333id_/https://twitter.com/qtecqot/status/2066383587763769681
- **Local copy:** `raw/2066383587763769681.json`
- **Live check:** `curl -s https://api.fxtwitter.com/qtecqot/status/2066383587763769681` → 404 (deleted)

```
Disclosure continuity release 5/8:
https://t.co/wurTpAvirv
```

## 2026-06-15 04:54:05 UTC — DELETED

`2066383721474019678`  ·  https://x.com/qtecqot/status/2066383721474019678

- type: original
- conversation: `2066383721474019678`
- author at post time: 5 posts · 0 followers · 3 following · 3 likes given · 3 media
- link: https://t.co/iDeW1aJzuj → https://www.youtube.com/watch?v=Oqw96jCOP7A
- **Archived:** https://web.archive.org/web/20260615045405id_/https://twitter.com/qtecqot/status/2066383721474019678
- **Local copy:** `raw/2066383721474019678.json`
- **Live check:** `curl -s https://api.fxtwitter.com/qtecqot/status/2066383721474019678` → 404 (deleted)

```
Disclosure continuity release 6/8:
https://t.co/iDeW1aJzuj
```

## 2026-07-28 07:18:28 UTC — LIVE

`2082002737362039094`  ·  https://x.com/qtecqot/status/2082002737362039094

- type: original
- conversation: `2082002737362039094`
- author at post time: 1 posts · 2 followers · 3 following · 8 likes given · 0 media
- **Archived:** https://web.archive.org/web/20260728071828id_/https://twitter.com/qtecqot/status/2082002737362039094
- **Local copy:** `raw/2082002737362039094.json`
- **Live check:** `curl -s https://api.fxtwitter.com/qtecqot/status/2082002737362039094` → 200 (still up)

```
🔹 I am not Ivan0135. I have not met him/her, but I have been in intermittent contact through electronic means as circumstances dictated. No contact since April of 2026.

🔹 I am of Eastern European descent, but fluent in English.

🔹 I am not suicidal. DMS in use, unlike 0135.
```

## 2026-07-29 08:18:46 UTC — LIVE

`2082380299598753907`  ·  https://x.com/qtecqot/status/2082380299598753907

- type: replied_to → 2082002737362039094  (@qtecqot)
- conversation: `2082002737362039094`
- author at post time: 2 posts · 12 followers · 3 following · 10 likes given · 0 media
- **Archived:** https://web.archive.org/web/20260729081846id_/https://twitter.com/qtecqot/status/2082380299598753907
- **Local copy:** `raw/2082380299598753907.json`
- **Live check:** `curl -s https://api.fxtwitter.com/qtecqot/status/2082380299598753907` → 200 (still up)

```
Clarification:  DMS = Deadman's Switch
```

## 2026-07-31 07:21:01 UTC — DELETED

`2083090538929193432`  ·  https://x.com/qtecqot/status/2083090538929193432

- type: retweeted → 2082824913815998748
- conversation: `2083090538929193432`
- author at post time: 3 posts · 66 followers · 3 following · 10 likes given · 0 media
- media: photo 586×1629 https://pbs.twimg.com/media/HOetq4JX0AADV9s.jpg **(404 — X purges media on delete)**
- **Archived:** https://web.archive.org/web/20260731072101id_/https://twitter.com/qtecqot/status/2083090538929193432
- **Local copy:** `raw/2083090538929193432.json`
- **Live check:** `curl -s https://api.fxtwitter.com/qtecqot/status/2083090538929193432` → 404 (deleted)

```
RT @AbbottEddi5270: SKINNY BOB FACTS:

Those who know who I am, know that I am one of the first Whistleblower to come out on hidden bases u…
```

## 2026-07-31 10:15:58 UTC — DELETED

`2083134567695925347`  ·  https://x.com/qtecqot/status/2083134567695925347

- type: original
- conversation: `2083134567695925347`
- author at post time: 3 posts · 67 followers · 4 following · 12 likes given · 1 media
- media: photo 1355×908 https://pbs.twimg.com/media/HOjHpt4awAANdX7.jpg **(404 — X purges media on delete)**
- media: photo 1370×812 https://pbs.twimg.com/media/HOjHpt_bcAAi7wr.jpg **(404 — X purges media on delete)**
- link: https://t.co/WIu7iHu2xJ → https://x.com/qtecqot/status/2083134567695925347/photo/1
- link: https://t.co/WIu7iHu2xJ → https://x.com/qtecqot/status/2083134567695925347/photo/1
- **Archived:** https://web.archive.org/web/20260731101558id_/https://twitter.com/qtecqot/status/2083134567695925347
- **Local copy:** `raw/2083134567695925347.json`
- **Live check:** `curl -s https://api.fxtwitter.com/qtecqot/status/2083134567695925347` → 404 (deleted)

```
https://t.co/WIu7iHu2xJ
```

## 2026-07-31 10:18:24 UTC — LIVE

`2083135181737914543`  ·  https://x.com/qtecqot/status/2083135181737914543

- type: original
- conversation: `2083135181737914543`
- author at post time: 3 posts · 67 followers · 4 following · 12 likes given · 1 media
- media: photo 1370×812 https://pbs.twimg.com/media/HOjIXX2bwAApC9-.jpg
- media: photo 1355×908 https://pbs.twimg.com/media/HOjIXX2aoAAqs6f.jpg
- link: https://t.co/V2NaDvLhnF → https://x.com/qtecqot/status/2083135181737914543/photo/1
- link: https://t.co/V2NaDvLhnF → https://x.com/qtecqot/status/2083135181737914543/photo/1
- **Archived:** https://web.archive.org/web/20260731101824id_/https://twitter.com/qtecqot/status/2083135181737914543
- **Local copy:** `raw/2083135181737914543.json`
- **Live check:** `curl -s https://api.fxtwitter.com/qtecqot/status/2083135181737914543` → 200 (still up)

```
https://t.co/V2NaDvLhnF
```

## 2026-07-31 22:33:22 UTC — LIVE

`2083320140276674766`  ·  https://x.com/qtecqot/status/2083320140276674766

- type: replied_to → 2083150753347039637  (@VOprograma)
- conversation: `2083135181737914543`
- author at post time: 4 posts · 76 followers · 4 following · 16 likes given · 1 media
- **Archived:** https://web.archive.org/web/20260731223322id_/https://twitter.com/qtecqot/status/2083320140276674766
- **Local copy:** `raw/2083320140276674766.json`
- **Live check:** `curl -s https://api.fxtwitter.com/qtecqot/status/2083320140276674766` → 200 (still up)

```
@VOprograma 👽 👍
```

## 2026-08-01 02:09:43 UTC — LIVE

`2083374588696863014`  ·  https://x.com/qtecqot/status/2083374588696863014

- type: retweeted → 2082824913815998748
- conversation: `2083374588696863014`
- author at post time: 5 posts · 79 followers · 4 following · 16 likes given · 1 media
- media: photo 586×1629 https://pbs.twimg.com/media/HOetq4JX0AADV9s.jpg
- **Archived:** https://web.archive.org/web/20260801020943id_/https://twitter.com/qtecqot/status/2083374588696863014
- **Local copy:** `raw/2083374588696863014.json`
- **Live check:** `curl -s https://api.fxtwitter.com/qtecqot/status/2083374588696863014` → 200 (still up)

```
RT @AbbottEddi5270: SKINNY BOB FACTS:

Those who know who I am, know that I am one of the first Whistleblower to come out on hidden bases u…
```

## 2026-08-01 03:37:11 UTC — LIVE

`2083396597241835761`  ·  https://x.com/qtecqot/status/2083396597241835761

- type: original
- conversation: `2083396597241835761`
- author at post time: 6 posts · 79 followers · 4 following · 16 likes given · 1 media
- **Archived:** https://web.archive.org/web/20260801033711id_/https://twitter.com/qtecqot/status/2083396597241835761
- **Local copy:** `raw/2083396597241835761.json`
- **Live check:** `curl -s https://api.fxtwitter.com/qtecqot/status/2083396597241835761` → 200 (still up)

```
🔹 The film recordings will never be monetized. Financial gain is not the objective. 

🔹 I have been given access to less than 2% of the network's cache of materials, with authorization to distribute. I have seen samples from the remainder. This is the "tame" stuff.
```

## 2026-08-01 03:45:49 UTC — LIVE

`2083398773242573299`  ·  https://x.com/qtecqot/status/2083398773242573299

- type: original
- conversation: `2083398773242573299`
- author at post time: 7 posts · 79 followers · 4 following · 16 likes given · 1 media
- **Archived:** https://web.archive.org/web/20260801034549id_/https://twitter.com/qtecqot/status/2083398773242573299
- **Local copy:** `raw/2083398773242573299.json`
- **Live check:** `curl -s https://api.fxtwitter.com/qtecqot/status/2083398773242573299` → 200 (still up)

```
🔹I will not disable my channel(s) voluntarily. Any censorship or blackout should be presumed as government/corporate intervention.

🔹Any "ads" associated with the YouTube posts were not at my direction. If anyone knows how to completely disable this feature, please advise me.
```

## 2026-08-02 03:24:49 UTC — LIVE

`2083755876188627359`  ·  https://x.com/qtecqot/status/2083755876188627359

- type: replied_to → 2083599624988713043  (@CytHyper)
- conversation: `2083398773242573299`
- author at post time: 8 posts · 95 followers · 4 following · 16 likes given · 1 media
- **Archived:** https://web.archive.org/web/20260802032449id_/https://twitter.com/qtecqot/status/2083755876188627359
- **Local copy:** `raw/2083755876188627359.json`
- **Live check:** `curl -s https://api.fxtwitter.com/qtecqot/status/2083755876188627359` → 200 (still up)

```
@CytHyper There is- an error in the tables on pages 3, 6 and 7.  Case 28 belongs to tape 5, not tape 4.
```
## 2026-08-02, ~09:00–11:00 UTC — DELETED (screenshot only)

`id unknown`  ·  posted and removed the same morning

- type: original, with a YouTube link card
- **Provenance:** browser screenshot taken by the investigator while the post was live,
  captioned "· 1h" by X at capture time. **This is the only surviving copy anywhere.**
- **Local copy:** `media/2026-08-02_deleted_fake-copycat-channel.png`
  (594×236, sha256 `6e977d3540668d896668c6941f77f4b8206c7c1486ac49acfe63f8ac2b23e8f4`)
- **Engagement at capture:** 1 reply · 0 reposts · 0 likes · 20 views
- **Not in:** the Wayback Machine, `api.fxtwitter.com`, or the xAI `x_search` index — checked
  2026-08-02 12:10 UTC, after deletion. The account's public post counter is back to 8.

```
◆ Fake copycat channel:

[link card] youtube.com
            qtecqot
            THERE TRYING TOO SILENCE ME
```

The card's target was **`https://www.youtube.com/@qtecqot2`** — an impostor channel using his
name, whose about-text is the card's second line. Checked 2026-08-02 12:12 UTC: `@qtecqot2`
returns **404**, has **no Wayback capture**, and does not appear in YouTube's channel or video
search. Handle variants `@qtecqot0/1/3/4/_/-`, `@qtecq0t`, `@qteqcot`, `@qtecgot`, `@qtecqut`,
`@realqtecqot`, `@qtecqotofficial`, `@qtecqotreal`, `@qtecqotarchive` all 404 as well; the only
live spelling is the real `@qtecqot` (`UCw1EA-KJud9OmMA5p7_MWgw`, 6.42K subs, 3 videos).

**Eyewitness detail, recorded because nothing else preserves it.** The investigator opened
`@qtecqot2` while it was live and reports it **displayed the same three videos as the real
channel**. That makes it a *clone*, not a squatted empty handle — someone had re-uploaded or
embedded his three releases under a near-identical name. Neither the channel nor its uploads
survive anywhere checked. This is a single unverified observation and is marked as such, but it
is the only account of what was on that page, and it changes what the deleted tweet was about:
not a name-squatter, a mirror of his own material.

It was removed within hours of the tweet, and the tweet within about one hour of posting.
Which of the two was removed first, and by whom, is not established. A YouTube copyright or
impersonation takedown, a voluntary deletion by whoever made it, and a platform termination all
produce the same 404.

**Bounds on the timestamp.** After `2083755876188627359` (2026-08-02 03:24:49 UTC, the last
surviving post) and before the 12:10 UTC check. The "1h" label is relative to a capture whose
exact clock time was not recorded, so the hour is approximate and the UTC offset is unresolved.

**Why this entry exists.** It is the second documented instance of this account publishing and
erasing inside a short window — the first being the three posts erased eleven minutes after
video 1 went public on 2026-05-25. Neither was caught by any archive. `watch/xwatch.py` was
written the same day to close that gap; from 2026-08-02 12:17 UTC onward the timeline is polled
every two minutes and every new status is captured with its media before it can be withdrawn.

## 2026-08-02 13:05:32 UTC — LIVE

`2083902015831511168`  ·  https://x.com/qtecqot/status/2083902015831511168

- type: replied_to → 2083884868514058699  (a reader who had posted a tape-and-case ledger)
- conversation: `2083599624988713043`
- author at post time: 102 followers · 4 following · 17 likes given
- **Local copy:** `raw/2083902015831511168.json` — captured live by `watch/xwatch.py`, not
  recovered. Nothing after 2026-08-02 12:17 UTC has had to be.
- **Live check:** 200, 11 views · 0 likes · 1 reply at capture

```
@CytHyper Your efforts are commendable and appreciated. The cases however are not limited to a specific run duration. They advance sequentially across 7 tapes, beginning at tape 01, case 01 and ending  at tape 07, case 40.

Of note is a minor indexing error in 2011.

Ty for your interest.
```

The most explicit statement of the numbering scheme he has made. Dossier §6.2 had derived a
7-tape scheme from the title cards; this confirms it and volunteers the bounds. "A minor
indexing error in 2011" is a claim about ivan0135's material, made in 2026, and it is testable
against the 2011 cards.

## 2026-08-02 13:12:34 UTC — LIVE

`2083903785219551469`  ·  https://x.com/qtecqot/status/2083903785219551469

- type: replied_to → 2083902015831511168 (his own, seven minutes earlier), still addressed
  `@`-first to the same reader — so it is a self-reply by threading and a reply by content
- conversation: `2083599624988713043`
- author at post time: 102 followers · 4 following · 17 likes given
- **Local copy:** `raw/2083903785219551469.json` — captured live
- **Live check:** 200, 7 views · 0 likes · 0 replies at capture

```
@CytHyper I can confirm that the next release will contain content from Tape 7 and will be in color.  

Some may find it slightly more disturbing than previous footage.
```

Slot 8 of the "N of 8" counter, described before release and therefore falsifiable. Two
caveats belong with it. Colour footage was already in circulation as a claim: the
2026-05-27 UAP post he replied to on 2026-06-14 attributes colour footage and a two-craft
clip to a named interviewee, so this is not the first time the assertion was made in public
where he could see it. And `reports/agent_colour_duplicate_count.md` holds the measurement to
run against a colour release the day it lands.
