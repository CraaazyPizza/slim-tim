#!/usr/bin/env python3.12
"""Per-frame chroma time series -> segment boundaries.
Uses the picture-window (pass2) chroma stats.  A frame is called COLOURED if
sdU (over the picture rect) exceeds THR."""
import numpy as np
O = "/home/user/new-skinny-bob/analysis/compare-eras/band"
K = [("OpSTlDJWFFI",30000/1001),("Oqw96jCOP7A",30000/1001),("l9RAhmPHM_A",30000/1001),
     ("ZB788PtqQvg",25.),("RsQCXN4o4Ps",25.),("Xju_CY5ZESA",25.),("a6TLGkrfNKI",25.)]
C = ["mU","mV","sU","sV","fU2","fU4","fU8","fV2","fV4","fV8","mag","magp99","magmax","mY"]
THRS = (2.0, 3.0)
for key, fps in K:
    d = np.load(f"{O}/{key}_p2.npz"); a = d["cst"]
    sU, sV = a[:, 2], a[:, 3]
    mag99 = a[:, 11]
    print(f"\n=== {key}  (rect {list(d['rect'])})")
    for thr in THRS:
        m = (sU > thr) | (sV > thr)
        if not m.any():
            print(f"  sd>{thr}: no frames"); continue
        # contiguous runs
        idx = np.where(m)[0]
        runs = []
        s = idx[0]; p = idx[0]
        for i in idx[1:]:
            if i - p > int(0.4*fps):
                runs.append((s, p)); s = i
            p = i
        runs.append((s, p))
        tot = m.sum()
        print(f"  frames with sdU or sdV > {thr}: {tot} ({100*tot/len(a):.1f}%)  runs:")
        for s, e in runs:
            if e-s < 3: continue
            w = a[s:e+1]
            print(f"    f{s+1:05d}-f{e+1:05d}  t={s/fps:6.2f}-{e/fps:6.2f}s "
                  f"({(e-s+1)/fps:5.2f}s)  meanU={w[:,0].mean():7.3f} meanV={w[:,1].mean():7.3f} "
                  f"sdU={w[:,2].mean():6.3f} sdV={w[:,3].mean():6.3f} "
                  f"magp99={w[:,11].mean():6.2f} magmax={w[:,12].max():6.1f} "
                  f"fU8={w[:,6].mean():.3f} fV8={w[:,9].mean():.3f}")
    # overall max frame
    j = int(np.argmax(sU+sV))
    print(f"  peak-chroma frame f{j+1:05d} t={j/fps:.2f}s sdU={sU[j]:.3f} sdV={sV[j]:.3f} "
          f"magp99={mag99[j]:.2f} magmax={a[j,12]:.1f}")
