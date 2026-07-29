"""POWER CALIBRATION for the typeface test.
Render the known line-1 string in a KNOWN font, stretch by a known kx, blur to the
measured PSF, scale to the measured ink depth, inject into caption-free frames, then
run the identical sweep. Does the test put the true face first, and by how much?"""
import numpy as np, sys, json, time
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from fast import *
TEXT=L1_TEXT; ROWS=(902,1002); XS=(430,1620)
ALL=json.load(open('fonts.json'))
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
H=ROWS[1]-ROWS[0]; W=XS[1]-XS[0]
from scipy.ndimage import gaussian_filter as gf
# measured: ink depth in a single frame ~11.9/255 of the normalised luma; PSF sigma ~1.0
DEPTH=11.9/255.0
def carrier(fs):
    return (-RESL[[FR.index(f) for f in fs]].mean(0))[(ROWS[0]-Y0):(ROWS[1]-Y0),(XS[0]-X0):(XS[1]-X0)]
KX=np.round(np.arange(1.00,1.63,0.06),2); BL=[0.5,0.8,1.2,1.7,2.4,3.4,4.6]; CAPS=[51,53.5,56]
def sweep(fl):
    out=[]
    for n,fp in ALL.items():
        best=None
        for cap in CAPS:
            s=capsize(fp,cap); A=base_render(fp,TEXT,s)
            for kx in KX:
                ink=place(A,kx,fl.H,fl.W)
                for r,bl,dx,dy in fl.match(ink,BL):
                    if best is None or r>best[0]: best=(r,cap,float(kx),bl)
        out.append((n,best[0],best[1],best[2],best[3]))
    out.sort(key=lambda t:-t[1]); return out
TRUTH=[('Lato Bold',1.40),('Carlito Bold',1.34),('Open Sans Semibold',1.36),('DejaVu Sans Bold',1.20)]
NULLFR=[list(range(1010,1030))]
report={}
for tname,tkx in TRUTH:
    fp=ALL[tname]; s=capsize(fp,53.5)
    ink=place(base_render(fp,TEXT,s),tkx,H,W)
    lay=gf(ink,1.0)*DEPTH
    for cf in NULLFR:
        fl=Field(carrier(cf)+lay,H,W)
        out=sweep(fl)
        rk=[i for i,t in enumerate(out) if t[0]==tname][0]
        print('\nINJECTED %s at kx=%.2f  -> recovered rank %d/%d'%(tname,tkx,rk+1,len(out)))
        print('   %-38s %7s %6s %5s %5s'%('face','r','cap','kx','blur'))
        for t in out[:8]: print('   %-38s %7.4f %6.1f %5.2f %5.1f  %s'%(t[0],t[1],t[2],t[3],t[4],'<== TRUTH' if t[0]==tname else ''))
        report[tname]=dict(kx=tkx,rank=rk+1,top=[list(map(str,t)) for t in out[:10]])
        sys.stdout.flush()
json.dump(report,open('inj.json','w'),indent=1,ensure_ascii=False)
