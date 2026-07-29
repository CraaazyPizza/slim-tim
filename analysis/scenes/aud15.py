import numpy as np, wave
from scipy import signal
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def rd(p):
    w=wave.open(p); n=w.getnframes(); sr=w.getframerate()
    return np.frombuffer(w.readframes(n),dtype=np.int16).astype(np.float64)/32768., sr
v1,sr=rd('v1_full.wav')
x=v1[int(86.0*sr):int(97.0*sr)]
def analytic_band(y,f0,bw):
    N=len(y); F=np.fft.rfft(y); f=np.fft.rfftfreq(N,1/sr)
    G=np.exp(-0.5*((f-f0)/(bw/2.355))**2)
    z=np.fft.irfft(F*G,N)
    return signal.hilbert(z)
def instf(y,f0,bw=1.5,W=0.5,hop=0.05):
    z=analytic_band(y,f0,bw); ph=np.unwrap(np.angle(z))
    w=int(W*sr); t=np.arange(0,len(ph)-w,int(hop*sr))
    fr=np.array([(ph[i+w]-ph[i])/(2*np.pi*w/sr) for i in t])
    return t/sr,fr
plt.figure(figsize=(13,7)); res={}
for i,(f0,lab) in enumerate([(99.907,'99.907 Hz'),(143.864,'143.864 Hz'),(191.814,'191.814 Hz')]):
    t,fr=instf(x,f0); res[f0]=(t,fr)
    print('%s: mean %.4f, sd %.4f, p2p %.4f Hz'%(lab,fr.mean(),fr.std(),fr.max()-fr.min()))
    plt.subplot(3,1,i+1); plt.plot(t+86,fr,lw=1); plt.axhline(fr.mean(),color='r',ls=':'); plt.ylabel(lab); plt.grid(alpha=.3)
plt.xlabel('video s'); plt.suptitle('Instantaneous frequency, three strongest col/s tones (0.5 s window)')
plt.tight_layout(); plt.savefig('aud_instfreq.png',dpi=120); plt.close()
a=res[99.907][1]/99.907; b=res[143.864][1]/143.864; c=res[191.814][1]/191.814
n=min(map(len,[a,b,c])); a,b,c=a[:n],b[:n],c[:n]
print('fractional drift corr: 99/144 %.3f  144/192 %.3f  99/192 %.3f'%(np.corrcoef(a,b)[0,1],np.corrcoef(b,c)[0,1],np.corrcoef(a,c)[0,1]))
rng=np.random.default_rng(3)
amp=np.sqrt(np.mean(np.abs(analytic_band(x,99.907,1.5))**2))
syn=amp*np.sqrt(2)*np.sin(2*np.pi*99.907*np.arange(len(x))/sr)+rng.standard_normal(len(x))*np.std(x)
t,fr=instf(syn,99.907); print('CONTROL synthetic pure tone, matched SNR: sd %.4f Hz'%fr.std())
