import numpy as np, sys, json
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from scipy.ndimage import gaussian_filter as gf
from scipy.optimize import curve_fit
from scipy.special import erf
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
ci=[FR.index(f) for f in CAP]
def A(X):
    Y=X-np.median(X,axis=1,keepdims=True); return -gf(Y-gf(Y,16),0.8)
OB={'f983':A(RESL[FR.index(983)]),'best5':A(RESL[[FR.index(f) for f in (983,973,974,984,981)]].mean(0)),
    'stack20':A(RESL[ci].mean(0))}
def edge(X,xs,rows,rising,g):
    prof=np.clip(X[(rows[0]-Y0):(rows[1]-Y0),(xs[0]-X0):(xs[1]-X0)],0,None).mean(1)
    t=np.arange(len(prof))
    def m(t,t0,s,Aa,c): return c+(abs(Aa) if rising else -abs(Aa))*0.5*(1+erf((t-t0)/(abs(s)*np.sqrt(2))))
    lo=[0,0.2,0,-1]; hi=[len(prof),8,10,10]
    p,_=curve_fit(m,t,prof,p0=[g,1.2,prof.max()-prof.min(),prof.min()],bounds=(lo,hi),maxfev=80000)
    return p[0]+rows[0],abs(p[1])
print('=== LINE 1 vertical metrics (from single frame f983 and small stacks) ===')
out={}
for tag,X in OB.items():
    ct,cs = edge(X,(452,504),(902,935),True,18)      # П cap top
    bl,bs = edge(X,(452,504),(972,1000),False,13)    # П baseline (stems, no descender)
    xt,xs_ = edge(X,(1176,1220),(925,960),True,20)   # 'o' x-height top (has overshoot)
    xb,_   = edge(X,(1176,1220),(975,1000),False,11) # 'o' bottom
    print('  %-8s  capTop %.2f(s%.2f)  base %.2f(s%.2f)  CAP=%.2f | xTop %.2f  xBot %.2f  XH=%.2f  ratio %.3f'
          %(tag,ct,cs,bl,bs,bl-ct,xt,xb,xb-xt,(xb-xt)/(bl-ct)))
    out[tag]=dict(capTop=ct,base=bl,cap=bl-ct,xTop=xt,xBot=xb,xh=xb-xt,ratio=(xb-xt)/(bl-ct),
                  sig_captop=cs,sig_base=bs)
print('\n=== stroke weight: width of the two П stems and the "н" stems (FWHM of ink) ===')
def stemw(X,rows,xrange):
    b=np.clip(X[(rows[0]-Y0):(rows[1]-Y0),(xrange[0]-X0):(xrange[1]-X0)],0,None).mean(0)
    pk=b.max(); h=pk/2
    above=b>=h
    idx=np.where(above)[0]
    # contiguous run containing the max
    m=int(np.argmax(b)); a=m
    while a>0 and above[a-1]: a-=1
    e=m
    while e<len(b)-1 and above[e+1]: e+=1
    # sub-pixel via linear interp
    l = a-1 + (h-b[a-1])/(b[a]-b[a-1]) if a>0 and b[a]!=b[a-1] else a
    r = e + (b[e]-h)/(b[e]-b[e+1]) if e<len(b)-1 and b[e]!=b[e+1] else e
    return r-l
for tag,X in OB.items():
    w1=stemw(X,(930,980),(442,466))      # П left stem
    w2=stemw(X,(930,980),(492,514))      # П right stem
    print('  %-8s П left stem FWHM %.2f px, right stem %.2f px'%(tag,w1,w2))
json.dump(out,open('metrics.json','w'),indent=1)
