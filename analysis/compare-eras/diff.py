import sys,os,numpy as np
from PIL import Image
fd='frames/OpSTlDJWFFI'
files=sorted([f for f in os.listdir(fd) if f.endswith('.png')])
def L(i): return np.asarray(Image.open(os.path.join(fd,files[i-1])).convert('L'),dtype=np.float32)
def avg(rs):
    acc=None;n=0
    for a,b in rs:
        for i in range(a,b+1):
            x=L(i); acc=x if acc is None else acc+x; n+=1
    return acc/n,n
T,nt=avg([(959,1000)])
N,nn=avg([(917,958),(1001,1042)])
D=T-N
print('text-avg over %d frames, no-text-avg over %d frames'%(nt,nn))
print('diff stats: mean=%.3f sd=%.3f min=%.2f max=%.2f'%(D.mean(),D.std(),D.min(),D.max()))
np.save('analysis/compare-eras/cyr/D.npy',D)
# row energy of the diff to find the text band
e=np.abs(D-np.median(D)).mean(1)
top=np.argsort(-e)[:24]
print('rows with largest |diff| energy:',sorted(top.tolist()))
for y in range(880,1060,4):
    print('   y=%4d |d|=%.4f %s'%(y,e[y],'#'*int(e[y]*40)))
