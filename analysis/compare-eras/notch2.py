import sys,os,numpy as np
from PIL import Image
def gb(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
def notch_x(g,periods=(32,16,32/3,8,32/5,16/3,32/7,4)):
    H,W=g.shape; F=np.fft.rfft(g,axis=1); fr=np.fft.rfftfreq(W)
    for p in periods:
        m=np.abs(fr-1.0/p)<(1.6/W)
        F[:,m]=0
    return np.fft.irfft(F,n=W,axis=1)
fd,label=sys.argv[1],sys.argv[2]; f0,f1=int(sys.argv[3]),int(sys.argv[4])
Y0,Y1,x0,x1=map(int,sys.argv[5:9]); cy0,cy1=int(sys.argv[9]),int(sys.argv[10]); out=sys.argv[11]
files=sorted([f for f in os.listdir(fd) if f.endswith('.png')])
acc=None;n=0
for i in range(f0,f1+1):
    a=np.asarray(Image.open(os.path.join(fd,files[i-1])).convert('L'),dtype=np.float32)[Y0:Y1,x0:x1]
    acc=a if acc is None else acc+a; n+=1
M=acc/n
hp=M-gb(M,22); hp=hp-hp.mean(axis=0,keepdims=True); hp=notch_x(hp); hp=gb(hp,1)
g=hp[cy0-Y0:cy1-Y0]
print('%s n=%d display y%d-%d sd=%.4f'%(label,n,cy0,cy1,g.std()))
for pct,tag in [((2,98),'a'),((6,94),'b'),((14,86),'c')]:
    lo,hi=np.percentile(g,pct[0]),np.percentile(g,pct[1])
    v=np.clip((g-lo)/(hi-lo+1e-9),0,1)
    Image.fromarray(((1-v)*255).astype(np.uint8)).resize(((x1-x0)*2,(cy1-cy0)*5),Image.LANCZOS).save('%s_%s_inv.png'%(out,tag))
    Image.fromarray((v*255).astype(np.uint8)).resize(((x1-x0)*2,(cy1-cy0)*5),Image.LANCZOS).save('%s_%s_pos.png'%(out,tag))
