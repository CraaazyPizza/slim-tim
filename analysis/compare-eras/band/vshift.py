#!/usr/bin/env python3.12
"""Global vertical image shift per frame, by sub-pixel cross-correlation of
consecutive row-mean profiles.  Needed to show that the small phase drifts seen
in the banding analysis are just the picture translating vertically (film weave
/ gate float), not a band rolling relative to the picture."""
import numpy as np
O = "/home/user/new-skinny-bob/analysis/compare-eras/band"
K = [("OpSTlDJWFFI",30000/1001,120,900,[(31,97)]),("Oqw96jCOP7A",30000/1001,120,900,[(16,80)]),
     ("l9RAhmPHM_A",30000/1001,140,900,[(16,141)]),("ZB788PtqQvg",25.,120,900,[(5,46)]),
     ("RsQCXN4o4Ps",25.,120,900,[(24,59)]),("Xju_CY5ZESA",25.,120,900,[(5,20),(82,96)]),
     ("a6TLGkrfNKI",25.,60,420,[(67,82)])]
for key, fps, R0, R1, rg in K:
    d = np.load(f"{O}/{key}_p2.npz")
    P = d["rowprof"][:, R0:R1].astype(np.float64)
    M = R1-R0
    x = np.linspace(-1, 1, M)
    A = np.vstack([x**i for i in range(3)]).T
    c, *_ = np.linalg.lstsq(A, P.T, rcond=None)
    D = (P-(A@c).T)*np.hanning(M)
    sel = np.zeros(len(P), bool)
    for a, b in rg:
        sel[int(a*fps):min(len(P), int((b+1)*fps))] = True
    ii = np.where(sel)[0]
    F = np.fft.rfft(D[ii], axis=1)
    sh = []
    for i in range(len(ii)-1):
        if ii[i+1] != ii[i]+1: continue
        cc = np.fft.irfft(F[i+1]*np.conj(F[i]), n=M)
        cc = np.roll(cc, M//2)
        j = int(np.argmax(cc))
        if 0 < j < M-1:
            den = cc[j-1]-2*cc[j]+cc[j+1]
            sub = 0.5*(cc[j-1]-cc[j+1])/den if den != 0 else 0.0
        else:
            sub = 0.0
        sh.append(j+sub-M//2)
    sh = np.array(sh)
    print(f"  {key:12s} vertical shift per frame: median={np.median(sh):+.4f}px  "
          f"mean={sh.mean():+.4f}px  sd={sh.std():.3f}px  "
          f"p5..p95={np.percentile(sh,5):+.2f}..{np.percentile(sh,95):+.2f}px  "
          f"|shift|>0.2px in {np.mean(np.abs(sh)>0.2):.2f} of frames  ({len(sh)} pairs)")
