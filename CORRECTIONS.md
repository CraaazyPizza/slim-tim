# Corrections log

Every claim this investigation made and later had to withdraw, narrow or reverse, with
what caused the change. Kept as a separate document because corrections scattered through
a 2,100-line notebook are corrections nobody reads — and because **the credibility of
anything we publish rests on being able to show this list exists.**

Newest first. "Ours" = a claim we made; "outside" = a claim someone else made that we tested.

---

## 2026-08-02 — the deleted-post recovery

Eleven deleted @qtecqot posts were recovered from Wayback captures of Twitter API v2
lookups. They contradict four published claims. Method and evidence:
`qtecqot-x-recovered/PROVENANCE.md`.

### 1. ★ "Central European is a clean seven-for-seven morning band" — WITHDRAWN (ours)
**Was:** `reports/agent_qtecqot_dossier.md` §3 rendered **7** machine-read instants against
four candidate zones and reported CEST as a clean 06:23–11:39 morning band, "eight for eight"
if a ninth act were included. From that it built a best-fit-zone comparison against ivan0135
and concluded the two clocks "do not overlap".
**Now:** the account authored **19** X posts, not 2. Against all 19, counting acts falling
outside 07:00–24:00 local, **CEST puts 7 of them in the small hours**, Moscow 5, US Pacific 10,
US Eastern 11. The only offsets under which *no* post lands in the small hours are **UTC+8.5 to
+10**. The published European reading does not survive, and the replacement is not "it is
UTC+9" but **the clock no longer identifies a zone at all**: the constraint is brittle, one
late-night post kills a candidate, and the acts split into two epochs (14 posts in UTC
04:53–13:32 up to 2026-07-31 10:18, then 5 posts in UTC 22:33–03:45). Those two epochs are
*not* incompatible, they overlap at UTC+8.5 to +10, but the discontinuity is the strongest
structure in the data and it is unexplained.
**Cause:** a 7-point sample treated as the population. The 17 missing acts were deleted posts,
and no one had looked for deleted posts. Recompute: `analysis/clock-redo/`.

### 2. "the two tweets" — SUPERSEDED (ours)
**Was:** dossier §4.5 presented the account's output as two posts.
**Now:** 19 recovered, 11 of them deleted. §4.5 is a subset, not the record.

### 3. "replies to anyone, ever: 1" — WRONG (ours)
**Was:** dossier §9.
**Now:** at least three replies to third parties plus two retweets, one of which was itself
deleted and reposted.

### 4. "the X account was dormant April to July" — WRONG (ours)
**Was:** implied by `FINDINGS.md` §23 and the July check that found zero posts.
**Now:** it posted 30 minutes after registration and was wiped before 2026-07-28 07:18:28. The
July "zero posts" reading was the *result* of a purge, not evidence of dormancy. Relaunch, not
activation.

### 5. "one username change, prior handle not recoverable" — NARROWED, not withdrawn (ours)
**Was:** dossier §9 and `docs/TIMELINE.md` line 211 left this as an open item.
**Now:** all 19 archived records carry `username` alongside an at-post-time `tweet_count`, so
each reflects the handle as it stood then. All 19 read `qtecqot`, the earliest at 05:54:16, and
the account was created at 05:24:54. The rename happened inside **29 minutes 22 seconds** with
zero posts and one follower. That is the ordinary signup flow. The item can be closed as
carrying no information rather than left standing as unexplained.

### 6. Method note, ours, caught in-flight
The first pass of the clock recompute scored zones by "width of the tightest arc containing
all acts". That metric is **uninformative by construction** — a constant offset cannot change
an arc's width — and duly returned 14.98 h for all nine zones. A second pass then read a
printout that collapsed a set of admissible offsets to its min and max, and concluded the two
epochs were incompatible. They are not. Both errors were caught before publication and both are
recorded in the scripts. `analysis/clock-redo/clock19c.py` is the one to trust.

---

## 2026-08-01 — the colour-segment duplicate count

Both entries come from one independent re-measurement of `OpSTlDJWFFI` f2571–2917 with
no reuse of either prior classification. Method, all 29 pairs, threshold sweep and codec
cross-check: `reports/agent_colour_duplicate_count.md`. Scripts:
`analysis/colour-duplicate-count/`.

### 1. ★ "Period-12 conform is only weakly expressed here" — NOT REPRODUCED (ours)
**Was:** `agent_mk5_claims.md` item 5e reported **3** near-identical consecutive pairs in
346 frames for the colour Mk.5 segment, concluding the conform was barely present there.
**Now:** **29** duplicate pairs, all at one phase, disjoint from the other 317 pairs on
raw mean-abs-luma (highest duplicate 0.3885, lowest non-duplicate 0.5195) and identical
under both codecs. The conform is fully expressed.

**Cause, and it reproduces exactly:** an absolute threshold (`mad 0.02–0.07`) calibrated
on videos 2 and 3 was applied to a segment with a higher AV1 noise floor. A cut at
0.05–0.06 yields two to four pairs; the full series needs 0.40. Every detection at every
cut lands on the same phase, so the series was being **truncated, not absent**.

**Standing rule: never carry an absolute similarity threshold between segments.**
Normalise locally, or derive the cut from the distribution you are actually measuring.
The report's own note that all three of its hits sat at one phase of twelve (p ≈ 0.7% by
chance) was the available tell. → §20

### 2. "Bit-identical frame every 12" — WRONG FOR THE MEASURED COPY (ours)
**Was:** `agent_video1_OpSTlDJWFFI.md` describes the period-12 pairs as "bit-identical",
and FINDINGS §20 repeats it. `agent_triage_technical.md` §9.3 had already flagged the
conflict with videos 2 and 3, which call the same phenomenon "near-identical, *not*
bit-identical".
**Now:** measured both ways. **Zero** of the 29 pairs are bit-identical in `videos/2026/`
(AV1); **one** is in `videos/2026-avc/` (AVC). Both reports were right about their own
copy. "Near-identical" is the defensible word for the corpus the writeups were measured
on, and it is a claim a reader can check.

Same measurement also **confirms the 11/12 conform factor for this segment directly** —
unique fraction 317/346 = 0.91618 against 11/12 = 0.91667, agreeing to 0.05% — which had
previously been carried into the colour clip on the strength of the global result only.
Consequence for FINDINGS §20's "40.8 distinct images per source second": it becomes
**41.2**, not the 41.7 proposed in `agent_triage_technical.md` §4.6. → §20

*`agent_mk5_claims.md` and `agent_video1_OpSTlDJWFFI.md` are left unedited. Reports are
the historical record; corrections live here.*

---

## 2026-07-29 — the "other people" section

### 1. "Rock Ferguson['s Facebook page carries a] Meta-verified badge" — WRONG (ours)
**Was:** `FINDINGS.md` §6d described the small icon next to the "Rock Ferguson" name in
both reel screenshots (`Screenshot 2026-07-26 215849.png`, `…215915.png`) as a
"Meta-verified badge."
**Now:** it is not. At 6–8× pixel zoom on both screenshots, the icon is unambiguously a
grey globe — Facebook's standard "Public" post-visibility indicator, not the blue
checkmark that denotes a verified Page. Gemini's independent read of both images agreed
before this was written up, per this project's practice of getting a second, less
bias-prone visual read before publishing a claim about an image. No verification claim
about this Page should be made from these two screenshots.
**Cause:** a small icon, described from memory rather than re-examined at zoom. Full
writeup: `reports/agent_other_people.md` §3.1.

---

## 2026-07-29 — the self-audit wave

An 11-lane read-only agent sweep over the whole corpus, with an independent skeptic
attempting to refute each candidate. It found **no measurement error**. What it found was
the failure mode CORRECTIONS.md was created to prevent, still operating: **early sections
were never annotated when later ones reversed them**, so a reader going in order met
retracted claims stated as settled. Eleven items, all now fixed in place.

### 10. ★ OUTREACH Draft 3 printed every number the hold-back policy forbids (ours, operational)
**Was:** Draft 3 — the file's own recommended post — contained all six HOLD items in the
clear (font metrology 43.94–44.00 vs 42.18–42.56 and the slash angles, the frames-per-tick
fingerprint, 0.538×/0.666×, the 13.0 Hz bed, the 50/100 Hz hum, step-printing and colour
geometry) **and the 8/8 timing prediction plus tape number in plaintext** — the single item
the policy names for sealing. "Notes for the owner" (iii) then told the poster to keep the
prediction "even if the post gets trimmed", contradicting the seal-and-hash instruction
three paragraphs above. The quarantine banner flagged two *other* Draft-3 problems and
missed this.
**Now:** findings stated without the metrics; prediction moved to a SHA-256 seal (slot ⟨F⟩,
unfilled); note (iii) reversed; banner extended.
**Cause:** the policy was written on 07-28 and Draft 3 was written *before* it, then never
re-checked against it. **The policy governs the file; it did not govern the file.**

### 11. ★ "2026 runs at ~0.55×, same as 2011" — falsified by §12, never retired (ours)
**Was:** §4 "Triage segment: 7 video seconds per 4 source seconds ≈ 0.57× … close to the
~0.55× slowdown long claimed for the 2011 originals", and §5 "**13 Hz independently
corroborates the ~0.55× slowdown** … the audio and the burned-in-timecode cadence agree."
**Now:** both retracted. The frame-exact ratio for that exact segment was already in the
report §4 cites — 45 frames/tick × 4, **0.666 ± 0.01** — making 0.57× a fencepost slip. And
§19 resolves the audio the *other* way: 13 Hz = 24 fps at **2011's** 0.538×, not 2026's
0.666× (which gives ≈16 Hz). The audio and picture are **decoupled by ~3 Hz**; the bed was
copied from 2011 unchanged.
**Why it matters:** §12 — the designated linchpin — exists to establish that 2026 is *not*
the 2011 timing. Two earlier passages said the reverse, unmarked, in the same file. **The
second one is not just wrong, it is a result pointing the other way that was read as
agreement.** → §4, §5.2

### 12. "The only human face in the corpus" was refuted twice and still stood at its source (ours)
§31.1 contained the literal instruction *"Replace §20's 'the only human face in the entire
seven-video corpus' with:"*. It was never carried out. Now done. See #1 below — this is that
correction finally reaching the sentence it was about. ⚠ **Video 3 remains unswept.**

### 13. §21's morphometry verdict read as final after §28 reversed it (ours)
"Real continuity" and "**morphometry moves the provenance question in neither direction**"
sat unannotated ~500 lines before the section that reverses them. Now marked in place, with
the D4/D3 row that went unread called out where it sits. See #2 below.

### 14. Channel creation "2026-04-21 (API-exact)" — WRONG, it is Apr 22 (ours)
**Was:** §4b, "qtecqot channel created (API-exact; matches the in-lore date '0135 location
and status unclear as of 2026/04/21' **exactly**)."
**Now:** `2026-04-22T05:27:55+00:00` (`watch/CHANGELOG.md`, `watch/snapshots/`). §6e, §24 and
§25 all already said Apr 22.
**Why it matters:** the error **manufactured a same-day coincidence that does not exist**.
The real relationship — account stood up the day *after* its own fictional trigger date — is
still interesting, but it is an offset, not a match. Of everything in this wave this is the
only one that invented a fact rather than failing to retire one.

### 15. ★ agent_cyr3 landed after every synthesis document and was folded into none (ours, process)
`reports/agent_cyr3.md` (00:54) postdates FINDINGS.md (00:11), CORRECTIONS.md (00:12) and
UNFINISHED_BUSINESS.md (00:37). Meanwhile §26.3 still said "re-derivation **dispatched**"
and §26.7 still called the AARO question "the single highest-value pixel test available
(dispatched)" — it had been run and had come back **refuted**. Now folded in as **§2a**.
Headline: geometry was wrong (baseline **1056** not 1048, size **0.86×** not 0.6×, Roboto
Medium not DejaVu); at the corrected geometry **«ААРО» = AARO is refuted** (z ≤ +0.78, rank
286–997/1500, and no ink where its 4th capital must sit) as is «ААРС»; «об АА» survives at
≈2.7σ — exactly the level a *known-correct* pair scores, and eight other pairs score as well.
**The downscale-then-stretch recipe changes measurement by <0.5 %** — our "unreadable at this
amplitude" was right as a measurement and wrong only about perceptibility.

### 16. The frames-per-tick argument lost its hedge in transcription (ours)
Source report: "**Suggestive, not proof.**" FINDINGS turned "the telling detail" into "the
**smoking-gun** detail" and "is the signature of" into "**actively argues**". This is the
most-repeated argument in the document and the weakest link in the chain that carries it —
the same author using a different editor, or a written-down "hold N frames" setting, leaves
an identical trace. Hedge restored at §12.

### 17. The 50 Hz hum: disclaimed as a hypothesis, then reused as "our physical evidence" (ours)
§6e: "**only a hypothesis and cannot serve as a physical geolocation counterweight**". §24.5,
same day: "Convergence with **our physical evidence**: Croatia = 50 Hz grid". Hardened again
at §25.1 ("our physical evidence predicted it", "the only physical evidence on that point").
Now bounded in place: **all of Europe and Russia is 50 Hz** — it excludes the Americas and
essentially nothing else.

### 18. The ledger's sharpest result never reached FINDINGS (ours, miss)
`agent_catalog_ledger.md` called the **one-name-per-case rule** "the sharpest lore
inconsistency I found", and INDEX.md routed it to §11.6/§18 — but neither the rule nor its
score (**2011: 0 of 4 renames; 2026: 3 of 4 within-era, 2 of 2 cross-era**) was ever written
down. §18 narrates all the same case names without stating the pattern. Now recorded as §18b.
**Second instance of the #2 failure mode: a result we had, in a report we archived, unread.**

### 19. Smaller slips, all confirmed and fixed
| item | was | is |
|---|---|---|
| §22 upload cadence | "RsQ→Xju exactly **7 days + 12 min** apart" | 604,080 s = **7 days *minus* 12 min** — sign backwards |
| §31.3 raster-lock | "holds position to **±1.5 px**" | its own table says **−1.5 → +3.5 px** (5.0 px spread) — understated the max excursion >2× |
| §21 profile gap | "**9σ** difference" | z = 0.059/√(0.008²+0.003²) = **6.90σ**; copied unchanged from the report |
| §5b audio match | whole-video "spectrally indistinguishable" | **b/w portions only** (§19 narrows it; §5b never said so) |
| §26.4 face duration | "a **~8 s** sample (f1435–1670)" | **f1437–1570 ≈ 4.5 s** |
| OUTREACH Draft 3 | cites **f1620** as a "service cap" | ~50 frames past where the figure ends (f1570) |
| §2 leader extent | "frames ~917–1249" | **f917–1048** (already logged as #7; the source sentence was never edited) |
| §2c flashes | "**bracket** the hidden-Cyrillic leader" | runs not single frames, not blank, and the first sits *inside* the leader (already logged as #6; same) |
| §16 slashed zero | "the real 2011 zero is **visibly** slashed" (citing font_glyph_grid_2011.png) | the fit is sound (R²=0.995) but **that figure shows no visible diagonal** — confirmed by direct view, 5× crop, and two non-leading Gemini reads. Cite the fit, not the picture |

**Note on #7 and #6:** both were already logged here on 07-28 — and both were *still* wrong
at their source sections when this audit ran. **A correction logged centrally but never
anchored at the claim is a correction that only protects readers who read this file first.**
That is now the standing argument for doing both.

---

## 2026-07-28 / 29 — the community wave

### 1. ★ "The only human face in the entire seven-video corpus" — WRONG (ours)
**Was:** §20 stated the video-2 Case 22 bearded man was the only human face across both eras.
**Now:** There are **two**, both in the 2026 material. Video 1 f1437–1570 (Case 12) shows a
head and shoulders in near-profile that is *better* than the Case 22 one — legible in a
single raw frame with only a linear stretch, no stacking. Passed rotation, five
non-overlapping stack windows, five matched control regions, and the grey-identity control.
**Cause:** the outside analyst pointed at the range; our scenes agent had explicitly never
swept videos 1 or 3. **Video 3 is still unswept — do not restate any corpus-wide claim.**
→ §31.1, `reports/agent_v1faces.md`

### 2. ★ "The four-digit hand matches the 2011 plate — real continuity" — REVERSED (ours)
**Was:** §21/§8 reported the 2026 hand matching the published 2011 print "almost exactly"
and concluded morphometry does not discriminate provenance.
**Now:** The three-finger length *gradient* differs. R = 0.676 (2011) vs 0.854 ± 0.059
(2026), +26 %, holding in all 49 usable frames across five camera setups; distributions do
not overlap. The palm-vs-dorsum systematic is excluded because it must move both ratios the
same way and they move in **opposite** directions.
**Cause:** an outside analyst noticed by eye. Worse — **the number was already in our own
table** (D4/D3 0.67 vs 0.80, a 19 % gap, tabulated without comment beside two that matched).
We had it and did not look.
**Also unresolved:** the new palm-width figures (2.01 vs 1.40) contradict §21's (1.38 vs
1.37). One has a definitional problem; §21's is what currently carries the old claim.
→ §28, `reports/agent_finger.md`

### 3. "The «об АА» convergence supports the owner's reading" — WITHDRAWN (ours, same day)
**Was:** I told the owner that LC's independent reading corroborated his line-2 attestation.
**Now:** LC published **two mutually inconsistent readings of the same pixels two days
apart**. And §2 had already shown *why*: «предупреждало» is nearly the only natural
neuter-past continuation after «Предыдущее сообщение», so models converge on it from
grammar with zero pixel evidence. It is a second draw from the same biased generator.
**Survives:** two AI systems and one human all place a capital-А pair after «об», matching
the one thing pixel-ranking supported. **The owner's reading is unchanged in status** — no new
support, no new damage. → §25.2 item 5

### 4. "Eastern European descent contradicts the US flag" — OVERSTATED (ours, same day)
**Now:** "Descent" is ancestry, not residence. An American of Eastern European descent
satisfies the tweet *and* the flag. It is a convergence with our measurements, not a
retraction by the author. The 50 Hz hum remains the only physical evidence on the point.
→ §25.1

### 5. "Zero public discussion of qtecqot anywhere" — INSTRUMENT ARTIFACT (ours)
**Was:** §23 reported a total absence of public footprint as of 2026-07-27.
**Now:** An r/SkinnyBob thread existed from ~2026-07-24, started by someone else. It was
invisible because **Reddit blocks this sandbox at the network layer.** Search-indexed
discussion was and is zero; Reddit discussion was not.
**Standing rule: never report a blocked-network null as an absence.** → §25.3

### 6. Leader-flash frames "blank / content pending" — WRONG (ours)
**Now:** Both are film burn-through events full of structure, and they are *different from
each other*: f1040–1044 orange (R/G 1.65), burn front rising from the bottom, with a
hard-edged Γ/r-shaped bright mark at **f1043 only**; f1248–1249 yellow (R/G 1.09), front
descending from the top, carbonised specks, picture still visible through it. Also they are
**runs, not single frames**, and §2c's claim that they "bracket" the Cyrillic leader is
wrong — the first sits *inside* it. → §31.5, §26.3

### 7. Hidden-Cyrillic leader extent — IMPRECISE (ours)
**Was:** "~f917–1249". **Now:** f917–1048. f1049–1249 is Case 11 picture; f1250–1260 is a
second, separate 11-frame leader we had never catalogued. → §26.3

### 8. "Line 2 is unreadable at this amplitude" — TOO PESSIMISTIC (ours)
Measured with a high-pass/registered-average estimator. A downscale-then-stretch operation
(Lanczos to ~70 %, then percentile stretch) is a better matched low-pass for ~30 px glyphs
and recovers more. Re-derivation dispatched. → §26.3

### 9. Mk.5 colour segment bounds and cadence (ours)
Segment is **f2571–2917** (347 frames), not to 2990. Timecode runs :56→:03, eight ticks,
not ":56…59". **★ Flagged:** frame-precise ticks give **46.0 frames/second = 0.6515×**, the
same as the b/w clips — not §11.2's 44.5 / 0.6735×. If it replicates, **withdraw §11.2's
"the colour clip is retimed differently within the same video".** Not yet settled: two of
seven tick boundaries sit behind flares. → §30.4

**★ flag superseded — settled, and not in favour of 46.0.** `agent_triage_technical.md` §4
re-measured it: the colour segment yields exactly **one** fully measurable tick interval
(f2706 → 2751 = 45 frames), because in the flare windows the timecode is not faint, it is
**absent**, and no processing recovers it. So 46.0 rested on boundaries that cannot be read.
§11.2's differential-retime claim is withdrawn as flagged — but **46.0 is not substituted
for 44.5**; both were wrong. The answer is a count, **45.000**, holding in every fragment of
all three 2026 videos measurable to the frame. → FINDINGS §10.5

The follow-on measurement this flag called for is already logged above: the 2026-08-01 wave
recomputed §20's "40.8 distinct images per source second" — a figure derived from the
withdrawn 44.5 — to **41.2**.

---

## Outside claims we tested (the other direction)

| Claim | Source | Verdict |
|---|---|---|
| Little finger longer than the 2011 print | LC | **CONFIRMED**, amended to the whole gradient — and it reversed our §21 |
| Human figure in video 1 (f1435–1670) | LC | **CONFIRMED**, range over-extended ~100 frames (ends f1570) |
| Something added at f1225 | LC | **CONFIRMED as added**, but not adhesive tape — a raster-locked element that holds position to ±1.5 px while the scene translates 50×72 px behind it |
| Leader frames carry content | LC | **CONFIRMED** — better localised than ours |
| f1207–1210 discontinuity | LC | **CONFIRMED** (2-frame exposure dropout + viewpoint change); "film changeover" **REFUTED** (timecode continuous) |
| Chinook reflected in the Mk.5 hull, rotors turning | LC | **REFUTED** — fixed in craft coordinates; one apex not two pylons; rotor smears absent >10σ; same feature on a *different* craft in b/w 50 s earlier |
| Five-pointed star in the Mk.5 segment | LC | **REFUTED** — 5-point template never beats 6-point/disc controls in 1,044 cells |
| Five-pointed star on the shoulder board | LC | **REFUTED** — 5-fold self-correlation scores *below* 6-, 7- and 8-fold |
| Human face at f1210–1247 | LC | **REFUTED** — the most face-like object is the disc, which reads identically at all 8 rotations |
| "Family vacation" is in colour like the Mk.5 clip | LC | **REFUTED** — monochrome under a steep single-axis tint (resid V 0.97 vs 3.94) |
| Human voices in the col/s audio | LC + the owner | **NOT SUPPORTED** — no speech survives separation, pitch tracking or hallucination controls. Two independent listeners hearing it is a real fact about the *stimulus* |
| All Mk.4 sequences are on Tape 02 | LC | **FALSE** — video 3's own description puts one on Tape 03 |
| `T6-02/31` is the only unmasked prefix | LC | **FALSE corpus-wide** (video 2's `BL04 /22`); true within video 1 |
| Endpoint timecodes don't match the footage | ours | **RETRACTED** — house convention in BOTH eras; 2011 misses 27 % |
| "#020202 dots" are a watermark | community, 2011 | **REFUTED** — AV1 tile-corner artifact, now confirmed from a second codec |
| "Tape 06 kept its colour" | community, 2011 | **REFUTED** |
| 2011 runs at ~0.55× | community, 2011 | **CONFIRMED** — 0.538× |

---

## The pattern worth remembering

Four of the first nine corrections came from **one outside analyst with no forensics
training looking at frames by eye**, and two of those overturned conclusions we had
published with confidence. Two more were things sitting in our own tables unread.

Nothing there was caught by re-reading our own work harder. It was caught by someone with a
different prior looking at the same pixels. Budget for that: keep testing outside claims on
their merits, and keep the corrections visible.

**Amended 2026-07-29, after the audit wave (#10–#19).** The last clause of that paragraph
turned out to be half right in a way worth naming. A structured adversarial sweep — lanes
that could not see each other, each finding forced through a skeptic told to refute it —
*did* find eleven real things by re-reading our own work. So "you cannot audit yourself" is
too strong. But look at **what** it found: not one measurement error. Every single item was
**bookkeeping** — a reversal that never reached the sentence it reversed, a hedge dropped in
transcription, a report archived and not read, a policy that did not govern its own file.

That is the honest split. **An outside prior finds wrong measurements; a systematic
self-audit finds unpropagated corrections.** They are different failure classes and they need
different instruments. Neither substitutes for the other.

Two structural lessons:

1. **Log centrally *and* anchor locally.** Corrections #6 and #7 were logged here on 07-28
   and were still standing uncorrected at their source sections when the audit ran a day
   later. This file protects the reader who reads this file. Most readers read FINDINGS in
   order and never get here.
2. **A document that arrives after the synthesis does not enter the synthesis.**
   `agent_cyr3.md` — on its own account the most rigorous measurement in the corpus, and it
   *refuted* a reading we had been treating as the highest-value open question — sat
   unconsumed for forty minutes purely because it landed after FINDINGS was last written.
   Nothing flagged it. There is no mechanism that notices a new report; there should be.

The count is now nineteen. That is not a bad sign — an investigation this size with a
corrections log this short would be the thing to worry about.
