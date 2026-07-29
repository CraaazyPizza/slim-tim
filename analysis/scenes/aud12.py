import numpy as np, wave
from scipy import signal
from scipy.ndimage import median_filter
def rd(p):
    w=wave.open(p); n=w.getnframes(); sr=w.getframerate()
    return np.frombuffer(w.readframes(n),dtype=np.int16).astype(np.float64)/32768., sr
v1,sr=rd('v1_full.wav')
seg=v1[int(86.0*sr):int(97.0*sr)]
# Coherent-average approach: split into 8 chunks, average magnitude spectra -> lines survive, noise averages down
NF=1<<21
chunks=[seg[i:i+int(2.0*sr)] for i in range(0,len(seg)-int(2.0*sr),int(1.1*sr))]
acc=None
for c in chunks:
    w=c*np.hanning(len(c))
    F=np.abs(np.fft.rfft(w,NF))
    acc=F if acc is None else acc+F
f=np.fft.rfftfreq(NF,1/sr); P=20*np.log10(acc/len(chunks)+1e-12)
E=P-median_filter(P,1501)
m=(f>=15)&(f<=1500); ff=f[m]; EE=E[m]
carpet=np.percentile(EE,99.9)
print('99.9th pct carpet = %.1f dB (n=%d bins)'%(carpet,len(EE)))
pk=signal.find_peaks(EE,height=carpet,distance=int(1.0/(f[1]-f[0])))[0]
lines=sorted(zip(EE[pk],ff[pk]),reverse=True)
print('lines above 99.9pct carpet (%d):'%len(lines))
for v,fr in lines: print('   %8.3f Hz  %5.1f dB   /23.9760=%7.3f   /49.952=%7.3f'%(fr,v,fr/23.9760,fr/49.952))
