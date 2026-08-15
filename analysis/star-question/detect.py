"""Matched-filter detector for Arm 1 (D7, D8, D9).

Half-resolution, locally normalised, sweeping scales, with star6 and disc run as
controls against star5. The decision statistic is the MARGIN r5 - max(r6, rd), not the
bare star5 response and not the specificity ratio -- see MARGIN VS RATIO below for why
the ratio was tried, why it failed, and what the published specificity number actually
measured. A bare star5 response fires on any bright blob, which is what produced the
published "top-ranked candidates" that turned out to be the craft
(agent_mk5_claims.md:72).

CROP PARITY -- the condition attached to the runtime crop
------------------------------------------------------------------------------
The FFT search is cropped to the hull bounding box plus margin, which cuts the run from
~5.3 h/codec to ~1.3 h/codec. A false-positive rate is only valid for the statistics of
the region it was measured on, so the calibration nulls, the evaluation nulls and the
injected trials must all run on the IDENTICAL cropped domain. Two consequences, both
enforced structurally rather than by convention:

  1. The domain is derived from the CLEAN frame, never an injected one. A dark injection
     lowers luma; a threshold-derived hull mask taken from the injected frame would
     shrink relative to the null's, giving the two arms different search regions and
     biasing the FP rate in the direction that flatters detection. detect() therefore
     takes `domain` as a required argument and has no path to compute one itself.

  2. The domain depends only on the clean frame and on the LARGEST template in the scale
     sweep -- never on the injected size. The detector does not know the injected size
     (it sweeps all scales), so one domain serves every cell on that frame, and injected
     and null trials at every cell share it exactly.

selftest.test_crop_parity asserts both, including that deriving the domain from the
injected frame really does differ -- so the trap stays visible if anyone rewires this.

MARGIN VS RATIO -- amends D7, approved
------------------------------------------------------------------------------
D7 specified the statistic as the specificity ratio star5 / max(star6, disc). Built as a
per-pixel quotient that is numerically unusable: matched-filter responses are signed, so
wherever the control response approaches zero the quotient diverges, and the argmax lands
on the pixel with the smallest control response rather than on any star. Measured on
f2683 it returned 2.9e6 at a fixed location, identical for injected and null frames --
a detector completely insensitive to the injection.

Re-reading agent_mk5_claims.md:63-72, the published ratio is not a per-pixel map: it is
peak star5 divided by peak max(star6, disc), two independent maxima per (frame x scale)
cell. It summarises a region; it does not localise, and D9 needs a location.

So the decision statistic here is the MARGIN

    D(x) = r5(x) - max(r6(x), rd(x))

evaluated per pixel over the search mask.

The margin is finite and localisable, unlike the per-pixel quotient. Raw margin
distributions may differ across scales because the real image data are spatially
correlated and each scale maximises across multiple templates. Therefore no
scale-comparability claim is assumed analytically. The final decision statistic is the
maximum margin over the complete pre-specified scale/rotation sweep, and its threshold is
calibrated empirically on the disjoint null-calibration set using the identical cropped
domain. The held-out null-evaluation set reports the resulting false-positive rate and
Wilson CI.

The published-style scalar specificity is retained only as a historical comparison
measure against the 0.952 baseline (D33). It is not part of the decision rule.

POLARITY -- corrects a defect, not a design change
------------------------------------------------------------------------------
Templates are rendered as positive-amplitude shapes. The headline injections of D24 are
dark (mkfigs.py:216-217 subtracts). Correlating a bright template against a dark feature
returns a large NEGATIVE response, so the argmax lands anywhere except the star: measured
on f2683, the injected site ranked 59,739th of 59,740 pixels in the domain.

Polarity is therefore a property of the TemplateBank, applied to star5, star6 and disc
alike before the margin r5 - max(r6, rd) and the historical specificity are computed.
Negating only star5 would hand the target template a sign advantage its controls lack.

Polarity is pre-specified per run and is never inferred from pixel values. Inferring it,
or maximising over both signs, would double the null search space and inflate the
false-positive rate that the empirical calibration exists to measure.
"""
import numpy as np

import common as C

# Scale sweep in full-resolution px. Matches the injection grid (D20) and brackets the
# published survey's 24-140 px (agent_mk5_claims.md:59).
SCALES = [40, 60, 80, 100, 120, 140]

# Rotations for star5 and star6. A 5-point star has a 72 deg symmetry period, a 6-point
# star 60 deg; both are sampled at 4 steps across their own period so neither control is
# handicapped by orientation.
ROT5 = [0.0, 18.0, 36.0, 54.0]
ROT6 = [0.0, 15.0, 30.0, 45.0]

# D45 -- FROZEN. Local-normalisation window half-width, half-res px.
#
# Selected a priori at approximately 4x the half-resolution PSF FWHM: wide enough not to
# suppress a star, narrow enough to flatten the hull's shading gradient. The published
# survey says "locally-normalized" without stating a window, so this is our choice and is
# stated rather than inherited.
#
# Frozen before any calibration null is generated. It was selected before the injected-
# star outcome was evaluated and has never been varied or tuned in response to a result.
# Under polarity-corrected detection the 120 px / 35 DN fixture localises at 1.0 px
# FULL-resolution error at this value (the self-test compares result['xy_full'] against
# the full-resolution injection site). Do not tune it against grid outcomes.
NORM_HALF = 40

# D46 -- the D9 location tolerance is PER CODEC and is not defined here.
#
# "One resolution element" is that codec's measured PSF FWHM, produced by measure_psf.py
# and carried in psf_<codec>.json (D47). is_detection() takes it as a required argument;
# there is deliberately no module constant and no default, for the same reason detect()
# requires `domain` and TemplateBank requires `polarity`.
#
# Why not a fixed 20.0 px, as this held previously: a fixed tolerance is proportionally
# more generous to a sharper codec, so it would introduce codec-dependent bias in the
# direction that can flatter AVC -- the arm we are trying to test, not favour. A per-codec
# resolution-element tolerance follows D12 and applies the same physical criterion to both
# copies.
#
# Aggregation: SUPERSEDED BY D48. The rule here was originally the larger of two
# edge-spread cuts, chosen because agent_mk5_claims.md:220-222 reports two (8.13/8.40 px,
# 19.1/19.8 px) and specifies no aggregation. That rule presumed a second cut which
# measurably does not exist on f2600: above the hull mask at x 1050-1500 the image is
# already at 108-136 DN, so the 140 DN contour there runs through a smooth bright
# gradient rather than a step, and the craft has ONE background-to-hull silhouette,
# x ~ 948-1022. Requiring two cuts 150 px apart failed loud, correctly.
#
# D48 replaces it: the approved sigma per codec is the 84th percentile of the per-column
# sigma distribution pooled over that single clean edge (n ~ 75), and the location
# tolerance stays FWHM_PER_SIGMA x the approved sigma -- unchanged in form, so there is
# still one measurement with one provenance. The upper quantile preserves the pessimistic
# direction of the retired larger-of-two rule in the sense FINDINGS.md:23-27 requires:
# more blur means a harder detection and a floor that overstates rather than understates
# how blind we were.
#
# measure_psf.py is the authority; this comment records why the rule changed, not what it
# is. See analysis/star-question/README.md, D46 and D48.
FWHM_PER_SIGMA = 2.0 * np.sqrt(2.0 * np.log(2.0))       # 2.35482; 2.3548*8.13 = 19.15,
                                                        # 2.3548*8.40 = 19.78, matching
                                                        # the published 19.1 / 19.8


def crop_domain(clean_luma, sigma_full, thr=140.0):
    """Compute the shared search domain for every trial on one clean frame.

    `clean_luma` MUST be the unmodified frame. Returns a dict carrying the half-res
    crop box, the search mask inside it, and a fingerprint used to assert parity.

    The margin accommodates the largest template in SCALES plus the normalisation
    window, so responses inside the search mask are never computed against padding.
    """
    sigma_half = sigma_full / 2.0
    search_full = C.hull_mask(clean_luma, thr)
    if not search_full.any():
        raise ValueError('empty hull mask: threshold failed on this frame')

    half = C.halve(clean_luma)
    search = C.halve(search_full.astype(np.float64)) > 0.5

    ys, xs = np.nonzero(search)
    max_hw = max(int(np.ceil((s / 2.0) / 2.0)) + int(np.ceil(3.0 * sigma_half))
                 for s in SCALES)
    pad = max_hw + NORM_HALF
    y0 = max(0, int(ys.min()) - pad)
    y1 = min(half.shape[0], int(ys.max()) + pad + 1)
    x0 = max(0, int(xs.min()) - pad)
    x1 = min(half.shape[1], int(xs.max()) + pad + 1)

    return dict(box=(y0, y1, x0, x1),
                search=search[y0:y1, x0:x1].copy(),
                sigma_half=sigma_half,
                pad=pad,
                n_search=int(search.sum()),
                fingerprint=(y0, y1, x0, x1, int(search.sum())))


class TemplateBank:
    """Templates for the whole sweep, built once. Depends on sigma and polarity only, so
    one bank serves every frame of a codec at one polarity.

    Sharing a bank across injected and null trials guarantees they share a polarity, the
    same way sharing a `domain` guarantees crop parity. polarity=-1 is the dark headline
    grid (D24); polarity=+1 is the bright replicate.

    polarity is required and has no default, for the same reason detect() requires
    `domain`: a hypothesis that can be silently wrong will eventually be silently wrong.
    """

    def __init__(self, sigma_full, polarity):
        if polarity not in (-1, +1):
            raise ValueError('polarity must be -1 (dark) or +1 (bright)')
        self.sigma_half = sigma_full / 2.0
        self.polarity = polarity
        self.t = {}
        p = float(polarity)
        for s in SCALES:
            sh = s / 2.0
            self.t[(s, 'star5')] = [p * C.make_template('star5', sh, self.sigma_half, r) for r in ROT5]
            self.t[(s, 'star6')] = [p * C.make_template('star6', sh, self.sigma_half, r) for r in ROT6]
            self.t[(s, 'disc')] = [p * C.make_template('disc', sh, self.sigma_half, 0.0)]


def detect(luma, domain, bank):
    """Run the detector on one full-resolution frame over a pre-computed domain.

    `luma` may be injected or clean; `domain` must have come from the clean frame
    (see CROP PARITY above); `bank` carries the polarity hypothesis (see POLARITY above).
    Returns the peak margin, its full-resolution location, and the winning scale.
    """
    y0, y1, x0, x1 = domain['box']
    half = C.halve(luma)[y0:y1, x0:x1]
    norm = C.local_normalize(half, NORM_HALF)
    search = domain['search']

    best = dict(margin=-np.inf, xy_full=None, scale=None, star5=None, ctrl=None)
    per_scale = {}
    for s in SCALES:
        r5 = np.maximum.reduce([C.xcorr(norm, t) for t in bank.t[(s, 'star5')]])
        r6 = np.maximum.reduce([C.xcorr(norm, t) for t in bank.t[(s, 'star6')]])
        rd = np.maximum.reduce([C.xcorr(norm, t) for t in bank.t[(s, 'disc')]])
        ctrl = np.maximum(r6, rd)

        # The decision statistic (see MARGIN VS RATIO above): a signed difference of
        # matched-filter responses, well defined everywhere.
        margin = np.where(search, r5 - ctrl, -np.inf)
        py, px = np.unravel_index(np.argmax(margin), margin.shape)
        v = float(margin[py, px])

        # The published-style scalar, reported alongside for comparability with the
        # 0.952 baseline: peak star5 over the region divided by peak control over the
        # region. Two independent maxima, exactly as agent_mk5_claims.md:63-72 tabulates
        # them -- not a per-pixel quotient.
        s5_max = float(np.where(search, r5, -np.inf).max())
        ct_max = float(np.where(search, ctrl, -np.inf).max())
        per_scale[s] = dict(margin=v,
                            star5_max=s5_max,
                            ctrl_max=ct_max,
                            specificity=s5_max / ct_max if ct_max > 0 else float('nan'))
        if v > best['margin']:
            best = dict(margin=v,
                        xy_full=((x0 + px) * 2.0, (y0 + py) * 2.0),
                        scale=s,
                        star5=float(r5[py, px]),
                        ctrl=float(ctrl[py, px]))
    best['per_scale'] = per_scale
    best['specificity'] = per_scale[best['scale']]['specificity']
    return best


def is_detection(result, site_full, threshold, location_tol_full):
    """D9: a detection requires BOTH the margin clearing threshold AND the peak landing
    within one resolution element of the seeded site. Position-blind peak counting is
    how a blob detector manufactures a hit rate.

    `location_tol_full` is required and per codec (D46): the larger measured FWHM from
    that codec's psf_<codec>.json. No default is offered, for the same reason detect()
    requires `domain` and TemplateBank requires `polarity`.

    The decision path reads result['margin'] and nothing else. The specificity scalar is
    a historical comparison measure only and must never enter here.
    """
    if result['margin'] < threshold:
        return False
    if site_full is None:
        return True                       # null trial: threshold alone defines an FP
    dx = result['xy_full'][0] - site_full[0]
    dy = result['xy_full'][1] - site_full[1]
    return float(np.hypot(dx, dy)) <= location_tol_full
