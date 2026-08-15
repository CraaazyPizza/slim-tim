"""Null generation and threshold calibration (N1-N6, N3', D43, A1 redesign).

    .venv/bin/python analysis/star-question/calibrate.py <codec>

Writes nulls_<codec>_<substrate>_<polarity>_<sigma_mode>.jsonl incrementally and
thresholds_<codec>.json at the end. Reads sigma and the location tolerance from
psf_<codec>.json ONLY (D47/N7). Never imports selftest, whose 8.13/8.40 are pinned
regression fixtures (N9).

N3' -- THE NULL POPULATION IS THE UNIT POPULATION
==============================================================================
N3 originally said: nulls at 2x the injected trial count. Not implementable. A null is
detect() on a CLEAN unit with that unit's domain and the stratum's bank -- no injection,
no seeded site -- so it is a deterministic function of (unit, domain, bank). Two nulls on
one unit return the same margin bit for bit. "8640 nulls" would have been 8640 records
holding at most 347 distinct values, inflating apparent n ~25x and making every Wilson
interval far too narrow.

  1. A single-frame null UNIT is a unique frame. One unit, one null result.
  2. Repeated injected trials landing on that frame REFERENCE its null result. They never
     duplicate it into the pool.
  3. Calibration/evaluation counts and every Wilson CI use UNIQUE units only.
  4. thresholds_<codec>.json carries the FULL calibration id list, not a sample.
  5. Lag-1 autocorrelation of the frame-ordered null margin series is computed and
     reported, with n_eff = n(1-r1)/(1+r1) when material. Consecutive frames of one shot
     are not independent, so 347 units are not automatically 347 independent samples.
  6. Deviations from N2/N10 are logged in the README decision log as N3'.

STRATA (N6, item 3)
==============================================================================
The threshold namespace is (codec, substrate, polarity, sigma_mode). Nothing is shared
across it. Bright never reuses a dark threshold: the bank polarity changes every response,
so the null margin distribution is a different distribution. sigma_sens never reuses an
approved-sigma threshold: sigma 8.40 changes the templates, the injection blur, the
placement clearance AND the crop domain, so its nulls run under 8.40 too.

A1 -- THE STACKED STRATUM HAS NO THRESHOLD AND NO SPLIT
==============================================================================
f2571-2917 holds exactly SIX non-overlapping 50-frame windows. A calibrated 5 % FP
threshold with Wilson evaluation is not supportable on that: fitting a 95th percentile
from ~4 calibration units is meaningless, and a 0/2 evaluation gives a Wilson interval of
about [0, 0.6], which excludes nothing. Stride-5 windows would be a fiction -- adjacent
windows share 45 of 50 frames.

So the stacked stratum is DESCRIPTIVE. All six independent windows form one comparison
range; split_of() is never called for a stacked unit; no threshold is fitted. run_grid
reports each stacked injected margin as above / inside / below that range. n = 6 is
reported everywhere. n = 60 never appears.
"""
import hashlib
import json
import os
import sys

import numpy as np

import common as C
import detect as D

SPLIT_SEED = 20260804              # cal/eval membership ONLY; see run_grid.MASTER_SEED
FP_TARGET = 0.05
STACK_LEN = 50
DARK, BRIGHT = -1, +1
PUBLISHED_SIGMA = 8.40             # D48(5) sigma-sensitivity arm
AUTOCORR_MATERIAL = 0.20

# (substrate, polarity, sigma_mode)
STRATA = [
    ('single', DARK, 'approved'),
    ('single', BRIGHT, 'approved'),
    ('single', DARK, 'published_8.40'),
    ('stacked', DARK, 'approved'),
]
DESCRIPTIVE = {('stacked', DARK, 'approved')}      # A1: range only, no threshold


def stratum_name(substrate, polarity, sigma_mode):
    return '%s_%s_%s' % (substrate, 'dark' if polarity < 0 else 'bright', sigma_mode)


# ---------------------------------------------------------------- psf plumbing (D47/N7)


def load_psf(codec):
    path = os.path.join(C.HERE, 'psf_%s.json' % codec)
    if not os.path.exists(path):
        raise RuntimeError('missing %s -- run measure_psf.py first. No runner may fall '
                           'back to a literal sigma (D47).' % os.path.basename(path))
    with open(path) as fh:
        rec = json.load(fh)
    if rec.get('codec') != codec:
        raise RuntimeError('%s declares codec %r but was loaded for %r'
                           % (path, rec.get('codec'), codec))
    d = rec['derived']
    return dict(sigma=float(d['approved_sigma_px']),
                fwhm=float(d['approved_fwhm_px']),
                tol=float(d['location_tol_full_px']),
                psf_frame=int(rec['frame']),
                source=os.path.basename(path))


def sigma_for(psf, sigma_mode):
    if sigma_mode == 'approved':
        return psf['sigma'], psf['tol']
    if sigma_mode == 'published_8.40':
        return PUBLISHED_SIGMA, PUBLISHED_SIGMA * D.FWHM_PER_SIGMA
    raise ValueError(sigma_mode)


# ---------------------------------------------------------------- statistics


def wilson(k, n, z=1.959963984540054):
    """Wilson score interval -- correct at p near 0 and 1, where the normal
    approximation is not, which is exactly where an FP rate sits."""
    if n <= 0:
        return 0.0, 0.0, 1.0
    p = k / n
    d = 1.0 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)


def lag1_autocorr(values):
    """Lag-1 autocorrelation of a frame-ordered series (N3' item 5)."""
    x = np.asarray(values, dtype=np.float64)
    if len(x) < 3:
        return 0.0
    a, b = x[:-1], x[1:]
    sa, sb = a.std(), b.std()
    if sa == 0 or sb == 0:
        return 0.0
    return float(((a - a.mean()) * (b - b.mean())).mean() / (sa * sb))


def choose_threshold(cal_margins, fp_target=FP_TARGET):
    """Pre-specified finite-sample threshold rule (item D).

    Stated against the FROZEN decision path in detect.is_detection, where a detection is
    `margin >= threshold`. No library quantile and no interpolation default: those differ
    between implementations and would silently move the threshold off the data.

    Rule: the SMALLEST calibration margin t such that #{cal >= t} / n_cal <= fp_target.
    Candidates are the observed margins themselves, scanned ascending, so t is always a
    realised value and ties are resolved by the rule rather than arbitrarily -- every
    calibration margin equal to t is counted in the exceedance, and the count is recorded.
    """
    m = np.sort(np.asarray(cal_margins, dtype=np.float64))
    n = len(m)
    if n == 0:
        raise RuntimeError('no calibration margins')
    for t in np.unique(m):
        exceed = int((m >= t).sum())
        if exceed / n <= fp_target:
            first = int(np.searchsorted(m, t, side='left'))
            return dict(threshold_margin=float(t),
                        n_calibration=n,
                        rank_ascending_1based=first + 1,
                        exceedances_at_or_above=exceed,
                        realised_calibration_fp=exceed / n,
                        ties_at_threshold=int((m == t).sum()),
                        rule=('smallest calibration margin t with '
                              '#{cal >= t}/n_cal <= %.4f; detection is margin >= t'
                              % fp_target))
    # Unreachable only when ties at the top of the distribution are so heavy that no
    # OBSERVED margin achieves the target: the smallest achievable exceedance is the
    # multiplicity of the maximum. Fail loud rather than silently thresholding above the
    # data -- a threshold above every observed null gives FP = 0 on calibration and says
    # nothing about evaluation, which is precisely the false comfort this rule exists to
    # prevent. With continuous margins this cannot occur; if it does, the null
    # distribution is degenerate and that is the finding.
    top = float(m.max())
    mult = int((m == top).sum())
    raise RuntimeError(
        'no OBSERVED calibration margin achieves FP <= %.4f at n=%d. The maximum margin '
        '%.6f has multiplicity %d, so the smallest achievable exceedance rate is '
        '%d/%d = %.4f. This is a tie/degeneracy in the null margin distribution, not a '
        'sample-size problem; %d samples would otherwise suffice. Report it rather than '
        'thresholding above the data.'
        % (fp_target, n, top, mult, mult, n, mult / n, int(np.ceil(1.0 / fp_target))))


# ---------------------------------------------------------------- units and membership


def null_units(substrate):
    """The null population: every distinct unit on which a clean trial can be run."""
    lo, hi = C.SEGMENT
    if substrate == 'single':
        return [dict(kind='single', frame=n) for n in range(lo, hi + 1)]
    if substrate == 'stacked':
        # A1: NON-overlapping windows only. Six of them. Never stride-5.
        return [dict(kind='stacked', frames=[s, s + STACK_LEN - 1])
                for s in range(lo, hi - STACK_LEN + 2, STACK_LEN)]
    raise ValueError(substrate)


def unit_id(unit):
    return ('single:%d' % unit['frame'] if unit['kind'] == 'single'
            else 'stacked:%d-%d' % tuple(unit['frames']))


def unit_luma(codec, unit):
    if unit['kind'] == 'single':
        return C.load_luma(codec, unit['frame'])
    a, b = unit['frames']
    return C.load_stack(codec, list(range(a, b + 1)))


def split_of(unit_id_str, substrate, seed=SPLIT_SEED):
    """Calibration/evaluation membership: a pure function of
    (SPLIT_SEED, substrate, unit_id).

    Takes NO codec, NO list length and NO count, so membership is identical in both
    codecs and unchanged if one codec skips a unit. A permutation seeded with len(ids)
    -- the earlier draft -- would have re-shuffled the whole split the moment one null
    was dropped, silently desynchronising the two arms.

    hashlib rather than hash(): Python salts string hashes per process.

    Consequence, stated: a per-unit hash is approximately balanced, not exactly 50/50.
    Realised counts are recorded rather than assumed.

    NEVER called for a stacked unit (A1): that stratum has no split.
    """
    if substrate == 'stacked':
        raise RuntimeError('split_of() must not be called for the stacked stratum: A1 '
                           'uses all six independent windows as one comparison range')
    k = ('%d|%s|%s' % (seed, substrate, unit_id_str)).encode('utf-8')
    v = int.from_bytes(hashlib.sha256(k).digest()[:8], 'big')
    return 'calibration' if (v & 1) == 0 else 'evaluation'


# ---------------------------------------------------------------- JSONL integrity


def repair_torn_tail(path):
    """Amendment A, write side: repair a half-written working record at RESUME.

    Under append-mode resume a torn tail becomes a mid-file line, so tolerating a bad
    tail at READ time is not sound -- by then it is indistinguishable from corruption in
    the middle. The invariant is therefore enforced here, at write time: if the file does
    not end in a newline, or its final line does not parse, that line is truncated before
    anything is appended and the unit is re-run immediately.

    This repairs a working record, not a report. Loud on stderr, with line number and
    byte count.
    """
    if not os.path.exists(path):
        return None
    with open(path, 'rb') as fh:
        data = fh.read()
    if not data:
        return None

    if data.endswith(b'\n'):
        end = len(data) - 1
        start = data.rfind(b'\n', 0, end) + 1
        last = data[start:end]
        if not last.strip():
            return None
        try:
            json.loads(last)
            return None
        except ValueError:
            cut = start
    else:
        cut = data.rfind(b'\n') + 1

    dropped = len(data) - cut
    lineno = data[:cut].count(b'\n') + 1
    sys.stderr.write(
        'REPAIR %s: final line %d is unparseable or torn; truncating %d byte(s) '
        'before append. The unit will be re-run and re-appended.\n'
        % (os.path.basename(path), lineno, dropped))
    sys.stderr.flush()
    with open(path, 'rb+') as fh:
        fh.truncate(cut)
    return dict(line=lineno, bytes_dropped=dropped)


def load_nulls(path, substrate=None):
    """Amendment A, read side: strict.

    After repair-at-resume, an unparseable line ANYWHERE can only mean corruption or
    external editing, so any such line raises -- including the last one. Records are
    deduped by unit_id; a duplicate whose margin disagrees raises, because a null is
    deterministic given (unit, domain, bank) and a disagreement can only mean the code or
    the data changed mid-run.

    If `substrate` is given, a COMPLETENESS assertion runs after loading: the loaded unit
    set must EQUAL null_units(substrate), checked in both directions (S3). A missing unit
    means a partial run; an unexpected unit means the file was written under a different
    unit definition -- a changed segment, a changed stack length, or a stale file left in
    place. Both are fatal, and this assertion, not JSON parse success, is what stops a
    partial run masquerading as a complete one.
    """
    seen, out = {}, []
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
            uid = rec['unit_id']
            if uid in seen:
                if seen[uid]['margin'] != rec['margin']:
                    raise RuntimeError(
                        '%s: unit %s appears twice with different margins (%r vs %r). A '
                        'null is deterministic given unit/domain/bank, so the code or the '
                        'data changed mid-run.'
                        % (path, uid, seen[uid]['margin'], rec['margin']))
                continue
            seen[uid] = rec
            out.append(rec)

    if substrate is not None:
        want = {unit_id(u) for u in null_units(substrate)}
        have = set(seen)
        missing = sorted(want - have)
        unexpected = sorted(have - want)
        if missing or unexpected:
            parts = []
            if missing:
                parts.append('%d of %d units MISSING (first 10: %s)'
                             % (len(missing), len(want), missing[:10]))
            if unexpected:
                parts.append('%d UNEXPECTED units present that are not in '
                             'null_units(%r) (first 10: %s) -- the file was written under '
                             'a different unit definition (changed segment, changed stack '
                             'length, or a stale file left in place)'
                             % (len(unexpected), substrate, unexpected[:10]))
            raise RuntimeError(
                '%s fails the completeness assertion: %s. The loaded unit set must EQUAL '
                'null_units(%r) in both directions. A partial or mismatched null set must '
                'never be calibrated on.' % (path, '; '.join(parts), substrate))
    return out


# ---------------------------------------------------------------- run


def null_path(codec, substrate, polarity, sigma_mode):
    return os.path.join(C.HERE, 'nulls_%s_%s.jsonl'
                        % (codec, stratum_name(substrate, polarity, sigma_mode)))


def run_nulls(codec, substrate, polarity, sigma_mode, psf):
    sigma, tol = sigma_for(psf, sigma_mode)
    bank = D.TemplateBank(sigma, polarity=polarity)
    path = null_path(codec, substrate, polarity, sigma_mode)

    repaired = repair_torn_tail(path)
    done = set()
    if os.path.exists(path):
        for r in load_nulls(path):
            done.add(r['unit_id'])

    units = null_units(substrate)
    with open(path, 'a') as fh:
        for i, u in enumerate(units):
            uid = unit_id(u)
            if uid in done:
                continue
            luma = unit_luma(codec, u)
            try:
                dom = D.crop_domain(luma, sigma)
            except ValueError as e:
                raise RuntimeError('%s %s: %s -- a null unit with no hull mask cannot be '
                                   'silently dropped, it would break completeness'
                                   % (codec, uid, e))
            r = D.detect(luma, dom, bank)
            fh.write(json.dumps(dict(
                unit_id=uid, unit=u, substrate=substrate, codec=codec,
                trial_kind='null', sigma_mode=sigma_mode,
                bank_polarity=int(bank.polarity),
                sigma_px=sigma, location_tol_full_px=tol,
                domain_fingerprint=list(dom['fingerprint']),
                margin=r['margin'], peak_xy=list(r['xy_full']),
                winning_scale=r['scale'], specificity=r['specificity'])) + '\n')
            fh.flush()
            if (i + 1) % 25 == 0:
                print('    %d/%d' % (i + 1, len(units)), flush=True)
    return path, repaired


def calibrate_stratum(codec, substrate, polarity, sigma_mode, psf):
    name = stratum_name(substrate, polarity, sigma_mode)
    print('  %s ...' % name, flush=True)
    path, repaired = run_nulls(codec, substrate, polarity, sigma_mode, psf)
    recs = load_nulls(path, substrate=substrate)            # completeness enforced here
    sigma, tol = sigma_for(psf, sigma_mode)

    base = dict(stratum=name, substrate=substrate,
                polarity=int(polarity), sigma_mode=sigma_mode,
                sigma_px=sigma, location_tol_full_px=tol,
                n_units=len(recs), null_file=os.path.basename(path),
                tail_repair=repaired)

    if (substrate, polarity, sigma_mode) in DESCRIPTIVE:
        # A1: no split, no threshold. All six independent windows are the range.
        m = np.array([r['margin'] for r in recs])
        base.update(
            kind='descriptive_range',
            split='none -- A1 uses all independent windows as one comparison range',
            threshold_margin=None,
            null_margin_min=float(m.min()), null_margin_max=float(m.max()),
            null_margin_median=float(np.median(m)),
            unit_ids=sorted(r['unit_id'] for r in recs),
            claim_strength=('ORDINAL against %d independent non-overlapping windows. No '
                            'detection rate, no p(detect), no false-positive rate, no CI. '
                            'n = %d is the whole population of independent stacks in '
                            'f%d-%d.' % (len(recs), len(recs), *C.SEGMENT)))
        print('    n=%d (independent windows)  margin range [%.4f, %.4f]  -- no threshold'
              % (len(recs), m.min(), m.max()))
        return base

    cal = [r for r in recs if split_of(r['unit_id'], substrate) == 'calibration']
    ev = [r for r in recs if split_of(r['unit_id'], substrate) == 'evaluation']
    sel = choose_threshold([r['margin'] for r in cal])
    thr = sel['threshold_margin']

    ev_m = np.array([r['margin'] for r in ev])
    k = int((ev_m >= thr).sum())
    p, lo, hi = wilson(k, len(ev_m))

    ordered = [r['margin'] for r in sorted(recs, key=lambda r: r['unit_id'])]
    if substrate == 'single':
        ordered = [r['margin'] for r in sorted(recs, key=lambda r: r['unit']['frame'])]
    r1 = lag1_autocorr(ordered)
    n_eff = len(ev_m) * (1 - r1) / (1 + r1) if abs(r1) < 1 else float(len(ev_m))

    base.update(
        kind='calibrated_threshold',
        split_seed=SPLIT_SEED, fp_target=FP_TARGET,
        n_calibration=len(cal), n_evaluation=len(ev),
        threshold_selection=sel, threshold_margin=thr,
        calibration_unit_ids=sorted(r['unit_id'] for r in cal),   # N3' item 4: FULL list
        evaluation_false_positives=k,
        evaluation_fp_rate=p, evaluation_fp_wilson95=[lo, hi],
        lag1_autocorrelation=r1,
        autocorrelation_material=bool(abs(r1) >= AUTOCORR_MATERIAL),
        effective_n_evaluation=float(n_eff),
        effective_n_note=(
            'consecutive frames of one shot are not independent; n_eff = n(1-r1)/(1+r1) '
            '= %.1f against nominal n = %d. Read the FP interval as the weaker of the two.'
            % (n_eff, len(ev_m)) if abs(r1) >= AUTOCORR_MATERIAL else
            'lag-1 autocorrelation %.4f is below the %.2f materiality bar; nominal n stands'
            % (r1, AUTOCORR_MATERIAL)))
    print('    n=%d  cal=%d eval=%d  threshold %.4f (rank %d, %d at/above, %d ties)'
          % (len(recs), len(cal), len(ev), thr, sel['rank_ascending_1based'],
             sel['exceedances_at_or_above'], sel['ties_at_threshold']))
    print('    eval FP %d/%d = %.4f  Wilson95 [%.4f, %.4f]  lag1 r=%.4f  n_eff=%.1f'
          % (k, len(ev_m), p, lo, hi, r1, n_eff))
    return base


def main():
    codec = sys.argv[1] if len(sys.argv) > 1 else None
    if codec not in C.CODECS:
        raise SystemExit('usage: calibrate.py {av1|avc}')
    psf = load_psf(codec)
    print('%s: approved sigma %.4f px, tol %.4f px, from %s (measured on f%d)'
          % (codec, psf['sigma'], psf['tol'], psf['source'], psf['psf_frame']))

    out = dict(schema='star-question/thresholds/2', codec=codec,
               approved_sigma_px=psf['sigma'], approved_fwhm_px=psf['fwhm'],
               approved_location_tol_full_px=psf['tol'],
               published_sigma_px=PUBLISHED_SIGMA,
               psf_source=psf['source'], psf_frame=psf['psf_frame'],
               split_seed=SPLIT_SEED,
               n3_prime=('null population is the unit population; a null is deterministic '
                         'given (unit, domain, bank), so repeated injected trials '
                         'reference a unit result rather than duplicating it. Counts and '
                         'CIs use unique units only.'),
               strata={})

    for (substrate, polarity, sigma_mode) in STRATA:
        rec = calibrate_stratum(codec, substrate, polarity, sigma_mode, psf)
        out['strata'][rec['stratum']] = rec

    dst = os.path.join(C.HERE, 'thresholds_%s.json' % codec)
    with open(dst, 'w') as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
        fh.write('\n')
    print('-> %s' % os.path.relpath(dst, C.ROOT))


if __name__ == '__main__':
    main()
