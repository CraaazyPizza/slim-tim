"""Independent measurement of (a) line-1 ink extent, (b) the horizontal PSF."""
import numpy as np, sys, json
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from scipy.optimize import curve_fit

ci=[FR.index(f) for f in CAP]
INKs = -pp(RES[ci].mean(0))                      # stack, ink positive
INK1 = -pp(RES[FR.index(983)])                   # best single frame
NULL = -pp(RES[[FR.index(f) for f in range(1010,1030)]].mean(0))

def bandcols(X, rows):
    r=slice(rows[0]-Y0, rows[1]-Y0)
    b=X[r]; b=b-np.median(b,axis=1,keepdims=True)
    return b

# ---- ink extent from squared column energy vs null
for tag,X in [('stack',INKs),('f983',INK1)]:
    b=bandcols(X,(930,1000)); n=bandcols(NULL,(930,1000))
    e=(b**2).sum(0); en=(n**2).sum(0)
    z=(e-en.mean())/en.std()
    idx=np.where(z>4)[0]
    print('%-6s line1 ink cols z>4: x=%d..%d  (n=%d)'%(tag, idx.min()+X0, idx.max()+X0, len(idx)))

b=bandcols(INKs,(1000,1075)); n=bandcols(NULL,(1000,1075))
e=(b**2).sum(0); z=(e-(n**2).sum(0).mean())/(n**2).sum(0).std()
idx=np.where(z>3)[0]
print('stack  line2 ink cols z>3: x=%d..%d'%(idx.min()+X0, idx.max()+X0))

# ---- PSF: fit a Gaussian-blurred step to the LEFT edge of line 1 ('П' stem, x~445)
def stepmodel(x, x0, s, A, c):
    from scipy.special import erf
    return c + A*0.5*(1+erf((x-x0)/(s*np.sqrt(2))))

print('\n=== horizontal line-spread from the leading edge of line 1 (the "П" left stem) ===')
for tag,X in [('20-frame stack',INKs),('single frame f983',INK1)]:
    prof = bandcols(X,(935,995))[:, (445-40-X0):(445+40-X0)].mean(0)
    xs = np.arange(len(prof))
    p,_ = curve_fit(stepmodel, xs, prof, p0=[40, 3, prof[-20:].mean()-prof[:20].mean(), prof[:20].mean()],
                    maxfev=20000)
    print('  %-18s edge at x=%.1f   sigma = %.2f px' % (tag, p[0]+445-40, abs(p[1])))

# ---- PSF from the trailing edge of line 1 (right end, x~1597)
print('=== trailing edge (right end of line 1) ===')
for tag,X in [('20-frame stack',INKs),('single frame f983',INK1)]:
    prof = bandcols(X,(935,995))[:, (1597-40-X0):(1597+40-X0)].mean(0)
    xs=np.arange(len(prof))
    p,_=curve_fit(lambda x,x0,s,A,c: stepmodel(x,x0,s,-abs(A),c), xs, prof,
                  p0=[40,3,prof[:20].mean()-prof[-20:].mean(),prof[:20].mean()],maxfev=20000)
    print('  %-18s edge at x=%.1f   sigma = %.2f px'%(tag,p[0]+1597-40,abs(p[1])))

# ---- PSF from the vertical baseline edge of line 1 (row direction, undistorted by hp)
print('\n=== vertical line-spread from line-1 baseline (row profile of |ink| across x-height cols) ===')
def rowedge(X):
    r=slice(920-Y0,1010-Y0)
    b=X[r, (520-X0):(1250-X0)]
    b=b-np.median(X[r],axis=1,keepdims=True)
    return b.mean(1)
for tag,X in [('20-frame stack',INKs),('single frame f983',INK1)]:
    prof=rowedge(X); xs=np.arange(len(prof))
    # baseline is the falling edge near y=985 -> index 985-920=65
    seg=prof[45:85]; xs2=np.arange(len(seg))
    p,_=curve_fit(lambda x,x0,s,A,c: stepmodel(x,x0,s,-abs(A),c), xs2, seg,
                  p0=[20,3,seg[:8].mean()-seg[-8:].mean(),seg[:8].mean()],maxfev=20000)
    print('  %-18s baseline at y=%.1f   sigma = %.2f px'%(tag,p[0]+965,abs(p[1])))
