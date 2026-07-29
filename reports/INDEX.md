# Agent report index

Every subagent report in this investigation, archived **verbatim** (one exception, noted).
Each line: what it settles, and the FINDINGS section that consumes it.

Reports are the primary record. FINDINGS.md is the running synthesis and carries
corrections; where the two disagree, **FINDINGS is newer and wins** — but the report
holds the numbers and the method.

---

## Wave 1 — the original teardown (2026-07-26 / 27)

| Report | What it settles | FINDINGS |
|---|---|---|
| `agent_video1_OpSTlDJWFFI.md` | Per-video teardown of the 2026-05-25 release | §0–§2c |
| `agent_video2_Oqw96jCOP7A.md` | Per-video teardown of the 2026-06-15 release | §0–§4 |
| `agent_video3_l9RAhmPHM_A.md` | Per-video teardown of the 2026-07-24 release | §0–§8 |
| `agent_compare_2011_vs_2026.md` | **HEADLINE.** The 2026 pipeline is NOT the 2011 pipeline: timecode fonts 12–25σ apart, 0.538× vs 0.666× playback, both holding ~45–46 frames/tick at *different* frame rates = a copied *measurement*, not an inherited setting | §12 |
| `agent_cyrillic_line2.md` | Line 1 = «Предыдущее сообщение». Line 2 present but unread; «об утечке» falsified; **why VLMs converge on «предупреждало» from grammar alone, with zero pixel evidence** | §2 |
| `agent_grain_damage.md` | No grain loop either era; damage is frame-referenced and transient in BOTH — kills "filming a damaged print" both ways | §17 |
| `agent_banding_colour.md` | Banding absent both eras (the 2011 "CRT banding" is caption line-pitch + AV1 block comb); tint geometry a_v/a_u −0.96/−1.32 (2026) vs ≈0 (2011); tape-06-colour falsified | §17 |
| `agent_catalog_ledger.md` | 2026 extends the 2011 case scheme coherently but breaks one-name-per-case; endpoint mismatches are house convention in BOTH eras (2011 misses 27 %) — **retracted our §11.6 charge** | §11.6, §18 |
| `agent_scenes_content.md` | Case 22 bearded face resolved by motion-stacking; col/s audio deep-dive; walkabout physics corrections. **Explicitly did NOT sweep videos 1 and 3 for faces** — the gap §31 later closed | §20 |
| `agent_morphometry.md` | No ratio separates the eras in head or craft; four-digit hand HAS a published 2011 precedent. **Superseded in part by `agent_finger.md` — see §28** | §21, §8 |
| `codex_visual_audit.md` | Outside visual second opinion | — |

## Wave 2 — the community material (2026-07-28 / 29)

Triggered by qtecqot's first tweet and the arrival of the first outside analyst.

| Report | What it settles | FINDINGS |
|---|---|---|
| `agent_community_lc.md` | Behavioural profile of u/Outrageous_Courage97 ("LC"). **P(connected to qtecqot) ≈ 0.05** — methodology predates the target by 5 years, disjoint clocks, wrong nationality, missed what an author cannot miss. Stylometry: the tweet IS the same author as the video cards (~0.90–0.95), on bare "0135" and article-dropped status clauses | §25, §25.3 |
| `agent_pdf_breakout.md` | LC's 22-page deck verified. **All 8 ledger rows exact**, including two invisible boundaries. **Zero non-public information**, proven three ways. Found the v1 uniformed figure that broke our §20 claim | §26 |
| `agent_zip_toolkit.md` | The 1.61 GB toolkit carved and measured. **LC shipped their own YouTube download**, so provenance is measured not inferred: itag 137+140, no master. **§13 (the dots) independently confirmed from a second codec**; §2c insert proven to be real content, not an AV1 artifact. ⚠ *Only non-verbatim report — a real personal name is redacted* | §27 |
| `agent_finger.md` | **★ THE BIGGEST RESULT.** LC's little-finger claim CONFIRMED and amended: the whole three-finger gradient differs (R 0.676 vs 0.854, +26 %, all 49 frames, five shots). **Reverses §21.** First positive metric result favouring reconstruction | §28 |
| `agent_mk5_claims.md` | Chinook reflection and five-pointed star both REFUTED, with power — a rendered CH-47 at this exact PSF *still* shows both pylons. The wedge is on a *different* craft in a b/w shot 50 s earlier | §30 |
| `agent_v1faces.md` | **A SECOND human face confirmed** (v1 f1437–1570, no stacking needed, all four controls passed) → §20 corrected. Shoulder star refuted. Leader frames are NOT blank. **§11.5 strengthened 100×** by the f1207–1210 discontinuity | §31 |
| `agent_cyr3.md` | **★ The most rigorous measurement in the corpus.** Line 2 re-derived from scratch. **New glyph-agnostic result: the line ends in a run of exactly THREE capital-height glyphs** — two adjacent triangular/diagonal capitals (А Л Д Х class) + one stem-with-top-arm (Г Е Т Р Б class); cap band empty x 445–1250, occupied to z +113 at x 1300–1550, surviving line-1 subtraction and a descender-bleed control at 14:1. Geometry corrected: baseline **1056** (not 1048), size **0.86×** line 1 (not 0.6×), length **22.2 ± 2.4 chars**, typeface **Roboto Medium** (not DejaVu). **«ААРО» = AARO REFUTED** (z ≤ +0.78, the *weakest* of four candidates; no ink where its 4th glyph must fall; a true ААРО would score z +7.12 rank 1/602). **«ААРС» refuted.** **«АА» weakly supported at ≈2.7σ** — exactly the level a *known-correct* capital pair scores on line 1, so consistent with the pixels but **not selected by** them (8 other pairs tie). **«прослушано» refuted on length; «предупреждало» compatible and the only one of the two.** Establishes that the downscale-then-stretch recipe is a *display* improvement only (<0.5% measurable) | **§2a**, §2, §10, §26.7 |

## Wave 3 — transcript archaeology (2026-07-29)

The owner's instruction: mine both session transcripts for information he supplied in
conversation that never reached disk, and compile the unfinished business. Sessions are
`7f414e56` (2026-07-26/27, short) and `6c2508df` (2026-07-27/29, the long one).

| Report | What it settles | Consumed by |
|---|---|---|
| `agent_transcript_convoA.md` | Session A recovered. **Imgur `gallery/HGv2xDf` is 2020 prior art on the Case 25/26 timecode thread, downloaded but never transferred or read by anyone here** — the single highest-value loss. Pond5 8956463 has a free watermarked route, so §6a's "signup wall" is wrong by one item. §6a dropped its whole Duration/Res column (Getty 104161830 is natively **1756×1080 ProRes** — an odd width, itself a tell; Shutterstock 1018941496 is 25 fps). Claude-for-Chrome's capability envelope unrecorded, and `docs/PIPELINE.md` §7's stored prompt contains an impossible task | §6a, PIPELINE §7 |
| `agent_transcript_convoB1.md` | Session B, first half. Recovered the `queue-operation` messages the defective extractor missed | UNFINISHED_BUSINESS |
| `agent_transcript_convoB2.md` | Session B, second half — community wave, Croatia, the tweet, outreach. §1.12 holds the @UAPJedi follow detail that later drove §6e.1 | §6e.1, UNFINISHED_BUSINESS |
| `agent_openitems_audit.md` | Undischarged commitments, orphan references, record integrity, coverage gaps | UNFINISHED_BUSINESS |

⚠ **Known defect in the wave-3 input material.** The extractor that produced the
per-session user-turn files treated Read-tool image results as human turns, because the
harness logs them as `type: "user"`. Session A's "19 human turns" are really **five**; the
other 14 are tool results and `/compact` plumbing. Session B's "128" is inflated the same
way. Any future re-run must drop user messages whose only content is an `image` block.

## Wave 4 — the interior panel (2026-07-29)

| Report | What it settles | FINDINGS |
|---|---|---|
| `agent_symbols.md` | The video-3 interior symbol panel recovered for reverse search (`analysis/symbol-panel/`). **The mark is real ink, not stack noise** — four disjoint windows agree pairwise IoU 0.52–0.74 with 42 % of ink common to all four, matched control ROIs show no stroke structure, and injected test strokes set a detection floor of 4–12 DN against real strokes of 25–90 DN. PSF FWHM ≈ 5–6.6 px → the glyph is ~30 resolution elements across, so **form and topology are supportable but stroke widths and terminal shapes are not**. **Devanagari REFUTED** — no shirorekha; all four stem tops free and pointed, the single bar sits at ~40 % height, spans only the right pair, and over-runs right. **The `2Ц` reading in `agent_video3` does not survive resolution** and is retracted — most likely the bracket ornament or the small dial at ¼ scale. Best reading: a *designed* decorative/fictional-script mark (5:1 calligraphic weight modulation, consistent pen angle) sitting among other designed devices — i.e. set dressing; generative-AI pseudo-script is the live alternative. **No 2011 reuse and no reuse in the two 2026 siblings** — the panel is unique to video 3. Unrequested extra: across 145 registered frames the mark shows **anisotropy 1.00–1.42, median 1.04 — no foreshortening at all** while translating 380 px, but with selection bias (145/662) and a **failed ASIFT tilt control**, so this is a lead, not a result | §8, retracts a `agent_video3` reading |

## Wave 5 — consolidation and audit (2026-07-29)

The last pass. Four of these re-measure earlier claims rather than opening new ground, and
two are audits of the record itself.

| Report | What it settles | FINDINGS |
|---|---|---|
| `agent_corpus.md` | The seven videos as digital artefacts: identifiers, exact publication timestamps, encoding, on-screen text and the burned-in catalogue each carries. Every field verified directly against the media files, with SHA-256 per file. **The reference table the rest of the record hangs off** | §1 |
| `agent_audio2.md` | Audio re-verification after the owner challenged the 13.03 Hz reading. Redoes §5b properly with figures, and takes the "the projector is loud enough to mask speech" objection seriously — the negative is an SNR limit with a stated floor, not an absence. **Corrects the earlier claim that the modulation independently corroborated the donor finding** | §21 |
| `agent_cyr4.md` | The Cyrillic caption's best single frame, the typeface, and line 2. Supersedes specific numbers in `agent_cyr3.md` and `agent_cyrillic_line2.md` without overturning their method | §2, §2a |
| `agent_finger_figs.md` | Reader-facing figures for the hand result, plus an independent clean-room `gemini` vision check on unannotated crops and a from-scratch spot-check of the landmarks | §28 |
| `agent_triage_technical.md` | Re-measures §8, §9, §11, §12, §13, §17, §18/18b from the media files for the public rewrite. Scripts in `analysis/timecode-ticks/`, figures in `figs/technical/` | §8–§18 |
| `agent_vision_readjudication.md` | Re-adjudicates five disputed vision claims — the Case 22 face, the "second" face, the five-pointed star, the ghost disc, the missing blink — using `gemini` as independent eyes under clean-room conditions. **The source of several retractions in `CORRECTIONS.md`** | §20, §30.2, §31 |
| `agent_qtecqot_dossier.md` | The account's complete public record, reader-facing. Folds in and supersedes the scattered §6 family | §23 |
| `agent_other_people.md` | Everyone who is neither ivan0135 nor qtecqot: the one commenter qtecqot replied to, and the two outside creators who amplified the material. Public accounts, public posts, public numbers only | §16, §24 |
| `agent_record_integrity.md` | Read-only audit of every document for claims that read as current but have been superseded, and for personal information that should not ship. **No edits made by that agent** — it produced the list the cleanup then worked through. Its own before/after quotations are redacted where the "before" carried identifying detail | — |

## Reading order for someone picking this up cold

1. `FINDINGS.md` §0 for the corpus, then §12 for the headline.
2. `agent_compare_2011_vs_2026.md` — the load-bearing measurement.
3. `agent_finger.md` — the strongest single discriminator we have.
4. `FINDINGS.md` §25–§32 — everything that happened once the subject started talking back.
5. `docs/PIPELINE.md` — the post-processing stack as a standalone essay.
6. `CORPUS_QUALITY.md` — before you trust anything phrased as a limit.

## Standing rules for this archive

- **Archive agent reports verbatim.** The only permitted edit is redacting a real
  person's identifying information, and it must be flagged inline where it happens.
- **Never publish identity.** Behaviour, timestamps and measurements are fair game;
  names, addresses and locations of private individuals are not — this applies to the
  outside analyst, to the third-party identification thread, and to anyone else who did
  not choose to be part of this. Two public creators who wrote about this material under
  their own names are the entire exception.
- **Extraction recipe** (subagent JSONL → report): parse
  `/tmp/claude-1001/-home-user-new-skinny-bob/<session>/tasks/<agentId>.output`,
  take the longest assistant text block, write to `reports/`.
