# Agent report (verbatim): content physics + unexplored scenes (Case 22 head, col/s audio, walkabout)

Completed 2026-07-27. Final message verbatim:

---

All analysis complete. Here is my report.

---

# Report — three content leads, qtecqot 2026 videos

Working artifacts (all figures cited below): `/home/user/new-skinny-bob/analysis/scenes/`

---

## LEAD 1 — The "possible human head" in video 2, Case 22

### Localization

The ambiguous shape is a **discrete 29-frame shot, f1416–f1444** of `Oqw96jCOP7A` (video time 47.24–48.18 s). Hard cuts bracket it: mean-abs-frame-diff 16.6 DN at f1415→1416 and 12.1 DN at f1444→1445. Burned-in overlay reads `BL04 /22 00:30:26` for every frame of the shot (verified at f1416, f1420, f1444 — `c22_tc_check.png`); f1445 onward reads `BL04 /22 00:30:31`, the grey-type shot. So this is the **first second of Case 22 "Exit EBL04"**, immediately before the grey.

### Resolution: it is a human head. High confidence.

Method: NCC template registration of the head ROI (x 1000–1600, y 45–440) across all 29 frames with a ±60 px coarse / ±3 px fine search (NCC 0.87–1.00, smooth coherent trajectory spanning 75 px in x, 38 px in y — `c22_avg3.py`), then five-frame sliding aligned averages, unsharp mask (σ=3, 1.0×), 1–99 % stretch. Whole-shot averaging is useless (the head rotates); the five-frame groups are the readable product.

Resolved features, all present in ≥4 independent five-frame groups (`c22_head_groups.png`, `c22_face_frames.png`, annotated in **`c22_ANNOTATED_head.png`**):

- a **nose** with a distinct nostril/alar shadow
- a **moustache band** — a dark horizontal mass immediately below the nose
- **two lips**: a light upper-lip vermilion, a dark mouth line, a light lower lip with a specular highlight (clearest f1432–1444)
- a **full dark beard** covering the jaw, chin and lower cheek, with visible internal texture
- normal human facial proportions and spacing

Rotation test (`c22_head_rotations.png`): the crop reads as a face at 0° and degrades at every other angle, so the geometry is not a pareidolia of an arbitrarily-oriented shape.

This is categorically not the grey type. `c22_context_human_vs_grey.png` puts f1418/1432/1442 (human) beside f1450/1470/1520 (grey) at the same scale: the grey has the wraparound black eyes, no beard, no lips, cranial dome. The two are unmistakably different beings.

### Characterization

- **Framing:** the head is cut off at the **top of the film aperture** in every frame of the shot. The eyes and forehead are never visible. Only the lower ~40 % of the face is ever in frame.
- **Pose:** supine, head tilted back and to the left, seen from below/side — the same "casualty on a gurney" framing as the grey shot that follows.
- **Bedding:** lies on the same kind of bright white pillow/sheet as the grey. A pale shoulder/torso mass sits below-right.
- **Clothing:** none resolvable. No collar, no seam, no lapel. Bare or sheet-covered; cannot distinguish.
- **Consistency:** the face is present and stable in all 29 frames; features hold their relative geometry through the head's motion. No morphing, no feature drift.
- **Movement:** the mouth/lip configuration changes between the f1416–1428 group and the f1432–1444 group. I attempted a motion-compensated mouth-aperture metric (`c22_mouth.py`, `c22_mouth_metrics.png`) and it **failed** — the ROI-level registration is not accurate enough at ~15 px PSF, and the "dark band thickness" series (4–32 px) is dominated by tracking error. I cannot distinguish jaw motion (breathing/speaking) from head rotation. Undetermined.

### Lore significance

**This is the only human face in video 2**, and it has no counterpart in the 2011 corpus.

- Video 2's only other human presence is two distant walking silhouettes at Case 20 `00:03:55–56` (`Oqw96jCOP7A_c_02.jpg`, video t=32–33 s) — no faces.
- 2011 handlers, checked against the contact sheets and re-extracted frames: `a6TLGkrfNKI` t≈76–79 s shows the escort scene — humans appear **only as legs and torsos in dark trousers/uniform**, passing in the foreground (`ivan_a6t_escort.png`). `RsQCXN4o4Ps` 00:27:37–00:27:44 likewise shows bodies, never faces. **Across the 2011 set, no human face is ever shown.** 
- In-fiction it fits: the video's own title says "survival of EBL **Tim +2**", and Case 22 is "Exit EBL04". A human casualty in the adjacent bed, five source-seconds before the grey, is a coherent reading of "+2".

---

## LEAD 2 — Audio content of video 1's colour "(col/s)" segment

Everything here is new; prior work measured only RMS.

### The headline result: the colour segment's audio is a **different sound element**, not the projector bed turned up

This is the cleanest finding of the three leads, and I have high confidence in it.

The 2011/2026 projector bed is characterized by an amplitude-envelope modulation comb — an impulse train. Measured (`aud5.py`, `aud7.py`, `aud_modspec.png`):

| track | envelope-mod peak | prominence | spectral comb f0 |
|---|---|---|---|
| v1 b/w bed 55–80 s | 13.00 Hz | 20.9 dB | 13.032 Hz (16.5 dB mean harmonic excess) |
| 2011 `RsQCXN4o4Ps` | 13.25 Hz | 21.9 dB | 13.19 Hz (14.8 dB) |
| 2026 v2 | 14.00 Hz | 19.8 dB | 13.032 Hz (12.6 dB) |
| **v1 col/s 85.6–97 s** | **5.5 Hz** | **5.5 dB** | **12.54 Hz (1.4 dB)** — nothing |

Band-limited check (`aud9.py`), which rules out "the tick is just masked by louder rumble": in **every** band — 60–800, 800–2000, 2000–4000 and 4000–7000 Hz, including the top band where the two tracks sit at nearly the same absolute level — the bed shows 13.00 Hz at **18.0 / 19.0 / 20.6 / 18.6 dB** and the colour segment shows **4.5–6.0 dB at incoherent frequencies**. The projector bed is switched off for this clip and something else is switched on.

Corroborating: log-spectrum fine-structure correlation, bed ↔ 2026 v2 = **0.922** (same recording), bed ↔ col/s = **0.007** (unrelated); best correlation over all resampling ratios only 0.172, so it is not a pitch-shifted copy either (`aud5.py`).

**This is the one audio element in the entire 2026 corpus that is not derived from the 2011 sound bed.** FINDINGS §5b's 0.998 cosine to `RsQCXN4o4Ps` must come from the b/w portions.

### The element is cut to the picture

`aud10.py`, `aud_colseg_edges.png`. Level steps **+20.5 dB** (−34.7 → −14.2 dBFS). Rise crosses midpoint at **t = 85.680 s (frame 2568)**, 10–90 % rise **0.86 s** (a fade, not a butt cut); fall crosses at **t = 97.210 s (frame 2913)**. The colour picture runs f2571–2918. Alignment within **3 frames** at head and **5** at tail. "(col/s)" = colour/**sound** is implemented literally: this clip got its own audio.

### What is actually in it

**No voices. No speech. No language.** (High confidence.)
- Time-whitened narrowband spectrogram, 0–4 kHz, 43 ms hop (`aud_colseg_whitened.png` vs control `aud_bed_whitened.png`): no formant bands, no harmonic stacks, no F0 contours. Only broadband noise and occasional transients.
- Autocorrelation voicing test after notching all tonal lines (`aud8.py`): **1.4 %** of 40 ms frames exceed AC 0.5, with a **maximum continuous voiced run of 20 ms**. Bed control: 2.1 %, 20 ms. Pink-noise control: 0 %. Speech requires 100–300 ms continuous voiced runs. There is none.

**No music with movement, no rhythm.** All tonal components are frequency-constant across the whole 11 s (below). Waveform autocorrelation and spectrogram self-similarity find no loop (max off-diagonal similarity 0.31 at 21 ms = window overlap; nothing beyond — `aud_colseg_autocorr.png`).

**What it is:** broadband, low-frequency-weighted noise — roughly **+30 dB over the bed below 800 Hz, converging with it above ~2 kHz** (`aud_psd_absolute.png`) — plus exactly **six discrete stationary tones**.

Line inventory, single 11 s window, 4 Mpt FFT, excess over a 6 Hz-wide running median, strict 99.95 %-percentile carpet at 13.6 dB (`aud13.py`, `aud14.py`, **`aud_colseg_lines.png`**):

| Hz | dB over carpet |
|---|---|
| 95.913 | 14.7 |
| **99.907** | **23.3** |
| 107.906 | 13.8 |
| 119.888 | 14.3 |
| 143.864 | 19.9 |
| 191.814 | 16.7 |

Null rate for >13.6 dB at a random frequency: **0.10 %**. These six are unique to this segment — measured at the same six frequencies in v1's bed (two separate windows), v2 (two windows), 2011 Rs and 2011 ZB, all score ≤11.0 dB and mostly <8 dB.

Stability: 99.907 Hz tracked over 10 s in 2 s windows gives **99.906 ± 0.046 Hz**; 143.864 Hz gives 143.862 ± 0.034 Hz. No drift, no Doppler, no RPM ramp (`aud_100hz_track.png`, `aud_instfreq.png`). Phase-derived instantaneous frequency wanders with sd 0.058–0.12 Hz — about 10–20× more than a synthetic tone would at nominally matched SNR, though that control is imperfect.

### Mains frequency — 50 Hz if it is mains at all. Moderate confidence.

The dominant line, 99.907 Hz, is 2 × 49.954 Hz. Weaker companions sit at 49.85 Hz (8.2 dB) and 149.83 Hz (12.1 dB) — the 1st and 3rd of the same series, but both inside the noise carpet. A 60 Hz series is **not supported**: 58.95 Hz scores 5.5 dB and 180.5 Hz scores 3.9 dB. Above 200 Hz the 50 Hz harmonics are absent (n=4…12: 3.4, 0.2, 1.6, 8.8, 4.1, 4.7, −1.9, 4.0, 6.2 dB), which is thinner than a typical mains buzz.

So: **if any of these lines is mains hum, the grid is 50 Hz — Europe / Russia / most of Eurasia, and not North America.** 49.954 Hz is a completely ordinary instantaneous European grid value. I stop short of calling it mains outright because of the sparse harmonic ladder and the alternative below.

**The competing reading, stated for honesty.** All six frequencies are integer multiples of 3.9963 Hz (n = 24, 25, 27, 30, 36, 48; every residual <0.015 Hz). Equivalently they stand in the just ratios 1 : 25/24 : 9/8 : 5/4 : 3/2 : 2 above 95.91 Hz — unison, semitone, whole tone, major third, fifth, octave. That is a designed tonal cluster's interval set. **Against** it: only 6 of 43 multiples of 3.996 Hz exceed the carpet, so there is no actual dense comb; five of the six (n = 8, 9, 10, 12, 16 of 11.988 Hz) are also exactly what a rotating machine's blade-pass/gear-mesh harmonics look like, with 99.907 as an unrelated mains line on top. I cannot discriminate at this SNR. Also worth recording as a curiosity: 11.988 × 2 = **23.976 Hz = 24000/1001**, the NTSC film rate, matched to ~0.001 Hz.

### Speed correction: ×1.5 makes it worse — do not apply it

`aud16.py`, **`aud_speed_correction.png`**. The picture in this clip runs at 0.6735× (FINDINGS §11.2). Resampling the audio ×1.5 moves the line set to 143.9 / 149.9 / 161.9 / 179.8 / 215.8 / 287.7 Hz. **149.9 Hz is not a mains harmonic under 50 Hz or 60 Hz.** Only at the **native, unresampled** rate does the strongest line land exactly on a mains harmonic (2 × 49.95). Two consequences:

1. Present and analyse this audio at native speed. Speed-correcting it destroys the only physically-interpretable structure it has.
2. **The audio track was not time-stretched with the picture.** The 0.666× conform was applied to the image layer only, or the audio was laid in after the retime. This is a new, independent handle on the pipeline.

Same conclusion from the bed side, incidentally: the bed's 13.03 Hz tick is what a 24 fps projector gives at the **2011** 0.538× rate (24 × 0.538 = 12.9), not at 2026's 0.666× (which would give 16 Hz). The bed was copied, not regenerated for the new speed.

---

## LEAD 3 — Walkabout parallax and physics (video 2, Case 25)

Shot boundaries: **f1621–f1835** (215 frames, 7.17 s video, timecode `/25 00:02:07` → `00:02:12`). Cuts at f1620/1621 and f1835/1836 (mean-abs-diff 9.7 and 90.0 DN).

### First, a correction to FINDINGS §9.8

**"Bob's walkabout contains no walking — the figure stands in place" is wrong on the first half.** The figure's apparent size grows while the background does not:

| measurement | scale, f1625 → f1832 |
|---|---|
| figure (head+torso ROI, NCC scale search) | **1.18** (NCC 0.41); 1.08 at the midpoint f1730 |
| head-cap blob width, log-linear fit | 1.60 (log-residual sd 0.109 — noisy) |
| head-cap blob width, smoothed endpoints | 1.18–1.42 depending on smoothing |
| background building (NCC scale search) | 0.96 |
| background left terrain | 1.04 |
| background ground | 0.94 |
| background, affine fit to textured flow | 1.002 |

So the being closes roughly **20–35 %** of the camera distance (measurement-limited) against a background scale of **1.00 ± 0.05**. It approaches the camera. What it does *not* do is show any gait — see below. Net: it is a **dolly-less approach**, not a stand-still.

The approach is also **not steady**: `walk_physics.png`. Constant-speed fit (1/width linear in time) R² = 0.75 with visible systematic structure — the size increase is concentrated in f1660–1750 and flat after f1750. Caveat: the head-cap width proxy is confounded by head pose (the bright cap foreshortens when the head tips), which produces the spurious dip at f1630–1650.

### Camera motion: a large, rigid, quasi-periodic wobble — and no translation

Dense flow and phase correlation both fail on this footage; I report that as a measured limit below. What works is sub-pixel 1-D tracking of individual strong edges along fixed scanlines (`walk_edge.py`, `walk_edge_tracks.png`, `walk_kymographs.png`).

Six background edges tracked. They split cleanly into two families:
- **vertical-motion tracks** (V x=1300 @ y≈800 building base; V x=520 @ y≈500 left terrain): mutual correlation **+0.709**
- **horizontal-motion tracks** (H y=200 @ x≈1330; H y=430 @ x≈900; H y=880 @ x≈1150, plus the steeply-sloped V x=1300 @ y≈250 which projects into this family): mutual correlations **+0.35 to +0.66**
- cross-family correlations: **−0.33 to +0.14**, i.e. zero

That is the signature of a **single rigid 2-D field wobble** decomposed into independent x and y components. Amplitude, from the two faithful vertical tracks: **sd 23–26 px, peak-to-peak ~160–176 px**. Dominant period **25.6 frames = 1.17 Hz video rate = 1.76 Hz at source rate** — handheld-camera / walking-operator territory.

**Parallax test.** With background zoom = 1.00 there is no camera dolly, so the only parallax that could exist would come from a lateral translation component in the wobble. Depth-stratified test on the two vertical tracks (building base, nearer; left terrain, further): total-least-squares amplitude ratio **1.152, 95 % CI ±13 %** (n=214, r=0.708). Consistent with 1.00 at ~1.2σ. **No differential parallax detected, sensitivity ~±13 %.**

Honest limitation: this is a **null with limited power to discriminate**. A pure camera *rotation* over a genuine 3-D scene produces exactly this result too. The test cannot separate "panning camera, real 3-D scene" from "wobble applied to a flat plate." What it *can* say is that nothing anomalous is present — no region moves differently from any other.

### The figure is locked into the camera motion — a positive coherence result

`walk_gait.py`, **`walk_gait.png`**. The head-centre y residual (about its smooth trend) correlates **+0.835** with the background y wobble, and both peak at the same 1.17 Hz. In x: **+0.666**. The being is embedded in the same camera shake as the background, frame for frame.

Two readings follow:
1. Pro-coherence: a naively composited or independently-generated figure would not lock this tightly to the plate's shake.
2. **No gait.** The 1.17 Hz "bob" is the camera, not the being. After subtracting the background wobble the head's residual motion has no dominant periodicity (peak drops to 0.23 Hz, power/median 44 versus 231 and 446 for the two raw signals). A walking biped at ~1.8 Hz step rate would show a head bob at that frequency **relative** to the background. There isn't one. So the figure approaches without a detectable walking oscillation — glide rather than gait.

Head amplitude is 38 % larger than background amplitude at the shake frequency (31.6 vs 22.9 px). Most likely thresholded-blob centroid noise; a translational-parallax explanation would require the background to be only ~1.4× further away than the being, which the scene contradicts.

### Foot–ground contact: NOT TESTABLE

The being's feet are never in frame. `walk_feet.png`, `walk_bottom_1832.png`: the lower body is a near-black mass; the aperture bottom is at y≈1035; the burned-in `/25 00:02:1x` timecode sits across y 900–1000, exactly where the feet would be. Below y≈900 the silhouette is unresolvable at any stretch. No foot-plant, no shadow contact, nothing to measure. This is a lead the footage cannot answer.

### Occlusion / background regeneration: no repaint halo, no popping

Two independent tests, both null (which favours coherent material):

1. **Repaint-halo test** (`walk_halo.py`, `walk_halo.png`). For frame pairs Δ=15 across the shot, mean |ΔI| as a function of distance outside the figure silhouette, normalized by local gradient magnitude. Raw change does rise near the figure (14.5 DN at 0–20 px vs 6.2 DN at 220–240 px) — but so does the local gradient (6.97 vs 3.02), because the figure sits in the most detailed part of frame. Normalized: **2.21 near (0–40 px) vs 2.13 far (≥120 px), a +3.4 % excess**, and the ratio actually peaks at 60–100 px, not at the boundary. No boundary-localized excess change. Generative repainting around a moving subject would produce a clear hugging halo. There isn't one.

2. **Kymographs** (`walk_kymographs.png`), six scanlines through the shot. Every background structure traces an **unbroken continuous line across all 215 frames**. No structure appears, disappears, pops, splits or reforms. Median frame-to-frame step of the strongest edge: 0.00–1.00 px on four of six lines. The wobble is large but the *content* is stable.

Caveat that limits how far the occlusion result generalizes: **there is no genuine re-reveal in this shot.** The figure grows and translates right; it never retreats far enough to uncover a substantial patch of previously-hidden background cleanly. My silhouette segmentation (`walk_sil.py`) leaks into the dark left terrain and dark building shadow and is not trustworthy for a precise uncover measurement. The classic "does the background come back the same after occlusion" test is simply not available in this shot.

---

## What could not be determined, and why

1. **Whether the Case 22 human is speaking or breathing.** Motion-compensated mouth metrics failed at ~15 px PSF; head rotation and jaw motion are not separable. Would need a shot with the head static relative to camera; there isn't one.
2. **The Case 22 human's clothing, eyes, hair colour, age.** The aperture amputates the face above the nose in all 29 frames, and the effective resolution (a few hundred pixels across frame, per FINDINGS §9.6) puts collars and seams below the resolution limit in principle.
3. **Whether the 99.907 Hz tone is mains hum or a member of a designed tonal cluster.** Both hypotheses fit the six measured frequencies. The mains reading rests on one strong line with two weak companions; the cluster reading rests on a just-intonation ratio coincidence I chose the base frequency to fit. Distinguishing them would need either a longer sample or an independent copy of the source element.
4. **Whether the walkabout background is a real 3-D scene.** The camera does not translate, so parallax cannot arise regardless. The null (near/far amplitude ratio 1.15 ± 0.13) is real but has no power against the flat-plate hypothesis. Would need a shot with genuine lateral camera travel.
5. **Foot–ground contact anywhere in the walkabout.** Feet never enter frame; the timecode overlay occupies the relevant band.
6. **Background stability through a true occlusion cycle.** No re-reveal occurs in this shot. A different shot with a subject crossing in front of textured background would be needed.
7. **Whether a human face appears anywhere in videos 1 or 3.** I verified video 2 (only the Case 22 face plus two distant silhouettes at Case 20 `00:03:55–56`) and all four 2011 videos (humans appear only as legs/torsos in dark clothing, never a face). Videos 1 and 3 were not swept for this.

## Method notes worth carrying forward

- Dense optical flow (Farneback), phase correlation on windows, ECC affine registration and long LK feature tracks **all fail** on video 2's walkabout footage. Control measurement: adjacent-frame-pair "motion" over a 3-frame gap (5.6 px mean) is nearly as large as over a 207-frame gap (7.8 px), i.e. these estimators are noise-dominated. Anyone reporting flow-derived numbers on this footage without that control is reporting noise. **Sub-pixel 1-D edge tracking along fixed scanlines is the estimator that works** (median step 0.95–6.6 px, and clean two-family correlation structure).
- For the audio, envelope-modulation spectra computed **per frequency band** are the discriminator that settles "different element vs same element amplified"; broadband RMS and even full-band modulation spectra do not.
- Frames-not-time: the audio and picture of video 1's colour clip are on **different time bases**. Any future audio/picture sync work on these files must not assume the audio shares the picture's retime.
