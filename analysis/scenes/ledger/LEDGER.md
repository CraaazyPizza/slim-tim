# Cross-era catalog ledger — 2011 ivan0135 vs 2026 qtecqot

Machine-readable version: `ledger.csv`. Working scripts: `extract_glyphs.py`, `tc_windows.py`,
`strip.py`, `decode.py`. Crops/sheets: `crops/`, `sheets/`. 2011 frames decoded from the mkvs
into `frames2011/` (7,623 PNG, 25 fps native).

## A. Where each era's catalog actually lives

| Video | Era | Catalog source | Burned-in overlay? |
|---|---|---|---|
| `ZB788PtqQvg` | 2011 | YouTube **description** only. On screen: KGB emblem card, no fragment list | yes, 8 fragments |
| `RsQCXN4o4Ps` | 2011 | **On-screen card only** (description is empty) | yes, 3 fragments |
| `Xju_CY5ZESA` | 2011 | none | **no** — static handprint plate + text cards |
| `a6TLGkrfNKI` | 2011 | card `Tape 06 / Family vacation` + lore captions | **no** — swept whole video at high stretch |
| `OpSTlDJWFFI` | 2026 | on-screen card **and** description | yes, 5 fragments |
| `Oqw96jCOP7A` | 2026 | on-screen card **and** description | yes, 8 fragments |
| `l9RAhmPHM_A` | 2026 | on-screen card **and** description | yes, 2 sampled ranges |

### `RsQCXN4o4Ps` on-screen card, read at full resolution (mean of f520–589)

```
Tape 05 edited fragments:
Case 25/skinny Bob 00:08:42 - 00:08:50
Case 25/skinny Bob 00:27:36 - 00:27:45
Case 26/How to drive 00:55:07 - 00:55:12
```

Crops: `crops/RsQ_card_lines.png`, `RsQ_l2.png`, `RsQ_l3.png`, `RsQ_l4.png`, `RsQ_l6.png`,
`RsQcard_L6b.png`.

The 2026 cards use the identical header string `Tape NN edited fragments:` — not the
`Tape NN:` form used in ZB's description and in the 2026 *descriptions*.
Crops: `crops/card_OpSTlDJWFFI_700.png`, `card_Oqw96jCOP7A_400.png`, `card_l9RAhmPHM_A_400.png`.

RsQ's preceding card reads `The video contains a sample edited fragments of video tape 05.` —
the 2026 cards read `The video contains sample edited fragments of video tapes NN, NN.`
(the ungrammatical `a` removed).

## B. Merged timeline, both eras

```
--- Tape 01 ---
  2011  C07  Tin bird               00:08:41 - 00:08:47  (   7s)
--- Tape 02 ---
  2026  C11  Tin bird unauth        00:33:30 - 00:33:34  (   5s)
  2026  C11  Tin bird primer        00:36:02 - 00:36:07  (   6s)   gap same-era: 2:28
  2026  C12  Mk.4 taxi              01:08:21 - 01:08:22  (   2s)   gap same-era: 32:14
  2026  C12  Mk.4 pace lap          01:10:55 - 01:11:21  (  27s)   gap same-era: 2:33
--- Tape 03 ---
  2011  C15  Flying twin            00:27:11 - 00:27:13  (   3s)
  2011  C15  Flying twin            00:27:34 - 00:27:39  (   6s)   gap same-era: 0:21
  2026  C18  Mk.4 early boarding    02:13:18 ~ 02:23:57  ( 640s)   gap CROSS-ERA: 105:39
--- Tape 04 ---
  2026  C20  Brown boys             00:03:11 - 00:03:18  (   8s)
  2026  C20  Brown boys             00:03:55 - 00:04:05  (  11s)   gap same-era: 0:37
  2026  C20  Brown boys             00:04:10 - 00:04:11  (   2s)   gap same-era: 0:05
  2026  C21  Triage                 00:15:01 - 00:15:06  (   6s)   gap same-era: 10:50
  2026  C22  Exit EBL04             00:30:26 - 00:31:14  (  49s)   gap same-era: 15:20
  2011  C23  Blue boys              00:42:50 - 00:42:51  (   2s)   gap CROSS-ERA: 11:36
  2011  C24  Blue boys meeting      00:47:30 - 00:47:32  (   3s)   gap same-era: 4:39
  2011  C23  Blue boys              00:48:09 - 00:48:16  (   8s)   gap same-era: 0:37   <-- C23/C24 interleave
  2011  C24  Blue boys meeting      00:56:12 - 00:56:14  (   3s)   gap same-era: 7:56
  2011  C24  Blue boys meeting      00:58:26 - 00:58:28  (   3s)   gap same-era: 2:12
--- Tape 05 ---
  2026  C25  Bob's walkabout        00:02:07 - 00:02:12  (   6s)
  2011  C25  skinny Bob             00:08:42 - 00:08:50  (   9s)   gap CROSS-ERA: 6:30
  2011  C25  skinny Bob             00:27:36 - 00:27:45  (  10s)   gap same-era: 18:46
  2026  C25  Slim Tim               00:40:12 - 00:40:40  (  29s)   gap CROSS-ERA: 12:27
  2011  C26  How to drive           00:55:07 - 00:55:12  (   6s)   gap CROSS-ERA: 14:27
  2026  C26  Tim's show &tell       01:01:18 - 01:01:19  (   2s)   gap CROSS-ERA: 6:06  <-- closest approach
  2026  C28  False Cape study       02:51:01 ~ 02:51:32  (  32s)   gap same-era: 109:42
--- Tape 06 ---
  2026  C31  Mk.5 virgin (col/s)    00:57:56 - 00:58:04  (   9s)
  (2011 a6TLGkrfNKI is titled 'Tape 06 / Family vacation' but carries no timecode at all)
--- Tape 07 ---
  (never shown by either era)
```

## C. Key aggregates

- 2011 claimed source time: **60 s** across 11 fragments, 4 tapes.
- 2026 claimed source time: **834 s** of span (≈262 s actually present after the `~` sampling).
- 2011 timecode extent: **00:08:41 – 00:58:28** — never beyond 32.5 % of a 180-min tape.
- 2026 timecode extent: **00:02:07 – 02:51:32** — reaches 95.3 % of a 180-min tape.
- Cross-era timecode overlaps: **zero**. Closest approach 6 min 06 s (Tape 05, Case 26).
- Expected collisions if 2026's 13 fragments were placed **uniformly at random** on their
  tapes: **0.096** ⇒ P(no collision) ≈ **91 %**. Non-collision is therefore uninformative.

## D. Endpoint-exactness audit (new, and it changes an earlier FINDINGS conclusion)

2011 endpoints hit/missed (22 endpoints, 11 fragments):

| miss | fragment | claimed | observed |
|---|---|---|---|
| end −1 s | ZB C15 | …00:27:39 | last 00:27:38 (f636) |
| end −1 s | ZB C24 | …00:56:14 | last 00:56:13 (f1122) |
| end −1 s | ZB C24 | …00:58:28 | last 00:58:27 (f1188 = final frame) |
| start +1 s | RsQ C25 | 00:08:42… | first 00:08:43 (f607) |
| start +1 s, end −1 s | RsQ C25 | 00:27:36–45 | 00:27:37 (f969) – 00:27:44 (f1295) |
| start +1 s | RsQ C26 | 00:55:07… | first 00:55:08 (f1297) |
| indeterminate | ZB C15 | …00:27:13 | :13 falls in flare-washed f446–450 |

⇒ **6 hard misses + 1 indeterminate out of 22 endpoints (27 %)** in 2011.
2026 v1 has 1 miss / 10, v2 has 5 misses / 16 (31 %). Comparable.
FINDINGS §11.6's "first catalog mismatch found anywhere" (v1 Mk.4 pace lap ending 1 s short)
is **not** an anomaly — it is the house convention, present in both eras.
