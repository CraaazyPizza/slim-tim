# star-question

Rerun of the five-pointed-star null on the AVC copy, per `UNFINISHED_BUSINESS.md` "Start
here" item 1 and issue #4. Arm 1 (deterministic matched-filter detector) is under
construction; Arm 2 (blinded observer) is not started.

Scope is the **hull** star claim, `OpSTlDJWFFI` f2571–2917 (`CORRECTIONS.md:387`,
`reports/agent_mk5_claims.md:53-100`) — not the shoulder-board claim at
`CORRECTIONS.md:388`, which was refuted by a different method and needs its own design.

Run `.venv/bin/python analysis/star-question/selftest.py` before anything else. No
calibration and no grid run until every check passes.

## Files

| file | responsibility |
|---|---|
| `common.py` | frame access, shape-preserving blur, integral-image box stats, masks, shapes, templates, centre-aligned `xcorr`, injection |
| `detect.py` | the matched-filter detector (D7/D8/D9), the crop domain, and the margin decision statistic |
| `measure_psf.py` | per-codec edge-spread σ and FWHM on f2600, the poly-4 dome residual floor, the D48 pooled aggregation, the overshoot diagnostic and the robustness replicate. Writes `psf_av1.json` / `psf_avc.json` — **the only production source of σ and the location tolerance** |
| `calibrate.py` | null generation and per-stratum threshold calibration (N3′, N6, item D). Writes `nulls_<codec>_<stratum>.jsonl` and `thresholds_<codec>.json` |
| `run_grid.py` | the codec-neutral planning step and the injected-trial grid (D20–D28, D42, D44, D48(5), A1, S1). Writes `plan.json` and `grid_<codec>.jsonl` |
| `selftest.py` | invariants the grid depends on; expected-vs-measured printed throughout |

## Decisions log

### D42 — contrast is recorded on both axes

Contrast is injected as a **nominal pre-blur amplitude**, matching `mkfigs.py:216-217` and
keeping the published 35 DN figures directly comparable. The **delivered peak depth is
measured per trial** — `max |injected − clean|`, taken from that trial's own rendered star
rather than from a table — and the limit surface is reported on **both axes**.

Delivered depth at 35 DN nominal, dark polarity, rotation 0°, computed through the same
`common.inject` path `run_grid` uses for `contrast_delivered_dn`:

| size | σ = 8.13 (published) | AV1, σ = 4.5725 | AVC, σ = 4.4324 |
|---|---|---|---|
| 40 px | 21.91 DN (0.626) | **32.33 DN (0.924)** | **32.67 DN (0.933)** |
| 60 px | 30.05 DN (0.858) | 34.77 DN (0.993) | 34.82 DN (0.995) |
| 80 px | 33.45 DN (0.956) | 34.99 DN (1.000) | 34.99 DN (1.000) |
| 100 px | 34.62 DN (0.989) | 35.00 DN (1.000) | 35.00 DN (1.000) |
| 120 px | 34.92 DN (0.998) | 35.00 DN (1.000) | 35.00 DN (1.000) |
| 140 px | 34.99 DN (1.000) | 35.00 DN (1.000) | 35.00 DN (1.000) |

Rotation moves delivered depth by ≤ 0.12 DN at 40 px and not at all at ≥ 120 px. Dark and
bright polarity deliver identical magnitude.

**The rationale is weaker than originally stated, and the decision still stands.** At the
published σ the size axis distorted contrast by 37 % at 40 px; at the measured σ the worst
case is 7.6 %, and everything ≥ 80 px is exact to three decimals. A limit quoted in nominal
DN is therefore very nearly comparable across sizes after all. Recording both axes costs
nothing at runtime and 7.6 % is not zero, so D42 is retained — but it is **no longer
load-bearing**, and the report must not lean on it as though it were.

*Method note.* Recomputed with the repo's own injection path, not by hand. The same code at
σ = 8.13 reproduces the superseded figures — 34.92 and 21.91 against the 34.9 and 21.9
previously recorded — which is what licenses the replacement.

### D43 — disjoint null split

A **calibration** set fixes the threshold, a held-out **evaluation** set reports the
false-positive rate and its Wilson CI. Using one set for both would be circular.

*The "2× the injected trial count" of the original wording is **superseded by N3′** — it
presumed nulls could be drawn repeatedly, which they cannot. The disjoint-split principle
is unchanged.*

### D44 — polarity is a required `TemplateBank` property, with no default

`TemplateBank(sigma_full, polarity)` raises on anything but −1 (dark, the headline grid of
D24) or +1 (the bright replicate). There is no default, for the same reason `detect()`
requires `domain`: a hypothesis that can be silently wrong will eventually be silently
wrong. Sharing a bank across injected and null trials guarantees they share a polarity,
exactly as sharing a `domain` guarantees crop parity.

**The sign is applied at template level, to star5, star6 and disc alike**, so the margin
and the historical specificity are both computed from polarity-consistent responses.
Negating only star5 would hand the target template a sign advantage its own controls lack.
Polarity is pre-specified per run and never inferred from pixel values — inferring it, or
maximising over both signs, would double the null search space and inflate the very
false-positive rate the calibration exists to measure.

`is_detection()` remains **margin-only**. The specificity scalar is a historical
comparison measure and must never enter the decision path; a self-test asserts this by
parsing the function body with the docstring stripped.

### D45 — `NORM_HALF` frozen at 40

Frozen now, before any calibration null is generated. Rationale, recorded in full:

- selected a priori at approximately four times the half-resolution PSF FWHM;
- selected **before** the injected-star outcome was evaluated;
- never varied or tuned in response to a result;
- under polarity-corrected detection the 120 px / 35 DN fixture localises with **1.0 px
  full-resolution error** at this value.

### D46 — `LOCATION_TOL_FULL` is per codec

"One resolution element" is defined from **that codec's measured PSF FWHM**, produced by
`measure_psf.py`, replacing the former fixed `20.0`. `is_detection()` takes it as a
required argument; there is no module constant and no default.

*Rationale.* A fixed 20 px tolerance is proportionally more generous to a sharper codec
and therefore introduces codec-dependent bias in the direction that can flatter AVC — the
arm under test, not the arm to favour. A per-codec resolution-element tolerance follows
D12 and applies the same physical criterion to both copies.

*Aggregation.* **Superseded by D48 — see below.** The original rule was the larger of two
edge-spread cuts, since `agent_mk5_claims.md:220-222` reports two (8.13 / 8.40 px, 19.1 /
19.8 px) and specifies no aggregation. That rule presumed a second cut which does not
exist on the published frame. The per-codec principle above stands unchanged; only the
aggregation was replaced.

### D48 — pooled aggregation, superseding D46's two-cut rule

The two-cut rule failed loud on f2600 and was correct to. Above the hull mask at
x 1050–1500 the image already sits at 108–136 DN, so the 140 DN contour there runs through
a smooth bright gradient, not a step; measuring edge spread across an iso-luma contour of
a gradient measures the gradient, not the PSF. The craft has **one** background-to-hull
silhouette on f2600, x ≈ 948–1022 (75 columns). The longest clean span anywhere in the
segment is 168 px, and f2600 offers 74 px, so two cuts 150 px apart do not exist.

1. **Keep f2600**, the published frame, preserving the D33 comparison.
2. **Approved σ per codec = the 84th percentile of the per-column σ distribution** pooled
   over that single clean edge (n ≈ 75). Strictly more data than two cuts, and the upper
   quantile preserves the pessimistic direction of the retired rule. Location tolerance
   remains `FWHM_PER_SIGMA × approved σ`, unchanged in form. `n`, median, p16 and p84 are
   recorded in the JSON.
3. **Robustness replicate, reported not adopted:** the same pooled measurement on the
   frame selected deterministically as maximising the minimum clean span across both
   codecs. Agreement or disagreement is recorded in `notes.robustness_replicate`.
4. **Overshoot diagnostic**, read-only, run before the measurement. It gates the D33
   *interpretation* only and never the approved σ.
5. **Limitation, verbatim:** *approved sigma is measured on the single high-contrast
   silhouette step; if the chain's edge response is contrast-dependent (adaptive
   sharpening), the effective blur of faint marks may differ. Pre-specified consequence
   for the grid: a sigma-sensitivity replicate at the published 8.40 px on a small stated
   subset of cells, so the limit surface's dependence on this uncertainty is measured
   rather than argued.*
6. **Reporting language.** σ ≈ 4 is the measured effective edge response of the material
   as it stands — the correct injection blur for marks that must mimic real ones after the
   same chain. The delta against the published 8.13 / 8.40 is the D33 finding, attributed
   only as far as the diagnostics carry: tilt-smear ruled out (+1.0 % with alignment
   removed), mixed-edge ruled out (gradient-boundary columns give σ 5.006, all columns
   pooled 4.080 — nothing averages to 8.13), source/encoder sharpening live, and
   candidate 4 open, since the published method is code-less (C2) and "craft top edge,
   two cuts" may denote an edge, frame region or rise convention not identified here.

The `PIN_TOL_AV1` fixture in `selftest.py` is a published-figures regression anchor and is
**expected to differ** from the production tolerance under D48. That divergence is the
finding; it must not be reconciled by editing either value toward the other.

### D47 — per-codec σ plumbing

`measure_psf.py` writes `psf_av1.json` and `psf_avc.json`. `run_grid.py` loads **exactly
one** PSF file for its codec and takes the single approved σ from it. That same
codec-specific σ is passed to `crop_domain`, `TemplateBank`, `placement_mask` and
`inject` — one source per codec, no literals downstream.

Every trial record must include: **codec, measured σ, measured FWHM, location tolerance,
`bank.polarity`, trial polarity**. The runner must assert `bank.polarity == trial_polarity`
before calling `detect()` — the runner-level mirror of crop parity.

The `8.13` and `8.40` literals in `selftest.py` remain **pinned AV1 regression fixtures
only** and are commented as such. They are not a production PSF source; no runner,
grid script or calibration step may read a PSF value from that file.

### Crop parity

The cropped search domain is derived from the **clean** frame and is identical for
injected, calibration-null and evaluation-null trials. A false-positive rate is only valid
for the statistics of the region it was measured on. Enforced structurally: `detect()`
takes `domain` as a required argument and never computes one. The trap is real and is
demonstrated in the suite — a dark injection lowers luma, and a mask derived from the
injected frame loses 833 search pixels relative to the clean-frame mask.

### N3′ — the null population is the unit population

N3 originally specified nulls at 2× the injected trial count. Not implementable. A null is
`detect()` on a **clean** unit with that unit's domain and the stratum's bank — no
injection, no seeded site — so it is a deterministic function of (unit, domain, bank). Two
nulls on one unit return the same margin bit for bit. "8640 nulls" would have been 8640
records holding at most 347 distinct values, inflating apparent *n* about 25× and making
every Wilson interval far too narrow.

1. A single-frame null **unit is a unique frame**; one unit, one null result.
2. Repeated injected trials landing on that frame **reference** its null result; they
   never duplicate it into the pool.
3. Counts and every Wilson CI use **unique units only**.
4. `thresholds_<codec>.json` carries the **full** calibration id list, not a sample.
5. Lag-1 autocorrelation of the frame-ordered null margin series is computed and
   reported, with `n_eff = n(1−r₁)/(1+r₁)` when material. Consecutive frames of one shot
   are not independent, so 347 units are not automatically 347 independent samples.
6. Deviations from N2/N10 are logged here rather than left in the runner.

### A1 — the stacked stratum is descriptive, with no threshold

f2571–2917 holds exactly **six** non-overlapping 50-frame windows. A calibrated 5 % FP
threshold with Wilson evaluation is not supportable on that: fitting a 95th percentile
from ~4 calibration units is meaningless, and a 0/2 evaluation gives an interval of about
[0, 0.6], which excludes nothing. Stride-5 windows would be a fiction — adjacent windows
share 45 of 50 frames.

So the stacked stratum is **descriptive**. All six independent windows form one comparison
range; `split_of()` refuses a stacked unit; no threshold is fitted. `run_grid` reports each
stacked injected margin as **above / inside / below** that range. The claim is explicitly
weaker: an ordinal comparison against six clean stacks — no detection rate, no p(detect),
no FP rate, no CI. **n = 6 is reported everywhere; n = 60 never appears.**

This answers the substrate question behind the mkfigs-vs-mk5 discrepancy — 120 px / 35 DN
missed on a single frame against 70 px / 35 DN "clearly visible" on a 50-frame stack —
without pretending to a precision the segment cannot support.

### Item D — the finite-sample threshold rule

Stated against the frozen decision path in `detect.is_detection`, where a detection is
`margin >= threshold`. **No library quantile and no interpolation default**: those differ
between implementations and would silently move the threshold off the data.

> The **smallest** calibration margin `t` such that `#{cal >= t} / n_cal <= 0.05`.

Candidates are the observed margins themselves, scanned ascending, so `t` is always a
realised value. Ties are resolved by the rule rather than arbitrarily — every calibration
margin equal to `t` counts toward the exceedance, and the count is recorded. `n_cal`, the
selected rank, the threshold, exceedances at/above and ties at threshold all go into
`thresholds_<codec>.json`; evaluation is untouched and reports realised FP separately.

If ties at the top are so heavy that no observed margin reaches the target, the rule
**raises** rather than thresholding above the data — a threshold above every observed null
gives FP = 0 on calibration and says nothing about evaluation, which is the false comfort
the rule exists to prevent. With continuous margins this cannot occur; if it does, the null
distribution is degenerate and that is the finding.

### N21′ — runtime and incremental records

Per codec: 1047 nulls + 4650 injected = 5697 `detect()` calls; **11,394 across both
codecs**, ≈ 0.79 s each, so roughly **2.5 h** plus a one-off ~10 min planning step and
frame IO. The earlier 6–8 h estimate assumed 8640 nulls per codec under the uncorrected
N3, most of which would have been duplicates.

Trial and null records are written **incrementally** — one JSON object per line, flushed
after each — so an interruption loses minutes, not hours. Reruns skip completed work by id
and, because every site is fixed in `plan.json` from a recorded seed, a resumed run is
identical to an uninterrupted one.

### S1–S3 — corrections found in review

- **S1 (blocker).** Stacked injected units are drawn from the **six independent
  non-overlapping windows**, not from arbitrary starts. As originally written ~98 % of
  stacked trials would have had no paired null and `assert_crop_parity` would have raised
  mid-run, after the headline arm had already spent hours. It also strengthens A1:
  injections land on the very units whose clean margins define the comparison range.
- **S2.** `grid_<codec>.jsonl` gets the same treatment as the null files — repair a torn
  tail at write time before appending, and a strict `_done_ids` that raises on an
  unparseable line instead of swallowing it. Silent swallowing would let a resumed run
  re-execute trials whose records were lost, or skip trials whose records were mangled,
  with neither showing up anywhere.
- **S3.** The completeness assertion is **symmetric set equality**. Missing units mean a
  partial run; unexpected units mean the file was written under a different unit
  definition — a changed segment, a changed stack length, or a stale file left in place.
  Both are fatal. That assertion, not JSON parse success, is what stops a partial run
  masquerading as a complete one.

**Review provenance.** The N3′ / A–D / S1–S3 corrections were externally reviewed in three
parts — human review (D28 codec-key rejection, wildcard-approval and gate discipline), ChatGPT
(hash() process-salt warning behind the SHA-256 split, the tail-repair debate resolved as
repair-at-resume, the intersection-site strengthening, the finite-sample rank rule
sequencing), and Claude (line-by-line verification, S1–S3 findings). No correction was
applied without explicit approval.

## Calibration results — measured 2026-08-10

`calibrate.py` run for both codecs: 1047 nulls each across four strata (347 × 3 single +
6 stacked). Exit 0, **no `REPAIR` lines on stderr** — no torn tails, no resume repair.
Calibration realised FP is 8/170 = 0.0471 in every single-frame stratum, so the item-D rule
selected identically throughout: rank 163, 8 at/above, 1 tie.

**AV1** — approved σ 4.5725 px, tolerance 10.7673 px

| stratum | threshold | eval FP | Wilson95 nominal | Wilson95 on n_eff | r₁ | n_eff |
|---|---:|---:|---|---|---:|---:|
| single_dark_approved | 6.1942 | **0.0791** (14/177) | [0.0477, 0.1284] | [0.0207, 0.4468] | 0.9068 | 8.7 |
| single_bright_approved | 6.6075 | 0.0282 (5/177) | [0.0121, 0.0644] | [0.0000, 0.2765] | 0.8925 | 10.1 |
| single_dark_published_8.40 | 4.9984 | 0.0452 (8/177) | [0.0231, 0.0866] | [0.0000, 0.4214] | 0.9421 | 5.3 |
| stacked_dark_approved | none | — | — | — | — | n = 6 |

**AVC** — approved σ 4.4324 px, tolerance 10.4376 px

| stratum | threshold | eval FP | Wilson95 nominal | Wilson95 on n_eff | r₁ | n_eff |
|---|---:|---:|---|---|---:|---:|
| single_dark_approved | 6.1740 | **0.0734** (13/177) | [0.0434, 0.1216] | [0.0170, 0.3905] | 0.8881 | 10.5 |
| single_bright_approved | 6.6062 | 0.0621 (11/177) | [0.0351, 0.1078] | [0.0157, 0.3688] | 0.8795 | 11.3 |
| single_dark_published_8.40 | 4.9952 | 0.0565 (10/177) | [0.0310, 0.1009] | [0.0000, 0.3732] | 0.9296 | 6.5 |
| stacked_dark_approved | none | — | — | — | — | n = 6 |

Stacked margin ranges over the six independent windows, no threshold fitted (A1):
**AV1 [1.4703, 3.3604]**, median 2.4404; **AVC [1.5157, 3.3048]**, median 2.3968.

### The ruling — option (a), report as measured

The preregistered null definition, the SHA-256 split and the fitted thresholds are all
**frozen**. Nothing is redefined after seeing evaluation results.

Two alternatives were considered and **rejected as post-hoc**, because each would have
changed the experiment in response to its own outcome:

- **(b) redefine the null unit for independence** — temporally spaced frames only, trading
  count for independence.
- **(c) block split instead of hash split** — contiguous calibration and evaluation blocks
  so the two sets are temporally separated.

Both remain **notable as future robustness tracks**, to be preregistered and run as their
own exercise. Neither may be applied to this calibration.

### Autocorrelation — the nominal intervals are far too narrow

Lag-1 autocorrelation of the frame-ordered null margin series is **r₁ = 0.88–0.94** in
every single-frame stratum, `material = True` throughout. Effective sample size is
**n_eff = 5.3–11.3**, against a nominal n = 177. The 347 units carry roughly 3–6 % of the
information their count implies, because consecutive frames of one shot are near-duplicates.

Stated plainly: **the nominal Wilson intervals are too narrow by a factor of 4.8–6.6 in
width.** Every FP figure above is therefore given twice, and the effective-n interval is
the one that governs. (The "≈ 4×" shorthand used while this was being discussed understates
it; the measured range is larger.)

### Consequence for D31

**D31 is unchanged: p(detect) ≥ 0.80 AND FP ≤ 0.05.** Where held-out FP ≤ 0.05 is **not
demonstrated, no formal D31 detection limit may be claimed.**

On the headline `single_dark_approved` stratum it is not demonstrated — **0.0791 (AV1)**
and **0.0734 (AVC)**, both above target, with effective-n lower bounds of 0.0207 and 0.0170
and upper bounds beyond 0.39. Calibration realised 0.0471 and evaluation drifted to 0.079
and 0.073; the drift is not one-directional across strata (AV1 bright drifts −0.019), which
is consistent with threshold instability at n_eff ≈ 9 rather than a systematic bias.

### What the primary deliverable now is

The grid may still run under the frozen detector and produce a **descriptive sensitivity
surface**, with the realised FP and the n_eff limitation attached to every figure. But the
primary AV1-vs-AVC comparison therefore carries a descriptive surface rather than a formal
detection limit, and that is a **materially weaker deliverable than the design promised**.
It should be stated that way in the report, not only here.

The paired-margin comparison under the frozen detector still answers the substrate question
behind the mkfigs-vs-mk5 discrepancy — identical cells, identical seeds, identical frames
and identical injection sites across the two codecs (D28), so margins are directly
comparable even where no rate can be certified. That is a **complement to the weakened
deliverable, not compensation for it**: it answers a different question, and it does not
restore the detection limit.

### Pre-grid declarations — recorded 2026-08-10, before any grid run

1. **Every FP figure ships with both intervals**, nominal and effective-n, with the
   effective-n interval governing. A bare nominal interval is not to be quoted.
2. **No D31 claim on the headline stratum.** Any sensitivity surface derived from it is
   labelled descriptive, and the phrase "detection limit" is not used of it.
3. **Threshold sensitivity of the 0.80 contour**, recomputed from the stored raw margins,
   is **presentation analysis and never refitting**. Margins are recorded per trial
   precisely so the contour can be re-drawn at other thresholds without re-running; doing
   so does not license adopting a different threshold, and the frozen thresholds above
   remain the ones the analysis is reported against.

4. **Flagged cells are run but not necessarily plotted.** All trials run regardless of
   flags, and every cell is reported with k/n, realised n and both flags.

*As originally declared, a cell flagged on **either** `realised n < 10` **or**
`realised fraction < 0.5` was excluded from surface and contour construction and labelled
"insufficient n — not estimated". That was amended pre-outcome, before any margin existed,
to exclude on `n < 10` only. The original wording is kept here rather than overwritten,
on the same principle as D43 and D46.*

**Pre-outcome amendment to declaration 4, locked before any margin existed:**

> `realised_n < 10` excludes a cell from contour construction. `realised_fraction < 0.5`
> remains a MANDATORY coverage/population-shift flag but does not by itself exclude the
> cell.

*Rationale.* The two flags answer different questions. `n < 10` is a **precision**
problem: a p̂ on single-digit n is too unstable to position a contour. `frac < 0.5` is a
**coverage** problem: a smaller, size-selected frame population. A coverage warning must
not act as a precision test. Applied to the realised table this keeps the 140 px column
(n = 27–42) in the surface while flagging it, and excludes exactly three cells —
`sigma_sens` 100 px/35 DN (n = 9) and both 140 px σ = 8.40 cells (n = 3 and n = 4) —
labelled **"insufficient n — not estimated"** in the figures.

## Placement coverage and the estimand — recorded 2026-08-10

The plan realised **2501 of 4650 trials (0.538)**; the other **2149 are recorded skips**,
where the drawn frame offered no legal placement at that size. Every frame in the segment
has a hull that survives the 140 DN threshold — calibration would have raised otherwise —
but many do not survive erosion by the template support (43 px at 40 px size, 93 px at
140 px). The skip rule was pre-specified: record invalid, never silently fall back.

**Crossvalidation.** Executed and skipped counts per (arm, size, contrast, sigma_mode)
match `plan.json`'s `cell_summary` exactly in both codecs across all 47 cells, with no
cell present in a grid file and absent from the plan.

### The estimand

The surface estimates

> **P(detect | a legal site exists for this size on this frame)**

and **the conditioning set differs by size.** This is conditional on legal placement *by
construction* — it is the estimand, not a bias. But it means the 140 px column is not "the
same experiment with fewer trials"; it is a different conditioning set.

### The population shift

Larger sizes can only be placed on thick-hull frames, so **the frame population differs
across sizes** and cross-size comparisons carry a population shift:

| size | realised / planned (headline) | fraction |
|---|---|---:|
| 40 px | 548 / 720 | 0.761 |
| 60 px | 481 / 720 | 0.668 |
| 80 px | 436 / 720 | 0.606 |
| 100 px | 388 / 720 | 0.539 |
| 120 px | 314 / 720 | 0.436 |
| 140 px | 207 / 720 | 0.288 |

19 of 47 cells carry the coverage flag; 3 carry the precision flag.

### Intersection coverage

Sites are drawn from the intersection of both codecs' placement masks (D28), so the
intersection size is a property of the trial, not of the encode — the figures below are
identical for AV1 and AVC. Over the 2501 realised trials: min **1 px**, median 8923, max
359,804.

| intersection | trials | share |
|---|---:|---:|
| < 10 px | 22 | 0.88 % |
| < 100 px | 103 | 4.12 % |
| < 1000 px | 397 | 15.87 % |

A one-pixel intersection is legal under the rules but leaves the site no positional
freedom. These are not excluded — no such rule was pre-registered — but the counts are
recorded so a reader can see how thin the tail is.

### Stacked coverage

Both stacked cells realised **10 of 30**. Motion averaging shrinks the bright-hull area
that survives the 140 DN threshold, so a stack-mean hull is **smaller** than a single
frame's, and the 50-frame windows are correspondingly harder to place on. A1 is ordinal
per trial and is unaffected by this, but **n = 10 is not to be over-read**.

### Figure requirement

Every figure or table showing flagged cells carries **realised n, planned n and realised
fraction**, plus the caveat that **larger sizes sample a restricted thick-hull
population**.

### Options considered and rejected

Recorded so the choice is visible rather than implied. Option 1, accept and report
realised n per cell, was taken.

- **(2) Redraw conditioned on usability** — reject a drawn frame if that cell's
  intersection is empty and redraw from the seed. Rejected: it keeps n = 30 but makes the
  frame population depend on size, so cells would no longer be sampled from a common
  population, and D28 pairing would need re-deriving.
- **(3) Restrict the segment** to frames with a workable hull at every size. Rejected: it
  shrinks the population and changes what "across the segment" means, which is exactly
  what N20 option (a) was chosen to avoid.
- **(4) Loosen the clearance rule** so a star may sit nearer the hull edge with partial
  overlap. Rejected: D23 requires the full template support inside the mask, and changing
  it after seeing the coverage would be a post-hoc design change; it would need its own
  pre-registration.

## Results — Arm 1, both codecs

Produced by `run_grid.py` at `2b9247c` against the frozen thresholds of `1a8f1cb`; raw
records committed at `e2739a9`. **Direct measurements, derived statistics and
interpretation are kept separate below and are labelled as such.**

Realised n is identical in both codecs by construction — the plan is codec-neutral and
D28 pairing is exact — so a single n column serves both.

### A. Headline detection fractions — DIRECT + DERIVED

**Direct:** k/n among executed injected trials. **Derived:** the two intervals.
Cell entries read `k/n = fraction [nominal Wilson95] / [conservative n_eff Wilson95]`.
`cov` is realised/planned; **†** marks `realised_fraction < 0.5`, a mandatory coverage
flag that is **not** an exclusion.

| size | DN | n | cov | AV1 | AVC |
|---|---:|---:|---:|---|---|
| 40 px | 4 | 94 | 0.783 | 0/94 = 0.000 [0.000, 0.039] / [0.000, 0.455] | 0/94 = 0.000 [0.000, 0.039] / [0.000, 0.408] |
| 40 px | 8 | 99 | 0.825 | 0/99 = 0.000 [0.000, 0.037] / [0.000, 0.442] | 0/99 = 0.000 [0.000, 0.037] / [0.000, 0.396] |
| 40 px | 16 | 85 | 0.708 | 0/85 = 0.000 [0.000, 0.043] / [0.000, 0.480] | 0/85 = 0.000 [0.000, 0.043] / [0.000, 0.433] |
| 40 px | 24 | 94 | 0.783 | 0/94 = 0.000 [0.000, 0.039] / [0.000, 0.455] | 0/94 = 0.000 [0.000, 0.039] / [0.000, 0.408] |
| 40 px | 35 | 90 | 0.750 | 0/90 = 0.000 [0.000, 0.041] / [0.000, 0.466] | 0/90 = 0.000 [0.000, 0.041] / [0.000, 0.419] |
| 40 px | 50 | 86 | 0.717 | 0/86 = 0.000 [0.000, 0.043] / [0.000, 0.477] | 0/86 = 0.000 [0.000, 0.043] / [0.000, 0.430] |
| 60 px | 4 | 81 | 0.675 | 0/81 = 0.000 [0.000, 0.045] / [0.000, 0.492] | 0/81 = 0.000 [0.000, 0.045] / [0.000, 0.444] |
| 60 px | 8 | 87 | 0.725 | 0/87 = 0.000 [0.000, 0.042] / [0.000, 0.475] | 0/87 = 0.000 [0.000, 0.042] / [0.000, 0.427] |
| 60 px | 16 | 73 | 0.608 | 0/73 = 0.000 [0.000, 0.050] / [0.000, 0.518] | 0/73 = 0.000 [0.000, 0.050] / [0.000, 0.470] |
| 60 px | 24 | 77 | 0.642 | 0/77 = 0.000 [0.000, 0.048] / [0.000, 0.505] | 0/77 = 0.000 [0.000, 0.048] / [0.000, 0.457] |
| 60 px | 35 | 88 | 0.733 | 0/88 = 0.000 [0.000, 0.042] / [0.000, 0.472] | 0/88 = 0.000 [0.000, 0.042] / [0.000, 0.424] |
| 60 px | 50 | 75 | 0.625 | 0/75 = 0.000 [0.000, 0.049] / [0.000, 0.512] | 0/75 = 0.000 [0.000, 0.049] / [0.000, 0.464] |
| 80 px | 4 | 64 | 0.533 | 0/64 = 0.000 [0.000, 0.057] / [0.000, 0.551] | 0/64 = 0.000 [0.000, 0.057] / [0.000, 0.503] |
| 80 px | 8 | 74 | 0.617 | 0/74 = 0.000 [0.000, 0.049] / [0.000, 0.515] | 0/74 = 0.000 [0.000, 0.049] / [0.000, 0.467] |
| 80 px | 16 | 79 | 0.658 | 0/79 = 0.000 [0.000, 0.046] / [0.000, 0.499] | 0/79 = 0.000 [0.000, 0.046] / [0.000, 0.451] |
| 80 px | 24 | 67 | 0.558 | 0/67 = 0.000 [0.000, 0.054] / [0.000, 0.540] | 0/67 = 0.000 [0.000, 0.054] / [0.000, 0.492] |
| 80 px | 35 | 80 | 0.667 | 1/80 = 0.013 [0.002, 0.067] / [0.000, 0.496] | 1/80 = 0.013 [0.002, 0.067] / [0.000, 0.448] |
| 80 px | 50 | 72 | 0.600 | 5/72 = 0.069 [0.030, 0.152] / [0.000, 0.522] | 14/72 = 0.194 [0.120, 0.300] / [0.043, 0.678] |
| 100 px | 4 | 74 | 0.617 | 0/74 = 0.000 [0.000, 0.049] / [0.000, 0.515] | 0/74 = 0.000 [0.000, 0.049] / [0.000, 0.467] |
| 100 px | 8 | 52 | 0.433 † | 0/52 = 0.000 [0.000, 0.069] / [0.000, 0.602] | 0/52 = 0.000 [0.000, 0.069] / [0.000, 0.555] |
| 100 px | 16 | 55 | 0.458 † | 11/55 = 0.200 [0.116, 0.324] / [0.069, 0.826] | 16/55 = 0.291 [0.188, 0.421] / [0.056, 0.766] |
| 100 px | 24 | 70 | 0.583 | 49/70 = 0.700 [0.585, 0.795] / [0.179, 0.901] | 55/70 = 0.786 [0.676, 0.866] / [0.287, 0.944] |
| 100 px | 35 | 72 | 0.600 | 69/72 = 0.958 [0.885, 0.986] / [0.353, 0.984] | 70/72 = 0.972 [0.904, 0.992] / [0.464, 0.996] |
| 100 px | 50 | 65 | 0.542 | 60/65 = 0.923 [0.832, 0.967] / [0.404, 0.998] | 61/65 = 0.938 [0.852, 0.976] / [0.540, 0.998] |
| 120 px | 4 | 58 | 0.483 † | 0/58 = 0.000 [0.000, 0.062] / [0.000, 0.575] | 0/58 = 0.000 [0.000, 0.062] / [0.000, 0.528] |
| 120 px | 8 | 46 | 0.383 † | 6/46 = 0.130 [0.061, 0.257] / [0.000, 0.631] | 8/46 = 0.174 [0.091, 0.307] / [0.000, 0.585] |
| 120 px | 16 | 60 | 0.500 | 53/60 = 0.883 [0.778, 0.942] / [0.453, 1.000] | 54/60 = 0.900 [0.799, 0.953] / [0.348, 0.982] |
| 120 px | 24 | 46 | 0.383 † | 43/46 = 0.935 [0.825, 0.978] / [0.294, 0.994] | 45/46 = 0.978 [0.887, 0.996] / [0.507, 0.992] |
| 120 px | 35 | 62 | 0.517 | 62/62 = 1.000 [0.942, 1.000] / [0.432, 1.000] | 62/62 = 1.000 [0.942, 1.000] / [0.584, 0.991] |
| 120 px | 50 | 42 | 0.350 † | 42/42 = 1.000 [0.916, 1.000] / [0.331, 1.000] | 42/42 = 1.000 [0.916, 1.000] / [0.259, 0.979] |
| 140 px | 4 | 42 | 0.350 † | 2/42 = 0.048 [0.013, 0.158] / [0.000, 0.652] | 1/42 = 0.024 [0.004, 0.123] / [0.000, 0.607] |
| 140 px | 8 | 31 | 0.258 † | 18/31 = 0.581 [0.408, 0.736] / [0.128, 0.962] | 19/31 = 0.613 [0.438, 0.763] / [0.104, 0.925] |
| 140 px | 16 | 40 | 0.333 † | 40/40 = 1.000 [0.912, 1.000] / [0.353, 1.000] | 40/40 = 1.000 [0.912, 1.000] / [0.275, 0.987] |
| 140 px | 24 | 36 | 0.300 † | 36/36 = 1.000 [0.904, 1.000] / [0.410, 0.990] | 36/36 = 1.000 [0.904, 1.000] / [0.314, 0.998] |
| 140 px | 35 | 27 | 0.225 † | 27/27 = 1.000 [0.875, 1.000] / [0.149, 0.982] | 27/27 = 1.000 [0.875, 1.000] / [0.476, 0.965] |
| 140 px | 50 | 31 | 0.258 † | 31/31 = 1.000 [0.890, 1.000] / [0.525, 0.939] | 31/31 = 1.000 [0.890, 1.000] / [0.385, 0.996] |

The **0.80 contour of the descriptive sensitivity surface**¹ lies between 100 px / 24 DN
and 100 px / 35 DN, and is already crossed at 120 px / 16 DN.

> ¹ **Not a D31 detection limit.** Held-out FP ≤ 0.05 was **not demonstrated** on this
> stratum — realised 0.0791 (AV1) and 0.0734 (AVC). Read with the realised-FP and n_eff
> caveats in §E, per the pre-grid declarations. The term "detection limit" is not used of
> this stratum.

### Bright replicate (D24) and σ-sensitivity replicate (D48(5)) — DIRECT + DERIVED

| arm | size | DN | n | cov | AV1 | AVC |
|---|---|---:|---:|---:|---|---|
| bright | 60 px | 35 | 19 | 0.633 | 0/19 = 0.000 [0.000, 0.168] / [0.000, 0.781] | 0/19 = 0.000 [0.000, 0.168] / [0.000, 0.759] |
| bright | 100 px | 35 | 16 | 0.533 | 11/16 = 0.688 [0.444, 0.858] / [0.207, 1.000] | 14/16 = 0.875 [0.640, 0.965] / [0.200, 1.000] |
| bright | 140 px | 35 | 12 | 0.400 † | 12/12 = 1.000 [0.758, 1.000] / [0.207, 1.000] | 12/12 = 1.000 [0.758, 1.000] / [0.207, 1.000] |
| sigma_sens | 60 px | 16 | 15 | 0.500 | 0/15 = 0.000 [0.000, 0.204] / [0.000, 0.793] | 0/15 = 0.000 [0.000, 0.204] / [0.000, 0.793] |
| sigma_sens | 60 px | 35 | 14 | 0.467 † | 0/14 = 0.000 [0.000, 0.215] / [0.000, 0.793] | 0/14 = 0.000 [0.000, 0.215] / [0.000, 0.793] |
| sigma_sens | 100 px | 16 | 15 | 0.500 | 0/15 = 0.000 [0.000, 0.204] / [0.000, 0.793] | 0/15 = 0.000 [0.000, 0.204] / [0.000, 0.793] |
| sigma_sens | 100 px | 35 | 9 | 0.300 † | **insufficient n — not estimated** (0/9) | **insufficient n — not estimated** (0/9) |
| sigma_sens | 140 px | 16 | 3 | 0.100 † | **insufficient n — not estimated** (3/3) | **insufficient n — not estimated** (1/3) |
| sigma_sens | 140 px | 35 | 4 | 0.133 † | **insufficient n — not estimated** (4/4) | **insufficient n — not estimated** (4/4) |

The three excluded `sigma_sens` cells remain visible above rather than omitted, per
declaration 4 as amended.

### B. Empirical headline findings — DIRECT

- **Exact zero detection at 40 px and 60 px, at every contrast through 50 DN, in both
  codecs.** Ten cells, 0/94 through 0/75. Nominal upper bounds run 0.037–0.050.
- Detection first appears at 80 px / 35 DN (1/80) and 80 px / 50 DN (5/72 AV1, 14/72 AVC).
- **120 px / 35 DN is 62/62 in both codecs**, as is every 140 px cell at ≥ 16 DN.
- **The previous 120 px / 35 DN miss is not reproduced by the corrected detector; the same
  nominal cell is detected in 62/62 trials in both codecs. This is consistent with the
  previously identified polarity defect being consequential.** No exclusive causal
  attribution is made: the injection σ, the decision statistic, the crop domain and the
  threshold all differ from the historical figure as well.
- **σ-sensitivity (D48(5)): at the published σ = 8.40, every estimable cell at ≤ 100 px is
  zero detections** — 0/15, 0/14, 0/15. The three low-n cells remain **not estimated**.
  The replicate cannot bracket the σ uncertainty as designed, because σ = 8.40 enlarges
  the template support enough to make placement itself fail at the sizes that mattered.

### C. Stacked replicate (A1) — DIRECT, ORDINAL ONLY

Position of each injected margin relative to the margin range of the six independent
non-overlapping clean stack windows. **No detection fraction and no calibrated
false-positive rate is computed for this stratum.**

| cell | AV1 | AVC |
|---|---|---|
| 70 px / 35 DN | above 9, inside 1, below 0 | above 10, inside 0, below 0 |
| 120 px / 35 DN | above 10, inside 0, below 0 | above 10, inside 0, below 0 |

**39 of 40 injected stacked margins fall above the six-window clean range.** n = 6
independent windows; 10 realised trials per cell. Not to be over-read.

### D. Paired AV1-vs-AVC margin — DIRECT + DERIVED

Same trial, same frame, same site, same seed (D28). AVC margin minus AV1 margin.

| subset | n | mean | median | sd | p10 | p90 | frac > 0 |
|---|---:|---:|---:|---:|---:|---:|---:|
| all executed | 2501 | +0.1280 | +0.0740 | 0.3444 | -0.1978 | +0.5766 | 0.637 |
| headline | 2374 | +0.1270 | +0.0740 | 0.3479 | -0.2112 | +0.5822 | 0.636 |
| bright | 47 | +0.2112 | +0.1569 | 0.2953 | -0.1032 | +0.6036 | 0.723 |
| sigma_sens | 60 | +0.0390 | -0.0043 | 0.2395 | -0.1498 | +0.3461 | 0.467 |
| stacked | 20 | +0.3226 | +0.3322 | 0.0894 | +0.2357 | +0.4488 | 1.000 |
| headline 40 px | 548 | +0.0434 | +0.0145 | 0.3090 | -0.2670 | +0.4211 | 0.527 |
| headline 60 px | 481 | +0.0576 | +0.0238 | 0.3073 | -0.1879 | +0.4353 | 0.557 |
| headline 80 px | 436 | +0.0961 | +0.0696 | 0.3038 | -0.1927 | +0.4786 | 0.633 |
| headline 100 px | 388 | +0.2177 | +0.1909 | 0.3426 | -0.1737 | +0.6570 | 0.758 |
| headline 120 px | 314 | +0.2316 | +0.2105 | 0.3893 | -0.1976 | +0.7070 | 0.739 |
| headline 140 px | 207 | +0.2456 | +0.2340 | 0.4405 | -0.2588 | +0.8142 | 0.734 |

**Measured finding.** The AVC-minus-AV1 margin is positive on average and **grows with
size**, from about **+0.043 at 40 px to +0.246 at 140 px**; the stacked subset is positive
on **20 of 20** paired trials.

This is recorded as a **finding candidate — a paired-margin signal**. It is **not** a
conclusion about a codec mechanism.

**Instrument caveat.** Pairing controls frame, site and seed exactly, but **not complete
instrument identity**: each codec uses its own measured σ (4.5725 vs 4.4324), and therefore
its own template bank, its own placement clearance and its own crop domain. The two
headline thresholds are near-identical — 6.1942 (AV1) against 6.1740 (AVC) — which
**supports scale similarity between the two instruments but does not prove they are
identical**.

*Interpretation, not measurement:* a higher-bitrate encode preserving more of the injected
signal is one explanation among others for the size-growing gap. It is offered as an
alternative explanation only, and nothing here establishes it.

### E. False-positive and dependence limitations

- **Calibration remained frozen throughout.** No post-hoc refit, no re-split, no unit
  redefinition. Option (a) as ruled.
- **Held-out headline FP: 0.0791 (AV1), 0.0734 (AVC)** — above the 0.05 target.
- **Severe temporal autocorrelation** in the consecutive null-frame series: r₁ = 0.88–0.94,
  giving n_eff 5.3–11.3 against a nominal 177, so the nominal Wilson intervals on the FP
  rates are too narrow by a factor of 4.8–6.6 in width.
- **The n_eff intervals in §A are a conservative bound of uncertain applicability, not a
  like-for-like injected-trial effective sample size.** They transfer the null-series r₁,
  measured on consecutive frames, onto injected trials drawn scattered across the segment.
  A cell's trials sit on nearly as many distinct frames as it has trials, so this transfer
  is likely far too harsh. **No proper injected-trial n_eff is claimed**; deriving one
  would be separate work.
- **D31 is unchanged and unmet as a formal ≤ 5 % FP criterion on the headline stratum.**

### F. Coverage and estimand limitations

- Detection fractions are **conditional on legal D23 placement**: the estimand is
  P(detect | a legal site exists for this size on this frame).
- **Larger sizes sample a more restricted thick-hull frame population** — realisation falls
  from 0.761 at 40 px to 0.288 at 140 px — so cross-size comparisons carry a population
  shift.
- **`realised_fraction < 0.5` is a mandatory coverage flag, not an exclusion** (19 of 47
  cells).
- **`realised_n < 10` is the contour exclusion criterion** (3 cells, all `sigma_sens`).
- **Stacked coverage:** motion averaging shrinks the bright-hull area surviving the 140 DN
  threshold, so stack-mean hulls are smaller than single frames' — 10 of 30 realised at
  both stacked cells.

## Hygiene notes for the report

- **C2 — `analysis/mk5-colour-segment/` ships figures, not code.** The directory contains
  six PNGs and zero `.py` files. No tracked code anywhere in the repo produces the
  matched-filter survey (§2.1), the hull SNR table (§2.2), the 70 px injection (§2.3) or
  the PSF measurement (§4) of `reports/agent_mk5_claims.md`. Those numbers survive only as
  report text and must be rebuilt, not re-run. This is **not** a sparse-checkout artefact:
  the files are absent from the tracked tree, not merely unmaterialised.
- **C6 — `reports/agent_vision_readjudication.md` does not exist.** Indexed at
  `reports/INDEX.md:79` as "the source of several retractions in `CORRECTIONS.md`", but
  present on no ref (`git log --all` returns nothing), and `reports/` is fully inside the
  sparse cone, so this is real absence. Consequence: the "5/5 frames return 'no markings'
  with a null option offered" of `FINDINGS.md:286` has **no primary source** — observer
  count, prompt wording, frame selection and clean-room conditions are all unrecoverable.
  The prior null cannot be matched, only replaced. Three other indexed reports are
  likewise absent: `agent_community_lc.md`, `agent_openitems_audit.md`,
  `agent_record_integrity.md`.
- **D39 — interpreter.** `AGENTS.md` says `python3.12`, not `python3`. On this machine the
  system `python3.12` has **no numpy**; the pinned environment is `.venv/bin/python`
  (3.12.13, numpy 2.4.6 / pillow 12.3.0 / scipy 1.18.0 / opencv 5.0.0). Everything here
  must be run with the venv interpreter.
- **Injection-window mean: 178.2 DN measured, 185 DN asserted.** `mkfigs.py:204` documents
  the injection site as "the brightest 120 px window on the hull (mean 185 DN)". Measured
  directly on `frames/OpSTlDJWFFI/f02683.png`, the 120 px window centred on (1290, 550)
  has **mean 178.16 DN** (AV1) and **178.38 DN** (AVC) — a 3.7 % overstate, i.e. the
  published best-case site was slightly less favourable than described. Logged under D33
  (rebuild vs published) alongside the PSF and dome-floor figures.

## Self-test observations, not results

These are **one-frame self-test observations** on a single fixture (`OpSTlDJWFFI` f2683,
AV1, one injection site, 120 px at 35 DN nominal, dark). They are recorded so the
implementation gate is auditable. **They are not a detection-power result and must not be
generalised into one before calibration and the grid have run.**

| quantity | value |
|---|---:|
| injected margin | **6.8413** |
| null maximum margin | **4.3838** |
| injected historical specificity | **1.0639** |
| null historical specificity | **0.8498** |

Both historical specificity values fall **within** the previously published
null-material range (mean 0.952, σ 0.058, max 1.191 — `agent_mk5_claims.md:72`), so on
that measure the injected star does not separate from star-free material. The **margin**
did separate this particular null/injected fixture. One fixture is not a rate: no
p(detect), no false-positive rate and no detection limit follows from it.
