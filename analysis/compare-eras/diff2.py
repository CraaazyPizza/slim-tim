import os,numpy as np
from PIL import Image
fd='frames/OpSTlDJWFFI'
files=sorted([f for f in os.listdir(fd) if f.endswith('.png')])
def L(i): return np.asarray(Image.open(os.path.join(fd,files[i-1])).convert('L'),dtype=np.float32)
def gb(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
y0,y1,x0,x1=915,1015,380,1600
def avg(rs):
    acc=None;n=0
    for a,b in rs:
        for i in range(a,b+1):
            x=L(i)[y0:y1,x0:x1]; acc=x if acc is None else acc+x; n+=1
    return acc/n
T=avg([(959,1000)])
N=avg([(920,950),(1012,1042)])
# normalise each for overall brightness before differencing
Tn=T-gb(T,40); Nn=N-gb(N,40)
D=Tn-Nn
print('D sd=%.4f'%D.std())
for pct,tag in [((2,98),'p2'),((8,92),'p8'),((20,80),'p20')]:
    lo,hi=np.percentile(D,pct[0]),np.percentile(D,pct[1])
    v=np.clip((D-lo)/(hi-lo+1e-9),0,1)
    for pol,pn in [(v,'pos'),(1-v,'inv')]:
        Image.fromarray((pol*255).astype(np.uint8)).resize(((x1-x0)*2,(y1-y0)*2),Image.LANCZOS).save('analysis/compare-eras/cyr/DF_%s_%s.png'%(tag,pn))
np.save('analysis/compare-eras/cyr/DF.npy',D)
rp=np.abs(D).mean(1)
print('row energy:')
for i in range(0,len(rp),3): print('   y=%4d %.4f %s'%(y0+i,rp[i],'#'*int(rp[i]*60)))
