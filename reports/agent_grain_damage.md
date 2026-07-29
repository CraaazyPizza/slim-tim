# Agent report (verbatim): grain/damage cross-era comparison

Agent task ac8e3553cfa32828a, completed 2026-07-26. Final message verbatim:

---

All measurements complete. Here is the report.

## Setup and picture-area geometry (all rects are in decoded 1080p/480p pixel coords)

Picture (inside-gate) rects used throughout, derived from 60-frame temporal means (`meanmax_*.npy`, `mean_*.png`):

| video | era | frames | picture rect y0:y1, x0:x1 | matte rect sampled |
|---|---|---|---|---|
| OpSTlDJWFFI | 2026 | 2998 | 70:1010, 340:1570 | 300:1000, 40:270 |
| Oqw96jCOP7A | 2026 | 2503 | 70:1010, 350:1560 | 200:900, 60:280 |
| l9RAhmPHM_A | 2026 | 4395 | 90:990, 320:1580 | 300:1000, 30:280 |
| ZB788PtqQvg | 2011 | 1188 | 40:1010, 270:1690 | 300:1000, 40:190 |
| RsQCXN4o4Ps | 2011 | 1500 | 40:1000, 290:1660 | 300:1000, 40:210 |
| Xju_CY5ZESA | 2011 | 2598 | 60:1020, 300:1490 | 300:1000, 40:250 |
| a6TLGkrfNKI | 2011 | 2337 | 35:430, 10:630 | 200:400, 2:30 |

**Matte / dark-surround result first, because it kills one line of attack for everyone.** In the outside-gate matte, 8 consecutive frames at 45% through each video give spatial std / per-pixel temporal std (DN):

- Oqw96jCOP7A 0.054 / 0.004 (3 distinct values in the whole 230×1000 patch)
- OpSTlDJWFFI 0.397 / 0.160; l9RAhmPHM_A 0.349 / 0.132 (2 distinct values)
- ZB788PtqQvg 1.543 / 0.807; RsQCXN4o4Ps 0.937 / 0.478; a6TLGkrfNKI 3.050 / **0.000**

Row-coherent (scanline) structure in the matte peaks at ≤0.034 DN amplitude in every one of the seven. **There is no overlay grain layer and no scanline layer reaching into the matte in any video, 2011 or 2026.** This is not evidence of a shared pipeline: AV1 at YouTube rates codes a near-flat dark region as skip/DC and annihilates sub-DN noise there by construction. The matte channel is unusable as a discriminator. (a6TLGkrfNKI's 3.05 DN spatial std with exactly 0.000 temporal std is a static vignette gradient, not noise.)

---

## (A) Grain / noise power spectrum — verdict: **INDETERMINATE, consistent with SAME family, but the measurement is dominated by AV1**

Method: 256×256 flat patches (180×180 for 640×480 a6TLGkrfNKI), selected by lowest std of a σ=6 Gaussian-blurred copy within the picture rect. Noise isolated two ways: (i) single-frame high-pass `a − gauss(a,8)`; (ii) temporal difference `(f_{k+5} − f_k)/√2` then high-passed (isolates only the per-frame-varying component). Hanning-windowed 2D FFT, radially averaged into 64 bins.

Radially averaged power at 0.05 / 0.10 / 0.20 / 0.30 / 0.40 cyc/px, log-log slope over f∈[0.04,0.45], and autocorrelation half-width:

| video | era | patch | frame, rect | mean DN | P(.05) | P(.10) | P(.20) | P(.30) | P(.40) | slope | ACF hw px |
|---|---|---|---|---|---|---|---|---|---|---|---|
| OpSTlDJWFFI | 2026 | DARK | f01650 y582:838 x1236:1492 | 18.6 | 1.91 | 1.59e-1 | 2.85e-2 | 1.19e-2 | 5.7e-3 | **−2.58** | 3.52 |
| OpSTlDJWFFI | 2026 | BRIGHT | f02200 y300:556 x900:1156 | 174.8 | 11.8 | 3.70e-1 | 1.55e-2 | 5.5e-3 | 3.7e-3 | **−3.59** | 5.10 |
| Oqw96jCOP7A | 2026 | DARK | f00800 y646:902 x1246:1502 | 30.4 | 4.62e-1 | 5.41e-2 | 1.20e-2 | 3.5e-3 | 2.0e-3 | **−2.41** | 3.49 |
| Oqw96jCOP7A | 2026 | BRIGHT | f01900 y326:582 x414:670 | 151.1 | 1.10 | 1.01e-1 | 1.88e-2 | 5.3e-3 | 5.4e-3 | **−2.67** | 4.53 |
| l9RAhmPHM_A | 2026 | BRIGHT | f01098 y538:794 x640:896 | 123.6 | 1.83 | 8.45e-2 | 4.31e-2 | 9.5e-3 | 5.8e-3 | **−2.47** | 4.29 |
| ZB788PtqQvg | 2011 | DARK | f01009 y488:744 x462:718 | 18.2 | 1.03 | 8.01e-2 | 1.88e-2 | 5.1e-3 | 3.3e-3 | **−2.49** | 4.45 |
| ZB788PtqQvg | 2011 | BRIGHT | f00297 y104:360 x1102:1358 | 208.4 | 3.37 | 1.58e-1 | 3.01e-2 | 1.05e-2 | 6.2e-3 | **−2.58** | 5.05 |
| RsQCXN4o4Ps | 2011 | DARK | f01125 y488:744 x994:1250 | 22.1 | 4.87e-1 | 3.52e-2 | 7.4e-3 | 2.8e-3 | 1.9e-3 | **−2.71** | 3.75 |
| RsQCXN4o4Ps | 2011 | BRIGHT | f01275 y552:808 x1314:1570 | 118.4 | 1.64 | 2.33e-1 | 3.89e-2 | 9.9e-3 | 9.4e-3 | **−2.54** | 3.67 |
| Xju_CY5ZESA | 2011 | DARK | f02208 y60:316 x492:748 | 52.5 | 2.39e-1 | 2.85e-2 | 5.8e-3 | 1.7e-3 | 9.0e-4 | **−2.59** | 2.72 |
| a6TLGkrfNKI | 2011 | DARK | f01986 y60:240 x340:520 | 89.8 | 3.41 | 2.70e-1 | 6.81e-2 | 2.22e-2 | 1.9e-2 | **−2.40** | 8.87 |

Slope summary (clean flat patches only): 2026 median **−2.58**, range −3.59…−2.41 (n=5). 2011 median **−2.55**, range −2.71…−2.40 (n=6). ACF half-width: 2026 median 4.29 px, 2011 median 3.75 px (excluding a6TLGkrfNKI, whose 8.87 px is in its native 640-wide grid and not comparable). Temporal-difference spectra give the same slopes to within ±0.15 in every case where the shot is static enough (e.g. ZB DARK hp8 −2.49 vs td5 −2.45; Rs BRIGHT −2.54 vs −2.50; OpST DARK −2.58 vs −2.58).

Band-limited noise amplitude vs luminance (band = gauss σ1.2 − gauss σ6, ≈0.08–0.4 cyc/px, low-gradient pixels only, 5–6 frames per video), in DN:

| video | era | 10–25 | 25–45 | 45–70 | 70–100 | 100–135 | 135–175 | 175–215 |
|---|---|---|---|---|---|---|---|---|
| OpSTlDJWFFI | 2026 | 0.274 | 0.452 | 0.707 | 0.834 | **0.984** | 0.318 | 0.200 |
| Oqw96jCOP7A | 2026 | 0.223 | 0.532 | 0.804 | 1.231 | **1.965** | 1.711 | 1.664 |
| l9RAhmPHM_A | 2026 | – | 0.304 | **0.956** | 0.892 | 0.665 | 0.864 | 0.890 |
| ZB788PtqQvg | 2011 | 0.332 | 0.446 | 0.557 | 0.621 | **1.288** | 0.853 | 0.806 |
| RsQCXN4o4Ps | 2011 | 0.314 | 0.540 | **1.139** | 1.005 | 0.347 | – | – |

Same shape in both eras: rise from shadows, mid-tone peak around 100–135 DN (or 45–70 for the darker-graded RsQCXN4o4Ps / l9RAhmPHM_A), then fall. Peak amplitude 0.96–1.97 DN (2026) vs 1.14–1.29 DN (2011).

**Interpretation and limits.** Every number here — slope near −2.5, ACF half-width 3–5 px, sub-2-DN amplitude, mid-tone peak — is what an AV1 re-encode at YouTube 1080p rates produces from *any* soft, low-detail source, because the encoder's own reconstruction blur sets the roll-off. Direct evidence for this: with a σ=2 rather than σ=8 high-pass, all seven collapse to slope −1.1 to −1.4 and ACF half-width 0.66–0.81 px, i.e. the residual at fine scales is quantization dither, not grain. The genuine per-pixel noise floor in the picture area is 0.09–0.40 DN (σ=2 high-pass, low-gradient mask) for six of seven videos. **At this amplitude any original grain differences have been erased.** I cannot separate 2011 from 2026 on spectrum shape and I would not trust anyone who claims to. Two smaller caveats: a6TLGkrfNKI is 640×480 so its spatial frequencies are not on the same scale as the others; Xju_CY5ZESA is text-only and its picture-area statistics are contaminated by glyph edges (its σ=8 high-pass std is 0.36 DN but its raw top-hat peaks reach 260 DN, all text).

---

## (B) Static vs unique-per-frame grain — verdict: **no loop in either era; a clear temporal-cadence DIFFERENCE between eras**

### B1. Loop search
192×192 patch at picture centre, spans of 1000–1940 consecutive frames per video (e.g. OpSTlDJWFFI 1040–2900, N=1861, rect y444:636 x859:1051; ZB788PtqQvg 60–1150, N=1091, rect y429:621 x884:1076). Two noise channels: HP2 = `f − gauss(f,2)`; TRES = `f_i − ½(f_{i−1}+f_{i+1})` then σ=8 high-passed, which annihilates all static content including static edges. Frames unit-normalized, full Gram matrix, mean/median/p99/max NCC read off every off-diagonal for lags 1…900. Sharp-spike statistic = mean-NCC minus a ±25-lag running median, z-scored on the MAD.

Baseline mean-NCC beyond lag 30, and the largest isolated spike found:

| video | era | HP2 baseline (MAD) | HP2 top spike | TRES baseline (MAD) | TRES top spike |
|---|---|---|---|---|---|
| OpSTlDJWFFI | 2026 | +0.00124 (0.00115) | k=27, z=5.6 | −0.00004 (0.00133) | k=14, z=4.0 |
| Oqw96jCOP7A | 2026 | +0.00155 (0.00127) | k=140, z=3.4 | −0.000002 (0.00125) | k=13, z=3.6 |
| l9RAhmPHM_A | 2026 | — (0.00088) | k=810, z=3.5 | — (0.00149) | k=17, z=3.3 |
| ZB788PtqQvg | 2011 | +0.00152 (0.00139) | k=186, z=4.5 | +0.00001 (0.00294) | k=823, z=4.1 |
| RsQCXN4o4Ps | 2011 | +0.00048 (0.00116) | k=190, z=4.1 | +0.00002 (0.00158) | k=15, z=37 † |
| Xju_CY5ZESA | 2011 | degenerate ‡ | — | (0.01031) | k=15, z=41.5 † |
| a6TLGkrfNKI | 2011 | degenerate ‡ | — | — | odd lags † |

† not a loop — see B2; ‡ 474/900 and 24/900 lags contain bit-identical frame pairs because these videos hold static graphics for hundreds of frames, so the MAD collapses to 0 and the statistic is meaningless.

**No video in either era contains a grain loop.** The elevated lags that do appear (k=26–42 in OpSTlDJWFFI/Oqw96jCOP7A/ZB788PtqQvg/RsQCXN4o4Ps) form a smooth contiguous block continuous with the lag-1 decay tail, which is shot-length autocorrelation of the *content*, not a period. There is no isolated spike and no harmonic series anywhere in lags 1–900 (≈30 s at 29.97 fps, 36 s at 25 fps). The controlled TRES channel, which cannot see static content at all, has baselines of |0.00004| or less with MAD 0.0012–0.0030 and no spike above z=4.1 in any non-degenerate video. The maximum single-pair NCC of exactly 1.000 seen in RsQCXN4o4Ps at k=31–47 and in l9RAhmPHM_A at k=1–12 is bit-identical *freeze runs* (long held frames), not a loop: it appears at every lag inside the freeze, not at one period.

For completeness: HP2 mean-NCC at lag 1 → lag 10 is 0.42→0.033 (OpSTlDJWFFI), 0.42→0.033 (Oqw96jCOP7A), 0.44→0.029 (l9RAhmPHM_A), 0.47→0.033 (ZB788PtqQvg), 0.61→0.185 (RsQCXN4o4Ps, very static shots), 0.997→0.970 (Xju_CY5ZESA), 0.978→0.952 (a6TLGkrfNKI).

### B2. The one place the two eras genuinely diverge — frame cadence
Per-frame mean absolute difference computed over the whole picture area for every consecutive pair of all 7 videos (`fulldiff_*.npy`, ×4-downsampled). Restricted to live-action content spans:

| video | era | content span | frac pairs with diff < 0.05 DN | freeze-indicator autocorr lag1 | lag2 |
|---|---|---|---|---|---|
| OpSTlDJWFFI | 2026 | 1040–2900 | **0.013** | −0.013 | −0.013 |
| Oqw96jCOP7A | 2026 | 460–2400 | **0.017** | −0.018 | −0.018 |
| l9RAhmPHM_A | 2026 | 700–4300 | **0.021** | −0.008 | +0.020 |
| ZB788PtqQvg | 2011 | 60–1150 | **0.450** | **−0.785** | **+0.561** |
| RsQCXN4o4Ps | 2011 | 1000–1490 | **0.333** | **−0.447** | **+0.327** |
| Xju_CY5ZESA | 2011 | 100–2550 | 0.752 | +0.630 | +0.619 |
| a6TLGkrfNKI | 2011 | 100–2300 | 0.632 | +0.752 | +0.740 |

ZB788PtqQvg has 525 isolated single-frame freezes in 1187 pairs and RsQCXN4o4Ps has 310 — lag-1 autocorrelation of −0.79 and −0.45 with positive lag-2 is a textbook **exact period-2 alternation**: the 2011 live-action runs at ~12.5 unique fps step-printed into a 25 fps container. The 2026 live-action shows nothing of the kind: 1.3–2.1 % freezes, autocorrelation indistinguishable from zero. Independent confirmation from the TRES channel, where the temporal-Laplacian filter beats against a period-2 cadence and lifts all *odd* small lags: mean-NCC over odd lags 5–29 minus even lags 6–30 is **+0.024 (RsQCXN4o4Ps), +0.097 (Xju_CY5ZESA), +0.074 (a6TLGkrfNKI), +0.0009 (ZB788PtqQvg)** versus **−0.0009, −0.0011, −0.0004** for the three 2026 files. Corroborated pointwise in the (A) patches: ZB788PtqQvg f01009 dark patch has tdiff std 0.077 DN at k=1 but 0.724 at k=5 (9.4×); RsQCXN4o4Ps f01125 0.083 → 0.508 (6.2×); whereas OpSTlDJWFFI f02200 bright patch is 0.483 → 0.501 (1.04×) and l9RAhmPHM_A f01098 0.556 → 0.554 (1.00×).

### B3. Is there an animated grain layer at all? (both eras: no)
Over fully static title/text-card sections, 192×192 centre patch:

| video | era | frames | bit-identical pair frac | HP2 NCC lag1 | lag5 | mean abs diff DN |
|---|---|---|---|---|---|---|
| OpSTlDJWFFI | 2026 | 60–560 | 0.070 | 0.9815 | 0.9612 | 0.525 |
| Oqw96jCOP7A | 2026 | 40–430 | 0.756 | 0.9586 | 0.9557 | 0.084 |
| l9RAhmPHM_A | 2026 | 60–560 | 0.344 | 0.8068 | 0.7377 | 0.467 |
| Xju_CY5ZESA | 2011 | 200–700 | 0.000 | 0.9961 | 0.9801 | 0.151 |
| a6TLGkrfNKI | 2011 | 200–700 | 0.058 | 0.9776 | 0.9672 | 0.350 |

In both eras the high-frequency field over a frozen graphic is 96–99 % identical frame to frame (l9RAhmPHM_A's 0.81 is a fade, not a held card). So **neither era carries a global animated grain overlay** — what noise survives is a frozen pattern plus AV1 dither. This is a genuine common negative, but again a weak one, because a 0.1–0.5 DN animated grain layer would not survive this encode anyway.

**Verdict (B):** loop detection — **SAME (both null)**: no loop period exists in either era, to a mean-NCC sensitivity of ~0.003 over lags up to 900. Frame cadence — **DIFFERENT pipeline signature**: period-2 step-printing at 33–45 % freeze fraction in 2011 live-action, absent (1.3–2.1 %) in 2026. I flag that cadence is an editorial/telecine choice rather than a grain property, but a single shared pipeline would be expected to apply it consistently.

---

## (C) Damage layer behaviour — verdict: **SAME behaviour in both eras (frame-referenced and transient, not photographed-in); no recurrence in either**

### C1. Two-hypothesis displacement test
For 12 well-separated frame pairs per video (6 for RsQCXN4o4Ps), global translation from full-resolution phase correlation of the picture rect, retained only when 7 ≤ max(|dy|,|dx|) ≤ 40 px. Damage marks = connected components of the morphological black-hat / white-hat of `f − gauss(f,5)` above 5 DN, 6–1500 px, discarded if >40 % of their pixels sit above the 70th-percentile gradient (so marks on textured backgrounds are excluded) or within 45 px of the crop edge. For each mark I read the next frame's top-hat response at (a) the identical pixels, (b) those pixels displaced by the global motion vector, (c) 8 random displacements of comparable magnitude as a null. Retention = (A_hyp − A_rand)/(A_src − A_rand). 95 % CIs from 2000-sample bootstrap over marks.

| video | era | marks | pairs | A_src | A_frame | A_image | A_rand | **retention FRAME-FIXED** | **retention IMAGE-LOCKED** | diff [95 % CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| OpSTlDJWFFI | 2026 | 91 | 12 | 5.45 | 1.50 | 1.14 | 1.27 | **+0.055** | **−0.030** | 0.085 [−0.020, 0.184] |
| Oqw96jCOP7A | 2026 | 383 | 12 | 5.70 | 2.23 | 1.57 | 1.72 | **+0.130** | **−0.038** | 0.167 [0.094, 0.237] |
| l9RAhmPHM_A | 2026 | 656 | 12 | 5.89 | 2.46 | 2.43 | 2.41 | **+0.014** | **+0.005** | 0.009 [−0.075, 0.081] |
| ZB788PtqQvg | 2011 | 219 | 12 | 5.60 | 1.45 | 1.42 | 1.33 | **+0.027** | **+0.020** | 0.007 [−0.051, 0.062] |
| RsQCXN4o4Ps | 2011 | 40 | 6 | 5.56 | 1.58 | 1.01 | 1.21 | **+0.086** | **−0.046** | 0.131 [−0.007, 0.268] |

Example pairs: Oqw96jCOP7A f00600→f00601, g=(+10,+12), 21 marks, ret_frame +0.28 / ret_image −0.00; ZB788PtqQvg f00442→f00443, g=(−6,+34), 10 marks, ret_frame +0.15 / ret_image 0.00; OpSTlDJWFFI f02795→f02796, g=(+1,+18), 21 marks, ret_frame +0.20 / ret_image +0.05.

Two conclusions, both holding across eras:
1. **retention_IMAGE-LOCKED is zero or negative in every one of the five videos** (−0.046 to +0.020). The marks do not displace by the image motion vector. **They are not baked into the photographed content** — this rules out, for both eras, the hypothesis that the footage is a camera pointed at a damaged print.
2. **retention_FRAME-FIXED is only +0.014 to +0.130.** At most 13 % of a mark's amplitude survives one frame later even at the identical pixel. The overwhelming majority of dust/dirt is **single-frame transient**, in both eras. Note this does not by itself distinguish a digital dirt-overlay plugin from real dirt passing through a film gate — both are frame-referenced and both are transient.

### C2. Persistent-mark lock test (independent method)
For 30–36-frame runs with sustained motion I built three temporal medians of the σ=5 high-pass residual: unaligned (keeps frame-fixed structure), motion-compensated by cumulative phase correlation (keeps image-locked structure), and randomly shifted (null). Robust σ of the resulting median image, frame / image / random:

- Oqw96jCOP7A f1060–1090 (cum. motion −91,+101): 0.154 / 0.145 / 0.109; f1840–1870 (−13,−44): 0.143 / 0.083 / 0.048; f2340–2370 (+26,+22): 0.099 / 0.055 / 0.040
- ZB788PtqQvg f420–450 (−105,−99): 0.189 / 0.165 / 0.108; f230–260 (−5,−61): 0.164 / 0.137 / 0.085; f1090–1120 (−68,−55): 0.085 / 0.078 / 0.044
- RsQCXN4o4Ps f1105–1140 (−197,+1): 0.083 / 0.071 / 0.045; f700–730 (−96,−96): 0.160 / 0.151 / 0.068

σ_frame > σ_image > σ_random in 8 of 8 usable runs, ratio σ_frame/σ_random 1.4–3.0, with the same ordering and comparable ratios in both eras. Consistent with C1. (OpSTlDJWFFI and l9RAhmPHM_A yielded almost no usable runs — cumulative motion under 25 px over 31 frames in 4 of 4 and 3 of 4 candidate runs, so the hypotheses were not separable there. That is a genuine gap in coverage for those two videos.)

### C3. Recurrence
The lag analysis in B1 is exactly the recurrence test on the damage channel: identical marks reappearing at interval T would put an isolated spike in HP2 mean-NCC at T. Over lags 1–900, no video in either era shows a spike above z=5.6, and the top HP2 candidates (k=27, 140, 810, 186, 190) are not consistent across videos and have no harmonics. **No repeating damage interval in either era.**

**Verdict (C): SAME pipeline signature** on every axis I could measure — marks are frame-referenced not image-locked (retention_image ≈ 0 in all five), overwhelmingly transient (retention_frame ≤ 0.13), with a weak frame-fixed persistent residual, and never recurring. The one quantitative era difference is mark contrast: 2011 top-hat peaks max out at 11–33 DN (ZB788PtqQvg 11.5–16.6, RsQCXN4o4Ps 15.3–33.4) versus 24–66 DN in 2026 (OpSTlDJWFFI 24–45, Oqw96jCOP7A 44–55, l9RAhmPHM_A 37–66). That is a ~2× difference in damage strength, but it is confounded by grading, gate size and bitrate and I would not lean on it.

---

## Summary of verdicts

- **(A) noise spectrum: INDETERMINATE.** 2026 slope median −2.58 (range −3.59…−2.41), 2011 median −2.55 (range −2.71…−2.40); ACF half-width 4.29 vs 3.75 px; band-limited amplitude 0.96–1.97 vs 1.14–1.29 DN peak. Same family, but the entire signal lives at 0.1–2 DN, which is the AV1 reconstruction floor. This test has essentially no discriminating power on these files. To settle it you need pre-YouTube masters.
- **(B) grain static vs per-frame: no loop in either era (SAME, both null)**, sensitivity ~0.003 mean-NCC over lags 1–900; and neither era has an animated grain overlay (96–99 % frozen HF over static cards). But **DIFFERENT** on temporal cadence: 2011 live-action is period-2 step-printed (freeze fraction 0.33–0.45, freeze-autocorr lag1 −0.79/−0.45), 2026 is not (0.013–0.021, autocorr ≈ 0).
- **(C) damage layer: SAME pipeline signature.** Frame-referenced, not image-locked (retention_image −0.046…+0.020 across all five), transient (retention_frame +0.014…+0.130), no recurrence at any interval up to 900 frames, in both eras.

### Things I could not determine
- Whether the damage marks are digitally added or real gate dirt — frame-fixed transient behaviour is identical for both.
- Whether any original film grain differed between eras: erased by AV1 in all seven files.
- Task C displacement statistics for OpSTlDJWFFI and l9RAhmPHM_A are thin (91 marks / 12 pairs and 656 marks but retention ≈ 0 for both hypotheses); the persistent-mark test failed entirely on those two for lack of separable motion.
- Xju_CY5ZESA and a6TLGkrfNKI are text-only or near-static and contribute almost nothing to (A) or (C); a6TLGkrfNKI's 640×480 raster also makes its spatial-frequency numbers non-comparable to the 1080p files.

Working files, scripts and per-video JSON are in `/home/user/new-skinny-bob/analysis/compare-eras/grain/` (`taskA.json`, `taskBf_*.json`, `taskC3.json`, `taskC4.json`, `fulldiff_*.npy`, `lib.py` holds the rect tables). I deleted the ~7.5 GB of intermediate `thumb_*.npy` frame stacks; `scan.py` regenerates them.
