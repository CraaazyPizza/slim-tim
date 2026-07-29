#!/usr/bin/env python3.12
"""
Test the Getty stock-clip audio against the Skinny Bob projector tracks.

Replicates the two measurements from FINDINGS.md:
  §5  -- envelope-modulation peak (expect 12-14 Hz) and 99.9% spectral edge (expect ~7 kHz)
  §5b -- sliding 2 s log-spectrogram fingerprint, 48 log-bands 50 Hz-7 kHz, best cosine
"""
import subprocess, json
import numpy as np

SR = 48000

TRACKS = {
    "getty_104161830":  "analysis/prior-work/gettyimages-104161830-640_adpp.mp4",
    "getty_160602429":  "analysis/prior-work/gettyimages-160602429-640_adpp.mp4",
    "2011_RsQCX":       "videos/2011/RsQCXN4o4Ps.mkv",
    "2011_ZB788":       "videos/2011/ZB788PtqQvg.mkv",
    "2026_v1":          "videos/2026/OpSTlDJWFFI.mkv",
    "2026_v2":          "videos/2026/Oqw96jCOP7A.mkv",
}


def load(path):
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-vn",
           "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def env_mod(x):
    """Amplitude-envelope modulation spectrum: peak Hz + prominence over local median."""
    # rectify + smooth to ~1 kHz envelope, then decimate to 400 Hz
    e = np.abs(x)
    k = SR // 1000
    e = np.convolve(e, np.ones(k) / k, mode="same")[::SR // 400]
    fs = 400.0
    e = e - e.mean()
    if len(e) < 256:
        return None
    w = np.hanning(len(e))
    f = np.fft.rfftfreq(len(e), 1 / fs)
    p = np.abs(np.fft.rfft(e * w)) ** 2
    band = (f >= 4) & (f <= 40)
    if band.sum() < 8:
        return None
    i = np.argmax(p[band])
    pk_f = f[band][i]
    pk_p = p[band][i]
    med = np.median(p[(f >= 4) & (f <= 60)])
    return {"peak_hz": round(float(pk_f), 2),
            "prominence_x": round(float(pk_p / (med + 1e-20)), 1)}


def spectral_edge(x, q=0.999):
    """Frequency below which q of the total spectral energy sits."""
    n = 1 << 15
    acc = np.zeros(n // 2 + 1)
    hop = n
    cnt = 0
    for i in range(0, len(x) - n, hop):
        seg = x[i:i + n] * np.hanning(n)
        acc += np.abs(np.fft.rfft(seg)) ** 2
        cnt += 1
    if not cnt:
        return None
    f = np.fft.rfftfreq(n, 1 / SR)
    c = np.cumsum(acc) / acc.sum()
    return round(float(f[np.searchsorted(c, q)]), 0)


def fingerprint(x, win=2.0, hop=0.5):
    """Sliding 2 s log-spectrogram, 48 log-spaced bands 50 Hz - 7 kHz, L2-normalised."""
    n = int(win * SR)
    h = int(hop * SR)
    edges = np.geomspace(50, 7000, 49)
    f = np.fft.rfftfreq(n, 1 / SR)
    idx = [np.where((f >= edges[i]) & (f < edges[i + 1]))[0] for i in range(48)]
    out = []
    for i in range(0, len(x) - n, h):
        seg = x[i:i + n] * np.hanning(n)
        p = np.abs(np.fft.rfft(seg)) ** 2
        if p.sum() <= 0:
            continue
        v = np.array([np.log10(p[j].mean() + 1e-20) if len(j) else -20.0 for j in idx])
        v = v - v.mean()
        nv = np.linalg.norm(v)
        if nv > 0:
            out.append(v / nv)
    return np.array(out)


if __name__ == "__main__":
    sig, fps_ = {}, {}
    res = {}
    for k, p in TRACKS.items():
        x = load(p)
        if x.size == 0 or np.allclose(x, 0):
            res[k] = {"audio": "silent/absent"}
            continue
        sig[k] = x
        res[k] = {
            "dur_s": round(len(x) / SR, 2),
            "peak": round(float(np.abs(x).max()), 3),
            "rms": round(float(np.sqrt((x ** 2).mean())), 5),
            "env_mod": env_mod(x),
            "edge_99.9_Hz": spectral_edge(x),
        }
        print(k, json.dumps(res[k]), flush=True)

    print("\n--- fingerprint cosine (best over all window pairs) ---")
    fp = {k: fingerprint(v) for k, v in sig.items()}
    keys = list(fp)
    M = {}
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            A, B = fp[a], fp[b]
            if len(A) == 0 or len(B) == 0:
                continue
            C = A @ B.T
            M[f"{a} <-> {b}"] = [round(float(C.max()), 3), round(float(np.median(C)), 3)]
            print(f"{a:18s} <-> {b:18s} best={C.max():.3f}  median={np.median(C):.3f}")
    json.dump({"per_track": res, "cosine_best_median": M},
              open("audio_test.json", "w"), indent=1)
