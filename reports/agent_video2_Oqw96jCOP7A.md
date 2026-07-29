# Agent report — Forensic frame analysis, video 2 (`Oqw96jCOP7A`)

*Archived verbatim from the "Forensic analysis video 2" subagent, 2026-07-26.
Working files referenced: `/home/user/new-skinny-bob/analysis/teardown-video2/`.*

---

# Frame-level forensic analysis — `Oqw96jCOP7A`
### "ET crew recovery site D, survival of EBL Tim +2, skinny Bob"

**Material analysed:** 2503 PNG frames, 1920×1080, at `/home/user/new-skinny-bob/frames/Oqw96jCOP7A/fNNNNN.png`; 29.97 fps (2503 / 83.54 s = 29.96). Metadata: `/home/user/new-skinny-bob/videos/2026/Oqw96jCOP7A.info.json` — uploader `qtecqot`, upload_date 20260615, category "News & Politics", every delivered format reported at fps = 30. Working outputs and scripts: `/home/user/new-skinny-bob/analysis/teardown-video2/`.

**Stance:** provenance is treated as undetermined. Findings below are grouped so that observations pointing in different directions are given equal prominence. Everything under "OBSERVED" is a measurement; everything under "INFERENCE" is my reading of it; "COULD NOT DETERMINE" is explicit.

---

## 1. Shot-by-shot log

Frame ↔ time: `frame = round(s × 29.97) + 1`.

| Frames | Time | Content | Camera | Burned-in overlay (read at full res) |
|---|---|---|---|---|
| f1–f10 | 0.00–0.30 | Black. f2–f10 bit-identical to f1. | — | none |
| f11–f389 | 0.33–12.9 | Static title card: white monospace text on black reproducing the YouTube description's fragment table. Text pixel count constant (94,416–94,566 px > value 10 across f12–f380). **No grain, no dust, no damage anywhere on this card.** | static | n/a |
| f390–f414 | 13.0–13.8 | Card fades to black (f400 max=180, f410 max=62, f415 max=4). | — | n/a |
| f415–f456 | 13.8–15.2 | Pure black; frames bit-identical; max value 2 (codec noise). | — | none |
| f457–f707 | 15.2–23.6 | **Tape 02 / Case 11 "Tin bird primer."** A large smooth pale ovoid form (reads as the nose/forward fuselage of a big object) filling frame left-of-centre, carrying a dark angular emblem at ≈(x 800–900, y 470–560), against a clipped-white sky and a dark conifer treeline. By f600–f707 the pale form is a diagonal mass across the top and a flat pale field is revealed with a low ridge, **3–4 small dark standing human figures** mid-field (f600, f660, f700), and a large pale ribbed structure at frame right. Highlights heavily clipped. | Large motion early (12.84 px at f619), then global shift ≈ 0 from f623 with discrete jumps of 1–7 px | `/11 00:36:02` → `00:36:07` |
| f708–f710 | 23.6 | Cut. | | |
| f711–f967 | 23.7–32.2 | **Tape 04 / Case 20 "Brown boys" (a).** Murky, very low-contrast grey field with a large dark irregular mass (f730, f800, f880) — reads as disturbed/excavated ground or a debris mound. Internal cut ≈f932. | 87.5% of frame pairs have zero global shift (median 0.007 px) | `/20 00:03:11` → `00:03:18` |
| f968–f1017 | 32.3–33.9 | **"Brown boys" (b).** Bright flat pale ground; **two dark human figures walking away from camera**, the nearer in a peaked/military-style cap (f1010). A thin bright vertical line runs full frame height at x≈600 (f1010) — scratch-like. | near-static | `'20 00:03:55` → `00:03:56` |
| f1018–f1203 | 33.9–40.1 | **"Brown boys" (c).** Overexposed pale ground; from f1120, two or three pale lumpy elongated forms on the ground with darker mottling (f1120, f1180). Not resolvable enough to identify. | near-static | `'20 00:04:02` → `00:04:11` |
| f1204–f1206 | 40.1 | Cut. | | |
| f1207–f1414 | 40.2–47.2 | **Tape 04 / Case 21 "Triage."** Extreme close-up of a large-cranium hairless head, ¾ view, filling frame. Single strong key from upper left; prominent brow ridge, deep hollow cheek, one very large dark eye with a bright specular arc on its upper margin, small nose with a bright specular, small mouth. Dark background with faint vertical striping. | 48.0% zero-shift pairs, median 0.053 px, max 7.6 px | `/21 00:15:01` → `00:15:06` |
| f1415 | 47.2 | Cut. | | |
| f1416–f1444 | 47.2–48.2 | **Tape 04 / Case 22 "Exit EBL04" (a).** A head on a white pillow with white bedding: compact, dark-toned (hair/beard-like), **normal cranial proportions**, open mouth with a bright interior. Morphologically unlike the grey heads elsewhere. | slow reframe | `BL04 /22 00:30:26` |
| f1445–f1569 | 48.2–52.4 | **"Exit EBL04" (b).** Same bed, pillow, framing and lighting — now a **large-cranium grey-type head**, eyes closed or deeply shadowed, with a small bright point highlight at the top of the visible eye (f1460, 1480, 1500, 1540, 1560). A curved dark band crosses frame left. | 46.7% zero-shift pairs, median 0.058 px | `BL04 /22 00:30:31` → `00:30:34` |
| f1570–f1613 | 52.4–53.8 | **"Exit EBL04" (c).** Same subject, camera repositioned, head lower in frame, white sheeted mass foreground. | reframe | `BL04 /22 00:31:13` → `00:31:14` |
| f1614–f1620 | 53.8–54.1 | Cut. | | |
| f1621–f1835 | 54.1–61.2 | **Tape 05 / Case 25 "Bob's walkabout."** Exterior daylight. A slender figure standing centre frame facing camera: bright hairless dome cranium with a **persistent dark patch on the upper-left crown**, black facial mask region with two black almond eyes, small bright nose highlight, very narrow neck, dark torso with arms hanging at the sides. Background: pale sloping rubble ground, a pale rectangular structure frame right, dark objects on the ground. **The figure does not walk — it stands in place for the whole fragment.** | 77.0% zero-shift pairs (median 0.017 px); framing changes sharply f1761–f1783 | `/25 00:02:07` → `00:02:12` |
| f1836–f1839 | 61.3 | Cut. | | |
| f1840–f2422 | 61.4–80.8 | **Tape 05 / Case 25 "Slim Tim."** Interior. Head-and-shoulders of a large-cranium grey-type figure; bright flat wall/panel frame left, darker wall right. Head turns from near-profile (f1845–f1985, badly over-exposed) to nearly frontal (f2005–f2245) then away (f2265–f2405). Dark shoulders. Two internal splices (f1993, f2248). | Locked early; genuine large camera movement f2270–f2420 (only 16.7% zero-shift pairs, median 7.94 px) | `/25 00:40:12` → `00:40:40` |
| f2423 | 80.8 | **Hard cut of picture AND overlay text to black in one frame** (inner-frame mean 90.4 → 0.059; overlay-text box mean 116.2 → 0.000). No fade. | | none |
| f2423–f2458 | 80.8–82.0 | **Pure black picture with only dirt/scratch specks visible** (600–3200 px > value 10 per frame; peak values 52–80). | | none |
| f2459–f2503 | 82.0–83.5 | Completely clean black (max 2–3 = codec noise). | | none |

---

## 2. Catalog verification

### Overlay format (measured at full resolution)
- Monospace numeric/uppercase, white, blended over the picture. **12 visible character cells: `/NN HH:MM:SS`.** Character pitch **≈ 40.6 px**; glyph rows y ≈ **942–985** (cap height ≈ 44 px); string spans x ≈ **510–1005**.
- Left of the `/` there is a rectangular zone ≈ x 300–505, y 930–995 in which the picture is suppressed to a flat low level. **Its boundary is a soft ~12–15 px gradient, not a hard-edged bar** — measured vertical profile at x=400: f770 goes 56 → 16 over y 924–938; f1660 goes 16 → 30 over y 917–929.
- **Only in the Case 22 fragments** four further characters `BL04` are visible inside that zone (x ≈ 305–460), **left-clipped by the edge of the picture area at x ≈ 305** (f1420–f1610). The visible string there is `…BL04 /22 HH:MM:SS`, consistent with the case name "Exit EBL04". All other fragments show only `/NN`.
- **Glyph variation:** the character immediately before the case number reads as a complete `/` in Case 11, 21, 22, 25 and in Case 20 00:03:11–00:03:18 (f770, f900), but as a short **top-only stroke** (apostrophe-like) in Case 20 00:03:55–00:04:11 (f968, f1050, f1150). Glyph position is unchanged; only its lower-left portion is missing. INFERENCE: most consistent with the suppression zone reaching slightly further right in those frames, not a different glyph.
- A small bright dot sits immediately right of the last character in some fragments (after `BL04`, f1416–f1613; after the `4` of `:14`, f868–872), consistent frame to frame.
- **The overlay text sits at a fixed raster position:** vertical centroid of its high-pass energy = **964.1 px, σ = 1.6 px** over the whole video, and within **±0.7 px** if the five badly clipped frames are excluded.

### Claimed vs observed

| Claimed (description) | Observed frames | Observed timecodes | Verdict |
|---|---|---|---|
| T02 C11 Tin bird primer 00:36:02–00:36:07 | f457–f707 | :02 :03 :04 :05 :06 :07 | **exact — all 6 s present** |
| T04 C20 Brown boys 00:03:11–00:03:18 | f711–f967 | :11 :12 :13 :14 **:16** :17 :18 | in range, **00:03:15 entirely absent** |
| T04 C20 Brown boys 00:03:55–00:04:05 | f968–f1151 | 03:55 03:56 ‖ 04:02 :03 :04 :05 | in range, **00:03:57–00:04:01 absent** |
| T04 C20 Brown boys 00:04:10–00:04:11 | f1152–f1203 | 04:10 04:11 | **exact** |
| T04 C21 Triage 00:15:01–00:15:06 | f1207–f1414 | :01 :02 :03 :04 :05 :06 | **exact — all 6 s present** |
| T04 C22 Exit EBL04 00:30:26–00:31:14 | f1416–f1613 | 30:26 ‖ 30:31 :32 :33 :34 ‖ 31:13 :14 | in range, **only 7 of 49 claimed seconds present** |
| T05 C25 Bob's walkabout 00:02:07–00:02:12 | f1621–f1835 | :07 :08 :09 :10 :11 :12 | **exact — all 6 s present** |
| T05 C25 Slim Tim 00:40:12–00:40:40 | f1840–f2422 | :12 :13 :14 :15 ‖ :19 :20 :21 :22 :23 :24 :25 ‖ :36 :37 :38 :39 :40 | in range, **:16–:18 and :26–:35 absent** |

**No timecode anywhere in the video falls outside the claimed ranges.** Every case number observed (11, 20, 21, 22, 25) matches the description. Four of the eight listed ranges are, however, **not continuous** — they contain internal splices.

Notable specifics, verified frame by frame:
- **00:03:15 is missing with no visible cut.** f872 reads `:14`, f873 reads `:16` (checked at every frame f868–f879, montage `edge873.png`). The `:14` tick is truncated to 21 frames instead of 45.
- Slim Tim splice at f1993: f1984–f1992 read `:15`, f1993–f1996 read `:19` (only 4 frames), f1997 onward `:20`. Second splice at f2248: f2226–f2247 read `:25`, f2250 onward `:36`.
- Case 22 splices at f1445 (30:26 → 30:31) and f1570 (30:34 → 31:13).
- **Triage does contain 00:15:06** (f1402–f1414) — my first automated pass merged it with `:05`; direct reading (`gt_1180_1620.png`) corrects that.

---

## 3. Timecode cadence

**Method:** high-pass filtered crop of the two seconds digits (x 905–1000, y 938–990) correlated between frames; a run with r > 0.90 is one tick. Independently confirmed by direct visual reading of the digits at 6- and 10-frame intervals across the whole video, and frame-by-frame at every boundary quoted.

### Seven of eight fragments: a consistent 45 frames per tick

| Fragment | Tick-boundary frames | Tick lengths |
|---|---|---|
| C20 Brown boys | 761, 807, 852 · 914, 959 · 1058, 1102, 1147 | 46, 45 · 45 · 44, 45 |
| C21 Triage | 1221, 1266, 1311, 1356, 1401 | 45, 45, 45, 45 |
| C22 Exit | 1464, 1508, 1553 | 44, 45 |
| C25 Walkabout | 1641, 1686, 1731, 1777, 1823 | 45, 45, 46, 46 |
| C25 Slim Tim | 1997, 2042, 2086, 2131, 2177, 2222 · 2277, 2322, 2367, 2412 | 45, 44, 45, 46, 45 · 45, 45, 45 |

Aggregate **44–46 frames per tick, mean ≈ 45.0.** At 29.97 fps, 1.5 s = 44.955 frames, which predicts exactly the observed 45/45/45/45/44 alternation.

> **Ratio: 1.000 s of burned-in source timecode = 1.5015 ± 0.02 s of video ⇒ playback ratio 0.666 ± 0.01, i.e. 2/3 speed.** Consistent within measurement error across Tape 04 Cases 20, 21, 22 and Tape 05 Case 25.

### The one exception: Case 11 "Tin bird primer" is NOT on this cadence
Boundaries (both methods): `:02→:03` at **f519 ± 2**, `:03→:04` at **f553 ± 2**, `:04→:05` at **f588 ± 1**, `:05→:06` at **f634 ± 1**, `:06→:07` at **f678 ± 2**.

| Tick | Length (frames) | Implied s/s |
|---|---|---|
| :02 | ≥ 62 (fragment starts mid-tick at f457) | ≥ 2.07 |
| :03 | 33 | 1.10 |
| :04 | 35 | 1.17 |
| :05 | 46 | 1.53 |
| :06 | 44 | 1.47 |
| :07 | ≥ 30 (truncated by cut at f708) | — |

So within this single fragment the ratio varies from ~1.10 to ~1.53 s/s and increases monotonically over :03→:05. **CONFIDENCE NOTE:** the f519 and f553 boundaries are unambiguous and confirmed by two independent methods; the :05 and :06 boundaries are lower-confidence because the picture behind the overlay is clipped near-white there.

**Answer to the brief:** the cadence is highly consistent (45 frames/tick, 2/3 speed) across seven of eight fragments and non-constant in one.

---

## 4. The figure

### Fingers / digits — COULD NOT DETERMINE, anywhere in this video
- Walkabout (f1621–f1835): arms hang at the sides but the entire lower body including the hands is a near-black silhouette (values 10–30 against a 60–120 background). Lifting shadows aggressively (f1660, f1700, f1740 at percentile stretch 30–99.9, `walk_body.png`) shows arm contours but **no separable digits**.
- Exit (f1460, f1500): a pale irregular form below the head could be a hand or a shoulder/bedding; not resolvable.
- Triage and Slim Tim: no hands enter frame.
- The measured effective resolution (§5) makes finger counting physically impossible here. **I therefore can neither confirm nor refute the "black nails" detail from the other video.**

### Proportions — OBSERVED
Walkabout (f1621–f1835): bright cranial dome ≈ 150 × 130 px, visible neck ≈ 55 px wide, shoulders ≈ 230 px — an unusually large head-to-shoulder ratio and a very slender neck. Slim Tim (f2200): head ≈ 330 px wide with a cranium that overhangs the brow.

### Eyes — reflective in three fragments, matte in one
Large almond/teardrop shape; **no sclera, iris or pupil structure resolvable anywhere.**
- **Specular** — Triage: a distinct bright **curved arc along the upper margin of the eye** (f1250, f1330, f1370 clearly; f1215 in a different position). Curvature and position are what a single key above/left would produce on a wet, convex surface.
- **Specular** — Exit: a small bright point highlight at the top of the visible eye (f1460, 1480, 1500, 1540, 1560).
- **Specular** — early Slim Tim near-profile: a thin bright arc along the upper eye margin (f1865, 1885, 1905, 1925, 1945, 1965).
- **Matte** — Slim Tim frontal section: f2176–f2222 sampled every 2 frames (`blink_search.png`) shows a uniformly black eye region with zero internal structure and **no catchlight at all**.

INFERENCE: the highlight appears and disappears with head/light geometry, which is how a genuine specular surface behaves. This is a point **in favour** of optical/physical coherence.

### Blinking — none observed; not a determination
f2176–f2222 (46 consecutive frames, sampled every 2) shows constant eye shape. No frame in any fragment shows a closed or partly closed lid. **No eyelid line or crease is resolvable, so I cannot say whether the anatomy has lids.** The absence of a blink over ~19 s of source time in Slim Tim is an observation, but that fragment is heavily cut and I only sampled densely in one 46-frame window.

### Motion — evaluating "moves like a GTA character standing idle"
- **The figure never walks in this video.** In the fragment labelled "Bob's walkabout" it stands in one place throughout; the head reorients and the body makes small postural changes.
- **Direct test for a looping idle animation:** self-similarity of the head region vs temporal lag.
  - Walkabout f1775–f1835: r = **+0.929** at lag 1, decaying **monotonically** to +0.348 at lag 28, +0.347 at 29, +0.351 at 30 — no revival at any lag.
  - Slim Tim f2137–f2249: r = **+0.976** at lag 1 → **+0.780** at lag 30, monotonic, no revival.
  - A looped idle animation would produce a correlation **revival** at the loop period. **None is present.** On this evidence the "GTA idle loop" characterisation is **not supported** — the pose drifts progressively and does not cycle.
- **However**, a separate real finding does bear on any impression of unnatural motion: **the picture is pixel-locked.** Fraction of consecutive frame pairs whose global inter-frame translation (phase correlation over x 400–1550, y 120–960) is below 0.05 px: Case 20 f760–960 **87.5%** (median 0.007 px); Walkabout f1630–1830 **77.0%** (median 0.017 px); Triage f1210–1410 **48.0%** (0.053 px); Exit f1445–1610 **46.7%** (0.058 px); Slim Tim end f2270–f2420 **16.7%** (median 7.94 px — genuine large movement). Over long stretches the image does not move at all, then jumps discretely.

### Clothing — COULD NOT DETERMINE
Walkabout torso and arms are a dark silhouette; boosting reveals a lighter V-shaped region below the neck and a lighter horizontal band across the upper chest (f1660, f1700) that could equally be a garment edge or the clavicle/sternum contour under grazing light. Slim Tim shoulders are dark with a faint lighter diagonal (f2200, f2265–f2405). **No collar, seam, fastening, cuff, hem or fabric fold identifiable.**

### Other markings — OBSERVED, and temporally coherent
A dark patch on the upper-left of the crown in the Walkabout holds **the same position on the skull** across f1621, 1628, 1635, 1642, 1649, 1656, 1670, 1677, 1684, 1698, 1719, 1726, 1733 as the head reorients (`walk_head.png`). A small dark speck on the crown in Slim Tim at ≈(1330, 248) (f2200).

---

## 5. Artifact hunt — findings in both directions

### 5a. The film damage layer is demonstrably separate from the picture and independently timed (highest-confidence finding)

**(i) It outlives the picture by 36 frames.** At f2422 → f2423 the picture *and* the burned-in timecode both cut hard to black in one frame (inner-frame mean 90.4 → 0.059; overlay-text box mean 116.2 → 0.000). The dirt/scratch layer does not stop: it continues over pure black through **f2423–f2458** (600–3200 px above value 10 per frame, peak values 52–80), then stops completely at f2459 (max value 2). See `tail_2432.png`, `tail_2440.png`.

**(ii) It is matted with the picture but not timed with it.** Union bounding box of specks over f2424–f2457 is **x 320–1606, y 27–1049** — always inside the aperture, never in the surround.

**(iii) Its cadence is a strict repeating 3,2,2 pattern.** Per-frame Jaccard overlap of thresholded speck masks over f2422–f2459 is **bimodal with nothing in between**: consecutive frames either share the pattern (J = 0.97–1.00, and J = 1.0000 exactly at f2448→f2449) or share essentially nothing (J = 0.000–0.016). Group lengths: **3, 2, 2, 3, 2, 2, 3, 2, 2, 3, 2, 2, 3, 2, 2** — period exactly **7 output frames per 3 patterns = 2.3333 frames/pattern = 12.844 patterns/s.** Independently confirmed: autocorrelation of the frame-difference series over the same range peaks at **lag 7 (r = +0.72)** with troughs at lags 6 and 8 (r = −0.62, −0.60).

**(iv) It is not synchronised to the burned-in timecode.** 45 frames/timecode-second ÷ 2.3333 frames/pattern = **19.29, not an integer.** If the dirt were physically on the film whose frames the timecode counts, dirt-frames per timecode second would have to equal the film's frame rate, an integer.

**(v) It does not loop.** No Jaccard revival at any lag 3–16 (all mean ≤ 0.005); the patterns are individually distinct, just held 2–3 frames each.

**Answer to the brief's question:** the damage **floats over the image as a separate composited layer.** Concretely, within a held-plate group the dirt is bit-for-bit unchanged while the picture beneath changes — measured across nine distinct damage marks in the Case 11 fragment (f651, f652, f657, f678, f679, f681, f682, f685, f692): dirt-mask centroid displacement **4–63 px between plates, 0 px within a plate**, against a simultaneous image displacement of **≤ 0.11 px**.

**INFERENCE, carefully bounded:** this establishes that the dirt/scratch damage was **added in post as an independently-timed layer**. It does **not** by itself say anything about the provenance of the picture underneath — a film-look/damage pass is routinely applied to genuine archival footage as well as to synthetic footage.

Scratch geometry: heaviest damage columns at x **412–429** (an ~18 px band), **541–555**, **612**, **680–681**, **1511** — vertical scratch-like features consistent with film transport direction.

### 5b. Frame-rate structure of the delivered file
- **94 frames are bit-identical to their predecessor**, almost all in the static title card (f2–f10, f417–f456) and the clean black tail (f2467–f2503).
- Within the picture, a distinct set is *near*-identical (full-frame mean abs diff **0.02–0.06** vs a typical 0.3–4.0, fewer than 200 pixels differing by more than 4): **f1019, 1031, 1043, 1055, 1067, 1079, 1091, 1103, 1115, 1127, 1139, 1151, 1163, 1175, 1187, 1199, 1211, 1223, 1235, 1247, 1259, 1271, 1283, 1295, 1307, 1319, 1331, 1343, 1355, 1367, 1379, 1391, 1403, 1415, 1427, 1439** — strict period 12, unbroken — and again **f2015 … f2400** at period 12 (one +1 phase slip at f2280).
- **Crucially, the f1019–f1439 series runs straight through the shot cuts at f1207 (Case 20 → 21) and f1415/f1416 (Case 21 → 22) with no phase reset.** A per-clip frame-rate conform would reset phase at each cut.
- **INFERENCE:** a single global retime/conform was applied to the assembled timeline. One duplicate per ~12.09 output frames ⇒ the underlying image sequence ran at ≈ 29.97 × 11/12 ≈ **27.5 unique frames per second** before being conformed to 29.97. All YouTube formats report 30 fps, so this came from the uploaded master, not YouTube's transcode.
- Note the three cadences are mutually unrelated: timecode 45 frames/tick, conform duplicates every 12 frames, damage plates every 2.333 frames.

### 5c. The aperture / "film gate" — measured

The picture sits inside a soft-edged aperture surrounded by a **mathematically flat fill**: standard deviation **exactly 0.000** and mean **exactly 13.00** (f457–f929) or **12.00** (f930–f2349) over large sample regions (top/bottom/left/right strips and corners). **No grain, no noise, no dust anywhere outside the aperture.** From f2350 the fill level ramps 13 → 15 → 16 → 17 → 18 → 19 (f2350, 2360, 2370, 2380, 2403, 2415) in step with the picture brightening, then 0 at f2423 — so the fill is *inside* the final grade.

**Jitter measurement (direct answer):** over f2000–f2100 (101 consecutive frames), per-pixel temporal standard deviation along row 540 is **exactly 0.000 for every x ≤ 254**, only 0.10–0.77 across x 260–290, and becomes substantial only from x ≈ 296. On the right, temporal σ is **exactly 0.000 for every x ≥ 1626**. Vertically at x = 960, σ is **exactly 0.000 for y 48–60**.

> If the aperture moved by even one pixel between any two of those 101 frames, boundary pixels would sometimes carry picture and sometimes carry the flat fill, and σ there could not be zero. **The aperture boundary is pixel-identical across frames — zero measurable jitter, not the ±0.3–1 px weave of a mechanical projector or film gate.**

Two caveats stated explicitly:
1. **It is not a hard-edged rounded-corner mask.** It is a soft **40–80 px vignette gradient** blending into the flat fill (row 540, f2000: 12.00 at x=254 → 12.17 at 290 → 13.6 at 296 → 20.3 at 308 → 33.5 at 320 → 68.6 at 344 → 96 at 404), and its inner shape is **irregular and ragged** rather than a clean rectangle (`matte_2200.png`, `matte_900.png`). The left-edge position also differs by up to 58 px between fragments (x ≈ 256 in Slim Tim/Walkabout/Tin bird, 274 in Exit, 314 in Triage).
2. Because the outermost picture pixels are attenuated to well under half a code value, a **sub-pixel weave of the picture inside a rigidly fixed matte** would not be detectable at the boundary. What is unqualified: the matte does not move; and (from §4) the picture inside it does not drift sub-pixel either, median inter-frame displacement 0.007–0.06 px in the locked-off stretches.

Corroborating: the burned-in text sits at a fixed raster position (σ = 1.6 px overall, ≤ ±0.7 px excluding clipped frames). Text photographed onto weaving film would move with the weave.

### 5d. Effective resolution — the reason several questions are unanswerable
Radial power spectra of a 640 × 640 central patch: power falls from 7 × 10⁻³ at radius 10 to ~10⁻⁷ by radius 80, then flattens into a noise floor. Effective cutoff ≈ **8–13% of Nyquist** (f700: r ≈ 41/320; f1250: 38; f1500: 26; f2100: 29; f2200: 29). High-frequency residual after subtracting a σ = 2.5 blur has σ of only **0.15–1.9 code values**. **The picture is extremely soft — consistent with a low-resolution source (order of a few hundred pixels across) upscaled to 1920 × 1080, or with very heavy filtering.**

### 5e. Grain
**No per-frame independent grain is detectable.** The near-duplicate frames in §5b reproduce to within a mean absolute difference of 0.03 with fewer than 200 differing pixels out of 2.07 million. A photochemical grain layer is statistically independent between any two exposures and would show a full-frame difference of several code values even between otherwise identical frames. Autocorrelation of the high-frequency residual in a flat wall region (f2000–f2400, x 520–1000, y 300–900) shows **no revival at any lag from 3 to 200** (all mean r ≤ 0.015), so there is also **no looping grain plate**; the lag-1 value of 0.36 is explained by persistent image detail.

### 5f. Things I looked for and did NOT find (reported with equal weight)
- **No looping or repeating damage/grain plate** at any lag up to 200 frames.
- **No looping pose cycle** in either figure shot (monotonic self-similarity decay, no revival).
- **No mutating markings.** The dark angular emblem on the pale object in Case 11 keeps a consistent shape and position on the curved surface across f460, 472, 484, 496, 508, 520 while translating with it (`emblem2.png`). The Walkabout crown patch holds position across f1621–f1733. Overlay glyphs are stable in form and position.
- **No digit-count changes** — because digits are never resolvable.
- **No warped or melting object edges, no dissolving/reforming limbs, no background objects popping in and out** that I could identify.
- **Lighting is internally coherent.** Within each fragment the key direction is consistent; shading on the curved cranium is smooth and physically plausible; the eye speculars sit where a single upper-left key would place them; the specular on the pale ovoid in Case 11 tracks surface curvature. **No impossible shadow or contradictory light direction found.**
- **CAVEAT that applies to this whole list:** at an effective resolution of a few hundred pixels, small-scale generative artifacts would be **below the detection threshold.** Absence of evidence here is weak evidence.

### 5g. Anomalies whose cause I could NOT determine
- **Case 22 subject change.** At TC 00:30:26 (f1416–f1444) the head on the pillow is compact, dark-toned, with an open mouth and normal cranial proportions (`wide1418.png`, `human_1430.png`). From TC 00:30:31 (f1445) it is a large-cranium grey-type head in the same bed, framing and lighting (`grey_1460.png`). The timecode jumps 5 s and there is a cut at f1445, so this is presented as two separate moments and could legitimately be two different subjects — the title refers to "survival of EBL Tim +2". **I could not resolve the f1416–f1444 head well enough to identify it** and specifically cannot confirm it is human.
- **Horizontal streak artifacts** — thin light/dark lines a few pixels tall spanning tens of pixels — over mid-tone areas of the figures at f1430 (around the mouth), f1560 (around the eye and lower face), f1789–f1831 (across the face). They resemble line-based dropout or a line-doubling/deinterlace artifact. **Origin (source, upscaler, or codec) not determined.**
- **Faint vertical striping** in the Triage background (f1290, f1405). Not characterised.
- **Missing single second 00:03:15** with no visible picture cut, and the surrounding `:14` tick truncated to 21 frames.
- **Non-constant timecode cadence in Case 11 only** (§3).
- **Possible integer-pixel clustering of image translations — UNCONFIRMED, and I am flagging it as such.** When global shifts do occur they cluster close to whole pixels: (1.95, −7.93), (0.92, 10.73), (1.07, 20.99), (4.94, −3.92), (5.96, −4.04), (−5.04, 6.93), (−0.05, 4.01), (2.00, 1.00), (−3.98, −2.99), (8.94, −7.82), (9.95, −6.97), (24.01, −30.92), (−20.04, −0.90), (−29.03, −3.78), (−21.99, 6.93), (14.01, −24.01), (28.01, −41.01), (70.99, −52.02). Measured distribution of |fractional part| over n = 397: median **0.086**, histogram in 0.05 bins from 0 to 0.5 = [142, 70, 60, 32, 29, 17, 12, 13, 14, 8] against a uniform expectation of 40 per bin. **BUT my control run shows the estimator is itself biased toward integers for small fractions** — injecting known shifts into f2200 gave true 0.15 → measured 0.063; true 0.30 → 0.141; true 0.50 → 0.517; true 1.35 → 1.177; true 3.40 → 3.224; true 7.62 → 7.798 (errors up to ±0.18). That bias alone would map a uniform true distribution into roughly 15–20% of the first bin, not the observed 36%, so there is a residual excess — but it is not large enough, given the estimator's error, to establish integer-only repositioning. **Not established either way.**

### 5h. One internal inconsistency between the stated provenance and the presentation
The description calls the sources "**tapes**" ("sample edited fragments of tapes 02, 04, 05"), but the picture is presented inside a **film-frame-style aperture with a heavy vignette**, and the damage layer is **film-style dirt plus vertical scratches**. Video tape has no film gate and does not accumulate film dirt or transport scratches. This is an inconsistency between the stated medium and the applied look — it says nothing directly about the picture content, but it is worth recording.

---

## 6. Summary of what is and is not established

**Established by measurement (high confidence):**
1. Burned-in timecode advances 1 s per 45 video frames = **2/3 playback speed**, consistent across seven of eight fragments; **non-constant in Case 11** (33–46 frames/tick).
2. The tape/case/name/range catalog in the description **matches the pixels**: all case numbers correct, no timecode outside any claimed range. But **four of eight claimed ranges contain internal splices**, and 00:03:15 is missing outright.
3. The **dirt/scratch damage is a separate composited layer**, matted with the picture but timed independently: it outlives the picture and the text overlay by 36 frames, advances on a strict 3,2,2 (period-7) cadence at 12.844 patterns/s, and is not an integer divisor of the timecode tick. **It floats over the image; it does not track it.**
4. The **aperture is pixel-locked** — temporal σ exactly 0.000 at the boundary over 101 frames. **No gate weave.** The picture inside is likewise pixel-locked (median inter-frame shift 0.007–0.06 px in locked-off stretches). The overlay text sits at a fixed raster position (σ ≤ 0.7 px).
5. A **global period-12 duplicate-frame cadence runs unbroken through shot cuts** ⇒ one conform applied to the finished timeline; underlying sequence ≈ 27.5 unique fps.
6. **Effective resolution is very low** — signal dies at 8–13% of Nyquist.
7. **No per-frame grain**, **no looping grain or dirt plate**, **no looping pose cycle**, **no mutating markings**, **no incoherent lighting** found.

**Points consistent with real optics / hard to fake, reported with equal weight:**
- Eye speculars appear and vanish with light-and-head geometry (arc on the upper ocular margin in Triage f1250/1330/1370; point highlight in Exit f1460–1560; arc in early Slim Tim f1865–1965; absent in the frontal Slim Tim section) — behaviour of a genuine specular convex surface.
- Persistent, correctly-placed surface markings that track their substrate (crown patch f1621–f1733; emblem on the pale object f460–f520).
- Smooth, physically plausible shading on curved surfaces; consistent key direction within each fragment.
- Progressive, non-cyclic pose drift rather than a looped animation.

**Explicitly not determined:**
- Number of fingers/digits, fingernail appearance, presence of eyelids, presence of clothing — all below the resolution floor.
- Whether the figure blinks (no blink seen, but sampling is not exhaustive).
- Identity of the subject at Case 22 TC 00:30:26.
- Origin of the horizontal streak artifacts and the Triage vertical striping.
- Whether image translations are integer-only (control shows my estimator is itself integer-biased).
- **Provenance of the picture content itself.** The layer-compositing findings (§5a) establish that the film-damage look was applied in post; they are equally compatible with a stylised treatment of genuine footage and with a fully synthetic construction. Nothing I measured discriminates between those two.
