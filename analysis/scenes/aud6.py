import numpy as np, wave
from scipy import signal
from scipy.ndimage import median_filter
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def rd(p):
    w=wave.open(p); n=w.getnframes(); sr=w.getframerate()
    return np.frombuffer(w.readframes(n),dtype=np.int16).astype(np.float64)/32768., sr
v1,sr=rd('v1_full.wav')
seg=v1[int(85.6*sr):int(97.0*sr)]
bed=v1[int(55*sr):int(80*sr)]
# track 100Hz line in 2s windows
print('100 Hz line tracking in col/s (2 s windows, 0.5 s hop):')
res=[]
N=int(2*sr)
for i in range(0,len(seg)-N,int(0.5*sr)):
    w=seg[i:i+N]*np.hanning(N)
    F=np.abs(np.fft.rfft(w,1<<20)); f=np.fft.rfftfreq(1<<20,1/sr)
    m=(f>97)&(f<103); loc=(f>90)&(f<110)
    pk=f[m][np.argmax(F[m])]
    prom=20*np.log10(F[m].max()/np.median(F[loc]))
    res.append((85.6+i/sr,pk,prom)); print('  t=%.1f  peak=%.3f Hz  prom=%.1f dB'%(85.6+i/sr,pk,prom))
res=np.array(res)
print('100Hz line: mean %.4f Hz, sd %.4f Hz'%(res[:,1].mean(),res[:,1].std()))

# control: same tracking on the bed
print('\nsame tracking on bed:')
r2=[]
for i in range(0,len(bed)-N,int(2.0*sr)):
    w=bed[i:i+N]*np.hanning(N)
    F=np.abs(np.fft.rfft(w,1<<20)); f=np.fft.rfftfreq(1<<20,1/sr)
    m=(f>97)&(f<103); loc=(f>90)&(f<110)
    r2.append((f[m][np.argmax(F[m])],20*np.log10(F[m].max()/np.median(F[loc]))))
r2=np.array(r2); print('  bed 100Hz: mean %.3f sd %.3f, mean prom %.1f dB'%(r2[:,0].mean(),r2[:,0].std(),r2[:,1].mean()))

plt.figure(figsize=(12,4))
plt.subplot(1,2,1); plt.plot(res[:,0],res[:,1],'o-'); plt.axhline(100,color='r',ls=':'); plt.ylim(99,101); plt.xlabel('video s'); plt.ylabel('Hz'); plt.title('col/s: 100 Hz line frequency (stable => mains)')
plt.subplot(1,2,2); plt.plot(res[:,0],res[:,2],'o-'); plt.xlabel('video s'); plt.ylabel('dB prominence'); plt.title('100 Hz line strength')
plt.tight_layout(); plt.savefig('aud_100hz_track.png',dpi=110); plt.close()

# Speed-corrected (x1.5) rendering
import subprocess
subprocess.run(['ffmpeg','-y','-v','error','-i','col_85_97.wav','-filter:a','atempo=1.5','col_85_97_x1.5.wav'],check=True)
subprocess.run(['ffmpeg','-y','-v','error','-i','col_85_97.wav','-filter:a','asetrate=72000,aresample=48000','col_85_97_pitch1.5.wav'],check=True)
c15,_=rd('col_85_97_pitch1.5.wav')
f,P=signal.welch(c15,sr,nperseg=1<<18,noverlap=(1<<18)//2)
E=10*np.log10(P+1e-16)-median_filter(10*np.log10(P+1e-16),201)
for target in [50,60,75,100,120,150,180]:
    m=(f>target-2)&(f<target+2)
    print('pitch-x1.5 near %d Hz -> %.3f Hz  %.1f dB'%(target,f[m][np.argmax(E[m])],E[m].max()))
