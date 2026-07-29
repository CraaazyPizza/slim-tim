import numpy as np, wave
from scipy import signal
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
def rd(p):
    w=wave.open(p); n=w.getnframes(); sr=w.getframerate()
    return np.frombuffer(w.readframes(n),dtype=np.int16).astype(np.float64)/32768., sr
v1,sr=rd('v1_full.wav')
seg=v1[int(85.0*sr):int(97.0*sr)]
bed=v1[int(55*sr):int(80*sr)]      # b/w section bed
rs,_=rd('rs2011_full.wav'); zb,_=rd('zb2011_full.wav')
v2,_=rd('v2_full.wav')

def spec(x,sr,nper=4096,ov=None,fmax=8000):
    ov = ov or nper*3//4
    f,t,S=signal.spectrogram(x,sr,nperseg=nper,noverlap=ov,window='hann',scaling='spectrum',mode='magnitude')
    m=f<=fmax
    return f[m],t,20*np.log10(S[m]+1e-10)

fig,axs=plt.subplots(4,1,figsize=(15,13),sharex=False)
for ax,(name,x,off) in zip(axs,[('v1 col/s 85-97s',seg,85),('v1 b/w bed 55-80s',bed,55),('2011 RsQCXN4o4Ps full',rs,0),('2026 v2 full',v2,0)]):
    f,t,S=spec(x,sr)
    ax.pcolormesh(t+off,f,S,shading='auto',vmin=-100,vmax=-20,cmap='magma')
    ax.set_ylabel('Hz'); ax.set_title(name); ax.set_ylim(0,8000)
plt.tight_layout(); plt.savefig('aud_spec_overview.png',dpi=110); plt.close()

# zoom: low band 0-500 Hz for mains hum
fig,axs=plt.subplots(3,1,figsize=(15,10))
for ax,(name,x,off) in zip(axs,[('v1 col/s 85-97s (0-500Hz)',seg,85),('v1 bed 55-80s (0-500Hz)',bed,55),('2011 Rs (0-500Hz)',rs,0)]):
    f,t,S=spec(x,sr,nper=16384,fmax=500)
    ax.pcolormesh(t+off,f,S,shading='auto',cmap='magma')
    ax.set_ylabel('Hz'); ax.set_title(name)
plt.tight_layout(); plt.savefig('aud_spec_lowband.png',dpi=110); plt.close()

# average spectra, normalized
def avgspec(x,nper=16384):
    f,P=signal.welch(x,sr,nperseg=nper,noverlap=nper//2)
    return f,10*np.log10(P+1e-14)
plt.figure(figsize=(14,6))
for name,x in [('v1 col/s 85-97',seg),('v1 bed 55-80',bed),('2011 Rs',rs),('2011 ZB',zb),('2026 v2',v2)]:
    f,P=avgspec(x)
    plt.semilogx(f[1:],P[1:]-P[(f>200)&(f<400)].mean(),label=name,lw=.8)
plt.xlim(20,10000); plt.grid(alpha=.3); plt.legend(); plt.xlabel('Hz'); plt.ylabel('dB (normalized @200-400Hz)')
plt.title('Welch PSD, shape-normalized')
plt.tight_layout(); plt.savefig('aud_psd_compare.png',dpi=110); plt.close()

# mains hum test: high-res spectrum 40-130 Hz
plt.figure(figsize=(14,6))
for name,x in [('v1 col/s',seg),('v1 bed',bed),('2011 Rs',rs),('2026 v2',v2)]:
    f,P=signal.welch(x,sr,nperseg=1<<18,noverlap=(1<<18)//2)
    m=(f>=30)&(f<=200)
    plt.plot(f[m],10*np.log10(P[m]+1e-16),label=name,lw=.8)
for h in [50,100,150,60,120,180]:
    plt.axvline(h,color='r' if h%60==0 else 'b',ls=':',alpha=.5)
plt.legend(); plt.grid(alpha=.3); plt.xlabel('Hz'); plt.title('30-200 Hz fine spectrum (blue dotted=50Hz harmonics, red=60Hz)')
plt.tight_layout(); plt.savefig('aud_mains.png',dpi=110); plt.close()

# numeric peak picking 40-200Hz
print('=== fine peaks 35-200 Hz ===')
for name,x in [('v1 col/s',seg),('v1 bed',bed),('v1 full',v1),('2011 Rs',rs),('2011 ZB',zb),('2026 v2',v2)]:
    f,P=signal.welch(x,sr,nperseg=1<<18,noverlap=(1<<18)//2)
    m=(f>=35)&(f<=200); ff=f[m]; pp=10*np.log10(P[m]+1e-16)
    # local baseline
    from scipy.ndimage import median_filter
    base=median_filter(pp,201)
    exc=pp-base
    idx=signal.find_peaks(exc,height=3,distance=20)[0]
    tops=sorted(zip(exc[idx],ff[idx]),reverse=True)[:8]
    print(name, [(round(fr,3),round(e,1)) for e,fr in tops])
