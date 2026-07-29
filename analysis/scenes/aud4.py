import numpy as np, wave
from scipy import signal
from scipy.ndimage import median_filter
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def rd(p):
    w=wave.open(p); n=w.getnframes(); sr=w.getframerate()
    return np.frombuffer(w.readframes(n),dtype=np.int16).astype(np.float64)/32768., sr
v1,sr=rd('v1_full.wav')
t0=85.6; seg=v1[int(t0*sr):int(97.0*sr)]
bed=v1[int(55*sr):int(80*sr)]

# --- narrowband spectrogram 0-4kHz, high time res, whitened
def whiten_spec(x,nper,ov,fmax):
    f,t,S=signal.spectrogram(x,sr,nperseg=nper,noverlap=ov,window='hann',mode='magnitude')
    m=f<=fmax; f=f[m]; S=S[m]
    D=20*np.log10(S+1e-10)
    D=D-median_filter(D,size=(1,31))   # remove stationary lines -> highlight transients/speech
    return f,t,D
f,t,D=whiten_spec(seg,2048,2048-256,4000)
plt.figure(figsize=(18,6))
plt.pcolormesh(t+t0,f,D,shading='auto',vmin=-6,vmax=14,cmap='inferno')
plt.colorbar(label='dB above time-median'); plt.ylabel('Hz'); plt.xlabel('video time (s)')
plt.title('v1 col/s 85.6-97.0s — time-whitened spectrogram (stationary bed removed)')
plt.tight_layout(); plt.savefig('aud_colseg_whitened.png',dpi=110); plt.close()

f,t,D=whiten_spec(bed[:int(11.4*sr)],2048,2048-256,4000)
plt.figure(figsize=(18,6))
plt.pcolormesh(t+55,f,D,shading='auto',vmin=-6,vmax=14,cmap='inferno')
plt.colorbar(); plt.ylabel('Hz'); plt.title('CONTROL: v1 b/w bed 55-66.4s — same processing')
plt.tight_layout(); plt.savefig('aud_bed_whitened.png',dpi=110); plt.close()

# --- transient detection (spectral flux onsets)
def onsets(x,label):
    nper=1024; hop=128
    f,tt,S=signal.spectrogram(x,sr,nperseg=nper,noverlap=nper-hop,mode='magnitude')
    S=np.log10(S+1e-8)
    flux=np.maximum(np.diff(S,axis=1),0).sum(0)
    flux=flux/flux.std()
    pk,props=signal.find_peaks(flux,height=3.0,distance=int(0.06*sr/hop))
    tp=tt[pk+1]
    print(f'{label}: {len(tp)} onsets in {len(x)/sr:.1f}s = {len(tp)/(len(x)/sr):.2f}/s')
    return tt[1:],flux,tp
tt,flux,tp=onsets(seg,'col/s')
tt2,flux2,tp2=onsets(bed,'bed(25s)')
np.save('colseg_onsets.npy',tp)
print('col/s onset times (video s):',np.round(tp+t0,3)[:60])
d=np.diff(tp)
print('IOI stats: n=%d mean=%.3f med=%.3f min=%.3f max=%.3f'%(len(d),d.mean(),np.median(d),d.min(),d.max()))
# IOI histogram / autocorr of onset train for rhythm
plt.figure(figsize=(14,7))
plt.subplot(2,1,1); plt.plot(tt+t0,flux,lw=.6); plt.plot(tp+t0,np.interp(tp,tt,flux),'rv',ms=4)
plt.title('col/s spectral flux + detected onsets'); plt.xlabel('video s')
plt.subplot(2,1,2); plt.hist(d,bins=np.arange(0,2.0,0.04)); plt.xlabel('inter-onset interval (s)'); plt.title('IOI histogram')
plt.tight_layout(); plt.savefig('aud_colseg_onsets.png',dpi=110); plt.close()

# --- voicing test: autocorrelation-based F0 on 40ms frames, band 60-400 Hz
def voicing(x,label):
    N=int(0.040*sr); H=int(0.010*sr)
    b,a=signal.butter(4,[70/(sr/2),1200/(sr/2)],'band')
    xf=signal.filtfilt(b,a,x)
    res=[]
    for i in range(0,len(xf)-N,H):
        w=xf[i:i+N]*np.hanning(N)
        if np.sqrt((w**2).mean())<1e-4: res.append((0,0)); continue
        ac=np.correlate(w,w,'full')[N-1:]
        ac/= (ac[0]+1e-12)
        lo=int(sr/400); hi=int(sr/70)
        k=np.argmax(ac[lo:hi])+lo
        res.append((ac[k],sr/k))
    res=np.array(res)
    strong=res[:,0]>0.45
    print(f'{label}: frames={len(res)} voiced-like(ac>0.45)={strong.sum()} ({100*strong.mean():.1f}%)  median F0 of those={np.median(res[strong,1]) if strong.sum() else float("nan"):.1f} Hz')
    return res
rs_=voicing(seg,'col/s'); rb_=voicing(bed,'bed')
np.save('voicing_col.npy',rs_)
plt.figure(figsize=(16,5))
tv=np.arange(len(rs_))*0.010+t0
plt.subplot(2,1,1); plt.plot(tv,rs_[:,0],lw=.7); plt.axhline(0.45,color='r',ls=':'); plt.ylabel('AC peak'); plt.title('col/s periodicity strength (voicing proxy)')
plt.subplot(2,1,2); m=rs_[:,0]>0.45; plt.plot(tv[m],rs_[m,1],'.',ms=2); plt.ylabel('F0 Hz'); plt.xlabel('video s'); plt.ylim(60,400)
plt.tight_layout(); plt.savefig('aud_colseg_voicing.png',dpi=110); plt.close()
