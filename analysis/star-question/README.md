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
| `selftest.py` | invariants the grid depends on; expected-vs-measured printed throughout |

## Decisions log

### D42 — contrast is recorded on both axes

Contrast is injected as a **nominal pre-blur amplitude**, matching `mkfigs.py:216-217` and
keeping the published 35 DN figures directly comparable. The **delivered peak depth is
recorded per trial**, and the limit surface is reported on **both axes**. Blur attenuates
small stars, so a limit quoted in nominal DN alone is not comparable across the size axis.

> **Recompute before use.** The worked example here was 35 DN nominal delivering 34.9 DN
> at 120 px but only 21.9 DN at 40 px — computed at **σ = 8.13**, the published figure.
> Under D48 the measured σ is roughly half that, so the attenuation is markedly weaker and
> these two numbers are stale. They must be recomputed from each codec's approved σ once
> `psf_av1.json` / `psf_avc.json` clear review, and the grid must record delivered depth
> per trial regardless.

### D43 — disjoint null split

Null trials are generated at 2× and split disjointly: a **calibration** set fixes the
threshold, a held-out **evaluation** set reports the false-positive rate and its Wilson
CI. Using one set for both would be circular.

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
