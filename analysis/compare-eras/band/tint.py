#!/usr/bin/env python3.12
"""Tint vs genuine colour, from pass4 cross-moments.
For each frame fit (U-128) = a_u*Y + b_u and (V-128) = a_v*Y + b_v over the
picture rect at chroma resolution.  Then:
  R2_u             fraction of U variance explained by luma  -> 1 = pure tint
  resid_sd_u       sd of U not explainable from luma (LSB)   -> genuine colour
  a_u*100          tint slope, chroma LSB per 100 luma LSB
  b_u              chroma offset at Y=0 (LSB)
Aggregated over frames with meaningful chroma (sdU or sdV > 0.4)."""
import numpy as np, os
O = "/home/user/new-skinny-bob/analysis/compare-eras/band"
K = [("OpSTlDJWFFI",30000/1001),("Oqw96jCOP7A",30000/1001),("l9RAhmPHM_A",30000/1001),
     ("ZB788PtqQvg",25.),("RsQCXN4o4Ps",25.),("Xju_CY5ZESA",25.),("a6TLGkrfNKI",25.)]
SEG = {"OpSTlDJWFFI": [("colour seg", 2571, 2917), ("mono part", 1100, 2500),
                       ("flash", 1040, 1044)],
       "a6TLGkrfNKI": [("strongest", 1816, 2045)],
       "ZB788PtqQvg": [("strongest", 133, 407)]}

def fit(m):
    n, sY, sYY, sU, sV, sYU, sYV, sUU, sVV, sUV = m.T
    mY = sY/n; vY = sYY/n - mY**2
    mU = sU/n; vU = sUU/n - mU**2
    mV = sV/n; vV = sVV/n - mV**2
    cYU = sYU/n - mY*mU; cYV = sYV/n - mY*mV
    cUV = sUV/n - mU*mV
    with np.errstate(invalid="ignore", divide="ignore"):
        au = cYU/vY; av = cYV/vY
        r2u = np.where(vU > 0, cYU**2/(vY*vU), 0)
        r2v = np.where(vV > 0, cYV**2/(vY*vV), 0)
        ru = np.sqrt(np.maximum(vU*(1-r2u), 0)); rv = np.sqrt(np.maximum(vV*(1-r2v), 0))
        cuv = np.where((vU > 0) & (vV > 0), cUV/np.sqrt(vU*vV), 0)
    return dict(mY=mY, sdU=np.sqrt(np.maximum(vU,0)), sdV=np.sqrt(np.maximum(vV,0)),
                au=au, av=av, bu=mU-au*mY, bv=mV-av*mY,
                r2u=r2u, r2v=r2v, ru=ru, rv=rv, cuv=cuv, mU=mU, mV=mV)

def rep(lbl, f, m):
    if m.sum() < 3:
        print(f"    {lbl}: <3 frames"); return
    g = lambda k: np.median(f[k][m])
    print(f"    {lbl:12s} n={m.sum():5d}  sdU={g('sdU'):6.3f} sdV={g('sdV'):6.3f} | "
          f"a_u*100={g('au')*100:+7.3f} a_v*100={g('av')*100:+7.3f} "
          f"b_u={g('bu'):+7.3f} b_v={g('bv'):+7.3f} | "
          f"R2u={g('r2u'):.3f} R2v={g('r2v'):.3f} | "
          f"resid_sdU={g('ru'):6.3f} resid_sdV={g('rv'):6.3f} | corUV={g('cuv'):+.3f}")

for key, fps in K:
    p = f"{O}/{key}_p4.npz"
    if not os.path.exists(p):
        print(f"\n=== {key}: pass4 not ready"); continue
    d = np.load(p); f = fit(d["mom"])
    n = len(f["sdU"])
    print(f"\n=== {key}  ({n} frames, rect {list(d['rect'])})")
    act = (f["sdU"] > 0.4) | (f["sdV"] > 0.4)
    rep("ALL active", f, act)
    for lbl, a, b in SEG.get(key, []):
        m = np.zeros(n, bool); m[a-1:b] = True
        rep(lbl, f, m & act)
