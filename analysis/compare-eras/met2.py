import sys,numpy as np
from PIL import Image
def blur(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
pre,label,pick=sys.argv[1],sys.argv[2],int(sys.argv[3])
B=np.load(pre+'_band.npy'); idx=np.load(pre+'_idx.npy'); runs=np.load(pre+'_runs.npy')
lens=runs[:,1]-runs[:,0]; order=np.argsort(-lens)
a,b=runs[order[pick]]
m=B[a:b].astype(np.float32).mean(0)
h=m-blur(m,20)
h=h[4:-4,4:-4]                      # drop border ringing
print('%s  run f%d-f%d  n=%d  band shape %s'%(label,idx[a],idx[b-1],b-a,h.shape))
pos=np.clip(h,0,None)
# text bbox by 50% of max on smoothed positive
sm=blur(pos,1)
thr=sm.max()*0.5
ys,xs=np.nonzero(sm>thr)
print('   glyph-core bbox  y %d-%d (h=%d)   x %d-%d (w=%d)  [rel to crop]'%(ys.min(),ys.max(),ys.max()-ys.min()+1,xs.min(),xs.max(),xs.max()-xs.min()+1))
cp=pos.mean(0); rp=pos.mean(1)
# cap height: rows where col-mean profile exceeds 30% of peak
r=np.nonzero(rp>rp.max()*0.30)[0]
print('   row profile >30%%: rows %d-%d  => digit height ~%d px'%(r.min(),r.max(),r.max()-r.min()+1))
# pitch: autocorr of column profile restricted to text span
c=np.nonzero(cp>cp.max()*0.25)[0]
seg=cp[c.min():c.max()+1]; seg=seg-seg.mean()
ac=np.correlate(seg,seg,'full')[len(seg)-1:]; ac=ac/ac[0]
cands=[(l,ac[l]) for l in range(15,90) if 0<l<len(ac)-1 and ac[l]>=ac[l-1] and ac[l]>=ac[l+1]]
cands.sort(key=lambda t:-t[1])
print('   text span x %d-%d (w=%d); autocorr peaks:'%(c.min(),c.max(),c.max()-c.min()+1), [(l,round(float(v),3)) for l,v in cands[:6]])
np.save(pre+'_clean.npy',h)
lo,hi=np.percentile(h,0.5),np.percentile(h,99.7)
Image.fromarray((np.clip((h-lo)/(hi-lo),0,1)*255).astype(np.uint8)).resize((h.shape[1]*6,h.shape[0]*6),Image.LANCZOS).save(pre+'_clean.png')
