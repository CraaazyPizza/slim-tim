# Technical triage — FINDINGS §8, §9, §11, §12, §13, §17, §18/18b

Prepared for the public-facing rewrite. Everything below was re-measured from
`videos/2026/*.mkv`, `videos/2011/*.mkv`, `frames/<videoid>/` and
`frames/<videoid>/` unless marked otherwise. Scripts are in
`analysis/timecode-ticks/`; figures in `figs/technical/`.

Provenance-neutral throughout. The outside analyst is referred to only as "an outside
analyst". No private identity appears here.

---

## 0. Headline results of this pass

1. **The frames-per-tick reconciliation is settled, and the answer is neither number on
   record.** All three 2026 videos hold **45 frames per timecode second in every fragment
   tested**, including the colour Mk.5 clip. §11.2's 44.5 and §30.4's 46.0 are both
   over-precise readings of a segment in which only *one* tick boundary is actually
   measurable. §11.2's "the colour clip is retimed 3.4 % differently within the same
   video" should be **withdrawn, not replaced**.
2. **§12's linchpin argument survives and gets tighter.** Independently re-measured:
   2011 holds **45.8 ± 1.2** frames per tick at 25 fps, 2026 holds **45.2 ± 0.8** at
   29.97 fps. The frame counts agree to **1.3 %**; the resulting playback speeds differ by
   **21 %**. The published figures (46.5 vs 45.0, 3.3 % apart) understated how close the
   frame counts are.
3. **"Zero film weave" (§3) should be cut.** the owner's scepticism is correct and the
   reason is worse than he guessed: the frames the test was run on are a nearly
   featureless white leader (σ = 0.74 DN over 450,000 px), and the same estimator returns
   **55/55 exactly (0,0)** on a 2011 file. The measurement is real and means nothing.
4. **§13 (the dots) verified from raw YUV, exactly as written.** 2,048 pixels at Y=17 in
   two bit-identical 32×32 blocks at (0,0) and (960,0); everything else flat Y=16; zero
   pixels outside those blocks. Confirmed on 8 consecutive frames in v1 and in v3.
5. **§9.1 (the dirt layer floats) verified exactly, including the 3,2,2 cadence** — five
   complete cycles of period 7, unambiguous. This is the strongest single measurement in
   §8/§9/§11 and deserves to be the figure that represents them.
6. **§8.1 (the scanline layer) did not replicate on an independent re-check** and must not
   be published until it does. See §2 below.
7. **The v2 "bird-like hull marking" (§18 lead 2) is a Rorschach and should be cut or
   inverted.** An independent VLM, asked a non-leading question, reads a **five-pointed
   star at "extremely high (95 %+)" confidence** on two separate images — and §30.2/§31.2
   already **REFUTED** a five-pointed star by measurement. Three observers, three
   incompatible readings, from the same pixels.

---

## 1. Methodology note the coordinator should propagate

**Running `gemini` from inside `/home/user/new-skinny-bob` contaminates its answers.**
The CLI's IDE companion injects the repo into its workspace via
`GEMINI_CLI_IDE_WORKSPACE_PATH`, and `--skip-trust` / `cd` do not prevent it. Caught
red-handed twice: on a dots figure gemini volunteered *"diagnostic evidence proving a
codec-side YouTube AV1 encoder artifact rather than an authorial watermark"*, and on a
hull frame it opened *"Based on a factual analysis of the image and the surrounding
workspace documentation… corresponds to a frame from Video 2, Case 11 'Tin bird primer'"*
and cited *"the codebase's visual audits."* That is our own conclusion being read back to
us as if independent.

Clean-room recipe for any second-opinion use:

```
mkdir -p /tmp/vq && cp <image> /tmp/vq/a.png          # neutral filename, neutral dir
cd /tmp/vq && env -u GEMINI_CLI_IDE_WORKSPACE_PATH -u GEMINI_CLI_IDE_SERVER_PORT \
  -u GEMINI_CLI_IDE_AUTH_TOKEN GEMINI_CLI_TRUST_WORKSPACE=true \
  gemini --skip-trust -p "<non-leading question> @a.png"
```

Verify cleanliness by asking gemini to list the files it can see. The recipe circulated in
the main session (run from the repo directory) is fine for transcribing a title card, but
it is **not** valid for adjudicating a contested visual claim.

---

## 2. Per-claim triage — §8 (video 3)

| # | Claim | Verdict | Recommendation |
|---|---|---|---|
| 8.1 | Output-frame-locked scanline layer, period 5.38–5.40 px, SNR to 130×, phase locked ±0.1 px, 5–10× weaker in segment B | **UNSETTLED — did not replicate here** | **HOLD.** My independent re-run (y 300–800, x 700–1300, row-mean after 25-px vertical detrend, Hann-windowed rFFT) finds the dominant peak drifting between **5.95, 6.76 and 7.14 px** across three segment-A frames — never 5.4 — and segment-B frames giving **SNR up to 43× with amplitude 0.95 DN, higher than segment A's 0.22–0.56 DN**. Neither the period nor the A-vs-B contrast reproduced. Most likely a window mismatch, not a refutation, but it cannot be published until it is re-derived with the source report's exact ROI and frame list. Separately: §17's own banding agent puts the AV1 static block comb at **≤0.5 LSB in all seven files**, i.e. the same amplitude band as this signal — a confound FINDINGS never states. |
| 8.2 | Film-gate border is a rendered matte: 46 px feathered ramp, three-level fill 27–30 (σ 0.19), corners stable to \|Δ\|≤2 over 200 frames, "zero weave ≤0.25 px vs 1–5 px typical at 1080p for real 8 mm" | **KEEP the measurements, CUT the comparison** | The measured numbers check out against the report. But the **"1–5 px typical"** baseline is an **unsourced assertion**, and the sibling video-2 report asserts a *different* uncited baseline — **"±0.3–1 px"** — for the same physical comparison, 3–5× smaller. FINDINGS quotes only the larger one. Publish the measurement ("the matte edge does not move"), delete the invented benchmark. Also: FINDINGS cites one of four measured edges (46 px) without noting the 33–48 px spread. |
| 8.3 | Fixed hard-edged rectangle at the same ~15 px window in four scenes across both claimed tapes, 38 source-minutes apart | **KEEP** | Genuinely non-obvious and internally consistent (the catalog span is 38:14). A raster-locked element present across two supposedly different tapes is a real composite tell. Pairs with §31.3. |
| 8.4 | Timecode ticks every 45.000 frames = exactly 2/3 playback; image layer duplicates one frame in 12 | **KEEP — now independently confirmed** | I measure **45.000 exactly** over ten consecutive ticks in Case 28 (see §4). This is the cleanest tick measurement in the whole corpus and should be the figure. |
| 8.5 | Zero film dirt, hairs, scratches, splices; zero grain; high-pass RMS 0.1–0.65 | **COMPRESS to one line** | Correct, but it is an *absence*, and FINDINGS' own caveat concedes YouTube compression could have eaten grain. §17 goes further: all seven files sit at the AV1 reconstruction floor, so grain is **indeterminate by construction in both eras**. One sentence, in the "shared absences" bucket, not a numbered finding. |
| 8.6 | Shadow direction and penumbra width consistent across independent objects | **COMPRESS** | The penumbra-width measurement is real work; "shadows point the same way" is what any viewer sees. State as one line under "things that cut against naive AI-slop readings". |
| 8.7 | Bright specks track the scene for 30+ frames with coherent mutual motion | **KEEP** | Non-obvious, and it is one of the few positive results pointing at photographed material. |
| 8.8 | Symbol panel holds stable stroke topology over 165 frames of camera orbit | **KEEP, with `agent_symbols.md`'s hedges attached** | The topology-stability claim survives (IoU 0.52–0.74 across four disjoint windows, 42 % of ink common to all four). What does **not** survive is any script identification. `agent_symbols.md` refutes Devanagari and retracts the `2Ц` reading; a clean-room VLM asked a non-leading question instead volunteers **Georgian Mkhedruli** ("near-exact resemblance to ლ… რ… ქ"), with Latin monogram and Tengwar as alternates. Three passes, three different scripts — which is itself the result: at ~30 resolution elements across, the mark supports *form* but not *identity*. Present it that way. |
| 8.9 | Case 18: 87 of 640 source-seconds in 19 fragments; Case 28: 13 of 32 in 3; fragment durations close "within 6 frames out of 3244" | **KEEP the fragment accounting, FIX the closure figure** | The two coverage figures are exact. The "within 6 frames" is **not supported by the source report's own arithmetic**, which computes 3915 − 670 = 3245 predicted against 3244 measured — a **1-frame** gap. The report's body and its own summary disagree; FINDINGS inherited the summary. Publish 1 frame in 3244, or drop the number. |
| 8.x | "Four-digit hand" is real; the black nails on the human hand are inter-digit shadows; "flashlight vs fully-lit" and "lamp that lights nothing" do not survive measurement | **KEEP, and note it was later reversed in part** | A clean-room VLM asked to count digits with no expected answer supplied lands on **"4 clearly defined digits"** on every pass, on two different images — solid corroboration. Its count of the *comparison* hand is unstable (5 in one pass, 6 in another), which is exactly the resolution limit §9.6 quantifies. Note §21 → §28 reversed the morphometric verdict around this material; do not present §8's version without the §28 amendment. |

---

## 3. Per-claim triage — §9 (video 2) and §11 (video 1)

| # | Claim | Verdict | Recommendation |
|---|---|---|---|
| 9.1 | The dirt layer is a separate overlay: at f2422→2423 picture **and** timecode hard-cut to black in one frame, dirt keeps playing for 36 more frames, on a strict 3,2,2 cadence (period 7 ≈ 12.84 patterns/s); between plates it jumps 4–63 px while the image moves ≤0.11 px | **KEEP — verified exactly, and lead with it** | Re-measured from the frames. f2422 mean luma 63.4 → f2423 mean **0.04**, one frame. f2423–f2458 (**36 frames**) are black yet carry 2,085–13,798 pixels above value 2, peaking at 80. f2459 onward: no pixel above 2. Plate lengths, thresholding a new plate at max\|Δ\|>40: **1, 3,2,2, 3,2,2, 3,2,2, 3,2,2, 3,2,2** — five complete period-7 cycles. Figure: `figs/technical/fig_dirt_layer.png`. Keep FINDINGS' own bounded-inference hedge verbatim: this proves the *look* is manufactured, not the *content*. |
| 9.2 | Zero gate weave: aperture-boundary pixels σ = exactly 0.000 over 101 frames; outer fill flat 12.00/13.00 | **COMPRESS, and move to §12's "same in both eras" bucket** | True, but the identical result holds in the 2011 files (`agent_compare` Axis 6: matte edge sd 0.0144–0.0223 px in *both* eras). A locked gate with the picture floating inside it is the inverse of projector physics **in both eras** — that is an era-shared absence, not a 2026 finding. Presenting it per-video three times (§3, §8.2, §9.2, §11.5) inflates one observation into four. |
| 9.3 | Period-12 near-duplicates running unbroken through shot cuts ⇒ one retime on the assembled timeline; ≈27.5 unique fps in a 29.97 container; present in all uploaded formats so it is in the master | **KEEP** | Arithmetic checks: 29.97 × 11/12 = 27.4725, so both "≈27.5" (§9.3) and "≈27.47" (§11.1) are the same number. **Fix a terminology conflict:** §11.1 calls these frames "bit-identical", the v2 and v3 reports explicitly call the same phenomenon "near-identical, *not* bit-identical" (mad 0.02–0.07). Pick one — "near-identical" is the defensible word — because "bit-identical" is a claim a reader can check and lose faith over. |
| 9.4 | 45 frames/tick across seven of eight fragments; **exception:** Case 11 "Tin bird primer" non-constant, 33 → 46, drifting within one fragment | **KEEP the 45; DOWNGRADE the Case 11 exception** | The 45 is confirmed (Triage: 180 frames / 4 ticks = **45.00 exactly**). Case 11 is the *worst-conditioned* fragment in the corpus for this measurement: glyph contrast median 29.7 DN against 67–108 DN elsewhere, and **29 of 200 frames flare-blown**. My own detector returns garbage there for the same reason. "Drifting 33–46" is at least as likely to be the estimator failing as the source varying. State it as unmeasurable, not as an anomaly. |
| 9.5 | Catalog internally bounded but spliced: no timecode outside any claimed range, all case numbers match, 4 of 8 ranges contain hidden internal splices, source second 00:03:15 missing with no visible cut | **KEEP** | Non-obvious and checkable. The "missing endpoints are not 2026-specific" correction is now confirmed from primary source in the 2011 era too — see §7 below. |
| 9.6 | Effective resolution is a few hundred pixels (spectral cutoff 8–13 % of Nyquist), so fingers, nails, eyelids, seams are unresolvable *in principle* | **KEEP, and promote it** | This is the single most useful thing in §9 for a public audience, because it pre-empts half the comment section. It is also the reason §11.8, §8.8 and the hull-marking lead all end in "undetermined". Consider making it a standalone early section rather than a bullet buried in §9. |
| 9.7 | Points toward optical coherence: eye speculars behave correctly, patches track substrates, no looping idle animation, no melting or wrong shadows | **KEEP** | The "no idle loop" test (self-similarity decays monotonically) is a real falsification of a specific community claim and should be named as such. |
| 9.8 | Walkabout figure approaches 20–35 % but no gait resolves — reads as a glide | **KEEP, fix the citation** | This bullet is **not in** `agent_video2_Oqw96jCOP7A.md`, which says flatly the figure "stands in one place throughout". FINDINGS §9.8 already prints the *corrected* version, silently sourced to `agent_scenes_content.md` via §20. Fix the attribution or the next person to check will think §9 was fabricated. |
| 9.x | "Sources are called *tapes* but the applied damage is *film* dirt, scratches and a film gate" | **KEEP — one line, high value** | Cheap, checkable, and it lands. Same class as §8's "tapes vs 8mm" nomenclature tension; merge the two into one sentence. |
| 11.1 | Same 12-frame duplicate beat as v2 and v3 → one pipeline | **KEEP** | See 9.3 on the "bit-identical" wording. |
| 11.2 | 46.0 frames/tick in the b/w fragments (0.6515×) and **44.5 in the colour Mk.5 fragment (0.6735×)** — the colour clip retimed 3.4 % differently within the same video | **WRONG — WITHDRAW** | See §4. Not "replace with 46.0" either; §30.4's 46.0 is equally unsupported. |
| 11.3 | b/w picture advances in bursts of ~16 ± 1 distinct images per burned-in second (⇒ 16 fps cine source); colour clip moves every output frame (~40.8 distinct images/source-second) | **KEEP the b/w burst count; RECOMPUTE the colour number** | The 40.8 was derived as 44.5 × 11/12 and therefore inherits the retracted 44.5. At the measured 45.5 it becomes 41.7. Also restore the source report's own disclaimer — *"I state the arithmetic, not a conclusion"* — which FINDINGS softened into "consistent with a historically standard amateur rate". |
| 11.4 | Damage-layer ordering differs from v2: dirt amplitude preserved across hold groups, marks live 1.8–2.0 frames against a ~2.9-frame content hold ⇒ dirt applied *before* retiming | **KEEP** | Numbers match the report (1.83, 2.03, 2.875). Two different orderings of the same damage pass across two "tapes" is a real and non-obvious composite tell. |
| 11.5 | The v1 border is *not* frozen: drifts sub-pixel (σ 0.29–0.55 px) and the timecode moves **with** the border while the picture moves independently inside it | **CONTESTED — do not publish as written** | Direct, unacknowledged contradiction with `agent_compare_2011_vs_2026.md` Axis 6, which tracks the matte edge of *the same file* and gets **sd 0.0219 px, p2p 0.147**, concluding "the matte is locked". That is 13–25× smaller. Neither report specifies matched frame windows, so it cannot be adjudicated from the reports. Weight favours Axis 6: the v1 report's **own stated estimator noise is ~0.2–0.3 px**, i.e. comparable to its 0.29–0.55 px "effect" — it is close to measuring its own noise. FINDINGS compressed that admission into "(Low power: amplitudes < 1 px)", which reads far weaker than it is. Publish only the *qualitative* part (timecode and border are in the same layer, picture is in another) if it can be shown by inspection; drop the σ. |
| 11.6 | Mk.4 pace-lap range claims end 01:11:21, last timecode on screen is 01:11:20 — but the merged ledger found the same loose endpoint convention in both eras | **KEEP, now confirmed from primary source** | See §7: I measured the same shortfall directly in 2011 RsQCX. |
| 11.7 | "New find — a ghost image behind title card A, now confirmed": averaging f40–300 and median-suppressing the text reveals a dark lenticular disc silhouette, "the same craft profile as the tin bird shots"; "a deliberate hidden underlay" | **OVERSTATED — COMPRESS to one line, drop "hidden" and "deliberate"** | the owner is nearly right. Clean-room VLM, asked openly what is visible in the **upper portion** of five raw unmodified title-card frames (f60/150/250/400/450): **"nothing distinct", 5 times out of 5.** Point it at the region behind the text and it reports *"a distinguishable, faint, dark curved shape… visible within the illuminated central region directly behind the text."* A single frame with nothing but a gamma bump gives *"a subtle, dark, smooth curved diagonal shape/shadow sweeping through the bright central area."* Only the full ~260-frame stack yields a crisp silhouette — described unprompted, across two independent phrasings, as *"a dome-like upper section and a curved lower section separated by a horizontal gap"*, which does corroborate the shape read. A 24-frame partial stack (`v1_group0_n24.png`) shows **nothing but the two tile-corner blocks**. So: it is not invisible-and-hidden, and it is not obvious-to-anyone. It is a faint underlay you see the moment you raise the brightness. That is worth **one sentence** — "the opening cards are composited over a dimly visible craft plate, visible in a single frame if you lift the gamma" — not a numbered discovery, and definitely not "deliberate". Also: the source report describes it as *"very faint… visible only under strong local-contrast stretch"*; the method (f40–300 average, median suppression) and the confident silhouette description appear nowhere in the cited report. **And `analysis/ghost-disc/v1_f560_view.png` is not the disc card at all** — it is the edit-disclosure card ("Tape 02 edited fragments: Case 11/Tin bird unauth…"). Do not publish it captioned as ghost-disc material. |
| 11.8 | The "five fingers at 1:24" comment is unadjudicable, and the timecode glyphs sitting across the fist plausibly manufacture the extra "fingers" | **KEEP — this is a model paragraph** | Refuses to adjudicate, explains *why* it cannot be adjudicated, and offers a specific alternative mechanism. Keep the ~250 px / ~15 px PSF numbers; they are what make it convincing. |
| 11.9 | Russian captions are clipped at the film-frame aperture ⇒ composited inside the film layer, not over the 16:9 canvas | **KEEP** | Cheap, non-obvious, and it establishes layer order without any modelling. |
| 11.10 | Two morphologically near-identical sweeping-band artifacts 44 s apart in different shots (same start row ≈244, ~5 rows/frame, profile r = 0.84) — recurring artifact or reused effect element, undetermined | **COMPRESS** | Numbers match (r = 0.836, gap 1314 frames = 43.8 s). Honest "undetermined" ending. One line. |

---

## 4. The frames-per-tick reconciliation (§11.2 = 44.5 vs §30.4 = 46.0)

### 4.1 Method

The burned-in overlay counts whole seconds of source time, so the number of video frames
each value is held for is the retime ratio, read directly off the picture. I isolated the
**seconds-units glyph cell** (raster-locked to ±0.7 px per §9.2, verified stable across
fragments), high-pass filtered it, and detected tick boundaries as peaks in
`1 − NCC(mean of the 8 frames before, mean of the 8 frames from here on)`. Averaging 8
frames either side is what makes the low-contrast fragments measurable at all — in v1's
colour clip the glyph sits only ~8 DN above its local background and a frame-by-frame
segmenter shreds into 1–3 frame runs and returns noise. Each boundary was then refined to
the exact first frame on which the new glyph beats the old one.

**Every result was then verified by rendering the run-averaged timecode strip for each
run and reading the digit sequence.** If the seconds step by exactly one per run with no
skips, no boundary was missed and `span / n_intervals` is the cadence. That check is what
turns this from an estimate into a count. Scripts: `analysis/timecode-ticks/tickedge.py`,
`refine.py`, `readdigits.py`.

### 4.2 What is actually measurable in the colour Mk.5 segment

Seven tick boundaries; the segment reads `T6-02/31 00:57:56 → 00:58:03`.

| Boundary | Frame | Status |
|---|---|---|
| onset of `:57` | ~2617 | inside a flare — bracketed only |
| onset of `:58` | 2660 | measurable (marginal, NCC 0.80) |
| onset of `:59` | **2706** | clean, NCC 0.947 over a 45-frame run |
| onset of `:00` | **2751** | clean, NCC 0.761 over a 34-frame visible run |
| onset of `:01` | somewhere in **2782–2797** | **unmeasurable** |
| onset of `:02` | somewhere in **2846–2850** | **unmeasurable** |
| onset of `:03` | ~2884 | inside a flare — bracketed only |

I rendered every frame of f2782–2801 and f2836–2855 at high gain with three different
enhancements. In f2782–2796 and f2836–2845 the timecode is **not faint, it is gone** — a
bright flare sweeps the lower-left corner and blows the white glyphs into a white field.
No processing recovers them.

So the segment yields **exactly one fully measurable tick interval: 2706 → 2751 = 45
frames.**

### 4.3 Where 44.5 and 46.0 each came from

- **44.5 (§11.2)** = total span ÷ assumed tick count. My raw step detector reproduces it
  exactly: first boundary 2617, last 2884, 267 frames, 6 intervals, 267/6 = **44.50**. But
  both endpoints are flare-bracketed, so the span is uncertain by ±15 frames at each end —
  ±5 frames per tick.
- **46.0 (§30.4)** = two clean boundaries (2705, 2751 — one frame off mine) extrapolated
  into an arithmetic grid `2613/2659/2705/2751/2797/2843/2889`. That grid is a *model*
  fitted to one interval, not seven measurements. Its predicted `:01` onset (2797) sits at
  the very edge of my bracket and its predicted `:02` onset (2843) sits outside it.

**Both are one measurement stretched over unmeasurable ground.** §30.4 was right to flag
§11.2 and right that two boundaries sit behind flares; it was wrong to propose 46.0 as the
replacement.

### 4.4 What the b/w fragments say — the actual answer

v1 Case 12 gives twelve consecutive seconds with **no skips**, verified by reading the
strip: `01:10:56, :57, :58, :59, 01:11:00, :01, :02, :03, :04, :05, :06, :07`.

Onsets: 1354, 1400, 1446, 1495, 1539, 1585, 1630, 1676, 1720, 1765, 1810, 1855.
Gaps: 46, 46, 49, 44, 46, 45, 46, 44, 45, 45, 45.
**Span 501 frames / 11 ticks = 45.55 frames per tick, median 45, sd 1.29.**

The `49` and one `44` straddle a flare; the flare-free sub-run f1585→f1855 is
45, 46, 44, 45, 45, 45 = **270/6 = 45.00 exactly**.

### 4.5 Full recomputed table

**2026 — 29.97 fps**

| Fragment | Source seconds read | Onsets | Span / ticks | Frames/tick | Ratio |
|---|---|---|---|---|---|
| v1 Case 12 (b/w) | 01:10:56 → 01:11:07, 12 consecutive | 1354 … 1855 | 501 / 11 | **45.55** | 0.658× |
| v1 Case 31 (colour Mk.5) | only one interval measurable | 2706 → 2751 | 45 / 1 | **45.0** | 0.666× |
| v2 Case 21 "Triage" | 00:15:02 → :05, 5 consecutive | 1220, 1266, 1311, 1356, 1400 | 180 / 4 | **45.00** | 0.666× |
| v3 Case 28 | 02:23:45 → :54, 10 consecutive | 3150 … 3600 | 450 / 10 | **45.00** | 0.666× |
| **pooled** | | | 1176 / 26 | **45.23** | **0.663×** |

**2011 — 25 fps**

| Fragment | Source seconds read | Onsets | Span / ticks | Frames/tick | Ratio |
|---|---|---|---|---|---|
| RsQCX Case 25 | 00:27:41 → :44 | 1131, 1176, 1222, 1267 | 136 / 3 | **45.33** | 0.552× |
| RsQCX Case 26 | 00:55:08 → :11 | 1298, 1344, 1389, 1435, 1481 | 183 / 4 | **45.75** | 0.546× |
| ZB788 | 00:08:43 → :47 | 186, 233, 277, 325, 371 | 185 / 4 | **46.25** | 0.541× |
| **pooled** | | | 504 / 11 | **45.82** | **0.546×** |

Bonus: the `31`-frame "gap" at RsQCX f1267→1298 that looked like a cadence anomaly is a
**splice** — the timecode jumps `00:27:44 → 00:55:08` there, the Case 25 → Case 26
fragment boundary. Reading the digits caught it; a gap-length statistic would not have.

### 4.6 Consequences for the record

1. **Withdraw §11.2's differential-retime claim.** Do not substitute 46.0.
2. **Simplify §9's cross-video summary.** "The tick cadence is per-video — 46.0/44.5 (v1
   b/w/colour), 45.0 (v2, v3)" becomes: **45 frames per tick in all three 2026 videos, in
   every fragment measurable to the frame.** This makes §12 easier to state, not harder.
3. **Recompute §11.3's 40.8** (it was 44.5 × 11/12) to 41.7, or drop it.
4. **On the published ratios.** My 2011 figure is 0.546 ± 0.013; the report's 0.538 ± 0.007
   sits inside that, so they agree. But three significant figures overstate what the data
   support — the 2011 per-tick spread is 44–48 frames. For a public post the defensible
   statement is **"about 0.54× in 2011, about 0.67× in 2026"**, with 0.538/0.666 available
   as the figures of record. This preserves the owner's point completely: the *difference* is
   21 % and utterly secure. What is not secure is the third digit.
5. **The argument is stronger than the record says.** At 46.5 vs 45.0 the frame counts were
   3.3 % apart. Measured properly they are **1.3 %** apart — 45.8 vs 45.2 — while the
   speeds are 21 % apart. The coincidence being pointed at is tighter than advertised.

Figure: `figs/technical/fig_timecode_ticks.png`. An independent VLM transcribed every
timecode in it correctly and answered "yes, the argument is clear" to whether the figure
stands alone.

---

## 5. Film-weave verdict (§3) — CUT IT

**Claim.** Phase correlation of frames 950–1005 of video 1 returns exactly (0,0) for all
55 frames — "no gate jitter or projector weave whatsoever".

**Re-run.** `analysis/timecode-ticks/weave.py`. Five tests.

**T1 — what those frames contain.** f950–1005 is the bright white leader run. Inside the
leader field (y 300–800, x 500–1400) the standard deviation is **0.74 DN over 450,000
pixels** and mean gradient magnitude is **0.019**. There is essentially no image structure
there to align. A median of **67 %** of pixels are bit-identical to the previous frame (the
flat matte plus the flat leader). No pair is a whole-frame duplicate, so duplication is not
the explanation — **featurelessness is**.

**T2 — the original measurement.** Integer-argmax phase correlation reproduces it
approximately: **54 of 55** pairs return exactly (0,0), not 55.

**T3 — sub-pixel.** Parabolic refinement of the same peak returns garbage: sd of
**55.6 px** in dy and **29.2 px** in dx, max displacement 416 px. The correlation surface
does not have a well-formed single peak to refine. A (0,0) integer argmax on that surface
is a statement about the surface, not about the film.

**T4 — matched control, same estimator, files nobody claims are synthetic.**

| File | Era | pairs exactly (0,0) |
|---|---|---|
| v1 f950–1005 | 2026 | 54 / 55 |
| v1 f1600–1655 (**demonstrably moving** b/w picture) | 2026 | 50 / 55 |
| 2011 RsQCX f1131–1186 | 2011 | 42 / 55 |
| 2011 ZB788 f186–241 | 2011 | 37 / 55 |
| **2011 Xju f400–455** | **2011** | **55 / 55** |

The single most "perfectly locked" file by this metric is a **2011** file. And v1's own
moving picture scores 50/55 — the estimator says (0,0) even where the image is visibly
travelling, because the static matte occupies 37–43 % of the frame and pins the peak at
zero. This is exactly what `agent_compare_2011_vs_2026.md` Axis 6 already reported, and
FINDINGS never surfaced it: *"I reproduce it, but it is not diagnostic… It cannot
distinguish locked from weaving, and the 2011 videos give the identical answer."*

**T5 — injection test.** Shift a real frame by a known amount and see if the estimator
recovers it:

| injected dx | sub-pixel estimate | integer estimate |
|---|---|---|
| +0.10 px | +0.041 (under by 2.4×) | 0 |
| +0.25 px | +0.111 (under by 2.3×) | 0 |
| +0.50 px | +0.499 | 0 |
| +1.00 px | +1.000 | 1 |
| +2.00 px | +2.000 | 2 |

So the estimator *can* see displacement — but the **integer** variant returns 0 for
anything below 0.5 px by construction, and the sub-pixel variant is biased ~2.4× toward
zero for small shifts. An integer estimator returning (0,0) is compatible with any weave
under half a pixel, which is the entire range of interest.

**Verdict. This is an artifact of the estimator and the region, and I want to say that
loudly.** Three independent failure modes stack: the region has nothing to correlate, the
static matte dominates whatever is left, and the integer estimator quantises everything
under half a pixel to zero. A 2011 file scores a *perfect* 55/55 on the same test. The
number is real; it discriminates nothing.

**Recommendation: delete §3.** The defensible version of the underlying observation already
exists elsewhere and belongs in §12's "same in both eras" column: sub-pixel matte-edge
tracking gives sd 0.0144–0.0223 px in **both** eras, with the picture floating *inside* a
locked gate — the inverse of real projector physics, in both. That is one sentence, it is
properly controlled, and it is an era-shared absence rather than a 2026 tell. Everything
in §3, §8.2's weave clause and §9.2 collapses into it.

---

## 6. §13 — the consolidated passage (drop-in)

> ### The "hidden dots" in the black frames
>
> A community site had flagged barely-visible `#020202` dots in the black frames of the
> 2011 videos as a possible watermark or toolchain fingerprint. The same dots are in the
> 2026 videos, at the same coordinates — which briefly looked like a direct file-lineage
> link between the two eras.
>
> They are not. They are YouTube's.
>
> Decode a fully black frame of 2026 video 1 straight out of YouTube's AV1 stream and the
> luma plane is flat at value 16 — **except for exactly 2,048 pixels at value 17**. Those
> 2,048 pixels are two solid 32×32 blocks, one at pixel (0, 0) and one at (960, 0). Not one
> pixel of the mark falls anywhere else in the frame. YouTube encodes 1080p AV1 in two tile
> columns of 960 pixels each, and these are the first coding block of each column.
>
> Three things settle it:
>
> - **The two blocks are bit-identical.** The right block is the left block translated by
>   exactly +960 pixels — not mirrored. An earlier reading of these as the two corners of a
>   rounded "window" ghost, mirror-symmetric about x ≈ 505, was wrong: it is a translation,
>   and it follows the encoder's tile grid rather than anything in the picture.
> - **The same two blocks sit at the same coordinates in the 2011 files.** Both eras are
>   modern YouTube AV1 encodes — the 2011 AV1 streams were generated by YouTube years after
>   those videos were uploaded. Every one of the cross-era "constellation matches" that
>   looked significant — 88 shared positions between video 2 and the 2011 Xju upload,
>   video 3's 118 positions as a subset of the Xju leader, the 112 shared between videos 2
>   and 3 — lies inside these two blocks.
> - **It has been confirmed from a second, completely independent codec.** An outside
>   analyst published their own download of the same upload, taken through AVC rather than
>   AV1. Comparing their frames to ours: the maximum per-pixel difference anywhere is **1**,
>   the mean is **0.001**, our frames contain values {0, 1} and theirs contain only {0}. On
>   all sixteen strictly-black frames our decode has those two 32×32 blocks present and
>   theirs has them absent, and on fifteen of the sixteen **the entire difference between
>   the two people's frames is exactly those 2,048 pixels**. Two people, two codecs, one
>   public upload, and the delta is precisely the artifact. Nothing about it belongs to
>   whoever made the video.
>
> Everything else in the black frames is the level-1-to-4 tail of title cards that are
> plainly visible a few seconds later — video 1's "Source anonymity is maintained. /
> Failsafe contract is preserved." card, and the 2011 Xju "In response to posts about the
> documentary…" card. Fade residue, not hidden content.
>
> **Provenance information content: zero.** The watermark lead is closed. The lasting
> lesson is methodological: pixel-level watermark hunting on YouTube re-encodes has to
> control for codec behaviour first, and at 1080p that means masking the 32×32 blocks at
> (0, 0) and (960, 0) before you compare black frames at all. We spent real effort on a
> "cross-era pixel match" that was the encoder both times.

Notes for the rewrite:
- Everything above is re-verified from raw YUV: v1 f2991–2998, all eight frames identical
  in behaviour, and v3 f4394. `analysis/timecode-ticks/verify_tile_corners.py`.
- **Cut the "Investigation trail, kept for methodology" block** from the public version.
  It presents the superseded mirror-symmetry reading and the "an imitator could not have
  seen it to copy it" argument at length before retracting them. Keep it in the archive;
  in a public post it reads as burying the answer.
- Figure: `figs/technical/fig_tile_corners.png`. **All four existing dots figures fail a
  legibility check** — asked whether a reader at 900 px could tell what each showed without
  a caption, an independent VLM answered "No" to `dots_corners_x48.png`,
  `dots_maps_4up.png`, `dots_scatter_6up.png` and gave no usable read on
  `corner_icons_zoom.png` either. Do not reuse them. (Usefully, asked what the corner
  structure looked like with no hypothesis supplied, the same VLM volunteered
  *"a compression, quantization, or encoding artifact… blocky, stair-step pixel
  contours"* — independent corroboration of the resolution.)

---

## 7. §17 and §18/18b

**§17 (grain/damage and banding/colour).** These are the two most rigorous *negative*
reports in the corpus and §17 is where they go to be forgotten. Three of the four things
in it are load-bearing for other sections and should be moved to where they do work:

| §17 item | Where it belongs |
|---|---|
| **Noise spectra are indeterminate by construction** — all seven files sit at the AV1 reconstruction floor, per-pixel noise 0.09–0.40 DN, slope ≈ −2.5 in both eras because the encoder sets the roll-off | **Move to the front, as a limits-of-evidence preamble.** It is the single best inoculation against the comment section and it retires §8.5, half of §9.6 and every "the grain proves it" argument in one paragraph. |
| **Step-printing is an era discriminator, third independent method** — 2011 live action has 33–45 % single-frame freezes with textbook period-2 autocorrelation (lag-1 −0.79/−0.45); 2026 has 1.3–2.1 % and autocorrelation ≈ 0 | **Move into §12.** This is the second-strongest positive discriminator in the document and it is currently filed under "final two agent reports". |
| **Tint geometry** — 2026 two-axis orange/teal (a_v/a_u −0.96/−1.32, R²v 0.72–0.79); all 2011 single-axis blue/yellow with V pinned neutral (−0.004…−0.17, R²v 0.005–0.104) | **Move into §12**, where FINDINGS already cites it without the numbers. |
| **Banding absent in both eras**; the community's "CRT banding" is caption line pitch (25.6 px at 480p, 38.4 at 1080p) plus the AV1 block comb; "tape-06 kept its colour" falsified (steepest tint of all seven, R²u 0.968) | **Keep as a short "claims that died" list.** Note the agent's own caveat that the 2011 files carry more transcode generations, so absent-vs-absent cannot separate never-there from destroyed. The *claims* die; the pipeline question stays indeterminate. |

So: **the owner is right that §17 fits earlier.** But it should not move as a block — it should
be dismembered, with its limits material opening the document and its two positive
discriminators folded into §12. What remains is a paragraph.

**§18 (coarse rewatch).** Mostly a scene map, which is useful scaffolding for a reader and
carries almost no evidentiary weight. Compress hard. Two specific fixes:

- **Cut or invert lead 2, the "bird-like hull marking".** Asked a non-leading question
  with the word "bird" never used, a clean-room VLM read the marking on
  `v2_hull_emblem_enh.png` as *"a five-pointed star (such as a stylized military or state
  insignia)… Confidence Level: Extremely High (90 %–95 %)"*, and on `v2_f495_full.png` as
  *"clearly resolves into a five-pointed star… Confidence: Extremely High (95 %+)…
  consistent with military or state insignia (such as a Soviet Red Star)"*. Meanwhile
  §30.2 and §31.2 **refuted** a five-pointed star by measurement. Three observers, three
  incompatible readings, one set of pixels. That is not a lead, it is a demonstration that
  the marking does not resolve — and said that way it is *more* useful than "bird-like",
  because it shows the resolution limit biting on a specific object a reader can look at.
  §18 already concedes the frames resolve no aircraft-specific feature; finish the thought.
- **The "ghost disc plainly behind BOTH cards in lifted thumbs" parenthesis is the right
  register** and §11.7 should be brought down to match it, not the other way round.

**§18b (the naming rule).** **KEEP, promote, and it is now on firmer ground than when it
was written.** The rule: in 2011 a case number has exactly one name, repeated verbatim
across all its fragments (4 of 4 multi-fragment cases obey); in 2026, 3 of 4 break it
(C11 = `Tin bird unauth` *and* `Tin bird primer`; C12 = `Mk.4 taxi` *and* `Mk.4 pace lap`;
C25 = `Bob's walkabout` *and* `Slim Tim`), and both cases 2026 shares with 2011 are
renamed. Score: 2011 took 0 of 4 opportunities to rename; 2026 took 3 of 4 within-era and
2 of 2 cross-era.

I verified the premise from primary source. The title card at f501–575 of
`videos/2011/RsQCXN4o4Ps.mkv` reads, legibly at native resolution and confirmed by stacking
f510–569:

```
Tape 05 edited fragments:
Case 25/skinny Bob 00:08:42 - 00:08:50
Case 25/skinny Bob 00:27:36 - 00:27:45
Case 26/How to drive 00:55:07 - 00:55:12
```

So `Case NN/name` is **ivan0135's own 2011 on-screen convention**, not later fan
cataloguing — and Case 25 carries the identical name across both its fragments, right
there on the card, with his own lowercase "s". §18b is therefore comparing two documented
in-corpus authoring conventions rather than measuring 2026 against community practice.
Nothing in §8/§9/§11/§18 relies on the old "names are fan-applied" assumption — the
sections talk about case *numbers* and burned-in timecode — but `docs/SKINNY_BOB_DOSSIER.md`
did, and has been corrected.

Two further things fall out of that card, both cheap and both worth using:

1. **The 2026 timecode ranges I measured land inside the 2011 ranges' structure exactly.**
   Case 25's second fragment is claimed 00:27:36–00:27:45 and I read `00:27:41 → :44` on
   screen; Case 26 is claimed 00:55:07–00:55:12 and I read `00:55:08 → :11`. The catalog is
   internally clean in 2011 too.
2. **§11.6's "endpoint shortfall" is now confirmed in the 2011 era by direct
   measurement.** Case 26 claims an end of 00:55:12. The last tick onset is f1481 (`:11`),
   the picture goes to black by ~f1487, and the file ends at f1500 — so `:12` never gets to
   tick, cut ~40 frames early. That is the same house convention §11.6 was originally
   charged as a 2026 anomaly, seen directly rather than inferred from a merged ledger.
   Keep the retraction and cite this.

---

## 8. The KISS speed explainer (reader-facing, drop-in)

> ### The one measurement that does the most work
>
> Every one of these videos, 2011 and 2026, carries a timecode burned into the bottom-left
> corner — something like `00:15:02`. It is meant to be the reading from the original tape,
> and it counts up in whole seconds.
>
> That gives you a free stopwatch. Step through the video frame by frame and count how many
> frames go by before the timecode ticks over to the next second. If one second of the
> original takes more than one second of video to play out, the footage has been slowed
> down, and the frame count tells you by exactly how much.
>
> **In the 2026 videos, every timecode second is held for 45 frames.** Not approximately —
> I read ten consecutive seconds in one clip and got 45, 45, 45, 45, 44, 46, 45, 45, 45, 45.
> Those videos run at 29.97 frames per second, so 45 frames is 1.50 seconds of screen time
> for 1 second of original. They play at about **0.67× speed**.
>
> **In the 2011 videos, every timecode second is held for about 46 frames.** Four
> consecutive seconds in one of them: 47, 44, 48, 46. But 2011 was PAL — 25 frames per
> second. So 46 frames is 1.85 seconds of screen time for 1 second of original. They play at
> about **0.54× speed**.
>
> Here is the part that matters.
>
> The two sets of videos hold **nearly the same number of frames** per timecode second —
> about 46 in 2011, about 45 in 2026, a difference of one frame in forty-five. But because
> they run at different frame rates, that near-identical frame count produces **noticeably
> different speeds**: 0.54× against 0.67×, a gap of about a fifth.
>
> If the 2026 videos had come off the same editing setup as the 2011 ones, the thing that
> would have carried across is the **speed**. That is what a slow-motion setting is: a
> ratio. Change your project from 25 to 29.97 frames per second and a 0.54× slowdown stays
> 0.54× — the software adjusts the frame count for you, silently.
>
> What actually carried across was the **frame count**. And a frame count is not something
> you inherit from a project file. It is something you *measure* — by loading the published
> video into an editor, stepping through it, and counting how long the timecode sits still.
> Somebody appears to have done exactly that, then reapplied the number they got in a
> project running at a different frame rate, without noticing that the number was never the
> point.
>
> That is a fingerprint of working from the outside, from the published videos, rather than
> from whatever made them.
>
> It is suggestive rather than conclusive, and it is worth saying why. The same person, 15
> years later, on different software, working from a "hold it for 45 frames" note they wrote
> down at the time, would leave exactly this trace without measuring anything. That
> possibility is not excluded. But it does dispose of the argument that gets made most
> often — that the 2026 videos must be genuine because they are *the same* as the 2011 ones.
> On this measurement they are not the same. They are a copy of a number.

Notes for whoever edits this:
- It never uses the words phase correlation, NCC, cadence, conform, retime or template.
- The only figures quoted are 45, 46, 25, 29.97, 0.54 and 0.67 — all of which a reader can
  verify with a frame-stepping video player and no tools.
- **Do not** quote 0.57× or "close to ~0.55×", per the superseded fencepost note in §4.
- If a three-digit form is wanted, 0.538× / 0.666× are the figures of record; but see
  §4.6 item 4 — the data support two digits, and two digits make the same point.

---

## 9. Recommended running order

The current order was built by accretion and it buries the strongest material. Proposed
reader-facing sequence:

| # | Content | Why here |
|---|---|---|
| 1 | **What the corpus is** — seven videos, two eras, what each claims. Current §0/§4 catalog table. | A reader needs the objects before the arguments. |
| 2 | **What these files can and cannot tell you.** From §17: everything sits at the AV1 reconstruction floor; effective resolution is a few hundred pixels (§9.6) so fingers, eyelids and seams are unresolvable *in principle*; no production metadata survives in any of the seven files. | **This is the §17 relocation the owner asked for, and it is the highest-value move in the document.** Stating the resolution limit up front converts a dozen later "undetermined" verdicts from evasions into predictions, and it pre-empts the entire "but I can see five fingers" genre of reply. |
| 3 | **THE SPEED ARGUMENT.** §8 of this report verbatim, plus `fig_timecode_ticks.png`. | The single strongest thing in the investigation, requires no prior context, and a reader can check it themselves. It should be the third thing they read, not the twelfth. |
| 4 | **The rest of §12** — timecode font metrology (12–25σ), step-printing present/absent, tint geometry two-axis vs single-axis, 25 vs 29.97 native, redaction discipline. Plus the honest "same in both eras" column, into which §3, §8.2's weave clause and §9.2 all collapse. Absorb §17's step-printing and tint numbers here. | Speed is the headline; these are the four independent corroborations. Keeping them adjacent is what makes the verdict "moderate-to-high" instead of "one measurement". |
| 5 | **The composite tells** — the surviving §8/§9/§11 material, reorganised **by phenomenon rather than by video**: the damage layer floats (§9.1, with `fig_dirt_layer.png`); the damage-application order differs between the two "tapes" (§11.4); raster-locked elements that belong to the output frame, not the scene (§8.3, §31.3); the 12-frame conform running through cuts in all three videos (§9.3/§11.1); captions clipped at the film aperture (§11.9). | Three near-identical per-video sections is the worst structural problem in the current document — the same five findings are stated three times with different frame numbers. One pass per phenomenon, citing which videos show it. Cuts the length by half with no loss. |
| 6 | **The catalog** — burned-in timecodes vs stated ranges, in both eras; internal splices; the endpoint convention (§11.6, with the 2011 confirmation from §7 above); §18b's naming rule. | This is where **§18b belongs, promoted**. It is the sharpest lore-level result and it sits next to the measurements that establish the catalog is internally clean, which is what makes a *convention* break interesting. |
| 7 | **The hidden and the half-hidden** — the Cyrillic leader text (§2/§2a), the four-frame insert (§2c), the faintly visible plate behind the title cards (§11.7, compressed to one line). | Grouping these makes the "author likes hiding things" observation without any single item having to carry it. §11.7 at one line is fine here; at eight lines it is a liability. |
| 8 | **Claims that died** — the dots (§13, §6 of this report), the Chinook reflection, the five-pointed star, "tape 06 kept its colour", CRT banding, the grain-spectrum arguments, the hull marking that reads as three different things to three observers, "zero film weave". | **Put the refutations in one place and own them.** This is the section that buys credibility for everything above it, and §13 is its centrepiece: we chased a cross-era pixel match that turned out to be the encoder, twice. Say so. |
| 9 | **Open** — line 2 of the Cyrillic, the symbol panel's identity, whether the 2011 originals had grain, the finger/hand result and its reversal. | |

Two structural notes:

- **§17 does not move as a unit.** Its limits material opens the document (slot 2), its two
  positive discriminators join §12 (slot 4), and its refutations join slot 8. What is left
  of §17 is nothing, which is the correct outcome for a section titled "final two agent
  reports".
- **§8, §9 and §11 should not survive as sections at all.** They are three per-video
  teardowns that share five findings. Slot 5 replaces all three.

---

## 10. Figures delivered

All in `figs/technical/`, sized for inline Reddit display (1360 px wide, legible at 900).

| File | Content | Status |
|---|---|---|
| `fig_timecode_ticks.png` | The speed argument. Run-averaged timecode strips for four consecutive seconds of a 2011 file and six of a 2026 file, each labelled with the frames it is held for, and the arithmetic underneath. | **Verified legible.** An independent VLM transcribed all ten timecodes correctly from the image alone and confirmed the argument is clear without a caption. |
| `fig_tile_corners.png` | §13. The black frame's non-minimum pixels as a map; the luma profile along one row showing two one-code-value square pulses at columns 0–31 and 960–991; the three facts including the cross-codec confirmation. | New. Replaces four existing figures that all failed the 900-px legibility check. |
| `fig_dirt_layer.png` | §9.1. The hard cut to black at f2423; twelve of the following black frames thresholded so the dirt is unmistakable; the plate-length trace showing 3,2,2 repeating five times. | New. |

Not produced, deliberately:

- **No scanline figure (§8.1).** The claim did not replicate on independent re-check (§2).
  Producing a figure for it would have meant illustrating a number I could not reproduce.
- **No ghost-disc figure.** `analysis/ghost-disc_card.png` is fine as-is if the one-line version
  of §11.7 is kept, and gemini reads the silhouette from it unprompted and consistently.
  But at one line the claim does not need a figure. **`analysis/ghost-disc/v1_f560_view.png`
  must not be used** — it is the edit-disclosure card, not the disc card.
- **No hull-marking figure.** Publishing it would require captioning what it shows, and
  that is precisely what cannot be established (§7).

## 11. Scripts and reproduction

| Path | What it does |
|---|---|
| `analysis/timecode-ticks/band_<id>.raw` | gray8 crop of the timecode band, x 590–1209, y 895–1014, one 620×120 frame per video frame. Frame counts match `frames/<id>/` exactly (1-based PNG `f00001` = raw index 0). Generated with `ffmpeg -vf "crop=620:120:590:895,format=gray"`. |
| `analysis/timecode-ticks/tickedge.py` | Sliding-window tick-boundary detection (the working method). |
| `analysis/timecode-ticks/refine.py` | Refines each boundary to the exact onset frame; flags flare-blown boundaries. |
| `analysis/timecode-ticks/readdigits.py` | Renders the run-averaged strip per run so the digit sequence can be read and skips ruled out. **This is the step that makes the measurement a count rather than an estimate.** |
| `analysis/timecode-ticks/tickper.py` | Periodogram approach. **Kept as a negative result:** short-lag NCC is inflated by the moving picture underneath regardless of the digit, which biases the period estimate upward (it returns 48.6 for a fragment that is demonstrably 45.0). Do not use it. |
| `analysis/timecode-ticks/verify_tile_corners.py` | Raw-YUV verification of the §13 tile-corner blocks across all seven files. |
| `analysis/timecode-ticks/weave.py` | The five film-weave tests of §5. |
| `analysis/timecode-ticks/fig_ticks.py`, `fig_dots.py`, `fig_dirt.py` | The three figures. |
| `analysis/timecode-ticks/ticks.py` | First attempt at cell location; superseded — its automatic rightmost-glyph search latched onto flare edges in three of five fragments. Kept as a record of the failure mode. |

## 12. Open items this pass created

1. **§8.1 needs the source report's exact ROI and frame list** before it can be published
   or dropped. Currently unsettled.
2. **§11.5 vs `agent_compare` Axis 6** (0.29–0.55 px vs 0.0219 px on the same file) is a
   live contradiction that cannot be adjudicated from the reports. It needs one
   re-measurement with matched windows, or both numbers withdrawn.
3. **The two uncited "typical real film weave" baselines** (0.3–1 px in the video-2 report,
   1–5 px in the video-3 report) should be either sourced or deleted. Both are currently
   engineering assertions presented as reference values.
4. **The colour Mk.5 clip's cadence cannot be measured beyond one tick interval** with the
   overlay alone. If it matters, the picture-layer conform (the 12-frame beat, weakly
   expressed there per §30.4) is the only remaining route.
