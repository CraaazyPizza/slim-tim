#!/usr/bin/env python3.12
"""Chroma report: whole-frame (pass1) and picture-window (pass2) stats,
plus per-second time series and segment detection."""
import numpy as np, os, sys
O = "/home/user/new-skinny-bob/analysis/compare-eras/band"
KEYS = [("OpSTlDJWFFI",30000/1001),("Oqw96jCOP7A",30000/1001),("l9RAhmPHM_A",30000/1001),
        ("ZB788PtqQvg",25.0),("RsQCXN4o4Ps",25.0),("Xju_CY5ZESA",25.0),("a6TLGkrfNKI",25.0)]
C1 = ["mU","mV","sU","sV","fU2","fU4","fU8","fV2","fV4","fV8","mag","magmax","mY"]
C2 = ["mU","mV","sU","sV","fU2","fU4","fU8","fV2","fV4","fV8","mag","magp99","magmax","mY"]
PERSEC = "--persec" in sys.argv

def show(key, fps, arr, label, cols):
    idx = {c:i for i,c in enumerate(cols)}
    g = lambda c: arr[:, idx[c]]
    print(f"\n--- {key} [{label}] frames={len(arr)}")
    print("  meanU=%.3f meanV=%.3f  sdU=%.3f sdV=%.3f  <mag>=%.3f  magmax=%.1f" % (
        g("mU").mean(), g("mV").mean(), g("sU").mean(), g("sV").mean(),
        g("mag").mean(), g("magmax").max()))
    print("  frac |U-128|>2/4/8 = %.4f / %.4f / %.4f    |V-128|>2/4/8 = %.4f / %.4f / %.4f" % (
        g("fU2").mean(), g("fU4").mean(), g("fU8").mean(),
        g("fV2").mean(), g("fV4").mean(), g("fV8").mean()))
    if "magp99" in idx:
        print("  mag p99 (mean over frames)=%.2f" % g("magp99").mean())
    spf = int(round(fps)); ns = len(arr)//spf
    ser = np.array([[arr[s*spf:(s+1)*spf, idx[c]].mean() for c in
                     ("mU","mV","sU","sV","mag","fU4","fV4","mY")] for s in range(ns)])
    print("  per-second range: meanU %.2f..%.2f  meanV %.2f..%.2f  <mag> %.2f..%.2f" % (
        ser[:,0].min(), ser[:,0].max(), ser[:,1].min(), ser[:,1].max(),
        ser[:,4].min(), ser[:,4].max()))
    if PERSEC:
        print("   t(s)   meanU   meanV     sdU    sdV    <mag>   fU>4    fV>4    meanY")
        for s in range(ns):
            print("   %4d  %7.3f %7.3f  %6.3f %6.3f  %6.3f  %.4f  %.4f  %6.2f" %
                  (s, *ser[s]))
    return ser

for key, fps in KEYS:
    for f, cols, lab in ((f"{O}/{key}_p1.npz","p1","full frame"),
                         (f"{O}/{key}_p2.npz","p2","picture window")):
        if not os.path.exists(f): continue
        d = np.load(f)
        if cols == "p1":
            show(key, fps, d["cstats"], lab, C1)
        else:
            show(key, fps, d["cst"], lab + " " + str(list(d["rect"])), C2)
