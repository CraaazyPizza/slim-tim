#!/usr/bin/env python3.12
"""Low-frequency ('broad band') horizontal banding: periods 60-900 px.
A CRT/rolling-shutter beat gives 1-6 broad bands that ROLL vertically, so:
  - detrend each frame's row profile with a 4th-order polynomial (kills vignette)
  - subtract a local temporal mean (+-LW frames) to isolate what MOVES
  - FFT, look at periods 60..900 px
  - for the strongest band, track the complex phase per frame -> drift px/frame
Also does a sliding-window scan (WIN frames) so a banding episode confined to a
few seconds is not diluted by averaging over the whole video.
"""
import numpy as np, os, sys
O = "/home/user/new-skinny-bob/analysis/compare-eras/band"
CFG = {
 "OpSTlDJWFFI": (30000/1001, 120, 900, [(31, 97)]),
 "Oqw96jCOP7A": (30000/1001, 120, 900, [(16, 80)]),
 "l9RAhmPHM_A": (30000/1001, 140, 900, [(16, 141)]),
 "ZB788PtqQvg": (25.0, 120, 900, [(5, 46)]),
 "RsQCXN4o4Ps": (25.0, 120, 900, [(24, 59)]),
 "Xju_CY5ZESA": (25.0, 120, 900, [(5, 20), (32, 34), (58, 61), (82, 96)]),
 "a6TLGkrfNKI": (25.0, 60, 420, [(8, 12), (19, 24), (32, 35), (37, 40), (51, 56),
                                 (67, 82)]),
}
PADF = 8
LW = 20
POLY = 4
PMIN, PMAX = 60.0, 900.0
WIN = 60


def polydetrend(P, order=POLY):
    M = P.shape[1]
    x = np.linspace(-1, 1, M)
    A = np.vstack([x**k for k in range(order+1)]).T
    coef, *_ = np.linalg.lstsq(A, P.T, rcond=None)
    return P - (A @ coef).T


def logbaseline(f, ps, r=1.6, g=1.12):
    out = np.full(len(ps), np.nan)
    for i in range(1, len(ps)):
        fi = f[i]
        m = (f >= fi/r) & (f <= fi*r) & ~((f >= fi/g) & (f <= fi*g))
        if m.sum() >= 4:
            out[i] = np.median(ps[m])
    return out


def amp_at(P, per, M):
    n = P.shape[-1]
    f = np.fft.rfftfreq(n)
    F = np.fft.rfft(P, axis=-1)
    bp = np.fft.irfft(np.where(np.abs(f-1.0/per) <= 2.5/M, F, 0), n=n, axis=-1)
    return float(np.sqrt(2)*np.atleast_1d(bp.std(axis=-1)).mean())


def run(key, fps, R0, R1, ranges):
    d = np.load(f"{O}/{key}_p2.npz")
    RP = d["rowprof"]; nfr = RP.shape[0]
    sel = np.zeros(nfr, bool)
    for t0, t1 in ranges:
        sel[int(t0*fps):min(nfr, int((t1+1)*fps))] = True
    P = RP[:, R0:R1].astype(np.float64); M = R1-R0
    D = polydetrend(P)
    cs = np.cumsum(np.vstack([np.zeros((1, M)), D]), axis=0)
    DYN = np.empty_like(D)
    for i in range(nfr):
        a, b = max(0, i-LW), min(nfr, i+LW+1)
        DYN[i] = D[i] - (cs[b]-cs[a])/(b-a)
    NP = M*PADF
    f = np.fft.rfftfreq(NP)
    win = np.hanning(M)
    print(f"\n===== {key} rows {R0}..{R1} ({M}) footage {sel.sum()}/{nfr} "
          f"poly{POLY}-detrended, band {PMIN}-{PMAX}px")
    for nm, X, src in (("STATIC ", D[sel].mean(axis=0)[None, :], P[sel].mean(axis=0)[None, :]),
                       ("DYNAMIC", DYN[sel], DYN[sel])):
        ps = (np.abs(np.fft.rfft(X*win, n=NP, axis=-1))**2).mean(axis=0)
        bl = logbaseline(f, ps)
        with np.errstate(invalid="ignore", divide="ignore"):
            snr = ps/bl
        idx = np.where((f >= 1/PMAX) & (f <= 1/PMIN) & np.isfinite(snr))[0]
        srt = idx[np.argsort(snr[idx])[::-1]]
        pk = []
        for o in srt:
            if all(abs(1/f[o]-1/f[q]) > 0.12*(1/f[q]) for q in pk):
                pk.append(int(o))
            if len(pk) == 4:
                break
        print(f"  {nm} peaks: " + ", ".join(
            f"{1/f[q]:7.1f}px SNR={snr[q]:6.2f} amp={amp_at(src,1/f[q],M):.3f}LSB"
            for q in pk))
        print(f"          RMS in {PMIN}-{PMAX}px band = "
              f"{np.sqrt(2)*bandrms(X, PMIN, PMAX):.4f} LSB")
        if nm == "DYNAMIC" and pk:
            j = pk[0]; per = 1/f[j]
            kk = j*M/NP
            e = np.exp(-2j*np.pi*kk*np.arange(M)/M)*win
            c = DYN[sel] @ e
            mg = np.abs(c)
            dph = np.angle(c[1:]*np.conj(c[:-1]))
            good = (mg[1:] > np.percentile(mg, 60)) & (mg[:-1] > np.percentile(mg, 60))
            md = np.median(dph[good]) if good.sum() > 10 else np.nan
            print(f"          PHASE@{per:.1f}px median frame-to-frame dphi={md:+.4f}rad "
                  f"-> {-md/(2*np.pi)*per:+.3f}px/frame ({-md/(2*np.pi)*per*fps:+.2f}px/s); "
                  f"frac coherent (|dphi|<0.5rad)={np.mean(np.abs(dph[good])<0.5):.2f}; "
                  f"|c|cv={mg.std()/mg.mean():.2f}")
    # sliding window scan for a localised episode
    best = []
    ii = np.where(sel)[0]
    for a in range(0, len(ii)-WIN, WIN//2):
        blk = DYN[ii[a:a+WIN]]
        ps = (np.abs(np.fft.rfft(blk*win, n=NP, axis=-1))**2).mean(axis=0)
        bl = logbaseline(f, ps)
        with np.errstate(invalid="ignore", divide="ignore"):
            snr = ps/bl
        m = (f >= 1/PMAX) & (f <= 1/PMIN) & np.isfinite(snr)
        j = np.where(m)[0][np.nanargmax(snr[m])]
        best.append((float(snr[j]), 1/f[j], ii[a]/fps, amp_at(blk, 1/f[j], M)))
    best.sort(reverse=True)
    print("  sliding-window (%d fr) top episodes: " % WIN + "; ".join(
        f"t={t:.1f}s {p:.0f}px SNR={s:.1f} amp={a:.3f}LSB" for s, p, t, a in best[:4]))


def bandrms(X, pmin, pmax):
    n = X.shape[-1]
    f = np.fft.rfftfreq(n)
    F = np.fft.rfft(X, axis=-1)
    keep = (f >= 1/pmax) & (f <= 1/pmin)
    bp = np.fft.irfft(np.where(keep, F, 0), n=n, axis=-1)
    return float(np.atleast_1d(bp.std(axis=-1)).mean())


if __name__ == "__main__":
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    for k, v in CFG.items():
        if only and k not in only:
            continue
        run(k, *v)
