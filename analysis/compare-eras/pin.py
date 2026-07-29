import sys,os,numpy as np
from PIL import Image
fd=sys.argv[1]; f0=int(sys.argv[2]); f1=int(sys.argv[3])
y0,y1,x0,x1=map(int,sys.argv[4:8])
files=sorted([f for f in os.listdir(fd) if f.endswith('.png')])
def gb(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
B=[];idx=[]
for i in range(f0,f1+1):
    B.append(np.asarray(Image.open(os.path.join(fd,files[i-1])).convert('L'),dtype=np.float32)[y0:y1,x0:x1]); idx.append(i)
B=np.stack(B)
# reference text template from f959-1001
i0,i1=idx.index(959),idx.index(1001)
ref=B[i0:i1+1].mean(0); ref=ref-gb(ref,20); ref=ref-ref.mean(); ref/=np.linalg.norm(ref)
print('per-frame correlation with the f959-1001 text template:')
cs=[]
for j in range(len(B)):
    h=B[j]-gb(B[j],20); h=h-h.mean(); n=np.linalg.norm(h)
    c=float((h/n*ref).sum()) if n>0 else 0
    cs.append(c)
cs=np.array(cs)
# smooth
sm=np.convolve(cs,np.ones(5)/5,mode='same')
base=np.median(sm)
for j in range(0,len(B)):
    if sm[j]>base+ (sm.max()-base)*0.25:
        pass
on=[idx[j] for j in range(len(B)) if sm[j]>base+(sm.max()-base)*0.3]
print('   baseline=%.4f peak=%.4f'%(base,sm.max()))
print('   frames above 30%% of peak: %d..%d  (n=%d)'%(min(on),max(on),len(on)))
for j in range(0,len(B),3):
    bar='#'*int(max(0,(sm[j]-base)/(sm.max()-base+1e-9))*50)
    print('   f%-5d %+.4f %s'%(idx[j],sm[j],bar))
