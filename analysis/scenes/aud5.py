import numpy as np, wave
from scipy import signal
from scipy.ndimage import median_filter
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def rd(p):
    w=wave.open(p); n=w.getnframes(); sr=w.getframerate()
    return np.frombuffer(w.readframes(n),dtype=np.int16).astype(np.float64)/32768., sr
v1,sr=rd('v1_full.wav'); rs,_=rd('rs2011_full.wav'); v2,_=rd('v2_full.wav')
seg=v1[int(85.6*sr):int(97.0*sr)]; bed=v1[int(55*sr):int(80*sr)]
segA=v1[int(85.6*sr):int(91.3*sr)]; segB=v1[int(91.3*sr):int(97.0*sr)]

def modspec(x,label):
    e=np.abs(signal.hilbert(x))
    e=signal.decimate(e,10); fs=sr/10
    e=e-e.mean()
    f,P=signal.welch(e,fs,nperseg=int(fs*4),noverlap=int(fs*2))
    m=(f>4)&(f<40)
    base=median_filter(10*np.log10(P[m]+1e-16),31)
    E=10*np.log10(P[m]+1e-16)-base
    i=np.argmax(E)
    print(f'{label}: envelope-mod peak {f[m][i]:.3f} Hz, prominence {E[i]:.1f} dB')
    return f[m],E
plt.figure(figsize=(13,5))
for lab,x in [('v1 col/s 85.6-97',seg),('v1 col/s first half',segA),('v1 col/s 2nd half',segB),('v1 bed 55-80',bed),('2011 Rs',rs),('2026 v2',v2)]:
    f,E=modspec(x,lab); plt.plot(f,E,lw=.9,label=lab)
plt.legend(fontsize=8); plt.grid(alpha=.3); plt.xlabel('modulation freq (Hz)'); plt.ylabel('dB over local median')
plt.title('Amplitude-envelope modulation spectra')
plt.tight_layout(); plt.savefig('aud_modspec.png',dpi=110); plt.close()

# resample hypothesis: is col/s the bed pitch-shifted?
def logspec(x,nper=1<<16):
    f,P=signal.welch(x,sr,nperseg=nper,noverlap=nper//2)
    m=(f>60)&(f<9000)
    lf=np.log(f[m]); P=10*np.log10(P[m]+1e-16)
    g=np.linspace(lf[0],lf[-1],3000)
    v=np.interp(g,lf,P)
    v=v-median_filter(v,201)
    return g,v
g,vs=logspec(seg); _,vb=logspec(bed)
best=[]
for sh in np.arange(-200,201):
    a=np.roll(vs,sh)
    lo,hi=250,2750
    c=np.corrcoef(a[lo:hi],vb[lo:hi])[0,1]
    best.append((c,sh))
best.sort(reverse=True)
dg=g[1]-g[0]
print('\nresample-shift test col/s vs bed: best corr %.3f at ratio %.4f'%(best[0][0], np.exp(best[0][1]*dg)))
print('  corr at ratio 1.000:', round(np.corrcoef(vs[250:2750],vb[250:2750])[0,1],3))
# control: bed vs 2011 Rs
_,vr=logspec(rs)
print('  control bed vs 2011Rs at ratio 1.000:', round(np.corrcoef(vb[250:2750],vr[250:2750])[0,1],3))
_,v2s=logspec(v2)
print('  control bed vs 2026v2 at ratio 1.000:', round(np.corrcoef(vb[250:2750],v2s[250:2750])[0,1],3))
print('  col/s vs 2011Rs at ratio 1.000:', round(np.corrcoef(vs[250:2750],vr[250:2750])[0,1],3))
