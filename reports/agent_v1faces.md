All analysis complete. Report follows.

---

# Video 1 (`OpSTlDJWFFI`) — testing four outside-analyst claims, plus a full-video human-face sweep

Working directory: `/home/user/new-skinny-bob/analysis/faces/` (71 saved images; every conclusion below cites the file it rests on).

---

## 1. Method and controls used

**Baseline look.** Every claimed range was first inspected as unmodified full-resolution PNGs and as gamma-lifted (γ 0.30–0.45) frames before any stacking. Whole-video contact sheets at 1-in-6 frames with shadow lift: `sweep_0001_0595.png`, `sweep_0601_1195.png`, `sweep_1201_1795.png`, `sweep_1801_2395.png`, `sweep_2401_2995.png`.

**Registration + stacking (the §-scenes ladder).** Chain-tracked NCC template registration with adaptive template refresh and parabolic sub-pixel refinement (`track.py`), sub-pixel bicubic shift and windowed averaging (`stack.py`), then unsharp mask (σ 3–6, amount 1.3–1.6) and 0.5–99.5 % percentile stretch. Tracking quality was logged per frame; frames with NCC < 0.75–0.8 were excluded from stacks. Typical track NCC 0.98–1.00.

**Effective resolution.** Measured directly as the 10–90 % rise of the steepest edges in each shot (10th-percentile over ≥100 scanlines):

| shot | 10–90 % rise |
|---|---|
| f1200 (disc / Case 11) | 23 px |
| f1510 (insignia region) | 13 px |
| f1540, f1548 (head shot) | 18, 16 px |
| f1620 (later Case 12) | 20 px |

So the effective PSF is **≈13–23 px 10–90 %, i.e. FWHM ~12–21 px, one resolution element ≈15–18 px**. Every size claim below is converted into resolution elements.

**Controls run.**
- (a) **Rotation** — the candidate face crop rotated 0/45/90/135/180/225/270/315° plus mirror (`c2_rotation_control.png`).
- (b) **Independent windows** — five strictly non-overlapping 5-frame stacks, plus five *unstacked single raw frames* processed identically (`c2_independent_windows.png`).
- (c) **Matched control regions** — five same-size ROIs elsewhere in the same shot, tracked and stacked with the identical pipeline (`c2_control_regions.png`).
- (d) **Cross-object identity control** — the candidate placed beside video 2's known grey (`Oqw96jCOP7A` f2200) and video 2's known human (Case 22 f1438) at matched scale (`c2_compare_human_vs_grey.png`).
- (e) **Rotational-symmetry test** for the alleged star: k-fold self-correlation for k = 2…8 and angular peak counting at three radii.
- (f) **Raster-lock test** for added elements: independent NCC tracks on four disjoint ROIs (near-field structure, far-field object, candidate element, rivet line) to see which moves with the picture.

---

## 2. CLAIM 1 — "human face at f1210–1247, adhesive tape added at f1225 to mask the eyes"

### What is actually there (unaided)

f1210–1247 is one continuous shot of **Case 11, overlay `/11 00:33:33`→`00:33:34`**: a large overexposed lenticular disc filling the left two-thirds of the aperture, seen past an aircraft window frame on the right that carries a clearly resolved **line of rivets** (`c1_full_aperture_stack.png`). No face is visible unaided, and none appears after enhancement.

### Enhancement and controls

- Motion-compensated stacks over the shot, local-contrast normalised so both the blown disc and the dark right side are legible: `c1_localcontrast_groups.png`, `c1_full_aperture_stack.png` (11-frame stack, f1234–1244).
- The disc under the rotation control: `c1_disc_rotation.png` — reads as a smooth lenticular object at all eight orientations; no facial organisation at any angle.
- The dark right-hand region (the only place a shadowed face could hide) at γ 0.30 and high-pass: `c1_dark_right_gamma.png`, `c1_dark_right_enh.png` — amorphous mottled cabin interior, no structure above the 15–18 px resolution element.

**Verdict on the face: REFUTED.** There is no human face in f1210–1247. The most face-shaped object in the shot is the disc, and it fails the rotation control (it looks the same at every angle — which is the *opposite* of what a face does).

### But the "something was added at f1225" half of the claim is real — and it is not tape

Their frame number is exactly right, which incidentally confirms that their indexing matches ours.

**Measurement.** A hard-edged, dead-black bar with a chamfered left tip and a bracket at its upper end appears **in a single frame, fully formed, at f1225** (dark-pixel area in the band y 150–360 / x 1000–1600 jumps from 77.4 k px at f1224 to 107.7 k px at f1225; `c1_bar_onset.png`, `c1_bar_frames.png`). It then holds for 23 frames and vanishes with the shot at f1247.

Four independent NCC trackers over f1226–1247 (`c1_rois.pkl`):

| ROI | x range over the 22 frames | y range | NCC |
|---|---|---|---|
| window frame, lower (no bar) | −21 → +29 px | −38 → +18 px | 0.99–1.00 |
| rivet line | −20 → +27 px | −53 → +21 px | 0.98–1.00 |
| disc rim (far field) | −6 → +4 px | −24 → +10 px | 0.98–1.00 |
| **the bar** | **−1.5 → +3.5 px** | **−1.0 → +1.3 px** | **0.99–1.00** |

The near-field scene structure the bar *appears* to be attached to translates ~50 px in x and ~72 px in y; the bar stays put to about ±1.5 px and holds constant shape (NCC ≈ 1.00 against a fixed template for 22 frames). **The bar does not belong to the photographed 3-D scene.** Two readings survive: a composited element locked to output-raster coordinates (the same behaviour as the §8.3 fixed rectangle in video 3 and the redaction bar), or a physical object rigidly attached to the *camera body*. The second is weakened by the single-frame onset — a camera-mounted object cannot appear mid-shot.

Edge-sharpness does *not* discriminate: the bar's tip edge is 17–18 px 10–90 %, i.e. the same as the sharpest picture content, so it is not anomalously crisp. Its core luma (15–24 DN) partially tracks the picture's exposure flicker (slope ≈0.35 vs 0.74 for the darkest real scene region and 0.04 for the rendered outer matte), so if it is an overlay it was applied *inside* the picture layer, before the film-look/exposure pass — matching §11.4's finding that video 1's damage pass precedes the retime.

**Verdict on "something added at f1225": CONFIRMED as an added, non-scene element; its identity is UNDETERMINABLE.** "Adhesive tape masking eyes" is not supported (there are no eyes, and the object is a bracketed strut form, not a strip). This is a genuine new find for our record: **video 1 contains a 23-frame hard-edged black element that is raster-locked while the picture floats behind it.**

---

## 3. CLAIM 2 — "second human face, f1435–1670, kepi, shoulder-board insignia"

### This one is right about the face, and it changes our headline

**There is a human head-and-shoulders in video 1.** It is visible in a **single raw frame with nothing but a linear stretch — no stacking, no sharpening**: `c2_RAW_f1532_nostack.png`, `c2_RAW_f1548_nostack.png`. The annotated version is `c2_ANNOTATED_v1_face.png`.

**Localisation.** The figure enters at **f1437** (`c2_onset.png`; nothing at f1428–1436) and leaves at **f≈1570** (`sheet_1560_1658_right.png`). That is 134 output frames, t ≈ 47.95–52.39 s, inside one continuous shot (adjacent-frame correlation never drops below 0.77 across f1437–1670 — no cuts). Overlay: **`/12 01:10:57` → `01:11:00`, Case 12 "Mk.4 pace lap"** (claimed catalogue range 01:10:55–01:11:21 — internally consistent). The head with resolvable facial features is in frame **f1526–f1568**.

The analyst's range f1435–1670 is right at the start (±2 frames) and **over-extended by ~100 frames at the end** — the figure is gone by f1570 and the rest of that range is the craft against sky.

### Measurements

Head size: front silhouette at x≈1330 (f1532) / x≈1132 (f1548); vertex at or above the aperture top edge; chin at y≈465–615 (f1532) / y≈570 (f1548). **Vertex-to-chin ≈ 500–560 px**, i.e. **≈30–37 resolution elements** across the head. For comparison, video 2's Case 22 bearded face — our current "only human face" — is smaller and worse resolved than this.

Silhouette shape, measured as the front edge x(y) at 10-px steps on the raw frame (Gaussian σ 4, fixed threshold, f1532):

| y | x_front | |
|---|---|---|
| 182 | 1334 | protrusion 1 |
| 235 | 1428 | recess, 94 px deep |
| 355 | 1423 | protrusion 2 |
| 410 | 1467 | recess |
| 468 | 1447 | protrusion 3 |
| 523 | 1477 | recess |
| 615 | 1454 | neck/throat |

That alternating convex–concave–convex–concave–convex sequence, terminating in a neck and then shoulders, is the signature of a **human facial profile**. Below it: a neck, a piped collar edge, and a rectangular shoulder element (`c2_figure_1531_1535.png`).

**Honest limit on feature labelling.** Which bump is brow versus nose is *not* fully settled. The measured vertex-to-chin / nose-to-chin ratio comes out at 1.4–2.2 depending on the assignment, against ~3.1 for a canonical adult human head. The straightforward explanation is that **the crown is truncated**: in every frame of the shot the head column luma rises monotonically from the aperture edge (row 17–30) downward with no gap, i.e. the top of the head reaches the top aperture edge and merges into the 46-px vignette ramp. So the visible cranium is clipped, exactly as in video 2's Case 22. I therefore report the silhouette sequence as measured and decline to name each bump with confidence.

### Controls

- **Rotation** (`c2_rotation_control.png`): reads as a face at 0° and at mirror (expected — a mirrored profile is still a profile); at 45/90/135/180/225/270/315° it degrades to an unreadable lumpy edge. **Passes.**
- **Independent windows** (`c2_independent_windows.png`): five *non-overlapping* 5-frame stacks (1526–30, 1531–35, 1536–40, 1541–45, 1546–50) all show it, and so do five single raw frames processed identically. Not a stacking artifact — it is present in unstacked pixels. **Passes decisively.**
- **Matched controls** (`c2_control_regions.png`): five same-size ROIs in the same shot, same tracker, same stack, same sharpening — a craft panel, terrain, dark cabin wall, and two mixed regions. None produces anything face-like. **Passes.**
- **Identity control** (`c2_compare_human_vs_grey.png`): beside video 2's Slim Tim grey (huge cranium, wraparound black eyes, no nasal projection, vestigial mouth) the video-1 profile is categorically different — protruding nose, lips, chin, normal cranium/face proportion, ordinary neck, clothed shoulders. **It is not the grey type.**

**Verdict on the face: CONFIRMED.** A human head and shoulders in near-profile, visible unaided in single raw frames, surviving rotation, independent-window and matched-control tests, at ~30–37 resolution elements across the head.

### The insignia

There is a **rectangular shoulder-board / strap element** on the near shoulder from f1437 to f1568 (dark with bright metallic highlights f1437–1525, light with dark pips f1526–1568 as the lighting geometry changes: `c2_board_groups.png`, `c2_insignia_groups.png`, `c2_board_1536_1544_big.png`).

Discrete objects on it, measured (f1530/1532/1534, local-background-subtracted blob detection):

| object | size | persistence |
|---|---|---|
| dark pip 1 | 31–34 × 31 px | tracked f1530→1536 |
| dark pip 2 | 40–49 × 40–43 px | tracked f1530→1536, 62 px below pip 1 |
| bright object A | 100 × 73 px, peak 181 DN (**not** clipped) | f1530–1536 |
| bright object B | 68–74 × 63–65 px | f1530–1536 |

Earlier in the shot the same element carries two saturated highlights of **48 × 24 px** and **22 × 25 px** plus a fainter third (`c2_insignia_big.png`, 19-frame stack).

**Count** (3–4 discrete small objects) is compatible with the analyst's "two small pins + one large item + one indistinct badge". **Identification is not.**

Five-pointed-star test on the largest bright object (`c2_starblob_zoom.png`, 8× nearest-neighbour):

| k | k-fold rotational self-correlation |
|---|---|
| 2 | **0.658** (it is simply elongated) |
| 3 | 0.247 |
| 4 | 0.330 |
| **5** | **0.325** |
| 6 | 0.345 |
| 7 | 0.356 |
| 8 | 0.361 |

**5-fold is not elevated above 4-, 6-, 7- or 8-fold.** On the earlier 48 × 24 px highlight, angular peak counts at r = 10/14/18 px give 1/4/2 peaks — inconsistent, i.e. noise. Angular modulation 0.03–0.12.

Resolution arithmetic: the largest object spans **100 × 73 px ÷ 15–18 px = 5.6–6.7 × 4.1–4.9 resolution elements**; the earlier highlights **3.2 × 1.6** elements. Recognising a five-pointed star requires resolving five inter-arm notches; at ≤6 resolution elements across, with the object at or near specular saturation, those notches sit at or below the blur limit. Add the point the brief correctly flags: "five-pointed star" is precisely the prior a viewer brings to Soviet-themed material.

**Kepi.** Not assessable. The crown reaches the top aperture edge in every frame of the shot and merges into the vignette ramp; no cap band, crown seam or visor resolves anywhere (`f1548_grid.png`, `f1556_grid.png`, head-column luma profiles). Headgear present-or-absent is **UNDETERMINABLE**.

**Verdicts.** Shoulder-board element with 3–4 discrete small objects: **CONFIRMED as present**. Five-pointed star: **REFUTED** (no 5-fold signal; insufficient resolution elements even in principle). Soviet Army 1943–1990 pattern attribution: **UNDETERMINABLE at this resolution** — nothing in the pixels supports or excludes it. Kepi: **UNDETERMINABLE**.

---

## 4. CLAIM 3 — the leader-flash frames. They are not blank.

Our §2c called f1042 and f1249 "full-colour burnout leader frames … content identification pending" and treated them as empty. **They carry structure. The outside analyst is right on both counts, and their frame localisation is essentially exact.**

### Event 1 — f1040–1044, orange

A **film burn-through**, front advancing from the bottom of the aperture upward. Saturation (max−min channel) by row:

| frame | saturated rows |
|---|---|
| f1039 | none |
| f1040 | 958–991 (bottom edge only) |
| f1041–1042 | 100–1061 (full) |
| f1043 | 16–1059 |
| f1044 | 14–1061 |
| f1045–1048 | none (dark, mean 32) |

Aperture mean RGB: f1041/1042 **(204, 124, 29)**, R/G = 1.65 — orange. f1044 (250, 136, 48).

Persistent content: a bright two-lobed blob at x 1270–1420 / y 780–930 (present f1041–1043, the burn's origin), a near-white burn hole in the bottom-left corner, and vertical melt streaks (`leader_glyph_br_1040_1044.png`, `leader_hp_stack_1040_1044.png`, `leader_1040_1044_fullres.png`).

**The "r".** At **f1043 only** there is a hard-edged bright glyph at **x 715–802, y 956–1002** (`leader_r_hp.png`, `leader_r_glyph_1038_1049.png`). Measured form: a horizontal bar **86 × 14 px** with a stem **34 × 46 px** descending from its left portion — a **Γ / lowercase-r / T topology**, total height 46 px. Colour: mean RGB (205, 127, 62) against a local background of (138, 77, 12) — a *brighter-luma region under the same orange tint*, not a burn-through to white (the true burn hole reads (198, 178, 149)).

Single-frame, quantified: high-pass p99 in that window is 21.8 DN at f1043 versus 8.7 / 8.1 / 5.0 at f1041 / f1042 / f1044. So it is **f1043 alone**, with only a faint residue at f1044 — the analyst's "f1043–1044" is one frame too generous.

Resolution: 46 px tall ÷ 15 px = **~3 resolution elements in height, ~6 in width**. That is right at the floor for letter identification. A whole-video normalised-cross-correlation search for a repeat of this mark (`tmatch2.py`, 2998 frames, variance-floored NCC) found no convincing recurrence (best non-self score 0.837, on unrelated structure) — so it is not a reused damage-library element that I can demonstrate.

**Verdict: CONFIRMED that a hard-edged Γ/r-shaped bright mark exists at f1043. Whether it is a Roman "r", a Cyrillic "Г", a fragment of printed leader text, or a piece of bright single-frame film debris is UNDETERMINABLE at ~3 resolution elements.** Our "blank" characterisation of f1042 must go regardless: the frame is full of structure.

### Event 2 — f1248–1250, yellow

`f01248.png` at full resolution is the single most legible frame of the two events. A **film burn-through with the front advancing downward from the top**: the top ~80 rows still show the previous shot (grey sky, the disc's upper rim, the black strut), below which a scalloped burn edge with **dark carbonised specks** gives onto a translucent yellow field. Saturated rows: f1248 = 178–1061, f1249 = 168–1069, f1250 = none.

Aperture mean RGB f1248 **(175, 161, 47)**, R/G = 1.09 — **yellow, measurably a different hue from the f1042 orange (R/G 1.65)**. The two flashes are not the same colour element reused.

**The analyst's "translucent yellow material that seems to come physically above the footage" is a fair naive description of a real property**: through the yellow you can still see the underlying picture — the disc's shading arc and the window-frame vertical seam remain discernible — and the **burned-in timecode `/11 00:33:34` and redaction bar sit clearly on top of the yellow**, confirming the overlay is composited above the picture layer (consistent with our records). The correct characterisation is a burn-through of the picture, not a physical layer above it.

f1250 is a dark olive field with vertical scratch lines and, at **x ≈ 1330–1470 / y ≈ 370–470**, a **dark T/Γ-shaped mark** (`c3_f1250_mark.png`) — same topology as the f1043 bright mark, opposite polarity, different position. Recorded as an observation; I would not build anything on it. f1251 onward is blank leader; the blocky structure that appears there under high-pass is AV1 coding artifact on a flat field, not content (`c3_yellow_hp.png`).

**Verdict: CONFIRMED. Neither leader-flash neighbourhood is blank.** Both are film burn-through events with resolved internal structure, opposite-direction burn fronts, distinct hues, carbonised debris, and one hard-edged glyph-like mark each.

---

## 5. CLAIM 4 — the f1207–1210 discontinuity

**It exists.** Aperture-only (y 100–1000, x 320–1580) mean luma:

| frame | mean | ratio to f1207 | σ |
|---|---|---|---|
| f1204–1207 | 127.1–127.3 | 1.000 | 38.1 |
| **f1208** | **38.1** | **0.300** | 9.3 |
| **f1209** | **35.3** | **0.278** | 6.8 |
| f1210–1213 | 123.0–123.3 | 0.968 | 49.7 |

So it is a **2-frame exposure dropout to 28–30 % of level**, not a black gap. f1208 is not empty — the disc's bright rim is still visible as a crescent, in a different position (`gap_1207_1210_lift.png`). f1208 and f1209 differ (mean abs diff 3.0), so they are not a held duplicate pair.

**Registration across the gap** (NCC template matching, f1207 as reference):

| tracked object | shift f1207 → f1210 | NCC |
|---|---|---|
| window frame (near field) | **(−107, +59) px** | 0.91 |
| disc (far field) | **(−15, −84) px** | 0.79 (best over scale grid: 0.95×, still 0.79) |
| redaction bar (overlay) | **(+0.4, +0.1) px** | 0.998 |
| timecode glyph block (overlay) | **(+0.6, −0.3) px** | 0.935 |
| left aperture edge | **+1.7 px** (content noise ±3 px) | — |

**This bears directly on §11.5, and it supports it.** The burned-in overlay and the frame border stay fixed to sub-pixel while the picture jumps >100 px — the picture floats, the graphics and matte do not. Same geometry as §11.5, now demonstrated at a 100× larger amplitude than the sub-pixel wobble that section had to work with, so the conclusion no longer rests on <1 px measurements.

**Characterisation.** Near-field and far-field content move by *different* amounts and in *different* directions, and the disc's appearance does not recover at any scale (NCC ceiling 0.79 versus 1.00 before the gap). This is therefore **not** a plate-registration offset and **not** a global shift; it is a genuine change of scene/viewpoint geometry.

**"Film changeover" is not supported.** The burned-in source timecode reads `/11 00:33:33` on f1207, on both dark frames, and on f1210 — no reel change, no case change, no timecode jump. What the pixels show is a **2-frame exposure dropout coincident with a content splice inside one source second**: frames removed, scene resumed from a different viewpoint. Whether that splice is in the claimed source material or in the 2026 assembly cannot be told apart from the frames.

**Verdict: CONFIRMED (discontinuity real, 4 frames spanned, f1208–1209 the dropout); the "changeover" attribution is REFUTED; the border/timecode behaviour matches §11.5.**

---

## 6. Full-video human-face sweep

Contact sheets covering **all 2998 frames at 1-in-6 with γ 0.45 shadow lift** (`sweep_0001_0595.png` … `sweep_2401_2995.png`), plus dedicated per-frame passes over every shot containing organic content. Shot inventory from a rolling frame-difference detector (all boundaries with mean abs diff > 6 on 4×-decimated luma).

| span | content | human face? |
|---|---|---|
| f1–545 | title cards + the §11.7 ghost disc underlay | no |
| f546–916 | catalogue card | no |
| f917–1039 | bright leader (hidden Cyrillic band) | no |
| f1040–1048 | orange burn-through + dark | no |
| f1049–1207 | Case 11 disc through window | no |
| f1208–1209 | exposure dropout | no |
| f1210–1247 | Case 11 disc + raster-locked bar (Claim 1) | **no** (rotation-controlled) |
| f1248–1305 | yellow burn-through, blank leader | no |
| f1259–1305 | Case 12 gantry / pad wide shot — a small dark upright shape stands beside the disc at x≈1130–1250, y≈640–870 (`f01279.png`). Possible distant figure; ~120 px tall ≈ 7 resolution elements. No face resolvable, no face claimable. | no |
| f1306–1436 | Case 12, craft over landscape | no |
| **f1437–1570** | **Case 12 `/12 01:10:57–01:11:00` — human head and shoulders in near-profile with shoulder board** | **YES** |
| f1571–2498 | Case 12, long static craft-and-cable shot | no |
| f2500–2568 | Case 26 "Tim's show & tell" — hands and instruments against a curved marked surface (`sweep_case26.png`) | no |
| f2569–2918 | Case 31 Mk.5 colour segment | no |
| f2919–2970 | near-black leader | no |
| f2971–2974 | the 4-frame insert — re-checked at four rotations, both pose states (`insert_2971_rot.png`) | no |
| f2975–2998 | black | no |

**Result: exactly one human face in video 1 — the Case 12 figure at f1437–1570.** Sampling caveat, stated plainly: the sweep is 1-in-6, and video 1's content holds each image ~2.9 output frames with long static shots, so it cannot miss anything on screen for more than ~0.2 s; a face present for ≤5 frames could in principle escape it. All sub-6-frame events in the video (f1208–1209, f1043, f1248–1250, f2971–2974) were checked individually and contain no face.

---

## 7. BOTTOM LINE

**Our §20 statement is wrong as written and must be corrected before publication.**

Current text: *"This is the only human face in the entire seven-video corpus — 2011 showed humans only as legs/torsos, never a face."*

The clause about 2011 stands (untouched by this work). The scope claim does not: **video 1 contains a second human face**, and it is a *better* one — bigger, better resolved, visible in single unstacked frames, with a neck, a clothed shoulder and a shoulder board. The prior scenes agent explicitly flagged videos 1 and 3 as never swept; that gap is now closed for video 1.

Suggested rewording:

> **Human faces in the corpus: two, both in the 2026 material.** Video 2's Case 22 shows a bearded supine man (`/EBL04 /22 00:30:26`, f1416–1444; §20). **Video 1 shows a second, better-resolved human — a head and shoulders in near-profile in the extreme foreground of Case 12 "Mk.4 pace lap", `/12 01:10:57–01:11:00`, f1437–1570 (t 47.9–52.4 s), wearing a garment with a rectangular shoulder board carrying three or four small discrete objects.** Unlike Case 22, this face needs no stacking: it is legible in a single raw frame under a linear stretch (`analysis/faces/c2_RAW_f1532_nostack.png`, annotated at `c2_ANNOTATED_v1_face.png`), it survives rotation, five independent non-overlapping stack windows and five matched control regions, and it is categorically not the grey type (`c2_compare_human_vs_grey.png`). Both faces share one uncomfortable framing property: **the film aperture truncates the top of the head in every frame of both shots** — in Case 22 the eyes and forehead, in video 1 the crown. Video 3 has still not been swept.

Two secondary corrections for the record:

- **§2c** should no longer describe the two leader-flash frames as blank or as pending. Both are film burn-through events with resolved internal structure: f1040–1044 orange (R/G 1.65), burn front rising from the bottom, carrying a single-frame hard-edged Γ/r-shaped bright mark at f1043 (x 715–802, y 956–1002, 86 × 14 px bar plus 34 × 46 px stem); f1248–1249 yellow (R/G 1.09), burn front descending from the top, with carbonised specks, the underlying picture still visible through the yellow, and the burned-in timecode composited on top of it. Two different hues, two different burn directions — not one reused element.
- **§11.5** gains a much stronger demonstration: at the f1207→1210 discontinuity the picture displaces by up to 107 px while the redaction bar (+0.4 px), the timecode glyphs (+0.6 px) and the left aperture edge (+1.7 px) do not move at all.

And one new finding not previously in the record: **f1225–1247 carries a hard-edged black element that holds a fixed output-raster position (±1.5 px) and constant shape (NCC ≈ 1.00) for 23 frames while the near-field scene translates ~50 × 72 px behind it.** It is not part of the photographed scene. Whether it is a composited graphic or a camera-mounted object is undetermined, though the single-frame onset argues against the latter.