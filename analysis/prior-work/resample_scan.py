#!/usr/bin/env python3.12
"""
Is the Skinny Bob projector track the Getty 104161830 audio played slow?

Slowing audio by factor r scales BOTH the mechanical tick rate and the whole
spectrum by r. Getty ticks at 24.0 Hz with a 99.9% edge at 11372 Hz; the SB
tracks tick at 12-14 Hz with edges at 6.5-7.9 kHz. If SB = Getty x r, one
single r must explain both at once.

Scan r, resample, and score the long-term average spectrum against each SB
track. A real match shows a sharp peak in the correlation curve at the r that
also puts the tick rate on target.
"""
import subprocess, json
import numpy as np
from scipy.signal import resample_poly
from fractions import Fraction

SR = 48000


def load(path):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1",
         "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def ltas(x, lo=50, hi=9000, nb=96):
    """Long-term average log spectrum in nb log-spaced bands, mean-removed + L2."""
    n = 1 << 14
    acc = np.zeros(n // 2 + 1)
    c = 0
    for i in range(0, len(x) - n, n // 2):
        acc += np.abs(np.fft.rfft(x[i:i + n] * np.hanning(n))) ** 2
        c += 1
    if c == 0:
        return None
    f = np.fft.rfftfreq(n, 1 / SR)
    edges = np.geomspace(lo, hi, nb + 1)
    v = []
    for i in range(nb):
        m = (f >= edges[i]) & (f < edges[i + 1])
        v.append(np.log10(acc[m].mean() + 1e-30) if m.any() else -30.0)
    v = np.array(v)
    v -= v.mean()
    return v / (np.linalg.norm(v) + 1e-12)


def env_peak(x):
    e = np.abs(x)
    k = SR // 1000
    e = np.convolve(e, np.ones(k) / k, mode="same")[::SR // 400]
    fs = 400.0
    e = e - e.mean()
    w = np.hanning(len(e))
    f = np.fft.rfftfreq(len(e), 1 / fs)
    p = np.abs(np.fft.rfft(e * w)) ** 2
    b = (f >= 3) & (f <= 40)
    i = np.argmax(p[b])
    med = np.median(p[(f >= 3) & (f <= 60)])
    return round(float(f[b][i]), 2), round(float(p[b][i] / (med + 1e-20)), 1)


def slow(x, r):
    """Play x at r times speed (r<1 = slower). Frequencies scale by r."""
    fr = Fraction(r).limit_denominator(400)
    return resample_poly(x, fr.denominator, fr.numerator)


SB = {"2011_RsQCX": "videos/2011/RsQCXN4o4Ps.mkv",
      "2011_ZB788": "videos/2011/ZB788PtqQvg.mkv",
      "2026_v1": "videos/2026/OpSTlDJWFFI.mkv",
      "2026_v2": "videos/2026/Oqw96jCOP7A.mkv"}

if __name__ == "__main__":
    g = load("analysis/prior-work/gettyimages-104161830-640_adpp.mp4")
    g2 = load("analysis/prior-work/gettyimages-160602429-640_adpp.mp4")
    sb = {k: ltas(load(p)) for k, p in SB.items()}

    # control: white noise and a shuffled-phase version of getty, same treatment
    rng = np.random.default_rng(0)
    ctl = {"white_noise": ltas(rng.standard_normal(SR * 15))}

    out = {}
    for gname, gs in (("getty_104161830", g), ("getty_160602429", g2)):
        rows = []
        for r in np.arange(0.30, 1.02, 0.01):
            y = slow(gs, float(r))
            v = ltas(y)
            if v is None:
                continue
            row = {"r": round(float(r), 2)}
            for k in SB:
                row[k] = round(float(v @ sb[k]), 3)
            row["white_noise"] = round(float(v @ ctl["white_noise"]), 3)
            rows.append(row)
        out[gname] = rows
        print(f"\n===== {gname} =====")
        print("  r    " + "".join(f"{k:>12s}" for k in list(SB) + ["white_noise"]))
        best = {k: max(rows, key=lambda z: z[k]) for k in SB}
        for row in rows:
            if round(row["r"] * 100) % 5 == 0:
                print(f" {row['r']:.2f} " + "".join(f"{row[k]:12.3f}" for k in list(SB) + ["white_noise"]))
        print(" -- best r per track --")
        for k, b in best.items():
            y = slow(gs, b["r"])
            pk, prom = env_peak(y)
            print(f"   {k:12s} best r={b['r']:.2f} cos={b[k]:.3f}   "
                  f"tick@r={pk} Hz (prom {prom}x)")
        json.dump(out, open("resample_scan.json", "w"), indent=1)

    print("\n--- reference: unmodified tick rates ---")
    for nm, s in (("getty_104161830", g), ("getty_160602429", g2)):
        print(f"  {nm}: {env_peak(s)}")
    for k, p in SB.items():
        print(f"  {k}: {env_peak(load(p))}")
