# Agent report (verbatim): cross-era catalog ledger + overlap hunt

Completed 2026-07-26. Final message verbatim:

---

## LEDGER — every burned-in identifier, both eras

Artifacts: `/home/user/new-skinny-bob/analysis/scenes/ledger/` (`LEDGER.md`, `ledger.csv`, scripts `extract_glyphs.py` / `tc_windows.py` / `strip.py` / `decode.py`, 39 sheets in `sheets/`, 46 crops in `crops/`, 2011 frames decoded to `frames2011/`).

### Where each era's catalog lives (this was not previously established)

| Video | Catalog source | Burned-in overlay |
|---|---|---|
| `ZB788PtqQvg` 2011 | **description only** (on screen: KGB emblem card, no fragment list) | 8 fragments |
| `RsQCXN4o4Ps` 2011 | **on-screen card only — its description is empty** | 3 fragments |
| `Xju_CY5ZESA` 2011 | none | **none** (static handprint plate + text cards) |
| `a6TLGkrfNKI` 2011 | card `Tape 06 / Family vacation` + lore captions | **none anywhere** (full-frame and bottom-band sweep at high stretch: `sheets/a6TL_all.png`, `sheets/a6_bottomband.png`, `crops/a6full_1790.png`) |
| all three 2026 | on-screen card **and** description | 5 / 8 / 2 |

**`RsQCXN4o4Ps` carries a catalog card in exactly the 2026 format.** Read at full res from the mean of f520–589 (`crops/RsQ_card_lines.png`, `RsQ_l2/3/4/6.png`, `RsQcard_L6b.png`):

```
Tape 05 edited fragments:
Case 25/skinny Bob 00:08:42 - 00:08:50
Case 25/skinny Bob 00:27:36 - 00:27:45
Case 26/How to drive 00:55:07 - 00:55:12
```

The 2026 cards use the identical header string `Tape NN edited fragments:` — **not** the `Tape NN:` form used in ZB's description and in the 2026 *descriptions* themselves (`crops/card_OpSTlDJWFFI_700.png`, `card_Oqw96jCOP7A_400.png`, `card_l9RAhmPHM_A_400.png`). So the 2026 on-screen card is templated on RsQ's card, not on the descriptions. Note the accompanying line: RsQ says `The video contains a sample edited fragments of video tape 05.`; 2026 says `…contains sample edited fragments of video tapes NN, NN.` — the same copyist-corrects-source pattern FINDINGS §15.2 found in the descriptions, now confirmed on screen too.

### Merged timeline (2011 rows are new; 2026 rows pulled from FINDINGS §4/§8/§11)

```
Tape 01   2011  C07  Tin bird              00:08:41 - 00:08:47    7s
Tape 02   2026  C11  Tin bird unauth       00:33:30 - 00:33:34    5s
          2026  C11  Tin bird primer       00:36:02 - 00:36:07    6s
          2026  C12  Mk.4 taxi             01:08:21 - 01:08:22    2s
          2026  C12  Mk.4 pace lap         01:10:55 - 01:11:21   27s
Tape 03   2011  C15  Flying twin           00:27:11 - 00:27:13    3s
          2011  C15  Flying twin           00:27:34 - 00:27:39    6s
          2026  C18  Mk.4 early boarding   02:13:18 ~ 02:23:57  640s span   [CROSS-ERA gap 105:39]
Tape 04   2026  C20  Brown boys            00:03:11 - 00:03:18    8s
          2026  C20  Brown boys            00:03:55 - 00:04:05   11s
          2026  C20  Brown boys            00:04:10 - 00:04:11    2s
          2026  C21  Triage                00:15:01 - 00:15:06    6s
          2026  C22  Exit EBL04            00:30:26 - 00:31:14   49s
          2011  C23  Blue boys             00:42:50 - 00:42:51    2s        [CROSS-ERA gap 11:36]
          2011  C24  Blue boys meeting     00:47:30 - 00:47:32    3s
          2011  C23  Blue boys             00:48:09 - 00:48:16    8s        <-- C23/C24 INTERLEAVE
          2011  C24  Blue boys meeting     00:56:12 - 00:56:14    3s
          2011  C24  Blue boys meeting     00:58:26 - 00:58:28    3s
Tape 05   2026  C25  Bob's walkabout       00:02:07 - 00:02:12    6s
          2011  C25  skinny Bob            00:08:42 - 00:08:50    9s        [CROSS-ERA gap 6:30]
          2011  C25  skinny Bob            00:27:36 - 00:27:45   10s
          2026  C25  Slim Tim              00:40:12 - 00:40:40   29s        [CROSS-ERA gap 12:27]
          2011  C26  How to drive          00:55:07 - 00:55:12    6s        [CROSS-ERA gap 14:27]
          2026  C26  Tim's show &tell      01:01:18 - 01:01:19    2s        [CROSS-ERA gap 6:06 = closest]
          2026  C28  False Cape study      02:51:01 ~ 02:51:32   32s span
Tape 06   2026  C31  Mk.5 virgin (col/s)   00:57:56 - 00:58:04    9s   (a6TL is "Tape 06" but untimed)
Tape 07   never shown by either era
```

**2011 observed-vs-claimed, frame-exact** (my measurements; frames are 25 fps native):

| Fragment | Claimed | Observed | Frames |
|---|---|---|---|
| ZB C07 Tin bird | 08:41–08:47 | 08:41 … 08:47 ✓✓ | f134–f408 |
| ZB C15 Flying twin | 27:11–27:13 | 27:11 … 27:12, :13 indeterminate | f410–f450 |
| ZB C15 Flying twin | 27:34–27:39 | 27:34 … **27:38** | f452–f636, cut f648 |
| ZB C23 Blue boys | 42:50–42:51 | ✓✓ | f652–f699 |
| ZB C23 Blue boys | 48:09–48:16 | ✓✓ | f708–f972 |
| ZB C24 Blue boys mtg | 47:30–47:32 | ✓✓ | f984–f1080 |
| ZB C24 Blue boys mtg | 56:12–56:14 | 56:12 … **56:13** | f1081–f1125 |
| ZB C24 Blue boys mtg | 58:26–58:28 | 58:26 … **58:27** | f1130–f1188 (last frame) |
| RsQ C25 skinny Bob | 08:42–08:50 | **08:43** … 08:50 | f607–f957 |
| RsQ C25 skinny Bob | 27:36–27:45 | **08:27:37** … **27:44** | f969–f1295 |
| RsQ C26 How to drive | 55:07–55:12 | **55:08** … 55:12 | f1297–f1487 |

Evidence sheets: `sheets/tcwin_ZB788PtqQvg_0[0-4].png`, `tcwin_RsQCXN4o4Ps_0[0-2].png`, and the frame-exact strips `strip_zb_start08 / zb_2711 / zb_2713 / zb_2739 / zb_4809 / zb_4815 / zb_5614 / zb_5828 / rsq_start1 / rsq_start2 / rsq_0842 / rsq_0850 / rsq_2745 / rsq_5512.png`.

---

## (a) Overlaps and near-adjacency — verdict

**There is not a single timecode overlap anywhere.** Confidence: **high** (every 2011 second is now individually read).

There is one real *collision of identifiers*: **Tape 05, Cases 25 and 26 appear in both eras.** 2011's assignment comes from RsQ's on-screen card; 2026 re-uses both case numbers on the same tape at different times. Closest approach: 2011 C26 ends 00:55:12, 2026 C26 starts 01:01:18 — **6 min 06 s**.

**Content comparison at the collision (sheets `tape05_compare.png`, `bob_morphology.png`, `case26_compare.png`):**

- *Case 26.* 2011 `How to drive` (00:55:07–12) is a heavily over-exposed interior dominated by a large circular rim/disc edge with a small dark object at upper right. 2026 `Tim's show &tell` (01:01:18–19) is a bright interior with a dark angular chevron-shaped artifact held up by a hand, a being's silhouette bottom-right. **No geometric contradiction** (both bright interiors, 6 min apart) but also **no positive match** — no shared wall, fixture, prop or lighting geometry is identifiable. Verdict: **compatible, non-corroborating.** Confidence moderate; the 2011 shot is so blown out it carries little information either way.
- *Case 25.* 2011 `skinny Bob` (both fragments) shows one individual with three diagnostic features: a pronounced **lateral cranial flare / temporal "wings"**, a **step at the brow**, and **mottled/wrinkled cranial skin**. 2026's two Case-25 subjects — `Bob's walkabout` (00:02:07, outdoors in rubble) and `Slim Tim` (00:40:12, indoors) — both have **smooth ovoid crania with none of those three features**. Same genus, different individuals.
  - This is *not* a contradiction on its face: 2026 v2's own title says "survival of EBL Tim **+2**", i.e. it asserts multiple individuals.
  - It *is* notable that the fragment 2026 named `Bob's walkabout` does not show Bob's morphology. But at 00:02:08 the figure's head spans ~60–80 px, well inside the "unresolvable in principle" regime FINDINGS §9.6 established. **I cannot call this a contradiction.** Confidence: low-to-moderate that it means anything.
- *Cross-tape content consistency that does hold.* 2011 C07 `Tin bird` (Tape 01) is a distant domed-lenticular disc over a treeline; 2026 C11 `Tin bird unauth/primer` (Tape 02) is the **same craft profile** photographed close — domed top, flat underside with a lip (`sheets/tinbird_compare.png`). Genuine same-world continuity at object level. Caveat: that silhouette is plainly visible in the published 2011 video and therefore copyable (and FINDINGS §11.7 already found a "tin bird" ghost behind 2026 v1's title card).

**Net on (a): the two eras never contradict each other, and never corroborate each other either.** No shared set, prop, being or geometry can be matched across the era boundary. Confidence: high on "no contradiction", high on "no positive corroboration".

---

## (b) Avoidance, quantified — verdict: **the avoidance is meaningless, and I can show it**

- 2011 burned in **60 source-seconds total** across 11 fragments and 4 tapes.
- Against a fictional catalog of 7 × 180 min = 75,600 s, that is **0.079 %** of the timeline.
- Expected number of cross-era collisions if the 2026 author had placed all 13 fragments **uniformly at random** on their claimed tapes: **0.096**. P(no collision) ≈ **91 %**.

So "2026 systematically avoids every timecode 2011 showed" is a **null result**: a blind author avoids it nine times out of ten. Anyone offering the disjointness as evidence of care, or of insider knowledge, is over-reading. Confidence: high (this is arithmetic on measured quantities).

What *is* substantive in (b):

1. **The two eras occupy different depths of the tape.** Every 2011 timecode lies in **00:08:41 – 00:58:28** — 2011 never goes past **32.5 %** of a 180-min tape. 2026 ranges **00:02:07 – 02:51:32**, reaching **95.3 %**. 2026 also introduces the only material past the one-hour mark on any tape.
2. **2026 shows 4.4× as much source time** (834 s of span / ≈262 s present vs 60 s).
3. **Coverage of the fictional catalog:** 2011 touched cases {07, 15, 23, 24, 25, 26} on tapes {01, 03, 04, 05} plus an untimed tape 06. 2026 touched {11, 12, 18, 20, 21, 22, 25, 26, 28, 31} on tapes {02, 03, 04, 05, 06}. **2026 avoids Tape 01 entirely, and re-uses exactly the two cases (25, 26) that 2011 printed on an on-screen card.** Both are Tape 05, the tape of the single most-viewed 2011 video — the same video qtecqot commented on.
4. **Tape 07 has never been shown by either era**, and Tape 01 only by 2011. If release 8/8 is a finale, tape 07 (and/or tape 01) is the obvious remaining material — a cheap, falsifiable prediction.

---

## (c) Internal consistency of the shared lore

**Holds (2026 extends 2011 correctly):**

1. **Case-number ↔ tape mapping is a strictly monotone block partition, and 2026 never violates it.**
   T01→07 · T02→11,12 · T03→15,18 · T04→20,21,22,23,24 · T05→25,26,28 · T06→31.
   2026 had to place 18 above 2011's 15 and below 2011's 20-block, place 20–22 below 2011's 23, place 28 above 26, place 31 above 28 — all satisfied. Confidence: high that the constraint is honoured; moderate that honouring it is hard (a careful reader of ZB's description would get it right).
2. **Within-tape ascending order:** all cross-era sequences ascend (T05: all C25 < all C26 < C28). The *only* violation in the whole merged catalog is **2011-internal**: on Tape 04, C23's second fragment (00:48:09) comes after C24's first (00:47:30), so cases 23 and 24 interleave in tape time. 2026 introduces no violation — it is in fact **strictly rank-ordered, i.e. tidier than 2011**.
3. **Tape budget:** max timecode anywhere is 02:51:32, inside the boilerplate "Tape duration: 180 min". "Total recorded duration: 1.260 min" = 7 × 180. Both eras copy this boilerplate verbatim, European decimal point intact.
4. **Fragment ordering within a video** (group by tape, then case, then time) is identical in all six catalogued videos.
5. **Redaction-bar geometry matches.** The 2011 bar occupies x ≈ 305–516 (~205 px ≈ 4.7 chars at the 2011 pitch of 44.0 px). 2026's one exposed prefix `T6-02` occupies x ≈ 314–508 (~194 px ≈ 4.6 chars at the 2026 pitch of 42.3 px). Same raster footprint, both terminating just before the `/`. **Consistent with the same ~5-character `T<tape>-NN` prefix hidden in both eras** — though the bars are feathered (46 px in 2026 per FINDINGS §8.2) so this is ±0.5 char, and the position is copyable from the published files. Sheet: `sheets/bars_compare.png`. Confidence: moderate.

**Breaks (2026 violates 2011's own rule):**

6. **The naming rule.** In 2011 a case number has exactly **one** name, repeated verbatim across all its fragments — 4 of 4 multi-fragment cases obey (C15 ×2, C23 ×2, C24 ×3, C25 ×2). In 2026 **3 of 4** multi-fragment cases break it: C11 = `Tin bird unauth` **and** `Tin bird primer`; C12 = `Mk.4 taxi` **and** `Mk.4 pace lap`; C25 = `Bob's walkabout` **and** `Slim Tim`. Only C20 `Brown boys` ×3 obeys.
   And **both** cases 2026 shares with 2011 are renamed: **C25 `skinny Bob` → `Bob's walkabout`/`Slim Tim`; C26 `How to drive` → `Tim's show &tell`.**
   Score: 2011 took 0 of 4 opportunities to rename a case; 2026 took 3 of 4 within-era and 2 of 2 cross-era. This is the sharpest lore inconsistency I found. Confidence: **high** on the measurement; **moderate** on the interpretation (2026 could be treating the name as a per-fragment label by design — but then it is a different convention from the one 2011 demonstrably used).
7. **Register of the names.** 2011: six plain descriptive two-to-three-word names (`Tin bird`, `Flying twin`, `Blue boys`, `Blue boys meeting`, `skinny Bob`, `How to drive`) — no abbreviations, no possessives, no parentheticals, no codes. 2026 adds all of them: possessives (`Tim's`, `Bob's`), abbreviations (`Mk.4`, `Mk.5`, `unauth`, `&tell`), an alphanumeric code (`EBL04`), a proper-noun place (`False Cape`), clinical jargon (`Triage`), and a dense seam of aviation/motorsport idiom (`taxi`, `pace lap`, `virgin`, `early boarding`, `primer`). 2026 *does* echo 2011's families (`Blue boys` → `Brown boys`; `Tin bird` → `Tin bird unauth/primer`) — deliberate continuity — but the idiom is a different writer's. Consistent with FINDINGS §15.4.
8. **Capitalization.** ivan wrote `skinny Bob` (lowercase adjective). qtecqot writes `Slim Tim` (both capitalized) — the same copyist-tidies-the-source signature as the dropped `a` and the corrected tag misspellings.
9. **New notation with no 2011 precedent:** the `~` sampled-range separator (v3 only) and the `(col/s)` parenthetical (v1 only). Both are plausible extensions; neither exists anywhere in 2011. Weak tension worth noting on `(col/s)`: it marks a Tape-06 fragment as colour+sound, while the only 2011 tape-06 presentation (`a6TLGkrfNKI`) is monochrome and its audio track is digital silence — but that is a property of the upload, not necessarily of the source tape, and a6TL carries no timecode, so it cannot even be placed on tape 06's timeline. I would not press this.

---

## Correction to FINDINGS

**FINDINGS §11.6 — "First catalog mismatch found anywhere" — should be retracted as an anomaly.** The v1 `Mk.4 pace lap` claim ending 01:11:21 while the screen stops at 01:11:20 is not unusual; it is the house convention in **both** eras.

Endpoint audit: **2011 misses 6 of 22 endpoints outright (27 %), plus 1 indeterminate.** Three end-shortfalls in ZB, and RsQ misses the *claimed start second* three times out of three (`00:08:42`→first shown `:43`; `00:27:36`→`:37`; `00:55:07`→`:08`). For comparison the 2026 rate is 1/10 (v1) and 5/16 (v2, re-derived from FINDINGS §4's own observed column: C11 start, C20 end ×2, C21 end, C25 end). Same behaviour, comparable rate. Anything built on "2026's catalog has a mismatch" collapses.

Minor: FINDINGS §11 says v1's Card C is "verbatim identical to the description". It is not — the card uses the RsQ-style `Tape 02 edited fragments:` header where the description uses `Tape 02:`. The fragment lines themselves are identical.

---

## Could not determine

- **`ZB788PtqQvg` Case 15, whether `00:27:13` ever appears.** It would fall in f446–450, which is washed out by a full-frame flare (`sheets/strip_zb_2713.png`). Neither median-stacking nor percentile stretch recovers the glyphs.
- **Any tape number for the 2011 fragments beyond what the text states.** All 11 2011 overlays are redacted; 2011 never leaks a prefix (confirming FINDINGS §12). Tape attributions for ZB come from its description and for RsQ from its card — neither is verifiable from pixels.
- **Exact character count of the 2011 hidden prefix.** ~4.5 characters by footprint; the feathered bar edge leaves ±0.5 char. Cannot distinguish a 4- from a 5-character prefix, so I cannot confirm or refute that 2011 used `T<n>-02`.
- **Whether `a6TLGkrfNKI` (Tape 06) has a timecode outside the visible frame.** It is a magnified crop with a full film-gate border visible at f1790 and no overlay anywhere; the overlay may simply have been cropped out in 2011, or never existed for that tape. Either way it is unledgerable.
- **Whether 2026's Case-25 subjects could be the 2011 individual.** Resolution-limited, as above.
