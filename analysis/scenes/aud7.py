import numpy as np, wave
from scipy import signal
from scipy.ndimage import median_filter
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def rd(p):
    w=wave.open(p); n=w.getnframes(); sr=w.getframerate()
    return np.frombuffer(w.readframes(n),dtype=np.int16).astype(np.float64)/32768., sr
v1,sr=rd('v1_full.wav'); rs,_=rd('rs2011_full.wav'); v2,_=rd('v2_full.wav'); zb,_=rd('zb2011_full.wav')
seg=v1[int(85.6*sr):int(97.0*sr)]; bed=v1[int(55*sr):int(80*sr)]

def E_of(x,nfft=1<<20):
    f,P=signal.welch(x,sr,nperseg=min(nfft,len(x)),noverlap=min(nfft,len(x))//2,nfft=nfft)
    D=10*np.log10(P+1e-16); return f, D-median_filter(D,301)

def combfit(x,label,f0lo,f0hi,fmax=1000):
    f,E=E_of(x)
    m=f<=fmax; f=f[m]; E=E[m]
    best=(-99,0)
    for f0 in np.arange(f0lo,f0hi,0.0005):
        hs=np.arange(1,int(fmax/f0)+1)*f0
        idx=np.searchsorted(f,hs); idx=idx[idx<len(f)]
        v=E[idx].mean()
        if v>best[0]: best=(v,f0)
    print(f'{label}: best comb in [{f0lo},{f0hi}] -> f0={best[1]:.4f} Hz, mean harmonic excess {best[0]:.2f} dB')
    return best

for lab,x in [('col/s',seg),('v1 bed',bed),('2011 Rs',rs),('2011 ZB',zb),('2026 v2',v2)]:
    combfit(x,lab,23.0,25.0)
print()
for lab,x in [('col/s',seg),('v1 bed',bed),('2011 Rs',rs),('2026 v2',v2)]:
    combfit(x,lab,12.5,14.5)
print()
# individual harmonic excesses for col/s at 23.976 and 49.95
f,E=E_of(seg)
print('col/s harmonic table:')
for base,name in [(23.976,'23.976Hz'),(49.953,'49.953Hz')]:
    row=[]
    for n in range(1,13):
        tgt=base*n
        if tgt>2000: break
        m=(f>tgt-0.6)&(f<tgt+0.6)
        row.append((n,round(float(f[m][np.argmax(E[m])]),3),round(float(E[m].max()),1)))
    print(' ',name,row)
# same table for bed as control
f,E=E_of(bed)
print('bed control at 23.976:',[(n,round(float(E[(f>23.976*n-0.6)&(f<23.976*n+0.6)].max()),1)) for n in range(1,9)])
print('bed control at 49.953:',[(n,round(float(E[(f>49.953*n-0.6)&(f<49.953*n+0.6)].max()),1)) for n in range(1,5)])
