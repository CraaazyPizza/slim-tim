import sys,os,numpy as np
from PIL import Image
fd='frames/OpSTlDJWFFI'
files=sorted([f for f in os.listdir(fd) if f.endswith('.png')])
def L(i): return np.asarray(Image.open(os.path.join(fd,files[i-1])).convert('L'),dtype=np.float32)
def gb(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
y0,y1,x0,x1=920,1010,380,1600
for tag,rng in [('A',(956,1010)),('B',(959,1000)),('C',(989,1010)),('D',(956,970))]:
    acc=None;n=0
    for i in range(rng[0],rng[1]+1):
        a=L(i)[y0:y1,x0:x1]; acc=a if acc is None else acc+a; n+=1
    M=acc/n
    hp=M-gb(M,25)
    cp=np.abs(hp).mean(0)
    nz=[i+x0 for i,v in enumerate(cp) if v>np.median(cp)*1.4]
    print('%s frames %d-%d (n=%d): hp sd=%.3f  ink columns x%d..%d'%(tag,rng[0],rng[1],n,hp.std(),min(nz) if nz else -1,max(nz) if nz else -1))
    rp=np.abs(hp).mean(1)
    rr=[i+y0 for i,v in enumerate(rp) if v>np.median(rp)*1.25]
    print('    ink rows y%d..%d'%(min(rr) if rr else -1,max(rr) if rr else -1))
    for pct in [(4,96),(12,88),(20,80)]:
        lo,hi=np.percentile(hp,pct[0]),np.percentile(hp,pct[1])
        v=np.clip((hp-lo)/(hi-lo+1e-9),0,1)
        Image.fromarray(((1-v)*255).astype(np.uint8)).resize(((x1-x0)*2,(y1-y0)*2),Image.LANCZOS).save('analysis/compare-eras/cyr/BEST_%s_%d.png'%(tag,pct[0]))
    np.save('analysis/compare-eras/cyr/BEST_%s.npy'%tag,hp)
print('saved BEST_*')
