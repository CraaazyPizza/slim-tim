#!/usr/bin/env python3.12
"""Identify static text-card frames vs live 'footage' frames.
Static cards: frame-to-frame row-profile change ~0 AND high spatial contrast.
Prints per-second stillness so ranges can be read off."""
import numpy as np, os
O = "/home/user/new-skinny-bob/analysis/compare-eras/band"
K = [("OpSTlDJWFFI",30000/1001),("Oqw96jCOP7A",30000/1001),("l9RAhmPHM_A",30000/1001),
     ("ZB788PtqQvg",25.),("RsQCXN4o4Ps",25.),("Xju_CY5ZESA",25.),("a6TLGkrfNKI",25.)]
for key, fps in K:
    d = np.load(f"{O}/{key}_p2.npz")
    P = d["rowprof"][:, 120:900].astype(np.float64)
    dt = np.r_[0, np.sqrt(((np.diff(P, axis=0))**2).mean(axis=1))]
    spf = int(round(fps)); ns = len(dt)//spf
    ser = [dt[s*spf:(s+1)*spf].mean() for s in range(ns)]
    print(f"\n{key}: frame-to-frame row-profile RMS change, per second "
          f"(median={np.median(dt):.4f})")
    print("  " + " ".join(f"{s}:{v:.3f}" for s, v in enumerate(ser)))
