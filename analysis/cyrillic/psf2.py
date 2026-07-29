"""PSF measured on FLAT-ONLY data (no high-pass, which would sharpen x edges)."""
import numpy as np, sys
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from scipy.optimize import curve_fit
from scipy.special import erf
ci=[FR.index(f) for f in CAP]
Xs = -flat(RES[ci].mean(0))
X1 = -flat(RES[FR.index(983)])
def step(x,x0,s,A,c): return c + A*0.5*(1+erf((x-x0)/(abs(s)*np.sqrt(2))))

def fit_edge(prof, rising, x0g):
    xs=np.arange(len(prof))
    A0 = (prof[-8:].mean()-prof[:8].mean())
    if not rising: A0=-abs(A0)
    else: A0=abs(A0)
    p,_=curve_fit(lambda x,x0,s,A,c: step(x,x0,s,(abs(A) if rising else -abs(A)),c),
                  xs,prof,p0=[x0g,3.0,abs(A0),prof[:8].mean()],maxfev=40000)
    return p[0], abs(p[1])

print('=== horizontal edge-spread, FLAT-only data (no high-pass) ===')
for tag,X in [('20-frame stack',Xs),('f983 single',X1)]:
    for name,xc,rise in [('line1 left edge (П stem)',447,True),('line1 right edge',1598,False)]:
        w=30; prof = X[(915-Y0):(985-Y0), (xc-w-X0):(xc+w-X0)].mean(0)
        x0,s = fit_edge(prof, rise, w)
        print('  %-15s %-26s x0=%.1f  sigma_x = %.2f px'%(tag,name,x0+xc-w,s))

print('\n=== vertical edge-spread, FLAT-only ===')
for tag,X in [('20-frame stack',Xs),('f983 single',X1)]:
    prof = X[(960-Y0):(1000-Y0), (520-X0):(1250-X0)].mean(1)   # baseline falling edge
    x0,s = fit_edge(prof, False, 25)
    print('  %-15s line1 baseline           y0=%.1f  sigma_y = %.2f px'%(tag,x0+960,s))
    prof = X[(895-Y0):(935-Y0), (446-X0):(505-X0)].mean(1)     # П cap-top rising edge
    x0,s = fit_edge(prof, True, 15)
    print('  %-15s П cap top                y0=%.1f  sigma_y = %.2f px'%(tag,x0+895,s))

print('\n=== 2D check: radially-averaged autocorrelation width of the ink layer ===')
for tag,X in [('20-frame stack',Xs)]:
    b=X[(915-Y0):(1000-Y0),(440-X0):(1600-X0)]; b=b-b.mean()
    ac=np.fft.irfft2(np.abs(np.fft.rfft2(b))**2, b.shape); ac/=ac[0,0]
    print('  ACF along x: ', ' '.join('%d:%.3f'%(k,ac[0,k]) for k in range(0,9)))
    print('  ACF along y: ', ' '.join('%d:%.3f'%(k,ac[k,0]) for k in range(0,9)))
