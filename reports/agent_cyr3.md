I've completed the measurement. Here is the report.

---

# Line 2 of the hidden Cyrillic caption (video 1, `OpSTlDJWFFI`) — pixel measurement of the candidate readings

Agent: Opus "cyr3", 2026-07-29. Working directory `analysis/cyrillic/gen3/` (scripts + artefacts, all reproducible).
Prior work extended: `reports/agent_cyrillic_line2.md`, `reports/agent_pdf_breakout.md` §5.6, §6.1–2, FINDINGS §2.

**Bottom line up front.** The downscale-then-stretch recipe is a *display* improvement, not an information improvement — it changes measurable recovery by <0.5%. The prior record's line-2 geometry was wrong in a way that mattered (baseline off by 8 px, font size understated by ~40%); corrected, the pixels now say something they did not say before. Line 2 ends in a run of **capital-height glyphs**, and that is a hard, glyph-agnostic measurement. Within it, **«АА» scores exactly as well as a known-true capital pair scores on line 1** (z ≈ +2.7, rank 4–13 of 784) — but five to ten other capital pairs score as well or better. **«ААР» is unsupported. «ААРС» and «ААРО» are refuted**: there is no ink where their 4th glyph would have to be, and both score at or below the null. The verb «прослушано» is refuted on line length; «предупреждало» is not confirmed but is the only one of the two compatible with the measured line.

---

## 1. Estimator validation on line 1 (ground truth)

### 1.1 Re-derivation of the caption block

Frames 910–1049 of video 1, luma, brightness-normalised per frame; background = mean of all frames outside 966–993. Per-frame caption amplitude measured by projection onto the line-1 ink pattern:

- f970–989: amplitude **0.47 – 1.23** (mean 1.00), varying 2.6:1 within the block.
- Every other frame in 910–1049: **|amplitude| ≤ 0.029**; the largest outlier is f967 at +0.029.

Independent confirmation of f970–989 and of the earlier correction that the caption is *not* in f917–921.

### 1.2 The typeface is Roboto Medium, not DejaVu

Whole-phrase fit of «Предыдущее сообщение», 9 Cyrillic-capable faces × sizes 70–120 × blurs 0.8–7.5:

| face | best r | size | blur | x | baseline |
|---|---|---|---|---|---|
| **Roboto Medium** | **0.6662** | 104 | 5.0 | 438 | 985 |
| Roboto Regular | 0.5509 | 106 | 6.0 | 436 | 986 |
| Roboto Light | 0.5386 | 108 | 6.0 | 438 | 986 |
| DejaVu Sans | 0.5278 | 94 | 3.2 | 440 | 984 |
| Roboto Condensed | 0.5059 | 120 | 3.2 | 437 | 992 |
| Lato | 0.4975 | 106 | 3.2 | 436 | 985 |
| Liberation / Noto / Open Sans | 0.404 / 0.395 / 0.362 | | | | |

Roboto Medium beats DejaVu (the prior report's font) by 26%. All line-2 work below uses RobotoM templates. *Caveat recorded honestly:* RobotoM is the best available proxy, not an identification — line 1's horizontal metrics demand size 104 while its vertical ink band is only ~⅔ of Roboto's x-height at that size, so the real face has a lower x-height for its width than Roboto. §4.5 shows this does not affect the conclusions.

### 1.3 Head-to-head: prior ladder vs LC's downscale-then-stretch

Every preprocessor is applied identically to observation and template (so each is a legitimate matched filter). Nulls: 9 near-miss real Russian phrases of the same length, and 6 nonsense strings.

| preprocessor | r(true) | z vs near-miss | z vs nonsense | margin over best decoy | line-1 glyphs correct | mean glyph rank /32 |
|---|---|---|---|---|---|---|
| `flat` (row-median only) | 0.4260 | +3.36 | +5.14 | +0.111 | 5/19 | 3.37 |
| **`hp20` (prior ladder)** | **0.6648** | **+4.38** | **+6.68** | **+0.127** | 4/19 | 4.37 |
| `down70` (LC, linear part) | 0.4263 | +3.36 | +5.14 | +0.111 | 5/19 | 3.37 |
| `down70 + hp20` | 0.6655 | +4.38 | +6.68 | +0.127 | 4/19 | 4.42 |
| `down50 + hp20` | 0.6657 | +4.38 | +6.68 | +0.127 | 4/19 | 4.42 |
| `down85 + hp20` | 0.6372 | +3.53 | +7.13 | +0.077 | 4/19 | 5.37 |

Adding the clipping percentile stretch (the display half of the recipe):

| full pipeline | r(true) | z vs nonsense |
|---|---|---|
| hp20 | 0.6648 | +6.68 |
| down70+hp20 | 0.6655 | +6.68 |
| hp20 → 2/99.5 clip | 0.6712 | +6.71 |
| down70+hp20 → 2/99.5 clip | 0.6720 | +6.71 |
| down70+hp20 → 30/99.9 clip | 0.5738 | +7.11 |

Band signal-to-noise (band σ in excess of the caption-free null σ, divided by null σ):

| pipeline | line 1 | line 2 |
|---|---|---|
| hp20 | 5.86 | 2.94 |
| down70+hp20 | 6.03 | 3.04 |

**Verdict on the estimator: the downscale-then-stretch recipe is not better in any measurable sense.** It changes r by <0.001, z by <0.05, and glyph accuracy not at all. The reason is mechanical: the optimal template blur is already σ = 5.0 px, which cuts the same frequencies a 70% Lanczos downscale cuts, so the matched filter had already applied that low-pass. The recipe genuinely helps *human and VLM* reading — it removes high-frequency noise the eye integrates badly and enlarges the glyphs relative to it — and that is why LC and the PDF agent saw more. It adds no recoverable information. The PDF agent's item §5.6 should be amended: FINDINGS §2's "unreadable at this amplitude" was correct *as a measurement*; it was too pessimistic only as a claim about perceptibility.

The marginal winner is the prior ladder (`hp20`) on an amplitude-weighted frame combiner (r 0.6648 vs 0.6634 for plain block-differencing). That is what everything below uses. `down70+hp20` gives numerically identical answers throughout; I re-ran the critical tail segmentation under all four variants and the results are the same to within a pixel (§2.4).

Figure: `FIG_estimators.png` — lines 1 and 2 under `flat`, `hp20`, `down70+hp20`. They are visually near-identical for line 2.

### 1.4 The calibration that matters most: individual letters are not readable, even on line 1

With all other letters held at truth, swapping letter *k* for each of the 32 same-case Cyrillic letters and ranking:

- best pipeline: **4–5 of 19 letters correct**, mean rank of the true letter **3.4–4.4 out of 32**.
- The errors are systematic left-to-right (declining local SNR): `П→Л, р→р, е→е, д→д, ы→ы, д→ц, у→у, щ→ш, е→с, е→с, с→з, о→ч, о→я, б→с, щ→ш, е→с, н→ч, и→ф, е→ф`.

Line 1 carries **2.0×** line 2's amplitude and **1.16×** its font size. If we cannot identify individual letters on line 1, we cannot identify them on line 2. This bound governs everything that follows.

---

## 2. Measured geometry of line 2 — three corrections to the record

All measurements against a null built the same way from caption-free frames (20-frame blocks differenced against the remaining background frames, identical estimator).

### 2.1 Ink extent

| | left edge | right edge | width |
|---|---|---|---|
| line 1 | 445 | 1597 | 1152 px |
| line 2 | 445 | **1549** | **1104 px** |

Beyond x = 1555 there is nothing: full-band z = **−0.6**, cap-band z = −0.6 (x 1560–1600), and −0.5 / +0.4 (x 1600–1640). The line stops at 1549 ± ~4 px. (Prior record: "x ≈ 450–1560" — consistent, now tightened.)

### 2.2 Baseline and font size — **both were wrong in the prior record**

Row profile of line 2's lowercase region (x 450–1250) against the caption-free null: ink rises steeply at y 1019–1022, plateaus, falls steeply at 1055–1058.

- **Baseline y ≈ 1056**, not 1048.
- x-height top y ≈ 1021.

Font size, measured by the vertical ink-band width (q10–q90 of the rectified row profile, computed identically on both lines using **only x-height columns**, so the two are directly comparable), with the size exponent d log w80 / d log size = 0.79 calibrated from synthetic renders:

| | w80 | |
|---|---|---|
| line 1 (x-height columns only) | 33.7 ± 2.1 px | (block bootstrap over columns + frame bootstrap) |
| line 2 (x 450–1250) | 30.0 ± 1.8 px | |

**Size ratio line 2 / line 1 = 0.864 ± 0.095**, i.e. line 2 ≈ RobotoM 90 — *not* the 0.6× / x-height 30 px in the prior record.

Independent confirmation from the tail: the two triangular cap-height glyphs sit 61 px apart, which is exactly the capital-А advance at size 88–92 (58.7–61.3 px). They are adjacent letters with no letter-spacing. Under the old size assumption they would have been 45 px apart, and the 61 px would have had to be explained by 34%-em tracking.

### 2.3 Implied character count

A line-1-like string at ρ = 0.864 would span 1152 × 0.864 = 1004 px for 20 characters. Line 2 spans 1104 px.

**Line 2 contains 22.2 ± 2.4 characters.**

### 2.4 The tail is a run of capital-height glyphs — glyph-agnostic, and this is new

Cap-band occupancy test: capitals (and the few Russian lowercase ascenders) put ink between cap-height and x-height; ordinary lowercase does not. Calibrated on line 1, whose cap band is occupied at exactly two places — x 446–504 («П») and x 1299–1340 («б») — and empty everywhere else.

Line 2's cap band is **empty across x = 420–1250** (internal null over that range: mean z +2.0, sd 4.9) and **strongly occupied from x ≈ 1300 to 1550**: peaks at x = 1126 (z +41), 1184 (+30), **1312 (+113)**, **1427 (+88)**, **1486 (+30)**, 1541 (+12). Stable across baselines 1053 / 1057 / 1061.

Free-form segmentation of the tail, identical under all four estimator variants (`matched+hp20`, `between+hp20`, `matched+down70+hp`, `matched+flat`):

| blob x | width | ink rows | class |
|---|---|---|---|
| 1161–1181 | 21 | 1016–1062 | x-height |
| 1194–1210 | 17 | 1023–1060 | x-height |
| 1248–1265 | 18 | 1020–1069 | x-height + descender |
| 1306–1321 | 16 | 1002–1067 | full height (above cap *and* below baseline) |
| 1337–1355 | 20 | 1005–1056 | cap height |
| **1404–1448** | 45 | 1000–1048 | cap height, triangular |
| **1468–1507** | 41 | 1002–1051 | cap height, triangular |
| 1534–1549 | 16 | 1003–1056 | cap height, narrow stem |

Line-1 bleed control (this is the obvious way the result could be fake, so it was tested three ways):
1. The fitted line-1 model contributes 0.00059 to line 2's cap band against an observed 0.0184 — 3%.
2. Subtracting the fitted line-1 layer leaves the peak list **unchanged** (x 1312 z 113 → 113; x 1427 z 88 → 88).
3. Of line 1's eight descender columns, seven produce z ≤ +6.1 in line 2's cap band. The eighth (x 1420–1432, the «щ» tail of «сообщение») coincides with a line-2 peak of +88. But the *same glyph's* other descender at x 963–975 produces only +6.1. The tail signal is ~14× too large to be bleed.

Figures: `l2_tail_ruler.png`, `zoom_1390_1600.png` (5–8× zoom with measured baseline / x-height / cap-top guides and an x ruler), `l2_before_l1sub.png` / `l2_after_l1sub.png`.

---

## 3. Candidate ending tests and nulls

### 3.1 Protocol

Each candidate ending is rendered standalone at the measured geometry, slid over x ∈ [1250, 1600], scored by normalised cross-correlation over the full line-2 band, taking the maximum over position. **Nulls get the identical treatment**, including the same freedom in x. Five geometry settings (size 84/88/92 × blur 3.0/4.5).

- **CAPITAL null** (the meaningful one): all 784 capital 2-grams; 1500 sampled capital 3-grams; 1500 sampled capital 4-grams. Alphabet Α–Я less ъ ы ь ё й.
- **lowercase null** (the weak one): same counts, lowercase.

### 3.2 Results on the real data

| candidate | r (range over 5 geometries) | best-fit x | **z vs CAPITAL null** | **rank** | z vs lowercase null | rank |
|---|---|---|---|---|---|---|
| **АА** | 0.533 – 0.582 | **1394 – 1399** | **+2.44 … +2.95** | **4 – 13 / 784** | +3.36 … +4.01 | 1 – 5 / 784 |
| ААР | 0.319 – 0.396 | 1398 – 1464 | +0.97 … +1.86 | 72 – 240 / 1500 | +1.38 … +2.69 | 18 – 135 |
| ААРС | 0.179 – 0.298 | 1392 – 1401 | −0.16 … +1.59 | 93 – 835 / 1500 | −0.03 … +2.45 | 23 – 718 |
| ААРО | 0.155 – 0.240 | 1306 – 1401 | −0.49 … +0.78 | 286 – 997 / 1500 | −0.56 … +1.33 | 146 – 1075 |

Note the lowercase-null z is inflated by ~1.0–1.3 relative to the capital-null z for the same candidate. **This is exactly the artefact the prior agent warned about**, and it is the entire difference between the previously recorded "z = +4.0 over lowercase controls" and the truth. Only the capital-null column is meaningful.

Top-scoring capital pairs at the best geometry (size 88, blur 4.5): АТ 0.613, ХТ 0.598, АУ 0.593, АЭ 0.582, АЗ 0.580, **АА 0.580**, АХ 0.566, КА 0.564, АЛ 0.564.

### 3.3 What the tail glyphs actually are

Per-cell single-glyph identification at the 59-px letter pitch, full Cyrillic alphabet both cases, ±9 px search:

| cell | top matches | top-1 z vs capital null | gap to 2nd capital |
|---|---|---|---|
| x 1279 | п(lc) 0.620, К 0.603, Л 0.584, В 0.575, Н 0.573 | +1.53 | 0.019 |
| x 1338 | М 0.218, Ж 0.202, г(lc) 0.076 | +1.99 | 0.016 |
| x 1397 (triangle 1) | г(lc) 0.541, Е 0.501, к(lc) 0.492, е 0.459, х 0.454 | +2.05 | 0.050 |
| x 1456 (triangle 2) | л(lc) 0.651, д(lc) 0.637, **Х 0.630**, а 0.623, я 0.610, **А 0.579** | +1.75 | 0.051 |
| x 1515 (stem) | г(lc) 0.639, **Г 0.593**, т 0.530, Е 0.520, **Р 0.498** | +2.23 | 0.073 |

Capitals only, third cell: Г 0.565–0.640, Е 0.508–0.532, **Р 0.492–0.504 (rank 3–4 of 28, z +0.96 … +1.29)**, Т, Б, П. **О ranks 17–18, С ranks 11–13.**

**No individual glyph in the tail is identified.** The pixels constrain shape *class*: two adjacent cap-height glyphs with strong diagonal strokes (А / Л / Д / Х class), then a stem-with-top-arm glyph (Г / Е / Т / Р / Б class).

### 3.4 The layout constraint on the ending length

The two triangles occupy x 1404–1448 and 1468–1507. A third capital at the 59–61 px pitch occupies x ≈ 1528–1587 and its stem would sit at ~1534 — which is exactly where the last blob is. A **fourth** capital would need x ≈ 1587–1646. There is no ink there (z = −0.6).

**The terminal capital run has room for three glyphs, not four.** «ААРС» and «ААРО» require four.

---

## 4. Controls

### 4.1 Out-of-range frames (caption absent) — the pipeline must produce nothing, and does

Three disjoint 20-frame caption-free blocks through the identical machinery:

| control | АА | ААР | ААРС | ААРО | top capital pairs |
|---|---|---|---|---|---|
| f910–929 | z −0.47 (552/784) | +0.20 | +0.06 | +0.09 | ЭГ, ФГ, ЗГ, ЯГ |
| f950–997 (bg subset) | +1.74 (31/784) | +1.02 | +1.75 | +1.54 | ЛЕ, ЛГ, ЛТ, ГА |
| f1018–1037 | −0.72 (593/784) | −1.05 | +0.80 | +0.88 | ГЧ, ГГ, ТТ, ЕЧ |

Max |z| over all 12 candidate × block combinations: **1.75**. No candidate significant; the "winning" pairs differ every time. The pipeline does not manufacture signal.

### 4.2 Column-scramble

Randomly permuting the tail columns (x 1250–1600): «АА» collapses from r = 0.580 to **0.110** (z −0.39, rank 447/784); no candidate exceeds z = +0.72.

### 4.3 Parameter sensitivity

- «АА»: position stable at **x 1394–1399** (5 px spread) and z stable at +2.44 … +2.95 across sizes 84/88/92 and blurs 3.0/4.5. Degrades smoothly outside: z +1.0 to +2.1 at sizes 64–72, +1.2 to +1.9 at sizes 96–100.
- «ААР», «ААРС», «ААРО»: best-fit position jumps between x = 1306 and x = 1464 depending on geometry — the same signature of noise-fitting the prior agent identified for «утечке».

**Methodological trap worth recording.** At the *wrong* (old) size of 64 px, «АА» scored z = +0.95, rank 133/784 — nothing. Allowing free letter-spacing at that wrong size then pushed «АА» to rank 3/784 and «ААР» to rank 2/1745, which would have looked like strong support for a three-letter ending. It was an artefact: a wrong font size compensated by tracking. At the correct size no tracking is needed and the apparent support for the third letter disappears. Anyone re-running this must fix the size independently before testing strings.

### 4.4 Power by injection — the test *can* find a true ending

Known text injected into caption-free frames at the measured amplitude and geometry, right-aligned on line 2's measured ink edge, then run through the identical test:

| injected truth | АА | ААР | ААРС | **ААРО** |
|---|---|---|---|---|
| «предупреждало об **ААРО**» | z +4.24 | +5.26 | +6.44 | **+7.12, rank 1/602** |
| «предупреждало об **АА**» | **+5.40, rank 1/784** | +5.38 | +0.40 (196/602) | +0.44 (192/602) |

Robust to typeface mismatch (truth set in Lato / Open Sans / DejaVu, templates always RobotoM, x-height held equal): ААРО recovered at z +6.6 … +7.2, rank 1/502 in every case; АА at z +4.9 … +5.6, rank 1/784 in every case. Raising the injected SNR 2× and 4× changes nothing — the test is not SNR-limited at this level.

### 4.5 Power on *real* ground truth — the number that actually calibrates §3

Synthetic injections use clean ink and therefore overstate power. The honest calibration is to run the identical ending protocol on **line 1, whose ending we know**:

| ground-truth string tested | z vs matched null | rank |
|---|---|---|
| line 1 opening «П» (capital, known) | **+1.38 … +2.07** | 1 – 4 / 28 |
| line 1 opening «Пр» (known) | **+2.33 … +3.00** | 1 – 7 / 784 |
| line 1 opening «Пре» (known) | +2.25 … +2.99 | 1 – 82 / 6272 |
| line 1 ending «ие» (lowercase, known) | +0.15 … +0.54 | 264 – 370 / 784 |
| line 1 ending «ние» (known) | −0.83 … +0.62 | 460 – 1182 / 1444 |
| line 1 ending «ение» (known) | −0.98 … +0.78 | 385 – 1191 / 1499 |

Two things follow.

1. **Lowercase endings are simply not recoverable by this protocol, even on ground truth.** Random 3-grams («цсп», «бшф», «пщф») beat the true «ние» by r = 0.57 vs 0.36. Any lowercase reading of line 2's ending is untestable, and this is why the prior agent's «утечке» test could only ever have returned "unsupported".
2. **Capitals are recoverable, but only to ~+2.5σ.** The known-true capital pair «Пр» reaches z +2.33 … +3.00, rank 1–7 of 784, on a line carrying twice line 2's amplitude — and the known single capital «П» is beaten by «Л» at three of six geometries.

**Line 2's «АА» at z +2.44 … +2.95, rank 4–13 of 784, is statistically indistinguishable from how a correct capital pair performs in this data.** That is the fairest way to state the positive result — and equally, it means the near-ties (АТ, ХТ, АУ, АЭ, АЗ, АХ, КА, АЛ) cannot be excluded, because the protocol demonstrably fails to put the truth first even when it knows the truth.

Conversely, «ААР» at z +0.97 … +1.86 falls **below** the ground-truth benchmark for a 3-gram (+2.25 … +2.99), and «ААРС»/«ААРО» at z ≤ +1.59 / ≤ +0.78 fall below it further while also being geometrically impossible (§3.4).

---

## 5. Verdicts

| claim | verdict | numbers |
|---|---|---|
| **Line 2 ends in a run of capital-height glyphs** | **SUPPORTED BY PIXELS, decisively** | cap band empty (z ≈ +2 ± 5) for x 420–1250; occupied at z up to +113 for x 1300–1550; survives line-1 subtraction and the descender-bleed control (14:1 margin); identical under 4 estimators |
| **The run is 3 glyphs, not 4** | **SUPPORTED BY PIXELS** | no ink beyond x = 1555 (z = −0.6); 59–61 px letter pitch leaves room for 1404–1448, 1468–1507, ~1528–1587 |
| **Two of them are triangular / diagonal-stroke capitals (А, Л, Д, Х class)** | **SUPPORTED BY PIXELS** | blobs 1404–1448 (45 px) and 1468–1507 (41 px), tops at y 1000–1002, spaced 61 px = the capital advance at the independently-measured size |
| **«об АА»** | **WEAKLY SUPPORTED — at the ground-truth benchmark level, not above it** | z = **+2.44 … +2.95** vs the 784-capital-pair null, rank 4–13; position stable to 5 px; survives all controls. Benchmark: a *known-correct* capital pair on line 1 scores +2.33 … +3.00, rank 1–7. But АТ/ХТ/АУ/АЭ/АЗ/АХ/КА/АЛ score equal or better, and the protocol cannot separate them. Report as ≈2.7σ against the correct null; the +3.4–4.0σ against lowercase controls is the misleading number and should not be quoted |
| **«об ААР»** | **NOT DISTINGUISHABLE FROM NULL** | z +0.97 … +1.86, rank 72–240/1500, position unstable (1398 ↔ 1464). The third cell's best capital is Г (0.593); Р ranks 3–4 of 28 at z +0.96 … +1.29 — a plausible shape class, no more |
| **«об ААРС»** | **REFUTED** | z −0.16 … +1.59; and no ink exists where its 4th glyph must fall. Injection shows a true ААРС would reach z ≈ +6.4, rank 2/602 |
| **«об ААРО»** | **REFUTED** | z −0.49 … **+0.78**, rank 286–997/1500 — the *weakest* of the four candidates at 3 of 5 geometries. No ink where its 4th glyph must fall. A true ААРО would reach z = +7.12, rank 1/602, robustly across four typefaces. **The AARO-shaped reading receives no pixel support of any kind.** Consistent with prompt priming; the pixels do nothing to raise it above chance and the geometry rules it out |
| **Verb «прослушано»** | **REFUTED (on layout)** | whole-line matching is powerless for both verbs; but line 2 is 22.2 ± 2.4 characters, and «прослушано об АА» (16 ch) is **+6.2σ** short, «прослушано об ААРО» (18 ch) **+3.8σ** short |
| **Verb «предупреждало»** | **NOT CONFIRMED, but compatible — the only one of the two that is** | «предупреждало об АА» (19 ch) +3.1σ short, «предупреждало об ААР» (20 ch) +2.2σ, «…об ААРС/ААРО» (21 ch) +1.4σ. Whole-line template match z = +0.55, rank 7/22 in a null of same-shape phrases topped by a nonsense string. There is **no glyph-level evidence for the verb whatsoever** |

Two things about the verb that must not be blurred. The whole-line test gives **nothing** — all four candidate full lines sit inside a 21-phrase null (z ≤ +0.80), the winner is «щшгнёъьэюцх хк АА» at 0.331, and the fitted geometry wanders over baselines 1052–1071 and sizes 80–98. The *only* discriminating measurement is line length, and it is a length argument, not a reading. It carries systematic risk: it assumes lines 1 and 2 use the same typeface and that neither is tracked. Both assumptions are supported (the tail's letter pitch matches the untracked advance at the measured size) but neither is proved.

There is also a residual tension worth logging rather than smoothing over: the length measurement wants 22 ± 2 characters, i.e. a 3–4 character terminal token, while the glyph measurement supports only the first two. These are compatible — the tail plainly has three capital-height glyphs — but they mean **«предупреждало об АА» as a complete line is itself ~3σ short**. Something is there after the two triangles; we cannot say what.

---

## 6. What the project should record as line 2's status

Proposed replacement text for the line-2 paragraph in FINDINGS §2:

> **Line 2 — present, partially constrained, not read.** Measured (video 1, f970–989 only, all figures against caption-free nulls from the same frames):
>
> - Ink spans **x = 445 … 1549** (1104 px); nothing beyond x = 1555 (z = −0.6).
> - **Baseline y ≈ 1056** and **x-height top y ≈ 1021** — this corrects the earlier "baseline ≈ 1048".
> - **Font size = 0.86 ± 0.10 of line 1's** (RobotoM ≈ 90 against line 1's 104) — this corrects the earlier "x-height ≈ 30 px, roughly 0.6× line 1". Confirmed independently by the 61 px letter pitch of the tail capitals.
> - Amplitude ≈ **0.50×** line 1's (band SNR 2.95 vs 5.9).
> - **Length ≈ 22.2 ± 2.4 characters.**
> - The left ~850 px (x 445–1250) are **entirely x-height lowercase** — the cap band is empty there (z ≈ +2 ± 5).
> - The right end (x ≈ 1300–1550) is a **run of capital-height glyphs**, comprising two adjacent triangular / diagonal-stroke capitals (А Л Д Х class) at x 1404–1448 and 1468–1507, and a stem-with-top-arm capital (Г Е Т Р Б class) at x ≈ 1528–1587. **Room for exactly three, not four.** This is a glyph-agnostic measurement; it survives subtraction of the line-1 layer and a descender-bleed control at 14:1 margin.
> - The typeface of both lines is best matched by **Roboto Medium** (r = 0.666 on line 1, vs 0.528 for DejaVu); it is a proxy, not an identification.
>
> **Candidate readings, tested with the prefix held fixed and only the ending varied, against a null of 784 capital pairs / 1500 capital triples / 1500 capital quadruples (the lowercase null is not informative and its z-scores must not be quoted):**
>
> - **«об АА» — leading candidate, weakly supported, ≈2.7σ.** z = +2.44 … +2.95, rank 4–13 of 784, position stable to 5 px across all geometries, survives out-of-range, scramble and parameter controls. For scale: a *known-correct* capital pair on line 1 («Пр») scores z = +2.33 … +3.00, rank 1–7. So «АА» performs exactly as a correct reading performs in this data — and so do АТ, ХТ, АУ, АЭ, АЗ, АХ, КА and АЛ. **The reading is consistent with the pixels but is not selected by them.**
> - **«об ААР» — not distinguishable from null.** z = +0.97 … +1.86, rank 72–240/1500, unstable position. Р ranks 3rd–4th of 28 in the third glyph cell (z ≈ +1.1), i.e. the right shape class, nothing more.
> - **«об ААРС» and «об ААРО» — refuted.** z ≤ +1.59 and ≤ +0.78 respectively; ААРО is the *weakest* of the four candidates at most geometries. Both require a fourth capital at x ≈ 1587–1646 where there is no ink at all. Injection shows a true «ААРО» would score z = +7.12, rank 1 of 602, robustly across four typefaces — so this is a refutation, not a shrug. **«ААРО» = AARO receives no pixel support whatever**; a prompt-primed origin for that reading cannot be excluded and the geometry excludes the string.
> - **Verb.** Whole-line matching discriminates nothing (all candidates inside a 21-phrase null; a nonsense string wins). The only constraint is length: **«прослушано …» is refuted** (+3.8σ to +6.2σ too short), **«предупреждало …» is compatible** (+1.4σ to +3.1σ) and is the only one of the two that is. This is a length argument, not a reading; there is no glyph-level evidence for either verb.
>
> **Calibration for anyone re-testing.** On line 1 — known text, 2× line 2's amplitude — this machinery identifies only **4–5 of 19 individual letters** (mean rank 3.4/32), and applied to line 1's *known* lowercase ending «ие»/«ние»/«ение» it returns z = −0.98 … +0.54, rank 264–1191. **Lowercase endings are untestable here; capital endings are testable to about 2.5σ and no further.** Any future claimed reading of line 2 should be checked against the ink extent (445–1549), the character count (22 ± 2), the size ratio (0.86), and the three-capital terminal run before it is checked against a template.
>
> **Trap to avoid.** At the earlier (wrong) size of 64 px, «АА» scored z = +0.95 / rank 133 — nothing — and allowing free letter-spacing at that wrong size pushed «АА» to rank 3 and «ААР» to rank 2, which would have read as strong support for a three-letter ending. Fix the geometry independently before testing any string.
>
> Method note: the downscale-then-stretch enhancement (Lanczos ~70% + percentile stretch) was adopted and tested head-to-head against the registered-average + Gaussian-high-pass ladder on line 1. It changes r by <0.001 and the discrimination z by <0.05, and does not change glyph accuracy. It is a genuine improvement for human/VLM reading and no improvement at all for pixel measurement. Full report and scripts: `analysis/cyrillic/gen3/`.

---

## Artefacts

Scripts (all reproducible, python3.12) and images in `/home/user/new-skinny-bob/analysis/cyrillic/gen3/`:

- `core.py`, `prep.py` — data prep, estimators, template machinery
- `est_cmp.py`, `est_cmp2.py`, `fit1.py` — §1 estimator validation and typeface fit → `est_cmp.json`, `FIG_estimators.png`
- `extent.py`, `capband.py`, `capband2.py`, `l1sub.py`, `l1sub2.py`, `fullseg.py`, `tailseg.py`, `xheight.py`, `layout.py`, `layout_err.py`, `size2.py`, `size3.py`, `pitch.py` — §2 geometry
- `ends.py`, `ends2.py`, `final_ends.py`, `scan_tail.py`, `verb.py` — §3 candidate tests → `final_ends.json`, `verb.json`
- `power2.py`, `power3.py`, `power4.py`, `l1_ending.py` — §4 power and ground-truth calibration → `power3.json`, `power4.json`
- `figs.py`, `ruler.py` — figures

Key images: `FIG_estimators.png`, `FIG_overlays.png` (best-fit «АА» / «АТ» / «ААР» / «ААРО» outlines over the tail), `l2_tail_ruler.png`, `l2_head_ruler.png`, `l2_full_ruler.png`, `zoom_1390_1600.png`, `zoom_1140_1400.png`, `l2_before_l1sub.png`, `l2_after_l1sub.png`, `l1_residual.png`.