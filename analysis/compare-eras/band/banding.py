#!/usr/bin/env python3.12
"""Horizontal banding analysis (row-mean luma profile -> FFT down the row axis).

For each video, restricted to a rect strictly inside the vignette window and
above the burned-in timecode band:
  - incoherent : mean power spectrum over frames  (banding even if phase drifts)
  - coherent   : spectrum of the temporal-mean profile (STATIC banding/overlay)
  - dynamic    : mean spectrum of (profile - temporal mean) (rolling/moving banding)
Significance = peak power / local median power, with the local window and guard
band expressed in independent spectral resolution elements (NPAD/M bins each).
Amplitude in 8-bit luma code values: sqrt(2) * RMS of a +-2.5 resolution-element
band-pass of the *unwindowed* profile.
"""
import numpy as np, os, sys

O = "/home/user/new-skinny-bob/analysis/compare-eras/band"
CFG = {
 "OpSTlDJWFFI": (30000/1001, 120, 900),
 "Oqw96jCOP7A": (30000/1001, 120, 900),
 "l9RAhmPHM_A": (30000/1001, 140, 900),
 "ZB788PtqQvg": (25.0, 120, 900),
 "RsQCXN4o4Ps": (25.0, 120, 900),
 "Xju_CY5ZESA": (25.0, 120, 900),
 "a6TLGkrfNKI": (25.0, 60, 400),
}
NPAD = 8192
HP = int(os.environ.get("HP", 61))       # high-pass MA length -> periods < ~HP px
PMIN = float(os.environ.get("PMIN", 2.05))
PMAX = float(os.environ.get("PMAX", 60))


def highpass(P, k=HP):
    ker = np.ones(k) / k
    pad = np.pad(P, ((0, 0), (k // 2, k // 2)), mode="reflect")
    tr = np.stack([np.convolve(r, ker, mode="valid") for r in pad])
    return P - tr


def spec(x, win):
    return np.abs(np.fft.rfft(x * win, n=NPAD, axis=-1)) ** 2


def localmed(ps, res, nres=40):
    """local median excluding a +-3 resolution-element guard band"""
    k = int(nres * res); g = int(3 * res)
    n = len(ps); out = np.empty(n)
    for i in range(n):
        a, b = max(0, i - k), min(n, i + k + 1)
        w = np.concatenate([ps[a:max(a, i - g)], ps[min(b, i + g + 1):b]])
        out[i] = np.median(w) if len(w) else np.nan
    return out


def amp_at(P, per, M):
    f = np.fft.rfftfreq(P.shape[-1])
    F = np.fft.rfft(P, axis=-1)
    keep = np.abs(f - 1.0 / per) <= 2.5 / M
    bp = np.fft.irfft(np.where(keep, F, 0), n=P.shape[-1], axis=-1)
    return float(np.sqrt(2) * np.atleast_1d(bp.std(axis=-1)).mean())


def analyse(key, Pin, fps, R0, R1, tag, frames=None):
    P = Pin[:, R0:R1].astype(np.float64)
    if frames is not None:
        P = P[frames]
    nf, M = P.shape
    D = highpass(P)
    win = np.hanning(M)
    freqs = np.fft.rfftfreq(NPAD)
    res = NPAD / M
    lo = int(np.searchsorted(freqs, 1.0 / PMAX))
    hi = int(np.searchsorted(freqs, 1.0 / PMIN))

    inco = spec(D, win).mean(axis=0)
    mp = D.mean(axis=0)
    coh = spec(mp, win)
    dyn = spec(D - mp, win).mean(axis=0)

    print(f"\n===== {key} [{tag}] rows {R0}..{R1} ({M} rows) {nf} frames {fps:.3f}fps "
          f"HP={HP} band {PMIN}-{PMAX}px")
    out = {}
    for name, ps, src in (("incoherent", inco, P),
                          ("coherent/static", coh, P.mean(axis=0)[None, :]),
                          ("dynamic", dyn, P - P.mean(axis=0))):
        lm = localmed(ps, res)
        with np.errstate(invalid="ignore", divide="ignore"):
            snr = ps / np.where(lm > 0, lm, np.nan)
        sub = np.nan_to_num(snr[lo:hi])
        order = list(np.argsort(sub)[::-1] + lo)
        peaks = []
        for o in order:
            if all(abs(1/freqs[o] - 1/freqs[q]) > 0.08*(1/freqs[q]) for q in peaks):
                peaks.append(int(o))
            if len(peaks) == 4:
                break
        j = peaks[0]; per = 1.0/freqs[j]
        a = amp_at(src, per, M)
        print(f"  {name:16s} peak {per:7.2f}px SNR={snr[j]:6.2f} amp={a:.4f}LSB || " +
              ", ".join(f"{1/freqs[q]:.2f}px SNR{snr[q]:.2f} amp{amp_at(src,1/freqs[q],M):.3f}"
                        for q in peaks[1:]))
        out[name] = (per, float(snr[j]), a, j)

    print(f"  RMS: detrended={D.std():.4f} static(temporal mean)={mp.std():.4f} "
          f"dynamic={(D-mp).std():.4f} LSB")

    per, snr, a, j = out["incoherent"]
    k = j * M / NPAD
    e = np.exp(-2j*np.pi*k*np.arange(M)/M) * win
    c = (D * e).sum(axis=1)
    ph = np.unwrap(np.angle(c)); mag = np.abs(c)
    good = mag > np.percentile(mag, 50)
    t = np.arange(nf)[good]
    if len(t) > 30:
        sl, ic = np.polyfit(t, ph[good], 1)
        rr = ph[good] - (sl*t + ic)
        drift = -sl/(2*np.pi)*per
        print(f"  PHASE@{per:.2f}px slope={sl:+.5f}rad/frame -> {drift:+.5f}px/frame "
              f"({drift*fps:+.3f}px/s) resid_sd={rr.std():.3f}rad |c|cv={mag.std()/mag.mean():.2f}")
    return out


def load(key):
    f2, f1 = f"{O}/{key}_p2.npz", f"{O}/{key}_p1.npz"
    if os.path.exists(f2):
        d = np.load(f2)
        return d["rowprof"], f"rect cols {d['rect'][0]}..{d['rect'][1]}"
    d = np.load(f1)
    return d["rowmean"], "full width"


if __name__ == "__main__":
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    for key, (fps, R0, R1) in CFG.items():
        if only and key not in only:
            continue
        try:
            Pin, tag = load(key)
        except FileNotFoundError:
            continue
        analyse(key, Pin, fps, R0, R1, tag)
