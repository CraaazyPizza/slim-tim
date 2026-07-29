# The hidden Cyrillic caption: the best single frame, the typeface, and line 2

Agent: Opus "cyr4", 2026-07-29. Scripts and artefacts in `analysis/cyrillic/` (reproducible, `python3.12`). Figures in `figs/cyrillic/`.

This supersedes specific numbers in `reports/agent_cyr3.md`, `reports/agent_cyrillic_line2.md`, FINDINGS §2 and §2a. It does not overturn their method; it overturns their **geometry**, and the geometry was carrying everything else.

---

## Bottom line

1. **The single best frame is f983.** Averaging is not "wrong" — the caption layer is registered to within 0.38 px, so it cannot be smeared — but it buys far less than it looks like it should (20 frames reduce the band noise by only 1.55×, not 4.5×, because the codec noise is correlated across frames), and the residual it leaves is low-frequency and blocky, which reads worse. **The owner's practical judgement was right. One good frame is the better picture and very nearly the better measurement.**

2. **The caption is not faint-and-mushy; it is low-contrast and SHARP.** Ink depth 11.9/255 luma levels in one frame against a band noise of 0.97 → per-pixel SNR ≈ 12. Edge-spread fit on the leading stem of «П» gives **σ = 0.9 ± 0.2 px**. The earlier record's best-fit template blur of σ = 5.0 px was not a PSF measurement; it was a wrong geometry being papered over.

3. **★ The caption layer is HORIZONTALLY STRETCHED by kx ≈ 1.3 ± 0.1.** Measured «П» aspect (ink width / cap height) = **1.036–1.060**; the widest upright sans-serif «П» among all 234 installed faces is 0.900 (DejaVu Sans Bold), and nothing upright and unslanted reaches 1.0 except monospace. Fit the known line-1 string isotropically (what every previous pass did) and no face on this machine beats r = 0.25; allow a free horizontal scale and the same fonts reach **r = 0.67–0.78**. This single fact invalidates every typeface number previously recorded for this caption, including the Roboto Medium claim.

4. **The typeface — see §10, which supersedes this item and §9.** On the free-stretch test used here, five unrelated bold grotesques sit within 4% of each other and the winner moves with the grid, so §3 concluded UNDETERMINED and withdrew Roboto Medium. **§10 then added a constraint that breaks the tie**: because the stretch multiplies stem width but not cap height, each face's own stroke weight predicts the stretch it must have, and only two candidates fit the image at the stretch their weight demands — **Roboto Medium (r = 0.727) and Inter at wght ≈ 600 (0.702)**, with every bold weight collapsing 71–80%. So the answer is a **two-candidate shortlist**, the weight is **medium not bold**, and kx = 1.25–1.36. The owner's scepticism about the original claim was still correct: it was never demonstrated by the test that made it.

5. **Line 2 reads «предупреждало об АА» plus one further capital-height glyph.** At the measured geometry with the left edge pinned to the measured ink start, that reading scores **z = +10.7 (f983) / +10.3 (5-frame)** against a null of 22 same-length Russian and nonsense phrases; the best null is +1.9 and the best score the same test achieves on caption-free frames is +3.8. **This is a much stronger result than the record's "≈2.7σ, consistent but not selected".** The identity of the final glyph is **undetermined**: Г (z +2.07) > П > Б > В > Р > С > Е, against a caption-free ceiling of +2.1…+3.4. A **fourth** terminal capital is still unsupported, so **«ААРО» / AARO remains refuted**.

6. **Line 1 is «Предыдущее сообщени» — the final «е» is not rendered.** Column energy against a caption-free null is 28× at x 1600–1614, 3.5× at 1615–1629 and ≈1× beyond; a final «е» would have to occupy x 1612–1658. Two verified clean-room Gemini reads transcribe it the same way. Small, but it is a correction to a line the record calls "confirmed, no caveats", and it establishes that the text layer has a right boundary at x ≈ 1615 — which is one of the three legs the AARO refutation now stands on.

7. **The VLM corroboration for line 2 was contamination, and a single VLM read is worth nothing here.** Run from the project directory, Gemini returns «предупреждало об ААР» — and its own text admits it read our documentation. Run in an empty directory with a neutral filename, verified to see only `a.png`, the same model on the same line-2 crop returns **«пріпvпіпхvшапо гб лле»**, **«пресупихимпо сббАле»** and **«преступников сб лдпр»** — the last with per-character confidences of 90–99%. Given both lines together at lower magnification the same clean-room setup does read «Предыдущее сообщени / предупреждало об АЛ-», so it is not blind; it is unstable. Seven readings, six answers. **The line-2 reading below rests on the matched filter alone and would stand if no VLM had ever been asked.**

---

## 1. Best single frame

Frames 910–1049, luma, normalised per frame, background = mean of the 112 caption-free frames in that range. Per-frame score = normalised cross-correlation of the line-1 band against the **leave-one-out** mean of the other caption frames (so a frame cannot score on its own noise), plus its regression amplitude and a Tenengrad gradient-energy ratio against a text-free band 22 px above the line.

| frame | r (LOO, line 1) | amplitude | gradient-energy ratio | r (LOO, line 2) |
|---|---|---|---|---|
| **983** | **0.8650** | **1.199** | 8.50 | **0.7413** |
| 973 | 0.8488 | 1.135 | 7.96 | 0.7117 |
| 974 | 0.8381 | 1.135 | 11.09 | 0.7306 |
| 984 | 0.8328 | 1.170 | 7.90 | 0.7295 |
| 981 | 0.8315 | 1.209 | 10.90 | 0.7049 |
| 982 | 0.8298 | 1.151 | 8.91 | 0.6789 |
| … | | | | |
| 975 | 0.4795 | 0.557 | 11.59 | 0.4483 |
| 976 | 0.3485 | 0.400 | 13.55 | 0.4303 |
| best frame **outside** f970–989 | 0.1045 (f1031) | 0.060 | 1.06 | 0.0377 |

**f983 is the best frame on both lines.** The caption block is f970–989 exactly, as the record says. f983 also has the highest single-frame ink depth (11.9/255 vs 9.85 for the 20-frame mean).

Figure: **`figs/cyrillic/FIG1_best_frame.png`** — f983 at native resolution, 2× nearest-neighbour and 2× Lanczos for both lines, the 20-frame average for comparison, and a caption-free control frame through the identical pipeline (it is blank, as it must be).

### 1.1 the owner's objection to averaging, tested rather than assumed

Two separate questions, and they have different answers.

*Does averaging smear a moving overlay?* **No — the overlay does not move.** Sub-pixel registration of each caption frame against the leave-one-out mean, using the column ink profile: **dx s.d. = 0.382 px, full range −1.11 … +0.82 px**. The same measurement on caption-free frames gives s.d. 12.1 px, which is what "no signal" looks like, so the 0.38 px figure is a real measurement and not a floor. Split-half agreement *rises* with the number of frames averaged (k=1: 0.883, k=3: 0.957, k=10: 0.968). Mechanically, averaging cannot be destroying letterform detail here.

*Is averaging therefore worth doing?* **Barely.** The band noise falls only from 0.97 to 0.63 levels for a 20× increase in frames — a factor 1.55 where independent noise would give 4.5 — because the AV1 residual is strongly correlated between frames in the same GOP. Meanwhile the amplitude dilutes from 1.199 (f983) to 1.000 (block mean). Net band SNR: **f983 ≈ 12.3, 20-frame stack ≈ 15.6.** A 27% gain, and the noise that survives is low-frequency and blocky, which the eye integrates much worse than the single frame's high-frequency grain. Panel D of FIG1 shows the stack is visibly *worse* to read than panel B.

**Conclusion: single-frame is primary throughout this report; a 5-frame best-of stack (f973/974/981/983/984) is used only as corroboration and is always labelled.** The record's 20-frame "matched" stack is reported alongside but is not the basis of any claim.

---

## 2. The measurements the typeface question actually turned on

### 2.1 Point spread function

Erf edge-spread fits on the flat-only residual (no high-pass, which would sharpen an x-edge artificially):

| edge | f983 | 5-frame |
|---|---|---|
| leading edge of «П» (x ≈ 448) | σ = 0.71 px | σ = 0.89 px |
| trailing edge of line 1 (x ≈ 1600) | σ = 2.03 px | σ = 0.55 px |

Adopted **σ = 0.9 ± 0.2 px**. The caption is essentially at native sharpness. (The Mk.5 overt burned-in caption elsewhere in the same video measures σ = 2.55 ± 1.14 px, and the photographed scene content ≈ 19 px FWHM — three different layers, three different sharpnesses, exactly as you would expect from a composite.)

### 2.2 Letterform metrics, straight off the pixels

50%-of-peak bounding boxes, agreeing across f983, the 5-frame stack and the 20-frame stack:

| quantity | f983 | 5-frame | 20-frame |
|---|---|---|---|
| «П» ink width | 54.2 px | 54.7 px | 54.6 px |
| **cap height** (cap top → baseline) | **52.3 px** | 52.7 px | 51.6 px |
| **«П» aspect = width / cap height** | **1.036** | **1.037** | **1.060** |
| stem width (FWHM) | 11.96 / 11.34 px | 12.00 / 11.32 | 12.07 / 11.37 |
| cap top y | 922.0 | 922.0 | 925.3 |
| baseline y | 974.3 | 974.7 | 976.8 |

The record's baseline of y = 985 is wrong by ~11 px, and its RobotoM-104 size implies a cap height of ~74 px against a measured 52.

### 2.3 Line 1 ends «…сообщени», not «…сообщение»

Per-column ink energy in the line-1 band divided by the same statistic on caption-free frames, 15-px bins:

| x | 1585–1599 | **1600–1614** | 1615–1629 | 1630–1644 | 1645–1659 | 1660+ |
|---|---|---|---|---|---|---|
| energy ratio | 10.4 | **27.9** | 3.5 | 2.0 | 1.1 | ≤ 1 |

Ink stops at x ≈ 1615. At the measured 58 px letter pitch a final «е» would occupy x ≈ 1612–1658 and it is not there. Independently, clean-room Gemini transcribed line 1 as **«Предыдущее сообщени»**. So the rendered string is 19 glyphs, and either the text layer was clipped at its right edge or the string itself was truncated. Either way, this is the first hard evidence that the caption layer has a right-hand boundary at x ≈ 1615 — which matters for line 2, below.

### 2.4 ★ The horizontal stretch

Measured «П» aspect is 1.036–1.060. Across all 234 installed Cyrillic-capable faces:

| face | «П» aspect | implied kx |
|---|---|---|
| Roboto Medium | 0.785 | 1.32 |
| Roboto Regular | 0.757 | 1.37 |
| DejaVu Sans Bold | 0.900 | 1.15 |
| Liberation Sans Bold / Arimo Bold | 0.854 / 0.900 | 1.21 / 1.15 |
| Lato Bold | 0.811 | 1.28 |
| Carlito Bold | 0.795 | 1.30 |
| Nimbus Sans Bold | 0.795 | 1.30 |
| **widest UPRIGHT SANS on the machine** — DejaVu Sans Bold | **0.900** | — |
| next widest upright sans — Cantarell Extra Bold / Liberation Sans Bold / Arimo Bold / Lato Black / Roboto Black | 0.870 / 0.854 / 0.850 / 0.845 / 0.836 | — |
| widest monospace — Nimbus Mono PS Bold | 0.994 | — |
| the only faces that reach 1.04 unaided are **italics and display serifs** (EB Garamond Italic 1.41, DejaVu Serif Bold 1.17) — both excluded by the letterforms and by the controls in §3.2 | | |

And directly, from the matched filter on the known line-1 string (**`figs/cyrillic/FIG3_stretch_evidence.png`**):

| face | r at kx = 1.00 (isotropic) | peak r | kx at peak | peak r on caption-free frames |
|---|---|---|---|---|
| Arimo Bold | 0.149 | **0.779** | 1.28 | 0.088 |
| Nimbus Sans Bold | 0.160 | **0.775** | 1.35 | 0.087 |
| Liberation Sans Bold | 0.190 | **0.775** | 1.28 | 0.091 |
| Roboto Medium | 0.113–0.120 | **0.753** | 1.40 | 0.078 |
| Carlito Bold | 0.094–0.125 | 0.724 | 1.37–1.40 | 0.084 |
| Lato Bold | 0.124–0.142 | 0.702 | 1.40 | 0.082 |
| DejaVu Sans Bold | 0.182–0.252 | 0.675 | 1.10–1.16 | 0.082 |
| Open Sans Semibold | 0.122 | 0.585 | 1.375 | 0.081 |
| Noto Sans Regular | 0.171 | 0.491 | 1.425 | 0.091 |

A 5–7× jump in correlation from one extra parameter, peaking in a consistent band. Two independent cross-checks:

- **The film picture itself is not stretched.** At f983 the picture occupies columns 225–1680 of 1920 and all 1080 rows: aspect 1.35, i.e. a 4:3 image pillarboxed inside a 16:9 frame. Whatever stretched the text did not stretch the image.
- **The overt Mk.5 caption in the same video is not stretched.** A separate pass measured kx = 1.03 ± 0.06 on «Mark 5 (1961 год» with the PSF held at its own measured value. So the stretch belongs to *this text layer*, not to the export.

Interpretation is open and I am not going to over-read it: the most economical explanation is that the hidden line was composited as an element that was scaled non-uniformly to fit a box (a resized screenshot or a stretched text layer). It is a production artefact, not a message.

**Consequence, stated plainly: every typeface score previously recorded for this caption — including `agent_cyr3.md`'s Roboto Medium r = 0.666 vs DejaVu 0.528 — was computed at kx = 1 and is a fit to the wrong shape. Those numbers should not be quoted again.**

---

## 3. THE TYPEFACE TEST

Font inventory: `fc-list :lang=ru` yields 292 entries; **234** render every glyph of «ПредыущсобнимеАРОТХЛДГЕ» and are non-`.notdef`. All 234 were tested. Nothing was installed.

Method: the known line-1 string is rendered, stretched horizontally by kx, blurred, and matched against the pixels with the same row-mean-removal and Gaussian high-pass applied to both observation and template (a legitimate matched filter). Free parameters per face: cap height, kx, PSF σ, x and y offset. Score = normalised cross-correlation over the line-1 window.

### 3.1 Stage A — all 234 faces, coarse grid, word 1, frame 983

Field median r = 0.472, s.d. 0.147.

| rank | face | r | cap | kx |
|---|---|---|---|---|
| 1 | Arimo Bold *(Arial Bold metric clone)* | 0.8143 | 55 | 1.25 |
| 2 | Go Bold | 0.8058 | 55 | 1.34 |
| 3 | Carlito Bold *(Calibri Bold metric clone)* | 0.7949 | 55 | 1.34 |
| 4 | **Roboto Medium** | **0.7892** | 52 | 1.43 |
| 5 | DejaVu Sans Bold | 0.7379 | 52 | 1.16 |
| 6 | Liberation Sans Bold *(Arial Bold clone)* | 0.7286 | 55 | 1.25 |
| 7 | Cantarell Bold | 0.7255 | 55 | 1.34 |
| 8 | Lato Heavy | 0.7204 | 55 | 1.34 |
| 9 | Roboto Condensed Medium | 0.7106 | 55 | 1.52 |
| 10 | Go Medium | 0.7101 | 52 | 1.43 |
| 11 | Roboto Bold | 0.7100 | 52 | 1.43 |
| 12 | Noto Sans Bold | 0.7066 | 52 | 1.34 |

Four unrelated designs within 3%. Every leader is a **bold or medium weight**; every regular weight of the same family scores lower (Roboto Regular 0.700 vs Roboto Medium 0.789; Arimo Regular 0.654 vs Arimo Bold 0.814). Weight is the one thing the pixels are clear about.

### 3.2 Stage B — full line, fine grid, several observations

Free PSF (σ grid 1.0–5.8):

| face | f983 | 5-frame | 20-frame | caption-free control |
|---|---|---|---|---|
| Arimo Bold | 0.7634 | **0.8138** | **0.7666** | 0.0827 |
| **Roboto Medium** | 0.7632 | 0.7950 | 0.7384 | 0.0771 |
| Go Bold | 0.7599 | 0.7790 | 0.7372 | 0.0796 |
| Nimbus Sans Bold *(Helvetica Bold clone)* | **0.7781** | 0.6973 | 0.6322 | — |
| Liberation Sans Bold | 0.7440 | 0.7392 | 0.6841 | 0.0738 |
| Carlito Bold | 0.7091 | 0.7510 | 0.6853 | 0.0831 |
| Lato Bold | 0.6922 | 0.7347 | 0.6675 | 0.0840 |
| DejaVu Sans Bold | 0.2848 † | 0.7069 | 0.6527 | 0.0756 |
| DejaVu Sans Book | 0.6355 | 0.6427 | 0.5885 | 0.0823 |
| Open Sans Semibold | 0.5733 | 0.5585 | 0.4890 | 0.0823 |
| Noto Sans Regular | 0.4946 | 0.4748 | 0.4223 | 0.0800 |
| Liberation Serif Bold *(control, should lose)* | 0.5054 | 0.5209 | 0.5121 | — |
| Nimbus Mono PS Bold *(control, should lose)* | 0.2000 | 0.2488 | 0.2149 | 0.0739 |

† DejaVu Sans Bold wants kx = 1.16, which fell outside the kx grid used for the f983 column. Flagged rather than hidden: **the grid choice moves this table by more than the noise does.** That is itself the result.

PSF held at the independently measured σ = 0.9 px (only cap height and kx fitted — the honest like-for-like comparison, and the one shown in FIG2b):

| face | f983 | 5-frame | caption-free control |
|---|---|---|---|
| Nimbus Sans Bold | **0.7361** | **0.7645** | 0.0682 |
| Arimo Bold | 0.7271 | 0.7474 | 0.0716 |
| Go Bold | 0.7197 | 0.7473 | 0.0661 |
| **Roboto Medium** | 0.7183 | 0.7397 | 0.0691 |
| Liberation Sans Bold | 0.7056 | 0.7319 | 0.0738 |
| Carlito Bold | 0.6660 | 0.6875 | 0.0670 |
| Lato Bold | 0.6473 | 0.6644 | 0.0648 |
| DejaVu Sans Bold | 0.6217 | 0.6431 | 0.0756 |
| Open Sans Semibold | 0.5248 | 0.5348 | 0.0754 |
| Noto Sans Regular | 0.4417 | 0.4500 | 0.0725 |
| Nimbus Mono PS Bold *(control)* | 0.2394 | 0.2635 | 0.0739 |

**Top five span 0.706–0.736 on the single frame and 0.732–0.765 on the 5-frame stack — a 4% spread across five unrelated designs — while the caption-free control sits at 0.065–0.076 for every face.** The fit is real (10× the null). The ranking is not.

### 3.3 Error bars

Frame bootstrap: 200 resamples of 10 of the 20 caption frames, each face's geometry held at its 5-frame best fit.

| face | mean r | s.d. | paired Δ vs Arimo Bold | ranked 1st |
|---|---|---|---|---|
| Arimo Bold | 0.7474 | 0.0408 | — | 200/200 |
| Roboto Medium | 0.7171 | 0.0429 | +0.0303 ± 0.0042 (7.1σ) | 0/200 |
| Go Bold | 0.7155 | 0.0391 | +0.0320 ± 0.0035 (9.1σ) | 0/200 |
| Carlito Bold | 0.6655 | 0.0441 | +0.0819 ± 0.0063 | 0/200 |
| Liberation Sans Bold | 0.6649 | 0.0420 | +0.0825 ± 0.0040 | 0/200 |
| Lato Bold | 0.6460 | 0.0442 | +0.1015 ± 0.0065 | 0/200 |
| DejaVu Sans Bold | 0.6346 | 0.0387 | +0.1128 ± 0.0053 | 0/200 |
| Nimbus Sans Bold | 0.6069 | 0.0444 | +0.1406 ± 0.0069 | 0/200 |

**Read this correctly.** The bootstrap says only that *frame noise* cannot flip the ranking at fixed geometry. It says nothing about geometry uncertainty — and geometry uncertainty is the dominant term: with the cap-height grid extended down to 50.5 px, Nimbus Sans Bold overtakes Arimo Bold on f983 and Arimo Bold falls to 2nd; at the fixed measured PSF, Nimbus Sans Bold is 1st on both real observations. A 7σ frame-bootstrap difference between two faces whose ordering swaps when you add a grid point is not evidence about the typeface. Quoting it as such would be exactly the error the previous pass made.

### 3.4 Faces that could NOT be tested

Not installed, so untested: **PT Sans / PT Sans Caption** (the owner asked specifically), the real Arial, the real Helvetica, Segoe UI, Inter, SF Pro, Fira Sans, Source Sans Pro, Ubuntu, Montserrat, Manrope, Golos Text, YS Text, Circe, Museo Sans, Graphik, Proxima Nova. Nothing was installed for this test, per instruction.

Note the top of the table is populated by **metric-compatible clones** — Arimo and Liberation Sans for Arial, Nimbus Sans for Helvetica, Carlito for Calibri. Clones match metrics and approximate outlines, so the table constrains the *design* (Arial/Helvetica-family neo-grotesque) better than it constrains the *file*.

### 3.5 Verdict

**TYPEFACE: UNDETERMINED.** Positively constrained:

- a **bold or medium weight** grotesque / neo-grotesque sans (every regular weight loses to its own bold);
- **cap height 52 ± 2 px**, stem width **11.6 ± 0.4 px** (stem/cap = 0.22, i.e. genuinely bold);
- **horizontally stretched by kx = 1.3 ± 0.1** relative to any real face;
- PSF σ = 0.9 ± 0.2 px;
- serif, monospace, geometric (Comfortaa, URW Gothic) and light/regular weights are excluded — the controls behave (Nimbus Mono PS Bold 0.24–0.26, Liberation Serif Bold 0.51 against a leader band of 0.73–0.77).

Not determined: which face. Nimbus Sans Bold, Arimo Bold, Go Bold, Roboto Medium and Liberation Sans Bold are statistically interchangeable at this SNR and at this stretch.

**`agent_cyr3.md`'s claim that the typeface is Roboto Medium is withdrawn.** It was measured at kx = 1, where Roboto Medium scores r ≈ 0.11 and *nothing* fits; and at the correct geometry Roboto Medium ranks 2nd to 4th depending on which frames and which grid you use. The owner's "I don't trust what u say the font is" was the right call.

Figures:
- **`figs/cyrillic/FIG2_typeface_proof.png`** — full line 1: real pixels (single frame, then 5-frame) above eleven candidate faces, each rendered at its own best-fit geometry, degraded through the measured pipeline (stretch → PSF blur → measured ink depth 11.9/255), **added to a real caption-free frame of the same video**, and put through an identical display pipeline. Glyph-aligned, same scale, same contrast stretch.
- **`figs/cyrillic/FIG2b_typeface_closeup.png`** — the same comparison zoomed to «едыдущ» at 3×, with the **PSF held at the measured σ = 0.9 px** so nothing is hidden by blur. This is the figure to look at. Roboto Medium, Arimo Bold, Nimbus Sans Bold and Go Bold are indistinguishable by eye, and their scores say the same thing.
- **`figs/cyrillic/FIG3_stretch_evidence.png`** — r against kx for five faces plus the caption-free control, showing the collapse at kx = 1.

---

## 4. LINE 2

### 4.1 Geometry

| quantity | value |
|---|---|
| ink left edge | x = 439 (f983: 436) |
| baseline | y ≈ 1058 |
| cap height | 48 px (0.92 × line 1) |
| horizontal stretch | kx = 1.41 (line 1: 1.28–1.45) |
| two terminal «А» | x ≈ 1402–1472 and 1475–1521 |
| third terminal glyph | x ≈ 1526–1570 |
| ink end | x ≈ 1570 |

### 4.2 Whole-phrase test, left edge pinned

The template's ink-left is pinned to the measured x = 439 and may slide only ±8 px, so a candidate cannot buy its score by translating. Null: 22 same-length strings — 14 plausible Russian notification phrases and 8 nonsense strings. Fonts Arimo Bold / Roboto Medium / Liberation Sans Bold, cap 46–48, kx 1.36–1.47.

| string | r (f983) | z (f983) | r (5-frame) | z (5-frame) | best-fit dx |
|---|---|---|---|---|---|
| **предупреждало об ААГ** | 0.5924 | **+10.72** | 0.6981 | **+10.33** | −2 |
| предупреждало об ААБ | 0.5913 | +10.69 | 0.6936 | +10.24 | −2 |
| предупреждало об ААЕ | 0.5899 | +10.66 | 0.6910 | +10.18 | −2 |
| предупреждало об ААР | 0.5894 | +10.65 | 0.6916 | +10.20 | −2 |
| предупреждало об АА | 0.5889 | +10.63 | 0.6915 | +10.19 | −2 |
| предупреждало об ААП | 0.5850 | +10.53 | 0.6954 | +10.28 | −2 |
| предупреждало об ААРС | 0.5825 | +10.47 | 0.6764 | +9.88 | −1 |
| предупреждало об ААРО | 0.5685 | +10.11 | 0.6685 | +9.71 | −1 |
| предупреждало об этом | 0.5038 | +8.44 | 0.5846 | +7.94 | −2 |
| предупреждало об утечке | 0.4970 | +8.27 | 0.5670 | +7.57 | −2 |
| предупреждало обо всем | 0.4645 | +7.43 | 0.5340 | +6.88 | −2 |
| прослушано об АА | 0.2023 | +0.68 | — | — | 0 |
| прослушано об ААРО | 0.1909 | +0.38 | — | — | −8 |
| *best of the 22 nulls* | 0.2439 | **+1.75** | 0.2972 | **+1.89** | −4 |
| *same test on a caption-free frame, best candidate* | — | **+3.84** | — | — | — |

Three things follow.

1. **«предупреждало об АА…» is settled.** z ≈ +10 on the single best frame, ~5× the best null and ~3× the ceiling the same test reaches on caption-free frames. The fit does not slide (dx = −2 px out of ±8 allowed). It beats the two grammatically-plausible decoys with the same 15-character prefix («об этом», «об утечке») by 2.2–2.4σ, so the ending is contributing, not just the verb.
2. **«прослушано» is refuted** (z +0.68 / +0.38, inside the null). The record already said this on length grounds; it now falls on shape.
3. **Whole-line matching cannot choose the final glyph** — all eight terminal variants sit within 0.6σ of each other, because one glyph in 23 barely moves a whole-line correlation. That needs a localised test.

### 4.3 The glyph after «АА»

Geometry fixed by the prefix fit. Score computed on a window covering **only** the third terminal cell (x 1526–1617), so the rest of the line cannot pay for it. All 29 Cyrillic capitals, all 32 lowercase, and eight punctuation marks were tested.

| rank | glyph | r (5-frame) | z | r (f983) | z | r (20-frame) | z |
|---|---|---|---|---|---|---|---|
| 1 | **Г** | 0.4191 | **+2.07** | 0.2780 | +1.75 | 0.4594 | +1.87 |
| 2 | П | 0.3928 | +1.86 | 0.2363 | +1.31 | 0.4078 | +1.48 |
| 3 | Б | 0.3584 | +1.58 | 0.2404 | +1.35 | 0.3910 | +1.35 |
| 4 | В | 0.3422 | +1.45 | 0.2183 | +1.12 | 0.3618 | +1.13 |
| 5 | **Р** | 0.3339 | +1.38 | 0.2174 | +1.11 | 0.3514 | +1.06 |
| 6 | С | 0.3335 | +1.38 | — | — | 0.3496 | +1.04 |
| 7 | Е | 0.3047 | +1.15 | 0.2081 | +1.02 | 0.3385 | +0.96 |
| 8–14 | Щ, Ш, Н, б, й, К, **О** | 0.274–0.303 | +0.90…+1.13 | | | | |
| — | *same test on caption-free frames, best glyph* | | **+2.06** and **+3.36** | | | | |

- **The glyph exists.** Its cap-band ink energy is 3.9–4.5× the caption-free level at x 1536–1540, against 28× for the neighbouring «А» leg at x 1520 — i.e. a real but noticeably lighter mark, which is what a thin-top-bar form like Г, or a fading right edge of the layer, would produce. (The `''` = "nothing" option in the ranking scores 0 by construction and its bottom placement is an artefact, not evidence; ignore it.)
- **Its identity is undetermined.** The best real candidate reaches z = +2.07 and the same test on caption-free frames reaches +2.06 and +3.36. Nothing here clears the noise ceiling.
- Shape class is constrained: a **capital-height stem-with-top-arm** form — Г / П / Б / В / Р / С / Е. «Р» is 5th, so **«об ААР» is live but not established**; «Г» is the single best-scoring candidate on all three real observations, which is a consistency worth recording and nothing more.
- A clean-room Gemini asked to describe the same region *purely as shapes*, with letters explicitly forbidden, called it "a thick vertical block with **three** horizontal segments extending to the right from its top, middle, and bottom" — i.e. an «Е», not a «Г» (§5.2). That disagrees with my ranking and is logged rather than reconciled: both are in the measured shape class, neither clears the noise ceiling.

### 4.4 A fourth terminal capital: still not there

A fourth capital at the measured 71 px stretched advance would occupy x ≈ 1607–1678. Beyond x ≈ 1580 the caption-free control itself is elevated (bright vignette plus AV1 block noise at the picture edge) and no glyph-shaped structure survives; the signal-to-control ratio in the cap band there is ≈ 1. In the pinned whole-line test the four-glyph endings score **below** the three-glyph endings on all three real observations (ААРС +10.47/+9.88, ААРО +10.11/+9.71 vs ААГ +10.72/+10.33). Combined with §2.3's finding that the layer's right boundary is at x ≈ 1615 on line 1:

**«ААРО» = AARO remains refuted, and «ААРС» with it.** The refutation now rests on three independent legs — no ink in the required cell, a lower pinned whole-line score than the 3-glyph endings, and a text-layer right boundary that leaves no room — rather than on the record's single z-score.

### 4.5 Reconciling with the record

The two positions can now both be given their due.

- **The owner and the outside analyst were right about the reading.** «предупреждало об АА…» is not "weakly supported at ≈2.7σ"; at the corrected geometry it is a ~10σ result on a single frame. `agent_cyr3.md` was measuring a template that was 30% too narrow per glyph and 40% too tall, at a blur of σ = 5 that erased what letterform information there was. Its conservatism was not excessive caution; it was a geometry error producing a weak fit, which then looked like weak evidence.
- **`agent_cyr3.md` was right about the last letter, and about AARO.** Its "only the last letter is uncertain" and the owner's own phrasing agree exactly with the measurement here: the final glyph is present, it is capital-height, it is not identifiable, and it is not the second of a «РО» pair.
- The record's "line 2 is 22.2 ± 2.4 characters, so «предупреждало об АА» is 3σ short" **dissolves**: that length calibration inherited the isotropic geometry. At the measured geometry, «предупреждало об АА» + one glyph spans x 439 → ~1570, which is what the ink does.

Figure: **`figs/cyrillic/FIG4_line2.png`** — line 2 from f983 and the 5-frame stack, the pinned template at the same scale and position, a caption-free control, then the tail at 6× with two-glyph and three-glyph templates for comparison, and the ranked candidate list burned in.

---

## 5. Gemini as an independent reader — and why it is not one

`reports/agent_cyrillic_line2.md` established that VLMs generate grammatically-plausible Russian here from no pixel evidence. This pass adds a second, worse failure mode.

### 5.1 Contaminated runs (Gemini launched from the project directory)

Verbatim, non-leading prompt "Transcribe exactly the text visible in this image":

> предупреждало об ААР

Verbatim, "What characters can you see in this image? List them left to right":

> … 16. **А** (?) — Uppercase, large triangular/pointed shape class (А/Л/Д). 17. **А** (?) — Second uppercase triangular/pointed shape. 18. **Г** (?) / **Р** (?) / **-** (?) — A very faint, partial vertical stem/smudge at the far-right boundary, indicating a final cut-off capital-height character or hyphen.
> **Synthesized reading:** `предупреждало об АА...` (with high uncertainty for individual letterforms due to pixel degradation and horizontal compression artifacts, **which have been statistically analyzed in the project's verification reports**).

That last clause is the tell: it had read our files. A second contaminated run on the same image returned something else entirely:

> ```text
> препутуваме соб АЛЕ
> ```
> … 15. **А** … 16. **Л** … 17. **Е** — Capital Cyrillic Ie (`Е`), visible as a vertical stem with top, middle, and bottom horizontal arms extending right.

Three runs, three different answers, one of which cites our own documentation. None of this is admissible.

### 5.2 Clean-room runs

Empty directory, neutral filename `a.png`, `GEMINI_CLI_IDE_WORKSPACE_PATH` / `_SERVER_PORT` / `_AUTH_TOKEN` unset. Verified before trusting anything — asked to list every file it could see, the entire reply was:

> a.png

**On the line-2-only crop at 3× (image A), three phrasings, three answers, all wrong:**

> **"Transcribe ALL text visible in this image exactly as it appears… write [?] for the illegible part."**
> `пріпvпіпхvшапо гб лле`

> **"What writing, if any, is in this image? If you can read it, write it out. If you cannot, say you cannot."**
> The writing in the image is: `пресупихимпо сббАле`

> **"List the characters you can see, left to right, and give a confidence for each."**
> Based on the image **a.png**, the text consists of three Russian words/abbreviations written in Cyrillic characters from left to right: **преступников сб лдпр** (meaning *"criminals sb ldpr"*).
> … 1. **п** — **99%** 2. **р** — **99%** 3. **е** — **99%** 4. **с** — **98%** 5. **т** — **98%** … 15. **л** — **95%** 16. **д** — **96%** 17. **п** — **94%** 18. **р** — **90%** *(slightly blurred at the rightmost edge, but clearly recognizable in context)*

That third one is the most instructive object in this report: a completely fabricated reading, delivered with per-character confidences of 90–99%, on an image where the *same model in the same configuration* had just produced two different strings.

**But — and this matters — on the two-line crop at 2× (image B) the clean-room read is essentially correct:**

> **"Transcribe ALL text visible in this image exactly as it appears, line by line. Do not interpret or summarise."**
> Предыдущее сообщени
> предупреждало об АЛ-

And on line 1 alone (image D):

> Предыдущее сообщени

So the clean-room setup is not broken and the model is not simply blind here: given the two lines together, at lower magnification, it recovers line 1 exactly — **including the missing final «е», which is an independent corroboration of §2.3** — and gets line 2 to within one glyph. Given the line-2 crop alone it collapses into confident nonsense. That is a statement about how little margin there is, not a licence to average the answers.

**The shape-only question was the most useful thing it did.** Asked to describe the right-hand end of the tail purely as shapes, with letters explicitly forbidden:

> * **Second shape from the right:** An arch or inverted U-shape, formed by two thick, upward-slanted paths meeting at a rounded apex, leaving a light, hollow interior.
> * **Far-right shape:** A thick vertical block with **three horizontal segments extending to the right from its top, middle, and bottom**.

The first is an А/Л. The second, read literally, is a **«Е»** (or «В») rather than a «Г» — one arm versus three. That is a genuine, non-lexical observation from an independent reader and it disagrees with my own ranking, where Г leads and Е is 7th. Both are in the same measured shape class and neither clears the noise ceiling, so this does not settle anything; it is logged as a reason to keep Е live alongside Г, П, Б, В and Р.

**One more clean-room answer worth keeping.** Asked what typeface the line-1 lettering most resembles, with no mention of stretching:

> **1. Letter Gothic (Bold/Condensed Cyrillic)** — "…highly condensed proportions, vertical shapes, and very clean horizontal terminals…"
> **2. Lucida Console (Cyrillic)** — "…designed with an exceptionally high x-height and short ascenders/descenders…"
> **3. Soviet Teleprinter / Hardware Font (e.g. Robotron, Elektronika, or CP866 Telex Font)** — "…custom, highly simplified, blocky sans-serif monospaced fonts…"

All three guesses are **monospaced or condensed** faces, and the reasoning it gives is about *proportions being abnormal*. That is a non-lexical, independent observation pointing at the same thing §2.4 measures: a proportional face stretched 1.3× horizontally reads as monospace-like. (Its specific claim that the descenders are "eliminated or flattened" is wrong — «р», «у», «д», «щ» all have visible descenders in FIG1 — so this is corroboration of the *proportion anomaly*, not of any named font. None of the three are installed and none could be tested.)

**Conclusion on Gemini.** Four readings of line 2 from the project directory and three more from a clean room produced: «предупреждало об ААР», «препутуваме соб АЛЕ», «пріпvпіпхvшапо гб лле», «пресупихимпо сббАле», «преступников сб лдпр» (at 90–99% claimed confidence) and «предупреждало об АЛ-». **Any single VLM read of this caption is worth nothing** — including our own earlier record's, and including the ChatGPT/Gemini screenshot reads that FINDINGS §2 records as the owner's attestation. What survives is (a) the fact that the *shape envelope* is consistently recovered, and (b) the two clean-room reads of line 1, which agree with the pixels. **The line-2 reading in §4 rests entirely on the matched filter and its nulls, and would stand if no VLM had ever been asked.**

One more honesty note, since it cuts the same way: **my own eye is not an independent witness either.** I read FINDINGS before looking at the pixels and I read «предупреждало» out of the image immediately. The statistics are the only clean witness in this report, which is why §4 is built on pinned templates and 22 nulls rather than on what the enhanced crop looks like.

---

## 6. The Mk.5 caption (delegated pass, verbatim results retained)

Best single frame **f2655** (leave-one-out NCC 0.9564, rank 1 of 146 frames swept in f2560–2705; caption present f2603–~2698).

**Settled:** «Mark 5 (1961 год» is certain glyph by glyph; there is **no closing parenthesis** after «год» (checked to x = 1750); the caption occupies the **identical screen bounding box as the clip's routine burned-in timecode** `T6-02/31 00:57:xx`, proven by cropping the same pixel box in a caption-off frame (f2701) and a caption-on frame (f2655); the caption's own PSF is σ = 2.55 ± 1.14 px; **kx = 1.03 ± 0.06, i.e. no anamorphic stretch**; the ink in the ambiguous left zone starts at x ≈ 254–266 and is **not** clipped by the frame edge.

**Undetermined:** whether «Самолет» — or any specific word — precedes «Mark». Real pixel change occurs there when the caption switches on, but it is co-located with the timecode digits and cannot be resolved into letters. **FINDINGS §2b's «Самолет» is not confirmed by measurement** and should be marked as a guess. Also undetermined: the typeface (best candidate DejaVu Sans Condensed r = 0.616, next eight within 0.05, and a CJK font ties within noise — a clean demonstration that the correlation is responding to generic sans proportions, not identity).

Gemini on this caption, isolated directory, with «Mark» cropped out of the image so it could not anchor: it invented a fourteen-character Cyrillic phrase and a citation to "project documentation" that does not exist. Same failure mode as §5.

Figures: `figs/cyrillic/mk5_f2655_native.png`, `mk5_f2655_upscaled_NN.png`, `mk5_f2655_upscaled_Lanczos.png`, `mk5_f2655_context.png`, `mk5_reading_annotated.png`, `mk5_confound_diagnostic.png`, `mk5_excess_ink_profile.png`, `mk5_typeface_scores.png`. Scripts in `analysis/cyrillic/mk5-captions/`.

---

## 7. SETTLED vs UNDETERMINED

**SETTLED**

| | |
|---|---|
| Best single frame | **f983** (LOO r = 0.865 line 1, 0.741 line 2; block = f970–989) |
| The caption layer is static | horizontal drift s.d. **0.38 px** across the block (null 12.1 px) |
| Averaging is legitimate but nearly pointless | 20 frames cut the noise 1.55×, not 4.5×; SNR 12.3 → 15.6 |
| The caption is sharp, not mushy | PSF **σ = 0.9 ± 0.2 px**; ink depth 11.9/255; per-pixel SNR ≈ 12 in one frame |
| Cap height, stem, baseline | **52 ± 2 px**, **11.6 ± 0.4 px**, **y ≈ 974** (line 1) |
| **The text layer is horizontally stretched** | **kx = 1.3 ± 0.1**; «П» aspect 1.04–1.06 vs a maximum of 0.900 across all 234 installed upright sans faces; r goes 0.11 → 0.75 for the same font |
| The stretch is local to this layer | film picture is 4:3 pillarboxed; the Mk.5 overt caption measures kx = 1.03 ± 0.06 |
| Weight | bold / medium; every regular weight loses to its own bold |
| Line 1 | **«Предыдущее сообщени»** — the final «е» is not rendered; layer right boundary x ≈ 1615. Independently corroborated by a verified clean-room Gemini read |
| Line 2 reading | **«предупреждало об АА» + one more capital-height glyph**, z ≈ **+10** vs 22 nulls, left edge pinned, on the single best frame |
| «прослушано» | refuted on shape as well as length (z +0.68, inside the null) |
| «ААРО» / «ААРС» (AARO) | **refuted** — no ink in the fourth cell, lower pinned score than the 3-glyph endings, no room before the layer boundary |
| Mk.5 caption | «Mark 5 (1961 год» certain; no closing bracket; shares the timecode's bounding box; no stretch |

**UNDETERMINED**

| | |
|---|---|
| **The typeface** | five unrelated bold grotesques within 4% (Nimbus Sans Bold, Arimo Bold, Go Bold, Roboto Medium, Liberation Sans Bold); winner flips with the grid and with the frame set. **Roboto Medium withdrawn.** PT Sans and the real Arial / Helvetica / Segoe UI / Inter could not be tested — not installed |
| The glyph after «АА» | present, capital-height, stem-with-top-arm class. Г (+2.07) > П > Б > В > Р > С > Е, against a caption-free ceiling of +2.1…+3.4. «об ААР» live, not established. A clean-room shape-only VLM description favours Е (three arms) over Г (one) — logged, not resolved |
| Why the layer is stretched | production artefact of some kind; the specific mechanism is not identified and should not be guessed at |
| «Самолет» on the Mk.5 caption | not confirmed; entangled with the co-located timecode |
| The Mk.5 typeface | undetermined; a CJK face ties the winner within noise |

**A null is a null.** The typeface cannot be named from these pixels with the fonts on this machine, and saying so is the result. If the owner wants the font question closed, the productive next step is not more correlation — it is installing the Russian-market UI faces that are missing (PT Sans, Golos Text, YS Text, Circe, Inter, Fira Sans) and re-running §3.2, which now takes about two minutes per face because the geometry is finally right.

---

## Artefacts

`analysis/cyrillic/`: `c4.py` (data + estimators), `fast.py` (Fourier matched filter — the whole preprocessing chain and the PSF are applied as transfer functions, so the blur sweep is nearly free), `best.py` / `drift.py` (frame selection, registration, split-half), `psf.py` / `psf2.py` (edge-spread), `metrics.py` / `metrics2.py` / `vmet2.py` / `glyphbox.py` (letterform metrics), `fonts.py` (font inventory), `sweepA.py` (all 234 faces), `stageB.py` / `stageB2.py` / `fixpsf.py` (shortlist, several observations, fixed-PSF refit), `kx2.py` (stretch curves), `boot.py` (frame bootstrap), `l2fit.py` / `l2pin.py` / `l2last.py` / `l2phrase.py` (line 2), `figs4.py` / `fig2.py` / `fig2b.py` / `fig3.py` / `fig4.py` (figures), `enh.py` / `figlib.py` (display helpers). JSON results alongside each.

Clean-room Gemini transcript: `/tmp/vq/clean_answers.txt` (copy the file if it matters — `/tmp` is not durable). Contaminated transcript retained for the record at `analysis/cyrillic/second-opinion/answers.txt`.

---

## 8. Proposed replacement text for FINDINGS §2 / §2a

> **Line 1 — «Предыдущее сообщени»** ("Previous message", with the final «е» not rendered). Measured on video 1 frame 983, the sharpest of the twenty caption frames f970–989 (leave-one-out r = 0.865; best frame outside the block 0.10). Ink x 447.9–1615, cap top y 922, baseline y 974, cap height 52 ± 2 px, stem 11.6 px, PSF σ = 0.9 ± 0.2 px, ink depth 11.9/255 in one frame. The layer's right boundary is x ≈ 1615: column energy against caption-free nulls is 28× at x 1600–1614, 3.5× at 1615–1629 and ≈1× beyond, so a final «е» at x 1612–1658 is absent.
>
> **★ The text layer is horizontally stretched by kx = 1.3 ± 0.1.** Measured «П» aspect (ink width / cap height) is 1.036–1.060; the widest upright sans «П» among the 234 installed faces is 0.900 (DejaVu Sans Bold). Fitted isotropically, no face on the machine beats r = 0.25 on the known line-1 string; with a free horizontal scale the same fonts reach r = 0.67–0.78. **Every typeface number previously recorded for this caption was computed at kx = 1 and is void, including the "Roboto Medium r = 0.666 vs DejaVu 0.528" result.** The film picture is 4:3 pillarboxed inside the 16:9 frame and the overt Mk.5 caption measures kx = 1.03 ± 0.06, so the stretch belongs to this text layer, not to the export.
>
> **Typeface — UNDETERMINED, and this replaces the Roboto Medium claim.** All 234 installed Cyrillic-capable faces were fitted with free cap height, horizontal stretch, PSF and position. At the measured PSF the top five are Nimbus Sans Bold 0.765, Arimo Bold 0.747, Go Bold 0.747, Roboto Medium 0.740, Liberation Sans Bold 0.732 (5-frame; caption-free controls give 0.065–0.076 for every face). The winner flips between Nimbus Sans Bold and Arimo Bold depending on the cap-height grid and the frame set, so the 200-resample frame bootstrap that shows Arimo Bold ahead of Roboto Medium at 7σ must not be quoted as a typeface result. What is determined: a **bold-weight neo-grotesque sans**, cap 52 px, stem 11.6 px (stem/cap 0.22), stretched ~1.3× horizontally. Serif, monospace, geometric and light/regular weights are excluded. PT Sans, the real Arial and Helvetica, Segoe UI, Inter, Fira Sans, Golos Text and YS Text are **not installed and were not tested**.
>
> **Line 2 — «предупреждало об АА» + one further capital-height glyph.** Measured at the corrected geometry (ink left x 439, baseline y 1058, cap 48 px, kx 1.41). With the template's left edge pinned to the measured ink start and free to slide only ±8 px, the reading scores **z = +10.7 on frame 983** and **+10.3 on a 5-frame stack** against a null of 22 same-length Russian and nonsense phrases (best null +1.9; the same test on caption-free frames reaches at most +3.8). It beats the same prefix with the decoy endings «об этом» (+8.4) and «об утечке» (+8.3) by more than 2σ, so the ending is carrying signal and not just the verb. **«прослушано» is refuted** (z +0.68, inside the null). This supersedes §2a's "«об АА» weakly supported at ≈2.7σ", which was measured at kx = 1 with a σ = 5 px template blur.
>
> **The final glyph — present, not identified.** Its cap-band ink is 3.9–4.5× the caption-free level (against 28× for the adjacent «А» leg), so it exists. Scored on a window covering only its own cell: **Г +2.07 > П +1.86 > Б +1.58 > В +1.45 > Р +1.38 > С +1.38 > Е +1.15**, with О 14th. The same test on caption-free frames reaches +2.06 and +3.36, so nothing clears the noise. Shape class: capital-height stem-with-top-arm. **«об ААР» is live but not established.**
>
> **«ААРО» = AARO stays refuted**, now on three independent legs: no ink in the fourth cell (signal/control ≈ 1 there, in a region where the control is itself elevated by the picture-edge vignette); a *lower* pinned whole-line score than every three-glyph ending on all three observations; and the layer's right boundary at x ≈ 1615, established independently from line 1's missing final «е».
>
> **Method notes.** (a) The best single frame is f983 and single-frame reading is primary. The caption layer's horizontal drift across the block is 0.38 px, so averaging cannot smear it — but 20-frame averaging cuts the band noise only 1.55× (not 4.5×) because the AV1 residual is correlated between frames, and the amplitude dilutes, so the net SNR gain is 27% and the surviving noise is blocky and harder to read. (b) **Any single VLM read of this caption is worth nothing, and the earlier apparent corroboration was workspace contamination.** Launched from the project directory Gemini returns «предупреждало об ААР» *and cites "the project's verification reports"*; launched in an empty directory with a neutral filename, verified to see only the image, the same model on the same image returns «пріпvпіпхvшапо гб лле», «пресупихимпо сббАле» and «преступников сб лдпр» (the last with per-character confidences of 90-99%). Given the two lines together at lower magnification the same clean-room setup does read «Предыдущее сообщени / предупреждало об АЛ-», which corroborates the missing final «е»; and asked to describe the tail purely as shapes it reports an arch followed by a stem with three right-facing arms. Seven readings, six different answers. The reading above rests on the matched filter alone and would stand if no VLM had ever been asked. Full report: `reports/agent_cyr4.md`, scripts `analysis/cyrillic/`.

---

## 9. ADDENDUM (main session, 2026-07-29) — the missing fonts were installed and tested

§3.2 flagged that the Russian-market faces could not be tested because they were not on the
machine. Six were fetched and installed (`~/.local/share/fonts/cyr_test/`, fontconfig 234 →
244 faces with full coverage of the required glyph set): **PT Sans Bold**, **Fira Sans
Bold**, and variable **Inter**, **Golos Text**, **Rubik**, **Montserrat**.

**Method addition — the weight axis was set by measurement, not by the designer's label.**
The four variable faces were instanced at the weight whose rendered **stem/cap ratio matches
the measured 0.223**, sweeping `wght` in steps of 25 and measuring «П» at 200 px:

| face | wght chosen | stem/cap |
|---|---|---|
| Golos Text | 625 | 0.221 |
| Inter | 750 (opsz 16) | 0.219 |
| Montserrat | 675 | 0.218 |
| Rubik | 575 | 0.221 |
| Fira Sans (static Bold) | — | **0.237** |
| PT Sans (static Bold) | — | **0.196** |

This removes the weight-convention confound in §3.2's original table, where five different
designers' idea of "Bold" was being compared.

**Result — none of the new faces wins, and the conclusion is unchanged.** Fit at the measured
PSF σ = 0.9 px, free cap height and free `kx`, against the *known* line-1 string
«Предыдущее сообщение» (5-frame column; caption-free control in the last column):

| face | r (best5) | cap | kx | control |
|---|---|---|---|---|
| Nimbus Sans Bold | **0.7645** | 50 | 1.45 | 0.068 |
| Arimo Bold | 0.7474 | 52 | 1.30 | 0.072 |
| Go Bold | 0.7473 | 54 | 1.33 | 0.066 |
| Roboto Medium | 0.7397 | 54 | 1.36 | 0.069 |
| **Inter w750** | 0.7388 | 56 | 1.27 | 0.071 |
| Liberation Sans Bold | 0.7319 | 56 | 1.21 | 0.074 |
| **Rubik w575** | 0.7104 | 50 | 1.39 | 0.075 |
| **Montserrat w675** | 0.6826 | 54 | 1.18 | 0.070 |
| **PT Sans Bold** | 0.6824 | 52 | 1.51 | 0.069 |
| DejaVu Sans Bold | 0.6431 | 54 | 1.12 | 0.076 |
| **Golos Text w625** | 0.5901 | 50 | 1.39 | 0.076 |
| **Fira Sans Bold** | 0.5899 | 54 | 1.39 | 0.077 |

**What this buys.** The typeface stays **UNDETERMINED** — the top six still sit inside a ~4 %
band and the winner still moves with the cap grid and frame set, exactly as §3.2 reported.
But the negative is now properly bounded rather than merely unexplored:

- **PT Sans is refuted**, on two independent grounds. It scores 0.682, below every one of the
  original leaders, and it needs `kx = 1.51` to get there. Its stem/cap of **0.196** is well
  off the measured 0.223, so no weight of it fits. This matters because PT Sans is the
  obvious Russian-market guess and the owner asked for it specifically.
- **Golos Text and Fira Sans are clearly excluded** at 0.59 — barely above half the leaders'
  score, and Fira Sans is also too heavy at stem/cap 0.237.
- **Inter is the only new face that competes**, landing fifth at 0.7388, statistically
  indistinguishable from Roboto Medium's 0.7397. It joins the tie; it does not break it.
- Every control stays at 0.066–0.077 for every face, so the ~0.74 signal is unambiguous —
  what cannot be done is *attribute* it.

Still untested because they are proprietary and unobtainable here: the real **Arial**, real
**Helvetica**, **Segoe UI**, **SF Pro**, **Circe**, **YS Text**, **Proxima Nova**,
**Graphik**. Given that Arimo and Liberation Sans are metric-compatible Arial clones and both
land mid-table, a genuine Arial would be unlikely to separate either.

**Bottom line for publication:** a bold-weight neo-grotesque sans, cap 52 px, stem/cap 0.22,
stretched ~1.3× horizontally, and **not** PT Sans, Golos Text, Fira Sans, Montserrat, Rubik
or DejaVu. The face cannot be named from these pixels. That is the result.

Scripts: `analysis/cyrillic/mkinst.py` (weight instancing), `analysis/cyrillic/refit.py`
(the fit), results in `analysis/cyrillic/refit.json`.

---

## 10. ★ The stroke-weight constraint — which breaks the tie, and corrects §9

Added 2026-07-29 by the cyr4 agent, after the same six faces were installed. This section **does not replace §3**; it adds a constraint neither §3 nor §9 used, and that constraint changes the verdict. Where they disagree, this section wins and says why.

> **§9 above and this section reach different conclusions, and the difference is one specific error.** §9 instanced the variable faces at the weight whose stem/cap matches **0.223**, treating the measured ratio as the face's intrinsic ratio. It is not: 0.223 is the ratio **after** the horizontal stretch. Because the stretch multiplies stem width but leaves cap height alone, the intrinsic ratio of the true face is **0.2217 / kx** — around 0.17 at kx ≈ 1.3, not 0.22. Consequences:
> - §9's chosen weights (Inter 750, Golos 625, Montserrat 675, Rubik 575) are all roughly **30% too bold**, so its variable-font rows understate those families. Corrected, Inter peaks at **wght ≈ 600**, Golos at ≈ 500, Montserrat at ≈ 600, Rubik at ≈ 450.
> - §9's arguments of the form "its stem/cap of 0.196 is well off the measured 0.223, so no weight of it fits" (PT Sans) and "too heavy at 0.237" (Fira Sans) are **not valid as stated** — 0.196 is in fact almost exactly right for a face stretched by kx ≈ 1.13. Both faces do fail, but on the correlation at their predicted kx (§10.4), not on the raw ratio.
> - §9's bottom line, "a **bold-weight** neo-grotesque sans … stem/cap 0.22", is **superseded**: the intrinsic weight is **medium** (§10.5).
>
> Where §9 is right and this section agrees: none of the six new faces wins the free-kx test; every caption-free control sits at 0.066–0.077 for every face; and PT Sans, Fira Sans and Golos Text at bold weights are indeed excluded.

### 10.1 What was installed, and what is still missing

`~/.local/share/fonts/cyr_test/`, all verified to cover «ПАБВГРСЕТХЛДадеипрсуыщюёжбнмок»:

| face | type | axes |
|---|---|---|
| PT Sans Bold | static | — |
| Fira Sans Bold | static | — |
| Inter | variable | `opsz` 14–32, `wght` 100–900 |
| Golos Text | variable | `wght` 400–900 |
| Rubik | variable | `wght` 300–900 |
| Montserrat | variable | `wght` 100–900 |

fontconfig now reports 329 Cyrillic-capable entries. My inventory (full coverage of a 30-character test set, `.notdef` rejected) gives **241 static faces**; the four variable fonts were expanded into **125 instances** on a 25-unit weight grid (Inter at both optical sizes), giving **362 candidates, 361 measurable**.

**Still absent and untested, so the negative stays bounded:** the real **Arial**, the real **Helvetica**, **Segoe UI**, **Circe**, **YS Text**. Arimo and Liberation Sans are Arial *metric* clones and Nimbus Sans is a Helvetica clone — they match advance widths, but their stroke weights are their own drawings, so §9.4's exclusion of Arimo Bold is not strictly an exclusion of real Arial Bold.

### 10.2 The correction that has to come first

The measured ratio is **stem 11.64 px at cap height 52.5 px = 0.2217** (`realstem.py`, reproducing the coordinator's 0.223 with the identical construction, PSF-deconvolved). But that is the ratio **after** the stretch. The stretch acts on x only: cap height is a vertical measurement and is untouched, stem width is a horizontal measurement and is multiplied by kx. So

> intrinsic stem/cap of the true face = **0.2217 / kx**

Using 0.2217 directly against unstretched font metrics would have selected faces ~30% too bold. Handled correctly, this is better than a weight-matching recipe: **every candidate predicts its own kx from its own stroke weight**, `kx_pred = 0.2217 / (its intrinsic stem/cap)`, and the image fit then has to work at that kx. Weight and stretch are no longer independently adjustable. Uncertainty: ±4% on the ratio (threshold definition, PSF deconvolution, cap height) → **kx_pred ± 0.05**.

### 10.3 Unconstrained re-run — no new face wins, and the field is as degenerate as before

PSF fixed at the measured 0.9 px, free cap height, free kx, 5-frame observation:

| face | r (free kx) | kx | face | r (free kx) | kx |
|---|---|---|---|---|---|
| Arimo Bold | 0.7875 | 1.33 | Roboto Medium | 0.7397 | 1.36 |
| Liberation Sans Bold | 0.7846 | 1.33 | Rubik w625 | 0.7378 | 1.30 |
| Nimbus Sans Bold | 0.7645 | 1.45 | **Montserrat w750** | 0.7061 | 1.12 |
| **Inter w725 opsz14** | 0.7526 | 1.30 | **PT Sans Bold** | 0.6801 | 1.45 |
| **Inter w700 opsz14** | 0.7513 | 1.30 | **Golos Text w725** | 0.6163 | 1.27 |
| Go Bold | 0.7473 | 1.33 | **Fira Sans Bold** | 0.5899 | 1.48 |

Newly installed faces in bold. **None of them wins.** The leaders still span r = 0.74–0.79 across unrelated designs, exactly the degeneracy §3.2 reported. On the free-kx test alone, installing the six faces changed nothing — which is worth stating plainly, because it means the earlier UNDETERMINED verdict was not an artefact of a missing font.

### 10.4 The stroke-weight constraint — the bold faces are excluded

Same fits, but kx pinned to each face's own `kx_pred` (± the 0.05 uncertainty). Nothing else changes.

| face | intrinsic stem/cap | kx it must have | r free | **r constrained** | change |
|---|---|---|---|---|---|
| **Roboto Medium** | 0.1719 | **1.29** | 0.7397 | **0.7274** | **−1.7%** |
| **Inter w600 opsz14** | 0.1774 | **1.25** | 0.7019 | **0.7019** | **0%** |
| Inter w575 opsz14 | 0.1701 | 1.30 | 0.6808 | 0.6791 | −0.2% |
| Inter w550 opsz32 | 0.1615 | 1.37 | 0.6751 | 0.6533 | −3.2% |
| Rubik w450 | 0.1719 | 1.29 | — | 0.6031 | — |
| Montserrat w600 | 0.1839 | 1.21 | 0.6197 | 0.6022 | −2.8% |
| Open Sans Semibold | 0.1626 | 1.36 | 0.5480 | 0.5674 | +3.5% |
| Golos Text w500 | 0.1708 | 1.30 | 0.5639 | 0.5666 | +0.5% |
| Lato Semibold | 0.1632 | 1.36 | 0.6468 | 0.5190 | −19.8% |
| Arimo Bold | 0.2075 | 1.07 | 0.7875 | **0.2212** | **−71.9%** |
| Liberation Sans Bold | 0.2083 | 1.06 | 0.7846 | **0.2022** | **−74.2%** |
| PT Sans Bold | 0.1960 | 1.13 | 0.6801 | **0.1965** | **−71.1%** |
| Carlito Bold | 0.1989 | 1.11 | 0.6800 | **0.1874** | **−72.4%** |
| Nimbus Sans Bold | 0.2055 | 1.08 | 0.7645 | **0.1788** | **−76.6%** |
| Go Bold | 0.2073 | 1.07 | 0.7473 | **0.1590** | **−78.7%** |
| DejaVu Sans Bold | 0.2574 | 0.86 | 0.6580 | **0.1367** | **−79.2%** |
| Fira Sans Bold | 0.2362 | 0.94 | 0.5899 | **0.1156** | **−80.4%** |
| *caption-free control (f1010–1029), best of all 361 candidates* | | | **0.0887** | **0.0884** | |

Of 361 candidates, **45 pass the constraint** (|Δkx| ≤ 0.08) and **18 of those keep r > 0.5**. Identical conclusions on the single frame f983 (46 pass, 17 keep r > 0.5, same ordering).

Mechanically the reason is visible in the figure: a bold face needs only kx ≈ 1.07 to account for an 11.6 px stem, and at kx 1.07 the rendered line stops well short of the measured right-hand edge of the ink. It cannot be both bold enough and wide enough.

### 10.5 Verdict — the four-way tie is broken; the answer is a two-candidate shortlist

**Excluded** (fit only by adopting a stretch their own stroke weight contradicts, collapsing to 0.12–0.22 against a caption-free ceiling of 0.089): Arimo Bold, Liberation Sans Bold, Nimbus Sans Bold, Go Bold, Carlito Bold, DejaVu Sans Bold, **PT Sans Bold**, **Fira Sans Bold**, and every other bold weight tested.

**Survivors, in order:** Roboto Medium 0.7274 · Inter w600 0.7019 · Inter w575 0.6791 · Inter w550 0.6533 · Rubik w450 0.6031 · Montserrat w600 0.6022 · Open Sans Semibold 0.5674 · Golos Text w500 0.5666.

Margins measured against the ±0.03–0.05 grid/frame-set jitter characterised in §3.3:

| comparison | margin | in units of the jitter |
|---|---|---|
| Roboto Medium vs the excluded bolds | **+0.51** | **10–17×** — decisive |
| Roboto Medium vs the best other **static** survivor (Open Sans Semibold) | **+0.16** | **3–5×** — clear |
| Roboto Medium vs **Inter at weight 600** | **+0.026** | **0.5–0.9×** — **inside the jitter** |

So: **§3.5's withdrawal of Roboto Medium is itself partly withdrawn, and §9's "cannot be named, and it is bold" is superseded.** Roboto Medium is the single best-scoring candidate and is now the only *static* face that both fits the image and has the right stroke weight for the stretch it needs. But it is **not separated from Inter at weight 550–600**, and Inter is a Roboto-adjacent neo-grotesque, so this is a coherent shape class rather than a coincidence. The honest statement is a **two-candidate shortlist, not an identification**: the caption is set in Roboto Medium or in something very close to Inter at weight ~600, stretched horizontally by kx ≈ 1.25–1.36.

**§3.1, §3.5 and §9 also need one direct correction.** They concluded "every leader is a bold or medium weight; weight is the one thing the pixels are clear about". That was backwards. With kx free, a bolder face simply compensates with a larger stretch, so the free-kx test carries **no weight information at all** — which is why it filled its leaderboard with bolds. Under the constraint the survivors are **medium** weights (intrinsic stem/cap 0.15–0.19, i.e. wght ≈ 500–600), and every true bold is excluded.

### 10.6 A cross-check I attempted and could not use

I tried a second, independent kx estimator that never touches the stem or the cap height: in «о» the top and bottom arcs are horizontal strokes (thickness measured vertically, unaffected by the stretch) while the sides are vertical strokes (thickness measured horizontally, ∝ kx), so the measured side/arc ratio divided by a face's intrinsic side/arc ratio is kx.

**It does not work at this scale and I am not using it.** After PSF deconvolution the real «о» strokes are only 2–3 px, comparable to the PSF itself, and the three observations disagree wildly — side/arc = 0.851 (f983), 12.6 (5-frame), 0.713 (20-frame). Recorded so nobody repeats it. The stem constraint survives because the «П» stem is 11.6 px, comfortably above the PSF; the «о» strokes are not.

### 10.7 What could reopen this

1. **Synthetic emboldening.** If the compositor faux-bolded the text, the measured stem/cap would be inflated, every `kx_pred` would be too large, and the winner would shift back toward heavier faces — i.e. toward the very faces §10.4 excludes. Nothing in the pixels rules this out. This is the one systematic that could reverse §9.5 wholesale.
2. **The widening may not be a pure horizontal scale.** If it is a width axis, condensed/expanded designer drawing, or a tracking mechanism rather than a scale, the constraint is void. §2.4's evidence (r rising 5–7× at a consistent kx across unrelated faces) supports a scale but does not prove one.
3. **Variable faces get a free weight axis**, so their *ability* to satisfy the constraint is not evidence — only their r *at* the satisfying weight is. Roboto Medium satisfies it as a static face with nothing adjusted, which is a stronger form of the same statement, and is the main reason I put it ahead of Inter despite a margin inside the jitter.
4. **The faces still missing** (real Arial, real Helvetica, Segoe UI, SF Pro, Circe, YS Text, Proxima Nova, Graphik). Real Arial Bold's stroke weight is close to Arimo Bold's by design intent, so it would likely be excluded with it — but that is an inference, not a measurement. Note also that the surviving class is medium-weight, so the relevant untested instances are the **Regular/Medium** cuts of those families, not their Bolds.

### 10.8 Updated verdict lines

Replacing the corresponding rows of §7:

| | |
|---|---|
| **The typeface** — was UNDETERMINED across five faces | **now a two-candidate shortlist.** All bold weights are **excluded** by the stroke-weight constraint (they collapse 71–80%, to 0.12–0.22 against a 0.089 caption-free ceiling), including the newly installed **PT Sans Bold** and **Fira Sans Bold**. Survivors: **Roboto Medium (r = 0.727)** and **Inter at wght 550–600 (0.653–0.702)**, then Rubik w450, Montserrat w600, Open Sans Semibold, Golos Text w500 at 0.57–0.60. Roboto Medium beats the best other static survivor by 3–5× the jitter but beats Inter w600 by only 0.5–0.9× the jitter, so **it is the leading candidate, not an identification** |
| Weight | **medium, not bold** — intrinsic stem/cap 0.15–0.19 (wght ≈ 500–600). This reverses §3.1: the free-kx test had no weight information, because a bolder face just takes a larger stretch |
| Horizontal stretch | **kx = 1.25–1.36** for the surviving candidates, tightened from §2.4's 1.3 ± 0.1 and now cross-constrained by the stroke weight rather than free |
| Still untestable | real Arial, real Helvetica, Segoe UI, Circe, YS Text — not installed |

Figures: **`figs/cyrillic/FIG5_stem_constraint_best5.png`** (and `_f983.png`) — free-kx r against constrained r for all 361 candidates; self-consistent faces lie on the diagonal, the excluded bolds fall to the floor. **`figs/cyrillic/FIG6_stem_constrained.png`** — the same thing as pixels: each face forced to the kx its own stroke weight demands, where the failures are visibly too narrow to reach the measured edge of the ink. **`figs/cyrillic/FIG2b_typeface_closeup.png`** refreshed with all six new faces at free kx.

Scripts: `analysis/cyrillic/fonts2.py` (inventory), `fastvar.py` (variable-instance specs of the form `Inter.ttf#wght=575,opsz=14`, so every existing code path works on variable instances unchanged), `vfonts.py` + `realstem.py` (stem/cap measured identically on pixels and templates), `sweep3.py` (the 361-candidate free and constrained fits → `sweep3.json`), `stroke2.py` (the failed «о» cross-check), `fig5.py`, `fig6.py`.
