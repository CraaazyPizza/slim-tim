#!/usr/bin/env python3.12
"""Classify the pairs from dupdetect.py, deriving the threshold from the data.

Nothing here asserts a count, a phase or a cut. The threshold is placed at the
largest relative jump in the sorted similarity distribution; the duplicate phase is
whichever phase the classified set actually concentrates in; the separation figures
are read off the two populations. Every number printed is computed from
`pairs_*.json`, so a rerun on different frames yields different numbers rather than
these ones.

This is the deciding measurement for the count disputed between
`reports/agent_video1_OpSTlDJWFFI.md` (26) and `reports/agent_mk5_claims.md` (3).
Write-up in `reports/agent_colour_duplicate_count.md`.

Usage:
    python3.12 analysis/colour-duplicate-count/classify.py
"""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PERIOD_SPACE = 12  # phases enumerated, not a claim that the period is 12


def load(copy: str) -> tuple[dict, list[dict]]:
    doc = json.loads((HERE / f"pairs_{copy}.json").read_text())
    lo, hi = doc["segment"]
    return doc, [r for r in doc["pairs"] if lo <= r["a"] and r["b"] <= hi]


def derive_threshold(seg: list[dict], key: str = "norm") -> tuple[float, int]:
    """Largest relative jump in the lower half of the sorted scores.

    Searching only the lower half keeps the cut away from the long upper tail of
    ordinary motion, where the biggest absolute jumps live and mean nothing."""
    v = np.sort(np.array([r[key] for r in seg]))
    best = (0.0, 0)
    for i in range(len(v) // 2):
        if v[i] > 0 and v[i + 1] / v[i] > best[0]:
            best = (v[i + 1] / v[i], i)
    ratio, i = best
    return float((v[i] + v[i + 1]) / 2), i + 1


def report(copy: str) -> dict:
    doc, seg = load(copy)
    thr, n_below = derive_threshold(seg)
    dups = sorted([r for r in seg if r["norm"] < thr], key=lambda r: r["a"])

    counts = np.zeros(PERIOD_SPACE, int)
    for r in dups:
        counts[r["phase"]] += 1
    dom = int(counts.argmax())

    # the two populations, split on the phase the data picked out
    inph = [r for r in seg if r["phase"] == dom]
    other = [r for r in seg if r["phase"] != dom]
    hi_in = max(r["mad_y"] for r in inph)
    lo_out = min(r["mad_y"] for r in other)
    disjoint = hi_in < lo_out

    print(f"\n{'=' * 72}\n{copy.upper()}  {doc['frame_dir']}  "
          f"f{doc['segment'][0]}-{doc['segment'][1]}  ({len(seg)} pairs)\n{'=' * 72}")
    print(f"ffmpeg: {doc['tool_versions']['ffmpeg']}")
    print(f"derived threshold  norm < {thr:.4f}  ->  {n_below} pairs classified duplicate")
    print(f"phase histogram of classified set: "
          + " ".join(f"{p}:{counts[p]}" for p in range(PERIOD_SPACE) if counts[p]))
    print(f"dominant phase: a mod {PERIOD_SPACE} == {dom}  "
          f"(duplicate frame b mod {PERIOD_SPACE} == {(dom + 1) % PERIOD_SPACE})")
    print(f"purity: {counts[dom]}/{n_below} of classified pairs at phase {dom}")

    print(f"\nmean normalised score by phase (n per phase in brackets):")
    for p in range(PERIOD_SPACE):
        v = [r["norm"] for r in seg if r["phase"] == p]
        mark = "  <-- duplicate phase" if p == dom else ""
        print(f"  phase {p:2d} [{len(v):3d}]  mean {np.mean(v):7.4f}  "
              f"min {np.min(v):7.4f}{mark}")

    print(f"\npopulation separation on raw mad_y:")
    print(f"  phase-{dom} pairs   n={len(inph):3d}  median {np.median([r['mad_y'] for r in inph]):.5f}  max {hi_in:.5f}")
    print(f"  all other pairs  n={len(other):3d}  median {np.median([r['mad_y'] for r in other]):.5f}  min {lo_out:.5f}")
    print(f"  disjoint: {disjoint}"
          + (f"  (gap {lo_out / hi_in:.2f}x)" if disjoint else "  -- POPULATIONS OVERLAP"))
    print(f"  bit-identical pairs at phase {dom}: {sum(r['exact'] for r in inph)}")

    # every pair on the dominant phase, which is the full candidate series
    print(f"\nall {len(inph)} pairs at phase {dom}:")
    print(f"  {'pair':>15} {'mad_y':>9} {'mad_rgb':>9} {'norm':>8} {'max_y':>7} "
          f"{'frac>4':>8} {'exact':>6}")
    for r in sorted(inph, key=lambda r: r["a"]):
        print(f"  f{r['a']}->f{r['b']:<7} {r['mad_y']:9.4f} {r['mad_rgb']:9.4f} "
              f"{r['norm']:8.4f} {r['max_y']:7.2f} {r['frac_gt4'] * 100:7.2f}% "
              f"{str(r['exact']):>6}")

    # absolute-threshold sweep: reproduces how a transferred cut truncates the series
    print(f"\nabsolute-threshold sweep on mad_y (no local normalisation):")
    print(f"  {'cut':>8} {'pairs':>7} {'at phase ' + str(dom):>12}")
    for cut in (0.05, 0.06, 0.07, 0.08, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50):
        hit = [r for r in seg if r["mad_y"] < cut]
        print(f"  {cut:8.2f} {len(hit):7d} {sum(1 for r in hit if r['phase'] == dom):12d}")

    n_dup = len(inph)
    uniq = (len(seg) - n_dup) / len(seg)
    print(f"\nderived cadence:")
    print(f"  duplicate pairs   {n_dup} / {len(seg)} = {n_dup / len(seg):.5f}"
          f"   (1/{PERIOD_SPACE} = {1 / PERIOD_SPACE:.5f})")
    print(f"  implied period    {len(seg) / n_dup:.3f} frames")
    print(f"  unique fraction   {uniq:.5f}"
          f"   ({PERIOD_SPACE - 1}/{PERIOD_SPACE} = {(PERIOD_SPACE - 1) / PERIOD_SPACE:.5f})"
          f"   agreement {100 * abs(uniq - (PERIOD_SPACE - 1) / PERIOD_SPACE) / ((PERIOD_SPACE - 1) / PERIOD_SPACE):.3f}%")

    return {
        "copy": copy,
        "n_pairs": len(seg),
        "threshold_norm": thr,
        "n_classified": n_below,
        "dominant_phase_a": dom,
        "dominant_phase_b": (dom + 1) % PERIOD_SPACE,
        "purity": f"{int(counts[dom])}/{n_below}",
        "n_on_dominant_phase": len(inph),
        "max_mad_y_on_phase": hi_in,
        "min_mad_y_off_phase": lo_out,
        "populations_disjoint": bool(disjoint),
        "n_bit_identical": int(sum(r["exact"] for r in inph)),
        "duplicate_rate": n_dup / len(seg),
        "implied_period": len(seg) / n_dup,
        "unique_fraction": uniq,
        "series_first_duplicate_frame": min(r["b"] for r in inph),
        "series_last_duplicate_frame": max(r["b"] for r in inph),
        "duplicate_pairs": [[r["a"], r["b"]] for r in sorted(inph, key=lambda r: r["a"])],
        "tool_versions": doc["tool_versions"],
    }


def main() -> None:
    results = {c: report(c) for c in ("av1", "avc") if (HERE / f"pairs_{c}.json").exists()}
    if not results:
        raise SystemExit("no pairs_*.json -- run dupdetect.py first")

    if len(results) == 2:
        a, v = results["av1"], results["avc"]
        print(f"\n{'=' * 72}\nCODEC CROSS-CHECK\n{'=' * 72}")
        agree = a["duplicate_pairs"] == v["duplicate_pairs"]
        print(f"  same duplicate set in both copies: {agree}")
        print(f"  AV1 {a['n_on_dominant_phase']} pairs, AVC {v['n_on_dominant_phase']} pairs, "
              f"dominant phase {a['dominant_phase_a']} / {v['dominant_phase_a']}")
        print(f"  bit-identical: AV1 {a['n_bit_identical']}, AVC {v['n_bit_identical']}")

    (HERE / "classification.json").write_text(
        json.dumps(results, indent=1, sort_keys=True) + "\n")
    print(f"\nwrote {(HERE / 'classification.json').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
