# Skinny Bob 2026 — findings

**What this is.** A forensic examination of three videos posted in 2026 by the YouTube
channel **qtecqot**, which claim to continue the four 2011 videos posted by **ivan0135**.

**Provenance is undetermined and stays that way.** This document reports measurements and
account behaviour. It does not conclude that the material is authentic and it does not
conclude that it is fabricated. Where a measurement supports only a narrow claim, only that
claim is made.

**Built by inclusion, not redaction.** This file was written fresh rather than cut down from
the older working record, so that nothing arrives here by inheritance.

**On names.** No **private** individual is named, located, or identified here. One masked
registration address belonging to a pseudonymous account is reproduced (§19); it identifies an
account rather than a person, and nothing was ever sent to it. Pseudonymous accounts appear by handle and by behaviour
only, and no attempt is made to connect a handle to a person. Two people **are** named, in
§16: both are public creators who published about this material under their own names — one
self-identified in connection with it in 2011 and has discussed it publicly ever since. Only
their public output is described. That distinction is deliberate: protecting a private person
is not the same as declining to name a public one.

**Caveat that applies to the whole document.** These measurements were made on a
lower-bitrate copy of the videos than YouTube actually offered — 3–4× less information at the
same resolution. Findings that something *is* present are unaffected. Findings that something
is *absent*, and every stated detection floor, should be read as pessimistic. See
`CORPUS_QUALITY.md`; it is one page and it matters.

**Where the detail is.** Per-topic write-ups and all numbers live in `reports/` — see
`reports/INDEX.md`. The long working record this was distilled from is not published; it
carried the full blow-by-blow including retractions, and the retractions that survived
scrutiny are in `CORRECTIONS.md`.

---

## 1. The corpus

Seven videos. Three from 2026, four from 2011. Everything below was verified with `ffprobe`
against the media files rather than taken from metadata, and every media file is pinned by
SHA-256 in `reports/agent_corpus.md`.

| # | Channel | ID | Published (UTC) | Duration | Frames | fps | Resolution |
|---|---|---|---|---|---|---|---|
| 1 | ivan0135 | `ZB788PtqQvg` | 2011-04-14 02:04:26 | 47.5 s | 1188 | 25 | 1920×1080 |
| 2 | ivan0135 | `RsQCXN4o4Ps` | 2011-05-02 05:21:51 | 60.0 s | 1500 | 25 | 1920×1080 |
| 3 | ivan0135 | `Xju_CY5ZESA` | 2011-05-09 05:09:51 | 103.9 s | 2598 | 25 | 1920×1080 |
| 4 | ivan0135 | `a6TLGkrfNKI` | 2011-05-18 00:35:43 | 93.5 s | 2337 | 25 | 640×480 |
| 5 | qtecqot | `OpSTlDJWFFI` | 2026-05-25 09:39:42 | 100.4 s | 2998 | 29.97 | 1920×1080 |
| 6 | qtecqot | `Oqw96jCOP7A` | 2026-06-15 04:23:35 | 83.5 s | 2503 | 29.97 | 1920×1080 |
| 7 | qtecqot | `l9RAhmPHM_A` | 2026-07-24 09:14:05 | 146.7 s | 4395 | 29.97 | 1920×1080 |

Two authoring differences that survive transcoding and are not artefacts of delivery: the
2011 videos are **25 fps (PAL)** and the 2026 videos are **29.97 fps (NTSC)**; a
same-pipeline continuation would plausibly have stayed at 25. Note the resolutions above are
what YouTube *delivers today*, not confirmed original camera resolutions.

**Release markers.** The June release carries "Continuation release 6 / 8." and the July release "Continuation
release 7 / 8." The May release carries no marker. A comment written 2–4 days after the May release says
"5 of 8 completed", which resolves the scheme: **ivan0135's four videos count as releases
1–4**. One release remains.

---

## 2. What these files can and cannot tell us

This section is second on purpose. Most of the "undetermined" verdicts later in this
document are consequences of the limits stated here, and a reader who has them in hand can
tell an honest null from an evasion.

- **All seven files sit at the AV1 reconstruction floor.** Film grain is therefore
  *indeterminate by construction* in **both** eras. Any argument of the form "there is no
  grain, so it was not shot on film" is unavailable to us, and so is its opposite.
- **Effective resolution on the subjects is a few hundred pixels.** The measured point
  spread function gives a full-width at half-maximum of roughly 5–6.6 px on the interior
  material. A feature spanning ~30 resolution elements can support claims about *form and
  topology*; a feature spanning 1–2 cannot support claims about *shape detail*.
- **A concrete illustration.** A real five-pointed star, 120 px across at 35 DN contrast,
  injected into these actual frames, is a formless smudge that an independent observer fails
  to detect. See §9.
- **Absences require a measured floor.** Wherever this document reports that something was
  not found, it states the level below which it could not have been found. An absence
  without a floor is not a result, and several of our earlier ones were withdrawn for
  exactly this reason (§10).

---

## 3. The soundtrack is a sample-level copy of a 2011 video

The strongest and least interpretable result in the corpus.

The 2026 black-and-white "projector bed" is not merely similar to the audio of the 2011
video `ZB788PtqQvg`. It is the same audio.

- **Time-scale factor α = 1.0000 exactly.** The 2026 audio was not resampled, stretched or
  retimed.
- **Waveform correlation 0.986–0.993** — waveform, not spectral envelope.
- On a confirmed **14.0-second verbatim run**, subtracting the 2011 audio from the 2026 audio
  leaves a residual at **−15.6 dB: 2.8 % of the energy unexplained**, consistent with Opus
  transcode noise and nothing else.
- **15 verbatim excerpts in the May 2026 release (`OpSTlDJWFFI`) and 19 in the June release (`Oqw96jCOP7A`)**, hand-placed to about a millisecond.

Figure: `figs/audio/figF` (sample-level waveform overlay). Detail: `reports/agent_audio2.md`.

**What this supports.** The 2026 audio bed is a copy of published 2011 audio, placed by hand.
**What it does not support.** It says nothing about the origin of the *picture*, and nothing
about the 2011 material itself.

**A correction to our own record.** We previously named `RsQCXN4o4Ps` as the donor. That was
wrong — median waveform r is 0.985 for `ZB788PtqQvg` against 0.09–0.14 for `RsQCXN4o4Ps`.
The 48-band fingerprint we originally used to identify it **saturates**: every bed pair
scores ≥0.993, so it could never have ranked donors at all.

---

## 4. The picture was retimed. The audio was not.

The 2026 videos carry a burned-in source timecode that ticks in whole seconds. Counting
video frames between ticks gives the playback ratio directly, with no assumptions.

- **2026: 45 frames per tick, exactly.** The July 2026 release, Case 28: ten consecutive seconds, 450
  frames, 45.000. The June 2026 release, Triage segment: 180 frames over 4 ticks. Verified the strict way,
  by reading the digit sequence off run-averaged strips — if the seconds step by one with no
  skips, no boundary was missed, so this is a count and not an estimate.
- **2011: 46–49 frames per tick** (bracketed 42–55).
- At 29.97 fps and 25 fps respectively, that is a playback ratio of **about 0.67× in 2026
  and about 0.54× in 2011**.

So the frame counts per tick agree closely across the eras while the *speeds* differ by
about 24 %. Set against §3 — a soundtrack copied at α = 1.0000 — the picture and the audio
in the 2026 videos are running on time bases that disagree by roughly a quarter.

There is no single playback rate that makes both the audio and the picture physically
interpretable. Native speed is correct for the audio; it is not correct for the picture.

**Deliberate imprecision.** We quote "about 0.54× vs about 0.67×". Three significant figures
would overstate the data, since the 2011 per-tick spread is 44–48 frames.

Detail: `reports/agent_triage_technical.md`, `reports/agent_audio2.md`.

---

## 5. The catalog

Both eras burn a catalog into the picture: a tape number, a case number, a case name, and a
source timecode span.

**The `Case NN/name` scheme is ivan0135's own 2011 convention**, not a later fan invention.
A title card at f501–575 of `RsQCXN4o4Ps` reads, legibly and without enhancement:

```
Tape 05 edited fragments:
Case 25/skinny Bob 00:08:42 - 00:08:50
Case 25/skinny Bob 00:27:36 - 00:27:45
Case 26/How to drive 00:55:07 - 00:55:12
```

Note the lowercase "s" in "skinny Bob" — his own inconsistency. This matters because it means
the 2026 ledger is being compared against a documented in-corpus convention rather than
against community practice, which is how it was previously framed.

**The 2026 ledger is internally consistent, and consistent with 2011.** Within every tape,
case number rises monotonically with cited timecode — and it keeps doing so when the 2011 and
2026 citations are interleaved. The 2026 tape-04 cases (20/21/22 at 00:03–00:31) sit correctly
before ivan0135's 23/24 (00:42–00:58). Tape 05's five citations from two eras interleave in
order. **The only ordering breach in the entire combined table is inside ivan0135's own 2011
list.**

Two conventions shared across both eras: `~` denotes a range that fragments were *sampled*
from while `-` denotes a contiguous clip; and stated end-times routinely overrun the last
visible tick by a few frames. Both were once charged against the 2026 videos as errors; both
are house style in 2011 as well, now confirmed by direct measurement in the 2011 era.

Detail: `reports/agent_catalog_ledger.md`, `reports/agent_qtecqot_dossier.md`.

---

## 6. The Cyrillic captions

The May 2026 release opens with two lines of Russian over the leader.

- **Line 1: «Предыдущее сообщени»** — and the final «е» is **genuinely not rendered**. Ink
  stops dead at x = 1615. This fixes the caption layer's right boundary.
- **Line 2: «предупреждало об АА»** plus one further capital-height glyph, unidentified.
  Measured at **z = +10.7** against 22 same-length nulls with the left edge pinned; the best
  null scores +1.9 and a caption-free control ceiling is +3.8. The trailing glyph ranks
  Г > П > Б > В > Р > С > Е and is not resolved.
- **The caption layer is horizontally stretched by about 1.3×.** Measured «П» aspect ratio is
  1.036–1.060, against a maximum of 0.900 across all Cyrillic-capable faces available. The
  film picture itself is 4:3 pillarboxed and *unstretched*, and the separate "Mark 5" caption
  measures 1.03 — so the stretch belongs to this text layer specifically.
- **Typeface: a two-candidate shortlist, not an identification.** Constraining each candidate
  to the horizontal stretch implied by its own stroke weight, **Roboto Medium (r = 0.727)** and
  **Inter Medium (r = 0.702)** survive; every bold face collapses by 71–80 %. The two are
  separated by 0.026, which is inside the measurement jitter. The surviving class is
  **medium weight, not bold**. Untestable here: Arial, Helvetica, Segoe UI, SF Pro, Circe,
  YS Text, Proxima Nova, Graphik.
- **«ААРО» / AARO is refuted** on three independent grounds, and «прослушано» is refuted on
  glyph shape.

**A correction.** Our earlier measurement put line 2 at ~2.7σ and called it "consistent with
the pixels but not selected by them". That was wrong, and the cause was fitting the text
*without* its horizontal stretch — under which the fit fails even on line 1, whose content we
already knew. Two members of the public read line 2 correctly before we measured it correctly.

**Also settled: the "Mark 5" caption reads «Mark 5 (1961 год»** — certain glyph by glyph, with
no closing bracket. The adjacent «Самолет» is **not confirmed**: that region sits underneath
the tape's own timecode overlay and cannot be resolved.

Detail and figures: `reports/agent_cyr4.md`, `figs/cyrillic/`.

---

## 7. The hand

The strongest positive metric result in the corpus, and one the reader cannot verify by eye.

Across the three-digit gradient of the subject's hand, a shared ratio measures **0.676 in
2011 against 0.854 in 2026** — a 26 % difference, holding across all 49 usable frames and
five separate shots. An independent from-scratch landmark detector, built on a single frame,
reproduces **0.682**, with two other ratios inside 1 %.

The leading false-positive mechanism — a systematic offset in where the finger cleft is
measured — is **excluded by its own sign**: such an offset pushes every affected ratio toward
1, but the observed D4/D3 moves toward 1 while D2/D3 moves away from it, and no single offset
does both.

**And it is not visible.** An independent observer, asked carefully and with no expected
answer supplied, does not detect the reversal, and cannot reliably count the digits on the
comparison hand (4 on one pass, 5 on another). That instability is itself the measurement of
what this material supports.

So this is a reproducible measurement that the eye does not deliver — which is why it went
unnoticed for fifteen years until someone measured instead of looked. Present it as something
the reader decides whether to trust, with the landmarks and the per-frame scatter shown.

**Known gap.** There is no five-digit human-hand control. The two arguments above do not
depend on one, but the print-versus-photograph systematics rest on argument rather than
calibration.

Honest negative retained: **palm width is unusable** as a denominator across these two
modalities, and gives figures that disagree in the opposite direction.

Detail and figures: `reports/agent_finger_figs.md`, `figs/finger/`.

---

## 8. The interior symbol panel

The July 2026 release (`l9RAhmPHM_A`) only. Neither the 2011 videos nor the two 2026 siblings contain it — non-reuse is the
finding.

**The mark is real ink, not stacking noise.** Four *disjoint* frame windows agree at pairwise
IoU 0.52–0.74, with 42 % of ink common to all four against a cross-IoU of 0.037 versus a
control. Matched control regions — same frames, same transforms, same enhancement — show
blur and mottle but no stroke structure. Injected test strokes place the detection floor at
4–12 DN; the real strokes run 25–90 DN, i.e. 5–20× above it.

**But its identity is unrecoverable.** At ~30 resolution elements across the glyph and 1–2 per
stroke, form is supportable and stroke terminals are not. Three independent attempts to name
the script produced three incompatible answers — Devanagari (refuted: no shirorekha, the one
horizontal bar sits at ~40 % height and crosses only the right stem pair), Georgian Mkhedruli,
and a Latin monogram. An earlier Cyrillic reading of an adjacent mark as `2Ц` **does not
survive resolution and is retracted**.

Best available reading: a *designed* decorative or fictional-script mark, sitting among other
designed devices — set dressing rather than instrumentation. Generative pseudo-script is a
live alternative and cannot be separated from it here.

One open lead, explicitly not a result: across 145 registered frames the mark shows **no
measurable foreshortening** (anisotropy median 1.04) while translating 380 px through a
changing composition. Only 145 of 662 frames registered, and the tilt control **failed**, so
this needs redoing before it means anything.

Detail: `reports/agent_symbols.md`. Search-ready images: `analysis/symbol-panel/`.

---

## 9. Claims that died

Findings that were made, tested, and did not survive. Reported because a corpus of only
surviving claims is not trustworthy.

| Claim | Status | Why |
|---|---|---|
| Chinook helicopter reflection | **Refuted, with power** | A rendered CH-47 at this exact PSF still shows both rotor pylons. Neither is present. |
| Five-pointed star on the hull | **Refuted, but weakly** | 5/5 frames return "no markings" with a null option offered. However a *real* injected star at this size and contrast is undetectable here — so we cannot separate "no star" from "a star we cannot see". |
| "Bird-like" hull marking | **Cut** | Three observers, three incompatible readings of the same few pixels. |
| The AV1 corner dots as an authorial mark | **Resolved as a codec artefact** | Now confirmed by direct control rather than by accident: the same video fetched in both codecs carries exactly 2048 marked pixels under AV1 and none at all under AVC. `analysis/corner-dots/controls/codec_control.py`. |
| "Ghost disc" behind the text as a deliberate element | **Downgraded to one line** | Present, but not conspicuous, and its identification is unstable across repeated reads (saucer / head / hat / eye). The "same craft profile" claim is withdrawn. |
| Differential retiming between segments | **Withdrawn** | Rested on a frames-per-tick value derived from an assumed tick count with both endpoints inside lens flares. |

---

## 10. What we got wrong

One failure mode produced most of these: **a measurement made on one window was promoted to
a corpus-wide claim between the report and the summary.** It happened at least four times.

1. **"A bearded human lower face."** The source report said it *"specifically cannot confirm
   it is human."* Eight passages carried the escalated version, and one figure had the
   conclusion printed into its own labels, which is how it survived review. That figure is
   quarantined. Status: **resolved** — it is an alien mouth.
2. **"The 2026 continuation shows no blink anywhere."** Withdrawn. The basis was a single
   ~19 s search of one subject in one video. A candidate eye-localised event now exists at
   the June 2026 release, f1215–1219 (eye-region Δ 7.62 against controls ≤1.05). Candidate, not finding.
   And **there is no blood** — the dark region on that face sits at the image black floor.
3. **"No speech."** Never a finding; a sensitivity limit. We could not have detected speech
   quieter than **−37.2 dBFS** on the b/w bed or **−21.9 dBFS** on the colour segment — only
   **3 dB below the bed itself**. A voice 20 dB under the projector is invisible to any
   analysis of this material. Our own aggressive separation chain also **manufactured
   90–340 ms of false voicing from bed-only input**, which invalidates any figure quoted
   after spectral subtraction.
4. **"Zero film weave."** Cut. The frames tested are a featureless white leader (σ = 0.74 DN);
   a demonstrably moving picture scores identically; a 2011 video scores a perfect 55/55 on
   the same estimator; and the integer estimator returns zero for any shift below half a
   pixel by construction — the whole range of interest.
5. **Frames per tick.** Both of our figures were wrong (44.5 and 46.0). In the flare windows
   the timecode is not faint, it is absent. The answer is a count: 45.000.
6. **Cyrillic line 2.** See §6. We reported ~2.7σ; it is z = +10.7.
7. **The audio donor.** See §3. Wrong video named, and the instrument used to name it cannot
   discriminate donors at all.
8. **The 13 Hz projector argument.** The measurement reproduces (13.030 ± 0.006 Hz), but the
   reasoning was weak: the beds carry a *second* tick rate at 14.058 Hz, and the frame-rate
   arithmetic is **degenerate** — 24 fps at the 2011 speed fits, but so does 18 fps (a
   standard Super-8 rate) at the 2026 speed. The conclusion survives only because it was
   re-derived without any projector-speed assumption at all (§3–§4).
9. **A "verified" badge** in an earlier observation about a third-party post is a
   **public-post globe icon**. Not a verification badge.
10. **Two accounts were conflated** — a 2011 channel and a similarly-named 2026 commenter
    have different channel IDs.

---

## 11. A methodological warning worth publishing

Vision-language models are not independent witnesses on material like this, and the failure
modes are not obvious.

- **They will read your own notes.** Run from inside this project directory, one silently
  ingested our own working notes and returned our conclusions as its own opinion, in one case
  opening *"Based on a factual analysis of the image and the surrounding workspace
  documentation…"* and citing our own audits. Every earlier vision result obtained that way
  is void.
- **Filenames leak the answer.** A crop called `bearded_face_case22.png` supplies the
  conclusion as surely as the notes do.
- **On degraded text they are confidently unstable.** Seven clean-room readings of the same
  Cyrillic crop produced **six different answers**, each at 90–99 % stated per-character
  confidence.
- **On audio they fabricate.** Fed synthetic babble containing no language at all, one
  returned a confident **Mandarin numeral transcription together with invented supporting
  evidence**. It reports "Russian" in the same clip with a different phrase every time, and
  misses real voiced speech at 0 dB SNR.
- **Leading questions manufacture findings.** Asked leadingly, the same model produces stars
  on low-resolution tiles that contain none.

They remain useful for one thing: transcribing high-contrast text, where the answer is
checkable. For adjudicating a contested visual claim, a matched filter with pinned templates
and matched nulls is the only clean instrument we found.

---

## 12. Open questions

- The trailing glyph in Cyrillic line 2 — unidentified.
- The typeface — a two-candidate shortlist; would need Regular/Medium cuts of the untestable
  commercial faces to close, and could be reopened entirely by synthetic emboldening.
- The symbol panel's script — three attempts, three answers.
- The candidate blink at the June 2026 release f1215–1219 — needs a proper control set.
- The five-pointed star — needs a frame reference from the person who reports seeing it.
- The no-foreshortening result on the symbol panel — needs the failed tilt control redone.
- A five-digit human-hand control for §7.
- Whether the 2011 material's own audio time bases (the two 2011 tracks are ~8 % apart from
  each other) bear on any of this.

---

## 13. The hidden four-frame insert

Video 1 contains a deliberate jump-scare that nobody reported for two months.

At **f2971–2974** — four frames, about 99.1–99.2 s, at the video's climax — a blue-tinted,
posterised flash is cut in. It is supported by engineered percussion hits at 98.70, 99.20,
99.60 and 99.95 s, so the audio was built around it.

Two facts about it matter more than the insert itself.

**Nobody found it.** It appears in no comment in either era's corpus, and an outside
analyst who frame-walked the entire video assigned frames 2571–2990 wholesale to a single
clip and never saw it. It was found by eye, by a viewer, not by any automated pass.

**Its content is unidentified, after two confident wrong answers.** One AI identification
named an Apollo-11 frame at ~95 % confidence; it was withdrawn. A later independent
identification named a well-known military UAP video at **99 % confidence**; it does not
hold either. Four frames at this resolution do not support an identification, and two
high-confidence attempts failing is the measurement of that.

Figures: `figs/vision/` jumpscare panels — both the raw frames and the enhanced versions.

---

## 14. Two positive findings that point at photographed material

Most of this document narrows or withdraws claims. These two survived scrutiny and run the
other way.

- **A raster-locked rectangle across two different tapes.** A hard-edged rectangle sits at
  the same ~15 px window in four separate scenes, spanning material the catalog places
  **38 source-minutes apart on two supposedly different tapes** (the catalog span is 38:14).
  An element fixed to the output raster, rather than to the scene, is a composite tell — and
  a real one, because it is not something a viewer would notice.
- **Bright specks that track the scene.** In the dark interior, bright specks hold coherent
  mutual motion for 30+ frames at constant brightness. That is the behaviour of physical
  objects in a volume, not of an overlay. This is one of the few results pointing toward
  photographed material.

**And one that did not replicate.** A claimed output-frame-locked scanline layer (period
5.38–5.40 px, SNR to 130×) **failed independent re-check**: the dominant peak drifts between
5.95, 6.76 and 7.14 px and never lands on 5.4, and the claimed weak-segment contrast
inverts. It is most likely a window mismatch rather than a refutation, but it cannot be
published until it is re-derived against the original region and frame list. Separately, the
AV1 static block comb sits at ≤0.5 LSB in all seven files — the same amplitude band as the
claimed signal, a confound never previously stated.

---

## 15. How many faces

Exactly **one** face in the 2026 corpus is established, and it is not the one the record
used to lead with.

- **Established:** a human figure in profile in video 1, f1437–1570 — nose bridge and tip,
  upper lip, mouth, chin, plus a shoulder board with two circular devices. Two independent
  models, unmodified frames, open non-leading questions, replicated under strict one-image
  isolation. No stacking required.
- **Not established:** the Case 22 head, which the record previously called "a bearded human
  lower face". See §10 item 1.

So the earlier framing had the ordering inverted: the doubtful one was presented as
resolved, and the solid one as a secondary confirmation.

---

## 16. Other people

Three parties published about this material. All three are treated as **public creators
acting publicly**; nothing here is derived from private information.

**Ben Philips**, a VFX professional who has publicly self-identified in connection with this
material since 2011, ran the 2011 YouTube channel `@Bedeekin`
(`UCzJ1dolFZi8x7Y41gOnTtEA`). It reposted ivan0135's videos eight days after upload and has
accumulated **116,067 views** — considerably more than the originals were getting at the
time. Fifteen years later he has commented again on the 2026 material.

⚠ **A distinction the earlier record blurred.** The 2026 commenter `@bedeekin6274`
(`UCMYqkbFffB_rqSjHEmyyV2A`) is a **different channel** from the 2011 `@Bedeekin`, with a
different channel ID and a display-name spelling one letter off. Same apparent person, not
the same account — and any argument resting on "the same account returned" is invalid.

**Rock Ferguson**, a Facebook creator, produced reposts that outdrew everything else
combined. One reel alone carries **6,700 likes**, against **657** likes across all three
qtecqot uploads. Facebook was login-walled on every URL attempted, including the share link
inside one of the reels, so these figures come from what was visible without an account and
are **incomplete by acknowledgement, not by inference**.

**`@m21-b5q`**, the account qtecqot answered. See the account-behaviour analysis: an
ordinary engaged audience member at roughly 85–90 %.

**The reach asymmetry is the finding here.** The analytical discussion of this material lives
on Reddit; the audience lives on Facebook, by an order of magnitude. Any account of "how the
community received this" that samples only Reddit is sampling the wrong population.

---

## 17. The corner dots, and an accidental confirmation

Small dark dots appear at fixed positions in frames across the 2026 corpus. They are a
**codec artefact, not an authorial mark** — 32×32 blocks at (0,0) and (960,0), AV1 tile
corners.

The confirmation arrived by accident and is the strongest available. An outside analyst
distributed frames decoded from **AVC**; ours were decoded from **AV1**. Comparing the same
frame: maximum per-pixel difference **1**, mean **0.001**. Our frame contains values {0,1};
theirs contains only {0}. That single-least-significant-bit delta *is* the tile-corner stamp
— present in the AV1 decode, absent from the AVC decode of the same source. Two independent
codec paths, and the artefact tracks the codec rather than the content.

---

## 18. Audio you can listen to

The re-derived audio work produced renders rather than only numbers. `audio/` holds 22
files: each 2026 video at native speed, each at the ×1.5 "correction", and the cleanest
speech-band isolations achievable.

Listening to the ×1.5 versions is itself informative — they sound wrong, and that is the
expected result. **×1.5 speeds up audio that was never slowed.** Native speed is correct for
the audio (§3–§4), so the correction that makes the *picture* interpretable makes the sound
worse. No single rate makes both right.

The colour-segment element is **not present in either 2011 file** — unlike the
black-and-white bed, it is original 2026 material. A previously reported "exactly six tones"
in it is threshold-dependent: 59 spectral lines clear 8 dB while only 2 clear a strict
carpet, which substantially weakens the tuned-cluster reading built on it.

---

## 19. The masked registration address

X exposes a masked form of an account's registration address through its recovery flow. For
`@qtecqot` that mask is:

> `cc*****@*****.com`

It identifies an account, not a person, and no attempt was made to resolve it further.
**Nothing was ever sent to it and nobody was contacted.**

What it does and does not constrain:

- The visible local part begins `cc`, on a `.com` domain.
- Whether the number of asterisks maps character-for-character to the real address is an
  **untested assumption.** X may preserve length, or may render a fixed-width mask. If length
  is preserved the local part is seven characters; if it is not, the mask says nothing about
  length at all.
- That distinction is settleable in about a minute by viewing the mask for an address you
  control and comparing, which is listed as an open item in `UNFINISHED_BUSINESS.md`. Until
  someone does it, no inference resting on the length is safe.

The mask is obtainable only by driving an account-recovery flow against a live account. It is
reproduced here because it is a fact of the record, not because it leads anywhere: on its own
it is consistent with an enormous number of addresses.

## 20. How the videos were put together

The strongest results here are not about what the footage shows. They are about the
assembly, and they are measurable.

**The damage layer floats.** In the June 2026 release, at frame 2422→2423, the picture
and the burned-in timecode both hard-cut to black in a single frame — and the film dirt
keeps playing over pure black for **36 more frames**. It runs on a strict 3-2-2 repeating
cadence, period 7 output frames, about 12.84 patterns per second, which is not an integer
relationship to the 45-frame timecode tick. Within a held plate the dirt is bit-identical
while the picture underneath moves; between plates it jumps 4–63 px while the image moves
0.11 px or less. It was applied in post.

Bounded inference, stated deliberately: film-look passes get applied to real archival
footage too. This establishes that the *look* is constructed. It says nothing about the
content underneath.

**The two 2026 videos were not processed identically.** In the May release the dirt
amplitude is preserved across hold groups and marks live 1.8–2.0 frames against a
~2.9-frame content hold, which puts the damage pass *before* the retiming stage — it
belongs to the picture layer. In the June release the dirt floats *after* assembly on its
own cadence. Same kind of pass, opposite ordering. One toolchain, per-video settings.

**One retime over an assembled timeline.** All three 2026 videos carry a bit-identical
frame every 12, an 11:12 conform from about 27.5 unique fps inside a 29.97 container, and
it runs unbroken through shot cuts with no phase reset. Every uploaded format reports 30
fps, so this is in the master rather than YouTube's transcode.

**There is no gate weave, and the border moves the wrong way.** Aperture-boundary pixels
have a temporal standard deviation of exactly 0.000 across 101 consecutive frames. In the
May release the vignette border does drift, sub-pixel at σ 0.29–0.55 px — and the
burned-in timecode drifts *with the border* while the picture moves independently inside
it. A real projector has a fixed gate and weaving film. This is the reverse. Amplitudes
are under 1 px, so the power is low.

**Source-rate archaeology.** The black-and-white picture advances in bursts of about 16 ± 1
distinct images per burned-in second, consistent with a 16 fps cine source — a standard
amateur rate — slowed by frame repetition. The colour Mk.5 clip instead moves on *every*
output frame, about 40.8 distinct images per source second, which is not a plausible 1961
camera rate. That implies either synthesized intermediates or a high-rate source for that
shot specifically.

**One mismatch in the story's own terms.** The sources are called "tapes" throughout. The
applied damage is film dirt, film scratches, and a film gate. Videotape has none of those.

## 21. The audio, beyond the copy

Section 3 covers the sample-level copy. Three further measurements:

**A projector-like tick sits in both eras.** Envelope-modulation peaks at 13.0 and 14.0 Hz
in the two 2026 videos with audio, and 13.1 and 12.0 Hz in the two 2011 videos with audio,
at comparable prominence. Both eras are band-limited to roughly 7 kHz, consistent with
deliberately narrow-band audio rather than full-bandwidth modern capture.

**The tick matches 2011's playback speed, not 2026's.** A 24 fps projector at the 2011
ratio of 0.538× ticks at 12.9 Hz. At the 2026 ratio of 0.666× it would tick near 16 Hz. The
measured 13 Hz therefore belongs to 2011. Audio and picture are decoupled by about 3 Hz —
which is the same conclusion as section 4, reached independently: the bed was copied
unchanged while the picture was retimed.

An earlier version of this claimed the 13 Hz figure *corroborated* the 2026 slowdown. That
was wrong and is retracted. It resolves the other way, and the other way is more
interesting.

**The July 2026 release has a real audio track containing digital silence.** Not a download
artifact: YouTube's Opus encode of it runs at 3.6 kbps, the rate Opus produces for silence.
This vindicates the top comment on that video, at 22 likes — *"Bro, you forgot to include
the sound of the projector running."* Two of the four 2011 videos are silent the same way.

## 22. Why the corner dots looked like a watermark for so long

Section 17 gives the conclusion. The derivation is worth keeping because the false trail
was well-evidenced.

The pure-black frames of the May release are flat Y=16 except for **exactly 2048 pixels at
Y=17: two solid 32×32 blocks at (0,0) and (960,0)**. Those are the first superblock of each
960-px tile column, YouTube encoding 1080p AV1 with two tile columns. The same blocks carry
partial and gradient versions of the mark in the other 2026 videos and in the 2011
`Xju_CY5ZESA` frames — pixel-identical between the left and right block under a +960
translation, and position-identical across videos and across eras, because the position is
fixed by the encoder's tile grid rather than by content.

That single artefact accounts for **every** cross-era "constellation match" that had looked
like file lineage: 88 shared positions between the June release and 2011 `Xju`, all 118 of
the July release's positions inside the 2011 leader field, 112 shared between the two 2026
videos. All of them lie inside those two blocks. Everything else in the black frames is the
level-1–4 fade tail of title cards that are plainly visible seconds later.

The matches had survived strict nulls — a local-density null and a lattice-preserving
shift-permutation test at ±16-px torus shifts, n≈200, giving 88 observed against a null
mean of 0.1. They were real. They were just the encoder's.

Provenance information content: zero. The methodological corollary is the part worth
carrying: **pixel-level watermark hunting on YouTube re-encodes has to control for codec
behaviour**, and at 1080p that means masking the 32×32 blocks at (0,0) and (960,0) before
comparing black frames at all.

**The control, run deliberately.** The original confirmation was luck — a third party
happened to have AVC frames that lacked the stamp. The same YouTube video has since been
fetched in both codecs and compared directly, which is the falsifiable form of the claim: an
authorial mark survives a change of codec, an encoder artefact does not. Frame 2 of
`OpSTlDJWFFI`:

| | AV1 (`videos/2026/`) | AVC (`videos/2026-avc/`) |
|---|---|---|
| luma histogram | 2,071,552 px at Y=16, **2,048 px at Y=17** | **2,073,600 px at Y=16**, nothing else |
| bounding box of marked pixels | rows 0–31, cols 0–31 and 960–991 | — |
| inside the two 32×32 tile corners | 2,048 of 2,048 | — |
| left block = right block at +960 | yes | — |

Every marked pixel falls inside the two predicted blocks, and the artefact is *completely*
absent from the AVC decode of the same frame. Reproduce with
`analysis/corner-dots/controls/codec_control.py`. One caution if you re-derive this by hand:
plain `-pix_fmt gray` rescales limited-range luma onto 0–255, collapsing the Y=16/Y=17
distinction the test depends on into 0/1 — the script forces full range to keep the codeword
values quoted here.

## 23. The account existed before the name did

The channel was created 2026-04-22 at 05:27:55 UTC. Video 1's title card reads *"0135
location and status unclear as of 2026/04/21. Incapacitation presumed."* The channel that
delivers those releases came into existence **one day after the story's own trigger date**,
and a month before the first upload.

An earlier version of this said the two dates matched *exactly*. They do not — that error
manufactured a same-day coincidence, and it is corrected here. The one-day offset is the
real observation.

The X account was created in the same month, 2026-04-28. The string "qtecqot" has
essentially no web footprint: it first appears publicly on 2026-05-25 with the first
upload. An account holding that exact name, registered before the name existed publicly,
cannot be someone squatting a handle they had seen. Whoever registered it knew the name
pre-launch.

At the July 2026 check the X account had zero posts, one follower, and followed exactly
three accounts: a UK UFO commentator, the Russian space agency, and Elon Musk. The second
of those stopped posting when Russia blocked Twitter, so following it is symbolic rather
than useful.

Whichever provenance hypothesis you hold, the operator committed to the 04/21 date before
going public and then acted on it. The infrastructure was staged, not improvised.

## 24. Two things the audience got right, and one worth retiring

**Right: the missing projector sound.** Covered in section 21 — the top comment on the July
video identified a genuine anomaly.

**Right: the audio resembling ivan's.** The recurring comment *"It's got sound similar to
Ivan?"* has a quantitative answer, and it is yes — same modulation band, same order of
prominence, and ultimately the same samples.

**Worth retiring: "five fingers at 1:24."** The hand spans about 250 px against a ~15 px
point-spread width with no grain, so digit count is unresolvable in principle. But there is
a specific reason the percept appears: **the burned-in timecode glyphs sit directly across
the fist**, and stationary bright glyph lobes over a moving hand read as extra fingers.

Also not supported: the "GTA idle animation" reading. Self-similarity decays monotonically
across the sequence, with no looping idle. Several things do point the other way — eye
speculars appear and vanish correctly with head-light geometry across four fragments, a
crown patch and an emblem track their substrates precisely, and there is no melting, no
mutating marks, and no wrong shadows.

## 25. Loose threads

Small, unresolved, and recorded so nobody has to rediscover them.

**One fragment is retimed differently from all the others.** Case 11 "Tin bird primer" on
Tape 02 runs non-constant, 33 to 46 frames per tick, drifting *within* the single fragment,
where every other fragment sits at a constant 45. Either a variable-speed source or a
different processing path for that tape.

**A hidden disc behind the opening title card.** Averaging frames 40–300 of the May release
and median-suppressing the text reveals a bright rounded film-frame field with a dark
lenticular disc silhouette in the lower left — domed top, flat underside with a lip, the
same craft profile as the "tin bird" shots. It is the same genre of device as the hidden
Cyrillic leader text and the four-frame insert: content placed where casual viewing will
not find it.

**A possibly reused effect element.** Two morphologically near-identical sweeping-band
artefacts appear 44 seconds apart in different shots — same start row near 244, same speed
of about 5 rows per frame, profile correlation r = 0.84. Either a recurring transfer
artefact or a reused effect element. Undetermined.

**The one account qtecqot answered.** `@m21-b5q` reads as an ordinary engaged viewer rather
than an alt: the account dates from 2015 with 3 subscribers and no uploads, its prose
carries an error fingerprint absent from qtecqot's clipped register, it misreads the lore in
ways an author would not, it replied in German elsewhere in the thread, and it demands raw
unedited source files — which is pressure an author of fabricated material cannot satisfy.
