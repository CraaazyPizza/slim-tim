import numpy as np, wave
from scipy import signal
from scipy.ndimage import median_filter
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def rd(p):
    w=wave.open(p); n=w.getnframes(); sr=w.getframerate()
    return np.frombuffer(w.readframes(n),dtype=np.int16).astype(np.float64)/32768., sr
seg,sr=rd('col_85_97.wav'); c15,_=rd('col_85_97_pitch1.5.wav')
fig,axs=plt.subplots(2,1,figsize=(15,9))
for ax,(lab,x) in zip(axs,[('as published (0.666x picture speed) — 85-97 s',seg),
                           ('audio resampled x1.5 ("undo" the slowdown)',c15)]):
    f,t,S=signal.spectrogram(x,sr,nperseg=8192,noverlap=8192-1024,mode='magnitude')
    m=f<=1000
    ax.pcolormesh(t,f[m],20*np.log10(S[m]+1e-10),shading='auto',vmin=-105,vmax=-40,cmap='magma')
    for h,c in [(49.95,'cyan'),(99.91,'cyan'),(149.86,'cyan')]:
        k=1.5 if 'x1.5' in lab else 1.0
        ax.axhline(h*k,color=c,ls=':',lw=.8)
    ax.set_ylabel('Hz'); ax.set_title('v1 colour (col/s) segment — '+lab+'   [cyan = the 49.95/99.91/149.86 Hz lines, scaled]')
axs[1].set_xlabel('s')
plt.tight_layout(); plt.savefig('aud_speed_correction.png',dpi=115); plt.close()
# numbers
for lab,x,k in [('native',seg,1.0),('x1.5',c15,1.5)]:
    f,P=signal.welch(x,sr,nperseg=1<<18,noverlap=1<<17)
    D=10*np.log10(P+1e-16); E=D-median_filter(D,301)
    out=[]
    for base in [50,60]:
        tot=0
        for n in (1,2,3):
            t_=base*n; m=(f>t_-1.5)&(f<t_+1.5); tot+=E[m].max()
        out.append((base,round(tot/3,1)))
    print(lab,'mean harmonic excess over n=1..3 :',out)
