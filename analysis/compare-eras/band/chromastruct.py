#!/usr/bin/env python3.12
"""Chroma structure report from pass2 `struct` (every 6th frame, picture rect).
Columns: corr(|chroma|,|gradY|), corr(U,V), sfracU, sfracV,
         acU(1),acU(2),acU(4),acU(8), corr(U,Y), corr(V,Y), sdU, sdV, sdY, meanGradY

Discriminators
  corr(U,Y) / corr(V,Y) near +-1  -> chroma is a fixed linear function of luma,
                                     i.e. a TINT on monochrome (no independent colour)
  sfrac (variance surviving 4x4 block averaging): ~1/16 = white noise,
                                     -> 1 = fully spatially structured
  acU(l)                          : chroma autocorrelation at lag l chroma-px
"""
import numpy as np, os
O = "/home/user/new-skinny-bob/analysis/compare-eras/band"
K = [("OpSTlDJWFFI",30000/1001),("Oqw96jCOP7A",30000/1001),("l9RAhmPHM_A",30000/1001),
     ("ZB788PtqQvg",25.),("RsQCXN4o4Ps",25.),("Xju_CY5ZESA",25.),("a6TLGkrfNKI",25.)]
N = ["cor_mag_grad","cor_UV","sfracU","sfracV","acU1","acU2","acU4","acU8",
     "cor_UY","cor_VY","sdU","sdV","sdY","meanGradY"]
for key, fps in K:
    f = f"{O}/{key}_p2.npz"
    if not os.path.exists(f): continue
    d = np.load(f); S = d["struct"]; si = d["sidx"]
    ok = S[:, N.index("sdU")] > 0.15      # frames with any chroma variation at all
    print(f"\n=== {key}  {len(S)} sampled frames (every 6th), {ok.sum()} with sdU>0.15")
    for i, n in enumerate(N):
        x = S[ok, i] if ok.sum() > 5 else S[:, i]
        print(f"   {n:13s} median={np.median(x):+8.4f}  p10={np.percentile(x,10):+8.4f} "
              f" p90={np.percentile(x,90):+8.4f}")
    # top-chroma frames
    j = np.argsort(S[:, N.index("sdU")])[::-1][:6]
    print("   highest-sdU sampled frames (frame#, t s, sdU, sdV, cor_UY, cor_VY, "
          "sfracU, cor_mag_grad):")
    for q in j:
        print("     f%05d t=%6.2f  sdU=%6.3f sdV=%6.3f  corUY=%+.3f corVY=%+.3f "
              "sfracU=%.3f cor_mg=%+.3f" % (si[q]+1, si[q]/fps,
              S[q, 10], S[q, 11], S[q, 8], S[q, 9], S[q, 2], S[q, 0]))
