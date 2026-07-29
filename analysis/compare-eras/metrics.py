import sys,numpy as np
from PIL import Image
pre=sys.argv[1]; label=sys.argv[2]
A=np.load(pre+'_hp.npy')          # (nruns, H, W) high-passed, unit-std
mx=A.max(0)
P=np.clip(mx,0,None)
# row profile -> cap height
rp=P.mean(1)
rthr=rp.max()*0.35
rows=np.nonzero(rp>rthr)[0]
# column profile -> pitch via FFT
cp=P.mean(0)
cthr=cp.max()*0.30
cols=np.nonzero(cp>cthr)[0]
seg=cp[cols.min():cols.max()+1]-cp[cols.min():cols.max()+1].mean()
F=np.abs(np.fft.rfft(seg*np.hanning(len(seg))))
freqs=np.fft.rfftfreq(len(seg))
# search pitch 20..80 px
band=[(1/f,F[i]) for i,f in enumerate(freqs) if f>0 and 20<=1/f<=80]
band.sort(key=lambda t:-t[1])
print('%-6s rows %d-%d  capH=%d   cols %d-%d  textW=%d'%(label,rows.min(),rows.max(),rows.max()-rows.min()+1,cols.min(),cols.max(),cols.max()-cols.min()+1))
print('       top pitch candidates:', [(round(p,2),round(v,1)) for p,v in band[:4]])
# refine: autocorrelation of column profile
s=seg-seg.mean(); ac=np.correlate(s,s,'full')[len(s)-1:]; ac/=ac[0]
best=[(lag,ac[lag]) for lag in range(20,81)]
best.sort(key=lambda t:-t[1])
print('       autocorr best lags:', [(l,round(v,3)) for l,v in best[:5]])
np.save(pre+'_P.npy',P)
print('       col profile valleys/peaks (x rel band):')
print('      ', ' '.join('%d:%d'%(i,round(v*10)) for i,v in enumerate(cp) if v>cthr*0.0 and i%1==0 and False) or '')
