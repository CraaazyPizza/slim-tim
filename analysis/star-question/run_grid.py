"""Injected-trial grid for Arm 1 (D20-D28, D42, D44, D47, D48(5), A1, N7-N21').

    .venv/bin/python analysis/star-question/run_grid.py --plan        # once, codec-neutral
    .venv/bin/python analysis/star-question/run_grid.py av1 [--only headline]
    .venv/bin/python analysis/star-question/run_grid.py avc [--only headline]

Writes plan.json once, then grid_<codec>.jsonl incrementally -- one JSON object per
trial, flushed after each (N21'). An interruption loses minutes. Rerunning skips trials
already present by trial_id, and because every site is fixed in the plan the resumed run
is identical to an uninterrupted one.

Reads sigma and the location tolerance from psf_<codec>.json ONLY (D47/N7) and thresholds
from thresholds_<codec>.json. No literal sigma in this file. Never imports selftest,
whose 8.13/8.40 are pinned regression fixtures (N9).

D28 -- THE EXPERIMENTAL KEY IS CODEC-INDEPENDENT
==============================================================================
AV1 and AVC injected trials must use identical cells, identical seeds and identical frame
indices, so the codec does not enter the RNG namespace. trial_key() is
(MASTER_SEED, arm, size, contrast, rotation, k) and nothing else. Codec appears only in
trial_id and in the output record, where it labels a trial without changing what the
trial is. calibrate.SPLIT_SEED is a separate namespace for null membership (N6); it may
not be used here and MASTER_SEED may not be used there.

Explicit entropy rather than SeedSequence.spawn(): a spawned child records only its spawn
index, so reconstructing from that index alone loses the parent entropy and every cell's
trial k would draw the same site.

THE SITE IS DRAWN ONCE, CODEC-NEUTRALLY, FROM THE MASK INTERSECTION
==============================================================================
--plan loads both codecs' clean frames, intersects the two placement masks and records
site_xy in plan.json; each codec run then reads the site rather than recomputing it.
Recomputing per codec per trial would reload both codecs 18,600 times across the two runs
and could diverge.

The site is drawn UNIFORMLY over the intersection: the SITE stream indexes the nonzero
pixel list. Nearest-legal snapping is rejected -- it concentrates draws on whichever mask
boundary faces each target and is not uniform over legal sites. Indexing is sound here,
unlike the per-codec case, because the intersection is one array shared by both codecs.

The two placement masks differ ONLY because the 140 DN hull threshold falls on different
pixel values between the codecs. The erosion radius is byte-identical in both: with
sigma 4.5725 and 4.4324, max(1, ceil(5*sigma)) is 23 either way.

Cost of exact pairing: neither codec is sampled over its own full legal-site population.
Both mask sizes and the intersection size are recorded per trial so the exclusion is
auditable rather than invisible.

GUARDS THAT FAIL LOUD (N12)
==============================================================================
  assert_polarity      -- bank.polarity == trial polarity, the runner-level mirror of D44
  assert_crop_parity   -- the injected domain fingerprint equals the paired null's, so
                          the FP rate and the detection rate are measured on one region
Both are module-level functions so selftest can exercise them without running a trial.

SIGMA MISMATCH IS RECORDED, NOT AVOIDED (N20)
==============================================================================
Approved sigma is measured on f2600 alone, but trials draw frames across f2571-2917 where
sigma varies by at least 1 px (the f2846 replicate sits +1.01 px above f2600 in both
codecs). Option (a): draw across the whole segment and record the mismatch per trial.
Every record carries psf_frame and the unit, so any trial's distance from the frame sigma
was measured on is auditable. The bound is what the D48(5) arm measures.
"""
import json
import os
import sys

import numpy as np

import common as C
import detect as D
import calibrate as CAL

MASTER_SEED = 20260803             # experimental design ONLY; see calibrate.SPLIT_SEED
STREAM_FRAME, STREAM_SITE = 0, 1
ARM_ID = dict(headline=1, bright=2, stacked=3, sigma_sens=4)

SIZES = [40, 60, 80, 100, 120, 140]                 # D20
CONTRASTS = [4.0, 8.0, 16.0, 24.0, 35.0, 50.0]      # D21
ROTATIONS = [0.0, 18.0, 36.0, 54.0]                 # D22, 72 deg symmetry / 4
N_TRIALS = 30                                       # D25
DARK, BRIGHT = CAL.DARK, CAL.BRIGHT

BRIGHT_CELLS = [(60, 35.0, 0.0), (100, 35.0, 0.0), (140, 35.0, 0.0)]     # D24
STACK_CELLS = [(70, 35.0, 0.0), (120, 35.0, 0.0)]                        # A1
SIGMA_SENS_CELLS = [(60, 16.0, 0.0), (60, 35.0, 0.0),                    # D48(5)
                    (100, 16.0, 0.0), (100, 35.0, 0.0),
                    (140, 16.0, 0.0), (140, 35.0, 0.0)]

PLAN_PATH = os.path.join(C.HERE, 'plan.json')

# S1/A1: stacked injected trials draw from the SAME six independent non-overlapping
# windows that form the null comparison range -- the FRAME stream indexes 0..5. Drawing an
# arbitrary window start would leave ~98 % of stacked trials with no paired null, so
# assert_crop_parity would raise mid-run; and it would compare injected margins against
# clean margins measured on different units. Injecting into the very units whose clean
# margins define the range is what makes the A1 ordinal comparison meaningful.
STACK_UNITS = CAL.null_units('stacked')


# ---------------------------------------------------------------- keys and streams


def trial_key(arm, size, contrast, rot, k):
    """D28: codec-independent. See the module docstring."""
    return [MASTER_SEED, ARM_ID[arm], int(size),
            int(round(contrast * 10)), int(round(rot)), int(k)]


def stream(key, which):
    """Named independent substreams off one trial key, so the frame draw and the site
    draw cannot collide."""
    return np.random.default_rng(np.random.SeedSequence(list(key) + [which]))


def trial_uid(arm, size, contrast, rot, polarity, sigma_mode, k):
    return '%s:%d:%g:%g:%d:%s:%d' % (arm, size, contrast, rot, polarity, sigma_mode, k)


# ---------------------------------------------------------------- guards (N12)


def assert_polarity(bank, trial_polarity, tid):
    if int(bank.polarity) != int(trial_polarity):
        raise RuntimeError('polarity mismatch on %s: bank %d, trial %d (D44/N12)'
                           % (tid, bank.polarity, trial_polarity))
    return True


def assert_crop_parity(domain, null_rec, tid):
    if null_rec is None:
        raise RuntimeError('no paired null for %s: crop parity cannot be checked, and an '
                           'unpaired trial would put the detection rate and the FP rate '
                           'on different regions (N12)' % tid)
    if list(domain['fingerprint']) != list(null_rec['domain_fingerprint']):
        raise RuntimeError('crop parity broken on %s: injected %s, null %s (N12)'
                           % (tid, list(domain['fingerprint']),
                              list(null_rec['domain_fingerprint'])))
    return True


# ---------------------------------------------------------------- planning


def _cells():
    for s in SIZES:
        for ct in CONTRASTS:
            for r in ROTATIONS:
                yield ('headline', s, ct, r, DARK, 'single', 'approved')
    for (s, ct, r) in BRIGHT_CELLS:
        yield ('bright', s, ct, r, BRIGHT, 'single', 'approved')
    for (s, ct, r) in STACK_CELLS:
        yield ('stacked', s, ct, r, DARK, 'stacked', 'approved')
    for (s, ct, r) in SIGMA_SENS_CELLS:
        yield ('sigma_sens', s, ct, r, DARK, 'single', 'published_8.40')


def build_plan():
    """Codec-neutral planning step. Loads both codecs' clean units, intersects their
    placement masks, and fixes one site per trial. Cached by (unit_id, size, sigma_mode)
    so each unit is loaded once per codec, not once per trial."""
    psf = {c: CAL.load_psf(c) for c in ('av1', 'avc')}
    lo, hi = C.SEGMENT
    luma_cache, mask_cache = {}, {}
    plan = []

    def luma(codec, unit):
        k = (codec, CAL.unit_id(unit))
        if k not in luma_cache:
            luma_cache[k] = CAL.unit_luma(codec, unit)
        return luma_cache[k]

    def inter_mask(unit, size, sigma_mode):
        k = (CAL.unit_id(unit), size, sigma_mode)
        if k not in mask_cache:
            ma = C.placement_mask(luma('av1', unit), size,
                                  CAL.sigma_for(psf['av1'], sigma_mode)[0])
            mb = C.placement_mask(luma('avc', unit), size,
                                  CAL.sigma_for(psf['avc'], sigma_mode)[0])
            mask_cache[k] = (ma, mb, ma & mb)
        return mask_cache[k]

    for (arm, size, ct, rot, pol, substrate, smode) in _cells():
        for k in range(N_TRIALS):
            key = trial_key(arm, size, ct, rot, k)
            rng = stream(key, STREAM_FRAME)
            if substrate == 'single':
                unit = dict(kind='single', frame=int(rng.integers(lo, hi + 1)))
            else:
                unit = dict(STACK_UNITS[int(rng.integers(len(STACK_UNITS)))])   # S1

            ma, mb, inter = inter_mask(unit, size, smode)
            ys, xs = np.nonzero(inter)
            if len(ys) == 0:
                site = None
            else:
                j = int(stream(key, STREAM_SITE).integers(len(ys)))
                site = [int(xs[j]), int(ys[j])]

            plan.append(dict(
                trial_uid=trial_uid(arm, size, ct, rot, pol, smode, k),
                arm=arm, size_px=size, contrast_nominal_dn=ct, rotation_deg=rot,
                trial_polarity=pol, substrate=substrate, sigma_mode=smode,
                unit=unit, unit_id=CAL.unit_id(unit), seed_key=key,
                site_xy=site,
                legal_sites_av1=int(ma.sum()), legal_sites_avc=int(mb.sum()),
                legal_sites_intersection=int(inter.sum())))
        print('  planned %s %d px %g DN %g deg (%d trials)' % (arm, size, ct, rot, N_TRIALS),
              flush=True)

    out = dict(schema='star-question/plan/1', master_seed=MASTER_SEED,
               n_trials=len(plan),
               sigma_used=dict((c, {'approved': psf[c]['sigma'],
                                     'published_8.40': CAL.PUBLISHED_SIGMA})
                               for c in ('av1', 'avc')),
               note=('codec-neutral: one site per trial drawn uniformly from the '
                     'intersection of both codecs placement masks, so AV1 and AVC inject '
                     'at exactly the same pixel'),
               trials=plan)
    with open(PLAN_PATH, 'w') as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
        fh.write('\n')
    print('-> %s (%d trials)' % (os.path.relpath(PLAN_PATH, C.ROOT), len(plan)))
    return out


def load_plan():
    if not os.path.exists(PLAN_PATH):
        raise RuntimeError('missing plan.json -- run: run_grid.py --plan')
    with open(PLAN_PATH) as fh:
        return json.load(fh)


# ---------------------------------------------------------------- execution


def _done_ids(path):
    """S2: strict, like CAL.load_nulls. The grid file gets the same Amendment-A
    treatment as the null files -- a torn tail is repaired at write time by
    CAL.repair_torn_tail before append, so an unparseable line here can only mean
    corruption or external editing and must raise. Silently swallowing it would let a
    resumed run re-execute trials whose records were lost, or skip trials whose records
    were mangled, without either showing up anywhere."""
    if not os.path.exists(path):
        return set()
    out = set()
    with open(path) as fh:
        for i, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except ValueError as e:
                raise RuntimeError(
                    '%s line %d is not valid JSON (%s). Resume repairs a torn tail at '
                    'write time, so a bad line here means corruption or external editing.'
                    % (path, i, e))
            if 'trial_id' not in rec:
                raise RuntimeError('%s line %d has no trial_id' % (path, i))
            out.add(rec['trial_id'])
    return out


def _null_index(codec, substrate, polarity, sigma_mode):
    path = CAL.null_path(codec, substrate, polarity, sigma_mode)
    if not os.path.exists(path):
        raise RuntimeError('missing %s -- run: calibrate.py %s'
                           % (os.path.basename(path), codec))
    return {r['unit_id']: r for r in CAL.load_nulls(path, substrate=substrate)}


def run(codec, only=None):
    psf = CAL.load_psf(codec)
    tpath = os.path.join(C.HERE, 'thresholds_%s.json' % codec)
    if not os.path.exists(tpath):
        raise RuntimeError('missing %s -- run: calibrate.py %s'
                           % (os.path.basename(tpath), codec))
    with open(tpath) as fh:
        thr = json.load(fh)

    plan = load_plan()
    trials = plan['trials']
    if only:
        trials = [t for t in trials if t['arm'] == only]

    banks, nulls = {}, {}
    for (substrate, pol, smode) in CAL.STRATA:
        sigma, _ = CAL.sigma_for(psf, smode)
        banks[(substrate, pol, smode)] = D.TemplateBank(sigma, polarity=pol)
        nulls[(substrate, pol, smode)] = _null_index(codec, substrate, pol, smode)

    out = os.path.join(C.HERE, 'grid_%s.jsonl' % codec)
    CAL.repair_torn_tail(out)                                            # S2
    done = _done_ids(out)
    todo = [t for t in trials if '%s:%s' % (codec, t['trial_uid']) not in done]
    print('%s: %d trials, %d done, %d to run' % (codec, len(trials),
                                                 len(trials) - len(todo), len(todo)),
          flush=True)

    with open(out, 'a') as fh:
        for i, t in enumerate(todo):
            fh.write(json.dumps(_run_one(codec, t, psf, banks, nulls, thr)) + '\n')
            fh.flush()
            if (i + 1) % 50 == 0:
                print('  %d/%d' % (i + 1, len(todo)), flush=True)
    print('-> %s' % os.path.relpath(out, C.ROOT))


def _run_one(codec, t, psf, banks, nulls, thr):
    tid = '%s:%s' % (codec, t['trial_uid'])
    skey = (t['substrate'], t['trial_polarity'], t['sigma_mode'])
    sigma, tol = CAL.sigma_for(psf, t['sigma_mode'])
    bank = banks[skey]
    stratum = thr['strata'][CAL.stratum_name(*skey)]

    assert_polarity(bank, t['trial_polarity'], tid)                       # N12

    base = dict(trial_id=tid, trial_uid=t['trial_uid'], arm=t['arm'],
                trial_kind='injected', codec=codec, substrate=t['substrate'],
                sigma_mode=t['sigma_mode'], stratum=CAL.stratum_name(*skey),
                sigma_px=sigma, fwhm_px=sigma * D.FWHM_PER_SIGMA,
                location_tol_full_px=tol, psf_frame=psf['psf_frame'],
                unit=t['unit'], unit_id=t['unit_id'],
                sigma_measured_on_this_unit=(t['unit'].get('frame') == psf['psf_frame']),
                bank_polarity=int(bank.polarity),
                trial_polarity=int(t['trial_polarity']),
                size_px=t['size_px'], rotation_deg=t['rotation_deg'],
                contrast_nominal_dn=t['contrast_nominal_dn'],
                legal_sites_av1=t['legal_sites_av1'],
                legal_sites_avc=t['legal_sites_avc'],
                legal_sites_intersection=t['legal_sites_intersection'],
                seed_key=t['seed_key'])

    if t['site_xy'] is None:
        return dict(base, skipped='no legal site in the mask intersection')

    clean = CAL.unit_luma(codec, t['unit'])
    dom = D.crop_domain(clean, sigma)                    # from the CLEAN unit, always
    assert_crop_parity(dom, nulls[skey].get(t['unit_id']), tid)           # N12

    cx, cy = t['site_xy']
    inj = C.inject(clean, cx, cy, t['size_px'], sigma,
                   t['contrast_nominal_dn'], t['rotation_deg'], t['trial_polarity'])
    delivered = float(np.abs(inj - clean).max())         # D42/N11, measured per trial

    r = D.detect(inj, dom, bank)
    rec = dict(base, domain_fingerprint=list(dom['fingerprint']), crop_parity='ok',
               site_xy=[cx, cy], contrast_delivered_dn=delivered,
               margin=r['margin'], peak_xy=list(r['xy_full']),
               winning_scale=r['scale'], specificity=r['specificity'])

    if stratum['kind'] == 'descriptive_range':
        # A1: no threshold exists for this stratum. Ordinal position only.
        lo_m, hi_m = stratum['null_margin_min'], stratum['null_margin_max']
        rec.update(threshold_margin=None, detected=None,
                   null_range=[lo_m, hi_m], n_independent_null_windows=stratum['n_units'],
                   range_position=('above' if r['margin'] > hi_m else
                                   'below' if r['margin'] < lo_m else 'inside'),
                   claim_strength=stratum['claim_strength'])
    else:
        tm = stratum['threshold_margin']
        rec.update(threshold_margin=tm,
                   detected=bool(D.is_detection(r, (cx, cy), tm, tol)))
    return rec


def main():
    args = sys.argv[1:]
    if '--plan' in args:
        build_plan()
        return
    codec = args[0] if args else None
    if codec not in C.CODECS:
        raise SystemExit('usage: run_grid.py --plan | run_grid.py {av1|avc} '
                         '[--only headline|bright|stacked|sigma_sens]')
    only = args[args.index('--only') + 1] if '--only' in args else None
    run(codec, only)


if __name__ == '__main__':
    main()
