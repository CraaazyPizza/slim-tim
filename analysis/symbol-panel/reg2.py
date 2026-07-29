#!/usr/bin/env python3.12
"""Stage 1: SIFT+RANSAC homography of every panel frame onto reference view,
refined by ECC in a canonical (upsampled) canvas centred on the glyph cluster.

Writes reg2.npz: frames, H (picture->ref-picture), inliers, ncc, sharpness, scale.
"""
import numpy as np, cv2, sys

FR = "/home/user/new-skinny-bob/frames/l9RAhmPHM_A/f%05d.png"
OUT = "/home/user/new-skinny-bob/analysis/symbol-panel/"
PB = (263, 60, 1561, 1043)
REF = 1694
GL = (400, 500, 730, 810)                       # glyph canvas src rect in ref picture coords
ZOOM = 3.0
TCM = (469 - PB[0], 938 - PB[1], 968 - PB[0], 1002 - PB[1])

S = np.array([[ZOOM, 0, -ZOOM * GL[0]], [0, ZOOM, -ZOOM * GL[1]], [0, 0, 1]], np.float64)
CW = int(ZOOM * (GL[2] - GL[0])); CH = int(ZOOM * (GL[3] - GL[1]))


def load(i):
    return cv2.imread(FR % i, cv2.IMREAD_GRAYSCALE).astype(np.float32)


def pic(a):
    return a[PB[1]:PB[3], PB[0]:PB[2]].copy()


def prep(c):
    bg = cv2.GaussianBlur(c, (0, 0), 25)
    d = c - bg
    d = np.clip(d / (4 * np.std(d) + 1e-6) + 0.5, 0, 1)
    u = (d * 255).astype(np.uint8)
    u[TCM[1]:TCM[3], TCM[0]:TCM[2]] = 128
    return u


def canon(u, H):
    return cv2.warpPerspective(u, S @ H, (CW, CH), flags=cv2.INTER_LANCZOS4)


def main():
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    sift = cv2.SIFT_create(nfeatures=5000)
    bf = cv2.BFMatcher()
    ra = prep(pic(load(REF)))
    kr, dr = sift.detectAndCompute(ra, None)
    rcan = canon(ra, np.eye(3)).astype(np.float32)
    rz = (rcan - rcan.mean()) / (rcan.std() + 1e-6)
    crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 1e-7)
    rows = []
    for i in range(lo, hi + 1):
        c = pic(load(i)); a = prep(c)
        k, d = sift.detectAndCompute(a, None)
        if d is None or len(k) < 8:
            rows.append((i, 0, 0, 0, 0, None)); continue
        mt = bf.knnMatch(d, dr, k=2)
        good = [p for p, q in mt if p.distance < 0.8 * q.distance]
        if len(good) < 10:
            rows.append((i, 0, 0, 0, 0, None)); continue
        src = np.float32([k[g.queryIdx].pt for g in good]).reshape(-1, 1, 2)
        dst = np.float32([kr[g.trainIdx].pt for g in good]).reshape(-1, 1, 2)
        H0, mask = cv2.findHomography(src, dst, cv2.RANSAC, 3.0, maxIters=10000)
        if H0 is None or mask is None or mask.sum() < 12:
            rows.append((i, 0 if mask is None else int(mask.sum()), 0, 0, 0, None)); continue
        nin = int(mask.sum())
        H = H0 / H0[2, 2]
        # ECC refine in canvas space: align canon(a,H) to rcan
        try:
            W = np.eye(3, dtype=np.float32)
            _, W = cv2.findTransformECC(rcan.astype(np.uint8), canon(a, H),
                                        W, cv2.MOTION_HOMOGRAPHY, crit, None, 5)
            Hr = S_inv @ np.linalg.inv(W.astype(np.float64)) @ S @ H
            Hr /= Hr[2, 2]
            t = canon(prep(c), Hr)
            if np.isfinite(Hr).all():
                H = Hr
        except cv2.error:
            pass
        w = canon(a, H).astype(np.float32)
        wz = (w - w.mean()) / (w.std() + 1e-6)
        ncc = float((wz * rz).mean())
        # local scale of H at glyph centre
        p = np.array([(GL[0] + GL[2]) / 2, (GL[1] + GL[3]) / 2, 1.0])
        J = H[:2, :2] / (H[2] @ p) - np.outer(H[:2] @ p, H[2, :2]) / (H[2] @ p) ** 2
        sc = float(np.sqrt(abs(np.linalg.det(J))))
        gx = cv2.Sobel(c, cv2.CV_32F, 1, 0); gy = cv2.Sobel(c, cv2.CV_32F, 0, 1)
        # sharpness measured in the source rect that maps to the glyph canvas
        q = cv2.perspectiveTransform(np.float32([[[GL[0], GL[1]]], [[GL[2], GL[1]]],
                                                 [[GL[2], GL[3]]], [[GL[0], GL[3]]]]),
                                     np.linalg.inv(H))[:, 0, :]
        m2 = np.zeros(c.shape, np.uint8); cv2.fillPoly(m2, [q.astype(np.int32)], 1)
        sh = float(np.mean((gx * gx + gy * gy)[m2 > 0])) if m2.sum() > 100 else 0.0
        rows.append((i, nin, ncc, sc, sh, H))
        if i % 50 == 0:
            print(i, nin, round(ncc, 3), round(sc, 3), round(sh, 1), flush=True)
    ok = [r for r in rows if r[5] is not None]
    np.savez(OUT + f"reg2_{lo}_{hi}.npz",
             frames=np.array([r[0] for r in ok]), inl=np.array([r[1] for r in ok]),
             ncc=np.array([r[2] for r in ok]), scale=np.array([r[3] for r in ok]),
             sharp=np.array([r[4] for r in ok]), H=np.array([r[5] for r in ok]),
             allframes=np.array([r[0] for r in rows]),
             allok=np.array([r[5] is not None for r in rows]))
    print("registered", len(ok), "of", len(rows))


S_inv = np.linalg.inv(S)
main()
