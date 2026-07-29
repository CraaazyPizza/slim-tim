#!/usr/bin/env python3.12
"""Test whether the ubiquitous 32/16/4-px static comb is the AV1 coded block
grid: if so its phase must be locked to row 0 of the CODED frame (multiples of
32 counted from the top of the 1080/480-line picture), identically in all files.
Uses pass1 full-width row means over ALL rows so absolute row indices are exact.
"""
import numpy as np
O = "/home/user/new-skinny-bob/analysis/compare-eras/band"
K = ["OpSTlDJWFFI","Oqw96jCOP7A","l9RAhmPHM_A","ZB788PtqQvg","RsQCXN4o4Ps",
     "Xju_CY5ZESA","a6TLGkrfNKI"]
print("period : phase of the static row-mean component, expressed as the row"
      " offset (0..period-1) of its MAXIMUM, counted from coded row 0")
for k in K:
    d = np.load(f"{O}/{k}_p1.npz")
    P = d["rowmean"].astype(np.float64)
    H = int(d["H"])
    R0, R1 = (100, 980) if H == 1080 else (40, 440)
    x = P[:, R0:R1]
    ker = np.ones(65)/65
    pad = np.pad(x, ((0, 0), (32, 32)), mode="reflect")
    x = x - np.stack([np.convolve(r, ker, mode="valid") for r in pad])
    m = x.mean(axis=0)
    n = len(m)
    out = []
    for per in (32.0, 16.0, 8.0, 4.0):
        kk = n/per
        if abs(kk-round(kk)) > 1e-9:
            pass
        e = np.exp(-2j*np.pi*np.arange(R0, R1)/per)
        c = (m*e).sum()
        off = (-np.angle(c)/(2*np.pi)*per) % per
        # amplitude
        amp = 2*abs(c)/n
        out.append(f"{per:.0f}px: off={off:5.2f} amp={amp:.4f}")
    print(f"  {k:12s} " + "  ".join(out))
