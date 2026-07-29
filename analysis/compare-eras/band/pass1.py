#!/usr/bin/env python3.12
"""Pass 1 (fast): stream native yuv420p from each mkv.
Every frame: integer row-sum luma profile (full width) + cheap chroma stats.
Every KTH frame: full-res per-pixel accumulators for mean/std maps (masking).
"""
import subprocess, sys, numpy as np

OUT = "/home/user/new-skinny-bob/analysis/compare-eras/band"
VIDS = {
 "OpSTlDJWFFI": ("/home/user/new-skinny-bob/videos/2026/OpSTlDJWFFI.mkv", 1920, 1080),
 "Oqw96jCOP7A": ("/home/user/new-skinny-bob/videos/2026/Oqw96jCOP7A.mkv", 1920, 1080),
 "l9RAhmPHM_A": ("/home/user/new-skinny-bob/videos/2026/l9RAhmPHM_A.mkv", 1920, 1080),
 "ZB788PtqQvg": ("/home/user/new-skinny-bob/videos/2011/ZB788PtqQvg.mkv", 1920, 1080),
 "RsQCXN4o4Ps": ("/home/user/new-skinny-bob/videos/2011/RsQCXN4o4Ps.mkv", 1920, 1080),
 "Xju_CY5ZESA": ("/home/user/new-skinny-bob/videos/2011/Xju_CY5ZESA.mkv", 1920, 1080),
 "a6TLGkrfNKI": ("/home/user/new-skinny-bob/videos/2011/a6TLGkrfNKI.mkv", 640, 480),
}
KTH = 12

def run(key):
    path, W, H = VIDS[key]
    cw, ch = W // 2, H // 2
    ysz, csz = W * H, cw * ch
    fsz = ysz + 2 * csz
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo",
                          "-pix_fmt", "yuv420p", "-"],
                         stdout=subprocess.PIPE, bufsize=fsz * 8)
    ysum = np.zeros((H, W), np.int64); ysq = np.zeros((H, W), np.int64)
    usum = np.zeros((ch, cw), np.int64); vsum = np.zeros((ch, cw), np.int64)
    usq = np.zeros((ch, cw), np.int64); vsq = np.zeros((ch, cw), np.int64)
    nacc = 0
    rowsum = []; colsum = []; cstats = []
    maghist = np.zeros(256, np.int64)
    n = 0
    rd = p.stdout.read
    while True:
        buf = rd(fsz)
        if len(buf) < fsz:
            break
        a = np.frombuffer(buf, np.uint8)
        Y = a[:ysz].reshape(H, W)
        U = a[ysz:ysz + csz].reshape(ch, cw)
        V = a[ysz + csz:].reshape(ch, cw)
        rowsum.append(np.add.reduce(Y, axis=1, dtype=np.int32))
        colsum.append(np.add.reduce(Y, axis=0, dtype=np.int32))
        du = U.astype(np.int16); du -= 128
        dv = V.astype(np.int16); dv -= 128
        au = np.abs(du); av = np.abs(dv)
        m2 = du.astype(np.int32) ** 2 + dv.astype(np.int32) ** 2
        mag = np.sqrt(m2, dtype=np.float32) if m2.dtype == np.float32 else np.sqrt(m2.astype(np.float32))
        maghist += np.bincount(np.minimum(mag.astype(np.int32), 255).ravel(), minlength=256)
        Np = au.size
        cstats.append((
            du.mean() + 128.0, dv.mean() + 128.0, du.std(), dv.std(),
            np.count_nonzero(au > 2) / Np, np.count_nonzero(au > 4) / Np,
            np.count_nonzero(au > 8) / Np,
            np.count_nonzero(av > 2) / Np, np.count_nonzero(av > 4) / Np,
            np.count_nonzero(av > 8) / Np,
            float(mag.mean()), float(mag.max()),
            float(rowsum[-1].sum()) / ysz))
        if n % KTH == 0:
            ysum += Y; ysq += Y.astype(np.int32) ** 2
            usum += U; usq += U.astype(np.int32) ** 2
            vsum += V; vsq += V.astype(np.int32) ** 2
            nacc += 1
        n += 1
    p.stdout.close(); p.wait()
    def ms(s, sq, k):
        m = s / k
        return m.astype(np.float32), np.sqrt(np.maximum(sq / k - m * m, 0)).astype(np.float32)
    ym, ys = ms(ysum, ysq, nacc); um, us = ms(usum, usq, nacc); vm, vs = ms(vsum, vsq, nacc)
    np.savez_compressed(f"{OUT}/{key}_p1.npz", n=n, W=W, H=H, nacc=nacc, KTH=KTH,
        ymean=ym, ystd=ys, umean=um, ustd=us, vmean=vm, vstd=vs,
        rowmean=(np.array(rowsum, np.float32) / W),
        colmean=(np.array(colsum, np.float32) / H),
        cstats=np.array(cstats, np.float64), maghist=maghist)
    print(key, "frames:", n, "acc:", nacc, flush=True)

if __name__ == "__main__":
    for k in sys.argv[1:] or VIDS:
        run(k)
