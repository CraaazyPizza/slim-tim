"""Best-single-frame selection. Three independent per-frame metrics, plus a
sub-pixel drift measurement that decides whether averaging is legitimate at all."""
import numpy as np, json, sys
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from scipy.ndimage import shift as ndshift

R1 = sl(L1_ROWS, L1_X); R2 = sl(L2_ROWS, L2_X)
# caption-free reference band (same rows, no text): use rows well above line1
NUL = sl((900, 922), L1_X)

Pf = np.array([pp(RES[i]) for i in range(len(FR))])     # ink NEGATIVE
INK = -Pf                                                # ink POSITIVE

def band(i, R): 
    b = INK[i][R]; return b - b.mean()

# ---------- template = mean over CAP, leave-one-out to keep it unbiased
ci = [FR.index(f) for f in CAP]
T1_all = INK[ci][:, R1[0], R1[1]].mean(0)

rows = []
for i, f in enumerate(FR):
    b1 = band(i, R1)
    if i in ci:
        loo = INK[[j for j in ci if j != i]][:, R1[0], R1[1]].mean(0)
    else:
        loo = T1_all
    loo = loo - loo.mean()
    r_loo = ncc(b1, loo)
    # amplitude (regression coefficient onto LOO template)
    amp = float((b1*loo).sum()/ (loo*loo).sum())
    # gradient energy (Tenengrad) on glyph band vs caption-free band
    gx = np.gradient(b1, axis=1); ge = float((gx**2).mean())
    nb = band(i, NUL); gxn = np.gradient(nb, axis=1); gen = float((gxn**2).mean())
    # RMS contrast in band vs null band
    rows.append(dict(f=int(f), r_loo=r_loo, amp=amp,
                     grad=ge, grad_null=gen, grad_ratio=ge/gen,
                     rms=float(b1.std()), rms_null=float(nb.std()),
                     r2=ncc(band(i,R2), INK[[j for j in ci if j!=i]][:, R2[0],R2[1]].mean(0)
                            - INK[[j for j in ci if j!=i]][:, R2[0],R2[1]].mean() if i in ci
                            else INK[ci][:, R2[0],R2[1]].mean(0)-INK[ci][:, R2[0],R2[1]].mean())))
rows.sort(key=lambda d: -d['r_loo'])
print('%-6s %8s %8s %9s %8s %8s'%('frame','r_LOO_l1','amp','gradratio','rms','r_LOO_l2'))
for d in rows[:26]:
    print('%-6d %8.4f %8.3f %9.3f %8.5f %8.4f'%(d['f'],d['r_loo'],d['amp'],d['grad_ratio'],d['rms'],d['r2']))
print('--- worst / out-of-block for scale ---')
for d in rows[-6:]:
    print('%-6d %8.4f %8.3f %9.3f %8.5f %8.4f'%(d['f'],d['r_loo'],d['amp'],d['grad_ratio'],d['rms'],d['r2']))

# ---------- DRIFT: does the caption layer move between frames?
print('\n=== sub-pixel registration of the caption layer, frame vs LOO template (line 1) ===')
def subpix(a, b, rad=4):
    """peak of NCC surface a vs b with parabolic interpolation, returns (dy,dx,peak)"""
    A = a - a.mean(); B = b - b.mean()
    F = np.fft.rfft2(A); G = np.fft.rfft2(B)
    cc = np.fft.irfft2(F*np.conj(G), A.shape)
    cc /= np.sqrt((A*A).sum()*(B*B).sum())
    cc = np.fft.fftshift(cc); c0 = (A.shape[0]//2, A.shape[1]//2)
    sub = cc[c0[0]-rad:c0[0]+rad+1, c0[1]-rad:c0[1]+rad+1]
    k = np.unravel_index(np.argmax(sub), sub.shape)
    dy, dx = k[0]-rad, k[1]-rad
    def par(v):
        if v[1] <= v[0] or v[1] <= v[2]: return 0.0
        return 0.5*(v[0]-v[2])/(v[0]-2*v[1]+v[2])
    yy = max(1,min(sub.shape[0]-2,k[0])); xx = max(1,min(sub.shape[1]-2,k[1]))
    fy = par(sub[yy-1:yy+2, xx]); fx = par(sub[yy, xx-1:xx+2])
    return dy+fy, dx+fx, float(sub[k])
drift=[]
for i in ci:
    loo = INK[[j for j in ci if j != i]][:, R1[0], R1[1]].mean(0)
    dy,dx,pk = subpix(INK[i][R1[0],R1[1]], loo)
    drift.append((FR[i],dy,dx,pk)); print('  f%d  dy=%+.3f dx=%+.3f  peak r=%.4f'%(FR[i],dy,dx,pk))
dys=np.array([d[1] for d in drift]); dxs=np.array([d[2] for d in drift])
print('  drift dy: mean %+.3f sd %.3f  max|.| %.3f' % (dys.mean(), dys.std(), np.abs(dys).max()))
print('  drift dx: mean %+.3f sd %.3f  max|.| %.3f' % (dxs.mean(), dxs.std(), np.abs(dxs).max()))
json.dump(dict(rows=rows, drift=[list(map(float,d)) for d in drift]), open(P+'best.json','w'), indent=1)
