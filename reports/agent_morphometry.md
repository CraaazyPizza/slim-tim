# Agent report (verbatim): EBE and craft morphometry across eras

Completed 2026-07-27. Final message verbatim:

---

Measurement work is complete. Here is the report.

---

# Morphometry of the depicted subjects and craft, 2011 ivan0135 vs 2026 qtecqot

Working artifacts: `/home/user/new-skinny-bob/analysis/scenes/morpho/`
– `crops/` — 29 annotated images, every reported ratio has its measurement lines drawn on the source pixels
– `measurements.json` — all numbers below in machine-readable form
– `work/` — scripts (`frontline.py`, `edge50.py`, `frontal.py`, `trace2.py`, `discshape.py`, `mcrop.py`, `hp.py`, `regavg.py`) and intermediates

All edge positions use one operational definition in both eras: **the sub-pixel 50 %-of-step crossing** of a locally-estimated intensity step inside a bracketing window, on rows smoothed with σ = 2 px. No era-specific thresholds except where noted.

---

## 1. RESULTS TABLE

### 1a. Frontal head — cranium width W / outer ocular span S

| Set | Era | Subject / case | n frames | W/S | Artifact |
|---|---|---|---|---|---|
| RsQCXN4o4Ps f1198–1250 | 2011 | Case 25 "skinny Bob", close-up | 14 | **1.492 ± 0.043** | `frontal_2011_f01206.png` |
| a6TLGkrfNKI f1981–1993 | 2011 | "tape 06" walking group, 640×480 | 3 | **1.286 ± 0.018** | `frontal_2011_a6T_f01990.png` |
| Oqw96jCOP7A f1770–1810 | 2026 | Case 25 "Bob's walkabout" | 3 | **1.231 ± 0.171** | `frontal_2026_walkabout_f01800.png` |
| Oqw96jCOP7A f2072 | 2026 | Case 25 "Slim Tim" | 1 | ~1.60 (unreliable) | `frontal_2026_slimtim_f02072.png` |

**The two 2011 sets differ from each other (1.29 vs 1.49) by more than either differs from 2026.** Verdict: **consistent / not discriminating.**

### 1b. Frontal head — minimum sub-cranial silhouette width / W

| Set | Era | n | ratio |
|---|---|---|---|
| RsQ f1198–1250 (minimum falls at the jaw/neck junction) | 2011 | 14 | 0.408 ± 0.011 |
| RsQ f1170 (true neck, mid-neck level) | 2011 | 1 | 0.51 |
| Oqw96 f1800 walkabout (true neck) | 2026 | 1 | 0.51 |

Level-sensitive; where the same anatomical level is measured the two eras agree exactly. **Consistent.**

### 1c. Profile — anterior facial-profile shape ("mid-face notch")

Deviation of the facial silhouette from the forehead→jaw chord, normalised by chord length; notch = dev(t=0.50) − ½[dev(t=0.30) + dev(t=0.80)]. Negative = concave mid-face (human-like brow / sub-nasal saddle / protruding chin); positive = convex arc.

| Group | n | notch | Artifact |
|---|---|---|---|
| 2011 RsQ, near-lateral | 5 | **+0.0089 ± 0.0033** | `profile_2011_all_traces.png`, `profile_2011_f00742.png` |
| 2011 RsQ, three-quarter | 7 | +0.0387 ± 0.0451 | same montage |
| 2026 Slim Tim, near-lateral | 6 | **−0.0399 ± 0.0268** (core n=5: −0.0504 ± 0.0084) | `profile_2026_f02416.png` etc. |
| 2026 Slim Tim, three-quarter | 4 | +0.0027 ± 0.0674 (range −0.063…+0.064) | `profile_2026_threequarter.png` |

Curves: `FIG_profile_deviation_pose.png`. **The metric's swing with pose (~0.11) exceeds the apparent era difference (~0.06). INDETERMINATE — see §3.**

### 1d. Hand

| Quantity | 2011 (Xju_CY5ZESA f01500 print plate) | 2026 (l9RAhmPHM_A f03866) |
|---|---|---|
| **Digit count** | **4** = 3 fingers + 1 opposed thumb behind a deep web | **4** = same arrangement |
| Digit length rank | D3 ≈ D2 > D4 > thumb | D3 > D2 > D4 > thumb |
| D3 / palm width | **1.38** | **1.37** |
| D3 / palm length | 1.11 | 1.31 |
| thumb / D3 | **0.68** | **0.64** |
| D4 / D3 | 0.67 | 0.80 |
| D3 slenderness (L/W) | 8.7 | ~10.5 |
| Distal tip caps | no information (solid ink impression) | glossy near-black caps, specular highlight |

Artifacts: `hand_2011_Xju_print.png`, `hand_2026_v3_f03866.png`, `context_2011_Xju_handplate_full.png`. **Consistent within the (large) print-vs-photograph systematic.**

### 1e. Craft silhouette — apparent width / height

| Set | Era | n | W/H | apparent W |
|---|---|---|---|---|
| ZB788PtqQvg f165–315, Case 07 disc | 2011 | 16 | **3.415 ± 0.192** | 162–182 px |
| OpSTlDJWFFI f1820–1880, Case 12 "Mk.4" (size-matched) | 2026 | 4 | **2.62 ± 0.08** | 151–206 px |
| OpSTlDJWFFI f1820–2100, full run | 2026 | 14 | 2.323 ± 0.279 | 83–206 px |

Artifacts: `craft_2011_ZB_f00235.png`, `craft_2026_v1_f01860.png`. **Numerically different, but the two objects are different craft in-lore and the viewing aspect is uncontrolled. INDETERMINATE — see §3.**

### 1f. Effective resolution (control)

Radial power spectrum of the head region, frequency at which power falls to 10⁻⁴ of the low-frequency value, as a fraction of Nyquist:

| 2011 RsQ f934 head | 2011 RsQ f1206 head | 2026 f2320 head | 2026 f2072 head | 2026 f1800 walkabout |
|---|---|---|---|---|
| 0.064 | 0.048 | 0.088 | 0.055 | 0.085 |

Both eras sit at ~15–20 px PSF at 1080p. **Anything below ~20 px is unresolved in both.** Broad shape features (≥100 px) are safe; digit tips, eyelids and skin texture are not.

---

## 2. INVENTORY OF USABLE VIEWS

**2011 (25 fps; RsQ/ZB/Xju native 1080p, a6TL 480p)**

| Source | Frames / duration | Pose | Scale | Limits |
|---|---|---|---|---|
| RsQ f626–950 | 325 f / 13.0 s | 3/4-away → near-lateral head, fills frame | facial chord 340–515 px | **skin luma ≡ background luma** (both ~116–121 DN); only a thin dark rim marks the silhouette; posterior cranium unrecoverable |
| RsQ f960–1100 | 140 f / 5.6 s | standing, waist-up, both hands at sides | hands ~90 × 200 px | digits unresolvable |
| RsQ f1100–1300 | 200 f / 8.0 s | frontal / near-frontal, camera tilts up; a raised hand at f1140–1160 | cranium W 650–770 px | **crown clipped by the aperture from f1198**; whole face below the cranium is a featureless dark mask |
| ZB f651–730 | 80 f / 3.2 s | two distant standing figures | head < 40 px | unusable |
| ZB f826–1000 | 175 f / 7.0 s | prone bodies | — | unusable |
| a6TL f1830–2045 | 215 f / 8.6 s | walking group: frontal, 3/4 and near-profile | head W 100–150 px at 640×480 | **best 2011 frontal — the only 2011 view with separable eyes and a bright nose bridge** |
| Xju (static plate) | whole file | hand print / impression | hand 500 × 930 px | 2-D print, no depth or tip information |

**2026 (29.97 fps, 1080p)**

| Source | Frames / duration | Pose | Scale |
|---|---|---|---|
| Oqw96 f1207–1414 "Triage" | 208 f / 6.9 s | extreme close-up, 3/4 from above, head clipped left & top | head > frame |
| Oqw96 f1416–1444 "Exit EBL04(a)" | 29 f / 1.0 s | compact dark **normal-proportioned** head on pillow | ~250 px |
| Oqw96 f1445–1613 "Exit EBL04(b/c)" | 169 f / 5.6 s | grey head on pillow, eyes closed, from above | ~400 px |
| Oqw96 f1621–1835 "Bob's walkabout" | 215 f / 7.2 s | full standing figure, frontal | cranium W ≈ 214 px |
| Oqw96 f1840–2422 "Slim Tim" | 583 f / 19.5 s | head+shoulders; near-profile → frontal → near-profile | facial chord 490–575 px |
| l9RAh f3715–4254 | 540 f / 18.0 s | 4-digit hand, dorsal, beside 5-digit human hands | hand ~410 × 530 px |
| OpST f2502–2568 | 67 f / 2.2 s | one pointing digit | unresolvable |

Inventory contact sheets: `inventory_2011_RsQ_profile_run.png`, `inventory_2011_RsQ_standing_run.png`, `inventory_2026_v2_slimtim_run.png`, `inventory_2026_v2_triage_run.png`.

---

## 3. INTERPRETATION, WITH CONFIDENCE

**No measured ratio separates the eras.** Every cross-era comparison the material supports came back either *consistent* or *indeterminate*. In particular:

**(i) The frontal head proportions are consistent — moderate confidence.** W/S is 1.29 (2011 a6TL) vs 1.23 (2026 walkabout) between the only two views in the whole corpus that show a fully-lit frontal face with an identifiable ocular boundary. The 2011 RsQ close-up gives 1.49, but its face is a uniform dark mask so its "S" is inflated by shadow and its 1.49 is a *lower bound*. The honest reading is that the within-2011 scatter (0.20) sets the real reproducibility of this ratio, and the era difference (0.06) sits inside it. Neck/cranium agrees exactly (0.51 both) when measured at the same level.

**(ii) The hand is the strongest cross-era agreement — and it is also the least informative for provenance.** The four-digit morphology is not new in 2026: the 2011 `Xju_CY5ZESA` plate is a hand *print* showing exactly four digits, three fingers plus one long opposed thumb behind a deep web, and its proportions match the 2026 hand almost exactly where the comparison is meaningful (D3/palm-width 1.38 vs 1.37; thumb/D3 0.68 vs 0.64). This is a real continuity. **But that plate is a published 2011 frame, plainly legible at full resolution — precisely the kind of detail a reconstructor working from the uploads would copy.** It therefore supports "faithful to the published canon" and does *not* discriminate H1 from H2. (I did not find this precedent recorded in FINDINGS §8, which reports the 2026 four-digit hand without noting the 2011 source; worth adding.)

**(iii) The profile result that looked decisive is killed by pose — and the control is the useful finding.** The 2026 Slim Tim's near-lateral facial profile is a textbook brow / sub-nasal saddle / protruding-chin S-curve (notch −0.050 ± 0.008, n=5), while every 2011 lateral view is a smooth convex arc with a receding chin (+0.009 ± 0.003, n=5) — a nominal 9σ gap. Before reporting it I ran the pose control: the **same 2026 subject, filmed 20 s earlier at three-quarter yaw, produces notch values of +0.058 and +0.064** (`profile_2026_threequarter.png`) — the metric flips sign with yaw and swings by 0.11, nearly twice the era difference. Every 2011 "profile" frame is yawed away from the camera by roughly 20–40°; the corpus contains **no pure lateral 2011 head view at usable scale**. I could not build an objective yaw proxy that works in 2011 (the face is too dark for the eye-inset measure to survive the contrast test in 10 of 12 frames). So the difference cannot be attributed to morphology. **Indeterminate, and I would treat any published claim resting on 2011-vs-2026 profile shape as unsafe unless it carries this control.**

**(iv) Craft: indeterminate, and probably unanswerable.** The 2011 ZB disc is consistently flatter in silhouette (W/H 3.42 ± 0.19 over 6 s) than the 2026 Mk.4 disc at matched apparent size (2.62 ± 0.08). But (a) they are different objects in-lore — 2011 Case 07 is the craft itself, 2026 Case 12 "Mk.4" is the human replica; (b) W/H depends on viewing aspect, which is unknown and varies within each run, so both figures are only lower bounds on diameter/thickness; (c) the two segmentations used slightly different thresholds (18 vs 16 DN) because the contrast differs. The 2011 disc is 180 px across with a 15–20 px PSF: no surface feature, rim geometry or dome ratio is recoverable from it, so the 2026 craft's rim, lip, fasteners and panel lines have **no 2011 counterpart to be checked against**. What can be said is qualitative and weak: both eras show the same lenticular family — domed top, flat-to-dished underside with a distinct equatorial lip (`context_2026_v1_ghostdisc.png`, `craft_2011_ZB_f00235.png`).

**(v) The asymmetry that actually matters is informational, not metric.** Almost everything the 2026 material renders in the face — supraorbital shelf, temporal fossae, a sagittal-ish crown ridge, vermiform crown wrinkling, a resolvable upper-lid rim with a specular arc, nostril pits, a lip line with a lower-lip highlight, an ear-analog flange behind the eye, and the glossy black digit caps — has **no counterpart anywhere in the 2011 record**, because in 2011 the entire face below the cranium is an unmodulated dark mask (measured: the face interior sits at 20–40 DN across x = 730–1170 at the eye rows of RsQ f1206, with the "nose bridge" only 15–25 DN above the eyes). Whoever produced the 2026 material had to invent that structure. That is neutral on its own — a genuine new source would also show detail absent from the old one — but it means the 2026 corpus offers no *testable* fine-morphological agreement with 2011 in the face, only in the hand, where the agreement exists and is copyable.

**Bottom line per subject:**

| Subject | Verdict |
|---|---|
| Head, frontal proportions | **Consistent** with the same subject type (moderate confidence) — but the discriminating power is low; within-2011 scatter swamps the era difference |
| Head, profile / mid-face structure | **Indeterminate** — pose-confounded, and 2011 supplies no pure lateral view |
| Head, fine facial morphology (lids, nostrils, ear, texture) | **Untestable** — absent from 2011 by construction |
| Hand | **Consistent** on digit count, arrangement and two of four proportions; **non-discriminating**, since the 2011 evidence is a plainly published frame |
| Craft | **Indeterminate** — different objects in-lore, uncontrolled aspect, 2011 resolution insufficient |

Nothing here is a reconstruction signature, and nothing here is a same-subject fingerprint. **Morphometry does not move the provenance question in either direction.** That is a real result given the hypothesis: H2 predicts errors in unseen angles and metric structure, and the honest finding is that the 2011 corpus does not contain enough metric structure to expose such errors even in principle. The one place H2 could have been caught — the hand, where 2011 does give a clean plate — the 2026 material matches it.

---

## 4. WHAT COULD NOT BE DETERMINED, AND WHY

1. **2011 posterior cranium / occiput.** In RsQ the subject's skin and the wall sit at the same luma (116–121 DN, difference < 5 DN over x = 1150–1450 at y = 150–250). Head length, cranial index, and any occiput-referenced ratio are unrecoverable.
2. **2011 crown-to-chin head height.** Clipped by the film aperture in every frontal frame from f1198 onward; in the earlier frames the head is pitched forward, so crown and chin are not simultaneously available at a usable pose.
3. **2011 eye landmarks.** The two eyes are never separable in RsQ — at the eye rows the whole face is a single dark region with a nose bridge only 15–25 DN brighter. Eye length, canthal positions, and inter-ocular distance are unmeasurable in the highest-resolution 2011 material. a6TL separates them, but at 640×480 with the bridge only ~8 DN above the eyes.
4. **Head-to-shoulder ratio.** Measurable in 2011 (RsQ f1170: 485/670 = 0.72) but not in 2026 — the walkabout figure's shoulders merge with a dark foreground on one side and a bright structure on the other (rows y = 700–760 are flat at 18–28 DN across the whole torso).
5. **2011 in-scene digit count.** The hands at the sides (RsQ f972–1032) are ~90 × 200 px with a 15–20 px PSF: 5–10 resolution elements. A high-pass pass on the raised hand (f1140–1160, `HPhand_01146.png`) shows 3–4 elongated ridges separated by inter-digital grooves — suggestive of four, not decisive. Registered averaging failed (the run is too short and the content changes).
6. **Digit tip caps in 2011.** The Xju plate is a solid ink impression, which carries no tip-surface information; the in-scene hands are below resolution. The 2026 caps are neither confirmed nor contradicted by 2011.
7. **An objective yaw measure for 2011 heads**, which is what would be needed to rescue the profile comparison. The eye-inset proxy requires ≥25 DN of skin-to-eye contrast and 2011 supplies it in only 1 of 5 near-lateral frames.
8. **Craft diameter/thickness in absolute terms.** Requires an assured edge-on view in each era; neither run provides one. The reported W/H values are aspect-dependent lower bounds on D/T.
9. **Whether the 2026 "Slim Tim" and 2011 "skinny Bob" are the same individual.** The morphologies differ visibly (Tim: narrow cranium, huge wrap-around eyes reaching the silhouette; Bob: cranium flaring well beyond the eyes), but both eras present multiple named individuals, so difference between *those two* is what the fiction itself asserts. The only same-name comparison available — 2011 Bob vs 2026 "Bob's walkabout" — is frontal-only on both sides and returns "consistent" (§1a).

One correction for FINDINGS: §8 records the four-digit hand as a 2026 finding. It has a 2011 precedent — the `Xju_CY5ZESA` hand-print plate, four digits, measured above — which changes how that observation should be weighted.
