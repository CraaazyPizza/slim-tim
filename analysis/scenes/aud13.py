import numpy as np, wave
from scipy import signal
from scipy.ndimage import median_filter
def rd(p):
    w=wave.open(p); n=w.getnframes(); sr=w.getframerate()
    return np.frombuffer(w.readframes(n),dtype=np.int16).astype(np.float64)/32768., sr
v1,sr=rd('v1_full.wav')
def inventory(x,label,fhi=1500):
    n=len(x); w=x*np.hanning(n)
    NF=1<<22
    F=np.abs(np.fft.rfft(w,NF)); f=np.fft.rfftfreq(NF,1/sr)
    P=20*np.log10(F+1e-12); E=P-median_filter(P,int(6/(f[1]-f[0])))
    m=(f>=20)&(f<=fhi); ff=f[m]; EE=E[m]
    carpet=np.percentile(EE,99.95)
    pk=signal.find_peaks(EE,height=carpet,distance=int(0.5/(f[1]-f[0])))[0]
    lines=sorted(zip(EE[pk],ff[pk]),reverse=True)
    print(f'\n=== {label}  (dur {n/sr:.1f}s)  99.95pct carpet {carpet:.1f} dB, {len(lines)} lines ===')
    for v,fr in lines[:25]:
        print('   %9.4f Hz  %5.1f dB   /23.976=%8.4f  /49.952=%8.4f  /13.03=%8.3f'%(fr,v,fr/23.976,fr/49.952,fr/13.032))
inventory(v1[int(86.0*sr):int(97.0*sr)],'v1 colour (col/s) 86-97 s')
inventory(v1[int(58*sr):int(69*sr)],'v1 b/w projector bed 58-69 s')
rs,_=rd('rs2011_full.wav'); inventory(rs[int(30*sr):int(41*sr)],'2011 RsQCXN4o4Ps 30-41 s')
