#!/usr/bin/env python3.12
"""Horizontal banding analysis, v3 -- text-card frames excluded, plus a
local-temporal-mean-subtracted 'dynamic' spectrum that cancels ANY static
overlay (burned-in text included) exactly.

Spectra per video:
  STATIC  : |FFT(mean over footage frames of highpassed row profile)|^2
            -> fixed banding baked into the picture (needs cards excluded)
  DYNAMIC : mean |FFT(prof_t - localmean_{t+-W}(prof))|^2
            -> banding that moves/flickers; immune to static text
  ALLFR   : mean |FFT(highpassed prof_t)|^2 over footage frames

Baseline = log-frequency-local median (f/1.35..f*1.35 minus f/1.06..f*1.06 guard).
Amplitude in 8-bit luma LSB = sqrt(2)*RMS of a +-2.5 resolution-element bandpass.
Comb search: for each candidate fundamental, sum log10(SNR) over its harmonics.
"""
import numpy as np, os, sys

O = "/home/user/new-skinny-bob/analysis/compare-eras/band"
# key: (fps, R0, R1, footage second-ranges [(t0,t1),...] inclusive)
CFG = {
 "OpSTlDJWFFI": (30000/1001, 120, 900, [(31, 97)]),
 "Oqw96jCOP7A": (30000/1001, 120, 900, [(16, 80)]),
 "l9RAhmPHM_A": (30000/1001, 140, 900, [(16, 141)]),
 "ZB788PtqQvg": (25.0, 120, 900, [(5, 46)]),
 "RsQCXN4o4Ps": (25.0, 120, 900, [(24, 59)]),
 "Xju_CY5ZESA": (25.0, 120, 900, [(5, 20), (32, 34), (58, 61), (82, 96)]),
 "a6TLGkrfNKI": (25.0, 60, 400, [(72, 82)]),
}
HP = int(os.environ.get("HP", 121))
PMIN, PMAX = 2.05, 120.0
PADF = 8
LW = 15          # local temporal mean half-width (frames)


def highpass(P, k):
    ker = np.ones(k)/k
    pad = np.pad(P, ((0, 0), (k//2, k//2)), mode="reflect")
    return P - np.stack([np.convolve(r, ker, mode="valid") for r in pad])


def logbaseline(f, ps, r=1.35, g=1.06):
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


def peaklist(f, snr, lo, hi, npk=5):
    idx = np.where((f >= 1.0/hi) & (f <= 1.0/lo) & np.isfinite(snr))[0]
    srt = idx[np.argsort(snr[idx])[::-1]]
    peaks = []
    for o in srt:
        if all(abs(1/f[o]-1/f[q]) > 0.06*(1/f[q]) for q in peaks):
            peaks.append(int(o))
        if len(peaks) == npk:
            break
    return peaks


def combsearch(f, snr, M, pmin=6.0, pmax=120.0, nh=16):
    """score each candidate fundamental by sum of log10(SNR) over harmonics"""
    cands = np.arange(pmin, pmax, 0.02)
    fi = np.nan_to_num(np.maximum(snr, 1e-3))
    best = []
    for per in cands:
        s = 0.0; k = 0
        for n in range(1, nh+1):
            fh = n/per
            if fh > 0.45:
                break
            j = int(round(fh*len(f)*2))
            j = min(max(j, 1), len(f)-1)
            # take max SNR within +-1.5 resolution elements
            w = int(1.5*PADF)
            s += np.log10(fi[max(1, j-w):j+w+1].max()); k += 1
        if k >= 4:
            best.append((s/k, per, k))
    best.sort(reverse=True)
    out = []
    for sc, per, k in best:
        if all(abs(per-p) > 0.06*p and abs(per-p*2) > 0.06*p and abs(per*2-p) > 0.06*p
               for _, p, _ in out):
            out.append((sc, per, k))
        if len(out) == 3:
            break
    return out


def run(key, fps, R0, R1, ranges):
    d = np.load(f"{O}/{key}_p2.npz")
    RP = d["rowprof"]
    nfr = RP.shape[0]
    sel = np.zeros(nfr, bool)
    for t0, t1 in ranges:
        sel[int(t0*fps):min(nfr, int((t1+1)*fps))] = True
    P = RP[:, R0:R1].astype(np.float64)
    M = R1-R0
    D = highpass(P, HP)
    # local temporal mean (box, reflect at ends)
    cs = np.cumsum(np.vstack([np.zeros((1, M)), D]), axis=0)
    lm = np.empty_like(D)
    for i in range(nfr):
        a, b = max(0, i-LW), min(nfr, i+LW+1)
        lm[i] = (cs[b]-cs[a])/(b-a)
    DYN = D - lm

    NP = M*PADF
    f = np.fft.rfftfreq(NP)
    win = np.hanning(M)
    Ds, DYs = D[sel], DYN[sel]
    mp = Ds.mean(axis=0)
    S = {"STATIC": np.abs(np.fft.rfft(mp*win, n=NP))**2,
         "DYNAMIC": (np.abs(np.fft.rfft(DYs*win, n=NP, axis=-1))**2).mean(axis=0),
         "ALLFR": (np.abs(np.fft.rfft(Ds*win, n=NP, axis=-1))**2).mean(axis=0)}
    SRC = {"STATIC": P[sel].mean(axis=0)[None, :], "DYNAMIC": DYN[sel],
           "ALLFR": P[sel]}
    print(f"\n===== {key}  rect cols {d['rect'][0]}..{d['rect'][1]}, rows {R0}..{R1} "
          f"({M} rows)\n      footage frames {sel.sum()}/{nfr} from t={ranges}  "
          f"{fps:.3f}fps  HP={HP}")
    res = {}
    for nm in ("STATIC", "DYNAMIC", "ALLFR"):
        ps = S[nm]
        bl = logbaseline(f, ps)
        with np.errstate(invalid="ignore", divide="ignore"):
            snr = ps/bl
        pk = peaklist(f, snr, PMIN, PMAX)
        print(f"  {nm:8s} peaks: " + ", ".join(
            f"{1/f[q]:7.2f}px SNR={snr[q]:7.2f} amp={amp_at(SRC[nm],1/f[q],M):.4f}"
            for q in pk))
        cb = combsearch(f, snr, M)
        print(f"           comb fundamentals: " + ", ".join(
            f"{p:.2f}px (mean log10SNR/harm={s:+.2f}, {k}h)" for s, p, k in cb))
        res[nm] = (snr, f, pk)
    print(f"  RMS (LSB): detrended={Ds.std():.4f}  static-mean={mp.std():.4f}  "
          f"dynamic(local)={DYs.std():.4f}")

    # phase drift on strongest DYNAMIC and STATIC peaks
    for nm in ("DYNAMIC", "STATIC"):
        snr, ff, pk = res[nm]
        if not pk:
            continue
        j = pk[0]; per = 1/ff[j]
        if snr[j] < 5:
            print(f"  {nm}: top peak SNR {snr[j]:.2f} < 5 -> no drift fit (no banding)")
            continue
        kk = j*M/NP
        e = np.exp(-2j*np.pi*kk*np.arange(M)/M)*win
        c = (DYN[sel] if nm == "DYNAMIC" else D[sel]) @ e
        ph = np.unwrap(np.angle(c)); mg = np.abs(c)
        good = mg > np.percentile(mg, 50)
        t = np.arange(len(c))[good]
        sl, ic = np.polyfit(t, ph[good], 1)
        rr = ph[good]-(sl*t+ic)
        dph = np.angle(c[1:]*np.conj(c[:-1]))
        print(f"  {nm} PHASE@{per:.2f}px: fit {sl:+.5f}rad/fr -> "
              f"{-sl/(2*np.pi)*per:+.5f}px/fr ({-sl/(2*np.pi)*per*fps:+.3f}px/s); "
              f"resid_sd={rr.std():.2f}rad; median dphi={np.median(dph):+.4f}rad "
              f"({-np.median(dph)/(2*np.pi)*per:+.4f}px/fr) IQR={np.subtract(*np.percentile(dph,[75,25])):.3f}rad; "
              f"|c|cv={mg.std()/mg.mean():.2f}")


if __name__ == "__main__":
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    for k, (fps, R0, R1, rg) in CFG.items():
        if only and k not in only:
            continue
        run(k, fps, R0, R1, rg)
