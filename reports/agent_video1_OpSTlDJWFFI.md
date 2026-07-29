# Agent report — Forensic frame analysis, video 1 (`OpSTlDJWFFI`)

*Archived verbatim from the "Forensic analysis video 1" subagent, 2026-07-26.
Working files referenced: `/home/user/new-skinny-bob/analysis/teardown-video1/`.*

---

# Frame-level forensic analysis — `OpSTlDJWFFI` (100.06 s, 2998 frames, 29.97 fps, 1920×1080)

All frame numbers are 1-based; **t = (frame − 1) / 29.97**. Working files in `/home/user/new-skinny-bob/analysis/teardown-video1/`.

Provenance is treated as open. Where a measurement points toward "consistent with real film/video capture" I say so as plainly as where it points the other way, and I flag what the resolution does not permit.

---

## 1. Shot-by-shot log

### Seg 0 — Title cards · f1–882 (t 0.000–29.40)
Dark grey field (luma 6.7), monospaced white text, cross-dissolves at ≈f11, ≈f321–332, ≈f560.
- Card A (f1–~310): *"0135 location and status unclear as of 2026/04/21. Incapacitation presumed. / Per provision with network, continuity releases are triggered. / 7 video tapes with material recorded between 1942-1969. / Material containing UFO incidents, recovery and study of extraterrestrial life forms. Full disclosure pending."* (read at f60)
- Card B (f~330–555): *"Source anonymity is maintained. / Failsafe contract is preserved."*
- Card C (f~570–882): the fragment list, **verbatim identical to the description**, including the `&tell` typo (read at f700).
- Behind Card A there is a very faint large ghost image — a lens/disc outline plus vertical bars — visible only under strong local-contrast stretch (f60).
- ~517 of these 882 frames are **bit-identical** to their predecessor (static text + encoder), e.g. f2–10.
- f883–917 fade to black; f908–917 luma exactly 0.00.

### Seg 1 — Blank film leader · f918–1044 (t 30.60–34.80)
Hard cut at f918 (luma 0 → 117.7). A soft-edged, rounded-corner bright rectangle on a dark surround; interior near-uniform, level flickering (per-frame gain σ = 4.5 %). **No burned-in timecode.** Heavy transient dust (§5). f1041–1044 the lower frame goes warm/orange. **f1045–1048: four dark frames** (luma 32.2–32.4 vs 90–108 on either side).
- **Translucent dark Russian caption**, modern sans-serif, two lines, f≈969–990 (t 32.3–33.0): *"Предыдущее сообщени[е]…"*. Measured to be **clipped at the aperture** — no signal at x 1630–1780 (mean 24.1 DN at f978 vs 22.9 at f960, σ ≈ 9 both).

### Seg 2 — Case 11 "Tin bird unauth" · f1049–1247 (t 34.83–41.58, 199 frames)
Overlay: `[black rounded bar] /11 00:33:30` … `00:33:34`.
Content: a large white lenticular disc nearly filling the frame, seen from above/behind, over a pale ground with faint linear (field/pavement) features. Lit from upper-left: specular highlight along the upper rim, shaded underside with a distinct lip. From f≈1150 a dark curved structure with a regularly spaced ruler-like scale enters at right (wing/nacelle edge); f≈1230+ a dark angular member enters top-right. Camera nearly static; disc slowly grows/rotates.
- **f1208–1209**: two frames where the whole film frame shrinks and shifts, darkens (luma 30.0 / 26.8 vs 84), and the overlay jumps position and becomes crisp — a 2-frame frame-pull/splice event **mid-shot**; the burned-in timecode does **not** advance across it.
- **f1148–1151**: dark horizontal band with a bright edge below it, sweeping down y 245→262 (≈5.7 rows/frame), gone by f1152.

### Seg 3 — Case 12 "Mk.4 taxi" · f1250–1298 (t 41.64–43.24, 49 frames)
Overlay: `[bar] 12 01:08:21` → `01:08:22` (tick between f1266 and f1268). Dark interior looking out through an opening with a vertical mullion; a pale disc on the ground at middle distance, low horizon.
**f1299–1303 cut**: f1299–1300 pure black, f1301–1303 very dark with faint vertical striations.

### Seg 4 — Case 12 "Mk.4 pace lap" · f1304–2498 (t 43.51–83.32, 1195 frames)
Overlay: `[bar] /12 01:10:55` onward.
Opens with the disc low over a paved apron with expansion joints (f1304–1310), then a long sequence of the disc alongside an aircraft: white fuselage with rows of dark fasteners at frame right, bright overcast sky. From f≈1560 a **dark wiggly wire/aerial** hangs in front of the window, visibly flexing. The disc recedes from near-frame-filling (f1310) to a small dark lens (f2300). Camera pans/shakes.
- **f2462–2466**: a second downward-sweeping dark band, y 243→258 (≈5 rows/frame), morphologically near-identical to the f1148 event (row-profile correlation up to **0.836**, f1150 vs f2464).
- **f2499–2501 cut**: three near-black frames.

### Seg 5 — Case 26 "Tim's show &tell" · f2502–2568 (t 83.45–85.69, 67 frames)
Overlay: `[bar] /26 01:01:18` → `01:01:19`.
Content (best read in the 8-frame average of f2545–2552): a very bright, hazy, largely blown-out background. Centre-left, a large dark curved panel with a bright rim; over it a dark angular wedge carrying bold **white outline markings** (a chevron/"Z" plus a triangular wedge). Right of centre, a small bright lens/ellipse with a bright core — almost certainly the thing the commenter calls "the UFO". Lower centre, a **hand with one digit extended, pointing up-left**. Lower right, a second dark angular object with white markings. Camera drifts (dx up to 3 px/frame, dy up to 3.5 px/frame).
- **f2540–2541**: brief brightness dip (luma 38.8 vs local 60) — a flicker, not black.
- **f2569–2570 cut**: two dark frames.

### Seg 6 — Tape 06 / Case 31 "Mk.5 virgin (col/s)" · f2572–2917 visible (t 85.79–97.30), dark tail to f2977
Overlay: **`T6-02/31 00:57:56` … `00:58:03` — full string, NO redaction bar.**
Colour (strong green/teal cast). View out of an open aircraft door: green-painted doorframe and sill at left, a white lenticular disc gliding just outside, receding patchwork farmland below with a long pale line (runway or contrail). Camera shake 3–15 px/frame.
- **Russian caption `Самолет Mark 5 (1961 год…` over f≈2602–2656**, overlapping and obscuring the burned-in timecode. Modern sans-serif; clipped to the film-frame area.
- f2918 the image drops to near black (luma 24.4 → 8.5 by f2975) with the aperture still faintly visible to f2974; f2975–2990 a flat dark plate with **no** aperture; f2991–2998 pure black (luma 0.00).

---

## 2. Catalog verification

**Overlay format** (read at full res, f1120/1280/1380/2510/2596/2800): `T{tape}-02/{case} HH:MM:SS`, monospaced, white with a dark halo/drop-shadow, at the lower-left **inside** the film frame. In all four b/w fragments a **soft-edged black rounded-rectangle bar** covers the prefix, leaving `/11`, `12`, `/12`, `/26` visible. All four bars are the same width, consistent with a 5-character redacted prefix. Only the colour fragment is unredacted: `T6-02/31`.

| Claimed | Read from pixels | Verdict |
|---|---|---|
| Tape 02: Case 11 / Tin bird unauth **00:33:30–00:33:34** | `[bar]/11` `00:33:30`(f1049) → `00:33:34`(f1233–1247) | **seconds range exact.** Tape number **redacted → unverifiable** |
| Tape 02: Case 12 / Mk.4 taxi **01:08:21–01:08:22** | `[bar]12` `01:08:21`(f1250–1267) → `01:08:22`(f1268–1298) | **exact.** Tape redacted |
| Tape 02: Case 12 / Mk.4 pace lap **01:10:55–01:11:21** | `[bar]/12`; `01:10:55` begins f1308; last value present is **01:11:20** (f2458–2498). `01:11:21` would begin at f2504 — **6 frames after the cut at f2498** | **start exact; end is 1 s short of the claim.** Tape redacted |
| Tape 05: Case 26 / Tim's show &tell **01:01:18–01:01:19** | `[bar]/26` `01:01:18`(f2502–~2547) → `01:01:19`(~f2548–2568) | **exact.** Tape redacted |
| Tape 06: Case 31 / Mk.5 virgin (col/s) **00:57:56–00:58:04** | `T6-02/31` `00:57:56` begins f2572 (= first frame of the shot) … `00:58:03` last legible (f2884–2917). `00:58:04` would begin f2929, inside the near-black tail | **start exact and tape number confirmed (T6 = Tape 06); end not verifiable** |

**No timecode falls outside a claimed range**, and none is non-monotonic. Note the description's Tape-02/Tape-05 attributions are asserted but cannot be checked: exactly one of the five tape fields is legible, and that one agrees.

---

## 3. Timecode cadence / playback-speed ratio

I located tick boundaries to **single-frame precision** by reading the seconds digits frame-by-frame from high-pass-enhanced crops.

| Fragment | Exact tick frames | Frames per 1 s of burned-in TC |
|---|---|---|
| Case 11 | f1095 (→31), f1141 (→32); f1187 and f1233 consistent to ±2 | **46.0** |
| Case 12 pace lap | f1354 (→56), f1400 (→57), f1446 (→58) | **46.0** |
| Case 31 colour | f2706 (→59), f2751 (→00), f2884 (→03); (2884−2706)/4 = 44.5 exactly | **44.5** |
| Case 12 taxi, Case 26 | one tick each; both consistent with 46 | 46 (assumed) |

**Playback ratio vs the burned-in source clock:**
- b/w fragments: 29.97 / 46.0 = **0.6515×** (1 source second → 1.535 s of screen time)
- colour fragment: 29.97 / 44.5 = **0.6735×** (1 source second → 1.485 s)

**This is not the ~0.55× attributed to the 2011 originals.** Same direction (slowed), measurably different magnitude — ~0.65–0.67× here, and the colour fragment is retimed ~3.4 % differently from the b/w ones.

### Underlying temporal structure (this is where the strongest measurements are)
- **Bit-identical frame pairs on a strict 12-frame period**: f1611, 1623, 1635, 1648, 1660, 1672, 1684, 1696, 1708 … 2030, and f2578, 2590, 2602 … 2878. Confirmed independently by LK residual (rms 0.08–0.39 at those frames vs 1.3–15 elsewhere, dx = dy = 0.000) and by tracked-feature exact repeats. One duplicate per 12 output frames ⇒ an **11:12 rate/speed conversion** in the chain (pre-conversion rate 29.97 × 11/12 = **27.47 fps**).
- **In the b/w shots the picture advances in bursts.** Motion-compensated frame-to-frame residual is bimodal (median 2.60; 1–3 between bursts, 6–15 at a burst). Counting bursts inside consecutive 46-frame tick intervals across the whole pace lap: 15, 16, 16, 15, 16, 16, 15, 18, 17, 18, 22, 17, 17, 16, 18, 17, 17, 17, 17, 16, 17, 16, 16, 17 → **16 ± 1 distinct source images per second of burned-in timecode**. 46/16 = 2.875 output frames per source image — self-consistent with a **16 fps** source slowed to 0.6515×. (16 fps is a historically standard silent/amateur cine rate; I state the arithmetic, not a conclusion.)
- **The slowdown is by frame repetition, not blending/optical flow.** Dust specks appear at *identical* amplitude in the frames of a hold group with no ghosting in neighbours: f1032 −178.0 / f1033 −178.0; f1026 −177.0 / f1027 −177.0; f1013 −181.0 with −7.0 / −7.0 either side.
- **The colour shot behaves differently.** A tracked doorframe edge (f2790–2849) moves smoothly 3–15 px *every* frame, with exact repeats only on the 12-frame beat. No burst structure. So either its source ran at a much higher rate or intermediate frames were synthesised. 44.5 × 11/12 = 40.8 distinct images per source second, which is not a plausible 1961 camera rate — so *some* retiming beyond simple frame-holding is implied for this shot. **I cannot distinguish which.**

---

## 4. The disputed claim ("at 1:24 … FIVE fingers")

The shot is Seg 5, f2502–2568. t = 84.0 s is **f2518**. I examined f2502–2568 at up to 6× zoom, with percentile and local-contrast stretches, and with 5- and 8-frame averages over near-duplicate groups (f2529–2533, f2545–2552) to suppress compression noise.

**What is actually there:** a hand with **one** long, clearly separated digit extended and pointing up-left, and the rest of the hand folded. Below/left of the extended digit there is a second slender element with a dark gap between them — plausibly the thumb, but I would not certify it. The folded mass shows 1–3 low-contrast lobes that could be knuckles or could be tonal structure.

**Is the image quality sufficient to count? No.**
- Measured **10–90 % edge rise ≈ 15 px** on a high-contrast edge in this shot (8-frame average, row y = 900: 63 DN at x 1145 → 197 DN at x 1163).
- Radially averaged power spectra at f1200/1400/1900/2520/2700/2800 knee at ≈0.09 cycles/px (detail scale ≈ 11 px) and then hit a flat floor.
- **No grain to help**: high-pass RMS in a flat sky region (f1330–1390, x 400–700, y 180–420) is **0.26 DN out of 255**. The finest visible structure in the image is H.264 macroblocking (verified visually at f1320/f1330).
- The whole hand spans ~250 px; the extended digit's FWHM is ~40 px. Adjacent folded digits would be ~30–50 px apart — at or below a 15 px PSF with no texture.
- **Critical contamination the commenter almost certainly hit:** the burned-in timecode glyphs `01:01:18`/`19` occupy x ≈ 880–1030, y ≈ 935–1000 — **directly across the lower-left of the fist**, exactly where knuckles would be counted. They are stationary in frame coordinates while the hand moves (unambiguous in the f2530–2568 montage), so bright "finger-like" lobes in that area are partly overlay text.
- 8-frame averaging does **not** resolve individual digits.

**Adjudication:** "five fingers" is **not supportable** from the pixels. "Four" is equally unsupportable. **Digit count: undetermined.** On the separate charge that the scene looks "rigid": the shot does have continuous camera drift (up to 3 px/frame) and the hand does move, but because of the ~2.9-frame content hold the picture only *changes* about every 2.9 frames — which is a sufficient mechanical explanation for a stepped/stiff read, independent of origin.

---

## 5. Damage / dirt behaviour — the layering test

This is the test the brief flags as the cheapest tell. **It comes out on the side of the damage belonging to the picture, not floating over it.**

- **Lifetimes are short and match the retiming.** Blank leader f950–1039: run-length histogram of dark marks = 71 928 runs of 1 frame, 234 089 of 2, 11 817 of 3, essentially nothing longer; **mean 1.83 frames**. Picture-bearing footage, pace-lap sky f1600–1949: 799 compact-blob tracks, **mean length 2.03** (405 of 1, 187 of 2, 122 of 3, 47 of 4). With one source image occupying ~2.9 output frames, a 1-source-frame dirt event should live 1–3 output frames. That is exactly what is measured.
- **Amplitude is preserved across a hold group** (see §3) ⇒ the dirt was present **before** the frame-repeat stage. A damage layer stamped on at the end at 29.97 fps would give 1-frame marks and would vary per output frame. It does not.
- **No gate-locked persistent dirt.** High-pass of the 90-frame temporal median of the leader: σ = 0.37 DN, min −7 DN. Nothing fixed. (My first, percentile-stretched look suggested persistent blobs; that was an artifact of stretching a near-flat field — the "blobs" were the vignette plus macroblocks. Corrected.)
- **No damage over the black surround.** Outside the aperture (x < 180, x > 1760) temporal σ = 0.37–0.98 DN over 100-frame windows, at a level of 10–22 DN (not pure #000). Nothing floats over the letterbox.
- **The Russian editorial captions, by contrast, are clipped at the aperture too** (no signal at x 1630–1780 when the caption is on) — so they are composited inside the film-frame area, not slapped over the whole 16:9 canvas. Their vertical position could not be tracked (they fade in/out), so I cannot say whether they share the film layer's wobble.
- **Other damage-class events**: 2–5 near-black frames at every shot junction (f1045–1048, f1299–1303, f2499–2501, f2569–2570); two mid-shot events (f1208–1209 dark + frame-pull; f2540–2541 brightness dip); a faint curved bright scratch plus dust visible in the near-black tail at f2970 under extreme stretch.
- **One repetition worth flagging:** the two sweeping bands at f1148–1151 and f2462–2466 are in different shots 44 s apart yet share the same start row (≈244), the same speed (≈5 rows/frame), the same 4–5-frame life, and the same dark-trough-over-bright-band profile (row-profile r up to 0.836). That is consistent **either** with a recurring transfer/tape artifact **or** with a reused effect element. **I cannot distinguish.**

---

## 6. Film-frame border / "gate"

**It is a soft vignette, not a sharp gate.** 50 % points: left x ≈ 290–320, right x ≈ 1598–1616, top y ≈ 15–35, bottom y ≈ 1041–1049 (≈1325 × 1035 px), with the transition spread over **60–90 px**. Corners are rounded (clearest in the f2970 extreme stretch and the leader).

**It is NOT frozen.** Sub-pixel Lucas–Kanade fit of shift + gain + brightness ramps on the high-gradient border band:
- pace lap f1310–1470: **dx σ = 0.286 px** (range 1.86), **dy σ = 0.555 px** (range 3.03)
- leader f950–1040: dx σ = 0.94 px (range 7.1); dy unreliable there (flat-field brightness ramps contaminate it)

**But the motion is temporally smooth, not per-frame random.** It drifts, with runs where it is frozen to <0.1 px (e.g. f1336–1344: dx −0.011, +0.042, −0.082, −0.044, −0.028, +0.035, −0.141), then moves again. This tracks the ~3-frame content-hold cadence rather than independent per-frame weave.

**The burned-in overlay moves with the border.** Correlating the LK border offsets against sub-pixel template tracking of the overlay strip (x 300–1060, y 915–1010) over f1310–1469: **r = −0.753 (dx), −0.542 (dy)** — negative because the two estimators use opposite sign conventions, i.e. **common motion**. Overlay dx σ = 0.48 px vs border dx σ = 0.29 px. Independent corroboration: integer-shift alignment of the whole overlay strip returns (0, 0) for all 250 frames tested.

**Consequence:** there is **no measurable relative weave** between the border and the burned-in timecode, while the picture inside moves independently (3–15 px/frame in the colour shot). That is what you get if the border is the boundary of the *recorded video frame* — with the timecode burned into that frame — and the whole composite was later given a sub-pixel wobble. It is *not* what a projector/telecine gate with weaving film in it produces, where the border would be fixed and the image would move within it. **Caveat: every amplitude here is under 1 px and my estimator noise is ~0.2–0.3 px, so this test has limited power.**

**Across shots** the border sits in approximately the same place: right-edge 50 % point x = 1598–1616, left edge x = 289–322 (temporal-max method; the spread is at least partly explained by dark content sitting on the frame edges). **I could not establish pixel-exact identity of the border between shots.**

---

## 7. Coherence / artifact hunt — both directions

**Consistent; no artifact found:**
- The white outline markings on the objects in Seg 5 keep a **stable geometry across all 67 frames** while translating with the camera (f2506/2514/2522/2530/2538/2546/2554/2562). No mutation.
- Rows of dark fasteners on the white fuselage in the pace lap stay regularly spaced and consistent (f1450, 1600, 1720).
- The disc's shading is self-consistent and physically ordinary: specular highlight on the upper-left rim, shaded underside with a distinct lip — one high-left source, held across all of Seg 2 and the early pace lap.
- The wiggly line over the window is a **physical wire/aerial, not a scratch**: it moves with the aircraft structure and its shape changes smoothly and plausibly as it flexes (f1700–2050).
- The disc's centroid path is smooth: f1780–1829, 1–4 px/frame, no teleporting.
- **No interlace combing anywhere.** The comb-metric maxima (concentrated f1304–1354) are 1-pixel horizontal banding from compression/upscaling, confirmed visually at f1320/f1330 — not fields.
- No exact-duplicate whole frames in the footage other than the strict 1-in-12 beat.
- No limb/finger changing count or length; no melting or warped edges; no detail changing identity between frames; no text or marking that mutates.

**Weight of that negative result:** low. With a ~15 px effective PSF, zero grain (0.26 DN), and visible macroblocking, there is very little fine detail in which such artifacts *could* be seen. Absence here is not evidence of absence.

**Could not determine:** whether the imagery is photographic in origin. The spectral roll-off (knee ≈0.09 cyc/px, flat floor beyond), the absent grain, and the macroblocking are equally consistent with (a) a genuinely low-resolution transfer upscaled to 1080p and pushed through YouTube, and (b) a low-resolution synthesis upscaled the same way. I did not analyse chroma subsampling or colour fringing in the one colour fragment.

---

## 8. Explicitly undetermined

1. Tape numbers for four of the five fragments (redacted bar). Only `T6-02/31` is legible.
2. Whether 00:58:04 (Case 31) is actually present — it falls inside the near-black tail f2918–2977.
3. Whether the colour fragment's smooth per-frame motion comes from a high-rate source or from synthesised intermediate frames.
4. The digit count on the hand at t ≈ 84 s.
5. Pixel-exact identity of the border between shots.
6. Whether the two matched sweeping bands (f1148, f2462) are a recurring transfer artifact or a reused element.
7. Whether the dirt is locked to the image or to the frame — marks live only 1–3 frames, over which the image moves <1–3 px, below the discrimination threshold.
8. Origin of the material. The resolution does not support a determination in either direction, and I am not offering one.
