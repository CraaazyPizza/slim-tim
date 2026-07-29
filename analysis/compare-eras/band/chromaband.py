#!/usr/bin/env python3.12
"""Horizontal banding in the CHROMA planes (the claim is 'coloured banding').
U and V row-mean profiles at chroma resolution (H/2 rows, so 1 chroma row = 2
luma scanlines).  Same machinery as the luma version: poly-detrend, local
temporal mean subtraction for the dynamic part, log-frequency-local SNR.
Periods are reported in LUMA pixels (= 2 x chroma rows)."""
import numpy as np, os, sys
O = "/home/user/new-skinny-bob/analysis/compare-eras/band"
CFG = {
 "OpSTlDJWFFI": (30000/1001, 60, 450, [(31, 97)]),
 "Oqw96jCOP7A": (30000/1001, 60, 450, [(16, 80)]),
 "l9RAhmPHM_A": (30000/1001, 70, 450, [(16, 141)]),
 "ZB788PtqQvg": (25.0, 60, 450, [(5, 46)]),
 "RsQCXN4o4Ps": (25.0, 60, 450, [(24, 59)]),
 "Xju_CY5ZESA": (25.0, 60, 450, [(5, 20), (32, 34), (58, 61), (82, 96)]),
 "a6TLGkrfNKI": (25.0, 30, 210, [(8, 12), (19, 24), (32, 35), (37, 40), (51, 56), (67, 82)]),
}
PADF = 8; LW = 20; POLY = 4


def polydetrend(P, order=POLY):
    M = P.shape[1]; x = np.linspace(-1, 1, M)
    A = np.vstack([x**k for k in range(order+1)]).T
    c, *_ = np.linalg.lstsq(A, P.T, rcond=None)
    return P - (A @ c).T


def logbaseline(f, ps, r=1.5, g=1.1):
    out = np.full(len(ps), np.nan)
    for i in range(1, len(ps)):
        fi = f[i]
        m = (f >= fi/r) & (f <= fi*r) & ~((f >= fi/g) & (f <= fi*g))
        if m.sum() >= 4: out[i] = np.median(ps[m])
    return out


def amp_at(P, per, M):
    n = P.shape[-1]; f = np.fft.rfftfreq(n); F = np.fft.rfft(P, axis=-1)
    bp = np.fft.irfft(np.where(np.abs(f-1.0/per) <= 2.5/M, F, 0), n=n, axis=-1)
    return float(np.sqrt(2)*np.atleast_1d(bp.std(axis=-1)).mean())


def run(key, fps, R0, R1, ranges, PMIN, PMAX):
    d = np.load(f"{O}/{key}_p3.npz")
    for plane in ("uprof", "vprof"):
        RP = d[plane]; nfr = RP.shape[0]
        sel = np.zeros(nfr, bool)
        for t0, t1 in ranges:
            sel[int(t0*fps):min(nfr, int((t1+1)*fps))] = True
        P = RP[:, R0:R1].astype(np.float64); M = R1-R0
        D = polydetrend(P)
        cs = np.cumsum(np.vstack([np.zeros((1, M)), D]), axis=0)
        DYN = np.empty_like(D)
        for i in range(nfr):
            a, b = max(0, i-LW), min(nfr, i+LW+1)
            DYN[i] = D[i]-(cs[b]-cs[a])/(b-a)
        NP = M*PADF; f = np.fft.rfftfreq(NP); win = np.hanning(M)
        print(f"  {plane[0].upper()}: sd(profile)={P[sel].std():.4f} "
              f"detrended={D[sel].std():.4f} dynamic={DYN[sel].std():.4f} LSB", end="")
        for nm, X, src in (("STATIC", D[sel].mean(axis=0)[None, :], P[sel].mean(axis=0)[None, :]),
                           ("DYN", DYN[sel], DYN[sel])):
            ps = (np.abs(np.fft.rfft(X*win, n=NP, axis=-1))**2).mean(axis=0)
            bl = logbaseline(f, ps)
            with np.errstate(invalid="ignore", divide="ignore"):
                snr = ps/bl
            idx = np.where((f >= 1/(PMAX/2)) & (f <= 1/(PMIN/2)) & np.isfinite(snr))[0]
            srt = idx[np.argsort(snr[idx])[::-1]]
            pk = []
            for o in srt:
                if all(abs(1/f[o]-1/f[q]) > 0.1*(1/f[q]) for q in pk): pk.append(int(o))
                if len(pk) == 3: break
            print("\n     %-6s " % nm + ", ".join(
                f"{2/f[q]:7.1f}luma-px SNR={snr[q]:6.2f} amp={amp_at(src,1/f[q],M):.4f}"
                for q in pk), end="")
        print()


if __name__ == "__main__":
    for band in ((6.0, 120.0), (60.0, 900.0)):
        print(f"\n############ CHROMA BANDING, period band {band[0]}-{band[1]} luma px")
        for k, (fps, R0, R1, rg) in CFG.items():
            print(f"\n=== {k} chroma rows {R0}..{R1}")
            run(k, fps, R0, R1, rg, *band)
