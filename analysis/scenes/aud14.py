import numpy as np, wave
from scipy import signal
from scipy.ndimage import median_filter
def rd(p):
    w=wave.open(p); n=w.getnframes(); sr=w.getframerate()
    return np.frombuffer(w.readframes(n),dtype=np.int16).astype(np.float64)/32768., sr
v1,sr=rd('v1_full.wav')
x=v1[int(86.0*sr):int(97.0*sr)]
n=len(x); w=x*np.hanning(n); NF=1<<22
F=np.abs(np.fft.rfft(w,NF)); f=np.fft.rfftfreq(NF,1/sr)
P=20*np.log10(F+1e-12); E=P-median_filter(P,int(6/(f[1]-f[0])))
def exc(fr,w=0.05):
    m=(f>fr-w)&(f<fr+w); return float(E[m].max())
print('Hypothesis A: single comb at 3.9963 Hz -> excess at each multiple 18..60')
b=3.99628
vals=[]
for k in range(18,61):
    v=exc(b*k); vals.append((k,round(b*k,3),round(v,1)))
print(vals)
hit=[v for k,fr,v in vals if v>13.6]
print('multiples above 13.6 dB carpet: %d of %d'%(len(hit),len(vals)))
print()
print('Hypothesis B: comb at 11.988 Hz -> multiples 4..30')
b2=11.98815
v2=[(k,round(b2*k,3),round(exc(b2*k),1)) for k in range(4,31)]
print(v2)
print('above carpet: %d of %d'%(sum(1 for k,fr,v in v2 if v>13.6),len(v2)))
print()
print('Hypothesis C: 49.9535 Hz mains series')
print([(k,round(49.9535*k,3),round(exc(49.9535*k),1)) for k in range(1,13)])
print()
# null: how many random frequencies exceed 13.6?
rng=np.random.default_rng(1)
cnt=0;N=4000
for _ in range(N):
    fr=rng.uniform(60,1500)
    if exc(fr)>13.6: cnt+=1
print('null rate of >13.6 dB at random frequencies: %.2f%%'%(100*cnt/N))
