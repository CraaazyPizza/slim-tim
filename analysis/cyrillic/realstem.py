"""Measure the real «П» left-stem FWHM and cap height with EXACTLY the construction
used on the templates in vfonts.stem_cap, then deconvolve the measured PSF."""
import numpy as np, sys
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
import pipe
from pipe import sig, BEST5
SIG_PSF=0.9
def measure(X, capTop, base):
    cap=base-capTop
    y0=int(round(capTop+0.25*cap)); y1=int(round(capTop+0.95*cap))
    prof=X[(y0-Y0):(y1-Y0),(438-X0):(520-X0)].mean(0)
    prof=np.clip(prof,0,None)
    m=int(np.argmax(prof[:len(prof)//2]))
    h=prof[m]/2.0
    i=m
    while i>0 and prof[i-1]>=h: i-=1
    j=m
    while j<len(prof)-1 and prof[j+1]>=h: j+=1
    l=i-1+(h-prof[i-1])/(prof[i]-prof[i-1]) if i>0 and prof[i]!=prof[i-1] else i
    r=j+(prof[j]-h)/(prof[j]-prof[j+1]) if j<len(prof)-1 and prof[j]!=prof[j+1] else j
    return cap, float(r-l)
rows=[]
for tag,fs,ct,bl in [('f983',[983],922.0,974.3),('best5',BEST5,922.0,974.7),('stack20',list(CAP),925.3,976.8)]:
    cap,st=measure(sig(fs),ct,bl)
    st_deconv=float(np.sqrt(max(st**2-(2.3548*SIG_PSF)**2,0.01)))
    rows.append((tag,cap,st,st_deconv,st_deconv/cap))
    print('%-8s cap %.2f  stem FWHM %.2f  (PSF-deconvolved %.2f)  stretched stem/cap %.4f'%(tag,cap,st,st_deconv,st_deconv/cap))
m=np.mean([r[3] for r in rows[:2]]); c=np.mean([r[1] for r in rows[:2]])
print()
print('adopted: cap = %.2f px, stretched stem = %.2f px  ->  stretched stem/cap = %.4f'%(c,m,m/c))
print('the STRETCH acts on x only, so cap is unaffected and stem is multiplied by kx:')
print('   intrinsic stem/cap of the true face  =  %.4f / kx'%(m/c))
for kx in (1.15,1.20,1.25,1.30,1.35,1.40,1.45,1.50):
    print('   kx = %.2f  ->  intrinsic stem/cap = %.4f'%(kx,(m/c)/kx))
import json; json.dump(dict(cap=c,stem_stretched=m,ratio_stretched=m/c,rows=rows),open('realstem.json','w'),indent=1)
