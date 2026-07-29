import numpy as np, wave
from scipy import signal
from scipy.ndimage import median_filter
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def rd(p):
    w=wave.open(p); n=w.getnframes(); sr=w.getframerate()
    return np.frombuffer(w.readframes(n),dtype=np.int16).astype(np.float64)/32768., sr
v1,sr=rd('v1_full.wav'); rs,_=rd('rs2011_full.wav'); v2,_=rd('v2_full.wav')
seg=v1[int(85.6*sr):int(97.0*sr)]
bed=v1[int(55*sr):int(80*sr)]

def comb_scan(x, f0lo=8, f0hi=30, step=0.005, fmax=1500):
    f,P=signal.welch(x,sr,nperseg=1<<19,noverlap=(1<<19)//2)
    P=10*np.log10(P+1e-16); base=median_filter(P,401); E=P-base
    m=f<=fmax; f=f[m]; E=E[m]
    best=[]
    for f0 in np.arange(f0lo,f0hi,step):
        hs=np.arange(1,int(fmax/f0)+1)*f0
        idx=np.searchsorted(f,hs); idx=idx[idx<len(f)]
        best.append((E[idx].mean(),f0))
    best.sort(reverse=True)
    return best[:6], (f,E)

for name,x in [('v1 col/s',seg),('v1 bed',bed),('2011 Rs',rs),('2026 v2',v2)]:
    top,_=comb_scan(x)
    print(name,'comb f0 candidates:',[(round(f0,3),round(v,2)) for v,f0 in top])

# precise hum lines
print()
for name,x in [('v1 col/s',seg),('v1 bed',bed)]:
    f,P=signal.welch(x,sr,nperseg=1<<20,noverlap=(1<<20)//2)
    for target in [50,60,100,120,150,180]:
        m=(f>target-1.2)&(f<target+1.2)
        pk=f[m][np.argmax(P[m])]
        loc=(f>target-6)&(f<target+6)
        prom=10*np.log10(P[m].max()/np.median(P[loc]))
        print(f'{name}: near {target} Hz -> peak {pk:.4f} Hz, prominence {prom:.1f} dB')
    print()
