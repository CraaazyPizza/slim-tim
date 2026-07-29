# Master timeline — every timestamped act by ivan0135 and qtecqot

Compiled 2026-07-29. **Every timestamp we have for anything either account has done in
public**, with its precision and its source, plus the local-clock analysis that follows
from it.

Two accounts are listed because the central question is whether they are the same person.
qtecqot's own tweet says they are not.

## Method and precision classes

| class | meaning |
|---|---|
| **second** | machine-readable to the second: YouTube `timestamp` in yt-dlp metadata, or the Atom `published` field in the channel RSS feed |
| **minute** | rendered by a UI that shows minutes only (the X post) |
| **day** | YouTube deliberately fuzzes comment times; "3 weeks ago" resolved against capture date |
| **month** | X's "Joined April 2026" — coarse to a 30-day window |

All times below are **UTC**. Local conversions are in §3. Sources: `videos/2011/*.info.json`,
`videos/2026/*.info.json` (yt-dlp, captured 2026-07-26), `watch/latest.json` (YouTube channel
RSS, captured 2026-07-29), `FINDINGS.md` §6e/§22/§32, `snapshots/2026-07-29_state.json`.

---

## 1. ivan0135 — the 2011 account

Channel `UCC5AjFfZHRvILhJfWw5UcDw`, handle `@ivan0135`.

| # | UTC timestamp | prec. | Act | Source |
|---|---|---|---|---|
| 1 | **2011-04-14 01:08:36** | second | **Channel created** | RSS `published` |
| 2 | **2011-04-14 02:04:26** | second | Upload `ZB788PtqQvg` — "Disclosure leaked ufo alien case video confidential documents old footage" · 48 s · 25 fps · **56 min after creating the channel** | yt-dlp |
| 3 | **2011-05-02 05:21:51** | second | Upload `RsQCXN4o4Ps` — "alien grey extraterrestrial zeta reticuli ufo leaked footage" · 60 s · 25 fps | yt-dlp |
| 4 | **2011-05-09 05:09:51** | second | Upload `Xju_CY5ZESA` — "Ivan0135 about ALIEN and UFO documents" (the text-only reply video) · 104 s · 25 fps · **exactly 7 days 0 h 12 min after #3** | yt-dlp |
| 5 | **2011-05-18 00:35:43** | second | Upload `a6TLGkrfNKI` — "…tape 06 - family vacation" · 94 s · 25 fps | yt-dlp |
| — | **2011-05-18 → present** | — | **Nothing. Fifteen years.** No fifth upload, no post, no reply, no comment. ~9,400 comments across the four videos, not one answered | multiple |

**Total public acts on record: five.** One channel creation and four uploads, spanning
34 days.

### Discrepancy to be aware of
Some secondary sources (and skinnybob.info's countdown script) date the first upload
**2011-04-13**. YouTube's own `upload_date` field is `20110414` and the UTC timestamp is
`2011-04-14T02:04:26Z`. The 04-13 figure is what you get rendering that instant in a US
timezone (21:04 EDT / 19:04 PDT on Apr 13) — which is itself a small piece of evidence,
see §3.

---

## 2. qtecqot — the 2026 account

YouTube channel `UCw1EA-KJud9OmMA5p7_MWgw`, X handle `@qtecqot`.

| # | UTC timestamp | prec. | Act | Source |
|---|---|---|---|---|
| 1 | **2026-04-22 05:27:55** | second | **YouTube channel created** — one day after the in-fiction trigger date 2026/04/21 | RSS `published` |
| 2 | **2026-04-28 05:24:54.916** | **millisecond** | **X account `@qtecqot` created** (`rest_id` 2048996761101078528). Upgraded 2026-07-29 from "April 2026" by direct read of x.com; confirmed independently by snowflake decoding of the ID itself, agreeing to 23.9 s. One username change, also April 2026. **Still predates the string's first public appearance (2026-05-25) by a month, so squatting is impossible** | x.com direct, §6e.1 |
| 3 | **2026-05-25 09:39:42** | second | Upload `OpSTlDJWFFI` — "Confidential leaked ufo-ebe footage continuation of disclosure" · 100 s · 30 fps · **no release marker in the description**. Implicitly 5/8: the comment written 2–4 days later says "5 of 8 completed" when this was the only qtecqot video, so ivan0135's four count as releases 1–4 (FINDINGS §1) | yt-dlp |
| 4 | **2026-06-15 04:23:35** | second | Upload `Oqw96jCOP7A` — "ET crew recovery site D, survival of EBL Tim +2, skinny Bob" · 84 s · 30 fps · **"Continuation release 6 / 8."** | yt-dlp |
| 5 | **2026-05-27 … 05-29** | 3-day window | **Two comments** on ivan0135's `RsQCXN4o4Ps` — the *only* time either account has ever spoken in a comment thread. One top-level ("Continuation of series : …" + link to *video 1*, 6 likes); one **nested reply** to @m21-b5q carrying the "ivan0135 status is currently not known… 5 of 8 completed" statement (1 like). The nested one is invisible when sorting by newest. **Corrected 2026-07-29 from "~06-27" — the old figure was an artifact.** yt-dlp derives `timestamp` by subtracting YouTube's *rounded-down* relative string from the scrape epoch, so a single capture is unbounded above. Two captures bracket it: `"1 month ago"` at epoch 07-26 20:11 → true ∈ (05-26, 06-26]; `"2 months ago"` at epoch 07-29 02:30 → true ∈ (04-29, 05-29]. **Intersection (05-26, 05-29].** Reply must postdate its parent (@m21-b5q's plea, same window), so both sit **2–4 days after video 1 went up on 05-25** — he answered the plea almost immediately, and his own text names 2026/05/25 as the trigger | two yt-dlp captures, intersected |
| 6 | **2026-07-24 09:14:05** | second | Upload `l9RAhmPHM_A` — "interior walkthru and examination 8mm disclosure footage ufo" · 147 s · 30 fps · **"Continuation release 7 / 8."** — so exactly **one release remains**. ⚠ **Markers corrected 2026-07-29**: rows 3/4 previously assigned "6/8" and "7/8" to videos 1 and 2, shifted one video early, which silently contradicted FINDINGS §1. Verified against the `description` field of each `videos/2026/*.info.json` | yt-dlp |
| 7 | **2026-07-28 07:07:01** | second | **Description edit** on `l9RAhmPHM_A`, adding the "Official venue for dissemination…" block naming `x.com/qtecqot`. Corroborated by content diff against our 2026-07-26 capture, not by the timestamp alone | RSS `updated` + §32 |
| 8 | **2026-07-28 07:18:28.000** | **second** | **First tweet ever**, status ID `2082002737362039094` — the three-point statement ("I am not Ivan0135… of Eastern European descent… not suicidal. DMS in use"). **11 minutes after #7.** Cannot be scheduled through the normal X interface, so it is the first non-stageable timestamp we have. 5 likes, `conversation_count` 5, **never edited**. Confirmed by **three** independent routes: direct x.com read, and the public syndication endpoint `cdn.syndication.twimg.com/tweet-result?id=<ID>&lang=en&token=<T>` — which requires a computed token, JS `((id/1e15)*Math.PI).toString(36)` with the "." stripped (for this ID, `51osymyjowsl8krlqe61or`); without the token it returns `{}` | X + syndication, §6e.1, §32 |

| 9 | **2026-07-29 ~10:18 local** | minute, **timezone-unresolved** | **Second tweet ever** — a standalone reply to his own thread: "Clarification: DMS = Deadman's Switch". **8 views.** Confirms the reading FINDINGS §32 already committed to against a replier who read DMS as *direct messages*. Posted as a new tweet, **not** as a reply to the person who misread it — same engagement signature as YouTube: reads everything, answers almost nothing, never in-thread. ⚠ **The timestamp is a screenshot of X's UI rendered in *the owner's* local zone, not a machine read.** If that device is on CEST, 10:18 CEST = 08:18 UTC, which sits inside the established 06:23–11:39 CEST band and makes it **eight-for-eight**. Not yet verified — see the owner-only action below | X UI paste, unverified |

**Total public acts on record: nine**, spanning ~14 weeks and still running.

**owner-only action to close row 9 to the millisecond.** `cdn.syndication.twimg.com/tweet-result?id=<ID>&lang=en` was verified reachable and returned HTTP 200 with an exact `created_at` on 2026-07-29 (test ID `2058162476307407123` → `2026-05-23T12:25:47.000Z`, matching a snowflake decode of the same ID to sub-second). It needs only the numeric status ID. `x.com/qtecqot` itself is **not** a dependable channel — on 2026-07-29 it served a JS shell with no state blob, unlike the earlier read that produced §6e.1. So: click the clarification tweet and paste its `status/<digits>` URL, and the exact UTC instant follows without a login. Do **not** treat the current absence of a machine read as an absence of data.

### The 11-minute sequence of 2026-07-28
`07:07:01` the video description is edited to point at the X account → `07:18` that X
account, dormant since April, posts for the first time. The account was prepared months
before it was used, and then pointed at and activated within a quarter of an hour.

---

## 3. Local-clock analysis — the actual answer to "what are the activity patterns"

Same UTC instants, rendered in each candidate zone. **2011 Moscow was UTC+4** (Russia held
permanent summer time from March 2011); 2026 Moscow is UTC+3.

### ivan0135, 2011 — five events

| UTC | CEST (+2) | Moscow (+4) | US Eastern (−4) | US Pacific (−7) |
|---|---|---|---|---|
| 04-14 01:08 | 03:08 | 05:08 | Apr 13 **21:08** | Apr 13 **18:08** |
| 04-14 02:04 | 04:04 | 06:04 | Apr 13 **22:04** | Apr 13 **19:04** |
| 05-02 05:21 | 07:21 | 09:21 | 01:21 | May 1 **22:21** |
| 05-09 05:09 | 07:09 | 09:09 | 01:09 | May 8 **22:09** |
| 05-18 00:35 | 02:35 | 04:35 | May 17 **20:35** | May 17 **17:35** |
| **span** | 02:35–07:21 | 04:35–09:21 | 20:35–01:21 | **17:35–22:21** |

**US Pacific is the tightest fit by a distance: every one of the five acts falls between
17:35 and 22:21 — an ordinary evening.** US Eastern is a plausible second (evening running
into the small hours). Moscow gives an early-morning band. CEST puts two of five in the
middle of the night.

This is the single most under-weighted fact about ivan0135: **the upload clock does not
support the Russian self-presentation.** Set beside the KGB emblem, the name "Ivan", the
Soviet-anniversary date theory, and FatPhil's independent observation that the English
reads non-native, the most economical reading is a *constructed* Russian presentation
operated from the Americas — most likely the US west coast.

Caveat that must travel with this: five events is a small sample, and YouTube has offered
scheduled publishing for much of this period. But a scheduling operator building a Russian
cover would stage Russian-friendly hours, and didn't.

### qtecqot, 2026 — seven second-or-better-precision events

| UTC | CEST (+2) | Moscow (+3) | US Eastern (−4) | US Pacific (−7) |
|---|---|---|---|---|
| 04-22 05:27 | **07:27** | 08:27 | 01:27 | Apr 21 22:27 |
| 04-28 05:24 | **07:24** | 08:24 | 01:24 | Apr 27 22:24 |
| 05-25 09:39 | **11:39** | 12:39 | 05:39 | 02:39 |
| 06-15 04:23 | **06:23** | 07:23 | 00:23 | Jun 14 21:23 |
| 07-24 09:14 | **11:14** | 12:14 | 05:14 | 02:14 |
| 07-28 07:07 | **09:07** | 10:07 | 03:07 | 00:07 |
| 07-28 07:18 | **09:18** | 10:18 | 03:18 | 00:18 |
| **span** | **06:23–11:39** | 07:23–12:39 | 00:23–05:39 | 21:23–02:39 |

**And the two account registrations sit 181 seconds apart in time-of-day**, six days
apart: YouTube 05:27:55 UTC (07:27:55 CEST) on Apr 22, X 05:24:54 UTC (07:24:54 CEST) on
Apr 28. Two platforms, two sittings, the same ~07:25 morning slot. See §6e.1.

**CEST is the clean fit: a seven-for-seven morning band, 06:23–11:39, median ~09:10.** Moscow
works nearly as well. US Eastern puts everything in the small hours; US Pacific scatters
across evening and after-midnight.

The 07:18 tweet matters disproportionately here because **X does not let you schedule a
post through the normal interface** — it is the one timestamp in the entire corpus that
cannot be staged, and it lands inside the established morning band.

### The comparison

| | ivan0135 (2011) | qtecqot (2026) |
|---|---|---|
| best-fit zone | **US Pacific evening** (17:35–22:21) | **CEST morning** (06:23–11:39) |
| second-best | US Eastern evening | Moscow morning |
| worst fit | CEST (night) | US Eastern (small hours) |
| day-of-week | favours Monday (3 of 5) | favours Monday (2 of 3 uploads) |
| cadence | disciplined — two uploads exactly 7 d 0 h 12 m apart | 21 d then 39 d between uploads |
| responsiveness | **zero** in 15 years | replies to comments, edits descriptions, tweets |

**The two clocks do not overlap and the two behaviours are opposite.** ivan0135 posted in
what looks like a US evening and never spoke again; qtecqot posts in a Central European
morning and answers people. On clock evidence alone these are different operators, or one
operator who relocated across eight time zones and changed personality.

That is *consistent with qtecqot's own claim* — the tweet says "I am not Ivan0135" — and it
is the strongest independent support that claim has. It also converges with two unrelated
physical measurements pointing at the same European band: the 50 Hz mains hum in the audio,
and the CEST morning upload slot itself.

---

## 4. Tested and REFUTED — the "ivan0135 was active in 2026" hypothesis

**Do not re-chase this.** The channel RSS feed reports an Atom `updated` value for each of
ivan0135's four videos, and all four sit in **2026**:

| video | published | `updated` |
|---|---|---|
| RsQCXN4o4Ps | 2011-05-02 | 2026-04-14 20:35:03 |
| ZB788PtqQvg | 2011-04-14 | 2026-04-22 19:44:52 |
| a6TLGkrfNKI | 2011-05-18 | 2026-05-05 00:14:23 |
| Xju_CY5ZESA | 2011-05-09 | 2026-05-29 23:12:54 |

This looks explosive — one of them lands on the same calendar day the qtecqot channel was
created, another on the 15th anniversary of ivan0135's own channel creation. Two
calibrations initially seemed to support reading them as real edits: `updated` does **not**
move with view counts (views changed on 6 of 7 tracked videos while every `updated` held
fixed), and on qtecqot's video 3 the `updated` value matches a **content-verified**
description edit to the second.

**It is nonetheless an artifact.** Matched control: 5,387 channel IDs were harvested from
the commenters on ivan0135's own videos, 60 sampled, and every video they had published in
2015 or earlier was checked. **51 of 51 old videos on ordinary, unrelated accounts also
report `updated` in 2026 — clustered in the same April–May window** (e.g. a 2011-07-05
upload showing `2026-05-05`, a 2011-06-01 upload showing `2026-05-28`). YouTube re-touched
its old catalogue during that period. ivan0135's four videos are statistically unremarkable
inside that population.

**Conclusion: ivan0135 shows no 2026 activity. The "frozen since 2011" record stands.**

Consequence for the watcher: `watch/watch.py` flags `updated` changes as "METADATA EDITED",
which will produce **false positives on old videos** during platform-wide sweeps. A flag on
an ivan0135 video is only meaningful if a content diff confirms it. On qtecqot's recent
videos the flag is more trustworthy but still needs the content check — which is exactly how
§32 was established.

Also downgraded by this finding: qtecqot's videos 1 and 2 both carry `updated` values of
2026-07-26 (11:31:44 and 01:53:26). Those are **not** independently corroborated by any
content diff, so they should not be recorded as edits.

---

## 5. What is NOT in this timeline

- **Comment timestamps beyond a 3-day window.** YouTube serves only a rounded-down relative
  string, so a single capture has no upper bound. ~~qtecqot's two comments are pinned only
  to ~2026-06-27.~~ **RESOLVED 2026-07-29 — see row 5.** Intersecting two captures taken
  three days apart brackets them to **2026-05-27 … 05-29**. The "~06-27" figure was an
  artifact of the single-capture method, wrong by a month, and is withdrawn. Day precision
  *within* that window is still not available.
- ~~**The exact X join date.** "April 2026" is all the profile gives.~~ **RESOLVED — see
  row 2.** `2026-04-28T05:24:54.916Z`, to the millisecond, by three independent routes:
  direct x.com read, snowflake decode of the account `rest_id` (agreeing to 23.9 s), and
  the public syndication endpoint. It still brackets the YouTube channel creation of
  2026-04-22 — six days later, and 181 seconds apart in time-of-day.
- **The X username change** — one is recorded, "last in April 2026", but neither the prior
  handle nor the exact date is available to us.
- **Any private or off-platform activity** — the Chris Ramsay email thread, the Instagram
  DM, and anything under another identity. The Ramsay email is dated only to ~Sep 2025 and
  has never been tied to qtecqot.
- **Deleted acts.** We can only see what is still up. `comments.md` (the owner's browser capture
  of 2026-07-26 ~20:00) is the only record we hold that would show a deletion.
- **Release 8/8**, which has not happened. §22's prediction: most likely a Monday around
  09:00–10:00 UTC. A drop far outside that slot — especially in US daytime — is itself
  informative.

---

## 6. Maintenance

`watch/watch.py` polls all three channel feeds every 30 minutes via system cron and appends
any change to `watch/CHANGELOG.md`. New uploads, title changes, `updated` bumps, view/like
deltas and disappearing videos all get logged. **Append new events to this file from that
changelog**, and record the precision class and source for each, as above.
