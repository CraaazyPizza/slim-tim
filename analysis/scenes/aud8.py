import numpy as np, wave
from scipy import signal
from scipy.ndimage import median_filter
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def rd(p):
    w=wave.open(p); n=w.getnframes(); sr=w.getframerate()
    return np.frombuffer(w.readframes(n),dtype=np.int16).astype(np.float64)/32768., sr
v1,sr=rd('v1_full.wav')
seg=v1[int(85.6*sr):int(97.0*sr)]; bed=v1[int(55*sr):int(80*sr)]

# notch out mains + machine lines, then voicing test
x=seg.copy()
for fq in [49.95,99.91,149.86,23.98,47.95,71.93,95.9,119.89,143.87,167.8,191.8]:
    b,a=signal.iirnotch(fq/(sr/2),Q=60); x=signal.filtfilt(b,a,x)
def voicing(y,label,thr=0.5):
    N=int(0.040*sr); H=int(0.010*sr)
    b,a=signal.butter(4,[80/(sr/2),1500/(sr/2)],'band'); yf=signal.filtfilt(b,a,y)
    ac_pk=[];f0=[]
    for i in range(0,len(yf)-N,H):
        w=yf[i:i+N]*np.hanning(N)
        r=np.correlate(w,w,'full')[N-1:]; r/=(r[0]+1e-12)
        lo=int(sr/350); hi=int(sr/80); k=np.argmax(r[lo:hi])+lo
        ac_pk.append(r[k]); f0.append(sr/k)
    ac_pk=np.array(ac_pk)
    print(f'{label}: {100*(ac_pk>thr).mean():.1f}% frames AC>{thr}; max run of consecutive = {max([len(s) for s in "".join(["1" if v else "0" for v in ac_pk>thr]).split("0")] or [0])} frames ({10*max([len(s) for s in "".join(["1" if v else "0" for v in ac_pk>thr]).split("0")] or [0])} ms)')
    return ac_pk,np.array(f0)
voicing(x,'col/s (hum notched)')
voicing(bed,'bed control')
# random noise control
rng=np.random.default_rng(0)
nz=signal.lfilter([1],[1,-0.9],rng.standard_normal(len(x)))
voicing(nz/np.abs(nz).max()*0.2,'pink-ish noise control')

# absolute smoothed spectrum
plt.figure(figsize=(13,5))
for lab,y in [('v1 col/s 85.6-97',seg),('v1 b/w bed 55-80',bed)]:
    f,P=signal.welch(y,sr,nperseg=1<<15,noverlap=1<<14)
    D=10*np.log10(P+1e-16)
    plt.semilogx(f[1:],median_filter(D,51)[1:],lw=1.4,label=lab+' (smoothed)')
    plt.semilogx(f[1:],D[1:],lw=.35,alpha=.45)
plt.xlim(20,20000); plt.grid(alpha=.3,which='both'); plt.legend(); plt.xlabel('Hz'); plt.ylabel('dB (PSD)')
plt.title('Absolute PSD: colour(col/s) segment vs projector bed — v1')
plt.tight_layout(); plt.savefig('aud_psd_absolute.png',dpi=110); plt.close()

# annotated line chart
f,P=signal.welch(seg,sr,nperseg=1<<19,noverlap=1<<18)
D=10*np.log10(P+1e-16); E=D-median_filter(D,301)
plt.figure(figsize=(15,5))
m=(f>=15)&(f<=260); plt.plot(f[m],E[m],lw=.8,color='k')
for fq,lab,c in [(49.95,'49.95 (mains f0)','tab:red'),(99.91,'99.91 (mains 2f)','tab:red'),(149.83,'149.83 (mains 3f)','tab:red'),
                 (95.9,'95.9 (4x23.98)','tab:blue'),(119.89,'119.89 (5x)','tab:blue'),(143.88,'143.88 (6x)','tab:blue'),(191.8,'191.8 (8x)','tab:blue'),(71.96,'71.96 (3x)','tab:blue')]:
    plt.axvline(fq,color=c,ls=':',alpha=.8); plt.text(fq,22,lab,rotation=90,fontsize=7,color=c,va='top')
plt.ylabel('dB above local median'); plt.xlabel('Hz'); plt.ylim(-8,25); plt.grid(alpha=.3)
plt.title('v1 colour(col/s) segment: two independent line systems — 49.95 Hz mains series (red) and 23.98 Hz rotating-machine series (blue)')
plt.tight_layout(); plt.savefig('aud_colseg_lines.png',dpi=120); plt.close()
