#!/usr/bin/env python3.12
"""Pass 2: rect-restricted row profiles + chroma stats inside the picture window.
Rects chosen from pass1 temporal-std maps to sit inside the soft vignette window
and (for row profiles) rows are kept full so they can be sliced later.
"""
import subprocess, sys, numpy as np

OUT = "/home/user/new-skinny-bob/analysis/compare-eras/band"
# key: (path, W, H, C0, C1, R0, R1)  -- all even
VIDS = {
 "OpSTlDJWFFI": ("/home/user/new-skinny-bob/videos/2026/OpSTlDJWFFI.mkv", 1920,1080, 380,1500, 60,1030),
 "Oqw96jCOP7A": ("/home/user/new-skinny-bob/videos/2026/Oqw96jCOP7A.mkv", 1920,1080, 420,1500, 60,1040),
 "l9RAhmPHM_A": ("/home/user/new-skinny-bob/videos/2026/l9RAhmPHM_A.mkv", 1920,1080, 400,1460, 90,1030),
 "ZB788PtqQvg": ("/home/user/new-skinny-bob/videos/2011/ZB788PtqQvg.mkv", 1920,1080, 380,1560, 50,1040),
 "RsQCXN4o4Ps": ("/home/user/new-skinny-bob/videos/2011/RsQCXN4o4Ps.mkv", 1920,1080, 380,1540, 50,1040),
 "Xju_CY5ZESA": ("/home/user/new-skinny-bob/videos/2011/Xju_CY5ZESA.mkv", 1920,1080, 390*0+390,1500, 60,1030),
 "a6TLGkrfNKI": ("/home/user/new-skinny-bob/videos/2011/a6TLGkrfNKI.mkv", 640,480, 90,550, 50,430),
}
STRUCT_EVERY = 6

def blockmean(a, b):
    h, w = a.shape
    h -= h % b; w -= w % b
    return a[:h, :w].reshape(h//b, b, w//b, b).mean(axis=(1, 3))

def run(key):
    path, W, H, C0, C1, R0, R1 = VIDS[key]
    C0 &= ~1; C1 &= ~1; R0 &= ~1; R1 &= ~1
    cw, ch = W//2, H//2
    ysz, csz = W*H, cw*ch
    fsz = ysz + 2*csz
    cc0, cc1, cr0, cr1 = C0//2, C1//2, R0//2, R1//2
    p = subprocess.Popen(["ffmpeg","-v","error","-i",path,"-f","rawvideo",
                          "-pix_fmt","yuv420p","-"], stdout=subprocess.PIPE, bufsize=fsz*8)
    rowprof = []; cst = []; struct = []; sidx = []
    n = 0; rd = p.stdout.read
    nw = C1 - C0
    while True:
        buf = rd(fsz)
        if len(buf) < fsz: break
        a = np.frombuffer(buf, np.uint8)
        Y = a[:ysz].reshape(H, W)
        U = a[ysz:ysz+csz].reshape(ch, cw)
        V = a[ysz+csz:].reshape(ch, cw)
        rowprof.append(np.add.reduce(Y[:, C0:C1], axis=1, dtype=np.int32) / nw)
        u = U[cr0:cr1, cc0:cc1].astype(np.int16) - 128
        v = V[cr0:cr1, cc0:cc1].astype(np.int16) - 128
        au = np.abs(u); av = np.abs(v)
        mag = np.sqrt((u.astype(np.float32)**2 + v.astype(np.float32)**2))
        Np = au.size
        cst.append((u.mean()+128.0, v.mean()+128.0, u.std(), v.std(),
                    np.count_nonzero(au>2)/Np, np.count_nonzero(au>4)/Np,
                    np.count_nonzero(au>8)/Np, np.count_nonzero(av>2)/Np,
                    np.count_nonzero(av>4)/Np, np.count_nonzero(av>8)/Np,
                    float(mag.mean()), float(np.percentile(mag,99)), float(mag.max()),
                    float(Y[R0:R1, C0:C1].mean())))
        if n % STRUCT_EVERY == 0:
            uf = u.astype(np.float32); vf = v.astype(np.float32)
            Yc = Y[R0:R1, C0:C1].astype(np.float32)
            Yq = blockmean(Yc, 2)                     # luma at chroma resolution
            hh = min(Yq.shape[0], uf.shape[0]); ww = min(Yq.shape[1], uf.shape[1])
            Yq = Yq[:hh, :ww]; uu = uf[:hh, :ww]; vv = vf[:hh, :ww]
            gy = np.abs(np.diff(Yq, axis=0))[:, :-1]
            gx = np.abs(np.diff(Yq, axis=1))[:-1, :]
            g = gx + gy
            m = np.sqrt(uu*uu + vv*vv)[:-1, :-1]
            def cor(x, y):
                x = x.ravel() - x.mean(); y = y.ravel() - y.mean()
                d = np.sqrt((x*x).sum()*(y*y).sum())
                return float((x*y).sum()/d) if d > 0 else 0.0
            # variance retained after 4x4 block averaging = structure fraction
            def sfrac(x):
                vt = x.var()
                return float(blockmean(x, 4).var()/vt) if vt > 0 else 0.0
            # lag autocorrelation of chroma
            def ac(x, l):
                a1 = x[:, :-l].ravel(); a2 = x[:, l:].ravel()
                return cor(a1, a2)
            struct.append((cor(m, g), cor(uu, vv), sfrac(uu), sfrac(vv),
                           ac(uu,1), ac(uu,2), ac(uu,4), ac(uu,8),
                           cor(uu, Yq), cor(vv, Yq), float(uu.std()), float(vv.std()),
                           float(Yq.std()), float(g.mean())))
            sidx.append(n)
        n += 1
    p.stdout.close(); p.wait()
    np.savez_compressed(f"{OUT}/{key}_p2.npz", n=n, W=W, H=H,
        rect=np.array([C0,C1,R0,R1]),
        rowprof=np.array(rowprof, np.float32),
        cst=np.array(cst, np.float64),
        struct=np.array(struct, np.float64), sidx=np.array(sidx))
    print(key, n, "struct rows:", len(struct), flush=True)

if __name__ == "__main__":
    for k in sys.argv[1:] or VIDS:
        run(k)
