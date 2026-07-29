#!/usr/bin/env python3.12
"""Horizontal banding analysis, v2.

Row-mean luma profile per frame -> high-pass detrend -> Hann window -> FFT down
the row axis.  Three spectra:
  incoherent : mean |F|^2 over frames         (banding present even if phase drifts)
  static     : |F|^2 of the temporal-mean prof (fixed banding / baked-in overlay)
  dynamic    : mean |F|^2 of (prof - temporal mean) (rolling / moving banding)

Baseline for significance is a LOG-FREQUENCY-local median (window f/1.35..f*1.35,
guard f/1.06..f*1.06) computed on independent bins only, so a steep 1/f^a
continuum does not manufacture fake SNR.  Amplitude in 8-bit luma code values =
sqrt(2)*RMS of a +-2.5 resolution-element bandpass of the unwindowed profile.
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
HP = int(os.environ.get("HP", 121))
PMIN = float(os.environ.get("PMIN", 2.05))
PMAX = float(os.environ.get("PMAX", 100))
PADF = 8            # zero-pad factor


def highpass(P, k):
    ker = np.ones(k) / k
    pad = np.pad(P, ((0, 0), (k // 2, k // 2)), mode="reflect")
    return P - np.stack([np.convolve(r, ker, mode="valid") for r in pad])


def logbaseline(f, ps, lo_r=1.35, guard=1.06):
    out = np.full(len(ps), np.nan)
    for i in range(1, len(ps)):
        fi = f[i]
        m = (f >= fi/lo_r) & (f <= fi*lo_r) & ~((f >= fi/guard) & (f <= fi*guard))
        if m.sum() >= 4:
            out[i] = np.median(ps[m])
    return out


def amp_at(P, per, M):
    n = P.shape[-1]
    f = np.fft.rfftfreq(n)
    F = np.fft.rfft(P, axis=-1)
    keep = np.abs(f - 1.0/per) <= 2.5/M
    bp = np.fft.irfft(np.where(keep, F, 0), n=n, axis=-1)
    return float(np.sqrt(2)*np.atleast_1d(bp.std(axis=-1)).mean())


def analyse(key, Pin, fps, R0, R1, tag, frames=None, dump=False):
    P = Pin[:, R0:R1].astype(np.float64)
    if frames is not None:
        P = P[frames]
    nf, M = P.shape
    D = highpass(P, HP)
    win = np.hanning(M)
    NP = M*PADF
    f = np.fft.rfftfreq(NP)
    step = PADF                        # independent-bin stride
    mp = D.mean(axis=0)
    S = {"incoherent": np.abs(np.fft.rfft(D*win, n=NP, axis=-1)).__pow__(2).mean(axis=0),
         "static":     np.abs(np.fft.rfft(mp*win, n=NP))**2,
         "dynamic":    np.abs(np.fft.rfft((D-mp)*win, n=NP, axis=-1)).__pow__(2).mean(axis=0)}
    SRC = {"incoherent": P, "static": P.mean(axis=0)[None, :], "dynamic": P-P.mean(axis=0)}
    print(f"\n===== {key} [{tag}] rows {R0}..{R1} ({M}) nf={nf} {fps:.3f}fps "
          f"HP={HP} band={PMIN}-{PMAX}px")
    out = {}
    for name in ("incoherent", "static", "dynamic"):
        ps = S[name]
        bl = logbaseline(f, ps)
        with np.errstate(invalid="ignore", divide="ignore"):
            snr = ps/bl
        band = (f >= 1.0/PMAX) & (f <= 1.0/PMIN) & np.isfinite(snr)
        idx = np.where(band)[0]
        srt = idx[np.argsort(snr[idx])[::-1]]
        peaks = []
        for o in srt:
            if all(abs(1/f[o] - 1/f[q]) > 0.08*(1/f[q]) for q in peaks):
                peaks.append(int(o))
            if len(peaks) == 4:
                break
        txt = ", ".join(f"{1/f[q]:7.2f}px SNR={snr[q]:6.2f} amp={amp_at(SRC[name],1/f[q],M):.4f}"
                        for q in peaks)
        print(f"  {name:11s}: {txt}")
        out[name] = (1/f[peaks[0]], float(snr[peaks[0]]),
                     amp_at(SRC[name], 1/f[peaks[0]], M), peaks[0])
        if dump and name == "incoherent":
            print("    independent-bin spectrum (period px : SNR):")
            row = []
            for i in idx[::step]:
                row.append(f"{1/f[i]:6.1f}:{snr[i]:5.2f}")
            for a in range(0, len(row), 8):
                print("      " + "  ".join(row[a:a+8]))
    print(f"  RMS: detrended={D.std():.4f} static={mp.std():.4f} "
          f"dynamic={(D-mp).std():.4f} LSB")

    # ---- phase drift at the strongest incoherent peak
    per, snr, a, j = out["incoherent"]
    kk = j*M/NP
    e = np.exp(-2j*np.pi*kk*np.arange(M)/M)*win
    c = (D*e).sum(axis=1)
    ph = np.unwrap(np.angle(c)); mag = np.abs(c)
    good = mag > np.percentile(mag, 50)
    t = np.arange(nf)[good]
    if len(t) > 30:
        sl, ic = np.polyfit(t, ph[good], 1)
        rr = ph[good]-(sl*t+ic)
        drift = -sl/(2*np.pi)*per
        # frame-to-frame phase increment (robust to unwrap failures)
        dph = np.angle(c[1:]*np.conj(c[:-1]))
        print(f"  PHASE@{per:.2f}px: linear slope {sl:+.5f} rad/fr -> {drift:+.5f} px/fr "
              f"({drift*fps:+.3f} px/s), resid sd={rr.std():.3f} rad; "
              f"median frame-to-frame dphi={np.median(dph):+.4f} rad "
              f"({-np.median(dph)/(2*np.pi)*per:+.4f} px/fr), IQR={np.subtract(*np.percentile(dph,[75,25])):.3f}; "
              f"|c| cv={mag.std()/mag.mean():.2f}")
    return out


def load(key):
    f2, f1 = f"{O}/{key}_p2.npz", f"{O}/{key}_p1.npz"
    if os.path.exists(f2):
        d = np.load(f2)
        return d["rowprof"], f"rect cols {d['rect'][0]}..{d['rect'][1]}"
    d = np.load(f1)
    return d["rowmean"], "FULL WIDTH (p1 fallback)"


if __name__ == "__main__":
    dump = "--dump" in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    for key, (fps, R0, R1) in CFG.items():
        if only and key not in only:
            continue
        try:
            Pin, tag = load(key)
        except FileNotFoundError:
            continue
        analyse(key, Pin, fps, R0, R1, tag, dump=dump)
