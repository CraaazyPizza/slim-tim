#!/usr/bin/env python3.12
"""
Probe all seven Skinny Bob videos for observables that map 1:1 onto
Boris FX Sapphire S_FilmDamage parameter groups.

Groups tested:
  Flicker  -> global luma modulation: Random Amplitude/Frequency + Wave Amplitude/Frequency
  Shake    -> global image translation inside the gate: Amplitude/Frequency/Jumpiness
  Vignette -> radial luma falloff: Darkness/Radius/Edge Softness
  Grain    -> Mono flag: inter-channel correlation of temporal high-pass noise
  Dust/Stains -> Print/Negative ratio: dark vs bright transient blob counts
  Defocus  -> Random Amplitude/Frequency: per-frame HF energy modulation
"""
import subprocess, sys, json, os
import numpy as np

W, H = 480, 270          # working resolution for global stats
VIDS = [
    ("2026-v1", "videos/2026/OpSTlDJWFFI.mkv", 30000/1001),
    ("2026-v2", "videos/2026/Oqw96jCOP7A.mkv", 30000/1001),
    ("2026-v3", "videos/2026/l9RAhmPHM_A.mkv", 30000/1001),
    ("2011-ZB788", "videos/2011/ZB788PtqQvg.mkv", 25.0),
    ("2011-RsQCX", "videos/2011/RsQCXN4o4Ps.mkv", 25.0),
    ("2011-Xju",   "videos/2011/Xju_CY5ZESA.mkv", 25.0),
    ("2011-a6TL",  "videos/2011/a6TLGkrfNKI.mkv", 25.0),
]


def decode(path, w, h, pix="gray"):
    """Decode whole video to a numpy stack at w x h."""
    bpp = {"gray": 1, "rgb24": 3}[pix]
    cmd = ["ffmpeg", "-v", "error", "-i", path,
           "-vf", f"scale={w}:{h}", "-pix_fmt", pix, "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    n = len(raw) // (w * h * bpp)
    a = np.frombuffer(raw[:n * w * h * bpp], np.uint8)
    return a.reshape(n, h, w, bpp).squeeze()


def psd(x, fps):
    """Welch-ish PSD of a detrended 1-D signal. Returns (freqs, power)."""
    x = np.asarray(x, float)
    x = x - np.mean(x)
    n = len(x)
    if n < 64:
        return np.array([]), np.array([])
    win = np.hanning(n)
    f = np.fft.rfftfreq(n, 1.0 / fps)
    p = np.abs(np.fft.rfft(x * win)) ** 2
    return f, p


def peak_report(f, p, fmin=0.3):
    """Strongest spectral line above fmin, and how far it stands above the local median."""
    if len(f) == 0:
        return None
    m = f >= fmin
    if m.sum() < 8:
        return None
    ff, pp = f[m], p[m]
    med = np.median(pp)
    i = int(np.argmax(pp))
    return {"peak_hz": round(float(ff[i]), 3),
            "ratio_to_median": round(float(pp[i] / (med + 1e-12)), 1)}


def interior_mask(h, w, frac=0.60):
    """Central region, avoiding gate matte, redaction bars and burned-in timecode."""
    m = np.zeros((h, w), bool)
    y0, y1 = int(h * (0.5 - frac / 2)), int(h * (0.5 + frac / 2))
    x0, x1 = int(w * (0.5 - frac / 2)), int(w * (0.5 + frac / 2))
    m[y0:y1, x0:x1] = True
    return m


def phase_shift(a, b):
    """Sub-pixel-ish global translation between two frames via phase correlation."""
    A = np.fft.rfft2(a - a.mean())
    B = np.fft.rfft2(b - b.mean())
    R = A * np.conj(B)
    R /= np.abs(R) + 1e-9
    c = np.fft.irfft2(R, s=a.shape)
    iy, ix = np.unravel_index(np.argmax(c), c.shape)
    dy = iy - a.shape[0] if iy > a.shape[0] // 2 else iy
    dx = ix - a.shape[1] if ix > a.shape[1] // 2 else ix
    return float(dx), float(dy)


def analyse(name, path, fps):
    out = {"video": name, "fps": round(fps, 3)}
    g = decode(path, W, H, "gray").astype(np.float32)
    nfr = len(g)
    out["frames"] = nfr

    mask = interior_mask(H, W)
    lum = g[:, mask].mean(axis=1)

    # --- shot segmentation: big luma jumps split clips ---
    d = np.abs(np.diff(lum))
    cuts = [0] + list(np.where(d > 6.0)[0] + 1) + [nfr]
    segs = [(a, b) for a, b in zip(cuts[:-1], cuts[1:]) if b - a >= 90]
    out["long_segments"] = len(segs)

    # ---------- FLICKER ----------
    fl = []
    for a, b in segs:
        s = lum[a:b]
        s = s - np.convolve(s, np.ones(31) / 31, mode="same")  # remove slow drift
        s = s[15:-15]
        f, p = psd(s, fps)
        pr = peak_report(f, p)
        if pr:
            pr["seg"] = [int(a), int(b)]
            pr["rms_DN"] = round(float(np.std(s)), 3)
            fl.append(pr)
    fl.sort(key=lambda r: -r["ratio_to_median"])
    out["flicker"] = fl[:3]

    # ---------- SHAKE ----------
    cy, cx = H // 2, W // 2
    crop = g[:, cy - 96:cy + 96, cx - 96:cx + 96]
    dxs, dys = [], []
    for a, b in segs:
        for i in range(a + 1, min(b, a + 400)):
            dx, dy = phase_shift(crop[i - 1], crop[i])
            if abs(dx) < 20 and abs(dy) < 20:
                dxs.append(dx); dys.append(dy)
    if dxs:
        out["shake"] = {
            "n": len(dxs),
            "rms_dx_px": round(float(np.std(dxs)), 3),
            "rms_dy_px": round(float(np.std(dys)), 3),
            "frac_zero_motion": round(float(np.mean((np.abs(dxs) < .5) & (np.abs(dys) < .5))), 3),
        }
        f, p = psd(dys, fps)
        out["shake"]["dy_spectrum"] = peak_report(f, p)

    # ---------- VIGNETTE ----------
    bright = np.argsort(lum)[-max(8, nfr // 100):]
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((yy - H / 2) / (H / 2)) ** 2 + ((xx - W / 2) / (W / 2)) ** 2)
    prof = []
    stack = g[bright].mean(axis=0)
    for lo in np.arange(0, 1.0, 0.1):
        sel = (r >= lo) & (r < lo + 0.1)
        prof.append(round(float(stack[sel].mean()), 1))
    c = prof[0] if prof[0] else 1.0
    out["vignette_radial_profile"] = prof
    out["vignette_edge_over_center"] = round(prof[-2] / (c + 1e-9), 3)

    # ---------- GRAIN MONO ----------
    rgb = decode(path, 160, 90, "rgb24").astype(np.float32)
    n2 = min(len(rgb), nfr)
    hp = rgb[1:n2] - rgb[:n2 - 1]              # temporal high-pass
    R, G, B = hp[..., 0].ravel(), hp[..., 1].ravel(), hp[..., 2].ravel()
    def corr(a, b):
        return round(float(np.corrcoef(a, b)[0, 1]), 3)
    out["grain_channel_corr"] = {"RG": corr(R, G), "RB": corr(R, B), "GB": corr(G, B)}

    # ---------- DUST / STAINS polarity ----------
    dark = brightc = 0
    step = max(1, nfr // 300)
    idx = range(2, nfr - 2, step)
    for i in idx:
        ref = np.median(g[[i - 2, i - 1, i + 1, i + 2]], axis=0)
        diff = g[i] - ref
        d_in = diff[mask]
        sd = np.std(d_in) + 1e-6
        dark += int(np.sum(d_in < -6 * sd))
        brightc += int(np.sum(d_in > 6 * sd))
    tot = dark + brightc
    out["transient_marks"] = {
        "sampled_frames": len(list(idx)),
        "dark_px": dark, "bright_px": brightc,
        "print_negative_ratio": round(dark / (brightc + 1e-9), 2) if tot else None,
    }

    # ---------- DEFOCUS ----------
    lap = np.abs(np.diff(g, axis=2)).mean(axis=(1, 2))
    dfl = []
    for a, b in segs:
        s = lap[a:b]
        s = s - np.convolve(s, np.ones(31) / 31, mode="same")
        s = s[15:-15]
        f, p = psd(s, fps)
        pr = peak_report(f, p)
        if pr:
            dfl.append(pr)
    dfl.sort(key=lambda r: -r["ratio_to_median"])
    out["defocus"] = dfl[:2]
    return out


if __name__ == "__main__":
    res = []
    for name, path, fps in VIDS:
        if not os.path.exists(path):
            print(f"missing {path}", file=sys.stderr); continue
        try:
            r = analyse(name, path, fps)
        except Exception as e:
            r = {"video": name, "error": repr(e)}
        res.append(r)
        print(json.dumps(r), flush=True)
    json.dump(res, open("sapphire_probe.json", "w"), indent=1)
