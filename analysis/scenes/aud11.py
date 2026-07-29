import numpy as np, wave
from scipy import signal
from scipy.ndimage import median_filter
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def rd(p):
    w=wave.open(p); n=w.getnframes(); sr=w.getframerate()
    return np.frombuffer(w.readframes(n),dtype=np.int16).astype(np.float64)/32768., sr
v1,sr=rd('v1_full.wav')
seg=v1[int(86.6*sr):int(97.0*sr)]  # skip fade-in
x=seg-seg.mean()
n=len(x)
F=np.fft.rfft(x,2*n); ac=np.fft.irfft(F*np.conj(F))[:n]; ac/=ac[0]
lags=np.arange(n)/sr
m=(lags>0.05)&(lags<5)
pk=signal.find_peaks(ac[m],height=0.02)[0]
top=sorted(zip(ac[m][pk],lags[m][pk]),reverse=True)[:12]
print('waveform autocorr top lags (>0.05s):',[(round(l,4),round(v,4)) for v,l in top])
print('ac at 0.5005 s =',round(float(np.interp(0.5005,lags,ac)),4))
print('ac max in 0.05-5s =',round(float(ac[m].max()),4))
# spectral-frame self-similarity (loop detector, robust to phase)
f,t,S=signal.spectrogram(x,sr,nperseg=2048,noverlap=1024,mode='magnitude')
S=np.log10(S+1e-8); S=(S-S.mean(1,keepdims=True))/(S.std(1,keepdims=True)+1e-9)
C=np.corrcoef(S.T)
d=[]
for k in range(1,C.shape[0]-3):
    d.append((np.mean(np.diagonal(C,k)),k*1024/sr))
d.sort(reverse=True)
print('spectro self-sim top lags:',[(round(l,3),round(v,3)) for v,l in d[:8]])
print('median self-sim:',round(np.median([v for v,l in d]),3))
plt.figure(figsize=(13,4)); plt.plot(lags[lags<5],ac[lags<5],lw=.6); plt.xlabel('lag (s)'); plt.ylabel('normalised autocorr')
plt.title('col/s waveform autocorrelation — no loop peak'); plt.grid(alpha=.3)
plt.tight_layout(); plt.savefig('aud_colseg_autocorr.png',dpi=120); plt.close()
