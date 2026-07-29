# Agent report — Signature comparison: ivan0135 (2011) vs qtecqot (2026)

*Archived verbatim from the "Compare 2011 vs 2026 signatures" subagent, 2026-07-26.
Working files referenced: `/home/user/new-skinny-bob/analysis/compare-eras/`.*

---

**Framing.** The provenance of *both* sets is undetermined here. Every prior claim was treated as a hypothesis; three of them did not survive testing. All measurements are on YouTube AV1 re-encodes, which destroys some evidence outright — flagged per axis. Working files: `/home/user/new-skinny-bob/analysis/compare-eras/`.

## Axis 1 — Timecode overlay: **DIFFERENT**

Method: averaged runs of constant timecode (n=42–248 frames), illumination high-passed, glyphs clustered into per-digit templates (56/24/151/452 instances for ZB788/RsQCX/Oqw96/l9RAh). Character advance measured from subpixel centroids of the two colons, which are exactly 3 cells apart and identical in shape (no asymmetry bias).

| | pitch (px) | digit ink W | inkW/pitch | zero-slash angle |
|---|---|---|---|---|
| ZB788PtqQvg 2011 | **43.941 ± 0.070** (n=7) | 27.36 | 0.689 | **45.5°** (R²=0.995) |
| RsQCXN4o4Ps 2011 | **43.997 ± 0.034** (n=3) | 28.33 | 0.721 | **44.9°** (R²=0.997) |
| Oqw96jCOP7A 2026 | **42.181 ± 0.120** (n=19) | 31.94 | 0.787 | **39.5°** (R²=0.973) |
| l9RAhmPHM_A 2026 | **42.562 ± 0.098** (n=58) | 31.08 | 0.778 | **38.5°** (R²=0.956) |

Within-era agreement is 0.06 px (2011) and 0.38 px; the between-era gap is 1.38–1.82 px — **12 to 25 σ**. The 2026 glyphs are ~8–13% *wider* sitting in a ~4% *narrower* advance, so this is not a size change but different tracking/design. The slash-angle test was validated against the digit '8', whose mid-bar correctly returned +0.134 slope (97.7°, horizontal).

**The Consolas claim is INDETERMINATE, not confirmed.** Consolas is not installed here and I did not obtain it. Both eras have a **slashed** zero (not dotted, not plain) — I initially misread the 2011 zero as dotted and corrected it on measurement. A slashed zero, footed '1' and crossbar-less '7' are consistent with Consolas *and* with many other faces. Since the two eras differ in pitch and slash angle, at most one could be Consolas at a given size; I can neither confirm nor refute it for either.

Layout is otherwise closely matched: same vertical band (glyph rows 938–988 vs 941–993), same `<redacted>/NN HH:MM:SS` format, black redaction bar immediately left of the timecode **with rounded corners in both eras**. Ink contrast above local background +6.4/+16.4 DN (2011) vs +16.6/+23.7 (2026) — overlapping. One substantive difference: the 2026 set leaves prefix fragments unredacted (`BL04 /22 …`, `T6-02/31 …`) that the 2011 set always concealed.

## Axis 2 — Grain: **loop SAME (both null); spectrum INDETERMINATE**

Radial power slope: 2026 median −2.58 (range −3.59…−2.41), 2011 median −2.55 (−2.71…−2.40). ACF half-width 4.29 vs 3.75 px. Band-limited amplitude peaks 0.96–1.97 vs 1.14–1.29 DN. All of it sits at the AV1 reconstruction floor (true per-pixel noise 0.09–0.40 DN), so original grain differences are erased — this test has essentially no power on these files.

**No grain loop in either era**, to ~0.003 mean-NCC sensitivity over lags 1–900 (30–36 s), with no isolated spike and no harmonic series. A temporal-Laplacian channel that cannot see static content at all gives baselines ≤|0.00004|. Neither era carries an animated grain overlay (96–99% of the high-frequency field is frozen over held graphics). **The "looped Pond5 stock overlay" hypothesis is unsupported for both sets** — though a long or non-looping stock clip cannot be excluded.

## Axis 3 — Damage layer: **SAME**

Two-hypothesis displacement test (global motion from phase correlation; 40–656 marks per video):

| | retention frame-fixed | retention image-locked |
|---|---|---|
| OpSTlDJWFFI 2026 | +0.055 | −0.030 |
| Oqw96jCOP7A 2026 | +0.130 | −0.038 |
| l9RAhmPHM_A 2026 | +0.014 | +0.005 |
| ZB788PtqQvg 2011 | +0.027 | +0.020 |
| RsQCXN4o4Ps 2011 | +0.086 | −0.046 |

Image-locked retention is zero or negative everywhere: the marks **do not move with the picture** in either era, which rules out "camera pointed at a damaged print" for both. Frame-fixed retention ≤0.13 means marks are overwhelmingly single-frame transient. Independent persistent-mark test: σ_frame > σ_image > σ_random in 8/8 usable runs. No recurrence at any interval up to 900 frames. Mark contrast differs ~2× (2011 11–33 DN vs 2026 24–66 DN) but is confounded by grading and bitrate.

## Axis 4 — Horizontal banding: **INDETERMINATE (absent in both)**

No periodic luma component with SNR>3 and amplitude >0.03 LSB in 2–120 px; in the 60–900 px CRT-beat band the maximum dynamic SNR across all seven files is **7.3**; no drift above 0.006 px/frame; no chroma banding above 0.02 LSB. The only ubiquitous periodicity is the AV1 32/16/8/4-px block comb at ≤0.5 LSB, identical in both sets.

**The "modern-camera banding" claim for 2011 does not hold up.** What is likely being seen is caption line pitch — 25.6 px in a6TLGkrfNKI, 38.4 px in Xju_CY5ZESA, amplitude 2–5 LSB and genuinely visible — plus the AV1 comb. The "videos 1–2 shot off a CRT, tape-06 not" split gets no support. Caveat: the 2011 files have more transcode generations, so "absent" cannot distinguish *never there* from *destroyed*.

## Axis 5 — Colour: **DIFFERENT**

Calibration: Xju_CY5ZESA is the codec floor (max |chroma| 3.2, frac|U−128|>2 = 0.0000). Regressing chroma on luma separates tint from colour:

- **2011 (ZB788, RsQCX, a6TL):** single-axis blue/yellow tint. a_v ≈ 0 (+0.02, +0.82, +3.44 per 100), R²v 0.005/0.104/0.434 against R²u 0.96/0.79/0.97, corr(U,V) +0.03/−0.28/−0.66.
- **2026 (Oqw96, l9RAh):** two-axis near-antisymmetric orange/teal tint. a_v/a_u = −0.96 and −1.32, corr(U,V) = −0.80, R² 0.71–0.79.

Different grading operations, not different strengths of one. **Genuine luma-independent colour exists only in the 2026 set**, in OpSTlDJWFFI, in four events totalling 12.05 s — chiefly f2571–2917 (t 85.75–97.30 s), residual sdU 3.39 / sdV 2.55 LSB after de-tinting, max |chroma| 91.8.

**"(col/s)" resolved:** the intro card lists `Case 31/Mk.5 virgin (col/s) 00:57:56 - 00:58:04`; the colour segment's burned-in timecode reads `T6-02/31 00:57:56`–`00:58:03`; and audio RMS steps ~21 dB (−33 → −13 dBFS) exactly across t=85–96. Colour **and** sound.

**The "tape-06 retained colour" claim is falsified.** a6TLGkrfNKI is monochrome with the *steepest* single-axis tint of the seven (a_u = −26.75, R²u = 0.968): at ×10 chroma gain its bright background is yellow and its dark figure blue — inverse-luma, i.e. a tint.

## Axis 6 — Film gate: **SAME on jitter; INDETERMINATE on shape**

Subpixel matte-edge tracking: sd = **0.0223 px** (ZB788, p2p 0.157), **0.0144 px** (RsQCX, p2p 0.057), **0.0219 px** (OpSTl, p2p 0.147). The matte is **locked** in both eras — no simulated projector weave. Oqw96/l9RAh indeterminate (insufficient edge contrast in the windows sampled).

**On the (0,0) phase-correlation result: I reproduce it, but it is not diagnostic.** Full-frame integer phase correlation returns (0,0) for 140/140 consecutive pairs in ZB788, Oqw96, l9RAh *and* OpSTl — the static matte occupies 37–43% of the frame and pins the peak at zero regardless of what the picture does. It cannot distinguish locked from weaving, and the 2011 videos give the identical answer.

The picture *interior* does move: frame-to-frame subpixel sd dx/dy = 0.84/0.89 (ZB788), 1.02/0.77 (RsQCX), 0.51/0.43 (Oqw96), 0.05/0.57 (OpSTl), 0.48/0.20 (l9RAh), with 7–15 px cumulative wander over 140 frames. So in **both** eras the image floats inside a locked gate — the inverse of real projector behaviour. Corner radius and aperture aspect: indeterminate, because circle fits scattered 39–229 px with within-video spread (RsQCX: 46.5/47.2/127.2/47.0) exceeding the between-era difference.

## Axis 7 — Speed: **DIFFERENT** (and the 0.55x claim is confirmed for 2011)

Per-frame template OCR of the seconds digit using each era's own averaged templates:

- **Oqw96jCOP7A:** 45,46,45,44,45,44,45,45,45 → **44.89 ± 0.57 frames/tick** at 29.97 fps → **0.666x** (= 2/3)
- **l9RAhmPHM_A:** median 45.0 → **0.666x**
- **2011:** clean staircases give 46,46 (RsQCX f1389–1485: '0' for 46 frames, then '1' for 46), 47 (RsQCX f1298–1388), 47 (ZB788 f181–274); independently confirmed by the RsQCX sub-block ladder (23-frame blocks reading 41,42,42,43,43,44 → one tick per ~46 frames) → **46.5 ± 0.6 frames/tick** at 25 fps → **0.538 ± 0.007x**

The community's ~0.55x for 2011 is **confirmed** (0.538). The 2026 set does **not** reproduce it — it runs 24% faster. The telling detail: both eras hold each timecode second for nearly the same number of *video frames* (46.5 vs 45.0, 3% apart) but at different frame rates, and that is what produces the different speed. That is the pattern you get from someone who measured the original in frames in an editor and reapplied the frame count in a 29.97 fps project, rather than inheriting a time ratio. Suggestive, not proof.

Additional cadence result: 2011 live action is **period-2 step-printed** — freeze fraction 0.33–0.45, freeze-autocorr lag1 −0.79 (ZB788) / −0.45 (RsQCX) with positive lag2 → ~12.5 unique fps in a 25 fps container. The 2026 set shows nothing of the kind (0.013–0.021, autocorr ≈ 0). Unique frames per source second: **2011 ≈ 23, 2026 ≈ 45.** (My bit-exact md5 test found 99.3% unique frames in ZB788; the duplicates are near-identical rather than bit-identical because AV1 perturbs them below 0.05 DN. Consistent.)

## Axis 8 — Encode level: **metadata INDETERMINATE; cadence DIFFERENT; framing SAME**

All seven files carry identical YouTube fingerprints: av1 Main, yuv420p, bt709 (a6TL smpte170m), `HANDLER_NAME=ISO Media file produced by Google Inc.`, `MAJOR_BRAND=dash`, `COMPATIBLE_BRANDS=iso6av01mp41`, `ENCODER=Lavf58.76.100`, Opus 48 kHz stereo. **No production metadata survives in any file**, so the Sapphire/Boris FX claim is untestable on this material.

Native rates from the `info.json` format ladders: 2011 all four **25.000 fps** (PAL); 2026 all three **30000/1001 = 29.970** (NTSC). This survives transcoding and is a real authoring difference — a same-pipeline continuation would plausibly have stayed at 25. Native resolutions: ZB788/RsQCX/Xju 1920×1080 16:9 SAR 1:1; a6TL 640×480 4:3; all 2026 1920×1080 16:9. Neither era letterboxes the container; both draw a rounded-corner picture window into a dark matte inside the 16:9 frame — same convention.

## The Cyrillic lead

**Confirmed and localised, independently.** The anomaly is in **OpSTlDJWFFI only**, transient: frames **~959–1000** (t = 32.00–33.37 s), band y ≈ 934–994, spanning x ≈ 420–1520. Method: a 6×21-frame sub-block ladder across the bright leader run f917–1044 — the structure appears in the blocks starting f959 and f980 and is absent from those starting f917, f938, f1001, f1022. High-pass energy in the band is sd **1.95** against **0.135** in a control band at y 700–760 in the same frames (14.5×).

Your reconstruction (`analysis/cyrillic/gen1/line2.png`) resolves this to **"Предыдущее сообщение"** and I regard that reading as sound — it is legible in that artifact across several independent strips. **I could not improve on it.** My notch-filtered (AV1 comb removed at 32/16/8/4 px) and downscale-first reconstructions confirm a text-like band of the right size and position but did not reach legibility. **Line 2 is NOT recovered** — open.

**Null result elsewhere.** The identical ladder applied to the bright runs of RsQCXN4o4Ps (2011, f1151–1292), Oqw96jCOP7A (2026, f457–707) and l9RAhmPHM_A (2026, f3728–3958) shows **only** the burned-in timecode and the redaction bar — no ghosted Cyrillic, no second text layer. So the anomaly is specific to OpSTlDJWFFI and yields **no production link to the 2011 material**. Caveat: this is not an exhaustive frame-by-frame sweep. I started a whole-frame template scan across all seven videos but killed it — it did not complete in the time available, and it was flawed anyway, since the template is dominated by the timecode that both eras share, so a hit would not have been specific to the Cyrillic.

**Font/source identification: not achieved.** The letterforms are a modern humanist sans of the class used in Russian-language web and app UIs, but I will not name a face at this SNR and I did **not** determine which application the string comes from. "Предыдущее сообщение" is a generic UI label.

## Overall assessment

**Different on axes 1, 5, 7, and on frame rate within 8. Same on 3, on the locked-gate finding in 6, and on the null loop in 2. Indeterminate on 2 (spectrum), 4, 6 (shape), 8 (metadata).**

The "same" results are all shared *absences* or generic behaviours — no grain loop, no animated grain layer, damage frame-referenced and transient, gate locked with the image floating. That is what any competent-but-unelaborate digital fake looks like; none of it requires shared assets.

The "different" results are all *positive, quantitative authoring parameters* — precisely what a shared project template would have preserved: character advance 44.0 vs 42.2–42.6 px at 12–25σ; tracking ratio 0.70 vs 0.78; zero-slash 45.2° vs 39.0°; 25 vs 29.97 fps; 0.538x vs 0.666x; 2:2 step-printing present vs absent; single-axis vs two-axis tint geometry.

**The evidence favours reconstruction by an imitator working from the published 2011 videos, rather than access to original production assets.** The 2026 set reproduces everything *visible* in the published material — layout, the `/NN HH:MM:SS` format, a rounded-corner redaction bar left of the timecode, the rounded-corner gate matte, a monospace slashed-zero face, monochrome-plus-tint grading, ~45-frames-per-tick slow motion, and intro cards in the same `Case NN/<name> HH:MM:SS – HH:MM:SS` format — while missing everything that would require the original project. The frames-per-tick coincidence at a different frame rate is the single most telling detail: it is the signature of copying a measurement, not of inheriting a setting.

Confidence: **moderate-to-high** on "not the same production pipeline" — the font metrology and the speed/cadence results are individually strong and mutually independent. **Lower** on the stronger claim that the imitator had *only* the published videos; partial access to source material cannot be excluded, and axes 2/4/8 are genuinely uninformative because transcoding destroyed the relevant signal.

**Could not determine:** (1) whether either font is Consolas — not installed, not obtained; slashed zero is consistent with it in *both* eras and discriminates nothing; (2) line 2 of the Cyrillic overlay and its source application; (3) whether stock grain footage was used — no loop up to ~30 s argues against a short loop but cannot exclude a long/non-looping clip; (4) whether Sapphire/Boris FX was involved — no metadata survives; (5) gate corner radius and aperture aspect — content-dependent measurement, within-video scatter exceeded the between-era difference; (6) drop shadow on the timecode — confounded by the adjacent redaction bar; (7) redaction bar dimensions — height 57–58 px (2011) vs 79–90 px (2026) is **provisional**, partly clipped by my sampling windows; (8) whether 2011 banding was never present or was destroyed, given its extra transcode generations.
