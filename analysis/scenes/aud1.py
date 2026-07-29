import numpy as np, wave
from scipy import signal
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def rd(p):
    w=wave.open(p); n=w.getnframes(); sr=w.getframerate()
    a=np.frombuffer(w.readframes(n),dtype=np.int16).astype(np.float64)/32768.
    return a,sr
v1,sr=rd('v1_full.wav')
print('v1',len(v1)/sr,sr)
# RMS envelope over whole v1 to locate the step
hop=int(sr*0.05)
rms=np.array([np.sqrt((v1[i:i+hop]**2).mean()+1e-20) for i in range(0,len(v1)-hop,hop)])
t=np.arange(len(rms))*0.05
db=20*np.log10(rms+1e-12)
for lo,hi in [(0,85),(85,97),(97,100)]:
    m=(t>=lo)&(t<hi)
    print(f'{lo}-{hi}s  meanRMS {rms[m].mean():.5f}  dB {20*np.log10(rms[m].mean()+1e-12):.1f}  peak {np.abs(v1[int(lo*sr):int(hi*sr)]).max():.3f}')
plt.figure(figsize=(14,3)); plt.plot(t,db,lw=.6); plt.axvspan(85,97,color='orange',alpha=.25)
plt.xlabel('video time (s)'); plt.ylabel('dBFS RMS (50ms)'); plt.title('OpSTlDJWFFI RMS envelope; orange = colour (col/s) segment')
plt.tight_layout(); plt.savefig('aud_v1_envelope.png',dpi=110); plt.close()

# find exact boundaries of the step
d=np.diff(db)
i=np.argmax(db[1600:1960])+1600
print('loudest 50ms bin at t=',t[i])
# rising/falling edge
thr=(db[(t>60)&(t<80)].mean()+db[(t>87)&(t<95)].mean())/2
print('thr',thr)
above=db>thr
idx=np.where(above[1500:2000])[0]+1500
print('first above',t[idx[0]],'last above',t[idx[-1]])
