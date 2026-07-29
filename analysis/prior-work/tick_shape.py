#!/usr/bin/env python3.12
"""
Speed-invariant fingerprint of the projector tick.

Playing a recording slower scales the fundamental AND every harmonic by the
same factor, so the RATIOS h2/h1, h3/h1, h4/h1 of the amplitude-modulation
spectrum are invariant to the slowdown. They describe the SHAPE of one tick
(sharp click vs soft thump vs double-strike), which is a property of the
specific mechanism and recording -- not of playback speed.

If the Skinny Bob track is Getty 104161830 slowed down, the harmonic ratios
must agree. If they don't, no choice of speed can reconcile them.
"""
import subprocess, json
import numpy as np

SR = 48000
TRACKS = {
    "getty_104161830": "analysis/prior-work/gettyimages-104161830-640_adpp.mp4",
    "getty_160602429": "analysis/prior-work/gettyimages-160602429-640_adpp.mp4",
    "2011_RsQCX": "videos/2011/RsQCXN4o4Ps.mkv",
    "2011_ZB788": "videos/2011/ZB788PtqQvg.mkv",
    "2026_v1": "videos/2026/OpSTlDJWFFI.mkv",
    "2026_v2": "videos/2026/Oqw96jCOP7A.mkv",
}


def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-vn", "-ac", "1",
                          "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def mod_spectrum(x, fs_env=800.0):
    """Amplitude-envelope spectrum out to 400 Hz."""
    e = np.abs(x)
    k = SR // 2000
    e = np.convolve(e, np.ones(k) / k, mode="same")[::int(SR / fs_env)]
    e = e - e.mean()
    w = np.hanning(len(e))
    f = np.fft.rfftfreq(len(e), 1 / fs_env)
    p = np.abs(np.fft.rfft(e * w))
    return f, p


def harmonics(f, p, f0_lo=3, f0_hi=40, nh=5):
    b = (f >= f0_lo) & (f <= f0_hi)
    f0 = f[b][np.argmax(p[b])]
    amps = []
    for h in range(1, nh + 1):
        target = f0 * h
        if target > f[-1]:
            amps.append(0.0); continue
        w = (f > target - 1.2) & (f < target + 1.2)
        amps.append(float(p[w].max()) if w.any() else 0.0)
    a = np.array(amps)
    return float(f0), (a / (a[0] + 1e-20)).round(3)


def tick_profile(x, f0):
    """Average one modulation period of the envelope -> the shape of a single tick."""
    fs_env = 2000.0
    e = np.abs(x)
    k = SR // 4000
    e = np.convolve(e, np.ones(k) / k, mode="same")[::int(SR / fs_env)]
    per = fs_env / f0
    n = int(per)
    m = len(e) // n
    if m < 8:
        return None
    prof = e[:m * n].reshape(m, n).mean(axis=0)
    prof = prof - prof.min()
    prof = prof / (prof.max() + 1e-20)
    # resample to 64 points so profiles of different periods are comparable
    xi = np.linspace(0, n - 1, 64)
    prof = np.interp(xi, np.arange(n), prof)
    # rotate so the peak sits at index 0
    prof = np.roll(prof, -int(np.argmax(prof)))
    return prof


if __name__ == "__main__":
    res, profs = {}, {}
    for k, p in TRACKS.items():
        x = load(p)
        if x.size == 0 or np.allclose(x, 0):
            continue
        f, ps = mod_spectrum(x)
        f0, hr = harmonics(f, ps)
        pr = tick_profile(x, f0)
        profs[k] = pr
        # duty: fraction of the period above half the peak
        duty = float((pr > 0.5).mean()) if pr is not None else None
        res[k] = {"f0_Hz": round(f0, 2),
                  "harmonic_ratios_h1..h5": hr.tolist(),
                  "tick_duty_above_half": round(duty, 3) if duty else None}
        print(f"{k:18s} f0={f0:6.2f} Hz  h2..h5/h1={hr[1:].tolist()}  duty={duty:.3f}")

    print("\n--- tick-profile correlation (speed-invariant) ---")
    ks = list(profs)
    for i, a in enumerate(ks):
        for b in ks[i + 1:]:
            if profs[a] is None or profs[b] is None:
                continue
            c = float(np.corrcoef(profs[a], profs[b])[0, 1])
            print(f"  {a:18s} <-> {b:18s} r={c:+.3f}")
    json.dump(res, open("tick_shape.json", "w"), indent=1)
