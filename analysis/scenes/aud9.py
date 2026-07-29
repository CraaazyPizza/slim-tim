import numpy as np, wave
from scipy import signal
from scipy.ndimage import median_filter
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def rd(p):
    w=wave.open(p); n=w.getnframes(); sr=w.getframerate()
    return np.frombuffer(w.readframes(n),dtype=np.int16).astype(np.float64)/32768., sr
v1,sr=rd('v1_full.wav')
seg=v1[int(85.6*sr):int(97.0*sr)]; bed=v1[int(55*sr):int(80*sr)]
# is the 13 Hz bed still present in col/s, in the HF band where col/s adds little?
def hp_modspec(x,lab,band):
    b,a=signal.butter(4,[band[0]/(sr/2),band[1]/(sr/2)],'band'); y=signal.filtfilt(b,a,x)
    e=np.abs(signal.hilbert(y)); e=signal.decimate(e,10); fs=sr/10; e=e-e.mean()
    f,P=signal.welch(e,fs,nperseg=int(fs*4),noverlap=int(fs*2))
    m=(f>6)&(f<25); D=10*np.log10(P[m]+1e-18); D=D-median_filter(D,31)
    i=np.argmax(D)
    print(f'{lab} band {band}: mod peak {f[m][i]:.2f} Hz, prom {D[i]:.1f} dB')
for band in [(60,800),(800,2000),(2000,4000),(4000,7000)]:
    hp_modspec(seg,'col/s',band); hp_modspec(bed,'bed  ',band); print()

# clean PSD plot
plt.figure(figsize=(13,5.5))
for lab,y,c in [('v1 colour "(col/s)" 85.6-97 s',seg,'tab:blue'),('v1 b/w projector bed 55-80 s',bed,'tab:green')]:
    f,P=signal.welch(y,sr,nperseg=1<<15,noverlap=1<<14); D=10*np.log10(P+1e-16)
    plt.semilogx(f[1:],D[1:],lw=.3,alpha=.3,color=c)
    plt.semilogx(f[1:],median_filter(D,81)[1:],lw=2.0,color=c,label=lab)
plt.xlim(20,20000); plt.ylim(-140,-25); plt.grid(alpha=.3,which='both'); plt.legend()
plt.xlabel('Hz'); plt.ylabel('PSD dB'); plt.title('v1: colour segment adds ~30 dB of low-frequency rumble; the two converge above ~2 kHz')
plt.tight_layout(); plt.savefig('aud_psd_absolute.png',dpi=120); plt.close()
