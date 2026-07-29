import numpy as np, json
from lib import *
from scipy.ndimage import gaussian_filter, shift as ndshift, sobel
def phasecorr(a,b,maxsh=48):
    a=a-a.mean(); b=b-b.mean()
    w=np.outer(np.hanning(a.shape[0]),np.hanning(a.shape[1]))
    A=np.fft.fft2(a*w); B=np.fft.fft2(b*w)
    R=A*np.conj(B); R/=np.maximum(np.abs(R),1e-9)
    c=np.fft.fftshift(np.real(np.fft.ifft2(R)))
    cy,cx=np.array(c.shape)//2
    m=np.full(c.shape,-9.0); m[cy-maxsh:cy+maxsh+1,cx-maxsh:cx+maxsh+1]=c[cy-maxsh:cy+maxsh+1,cx-maxsh:cx+maxsh+1]
    iy,ix=np.unravel_index(np.argmax(m),m.shape)
    return iy-cy,ix-cx,float(c[iy,ix])
# candidate runs with sustained motion, chosen from the diff signal
RUNS={'OpSTlDJWFFI':[(2140,2170),(2400,2430),(1800,1830),(2820,2850)],
      'Oqw96jCOP7A':[(1060,1090),(1100,1130),(1840,1870),(2340,2370)],
      'l9RAhmPHM_A':[(1860,1890),(1010,1040),(1780,1810),(3500,3530)],
      'ZB788PtqQvg':[(420,450),(830,860),(230,260),(1090,1120)],
      'RsQCXN4o4Ps':[(1030,1060),(1105,1140),(700,730),(1400,1430)]}
rng=np.random.default_rng(7)
res={}
print('PERSISTENT-MARK LOCK TEST')
print('M_frame  = temporal median of high-pass residual, NO alignment      -> keeps marks fixed to the frame')
print('M_image  = temporal median after motion-compensating each frame      -> keeps marks fixed to the picture')
print('M_rand   = temporal median after random shifts of same magnitude     -> null')
print('score = 99.9th pct of |M| / robust sigma of M  (isolated-blob contrast)')
for k in RUNS:
    y0,y1,x0,x1=PIC[k]
    print('==== %s era%d'%(k,ERA[k]),flush=True)
    rows=[]
    for (s,e) in RUNS[k]:
        fr=[F(k,i)[y0:y1,x0:x1] for i in range(s,e+1)]
        cum=[(0.0,0.0)]
        ok=True
        for i in range(1,len(fr)):
            dy,dx,pk=phasecorr(fr[i-1],fr[i])
            cum.append((cum[-1][0]+dy,cum[-1][1]+dx))
        tot=max(abs(cum[-1][0]),abs(cum[-1][1]))
        if tot<25:
            print('   run %d-%d: total cumulative motion only %.0f px, skipped (hypotheses not separable)'%(s,e,tot)); continue
        R=[f-gaussian_filter(f,5.0) for f in fr]
        # trim border to the max shift so all three medians cover the same valid area
        M=int(np.ceil(max(max(abs(c[0]),abs(c[1])) for c in cum)))+3
        def med(shifts):
            st=[]
            for R_,(dy,dx) in zip(R,shifts):
                w=ndshift(R_,(-dy,-dx),order=1,mode='nearest')
                st.append(w[M:-M,M:-M])
            return np.median(np.stack(st),axis=0)
        Mf=med([(0,0)]*len(R))
        Mi=med(cum)
        rnd=[(0.0,0.0)]+[ (rng.normal()*abs(c[0]) if c[0] else rng.normal()*5, rng.normal()*abs(c[1]) if c[1] else rng.normal()*5) for c in cum[1:]]
        Mr=med(rnd)
        def score(A):
            sg=1.4826*np.median(np.abs(A-np.median(A)))
            return float(np.percentile(np.abs(A),99.9)/max(sg,1e-9)), float(sg), float(np.abs(A).max())
        sf=score(Mf); si=score(Mi); sr=score(Mr)
        print('   run %5d-%5d cumulative motion (dy,dx)=(%+.0f,%+.0f) |%d frames| : score M_frame=%5.2f (sig %.3f, max %5.2f) | M_image=%5.2f (sig %.3f, max %5.2f) | M_rand=%5.2f (sig %.3f, max %5.2f)'%(
            s,e,cum[-1][0],cum[-1][1],len(R),sf[0],sf[1],sf[2],si[0],si[1],si[2],sr[0],sr[1],sr[2]),flush=True)
        rows.append(dict(run=[s,e],cum=[float(cum[-1][0]),float(cum[-1][1])],frame=sf,image=si,rand=sr))
    res[k]=rows
json.dump(res,open('taskC4.json','w'),indent=1,default=float)
