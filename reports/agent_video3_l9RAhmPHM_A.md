# Agent report — Forensic frame analysis, video 3 (`l9RAhmPHM_A`)

*Archived verbatim from the "Forensic analysis video 3" subagent, 2026-07-26.
Working files referenced: `/home/user/new-skinny-bob/analysis/teardown-video3/`.*

---

# Forensic frame analysis — `l9RAhmPHM_A` ("interior walkthru and examination 8mm disclosure footage ufo")

**Material analysed:** 4395 PNG frames, 1920×1080, 29.97 fps, 146.68 s. All numbers below are measured from those frames. Working files in `/home/user/new-skinny-bob/analysis/teardown-video3/`.

**Framing note:** I treat provenance as undetermined. Findings that cut toward "assembled/composited in post" and findings that cut toward "coherent photographed material" are both reported, and I flag what the data cannot settle.

---

## 1. On-screen text — verbatim

Single card, **frames 11–393 at full brightness, fading f394–427, true black f428–456** (0.37 s – ~14.3 s). Read at full resolution from `f00150.png`; text bounding box x247–1635, y335–742; white monospace on pure black (frame mean 3.56, background 0–1).

```
The video contains sample edited
fragments of video tapes 03, 05.

Tape 03 edited fragments:
Case 18/Mk.4 early boarding 02:13:18 ~ 02:23:57

Tape 05 edited fragments:
Case 28/False Cape study 02:51:01 ~ 02:51:32
```

No other text card exists in the file. No end card. **Frames 4255–4394 are a flat gray field** (values 27–30 only, mean 28.9, σ 0.21), and **f4395 alone is true black**.

**Adjudicating the commenter's claim** ("a disclaimer stating it's compiled of two individual original source videos"): substantially correct in substance, wrong in wording. The card says "sample edited **fragments** of video **tapes** 03, 05" — it names two source tapes and calls the contents edited fragments. It does not use the words "disclaimer", "individual", or "source videos".

Note the card says **"video tapes"**, not film, while the video title says "8mm".

---

## 2. Shot-by-shot log

Overlay timecode read at full resolution for every ~15th frame (sheets `strips_a1…a6`, `strips_b1`) plus a per-frame template-matched pass over 3800 frames (`full.json`). Brightness values are raw 8-bit; the picture area's black floor is ~28–29, not 0.

| Video frames | Time | Burned-in overlay | Content / camera |
|---|---|---|---|
| 1–456 | 0:00–15.2 | none | Text card, then black |
| 457–789 | 15.2–26.3 | `/18 02:13:18`→`:25` | A long pale rod/strut at ~45°, rounded terminus, against near-black. Slow drift, no pan; local rotation. Scattered bright ellipses in the dark field (see §7). ~2.6% of picture area above 60 grey |
| 790–~900 | 26.4–30.0 | `02:14:09`→`:11` | Closer, softer organic forms; a domed specular surface enters at f880 |
| ~901–939 | 30.1–31.3 | `02:14:32` | A large glowing dome filling frame, horizontal line across it, dark spots — brightest object so far (max 209) |
| 940–~1000 | 31.4–33.4 | `02:15:25`→`:26` | Dark, indistinct forms; rapid handheld motion |
| 1005–1098 | 33.5–36.6 | `02:15:31`→`:33` | Push in to a near-uniform pale wall/panel (f1080: region mean 101, σ 9.5). Gate matte fully visible. Hotspot at x≈406–542; centre:edge brightness ratio **1.85** |
| 1099–~1390 | 36.7–46.4 | `02:17:48`→`:54` | **The "symbol panel" shot.** A pale angular structure at right; to its left a cluster of glyph-like markings (a crescent + 3 vertical strokes + a crossbar + a hook) plus dial-like paired circles and a `2Ц`-type mark. Slow orbit around the object |
| 1392–~1760 | 46.4–58.7 | `02:18:01`→`:09` | Continues around the same panel; brightest small highlight ~f1700 |
| 1765–1935 | 58.9–64.6 | `02:19:00`→`:08` (two fragments) | Wider: arched ribs / vaulted structure, floor with a pedestal. Camera tracks laterally |
| 1940–2100 | 64.7–70.1 | `02:19:17`→`:20` | Pedestal / stalk objects on a floor, low contrast |
| 2101–2231 | 70.1–74.4 | `02:19:33`→`:35`, `:50`→`:51` | Curved dark surfaces, a small bright point light at f2200 |
| 2233–~2570 | 74.5–85.8 | `02:19:59`→`02:20:06` | Ribbed / bone-like arch with a dark circular aperture; then dim pedestals |
| 2578–2674 | 86.0–89.2 | `02:22:15`→`:16`, `:19`→`:21` | Very soft, large pale mass — lowest sharpness of segment A |
| 2675–2962 | 89.3–98.8 | `02:22:31`→`:34`, `:37`→`:40` | A tall pale form under a large curved overhead surface; small bright ring at bottom |
| 2965–3112 | 99.0–103.8 | `02:23:16`→`:19` | **The clipped bright disc** (max 248, ~100 px across) with a tapering vertical flare plume, over a lit textured wedge. 22% of picture area above 60 grey — the most-illuminated shot in segment A |
| 3117–3700 | 104.0–123.5 | `02:23:44`→`02:23:57` | **The "lens" shot.** A large circular rim with glass-like elliptical internal highlights, sharp-edged; camera pulls back to reveal pale slab forms. Sharpness roughly doubles over the first 2.5 s (focus pull) |
| 3701–3713 | — | none | Dark gap |
| 3715–3832 | 124.0–127.9 | `/28 02:51:01`→`:03` | **Segment B begins.** Overhead shot of a lit table. Two pale examiner hands from top hold a divider/caliper over a long 4-digit hand; a 5-digit human hand rests at right with a dark suit cuff; a printed document and a small marked dark card on the table |
| 3835–4196 | 128.6–140.0 | `02:51:19`→`:26` | Same setup; the hands are laid flat and photographed, then a dark cuff/electrode with a wire is fitted around one digit. Handheld drift 3–12 px/frame |
| 4198–4253 | 140.1–141.9 | `02:51:31`→`:32` | Continues; last image frame ~f4254 |
| 4255–4395 | 142.0–146.7 | none | Flat 28.9 gray, final frame true black |

**Overlay format and font.** Every image frame carries a 12-character burn-in reading **`/NN HH:MM:SS`** — e.g. `/18 02:20:05`. Bounding box x469–960, y945–995; character pitch **42.67 px**, cap height **51 px**; heavy squarish monospace with a **slashed/dotted zero**, serifed `1`, square colons — the look of an upscaled 8×16-type bitmap character generator. **There is nothing to the left of the slash: the tape field is empty.** I checked the sibling video `Oqw96jCOP7A`, which shows `/11 00:36:03` and `/20 00:03:11` — so the orphan leading slash is the series' house convention, not a slip in this file.

---

## 3. Catalog verification

**Fragment inventory (22 fragments)**

Case 18 (19 fragments): 13:18–25 · 14:09–11 · 14:32 · 15:25–26 · 15:31–33 · 17:48–54 · 18:01–09 · 19:00–01 · 19:05–08 · 19:17–20 · 19:33–35 · 19:50–51 · 19:59–20:06 · 22:15–16 · 22:19–21 · 22:31–34 · 22:37–40 · 23:16–19 · 23:44–57
Case 28 (3 fragments): 51:01–03 · 51:19–26 · 51:31–32

**Endpoints match the card exactly.** Lowest Case-18 value observed is `02:13:18` (f457, first image frame); highest is `02:23:57` (f3690–3698). Lowest Case-28 value is `02:51:01` (f3715); highest is `02:51:32` (f4240–4253). **Zero out-of-range values, zero non-monotonic values, zero values from a third case.** The catalog is internally clean.

**The "~" separator does denote a range fragments were drawn from, not a continuous clip — confirmed and quantified.**
- Case 18 span 02:13:18→02:23:57 = 640 source seconds. Distinct source seconds actually present: **87 → 13.6% coverage**, in 19 discontinuous pieces.
- Case 28 span = 32 source seconds. Present: **13 → 41% coverage**, in 3 pieces.

This closes arithmetically against the cadence in §4. Segment B: 13 source seconds × 45 frames = 585, minus ~45 frames of partial first/last seconds across 3 fragments = **540**, and the measured extent f3715–4254 is **540 frames — exact**. Segment A: 87 × 45 = 3915, minus ~670 partial across 19 fragments ≈ 3245 vs measured 3244.

**Cross-check against the sibling videos:** `Oqw96jCOP7A`'s card uses `-` and lists short spans (5 s, 7 s, 15 s, 31 s, 48 s) consistent with contiguous clips. This video uses `~` with a 640-second span. That is consistent with the two separators carrying different meanings, exactly as the brief hypothesised.

---

## 4. Timecode cadence

Measured by template-classifying the seconds-units digit on **every** frame across five continuous fragments (`cad.py`, `cad.json`). Run lengths:

- f457–789: 41, 45, 45, 45, 45, 45, 45 (first run truncated by fragment start)
- f2255–2570: 45, 45, 45, 45, 47, 44
- f3125–3702: 45, 45, 45, 45, 44, 46, 45, 45, 45, 45, 45, 45 → **(3690 − 3150) / 12 ticks = 45.000 frames/tick exactly**
- f3830–4193: 45, 45, 44, 43, 45, …

**Result: 45.0 video frames per one-second tick of burned-in source timecode**, in both segments and across every fragment tested. The ±1–2 outliers are classifier error at motion-blurred boundaries, not cadence variation.

45 / 29.97 = **1.5015 s of video per source second**, i.e. playback at **0.666× (2/3) of the rate implied by the timecode**.

Tick *phase* differs between fragments (f3150 ≡ 0 mod 45; f2300 ≡ 5; f543 ≡ 3; f3875 ≡ 5), which is what you expect from independently trimmed clips laid on a timeline.

---

## 5. Community claims

### "The last scene with the four digit hand"

**Supported. Four digits, and the resolution is sufficient to say so.**

Best frames: **f3838, f3866, f3800, f4130, f4180** (`LW_3866.png`, `LW_4130b.png`, `hand_L_f3838.png`). The hand occupies ~410 × 530 native pixels; digits are ~30–40 px wide with 15–25 px gaps — comfortably resolved. In every frame examined I count **one digit set apart by a deep web (thumb position) plus three digits close together = 4**, and I can count **four metacarpal ridges** on the dorsum converging to the wrist. Proportionally the digits are all long and slender; the thumb-position digit is nearly as long as the others rather than short and thick.

Honest caveats: the hand is palm-down in every frame in the segment; the palm looks flat against the surface, so a fifth digit folded underneath is not strictly excluded, but nothing in the knuckle line or silhouette suggests one. I found no frame showing the palmar side or a side profile.

**Directly relevant control in the same frames:** the hand at the right of frame, with a dark suit cuff, has **4 fingers + thumb = 5** (`R_3866.png`), and the two examiner hands entering from the top (f3960) also read as 5 digits each. So the four-digit count is specific to one hand in a frame that also contains normal five-digit hands — a deliberate side-by-side comparison, whatever its origin.

### "Whats up with the black nails"

**Supported as an observation, with an important correction.**

On the four-digit hand each digit carries a **near-black cap at its distal tip** (`L_tips_4180.png` at 4× on f4180). Measured: the caps reach 20–30 grey against digit skin at 130–170, they extend slightly *wider* than the digit silhouette at the very end (i.e. they wrap the tip), they cover roughly a quarter to a third of the distal segment, and they carry a **small specular highlight on the upper-left** — so they are a glossy physical surface, not a shadow or a printing artifact.

The correction: the dark elongated marks on the **human** hand are **not nails**. Profiled at f3866 y=700, they are inter-digit shadow cores (values 26–33 with 20–30 px penumbrae) lying to the left of each finger, in exactly the same direction as the whole hand's cast shadow. Anyone reading "black nails" on both hands is misreading the human hand's shadows. Only the four-digit hand has dark tips.

I cannot determine from the pixels whether the caps are claws, pigmented tips, lacquer, or a prosthetic.

### "Lighting and resolution are inconsistent… blurry and grainy in some parts but then a close-up of a lens that's super sharp"

**The sharpness variation is real and measurable; the "inconsistency" framing is not supported.**

Normalised gradient energy per fragment (`sharp.json`), lowest to highest median:

| Fragment | grad |
|---|---|
| 02:23:16–19 (bright disc) | 0.0084 |
| 02:22:15–16 | 0.0108 |
| 02:15:31–33 | 0.0107 |
| 02:13:18–25 (rod) | 0.0142 |
| 02:23:44–57 (**the lens**) | 0.0160 |
| 02:19:05–08 | 0.0210 |
| 02:51:19–26 (hands) | 0.0224 |
| 02:51:01–03 (hands) | **0.0228** |

Range **2.7×**. So yes — the hand examination and the lens close-up are genuinely much sharper than the disc and wall shots.

But: **within-fragment coefficient of variation is 0.04–0.22** in every fragment, and I found **no frame-to-frame sharpness discontinuity anywhere**. Inside the lens fragment, grad climbs 0.0089 → 0.0196 smoothly over f3125→3200 (2.5 s) and then holds — the signature of a focus pull, not a splice. Sharpness tracks subject distance and focus exactly as it should in real photography. Verdict: **complaint unfounded as stated**; the variation is between shots and gradual, which is normal.

On "grainy": see §7 — there is essentially no grain anywhere in this file (high-pass RMS 0.14–0.65 grey levels). What reads as graininess is compression mottle and posterisation contours.

### "Super dark in there and they're using a flashlight, but then there's an area where the entire structure is lit up"

**Not supported.** Fraction of the picture area above 60 grey, sampled across segment A: f600 2.6%, f1500 1.3%, f2300 1.9%, f2000 2.9%, f3300 9.2%, f1000 15.4%, f2700 16.2%, f3000 22.2%. **No frame in segment A ever approaches an evenly lit interior.** The two frames that read as "everything is lit" are the *closest* shots: f1062–1098 is the camera pressed almost against a pale wall, and even there the falloff is 1.85:1 from hotspot to edge with the hotspot displaced left of centre — precisely what a close handheld source does. Segment B is uniformly bright, but it is a table-top examination under overhead lighting, a completely different setup, and the card says so.

### "A lamp on the top of the craft that's not lighting anything up whatsoever but it's showing up as a light"

**Not supported for either candidate object.**

*Candidate 1 — the oblique bright ellipse on a stalk, f1005–1098 (`lt_lamp_1040.png`).* Its peak is ~178 (99.9th pct) / 214 (max) while adjacent structure reaches 130. A ratio of only **~1.4×** is not how an emitter behaves in-frame — real sources clip hard against what they illuminate. It also has visible internal mottling and a soft but definite edge. This reads as a **strongly reflective disc catching the scene light**, not a lamp. If it isn't emitting, no illumination is "missing".

*Candidate 2 — the clipped white disc, f2965–3112 (`lt_disc_3000.png`).* This one *is* a source or a specular of one: clipped at 248, with a tapering vertical flare plume (classic veiling glare / halation). And it **does** illuminate: measured along the horizontal through its centre at f3000, the surface to its left runs 96 → 109 → 103 → 89 → 84 → 71 → 65 → 50 as radius goes 120 → 540 px, i.e. a coherent gradient anchored on the disc. To its right, everything beyond r=240 is at the 26–29 black floor, and directly above beyond ~120 px likewise. That asymmetry is explained by there being nothing to the right to reflect — open dark volume.

One honest qualification: the left-side falloff is **far slower than inverse-square** ((I−28.8)·r² rises monotonically from 97 to 834 over that span). That is *not* an anomaly by itself — an obliquely oriented receding panel does exactly this — but it does mean I cannot use falloff to *confirm* the disc is the sole source rather than a bright object inside a broader pool of light.

---

## 6. Lighting physics

**Shadow direction and softness are self-consistent where I can measure them.** Segment B, f3866 (`shadow_f3866.png`), profiled across two independent objects at the same scan line (y=700):

- Four-digit hand: bright 97 → penumbra x505–535 → core **28–29** at x540–580 (~45 px) → sharp rise to 145 at the hand's lit edge.
- Human hand: bright 130 → penumbra x1080–1115 → core **26–33** at x1120–1145 (~30 px) → rise to 96.

Both cast **to the left with a small downward component**, both with **20–30 px penumbrae** — same light direction, same source angular size. The examiner hands and the caliper are consistent with this too. I found **no object casting a shadow the wrong way** in this frame. That is a positive finding for physical coherence.

Two things I could not determine: (a) whether the bright ridge at x365–400 in the same frame is a lit fold or a second light's shadow edge — it reads as a lit raised edge in the cloth, not a shadow, but I can't prove it; (b) shadow direction anywhere in segment A, where 97%+ of the picture area sits within a few grey levels of the black floor and there is nothing to measure.

**Note on black level:** shadow cores bottom out at **26–29** — the *same* value as the outer matte field. The whole image is tone-mapped so that "black" is the film-base gray. Consistent throughout, both segments.

---

## 7. Grain, dust, film damage, and layer separation

### 7a. Does the film damage move with the image or float over it?

**The premise mostly fails: there is no detectable film-damage layer to test.** But one layer *does* demonstrably float over the image, and it is not the damage — see 7d.

**No per-frame dirt.** A single-frame impulse detector (`min(f−f₋₁, f−f₊₁) > 22`, bright and dark) was run at 43 sample points across the whole runtime. Where inter-frame motion is slow, the count is **exactly 0** (f1082, f1179, f1470, f2052, f2246, f2440, f2537, f2634, f2731, f2828, f2925, f3119, f3410, f3507, f3604, f3740, f3793, f3952, f4058). Non-zero counts occur only at high-motion frames (f1276, f1955, f3899) and are motion residue. **No hairs, no dust flashes, no splice bars, no vertical scratches were found anywhere I looked.** Real 8mm and real videotape dubs are not this clean.

**The bright specks in segment A are scene content, not film dirt — measured.** Three specks tracked frame-by-frame f594→625 (`speck_A` / tracking output):

| f | speck 1 | speck 2 | speck 3 |
|---|---|---|---|
| 594 | (1500, 217) | (1336, 254) | (1200, 174) |
| 604 | (1526, 216) | (1354, 246) | (1217, 156) |
| 614 | (1510, 176) | (1330, 203) | (1191, 109) |
| 625 | (1438, 118) | (1250, 145) | — |

All three **persist continuously for 30+ frames**, **move smoothly and together** (their mutual separations stay within ~20 px), hold constant peak brightness (95–108), and grow slowly in area (speck 1: 213 → 440 px). Film-plane dirt changes identity every frame; a composited static overlay does not move. These do neither — they behave like physical objects drifting in the volume, tracking with the scene. **Positive finding for scene coherence.**

**One unresolved mark.** At **f2598–2601** a hard-edged dark vertical bar ~10 px wide appears *within* the timecode text band, aligned to a character gap, and vanishes by f2602 (`stripe2.png`). It does not extend upward through the image. I could not determine whether it is scene content, a dark outline of the overlay glyphs becoming visible against a bright background, or a transient mark applied above the burn-in. **Flagged as undetermined** — it is the only candidate in the file for damage layered over the text.

### 7b. Grain

**Essentially absent.** 5×5 high-pass residual RMS, measured over flat regions across 6 consecutive frames:

- Segment B table (bright, mean ~110): **0.57–0.65** grey levels
- Segment A bright panel: **0.31–0.46**
- Segment A dark region: **0.09–0.19**

Lag-1 temporal correlation of that residual is ~0 in the bright regions (−0.017 to 0.21) and high in the dark region (0.35–0.97). Reading: whatever texture survives is **per-frame independent** where there is signal, and is **encoder block-reuse** where the scene is static and dark.

The "empty table" high-pass view (`speck_B.png`) shows the character clearly: **smooth swirling posterisation contours and 8×8 hatched blocks**, not stochastic grain.

**Important caveat I cannot get around:** this is a YouTube-transcoded stream. Compression at this bitrate destroys fine grain. **I cannot determine whether the original had grain.** What I *can* say is that the delivered file has none, and that a fake-film treatment built from grain plates would be equally invisible here. This test is inconclusive in both directions.

### 7c. Temporal coherence and geometry — no generative-style artifacts found

**Symbol panel, f1195–1360** (`glyph_seq.png`, `glyph_zoom.png`): the glyph cluster persists across **165 frames / 5.5 s** with stable topology — the left crescent, **the same count of three vertical strokes**, the crossbar over the right pair, the terminal hook. Its apparent size and perspective change correctly with camera motion. Adjacent features (paired dial-like circles above, a `2Ц`-type mark below) also persist. **No melting, no stroke-count changes, no mutating texture.** This is the best mutation test in the file and it passes.

Limit: comparing f1300 and f1345 at maximum zoom, the *fine terminal detail* on the crossbar's right end differs in appearance (a curling hook vs a straight riser). This is consistent with perspective and focus change, but at this blur level **I cannot certify the glyph is stroke-identical**, only that its gross topology is stable.

**Document, f3860–4180** (`doc_caliper.png`): the printed sheet holds a stable **11–13 line** layout with consistent slope and word-like segmentation across ~10 s. Individual "words" are not resolvable, so glyph-level mutation can be neither confirmed nor excluded.

**Instruments and anatomy:** the divider/caliper (two legs, knurled pivot wheel, adjusting screw) is geometrically consistent across frames. Hand topology in the sharpest footage (f3960) is correct on all four hands present — no extra or fused digits, no melting, no impossible reflections found.

**Motion is native, not optical-flow interpolated.** Phase correlation between consecutive frames in segment B gives smooth 3–12 px translations with occasional exact repeats — no smeared or morphing intermediate frames.

### 7d. What *does* float over the image: a frame-locked horizontal line pattern

This is my strongest layer-separation result.

Segment A contains a fine **horizontal line pattern** visible on flat bright fields. Measured pitch:

| frame | period | amplitude | spectral SNR |
|---|---|---|---|
| f985 | 5.376 px | 0.94 grey | 79× |
| f1080 | 5.385 px | 0.72 grey | 53× |
| f2100 | 5.405 px | 4.39 grey | **132×** |

Pitch agreement within **0.5%**. 1080 / 5.39 = **200.4** → ≈200 lines over the full output frame height. It is purely anisotropic (no matching horizontal-direction periodicity), so it is a scanline-type pattern, not upscaling blocks or compression noise.

**Phase test — the decisive part.** Fitting sin/cos at that frequency in **absolute output-frame y coordinates** (`phase` fit):

- f1062→1098 (36 frames, camera and scene moving substantially): phase **−113.6° … −100.7°**, i.e. constant within ±6° = **±0.09 px**.
- f2090→2120 (a different shot): phase **−55.1° … −59.5°**, constant within ±2.5° = **±0.04 px**.

**The pattern is locked to the output frame to within a tenth of a pixel while the image content moves freely underneath.** It is a separate layer, not part of the photographed scene. Its phase differs between shots (−107° vs −58°, a 0.73 px offset), so it is applied per-clip rather than as one global pass.

**And it is absent from segment B**: on comparably bright flat table regions (f3880–3916) the amplitude is **0.013–0.10 grey** with unstable phase — 5–10× weaker than segment A at equivalent brightness. The two claimed source tapes were therefore processed differently, even though the card describes both as "video tapes".

*Alternative reading I want to keep on the table:* screen-locked scanlines are exactly what you get from **filming or capturing a monitor**, which is a legitimate real-world path to a frame-locked line pattern. That would explain segment A but not its near-total absence in segment B.

### 7e. Frame-rate conversion: a duplicated frame every 12 frames

Frame-to-frame mean absolute difference, normalised by a local 13-frame median, binned by frame index **mod 12** over f460–4255:

| phase mod 12 | 0 | 1 | **2** | **3** | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fraction with normalised diff < 0.3 | .01 | .01 | **.23** | **.23** | .01 | .00 | .00 | .00 | .00 | .00 | .00 | .00 |

128 of the detected duplicate-pair gaps are **exactly 12 frames**. Duplicates sit at a **fixed phase (2–3 mod 12) across the entire runtime, both segments**. Spot-checked pairs (f1202/1203, f1214/1215, f3865/3866, f3901/3902) are near-identical but not bit-identical: mad 0.02–0.07, max diff 6–9, only 1–5% of pixels differing at all — i.e. **true frame duplication independently re-quantised by the encoder**, not frame blending.

So the delivered sequence carries ≈**27.5 unique images per second** in a 29.97 fps container (ratio 11/12).

Two cadences therefore coexist and are **incommensurate**: the timecode ticks every **45** frames, the image layer duplicates every **12**. gcd = 3, so they realign only every 180 frames. **Inference:** the timecode/vignette/line-pattern graphics were rendered at the output rate, while the image layer arrived through a separate non-integer frame-rate conversion. Both were applied to the assembled timeline — the 12-frame cadence is uniform across both claimed tapes, so it post-dates their joining.

**Caveat:** I could not read the container's true frame rate — the saved `playerResponse` JSON has no format block (playability error), and no source media file is present, only extracted PNGs. Part of this cadence could have been introduced by the download/extraction chain rather than the author's export. The **fixed phase across the whole file** argues for it being baked in, but I cannot prove that from frames alone.

---

## 8. The "film gate" border — metrology

**It is a soft feathered matte over a solid gray field, not a photographed aperture.**

**Edge profile is a wide ramp, not a step.** At f3900, averaged over 300 rows: left edge climbs 28.1 (x=258) → 89.8 (x=304), a **~46 px** transition; right edge falls 102 (x=1535) → 28 (x=1583), **~48 px**; top **~45 px**; bottom **~33 px**. A real gate aperture or film-base boundary gives a few pixels of blur, not forty-six.

**The outer field is a solid fill.** Across the entire border annulus (~1.08 M pixels) the values span only **27–30 — three distinct levels** — with mean 28.82–28.92 and σ 0.18–0.19, and this holds across 200 frames (`plateauL`, `plateauT` frame-to-frame |Δ| median 0.086–0.123). Pixel comparison of the far corner between f3900 and f4100 gives max |diff| = **2**. Real film base carries grain and density variation; this carries neither. *(Same compression caveat as §7b, but note that a low-bitrate encoder does not *lift* black to 28.9 — that level is authored.)*

**Aspect ratio** of the visible area: measured width/height ≈ **1.33 (4:3)** in segment A, ≈1.28 in segment B.

**Jitter: none detectable — the border does not weave like a projector or telecine.** Three independent measurements:

1. **Plateau-pixel count** in the border annulus over f3860–3980: median frame-to-frame change **1167 px**. With a boundary perimeter of ~4600 px, that corresponds to **≤0.25 px** of equivalent uniform boundary displacement per frame. (Count changes also from content entering the annulus, so this is an upper bound.)
2. **Ramp-onset position** (plateau + 1.2 grey, sub-pixel) over f3835–4190: median frame-to-frame |Δ| = **0.48 px** left, **0.54 px** right, **1.07 px** top, **1.01 px** bottom — again upper bounds, since the onset threshold is sensitive to interior brightness.
3. **Clean single-shot case**, f1062–1094 (39 frames): left onset spans 456.8–459.2 px (σ **1.71 px**) with frame-to-frame |Δ| mean **0.34 px**, max **0.94 px** — and the variation is monotonic *drift*, not random hop.

For comparison, 8 mm projector or telecine weave typically runs 0.1–0.5% of frame height, i.e. **1–5 px at 1080p**, and presents as visible frame-to-frame hopping. Nothing like that is present. (An electronically stabilised or pin-registered scan would also be steady, so this is not by itself decisive — but combined with the 46 px feathered edge and the grainless solid fill, the border reads as a rendered matte in output coordinates.)

**A fixed graphic element inside the picture area.** A hard-edged, axis-aligned dark rectangle with a step occupies the bottom-left of the picture area (`notch.png`), immediately left of the timecode. Its interior value is **28.2–29.1** — identical to the matte plateau. Measured right edge / top edge:

| frames | tape/case | right edge x | top edge y |
|---|---|---|---|
| 1062–1094 | /18 | 456.8–459.2 (σ 0.9) | 920.3–921.2 (σ 0.3) |
| 2098–2118 | /18 | 460.6–466.3 | ~919.7 |
| 3756–3820 | /28 | 449.9–452.7 | 919.5–924.7 |
| 4092–4182 | /28 | 452.2–467.1 | 917.7–923.2 |

The **same hard-edged shape occupies the same ~15 px window of the frame in four different scenes from two different claimed source tapes 38 source-minutes apart**, and within a shot it is stable to under a pixel. Straight axis-aligned edges plus cross-tape positional persistence identify it as an element of the output composite, not a photographed feature of either scene. (Frame-to-frame IoU is 0.977 for f1080/f1090 but drops to 0.63 for f1080/f3900 — because scene shadow merges with it in segment B, so it is not one pixel-identical stencil across the whole file.)

**Layer order of the burn-in.** The timecode's peak level is **179–195** regardless of what is behind it — background 28.5 (f600, f1500, f2500) or background 100 (f3760, f4100): peak/background ratio swings **1.95× to 6.75×** while the peak barely moves. It is opaque and leveled to a fixed sub-white value (~187, never clipped to 255, matching the image's own tonal ceiling). Glyph pixels do vary ~7–11 grey levels between frames sharing the same timecode value, attributable to soft edges mixing with moving content plus encoder noise.

---

## Summary of what the pixels support

**Pointing toward post-production assembly / synthetic layers:**
- A horizontal line pattern locked to output-frame coordinates to ±0.1 px while the scene moves (§7d), present in segment A and near-absent in segment B.
- A 46 px feathered matte over a grainless three-level solid gray fill, with no projector weave (≤0.25 px) (§8).
- A hard-edged axis-aligned dark rectangle at a fixed frame position across both claimed source tapes (§8).
- Two incommensurate cadences: timecode ticks every 45 frames, image layer duplicates every 12 (§4, §7e).
- Zero film dirt, hairs, scratches or splice marks anywhere tested; no grain (§7a, §7b) — though compression makes this inconclusive.
- Playback at exactly 2/3 the rate its own timecode implies (§4).

**Pointing toward coherent photographed material:**
- Shadow direction and penumbra width consistent across independent objects in the same frame (§6).
- Bright specks in segment A track with the scene over 30+ frames with constant brightness and growing size — scene-locked, not a damage layer (§7a).
- Sharpness varies 2.7× *between* shots but smoothly *within* them, tracking focus and subject distance; no intra-shot discontinuity found (§5).
- The recurring symbol cluster holds stable topology and correct perspective over 165 frames; instrument and hand geometry are consistent; no melting, mutation, or impossible reflections found (§7c).
- Motion is native, not interpolated (§7c).
- The catalog is internally clean: endpoints hit exactly, no out-of-range or non-monotonic timecodes, and fragment durations close arithmetically against the 45-frame cadence to within 6 frames out of 3244 (§3).
- The "lamp casts no light" and "everything is lit up" complaints do not survive measurement (§5).

**Could not determine:** whether the original material had grain (compression); whether the glyph and document detail is stroke-identical frame to frame (optical blur); container frame rate and how much of the 12-frame duplicate cadence came from the download chain (no source media, no format metadata); the nature of the transient dark mark over the burn-in at f2598–2601; whether a fifth digit is occluded beneath the palm; and shadow geometry anywhere in segment A, where there is almost no lit surface to measure.
