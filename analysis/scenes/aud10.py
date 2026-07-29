import numpy as np, wave
from scipy import signal
from scipy.ndimage import median_filter
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def rd(p):
    w=wave.open(p); n=w.getnframes(); sr=w.getframerate()
    return np.frombuffer(w.readframes(n),dtype=np.int16).astype(np.float64)/32768., sr
v1,sr=rd('v1_full.wav')
# fine boundary
hop=int(sr*0.01)
r=np.array([np.sqrt((v1[i:i+hop]**2).mean()+1e-20) for i in range(int(84*sr),int(100*sr),hop)])
t=84+np.arange(len(r))*0.01
db=20*np.log10(r+1e-12)
lo=db[(t>84)&(t<85)].mean(); hi=db[(t>87)&(t<95)].mean()
thr=(lo+hi)/2
i=np.argmax(db>thr); print('rise crosses midpoint at t=%.3f s (video frame %.1f)'%(t[i],t[i]*30000/1001))
j=np.where((t>96)&(t<98.5)&(db<thr))[0]
print('falls below midpoint at t=%.3f s (frame %.1f)'%(t[j[0]],t[j[0]]*30000/1001))
print('level before %.1f dBFS, during %.1f dBFS, step %.1f dB'%(lo,hi,hi-lo))
# rise time
k=np.where((t>85)&(t<86.5))[0]
d=db[k]; print('rise 10-90%% takes %.3f s'%( (t[k][np.argmax(d>lo+0.9*(hi-lo))]-t[k][np.argmax(d>lo+0.1*(hi-lo))])))
plt.figure(figsize=(14,4)); plt.plot(t,db,lw=.6); plt.axvline(t[i],color='g',ls='--'); plt.axvline(t[j[0]],color='r',ls='--')
plt.axvspan(85.8,97.36,color='orange',alpha=.15,label='colour picture (f2571-2918)')
plt.legend(); plt.xlabel('video s'); plt.ylabel('dBFS (10ms RMS)'); plt.title('v1 audio around the colour segment: gate edges vs picture edges')
plt.tight_layout(); plt.savefig('aud_colseg_edges.png',dpi=120); plt.close()

# 23.98 line stability over time
seg=v1[int(85.6*sr):int(97.0*sr)]
N=int(3*sr); print()
for tgt,w in [(143.88,1.0),(99.91,1.0)]:
    out=[]
    for s in range(0,len(seg)-N,int(1*sr)):
        x=seg[s:s+N]*np.hanning(N)
        F=np.abs(np.fft.rfft(x,1<<21)); f=np.fft.rfftfreq(1<<21,1/sr)
        m=(f>tgt-w)&(f<tgt+w); out.append(f[m][np.argmax(F[m])])
    out=np.array(out); print('line near %.2f Hz: mean %.4f sd %.4f Hz (n=%d)'%(tgt,out.mean(),out.std(),len(out)))
