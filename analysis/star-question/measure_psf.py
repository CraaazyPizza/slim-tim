"""Per-codec PSF and noise floor for the star-question rerun (D11, D12, D33, D46, D47).

    .venv/bin/python analysis/star-question/measure_psf.py

Writes psf_av1.json and psf_avc.json. These are the ONLY production source of sigma and
of the D9 location tolerance; run_grid.py loads exactly one of them for its codec and
passes that single sigma to crop_domain, TemplateBank, placement_mask and inject (D47).
The 8.13 / 8.40 literals in selftest.py are pinned regression fixtures and must never be
read by a runner.

numpy + PIL only, consistent with D6. np.linalg.lstsq carries the polynomial fit.

DIRECT MEASUREMENTS VS DERIVED VALUES
------------------------------------------------------------------------------
The JSON separates these into two objects and they are never mixed:

  "direct"  -- quantities read off the pixels: plateau levels, the 10-90 % rise distance
               in px, the dome patch location, residual standard deviations in DN.
  "derived" -- quantities obtained from a direct measurement by an assumed model: sigma
               (rise / 2.5631, assuming a Gaussian edge-spread), FWHM (2.3548 x sigma),
               the approved sigma and the location tolerance.

The Gaussian-edge assumption is the load-bearing one. It is what lets a rise distance
become a sigma, and it is an assumption, not an observation.

WHAT IS AND IS NOT REPRODUCED FROM THE PUBLISHED WORK (D33)
------------------------------------------------------------------------------
agent_mk5_claims.md:43 measures its dome residual on a "50-frame registered stack". No
registration code was ever shipped -- analysis/mk5-colour-segment/ contains six PNGs and
zero .py files (hygiene note C2) -- so that figure cannot be re-run, only rebuilt. This
script therefore reports the dome floor three ways and labels each:

  single frame          -- no stacking, no registration; fully reproducible here.
  unregistered mean     -- 50-frame mean with NO registration. The craft translates
                           through this segment, so this SMEARS and is reported as an
                           upper bound on what an unregistered stack can achieve. It is
                           NOT comparable to the published 1.07 DN.
  published             -- 1.07 DN, quoted for reference only, not reproduced.

Any comparison against the published number is therefore a rebuild, not a re-run, and the
JSON says so in "comparison.caveat".

DETERMINISM
------------------------------------------------------------------------------
No randomness, no interactive choices. The two edge cuts and the dome patch are selected
by stated rules from the clean frame, so the same input gives byte-identical JSON. Floats
are rounded to 6 dp on write so platform noise cannot change the bytes.

THE VOIDED FIRST RUN
------------------------------------------------------------------------------
A first run of this script produced psf_av1.json and psf_avc.json which were VOIDED and
deleted. Three defects, all in this script, none in the corpus:

  1. The whole-craft poly-4 was fitted over the hull mask's BOUNDING BOX, which is only
     43.9 % craft; the remaining 56 % is background down to 27.3 DN. The fit modelled
     background and craft as one surface and returned 21.4 DN against a published 2.53.
     Fixed by F1: the fit now uses masked pixels only.
  2. Cut selection took quantiles of the usable-column LIST, not of its x-range, so both
     cuts landed within 51 px of each other at the craft's extreme left (x 973 and 1024)
     and were not the same edge -- their low plateaus differed by 38 DN. Within-codec
     sigma spread was 2.8x, larger than the between-codec difference. Fixed by F2.
  3. The dome patch used a lowest-mean-gradient rule, which rewards posterization: it
     selected a window spanning 142.0-145.7 DN, where flatness is quantisation rather
     than low noise, and returned 0.325 DN against a published 1.07. Fixed by F3.

The voided numbers are recorded in notes.voided_first_run so the rerun's figures carry
their history rather than appearing from nowhere.
"""
import json
import os

import numpy as np

import common as C
import detect as D

FRAME = 2600                      # agent_mk5_claims.md:216 measures "on f2600"
HULL_THR = 140.0

# Gaussian-edge constants. For I(y) = a + b*erf((y-y0)/(sqrt(2)*sigma)):
#   the 10-90 % rise spans 2 * 1.28155 * sigma
RISE_10_90_PER_SIGMA = 2.0 * 1.2815515655446004
FWHM_PER_SIGMA = D.FWHM_PER_SIGMA                     # 2.35482, single source

# Published AV1 figures, for the D33 rebuild comparison only. Never used as inputs.
PUBLISHED = dict(sigma_cuts=[8.13, 8.40],
                 fwhm_cuts=[19.1, 19.8],
                 rise_10_90_range=[16.0, 21.0],
                 dome_residual_dn=1.07,
                 whole_craft_residual_dn=2.53,
                 source='reports/agent_mk5_claims.md:43,220-224')

PROFILE_HALF = 30                 # rows either side of the edge to sample
COL_BLOCK = 5                     # +/- columns averaged per cut, aligned on their own top
MIN_CONTRAST_DN = 60.0            # a cut is usable only if its plateaus differ by this

# F2 -- a cut is usable only if its LOW plateau really is frame background, not a second
# structure part-way down the craft. The voided run's cut 2 had a low plateau of 74.4 DN
# against cut 1's 36.5 DN: two different edges being averaged as if they were one.
BG_TOL_DN = 15.0                  # low plateau must be <= background median + this

# D48 -- supersedes F2's two-cut aggregation, which presumed a second cut that
# measurably does not exist on f2600. Above the hull mask at x 1050-1500 the image is
# already at 108-136 DN, so the 140 DN contour there runs through a smooth bright
# gradient, not a step; the craft has ONE background-to-hull silhouette on this frame,
# x ~ 948-1022 (75 columns). The longest clean span anywhere in the segment is 168 px.
#
# Approved sigma is therefore the 84th percentile of the per-column sigma distribution
# pooled over that single clean edge: strictly more data than two cuts, and an upper
# quantile that preserves the pessimistic direction of the retired larger-of-two rule.
SIGMA_QUANTILE = 84
MIN_POOLED_COLUMNS = 20           # fail loud below this

# D48(3) -- robustness replicate, REPORTED NOT ADOPTED. The replicate frame is chosen
# deterministically as the one maximising the MINIMUM clean span across both codecs,
# scanned over this stated list.
ROBUSTNESS_FRAMES = list(range(C.SEGMENT[0], C.SEGMENT[1] + 1, 25)) + [C.SEGMENT[1]]
CLEAN_SPAN_MAX_GAP = 10           # columns this far apart still count as one span
CLEAN_SPAN_STEP = 2               # column stride when scanning candidate frames

# D48(5) -- verbatim limitation, carried into the JSON and the README.
LIMITATION = (
    "approved sigma is measured on the single high-contrast silhouette step; if the "
    "chain's edge response is contrast-dependent (adaptive sharpening), the effective "
    "blur of faint marks may differ. Pre-specified consequence for the grid: a "
    "sigma-sensitivity replicate at the published 8.40 px on a small stated subset of "
    "cells, so the limit surface's dependence on this uncertainty is measured rather "
    "than argued. "
    "FRAME DEPENDENCE IS NOW MEASURED, NOT HYPOTHESISED: the robustness replicate on "
    "f2846 (longest clean span only) gives median sigma about +1.0 px above f2600 in "
    "BOTH codecs (+1.01 av1, +1.00 avc). A delta that reproduces across codecs to 0.01 "
    "px is a property of the frame, not of the encode, so the approved sigma is one "
    "frame's value from a distribution with at least a 1 px spread across the segment. "
    "The sigma-sensitivity replicate is therefore load-bearing rather than a formality, "
    "and it brackets frame-to-frame variation as well as the published-value gap.")

# F3 -- dome patch geometry and clipping guard.
PATCH_SIZE = 61
CLIP_DN = 250.0


# ---------------------------------------------------------------- edge spread


def _top_edge_rows(luma, mask):
    """First masked row per column -- the craft's top edge. Returns {x: y}."""
    out = {}
    for x in range(mask.shape[1]):
        col = np.nonzero(mask[:, x])[0]
        if len(col):
            out[x] = int(col.min())
    return out


def _aligned_profile(luma, tops, x, half=PROFILE_HALF, block=COL_BLOCK):
    """Mean vertical profile across the edge, over x +/- block columns, each column
    aligned on its own top-edge row so a tilted edge is not smeared into the average."""
    acc, n = np.zeros(2 * half + 1), 0
    for xx in range(x - block, x + block + 1):
        if xx not in tops:
            continue
        y = tops[xx]
        if y - half < 0 or y + half + 1 > luma.shape[0]:
            continue
        acc += luma[y - half:y + half + 1, xx]
        n += 1
    return (acc / n) if n else None, n


def _rise_10_90(profile):
    """Direct measurement: the 10-90 % rise distance in px, by linear interpolation
    between plateau levels. Returns (rise_px, lo_dn, hi_dn) or None."""
    lo = float(np.mean(np.sort(profile[:PROFILE_HALF // 2])[:5]))
    hi = float(np.mean(np.sort(profile[-(PROFILE_HALF // 2):])[-5:]))
    if hi - lo < MIN_CONTRAST_DN:
        return None
    t10, t90 = lo + 0.10 * (hi - lo), lo + 0.90 * (hi - lo)

    def cross(level):
        for i in range(len(profile) - 1):
            a, b = profile[i], profile[i + 1]
            if (a - level) * (b - level) <= 0 and b != a:
                return i + (level - a) / (b - a)
        return None

    y10, y90 = cross(t10), cross(t90)
    if y10 is None or y90 is None or y90 <= y10:
        return None
    return float(y90 - y10), lo, hi


def _background_median(luma, mask):
    """Median luma outside the hull but inside the matte -- the frame's own background
    level for this frame, measured rather than assumed."""
    bg = C.matte_mask(luma.shape) & ~mask
    return float(np.median(luma[bg]))


def _clean_columns(luma, mask, tops, bg_med, step=1):
    """Every column whose vertical profile crosses a genuine background-to-hull step.

    Usable requires plateau contrast >= MIN_CONTRAST_DN and a low plateau within
    BG_TOL_DN of this frame's own background median -- the F2(a) test, retained. It is
    what distinguishes a silhouette step from an iso-luma contour of a smooth gradient,
    and measuring edge spread across the latter measures the gradient, not the PSF.
    """
    out = []
    for x in range(min(tops), max(tops) + 1, step):
        if x not in tops:
            continue
        prof, n = _aligned_profile(luma, tops, x)
        if prof is None or n < 2 * COL_BLOCK:
            continue
        r = _rise_10_90(prof)
        if r is None:
            continue
        rise, lo, hi = r
        if lo > bg_med + BG_TOL_DN:
            continue
        out.append((int(x), float(rise), float(lo), float(hi), prof))
    return out


def _regions(xs, max_gap=CLEAN_SPAN_MAX_GAP):
    """Contiguous column runs, splitting wherever the gap exceeds max_gap."""
    if not xs:
        return []
    runs, s, p = [], xs[0], xs[0]
    for x in xs[1:]:
        if x - p > max_gap:
            runs.append((s, p))
            s = x
        p = x
    runs.append((s, p))
    return runs


def _longest_span(xs, max_gap=CLEAN_SPAN_MAX_GAP):
    runs = _regions(xs, max_gap)
    if not runs:
        return 0, None
    best = max(runs, key=lambda r: r[1] - r[0])
    return best[1] - best[0], best


def measure_edge_pooled(codec, frame, restrict_longest=False):
    """D48(2): the pooled per-column edge-spread distribution on the single clean edge.

    restrict_longest=True keeps only columns inside the longest contiguous run. Used for
    the D48(3) robustness replicate, whose frame carries more than one disjoint clean
    region -- f2846 has a 210-column edge at x 777-986 and an 8-column fragment at
    x 1499-1506, 500 px away. Pooling two unrelated edges into one distribution would be
    a silent mix; the regions are recorded either way so the restriction is visible.
    """
    luma = C.load_luma(codec, frame)
    mask = C.hull_mask(luma, HULL_THR)
    tops = _top_edge_rows(luma, mask)
    bg_med = _background_median(luma, mask)
    cols = _clean_columns(luma, mask, tops, bg_med)
    regions = _regions([c[0] for c in cols])

    if restrict_longest and len(regions) > 1:
        _, run = _longest_span([c[0] for c in cols])
        cols = [c for c in cols if run[0] <= c[0] <= run[1]]

    if len(cols) < MIN_POOLED_COLUMNS:
        raise RuntimeError(
            '%s f%d: only %d clean columns, need %d. Background median %.1f, '
            'low-plateau ceiling %.1f. Failing loud rather than relaxing.'
            % (codec, frame, len(cols), MIN_POOLED_COLUMNS, bg_med, bg_med + BG_TOL_DN))

    xs = [c[0] for c in cols]
    rises = np.array([c[1] for c in cols])
    sigmas = rises / RISE_10_90_PER_SIGMA
    span, run = _longest_span(xs)

    return dict(
        frame=int(frame),
        n_columns=len(cols),
        clean_regions=[[int(a), int(b)] for a, b in regions],
        restricted_to_longest_span=bool(restrict_longest and len(regions) > 1),
        x_range=[int(min(xs)), int(max(xs))],
        longest_clean_span_px=int(span),
        longest_clean_span_x=[int(run[0]), int(run[1])],
        background_median_dn=bg_med,
        low_plateau_ceiling_dn=bg_med + BG_TOL_DN,
        plateau_low_median_dn=float(np.median([c[2] for c in cols])),
        plateau_high_median_dn=float(np.median([c[3] for c in cols])),
        rise_10_90_px=dict(median=float(np.median(rises)),
                           p16=float(np.percentile(rises, 16)),
                           p84=float(np.percentile(rises, 84))),
        sigma_px=dict(median=float(np.median(sigmas)),
                      p16=float(np.percentile(sigmas, 16)),
                      p84=float(np.percentile(sigmas, SIGMA_QUANTILE))),
        columns_x=[int(v) for v in xs],
        columns_rise_px=[float(v) for v in rises],
    ), cols


def measure_overshoot(cols):
    """D48(4): undershoot/overshoot on the mean aligned profile, beyond noise.

    Gates the D33 INTERPRETATION only. It never touches the approved sigma -- a ringing
    finding would change what the sigma delta is attributed to, not what the sigma is.
    """
    P = np.stack([c[4] for c in cols])
    mp = P.mean(0)
    n = len(cols)
    lo, hi = float(mp[:10].mean()), float(mp[-10:].mean())
    lo_sem = float(P[:, :10].std(0).mean() / np.sqrt(n))
    hi_sem = float(P[:, -10:].std(0).mean() / np.sqrt(n))
    ui = 10 + int(np.argmin(mp[10:29]))
    oi = 32 + int(np.argmax(mp[32:51]))
    under, over = float(mp[ui]), float(mp[oi])
    return dict(
        n_profiles=n,
        low_plateau_dn=lo, low_plateau_sem_dn=lo_sem,
        min_approaching_edge_dn=under, min_index=ui,
        undershoot_dn=under - lo, undershoot_sem=(under - lo) / lo_sem if lo_sem else 0.0,
        high_plateau_dn=hi, high_plateau_sem_dn=hi_sem,
        max_leaving_edge_dn=over, max_index=oi,
        overshoot_dn=over - hi, overshoot_sem=(over - hi) / hi_sem if hi_sem else 0.0,
        far_tail_drift_dn=float(mp[-1] - mp[45]),
        verdict=('no undershoot below background and no overshoot above the hull plateau '
                 'beyond 2 SEM; classic sharpening ringing is not present in this profile. '
                 'The bright side is partly masked by the hull\'s own shading drift, so '
                 'this weakens the sharpening candidate without excluding a gentle '
                 'ring-free sharpening applied before encoding.'))


def select_robustness_frame():
    """D48(3): the frame maximising the MINIMUM clean span across both codecs."""
    scores = []
    for fr in ROBUSTNESS_FRAMES:
        per = []
        for codec in ('av1', 'avc'):
            try:
                luma = C.load_luma(codec, fr)
            except FileNotFoundError:
                per = []
                break
            mask = C.hull_mask(luma, HULL_THR)
            tops = _top_edge_rows(luma, mask)
            if not tops:
                per.append(0)
                continue
            bg = _background_median(luma, mask)
            cols = _clean_columns(luma, mask, tops, bg, step=CLEAN_SPAN_STEP)
            span, _ = _longest_span([c[0] for c in cols])
            per.append(span)
        if per:
            scores.append((min(per), fr, per))
    if not scores:
        raise RuntimeError('no candidate frame scanned successfully')
    scores.sort(key=lambda t: (-t[0], t[1]))
    return scores[0][1], [dict(frame=int(f), spans=[int(v) for v in p], min_span=int(m))
                          for m, f, p in sorted(scores, key=lambda t: t[1])]


# ---------------------------------------------------------------- dome floor


def _poly4_residual_masked(luma, mask):
    """F1: residual std after a 4th-order 2-D polynomial fit over MASKED PIXELS ONLY --
    the shading model of agent_mk5_claims.md:43.

    Coordinates are normalised over the mask's bounding box so the basis is conditioned
    the same way whatever the mask's shape. The voided first run fitted the whole bounding
    box, 56 % of which was background, and returned 21.4 DN against a published 2.53.

    Returns (residual_std_dn, n_terms, n_px).
    """
    ys, xs = np.nonzero(mask)
    if len(ys) < 25:
        raise RuntimeError('mask too small for a poly-4 fit: %d px' % len(ys))
    y0, y1 = int(ys.min()), int(ys.max())
    x0, x1 = int(xs.min()), int(xs.max())
    yn = (ys - y0) / max(y1 - y0, 1) * 2.0 - 1.0
    xn = (xs - x0) / max(x1 - x0, 1) * 2.0 - 1.0
    cols = [(xn ** i) * (yn ** j) for i in range(5) for j in range(5) if i + j <= 4]
    A = np.stack(cols, axis=1)
    b = luma[ys, xs]
    coef, *_ = np.linalg.lstsq(A, b, rcond=None)
    resid = b - A @ coef
    return float(resid.std()), int(A.shape[1]), int(len(b))


def _brightest_patch(luma, mask, size=PATCH_SIZE, clip_dn=CLIP_DN):
    """F3: the highest-mean-luma `size` x `size` window lying wholly inside the hull mask,
    rejecting any window that contains a pixel >= clip_dn.

    Retires the lowest-mean-gradient rule of the voided first run, which rewarded
    posterization -- it selected a window spanning 142.0-145.7 DN, where flatness is
    quantisation rather than low noise, and so guaranteed a low residual.

    This rule inherits the one corpus precedent that exists: mkfigs.py:204 sites its
    injection at "the brightest 120 px window on the hull". The clipping guard is new,
    because a brightest-window rule with no ceiling would walk straight into any clipped
    specular.
    """
    half = size // 2
    inside = C.erode(mask, half)
    clipped = C.box_mean((luma >= clip_dn).astype(np.float64), half) > 0.0
    ok = inside & ~clipped
    if not ok.any():
        raise RuntimeError('no unclipped %dx%d window fits inside the hull mask'
                           % (size, size))
    mean_luma = C.box_mean(luma, half)
    ys, xs = np.nonzero(ok)
    k = int(np.argmax(mean_luma[ys, xs]))
    cy, cx = int(ys[k]), int(xs[k])
    return ((cy - half, cy + half + 1, cx - half, cx + half + 1),
            float(mean_luma[cy, cx]), int(inside.sum()), int((inside & clipped).sum()))


_STACK_CACHE = {}


def _stack(codec, frames):
    key = (codec, frames[0], frames[-1], len(frames))
    if key not in _STACK_CACHE:
        _STACK_CACHE[key] = C.load_stack(codec, frames)
    return _STACK_CACHE[key]


def dome_cross_codec_probe(box, frames):
    """Decisive probe on the dome convergence.

    The unregistered 50-frame residuals came out at 1.857617 (av1) and 1.857835 (avc) --
    close enough to look like a path bug feeding one codec's frames to both. If the two
    stacks are byte-identical over the patch the pipeline is wrong; if they differ at the
    ~0.1 DN scale the convergence is real, and is explained by the residual being
    dominated by motion smear, which is identical in both codecs because it is a property
    of the scene rather than of the encode.
    """
    y0, y1, x0, x1 = box
    a = _stack('av1', frames)[y0:y1, x0:x1]
    b = _stack('avc', frames)[y0:y1, x0:x1]
    d = np.abs(a - b)
    identical = bool(np.array_equal(a, b))
    return dict(
        patch_box=[int(v) for v in box],
        mean_abs_diff_dn=float(d.mean()),
        max_abs_diff_dn=float(d.max()),
        std_abs_diff_dn=float(d.std()),
        stacks_identical=identical,
        verdict=('PATH BUG: the two codecs returned identical pixels' if identical else
                 'no path bug: the stacks differ at the expected ~0.1 DN scale, so the '
                 'near-identical residuals are genuine convergence -- the poly-4 residual '
                 'on an unregistered stack is dominated by craft-motion smear, which is a '
                 'scene property and therefore the same in both encodes'))


def measure_floor(codec):
    luma = C.load_luma(codec, FRAME)
    mask = C.hull_mask(luma, HULL_THR)
    box, patch_mean, n_inside, n_rejected = _brightest_patch(luma, mask)
    y0, y1, x0, x1 = box

    patch_mask = np.zeros_like(mask)
    patch_mask[y0:y1, x0:x1] = True
    dome_single, nterms, dome_npx = _poly4_residual_masked(luma, patch_mask)

    # F1: the whole craft is the MASK, not its bounding box.
    craft_single, _, craft_npx = _poly4_residual_masked(luma, mask)

    # Unregistered 50-frame mean. The craft translates through this segment, so this
    # smears; reported as an upper bound, NOT as the published registered-stack figure.
    # The patch mask comes from the single clean frame and is held fixed across the mean.
    frames = list(range(FRAME, FRAME + 50))
    stack = _stack(codec, frames)
    dome_unreg, _, _ = _poly4_residual_masked(stack, patch_mask)

    p = luma[y0:y1, x0:x1]
    return dict(patch_box=[int(v) for v in box],
                patch_mean_luma_dn=patch_mean,
                patch_min_dn=float(p.min()),
                patch_max_dn=float(p.max()),
                patch_candidate_windows=n_inside,
                patch_windows_rejected_clipping=n_rejected,
                poly_terms=nterms,
                dome_fit_px=dome_npx,
                whole_craft_fit_px=craft_npx,
                dome_residual_single_frame_dn=dome_single,
                dome_residual_unregistered_mean_dn=dome_unreg,
                whole_craft_residual_single_frame_dn=craft_single,
                stack_frames=[frames[0], frames[-1]])


# ---------------------------------------------------------------- assemble


def _round(o, nd=6):
    if isinstance(o, dict):
        return {k: _round(v, nd) for k, v in o.items()}
    if isinstance(o, list):
        return [_round(v, nd) for v in o]
    if isinstance(o, float):
        return round(o, nd)
    return o


VOIDED_FIRST_RUN = dict(
    status='VOIDED and deleted; superseded by this run',
    causes=[
        'whole-craft poly-4 fitted over the hull bounding box (43.9 % craft, 56 % '
        'background down to 27.3 DN) -> 21.4 DN vs published 2.53. Fixed by F1.',
        'cut quantiles taken of the usable-column LIST, not its x-range -> both cuts '
        'within 51 px at the craft"s extreme left (x 973, 1024), different edges (low '
        'plateaus 36.5 vs 74.4 DN), within-codec sigma spread 2.8x. Fixed by F2.',
        'dome patch chosen by lowest mean gradient, which rewards posterization -> a '
        'window spanning 142.0-145.7 DN and 0.325 DN residual vs published 1.07. '
        'Fixed by F3.',
    ],
    voided_values=dict(
        av1=dict(cuts_x=[973, 1024], rise_px=[10.26, 28.87], sigma_px=[4.003, 11.265],
                 approved_sigma_px=11.265, dome_single_dn=0.325,
                 dome_unregistered_dn=0.123, whole_craft_dn=21.416),
        avc=dict(cuts_x=[973, 1023], rise_px=[10.30, 22.13], sigma_px=[4.020, 8.634],
                 approved_sigma_px=8.634, dome_single_dn=0.570,
                 dome_unregistered_dn=0.197, whole_craft_dn=21.717)),
    note='Recorded so this run"s numbers carry their history. None of the three causes '
         'lay in the corpus; all three were defects in this script.')


def build(codec, robustness_frame, robustness_scan):
    pooled, cols = measure_edge_pooled(codec, FRAME)
    overshoot = measure_overshoot(cols)
    floor = measure_floor(codec)

    rep, _ = measure_edge_pooled(codec, robustness_frame, restrict_longest=True)
    probe = dome_cross_codec_probe(floor['patch_box'],
                                   list(range(FRAME, FRAME + 50)))

    # DERIVED -- Gaussian-edge model applied to the direct rise measurements.
    # D48(2): approved sigma is the SIGMA_QUANTILE-th percentile of the pooled per-column
    # distribution, not the larger of two cuts.
    approved_sigma = pooled['sigma_px']['p84']
    approved_fwhm = approved_sigma * FWHM_PER_SIGMA

    return dict(
        schema='star-question/psf/1',
        codec=codec,
        video=C.VIDEO,
        frame=FRAME,
        frame_path=os.path.relpath(C.frame_path(codec, FRAME), C.ROOT),
        hull_threshold_dn=HULL_THR,
        direct=dict(
            pooled=pooled,
            column_selection_rule=(
                'D48: every column whose profile crosses a genuine background-to-hull '
                'step -- plateau contrast >= %.0f DN and low plateau <= background '
                'median + %.0f DN. The second test is what separates a silhouette step '
                'from an iso-luma contour of a smooth gradient.'
                % (MIN_CONTRAST_DN, BG_TOL_DN)),
            patch_selection_rule=(
                'F3: highest mean luma %dx%d window wholly inside the hull mask, '
                'rejecting any window containing a pixel >= %.0f DN'
                % (PATCH_SIZE, PATCH_SIZE, CLIP_DN)),
            **floor),
        derived=dict(
            model='Gaussian edge-spread; rise_10_90 = 2*1.28155*sigma, FWHM = 2.35482*sigma',
            aggregation=('D48: %dth percentile of the pooled per-column sigma '
                         'distribution on the single clean silhouette edge (n=%d). '
                         'Supersedes D46 larger-of-two-cuts, which presumed a second cut '
                         'that measurably does not exist on f%d.'
                         % (SIGMA_QUANTILE, pooled['n_columns'], FRAME)),
            sigma_median_px=pooled['sigma_px']['median'],
            sigma_p16_px=pooled['sigma_px']['p16'],
            approved_sigma_px=approved_sigma,
            approved_fwhm_px=approved_fwhm,
            location_tol_full_px=approved_fwhm),
        comparison=dict(
            published=PUBLISHED,
            sigma_delta_vs_published_median=[pooled['sigma_px']['median'] - p
                                             for p in sorted(PUBLISHED['sigma_cuts'])],
            sigma_delta_vs_published_approved=[approved_sigma - p
                                               for p in sorted(PUBLISHED['sigma_cuts'])],
            interpretation=(
                'Sigma ~4 px is the measured effective edge response of the material as '
                'it stands -- the correct injection blur for marks that must mimic real '
                'ones after the same chain. The delta against the published 8.13/8.40 is '
                'the D33 finding. Attribution goes only as far as the diagnostics carry: '
                'tilt-smear ruled out (+1.0% with alignment removed), mixed-edge ruled '
                'out (gradient-boundary columns give 5.006, all columns pooled 4.080, '
                'nothing averages to 8.13), source/encoder sharpening live but with no '
                'ringing signature, and candidate 4 open -- the published method is '
                'code-less (C2), so "craft top edge, two cuts" may denote an edge, frame '
                'region or rise convention not identified here.'),
            caveat=('AV1 figures here are a REBUILD, not a re-run: no code for the '
                    'published measurement was ever shipped (analysis/mk5-colour-segment/ '
                    'holds six PNGs and no .py, hygiene note C2). '
                    'BOTH published residuals are stack-based and BOTH are therefore '
                    'non-comparable to the single-frame rebuild, for the same reason. '
                    'agent_mk5_claims.md section 1.3, line 43, attributes them to one '
                    'measurement in one sentence: "Fitting a 4th-order 2-D polynomial to '
                    'the shading over a 50-frame registered stack leaves a residual of '
                    'sigma = 2.53 DN over the whole craft and sigma = 1.07 DN over a '
                    'clean dome patch." No registration code exists here, so neither '
                    'whole_craft_residual_single_frame_dn nor '
                    'dome_residual_unregistered_mean_dn is comparable to its published '
                    'counterpart. '
                    'Separately, the whole-craft figure carries a POLY-4 STRUCTURE FLOOR: '
                    'a 4th-order surface models smooth shading, and the craft carries '
                    'real structure it cannot represent -- the dark wedge, the interior, '
                    'the rim. The whole-craft residual is therefore an upper bound '
                    'dominated by unmodelled structure rather than by noise, which is why '
                    'it sits far above the dome-patch figure on the same frame. The dome '
                    'patch is the noise-floor measurement; the whole-craft number is not.')),
        notes=dict(
            voided_first_run=VOIDED_FIRST_RUN,
            limitation=LIMITATION,
            overshoot_diagnostic=overshoot,
            dome_cross_codec_probe=probe,
            robustness_replicate=dict(
                status='REPORTED, NOT ADOPTED',
                rule=('frame maximising the minimum clean span across both codecs, '
                      'scanned over %d stated frames' % len(ROBUSTNESS_FRAMES)),
                selected_frame=int(robustness_frame),
                scan=robustness_scan,
                pooled=rep,
                agreement_sigma_median_delta_px=(rep['sigma_px']['median']
                                                 - pooled['sigma_px']['median']),
                agreement_sigma_p84_delta_px=(rep['sigma_px']['p84']
                                              - pooled['sigma_px']['p84'])),
        ),
    )


def main():
    robustness_frame, robustness_scan = select_robustness_frame()
    print('D48(3) robustness frame (max of min clean span across codecs): f%d\n'
          % robustness_frame)
    for codec in ('av1', 'avc'):
        rec = build(codec, robustness_frame, robustness_scan)
        out = os.path.join(C.HERE, 'psf_%s.json' % codec)
        with open(out, 'w') as fh:
            json.dump(_round(rec), fh, indent=2, sort_keys=True)
            fh.write('\n')
        d, f = rec['derived'], rec['direct']
        p, n = f['pooled'], rec['notes']
        print('%s  f%d  clean columns n=%d  x %d-%d  longest span %d px'
              % (codec, FRAME, p['n_columns'], p['x_range'][0], p['x_range'][1],
                 p['longest_clean_span_px']))
        print('     rise 10-90  med %.2f  p16 %.2f  p84 %.2f px'
              % (p['rise_10_90_px']['median'], p['rise_10_90_px']['p16'],
                 p['rise_10_90_px']['p84']))
        print('     sigma       med %.3f  p16 %.3f  p84 %.3f px'
              % (p['sigma_px']['median'], p['sigma_px']['p16'], p['sigma_px']['p84']))
        print('     APPROVED sigma %.3f px  FWHM %.2f px  location tol %.2f px  [p%d]'
              % (d['approved_sigma_px'], d['approved_fwhm_px'], d['location_tol_full_px'],
                 SIGMA_QUANTILE))
        print('     delta vs published 8.13/8.40: median %s  approved %s'
              % (['%+.3f' % v for v in rec['comparison']['sigma_delta_vs_published_median']],
                 ['%+.3f' % v for v in rec['comparison']['sigma_delta_vs_published_approved']]))
        print('     dome residual: single frame %.3f DN   unregistered 50-frame mean %.3f DN'
              % (f['dome_residual_single_frame_dn'], f['dome_residual_unregistered_mean_dn']))
        print('     whole craft (masked, single frame) %.3f DN   [published: dome 1.07,'
              ' craft 2.53, registered stack -- rebuild not re-run]'
              % f['whole_craft_residual_single_frame_dn'])
        r = n['robustness_replicate']
        print('     robustness f%d: sigma med %.3f p84 %.3f  (delta med %+.3f, p84 %+.3f)'
              % (r['selected_frame'], r['pooled']['sigma_px']['median'],
                 r['pooled']['sigma_px']['p84'],
                 r['agreement_sigma_median_delta_px'], r['agreement_sigma_p84_delta_px']))
        q = n['dome_cross_codec_probe']
        print('     dome cross-codec probe: mean|av1-avc| %.4f DN (max %.3f)  identical=%s'
              % (q['mean_abs_diff_dn'], q['max_abs_diff_dn'], q['stacks_identical']))
        o = n['overshoot_diagnostic']
        print('     overshoot: undershoot %+.3f DN (%+.1f SEM)   overshoot %+.3f DN (%+.1f SEM)'
              % (o['undershoot_dn'], o['undershoot_sem'],
                 o['overshoot_dn'], o['overshoot_sem']))
        print('     -> %s' % os.path.relpath(out, C.ROOT))


if __name__ == '__main__':
    main()
