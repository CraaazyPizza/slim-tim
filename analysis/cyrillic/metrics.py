"""Measure the letterform METRICS of line 1 straight off the pixels:
cap height, x-height, stroke weight, per-glyph advance positions."""
import numpy as np, sys, json
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from scipy.ndimage import gaussian_filter as gf, gaussian_filter1d as g1
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
ci=[FR.index(f) for f in CAP]
def A(X):                       # ink-positive, low-freq removed, mild smooth
    Y=X-np.median(X,axis=1,keepdims=True); return -gf(Y-gf(Y,16),0.8)
OB = {'f983':A(RESL[FR.index(983)]), 'stack':A(RESL[ci].mean(0)),
      'best5':A(RESL[[FR.index(f) for f in (983,973,974,984,981)]].mean(0))}
NULL = A(RESL[[FR.index(f) for f in range(1010,1030)]].mean(0))

def colprof(X, rows, xs):
    b=X[(rows[0]-Y0):(rows[1]-Y0),(xs[0]-X0):(xs[1]-X0)]
    return np.clip(b,0,None).sum(0)

print('=== line-1 column ink profile: glyph boundaries (f983, rows 905..1000) ===')
p=colprof(OB['f983'],(905,1000),(430,1620)); p=g1(p,1.5)
thr=0.25*np.percentile(p,90)
on=p>thr
segs=[]; i=0
while i<len(on):
    if on[i]:
        j=i
        while j<len(on) and on[j]: j+=1
        if j-i>=6: segs.append((430+i,430+j-1))
        i=j
    else: i+=1
print('  %d segments:'%len(segs))
for a,b in segs: print('    x %4d..%4d  w=%3d'%(a,b,b-a+1))

print('\n=== vertical metrics ===')
def redge(X, xs, rows, rising, guess):
    from scipy.optimize import curve_fit
    from scipy.special import erf
    prof=np.clip(X[(rows[0]-Y0):(rows[1]-Y0),(xs[0]-X0):(xs[1]-X0)],0,None).mean(1)
    t=np.arange(len(prof))
    def m(t,t0,s,Aa,c):
        return c+(abs(Aa) if rising else -abs(Aa))*0.5*(1+erf((t-t0)/(abs(s)*np.sqrt(2))))
    p,_=curve_fit(m,t,prof,p0=[guess,1.5,abs(prof.max()-prof.min()),prof[0]],maxfev=60000)
    return p[0]+rows[0], abs(p[1])
for tag in ['f983','stack','best5']:
    X=OB[tag]
    ct,cs = redge(X,(450,500),(900,940),True,12)     # П cap top
    bl,bs = redge(X,(450,500),(965,1000),False,20)   # П baseline
    print('  %-6s П: cap top y=%.2f (sig %.2f)  baseline y=%.2f (sig %.2f)  => CAP HEIGHT = %.2f px'
          %(tag,ct,cs,bl,bs,bl-ct))
