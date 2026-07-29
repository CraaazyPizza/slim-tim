I have everything I need. Here is the report.

---

# Mk.5 colour segment (video 1, `OpSTlDJWFFI`) — independent test of u/Outrageous_Courage97's two claims

Analyst working directory: `/home/user/new-skinny-bob/analysis/mk5-colour-segment/`
All frame numbers are 1-indexed PNGs in `/home/user/new-skinny-bob/frames/OpSTlDJWFFI/`, 1920×1080, 29.97 fps.
Everything below separates **measurement** (numbers, reproducible) from **interpretation** (labelled as such).

---

## 1. Segment survey and what is in it

### 1.1 Boundaries — corrected

Saturation (mean of `max(R,G,B) − min(R,G,B)` over x 400–1500, y 200–900) sits at ~6 DN through the monochrome material, jumps to 23 DN at **f2571**, and drops back to 6 DN at **f2918**.

**The colour segment is f2571–2917 inclusive: 347 frames, t = 85.75–97.33 s.** The brief's upper bound of 2990 overshoots — f2918–2970 is black leader, and f2971–2974 is the already-catalogued four-frame insert (FINDINGS §2c). FINDINGS §2b's "t ≈ 85.8–97 s" is correct.

### 1.2 Content

One continuous handheld shot, no cuts (largest frame-to-frame mean-abs-diff is 20.4 DN at f2905, which is the terminal white-out, not a discontinuity; median 2.15 DN).

Survey sheets: `sheet_clahe_all.jpg` (58 tiles, every 6th frame, CLAHE-lifted — the frame-by-frame survey of record), `sheet_A.jpg` / `sheet_B.jpg` (native), `sheet_late.jpg` (f2820–2917 at 2-frame steps), `full_clahe_2620.png`, `full_clahe_2760.png`.

The camera is inside a dark structure looking out through a large rectangular opening with a rounded top-left corner. Left two-thirds of frame is unlit interior dominated by a vertical structural post. Outside: a high-altitude view over a plain/coastal landscape with a cloud deck near the top of the aperture.

A **white lenticular craft** flies in the opening and drifts left while receding:

| frame | convex-hull major axis (apparent length) | position angle |
|---|---|---|
| 2571 | 425 px | 8° |
| 2661 | 387 px | 17° |
| 2751 | 279 px | 28° |
| 2781 | 206 px | 38° |
| >2830 | occluded by the post / unresolvable | — |

So over the usable span the craft's apparent size **halves** and its position angle rotates **30°**. This matters for §3: the viewing geometry changes a lot.

### 1.3 Every reflective surface and every candidate marking

- **The craft's upper surface** is the only bright/specular surface in the shot. Fitting a 4th-order 2-D polynomial to the shading over a 50-frame registered stack leaves a residual of **σ = 2.53 DN** over the whole craft and **σ = 1.07 DN** over a clean dome patch (`dome_polyresid.png`, `dome_highpass_s{8,16,30}.png`). There is **no secondary image, no reflected horizon, no reflected aircraft, no reflected cloud deck, no marking** — the surface renders as a smooth diffuse body with one broad specular lobe.
- **The single exception** is one dark elongated wedge on the lower-front of the visible surface, at **x 1306–1500, y 578–668** at f2571–2620 (194 × 90 px), 145 DN below the surrounding hull. This is the only non-smooth feature anywhere on the craft, and it is what claim (b) is about.
- **The interior** is matte, unlit, and heavily block-posterized by AV1 (`interior_gamma.png`). It carries a vertical ladder-like row of ~10 evenly spaced horizontal marks at ~30 px pitch down the left edge of the post (`interior_ribs2.png`, `interior_stacks.png`), and a small bright fitting near the post's top (~x 590–640, y 180–230). No text, no insignia.
- **The landscape** carries a single bright diagonal line from ~f2751 onward (road/river/coastline; it scrolls with the terrain).
- Burned-in overlay `T6-02/31` + timecode; Russian caption from f2603.

**No insignia of any kind exists anywhere in this segment above the measured noise floors.**

---

## 2. The five-pointed star claim — evidence and verdict

> *"clearly see a military (at least one big 5 spikes star, could be sovietic…)"*

### 2.1 Automated search

Matched-filter survey over 174 frames (every 2nd frame of the segment), 6 scales (24–140 px outer diameter), on locally-normalized half-resolution frames with the film matte and the caption/timecode band masked. Three template families were run **against each other as controls**: 5-pointed star (6 rotations), 6-pointed star (4 rotations), and a near-circular disc.

The controls are the point. A real five-pointed star produces a response that a 6-point and a disc template cannot match. Observed:

| scale (full-res px) | star5 max | star6 max | disc max |
|---|---|---|---|
| 24 | 11.66 | **12.65** | 11.01 |
| 36 | **15.82** | 15.28 | 12.34 |
| 52 | 16.98 | **18.67** | 16.19 |
| 72 | 21.72 | **22.92** | 19.18 |
| 100 | 26.56 | 27.56 | **28.41** |
| 140 | 33.88 | **35.70** | 30.87 |

The 5-point template **never wins**. Specificity ratio star5 / max(star6, disc) over all 1,044 (frame × scale) cells: **mean 0.952, σ 0.058, max 1.191**. The top-ranked cells cluster at f2745–2755 near (1140, 520), f2833–2843 near (830, 575) and f2859–2863 near (790, 565) — all of which are simply the craft's bright blob (`star_candidates.png`; visual inspection confirms). The detector is responding to generic blobs, which is what it does on an image with no star in it.

### 2.2 Direct limit on the craft's hull

The hull is where a national insignia would sit and where the noise floor is best. Matched-filter SNR of an injected star against the measured 1.07 DN dome floor:

| star size | 5 DN contrast | 10 DN | 20 DN |
|---|---|---|---|
| 40 px | 9.9σ | 19.7σ | 39.5σ |
| 60 px | 14.8σ | 29.6σ | 59.2σ |
| 100 px | 24.7σ | 49.4σ | 98.7σ |

Nothing is present. **A hull insignia down to ~5 DN contrast is excluded at ≥10σ.**

### 2.3 Injection control — the honest caveat

`FIG3_star_injection.png` shows a real 70 px five-pointed star pasted onto the craft in the 50-frame stack at 8, 16 and 35 DN. At the measured PSF (§4): 8 DN is invisible; 16 DN is a faint mottle; **35 DN is a clearly visible dark blob whose five-pointedness is only marginally readable.** Below roughly 100 px, a genuine star renders as a rounded dark patch, not as points.

Two consequences, both worth stating:
- A **large, high-contrast** star would have been found. None is.
- Even if one existed at 60–80 px, **nobody could honestly "clearly see" five spikes** on this footage. The claim's own confidence level is not achievable here.

### 2.4 Chroma and visual sweeps

Red-excess survey (`r − (g+b)/2`, Gaussian σ6, every 3rd frame): median peak 14.4 DN; the single outlier is 99 DN at f2679 (344, 673) — a broad orange flare washing the interior wall, not a compact mark (`other_features.png`). Full 58-tile CLAHE contact sheet and the 49-tile late-segment sheet: nothing star-like at any point.

### 2.5 Verdict on claim (a)

**REFUTED** as stated. No five-pointed star exists on the craft, on the interior structure, or anywhere in the well-lit portion of the frame, at any scale from 24 to 140 px, in any of the 347 frames. The one region where the claim is merely **UNDETERMINABLE** is the deepest interior shadow (mean luma ~30 DN with heavy AV1 posterization) — but nothing star-shaped appears there either, and a star hidden in unlit shadow is not "clearly seen".

*Interpretation, offered separately:* the KGB shield-and-sword crest that Gemini read in 2011 `ZB788PtqQvg` (FINDINGS §23) is the most plausible source of a Soviet-insignia memory being transposed onto this segment. That is a guess about how the claim arose, not a measurement.

---

## 3. The Chinook reflection claim — evidence, controls, and verdict

> *"we can see the reflect on the craft of what seems to be a Chinook … we can see the movement of the 2 rotors plus the caracteristic Chinook form in the reflect (minus deformation of the reflect)"*

The object being described can only be the dark wedge, since it is the only non-smooth feature on the craft (§1.3). Seven independent tests follow. All fail the claim, in both halves — it is not a reflection, and it is not a tandem-rotor helicopter.

### 3.1 It is fixed in craft coordinates, not sliding like a reflection

229 frames were resampled into a canonical craft frame (translation + rotation + scale normalized using the **convex hull** of the craft mask, which is insensitive to the notch the dark feature cuts into the boundary). `canon_montage.png` shows the result; `canon_mean_all.png` is the 229-frame mean, in which the feature survives sharply — it registers.

Differential shift of the feature region against the dome region, per frame, by sub-pixel NCC:

- **dx: σ = 4.55 canon px = 2.1 % of disc length**
- **dy: σ = 2.29 canon px = 1.1 %**
- total systematic drift over the whole segment: −0.040 canon px/frame ≈ 9 px ≈ **4 % of disc length**

Over that same span the craft's apparent length halved and its position angle rotated 30°. A specular reflection of an external object under that much geometry change traverses a large fraction of the reflecting surface. This does not move.

### 3.2 Single apex, not two pylons — the decisive morphology test

The upper boundary of the dark feature was traced (brightest pixel per column, then first dark run below it) and smoothed. Applied to **four independent registered stack windows** and to **twelve individual unstacked frames**:

| source | apex x | apex y | humps |
|---|---|---|---|
| stack f2571–2620 | 1327 | 581.3 | **1** |
| stack f2575–2610 | 1327 | 581.8 | **1** |
| stack f2611–2646 | 1328 | 576.3 | **1** |
| stack f2647–2682 | 1332 | 575.1 | **1** |
| f2573 … f2617 (12 single frames) | 1324–1329 | 578–584 | **1** each |

Profile: y = 592 (x1310) → **581 (apex, x1327)** → 595 (x1360) → 618 (x1410) → 635 (x1460). One hump, then monotonic descent.

The same measurement applied to a rendered CH-47 side profile at matched span and matched PSF returns **two** prominent humps (prominences 3.5 px and 15.6 px) — the low forward pylon and the tall aft pylon. That is the defining silhouette feature of a tandem-rotor helicopter, and it is a coarse, large-scale feature that survives the blur. It is absent.

The stability across four stack windows *and* twelve unstacked frames is the control against stacking artifacts flagged in the brief: the apex is not a product of registration.

### 3.3 No rotor smears where they would have to be — a 21σ absence

`power2.py`: a CH-47 rendered at 215 px total rotor-tip span and blurred to the measured PSF has spinning-rotor smears of peak opacity **0.366** (= a **53 DN dip** at the observed feature's 145 DN contrast depth), overhanging the fuselage core by **54 px front and 56 px rear**, plus a rotor plane above the mass.

Measured residuals in exactly those zones on the 50-frame registered stack (`FIG1_feature_annotated.png`, which marks the zones):

| zone | residual σ | min / max |
|---|---|---|
| forward rotor-tip zone (x 1240–1305) | **1.41 DN** | −12.9 / +7.5 |
| rotor-plane zone (x 1300–1500, y 505–565) | **5.11 DN** | −13.8 / +15.8 |
| aft rotor-tip zone (x 1500–1560) | **4.86 DN** | −13.9 / +14.3 |
| clean-dome control | 1.07 DN | −4.4 / +6.1 |
| the feature core itself | 14.87 DN | −41.2 / +46.9 |

Required: 53 DN. Observed extremes: ≤16 DN. **The rotors are absent at >10σ in every zone.**

### 3.4 No rotor motion — the "movement of the 2 rotors" test

129-frame registered cube (f2571–2699, 4.3 s), cubic detrend, Hann window, per-pixel temporal FFT, averaged by region:

| region | peak | prominence over median |
|---|---|---|
| dark feature body | 0.232 Hz | 85× |
| feature head | 0.232 Hz | 100× |
| bright hull | 0.232 Hz | 144× |
| **sky background (control)** | 0.232 Hz | **185×** |
| dark under-region | 0.232 Hz | 235× |

Every region peaks at the same 0.232 Hz — the window-scale residual drift — and the peak is **strongest in the sky control**, weakest in the feature. No line at any candidate blade-pass frequency; power at the 2.4975 Hz period-12 conform frequency is no higher in the feature (3.5e3) than in the sky (1.7e3). Broadband 1–15 Hz power ratio feature/sky = 1.58, which the temporal-σ map explains completely: `feat_W1_f2575_2610_std.png` shows variance concentrated on the feature's **outline**, the signature of sub-pixel registration jitter at high-contrast edges, not two compact rotating discs.

### 3.5 Shape match — the CH-47 is the worst fit of four tested

Best scale-optimized NCC of the observed ink map against silhouettes rendered at matched span and blurred to the measured PSF (`FIG2_chinook_comparison.png`, `silhouette_comparison.png`):

| candidate | NCC |
|---|---|
| **plain tapering wedge** | **0.653** |
| single-rotor helicopter (UH-1) | 0.381 |
| fixed-wing aircraft | 0.379 |
| **CH-47 tandem-rotor** | **0.330** |

Of the four shapes tested, the Chinook is the *least* consistent with the pixels.

### 3.6 Deconvolution finds nothing more — with a control that shows why to be careful

Richardson–Lucy at σ = 4, 6, 8 (40–80 iterations) on the 50-frame stack (`feature_deconvolution.png`) sharpens the wedge into a blunt notched head plus a long taper. **No rotors, no second pylon appear at any setting.** The bottom two panels are the control: the same deconvolution applied to a genuinely featureless dome patch invents banded structure. Any "detail" read out of deconvolved views of this footage must be discounted accordingly.

### 3.7 The same feature is on a *different* craft, in a *different* shot, ~50 s earlier, in monochrome

This is the finding that closes the question. Video 1's black-and-white **Case 12 "Mk.4"** sequence (f1290–1900, burned-in `/12 01:10:55–01:11:07`) shows a lenticular craft at **430–500 px apparent width — better resolved than the colour Mk.5's 380 px** — carrying the same bright-dome-plus-dark-lower-region morphology, at several different orientations.

`FIG4_mk4_vs_mk5_hull.png` and `FIG5_hull_feature_scale_matched.png` (all four discs normalized to the same width) show it directly. At 450 px the Mk.4's dark region resolves as a smooth shadow gradient — the shaded underside of the overhanging rim — with no internal structure whatsoever, and certainly no helicopter.

A helicopter reflected in the Mk.5's hull cannot also be present on the Mk.4's hull in a monochrome shot from a different claimed case and tape fifty seconds earlier in the same video. The feature is a **design and lighting property of this craft family**.

### 3.8 The claim's own hedge is self-defeating

"minus deformation of the reflect" cannot be granted and withheld at once. If the reflection is distorted enough to erase both rotor discs — which are the largest elements of a Chinook, spanning nearly twice the fuselage length — then it cannot simultaneously preserve "the characteristic Chinook form". A convex mirror compresses an image; it does not delete the object's largest features while keeping the small ones.

### 3.9 Verdict on claim (b)

**REFUTED**, on both halves independently:

- **Not a reflection.** Fixed in craft coordinates to within 2 % of disc length across a 2× scale change and a 30° rotation (§3.1); present on a different craft in a different shot in monochrome (§3.7); and sitting on a surface whose measured residual is 1.07–2.53 DN, i.e. a surface that reflects *nothing else at all* — no horizon, no cloud deck, no observing aircraft (§1.3).
- **Not a Chinook.** One apex where a tandem rotor requires two pylons at different heights (§3.2); rotor smears absent at >10σ in all three zones where they would have to appear (§3.3); worst shape match of four candidates (§3.5).
- **"Movement of the 2 rotors": REFUTED.** No temporal periodicity anywhere; the only excess variance is edge jitter, and the strongest low-frequency signal is in the empty sky (§3.4).

*On the anachronism question:* moot, because there is no helicopter. Noted for the record only — had one been there, a 21 September 1961 first flight against a caption reading «1961 год» would be a period-boundary coincidence rather than a clean anachronism, and would not have been decisive either way.

*Best positive interpretation of the wedge (offered as interpretation, not measurement):* the shaded underside/rim of a lens-shaped body, possibly combined with a dark equatorial slot. The Mk.4 comparison at higher resolution supports this reading. It is not established, and it does not need to be — the claim fails regardless of what the wedge is.

---

## 4. Resolution limits: what is knowable here at all

Measured on f2600 in the craft region:

| measurement | value |
|---|---|
| edge-spread σ, craft top edge (two cuts) | 8.13 / 8.40 px |
| **PSF FWHM** | **19.1 / 19.8 px** |
| 10–90 % rise | 16–21 px |
| radial power falls to 1e-4 of DC at | 0.068 cyc/px (≈ 15 px period) |
| reaches AV1 reconstruction floor by | ~0.15 cyc/px |

**Smallest genuinely resolved feature: ~15–20 px.** The dark wedge (194 × 90 px) is therefore about **10 × 5 independent resolution elements**.

What that permits and forbids, stated carefully:

- **Recoverable.** Whole-object topology. My rendered CH-47 at exactly this span and PSF *still shows* two pylons at different heights and two rotor smears overhanging both ends (`synth_ch47_at_measured_psf.png`, `synth_ch47_rotors_only.png`). Tandem-rotor architecture is a coarse property and it survives 19 px blur. **This is not a case where "the resolution makes everything unknowable" — the test had real power, and the claim failed it.** That distinction matters: the refutation is positive, not a shrug.
- **Not recoverable.** Rotor blade count, hub or mast detail, windows, ramp, engine nacelles, tail geometry, national markings, or anything finer than ~20 px. **No specific helicopter type could be identified from this footage even if a helicopter were present.** Anyone naming a model from these pixels is overclaiming.
- **Star insignia.** A five-pointed star needs >~100 px for its points to read as points. Below that a genuine star renders as a rounded dark blob (`FIG3_star_injection.png`). "Clearly see a big 5 spikes star" is not an achievable observation on this material.
- **Compression.** The bright hull is clean (1.07 DN floor). The dark interior is not: heavy AV1 block posterization destroys low-contrast structure in shadow (`interior_gamma.png`). Negative results in the shadows are weak; negative results on the hull are strong.

---

## 5. Other findings (checked against FINDINGS first — new or refining only)

**a. Exact bounds.** f2571–2917, 347 frames, t 85.75–97.33 s. Consistent with §2b.

**b. Full timecode range.** The overlay runs `T6-02/31 00:57:56` → `00:58:03` — eight one-second ticks. FINDINGS §2b records only "00:57:56…59". The claimed catalog is 00:57:56 – 00:58:04, so the clip is cut **18 frames before :04 would tick** — the same endpoint-shortfall convention documented in §11.6, now confirmed for the colour clip. Evidence: `tc_strip.png`, `tc_transitions.png`.

**c. Cadence discrepancy with §11.2 — flagged for re-measurement.** Frame-precise tick boundaries from last-digit correlation strips: **:58→:59 at f2705, :59→:00 at f2751 — exactly 46 frames.** The first clean ":01" appears at f2797 (= 2751 + 46), and an independent coarse change-detector hits f2660 (= 2705 − 45), consistent with a 46-frame grid at 2613, 2659, 2705, 2751, 2797, 2843, 2889.

That gives **46.0 frames per burned-in source second = 0.6515× playback for the colour Mk.5 clip — the same as video 1's b/w fragments**, not the 44.5 / 0.6735× recorded in FINDINGS §11.2. If this replicates, §11.2's claim that "the colour clip is retimed 3.4 % differently from the b/w clips within the same video" should be withdrawn. I record this as a **measured discrepancy, not a settled correction** — two clean intervals both give 46, but two of the seven boundaries fall behind bright flares and could not be read directly.

**d. Caption timing refined.** «Самолет Mark 5 (1961 год» switches on abruptly between f2599 and f2603 (no fade-in), holds full amplitude to ~f2664, then fades out over ~35 frames to ~f2698. §2b's "frames ~2590–2670" is close; the onset is f2603 and there is a fade tail.

**e. Period-12 conform is only weakly expressed here.** 3 near-identical consecutive pairs in 346 frames, **all at phase 10 mod 12**. Consistent with §11.3's "moves smoothly every output frame", but it shows the same 12-frame grid is still underneath the colour clip.

**f. Interior structure detail (not in FINDINGS).** A vertical ladder-like row of ~10 evenly spaced horizontal marks at ~30 px pitch runs down the left edge of the interior post, with a small bright fitting at the post's top (~x 590–640, y 180–230). `interior_ribs2.png`, `interior_stacks.png`. Reads as rungs, hinges or louvres on a structural member. No text, no insignia.

**g. Landscape line.** A single bright diagonal crosses the terrain from ~f2751 to the end. It scrolls with the landscape — a road, river or coastline, not a tether or contrail.

**h. Strongest chroma event in the segment** is a broad orange flare washing the interior at f2679 (red excess 99 DN at (344, 673) vs a 14.4 DN segment median). It is a lighting/flare event, not a mark. Possibly one of the four luma-independent colour events recorded in §17.

**i. The best-resolved craft material in the corpus is the b/w Mk.4, not the colour Mk.5.** 430–500 px discs in Case 12 versus 380 px here. Anyone studying craft morphology should be working there.

---

## 6. Recommended follow-ups

1. **Independently re-measure the colour clip's frames-per-tick** (item 5c). If 46.0 replicates, correct FINDINGS §11.2 and withdraw the "colour clip retimed differently" claim.
2. **Ask LC for a frame timestamp and a screenshot** pinpointing both the star and the "two rotors". The machinery in `/home/user/new-skinny-bob/analysis/mk5-colour-segment/` can adjudicate any specific pixel location in minutes. Absent a pointer, this report tests the claims at every location and scale in the segment.
3. **Give the Mk.4 b/w sequence (f1290–1900) the treatment I gave the colour clip.** It is the highest-resolution craft material available (450 px discs) and I only sampled it. Specifically: f1442–1494 contains an unidentified object with repeated dark elements at frame right that I did not analyse.
4. **Test whether the Mk.4 and Mk.5 hulls are literally the same 3-D asset** — fit both to a common lens-of-revolution model and compare the dark region's angular extent and the rim profile. That would put the in-lore "Mk.4 vs Mk.5" distinction against production reality (one model reused, or two).
5. **No audio re-examination is warranted.** §19/§20 already establish no speech in this segment from two independent directions, and nothing I found visually justifies reopening it.

---

## Figure index

Headline evidence, in the order used:

| file | what it shows |
|---|---|
| `sheet_clahe_all.jpg` | the frame-by-frame survey of record — 58 CLAHE-lifted tiles covering f2571–2917 |
| `craft_annot_f2600.png` | iso-luma contour map delineating craft body vs dark wedge vs background |
| `canon_montage.png`, `canon_mean_all.png` | 229 frames resampled into canonical craft coordinates; the feature registers |
| `FIG1_feature_annotated.png` | measurements: 194×90 px feature, single apex x=1327, and the three rotor zones with their residuals |
| `feat_W1_f2575_2610_std.png` | temporal-σ map — variance sits on the feature *outline* (edge jitter), not in two compact discs |
| `FIG2_chinook_comparison.png` | observed feature vs CH-47 / UH-1 / plain wedge, all at 215 px span and the measured PSF |
| `synth_ch47_at_measured_psf.png`, `synth_ch47_rotors_only.png` | what a Chinook *does* retain at this resolution |
| `feature_deconvolution.png` | Richardson-Lucy at three settings, with the featureless-patch control that shows the ringing it invents |
| `FIG4_mk4_vs_mk5_hull.png`, `FIG5_hull_feature_scale_matched.png` | the same hull feature on the b/w Mk.4 at higher resolution — the finding that closes claim (b) |
| `dome_polyresid.png` | the craft's surface after shading removal: 2.5 DN, no reflection of anything |
| `star_candidates.png` | the five top-ranked 5-point-star hits: all are the craft's bright blob |
| `FIG3_star_injection.png` | detection limit — a real 70 px star at 8 / 16 / 35 DN on this hull |
| `tc_strip.png`, `tc_transitions.png` | timecode range :56→:03 and the frame-precise tick boundaries |
| `interior_ribs2.png`, `interior_stacks.png` | the interior post's rung row |

---

## Verdict summary

| claim | verdict | one-line basis |
|---|---|---|
| (a) five-pointed star insignia in this segment | **REFUTED** (UNDETERMINABLE only in the deep interior shadow) | 5-point template never beats 6-point or disc controls in 1,044 cells; hull insignia excluded to ~5 DN at ≥10σ; nothing star-like in 347 frames |
| (b) reflection of a tandem-rotor helicopter on the craft | **REFUTED** | fixed in craft coordinates to 2 % across a 2× scale change; present on a different craft in a b/w shot 50 s earlier; one apex not two pylons; rotor smears absent at >10σ; worst NCC of four shapes |
| (b′) "movement of the 2 rotors" | **REFUTED** | no periodicity in any band; peak temporal power is in the empty sky, not the feature |
| identification of a *specific* helicopter type from this footage, had one been present | **impossible in principle** | 19 px PSF; the wedge is ~10 × 5 resolution elements |