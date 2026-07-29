#!/usr/bin/env python3.12
"""Affine-invariant (ASIFT-style) search for the glyph in EVERY frame of the shot.

The reference glyph patch is simulated under a grid of out-of-plane tilts and
in-plane rotations; SIFT descriptors from all simulations are pooled.  Each frame
is then matched against the pool without any prior on viewing angle, so a
strongly foreshortened appearance of the glyph would be found just as readily as
a fronto-parallel one.  For every frame with a match we log the recovered
scale, in-plane rotation and anisotropy (= foreshortening).
"""
import numpy as np, cv2, json
from scipy.linalg import polar

FR = "/home/user/new-skinny-bob/frames/l9RAhmPHM_A/f%05d.png"
OUT = "/home/user/new-skinny-bob/analysis/symbol-panel/"
PB = (263, 60, 1561, 1043)
REF = 1694
GBOX = (420, 500, 620, 745)              # glyph patch in ref picture coords
TCM = (469 - PB[0], 938 - PB[1], 968 - PB[0], 1002 - PB[1])


def load(i):
    a = cv2.imread(FR % i, cv2.IMREAD_GRAYSCALE).astype(np.float32)
    return a[PB[1]:PB[3], PB[0]:PB[2]]


def prep(c):
    bg = cv2.GaussianBlur(c, (0, 0), 25)
    d = np.clip((c - bg) / (4 * np.std(c - bg) + 1e-6) + 0.5, 0, 1)
    u = (d * 255).astype(np.uint8)
    if u.shape[0] > TCM[3]:
        u[TCM[1]:TCM[3], TCM[0]:TCM[2]] = 128
    return u


def affine_skew(tilt, phi, img):
    """standard ASIFT simulation; returns warped image and the 2x3 affine Ai (img->warp)"""
    h, w = img.shape
    A = np.float32([[1, 0, 0], [0, 1, 0]])
    out = img
    if phi != 0.0:
        p = np.deg2rad(phi)
        s, c = np.sin(p), np.cos(p)
        A = np.float32([[c, -s], [s, c]])
        corners = np.float32([[0, 0], [w, 0], [w, h], [0, h]]) @ A.T
        x, y, w2, h2 = cv2.boundingRect(np.int32(corners.reshape(1, -1, 2)))
        A = np.hstack([A, [[-x], [-y]]])
        out = cv2.warpAffine(out, A, (w2, h2), flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_REPLICATE)
    if tilt != 1.0:
        s = 0.8 * np.sqrt(tilt * tilt - 1)
        out = cv2.GaussianBlur(out, (0, 0), sigmaX=s, sigmaY=0.01)
        out = cv2.resize(out, (0, 0), fx=1.0 / tilt, fy=1.0, interpolation=cv2.INTER_NEAREST)
        A[0] /= tilt
    return out, A


def main():
    sift = cv2.SIFT_create(nfeatures=3000)
    bf = cv2.BFMatcher()
    ra = prep(load(REF))
    patch = ra[GBOX[1]:GBOX[3], GBOX[0]:GBOX[2]]
    pool_desc, pool_pt = [], []
    for tilt in (1.0, 1.4, 2.0, 2.8, 4.0):
        phis = [0.0] if tilt == 1.0 else list(np.arange(0, 180, 72.0 / tilt))
        for phi in phis:
            w, A = affine_skew(tilt, phi, patch)
            k, d = sift.detectAndCompute(w, None)
            if d is None:
                continue
            Ai = cv2.invertAffineTransform(A)
            pts = cv2.transform(np.float32([kp.pt for kp in k]).reshape(-1, 1, 2), Ai)[:, 0, :]
            pts += np.float32([GBOX[0], GBOX[1]])
            pool_desc.append(d); pool_pt.append(pts)
    D = np.vstack(pool_desc); P = np.vstack(pool_pt)
    print("pooled template descriptors:", len(D))
    ctr = np.float32([[[(GBOX[0] + GBOX[2]) / 2, (GBOX[1] + GBOX[3]) / 2]]])
    rows = []
    for f in range(1099, 1761):
        a = prep(load(f))
        k, d = sift.detectAndCompute(a, None)
        if d is None or len(k) < 8:
            rows.append(dict(f=f, inl=0)); continue
        mt = bf.knnMatch(d, D, k=2)
        good = [x for x, y in mt if x.distance < 0.8 * y.distance]
        if len(good) < 8:
            rows.append(dict(f=f, inl=len(good))); continue
        src = np.float32([k[g.queryIdx].pt for g in good]).reshape(-1, 1, 2)
        dst = np.float32([P[g.trainIdx] for g in good]).reshape(-1, 1, 2)
        H, msk = cv2.findHomography(src, dst, cv2.RANSAC, 4.0, maxIters=10000)
        if H is None or msk is None or msk.sum() < 8:
            rows.append(dict(f=f, inl=0 if msk is None else int(msk.sum()))); continue
        Hi = np.linalg.inv(H); Hi /= Hi[2, 2]
        p = Hi @ np.array([ctr[0, 0, 0], ctr[0, 0, 1], 1.0])
        J = (Hi[:2, :2] - np.outer(p[:2] / p[2], Hi[2, :2])) / p[2]
        R, S = polar(J)
        ev = np.linalg.eigvalsh(S)
        rows.append(dict(f=f, inl=int(msk.sum()),
                         x=float(p[0] / p[2]), y=float(p[1] / p[2]),
                         rot=float(np.degrees(np.arctan2(R[1, 0], R[0, 0]))),
                         scale=float(np.sqrt(abs(ev[0] * ev[1]))),
                         aniso=float(ev.max() / max(ev.min(), 1e-6))))
        if f % 25 == 0:
            print(rows[-1], flush=True)
    json.dump(rows, open(OUT + "tilt_test.json", "w"))
    g = [r for r in rows if r.get("scale") and r["inl"] >= 10]
    an = np.array([r["aniso"] for r in g]); ro = np.array([r["rot"] for r in g])
    sc = np.array([r["scale"] for r in g])
    print("\nmatched frames: %d of 662" % len(g))
    print("anisotropy  median %.2f  p90 %.2f  max %.2f" % (np.median(an), np.percentile(an, 90), an.max()))
    print("in-plane rot  min %.1f  max %.1f  sd %.1f" % (ro.min(), ro.max(), ro.std()))
    print("scale  min %.2f  max %.2f" % (sc.min(), sc.max()))
    print("frames with aniso>1.6 (real foreshortening):",
          [r["f"] for r in g if r["aniso"] > 1.6][:40])


main()
