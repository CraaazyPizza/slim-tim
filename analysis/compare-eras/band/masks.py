#!/usr/bin/env python3.12
"""Determine picture-area rect and locate static burned-in text from pass1 maps."""
import numpy as np, glob, os
from PIL import Image
O = "/home/user/new-skinny-bob/analysis/compare-eras/band"
KEYS = ["OpSTlDJWFFI","Oqw96jCOP7A","l9RAhmPHM_A","ZB788PtqQvg","RsQCXN4o4Ps","Xju_CY5ZESA","a6TLGkrfNKI"]
for k in KEYS:
    f = f"{O}/{k}_p1.npz"
    if not os.path.exists(f): continue
    d = np.load(f)
    ym, ys = d["ymean"], d["ystd"]
    H, W = ym.shape
    rs = ys.mean(axis=1); cs = ys.mean(axis=0)   # temporal-std averaged per row/col
    rm = ym.mean(axis=1); cm = ym.mean(axis=0)
    print(f"\n=== {k}  {W}x{H} n={int(d['n'])} nacc={int(d['nacc'])}")
    print("  row temporal-std (every 40 rows):",
          " ".join(f"{i}:{rs[i]:.1f}" for i in range(0, H, 40)))
    print("  col temporal-std (every 80 cols):",
          " ".join(f"{i}:{cs[i]:.1f}" for i in range(0, W, 80)))
    print("  row ymean (every 40):", " ".join(f"{i}:{rm[i]:.1f}" for i in range(0, H, 40)))
    print("  col ymean (every 80):", " ".join(f"{i}:{cm[i]:.1f}" for i in range(0, W, 80)))
    # active rows/cols: temporal std above 15% of max
    tr = 0.15*rs.max(); tc = 0.15*cs.max()
    ar = np.where(rs > tr)[0]; ac = np.where(cs > tc)[0]
    print(f"  active rows {ar.min()}..{ar.max()}  active cols {ac.min()}..{ac.max()}")
    # save visualisations, contrast stretched
    for nm, arr in (("ymean", ym), ("ystd", ys)):
        a = arr.astype(np.float32); lo, hi = np.percentile(a, 1), np.percentile(a, 99.5)
        v = np.clip((a-lo)/max(hi-lo,1e-6)*255, 0, 255).astype(np.uint8)
        Image.fromarray(v).resize((W//2, H//2)).save(f"{O}/mont/{k}_{nm}.png")
