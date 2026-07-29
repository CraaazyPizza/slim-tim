# Agent report (verbatim): banding & colour-math cross-era comparison

Agent task ac9f0946332ca39f4, completed 2026-07-26. Final message verbatim:

---

# TASK 1 — HORIZONTAL BANDING

## Method / measurement geometry

Streamed native `yuv420p` from each `.mkv` (no RGB round-trip), computed per-frame row-mean luma profiles restricted to a rect strictly inside the soft vignette window and **above** the burned-in timecode band (which sits at rows ~920–1000). Rects used (full-res luma, cols × rows):

| video | rect cols | rect rows | frames |
|---|---|---|---|
| OpSTlDJWFFI | 380–1500 | 120–900 | 2998 |
| Oqw96jCOP7A | 420–1500 | 120–900 | 2503 |
| l9RAhmPHM_A | 400–1460 | 140–900 | 4395 |
| ZB788PtqQvg | 380–1560 | 120–900 | 1188 |
| RsQCXN4o4Ps | 380–1540 | 120–900 | 1500 |
| Xju_CY5ZESA | 390–1500 | 120–900 | 2598 |
| a6TLGkrfNKI | 90–550 | 60–420 | 2337 |

Windows were located from per-pixel temporal-std maps (`masks.py`, images in `mont/*_ystd.png`): OpSTlDJWFFI cols 238–1640, Oqw96jCOP7A 295–1622, l9RAhmPHM_A ~280–1600, ZB788PtqQvg 239–1698, RsQCXN4o4Ps ~240–1680, Xju_CY5ZESA 252–1624; a6TLGkrfNKI has no hard matte (vignette only).

**Static text cards were excluded** (they are a lethal contaminant — see below). Card ranges found from frame-to-frame row-profile RMS change (`cards.py`): OpSTlDJWFFI t=0–29s, Oqw96jCOP7A t=0–14s, l9RAhmPHM_A t=0–14s, RsQCXN4o4Ps t=2–22s (interleaved), Xju_CY5ZESA ~all, a6TLGkrfNKI ~all but t=72–82s.

Three spectra per video: STATIC (FFT of temporal mean), DYNAMIC (FFT of profile minus a ±15/±20-frame local temporal mean — cancels any static overlay exactly), ALLFR. Significance = power / log-frequency-local median baseline (window f/1.35…f×1.35, ±3-resolution-element guard) so a steep 1/f^a continuum cannot manufacture SNR. Two bands run separately: fine 2.05–120 px (`banding3.py`) and broad 60–900 px with poly-4 detrend (`lowband.py`). Chroma planes run identically (`chromaband.py`).

**Pipeline validated independently**: recomputing the same detrended row profiles from the pre-extracted PNGs (separate decode path) gives corr = **+0.9983 to +1.0000** against the coded-Y result, with gain 1.150–1.166 = the expected 255/219 limited-range factor (`verify.py`).

## Result A — the only ubiquitous periodicity is the AV1 block grid

Every one of the seven files shows a STATIC comb whose fundamentals fit **32 px** (peaks at exactly 32.0/16.0/10.72/8.0/5.33/4.57/4.00/3.56/2.91/2.67/2.29/2.13 px = 32/n). Comb-search fundamentals, all seven: **16.06 px and 10.72 px** (= 32 and 32/3).

Amplitudes (component amplitude at 32/16/8/4 px, from `gridphase.py`, measured over rows 100–980 / 40–440):

| video | 32px | 16px | 8px | 4px |
|---|---|---|---|---|
| OpSTlDJWFFI | 0.100 | 0.141 | 0.069 | 0.035 |
| Oqw96jCOP7A | 0.091 | 0.029 | 0.136 | 0.044 |
| l9RAhmPHM_A | 0.155 | 0.066 | 0.036 | 0.009 |
| ZB788PtqQvg | 0.017 | 0.012 | 0.007 | 0.004 |
| RsQCXN4o4Ps | 0.078 | 0.099 | 0.008 | 0.006 |
| Xju_CY5ZESA | 0.061 | 0.015 | 0.006 | 0.092 |
| a6TLGkrfNKI | **0.493** | 0.054 | 0.179 | 0.164 |

All ≤ 0.5 LSB (8-bit). Periods are exact powers-of-two multiples matching AV1 transform sizes; a6TLGkrfNKI's 32-px component is phase-locked to coded row 0 (offset 0.11 px). **This is recompression, identical in both sets, and carries zero discriminating power.** It also sets a hard floor: I cannot exclude a genuine production band of amplitude < ~0.5 LSB *at those specific periods*.

## Result B — the strong "banding" combs are burned-in TEXT, not banding

My first pass found spectacular combs and they were all text line pitch. Reported so you don't get misled by someone else's version of this measurement:

- **a6TLGkrfNKI**: comb fundamental **25.6 ± 0.05 px** (harmonics measured at 8.55, 6.40, 4.26, 3.67 px → ×3, ×4, ×6, ×7 = 25.65, 25.60, 25.56, 25.69), incoherent SNR 167, apparent amp up to 5.4 LSB. Phase drift **−0.0021 px/frame**, phase residual sd 0.357 rad, frame-to-frame dφ IQR = **0.000 rad** → perfectly rigid. This is the text line pitch of the caption cards (independently: ~26 px measured off frame f01700 geometry). Confirmed in chroma too: static U/V peak at 24.8 luma-px, SNR 22–28.
- **Xju_CY5ZESA**: comb fundamental **38.4 px** (peaks 19.20, 9.59, 6.39, 5.49, 4.27, 3.20 px = 38.4/n for n=2,4,6,7,9,12), static SNR 160–208, amp 2.2–3.1 LSB, drift **−0.00037 px/frame**, dφ IQR = 0.000 rad. Text line pitch at 1080p.

## Result C — no rolling / drifting banding anywhere, luma or chroma

After card exclusion, DYNAMIC (local-mean-subtracted) spectra:

Fine band 2.05–120 px, top DYNAMIC peak per video:

| video | period | SNR | amp (LSB) |
|---|---|---|---|
| OpSTlDJWFFI | 4.77 px | 122.5 | **0.0150** |
| Oqw96jCOP7A | 4.49 px | 58.9 | **0.0188** |
| l9RAhmPHM_A | 4.79 px | 166.6 | **0.0177** |
| ZB788PtqQvg | 20.39 px | 8.6 | 0.113 |
| RsQCXN4o4Ps | 7.21 px | 18.3 | **0.0140** |
| Xju_CY5ZESA | 6.39 px | 31.0 | 0.162 (text residue at card cuts) |
| a6TLGkrfNKI | 3.81 px | 7.9 | **0.0259** |

The high SNRs are against an extremely clean dynamic floor; the **amplitudes are 0.014–0.026 LSB**, i.e. 1/40 of a code value — physically invisible and far below any camera banding. All five 1080p files show a sub-LSB dynamic pair at ratio ≈9:8 (OpST 4.77/5.37, l9R 4.79/5.39, Oqw 4.49/5.04, RsQ 7.21/8.35, a6 3.81/4.23) which I attribute to AV1 in-loop restoration / grain synthesis; present in **both** sets, so not a fingerprint, and too weak to use.

Broad band 60–900 px (where a CRT/rolling-shutter beat would live — 1–6 bands per frame), top DYNAMIC peak:

| video | period | SNR | amp (LSB) | band-limited dynamic RMS |
|---|---|---|---|---|
| OpSTlDJWFFI | 81 px | 2.82 | 0.81 | 2.04 |
| Oqw96jCOP7A | 69 px | 2.96 | 0.91 | 2.91 |
| l9RAhmPHM_A | 117 px | 2.37 | 0.96 | 1.96 |
| ZB788PtqQvg | 83 px | 7.29 | 2.52 | 6.65 |
| RsQCXN4o4Ps | 125 px | 3.34 | 1.18 | 1.79 |
| Xju_CY5ZESA | 61 px | 2.15 | 0.15 | 0.26 |
| a6TLGkrfNKI | 115 px | 2.01 | 0.69 | 0.71 |

**Maximum DYNAMIC SNR across all seven videos in the CRT-beat band is 7.3.** Nothing survives.

Drift on the strongest sliding-window (60-frame) episodes, sub-pixel phase tracking (`verify.py`):

| video | window | period | amp | drift | dφ concentration |
|---|---|---|---|---|---|
| OpSTlDJWFFI | t=86–92s | 178 px | 4.15 ± 0.78 LSB | **+0.006 px/frame** (+0.19 px/s) | 0.984 (static) |
| Oqw96jCOP7A | t=76–80s | 80 px | 0.84 ± 0.22 | **+0.003 px/frame** | 0.911 (static) |
| ZB788PtqQvg | t=35–40s | 83 px | 0.43 ± 0.22 | +0.011 px/frame | 0.453 (incoherent) |
| RsQCXN4o4Ps | t=51–58s | 127 px | 0.40 ± 0.23 | −0.265 px/frame (−6.6 px/s) | 0.850 |
| a6TLGkrfNKI | t=73–78s | 80 px | 0.65 ± 0.27 | −0.254 px/frame (−6.3 px/s) | 0.832 |

RsQCXN4o4Ps and a6TLGkrfNKI both show ≈ **−0.26 px/frame**, but *identical in px/frame at two different periods*, which is the signature of a global vertical image translation (simulated film weave / gate float), not of a band rolling relative to the picture. Median inter-frame vertical shift is +0.000 px in all seven (`vshift.py`), with ±10–20 px content motion in the footage clips.

**Chroma banding** (U/V row profiles at chroma resolution, periods reported in luma px): maximum DYNAMIC SNR across all seven = **5.54** (ZB788PtqQvg U at 79 luma-px), amplitude 0.097 LSB; all others ≤ 3.2 SNR / ≤ 0.13 LSB. Static chroma structure is the same 32/16/6.4-luma-px block comb at 0.001–0.087 LSB, plus a6TLGkrfNKI's 24.8-luma-px text comb.

## TASK 1 VERDICT

**Banding in the 2026 set: ABSENT.** Upper limits: no periodic luma component with SNR > 3 and amplitude > 0.03 LSB in 2–120 px, none with SNR > 3 in 60–900 px; no drift above 0.006 px/frame on any candidate; no chroma banding above 0.02 LSB.

**Banding in the 2011 set: ALSO ABSENT.** The community claim of "horizontal coloured banding indicative of a modern camera" in the 2011 videos is **not supported by the data**. What I suspect people are looking at is (i) the burned-in caption line pitch (25.6 px in a6TLGkrfNKI, 38.4 px in Xju_CY5ZESA, amplitude 2–5 LSB and therefore genuinely visible) and (ii) the AV1 32-px block comb. Neither is a camera artifact and neither drifts.

**Pipeline verdict for (1): INDETERMINATE.** The feature is absent from both sets, so the test has no discriminating power. The only periodicity shared by all seven files is a YouTube-AV1 artifact, which proves nothing about production. The claim that "the two 1080p 2011 footage videos were filmed off a CRT/TV screen while the 640×480 tape-06 video was not" gets **no support**: none of the three shows a screen-capture beat, and the alleged CRT pair (ZB788PtqQvg, RsQCXN4o4Ps) is not distinguishable from a6TLGkrfNKI on this axis.

---

# TASK 2 — COLOUR / CHROMA

## Codec chroma noise floor (essential reference)

**Xju_CY5ZESA is the calibration standard.** It is the closest to mathematically grey of the seven: picture window (cols 390–1500, rows 60–1030) meanU = 127.577, meanV = 128.167, sdU = 0.350, sdV = 0.306, ⟨|chroma|⟩ = 0.507, **max |chroma| over all 2598 frames = 3.2**, frac|U−128|>2 = **0.0000**, frac|V−128|>2 = **0.0000**. So AV1 at yuv420p leaks up to ±3 code values of chroma into nominally grey material, with sd ≈ 0.3. Anything below sd ≈ 0.4 / max ≈ 3 is not interpretable.

## Per-video chroma statistics (picture window, actual U/V planes)

| video | meanU | meanV | sdU | sdV | ⟨mag⟩ | mag p99 | mag max | fU>2 / >4 / >8 | fV>2 / >4 / >8 |
|---|---|---|---|---|---|---|---|---|---|
| OpSTlDJWFFI | 126.034 | 126.539 | 1.237 | 0.762 | 2.982 | 5.22 | **91.8** | .2366/.0832/.0287 | .1381/.0682/.0230 |
| Oqw96jCOP7A | 126.690 | 129.031 | 0.682 | 0.677 | 1.703 | 2.97 | 6.4 | .2080/.0000/.0000 | .1153/.0000/.0000 |
| l9RAhmPHM_A | 126.708 | 128.658 | 0.438 | 0.573 | 1.542 | 3.25 | 7.2 | .1404/.0000/.0000 | .0703/.0000/.0000 |
| ZB788PtqQvg | 126.188 | 128.836 | 1.528 | 0.459 | 2.321 | 4.98 | 11.0 | .2381/.1599/.0021 | .0041/.0000/.0000 |
| RsQCXN4o4Ps | 127.487 | 128.299 | 1.085 | 0.539 | 1.190 | 3.12 | 7.3 | .1160/.0010/.0000 | .0054/.0000/.0000 |
| Xju_CY5ZESA | 127.577 | 128.167 | 0.350 | 0.306 | 0.507 | 1.07 | 3.2 | .0000/.0000/.0000 | .0000/.0000/.0000 |
| a6TLGkrfNKI | 127.214 | 128.452 | 1.604 | 0.454 | 1.872 | 3.58 | 13.9 | .3030/.0967/.0031 | .0079/.0003/.0000 |

## The decisive test: tint vs genuine colour

For every frame I regressed the chroma on the luma inside the rect at chroma resolution (`pass4.py`/`tint.py`): fit (U−128) = a_u·Y + b_u, likewise V. A **tint on monochrome** gives R² → 1 and near-zero residual; **genuine colour** gives low R² and large residual. Medians over frames with sdU or sdV > 0.4:

| video / segment | a_u ×100 | a_v ×100 | b_u | b_v | R²u | R²v | resid sdU | resid sdV | corr(U,V) |
|---|---|---|---|---|---|---|---|---|---|
| **OpSTlDJWFFI** mono part (f1100–2500) | −0.058 | +0.025 | **−1.824** | **−1.788** | 0.002 | 0.002 | 0.836 | 0.618 | +0.047 |
| **OpSTlDJWFFI** colour seg (f2571–2917) | +10.744 | −3.591 | −11.851 | −2.961 | **0.480** | **0.190** | **3.386** | **2.547** | −0.766 |
| **OpSTlDJWFFI** flash (f1040–1044) | +18.578 | −26.151 | −45.894 | +58.866 | 0.384 | 0.685 | **9.217** | **6.254** | −0.714 |
| **Oqw96jCOP7A** all | **−3.075** | **+2.962** | +0.481 | −0.747 | 0.747 | 0.793 | 0.381 | 0.365 | −0.797 |
| **l9RAhmPHM_A** all | **−2.262** | **+2.975** | −0.104 | −1.063 | 0.707 | 0.716 | 0.273 | 0.367 | −0.804 |
| **ZB788PtqQvg** all | −4.302 | **+0.016** | +1.435 | +0.891 | 0.744 | **0.005** | 0.554 | 0.467 | +0.032 |
| ZB788PtqQvg strongest (f133–407) | −4.460 | **−0.031** | +1.618 | +0.894 | **0.959** | **0.005** | 0.642 | 0.459 | +0.066 |
| **RsQCXN4o4Ps** all | −4.757 | +0.815 | +3.056 | −0.187 | 0.787 | 0.104 | 0.726 | 0.688 | −0.280 |
| **Xju_CY5ZESA** all | −0.816 | +0.311 | +0.018 | +0.006 | 0.230 | 0.038 | 0.414 | 0.430 | −0.397 |
| **a6TLGkrfNKI** all | −2.038 | +0.222 | −0.231 | +0.495 | 0.078 | 0.010 | 2.012 | 0.609 | −0.420 |
| a6TLGkrfNKI strongest (f1816–2045) | **−26.750** | +3.440 | +19.381 | −1.794 | **0.968** | 0.434 | **0.753** | 0.687 | −0.657 |

Corroborated by the independent spatial-structure pass (`chromastruct.py`, every 6th frame): median corr(U,Y) / corr(V,Y) = Oqw96jCOP7A **−0.867 / +0.892**, l9RAhmPHM_A **−0.840 / +0.842**, ZB788PtqQvg **−0.864 / +0.015**, RsQCXN4o4Ps **−0.875 / +0.296**, a6TLGkrfNKI top-chroma frames **−0.99 / +0.47…+0.84**, OpSTlDJWFFI **+0.009 / −0.031**. Chroma is spatially structured in all seven (4×4-block variance retention 0.87–0.97, lag-8 autocorrelation 0.72–0.93), i.e. it is not pixel noise — but in six of seven that structure is simply the luma structure re-expressed.

## Classification of the seven

- **(a) True greyscale, codec noise only** — **Xju_CY5ZESA** (2011). max|chroma| 3.2, frac>2 = 0.0000, R² 0.23. Indistinguishable from U=V=128 plus AV1 leakage.
- **(b) Flat uniform cast, no luma coupling** — **OpSTlDJWFFI monochrome sections** (2026): b_u = −1.82, b_v = −1.79, a_u ≈ a_v ≈ 0, R² = 0.002. A constant −1.8 offset on **both** axes = a uniform slightly-green cast. This is the only video whose grey sections are cast rather than tinted.
- **(c) Luma-coupled TINT, two-axis, near-antisymmetric** — **Oqw96jCOP7A** and **l9RAhmPHM_A** (2026). a_v ≈ −a_u (ratio −0.96 and −1.32), corr(U,V) = −0.80, R² 0.71–0.79, residual non-tint chroma 0.27–0.38 LSB (≈ codec floor). Visually: warm orange highlights / neutral shadows (see `viz/Oqw96jCOP7A.png`, chroma ×10).
- **(d) Luma-coupled TINT, single U axis** — **ZB788PtqQvg**, **RsQCXN4o4Ps**, **a6TLGkrfNKI** (all 2011). a_v ≈ 0 (+0.02, +0.82, +3.44 per 100), R²v = 0.005 / 0.104 / 0.434 vs R²u = 0.96 / 0.79 / 0.97, corr(U,V) = +0.03 / −0.28 / −0.66. Pure blue↔yellow axis: yellow-green highlights, lavender shadows (`viz/ZB788PtqQvg.png`). Residual non-tint chroma 0.46–0.75 LSB, at the codec floor.
- **(e) Genuine independent colour** — **only OpSTlDJWFFI** (2026), and only in specific segments.

## a6TLGkrfNKI: the "tape 06 retained colour" claim is FALSIFIED

It has the most chroma of the four 2011 files (window sdU 1.604, frac|U−128|>2 = 0.3030, max|chroma| 13.9, strongest segment f01816–f02045 = t 72.60–81.76 s with sdU 4.733) — so it is easy to see why people said "colour". But it is **monochrome with the steepest single-axis tint of the seven**: a_u = −26.75 per 100 luma LSB (6× steeper than ZB788PtqQvg/RsQCXN4o4Ps), R²u = **0.968**, a_v = +3.44 with R²v 0.43, and residual chroma not explainable from luma = **0.753 LSB** against a 0.44 LSB codec floor. frac|V−128|>4 = 0.0003. `viz/a6TLGkrfNKI.png` shows the tell: at ×10 chroma gain the bright background is yellow and the dark figure is blue — inverse-luma, i.e. exactly a_u < 0, not colour. There is no independent hue anywhere in this file.

## The 2026 colour segment ("col/s")

`segments.py` on OpSTlDJWFFI (threshold sdU or sdV > 3.0 in the window):

| frames | time | meanU | meanV | sdU | sdV | mag p99 | mag max | fU>8 | fV>8 |
|---|---|---|---|---|---|---|---|---|---|
| f00917–f00921 | 30.56–30.70 s (0.17 s) | 121.615 | 132.429 | 5.391 | 3.912 | 29.24 | 46.3 | 0.326 | 0.148 |
| f01040–f01044 | 34.67–34.80 s (0.17 s) | **86.523** | **163.121** | 10.296 | 8.189 | 71.01 | **91.8** | 0.853 | 0.835 |
| **f02571–f02917** | **85.75–97.30 s (11.58 s)** | 123.266 | 122.783 | 5.128 | 2.945 | 16.02 | 51.0 | 0.218 | 0.178 |
| f02971–f02974 | 99.10–99.20 s (0.13 s) | 139.616 | 123.666 | 17.032 | 2.798 | 55.11 | 67.3 | 0.387 | 0.100 |

Time series shape: chroma is flat at ⟨mag⟩ ≈ 2.5 from t=35 to t=84 with meanU ≈ meanV ≈ 126.25 (the flat green cast), then a hard step up at t=85 to sdU 2.0→5.8, fU>4 rising 0.003 → **0.54** (peak at t=89), holding through t=96, decaying by t=97. Peak-chroma frame in the segment: f02845 (t=94.89). Peak-chroma frame overall: f01041 (t=34.70, sdU 14.827, sdV 12.592, a bright red/orange full-frame flash).

**This segment is real independent colour**, not a tint: R²u = 0.48 only, residual sdU = 3.39 and sdV = 2.55 LSB after removing everything the luma can explain. `viz/OpSTlDJWFFI.png` (frames 2600/2700/2800/2900, chroma ×10) shows two *different* hues in different image regions — green in the lower/foreground area and cyan-blue in the upper sky/water area — which no single-parameter tint can produce.

**"(col/s)" resolved.** The intro card of OpSTlDJWFFI (readable at f00900) lists under Tape 06: `Case 31/Mk.5 virgin (col/s) 00:57:56 - 00:58:04`. The burned-in timecode inside the colour segment reads `T6-02/31 00:57:56` … `00:58:03`. So the annotation marks this fragment, and the colour segment delivers it. **The "s" is sound**: per-second audio RMS for OpSTlDJWFFI is −120 dBFS for t=0–29, then a constant −33…−36 dBFS bed for t=30–84, then jumps to **−13 dBFS for t=85–96** and back to −15…−22 by t=97–99 — a ~21 dB step exactly co-located with the colour segment. (Side note from the same pass: l9RAhmPHM_A, Xju_CY5ZESA and a6TLGkrfNKI have **completely silent** audio tracks — all-sample −∞; OpSTlDJWFFI, Oqw96jCOP7A, ZB788PtqQvg, RsQCXN4o4Ps carry a ~−34 dBFS bed.)

No colour segment exists anywhere in Oqw96jCOP7A (sdU or sdV > 2.0: **zero frames** of 2503; max sdU 1.421 at f02265, t=75.54) or l9RAhmPHM_A (zero frames; max sdU 1.261 at f03885, t=129.60).

## TASK 2 VERDICT

**DIFFERENT pipeline signature**, on two independent grounds:

1. **Tint geometry.** a_v/a_u = −0.96 (Oqw96jCOP7A), −1.32 (l9RAhmPHM_A) with corr(U,V) = −0.80 and R²v = 0.72–0.79 — a deliberate two-axis orange/teal monochrome tint. Versus −0.004 (ZB788PtqQvg), −0.17 (RsQCXN4o4Ps), −0.13 (a6TLGkrfNKI global) with corr(U,V) = +0.03…−0.42 and R²v = 0.005–0.104 — a single blue/yellow-axis tint with V held at neutral. These are different colour-grading operations, not different strengths of the same one.
2. **Colour content.** Genuine luma-independent chroma (residual sd 2.5–9.2 LSB after de-tinting, max|chroma| 91.8) exists **only** in the 2026 set, in OpSTlDJWFFI, in four localised events totalling 12.05 s. No 2011 file contains any chroma that is not a function of its own luma, at a residual limit of 0.75 LSB.

Countervailing evidence for "same pipeline" (which I measured but which is stylistic, not signal-level): both sets use a soft-edged vignette window inside a black matte, both burn in a bottom-left `/NN HH:MM:SS` timecode preceded by a black redaction bar, both are monochrome-plus-warm-tint, and both open with a `Case NN/<name> HH:MM:SS – HH:MM:SS` fragment-list card in the same monospace face. Matte luma levels: OpSTlDJWFFI 21.8, Oqw96jCOP7A 24.9, l9RAhmPHM_A 38.4, ZB788PtqQvg 26.2–31.1, RsQCXN4o4Ps 21.0–25.7, Xju_CY5ZESA exactly 16.0 with temporal std exactly 0.000. Matte temporal std (global grain layer bleeding over the matte): 2026 set 4.2 / 4.7 / 7.6, 2011 set 0.8–2.9 / 5.2–6.5 / 0.000 — overlapping, so not discriminating either.

---

# What I could not determine, and where recompression is the confound

1. **yuv420p is a hard limit on chroma resolution.** Chroma is 960×540 (320×240 for a6TLGkrfNKI). Any chroma banding with period < 4 luma px is undetectable *by construction*, and all chroma spatial detail I measured is already 2×2-averaged. Chroma statements below ~4 px scale are unavailable.
2. **AV1 chroma leakage sets a floor of sd ≈ 0.3–0.35 and max|chroma| ≈ 3.2** (measured on Xju_CY5ZESA). This means the 2011 set's a_v ≈ 0 is a *bound*, not a measurement: with sdV = 0.46–0.54 against a 0.31 floor I can say |a_v| < ~1 per 100 luma LSB but cannot pin it. The contrast with the 2026 set's a_v = +2.96…+2.98 at R²v 0.72–0.79 is nevertheless well outside this uncertainty.
3. **The 32/16/8/4-px block comb (≤ 0.5 LSB) is recompression** and is identical in both sets. Consequence: a real production banding component of amplitude below ~0.5 LSB *at exactly those periods* cannot be excluded in any file. At non-power-of-two periods my limit is tighter (~0.03 LSB dynamic, ~0.1 LSB static).
4. **Generational asymmetry.** The 2011 files were uploaded in 2011 and re-encoded to AV1 by YouTube much later, so they have been through more transcode generations than the 2026 files (their block-comb signature is correspondingly stronger: ZB788PtqQvg and RsQCXN4o4Ps had the cleanest static spectra with block SNR 1679 and 1248 in the fine band, indicating heavier quantization relative to detail). A fine banding pattern that existed in a 2011 master could have been quantized away in a way that a 2026 master's would not. **This asymmetry means my absent-vs-absent banding result cannot distinguish "never there" from "destroyed", and is the single biggest reason verdict (1) is INDETERMINATE rather than DIFFERENT.**
5. **a6TLGkrfNKI is 640×480**, 6.75× fewer pixels. A pattern at period P in a 1080-line master appears at 0.44P here and could alias past Nyquist. I therefore cannot rule out that a fine 1080p-native band exists in the ivan masters and simply does not survive into the 4:3 file.
6. **Both sets carry a heavy synthetic degradation layer** (blur, vignette, grain, gate float) that would itself smear any pre-existing camera banding. I measured the grain but did not attempt to invert the degradation.
7. **Not attempted:** audio spectral fingerprinting (I only measured per-second RMS), grain-model matching between sets, and font/kerning metrology on the caption cards — the last of these looks like the highest-value remaining test for the same-pipeline question, since the caption typography is a direct authoring artifact rather than a codec one, and the text line pitch I already measured (25.6 px at 480p, 38.4 px at 1080p in the 2011 set) is a concrete number to compare against the 2026 cards.

All scripts and intermediate arrays are in `/home/user/new-skinny-bob/analysis/compare-eras/band/` (185 MB): `pass1.py`–`pass4.py` (streaming YUV extraction), `banding3.py` / `lowband.py` / `chromaband.py` (banding), `tint.py` / `chromastruct.py` / `segments.py` (chroma), `verify.py` / `gridphase.py` / `vshift.py` (controls), `mont/` and `viz/` (visual evidence, including `viz/OpSTlDJWFFI.png` for the colour segment and `viz/a6TLGkrfNKI.png` for the tint-not-colour demonstration).
