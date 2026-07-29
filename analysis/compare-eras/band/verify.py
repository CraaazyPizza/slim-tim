#!/usr/bin/env python3.12
"""(a) Independent cross-check: recompute row-mean profile spectra from the
    pre-extracted PNG frames (separate decode path) and compare with the raw-YUV
    result for the same frames.
(b) Drift analysis on the strongest sliding-window banding candidates found by
    lowband.py, using a strictly local time window."""
import numpy as np, os
from PIL import Image
O = "/home/user/new-skinny-bob/analysis/compare-eras/band"
B = "/home/user/new-skinny-bob"
PNG = {"OpSTlDJWFFI": f"{B}/frames/OpSTlDJWFFI",
       "Oqw96jCOP7A": f"{B}/frames/Oqw96jCOP7A",
       "l9RAhmPHM_A": f"{B}/frames/l9RAhmPHM_A",
       "ZB788PtqQvg": f"{B}/frames/ZB788PtqQvg",
       "RsQCXN4o4Ps": f"{B}/frames/RsQCXN4o4Ps",
       "Xju_CY5ZESA": f"{B}/frames/Xju_CY5ZESA",
       "a6TLGkrfNKI": f"{B}/frames/a6TLGkrfNKI"}

print("=== (a) PNG vs raw-YUV row profile cross-check "
      "(BT.709 luma from RGB vs coded Y; correlation of the detrended profiles)")
for k, dirp in PNG.items():
    d2 = np.load(f"{O}/{k}_p2.npz")
    C0, C1, R0, R1 = d2["rect"]
    fno = 1500 if os.path.exists(f"{dirp}/f01500.png") else 700
    im = np.asarray(Image.open(f"{dirp}/f{fno:05d}.png").convert("RGB")).astype(np.float64)
    lum = 0.2126*im[..., 0]+0.7152*im[..., 1]+0.0722*im[..., 2]
    pp = lum[:, C0:C1].mean(axis=1)
    py = d2["rowprof"][fno-1].astype(np.float64)
    def hp(x, k=41):
        pad = np.pad(x, k//2, mode="reflect")
        return x - np.convolve(pad, np.ones(k)/k, mode="valid")
    a, b = hp(pp[R0:R1]), hp(py[R0:R1])
    r = np.corrcoef(a, b)[0, 1]
    print(f"  {k:12s} f{fno:05d}: corr(detrended PNG-luma, coded-Y)={r:+.4f}  "
          f"RMS PNG={a.std():.4f} RMS Y={b.std():.4f}  (gain {a.std()/b.std():.3f})")

print("\n=== (b) drift on strongest local episodes")
EP = [("OpSTlDJWFFI", 30000/1001, 120, 900, 86.0, 92.0, 178.0),
      ("RsQCXN4o4Ps", 25.0, 120, 900, 51.0, 58.0, 127.0),
      ("ZB788PtqQvg", 25.0, 120, 900, 35.0, 40.0, 83.0),
      ("Oqw96jCOP7A", 30000/1001, 120, 900, 76.0, 80.0, 80.0),
      ("a6TLGkrfNKI", 25.0, 60, 420, 73.0, 78.0, 80.0)]
for k, fps, R0, R1, t0, t1, per in EP:
    d = np.load(f"{O}/{k}_p2.npz")
    P = d["rowprof"][int(t0*fps):int(t1*fps), R0:R1].astype(np.float64)
    M = R1-R0
    x = np.linspace(-1, 1, M)
    A = np.vstack([x**i for i in range(5)]).T
    c, *_ = np.linalg.lstsq(A, P.T, rcond=None)
    D = P-(A@c).T
    win = np.hanning(M)
    e = np.exp(-2j*np.pi*np.arange(M)/per)*win
    z = D @ e
    dph = np.angle(z[1:]*np.conj(z[:-1]))
    amp = 2*np.abs(z)/win.sum()
    print(f"  {k:12s} t={t0:.0f}-{t1:.0f}s @ {per:.0f}px: amp={amp.mean():.3f}"
          f"+-{amp.std():.3f} LSB; median dphi={np.median(dph):+.4f} rad "
          f"-> {-np.median(dph)/(2*np.pi)*per:+.3f} px/frame "
          f"({-np.median(dph)/(2*np.pi)*per*fps:+.2f} px/s); "
          f"circ. concentration of dphi = {abs(np.mean(np.exp(1j*dph))):.3f} "
          f"(1=perfectly steady roll, 0=random)")
