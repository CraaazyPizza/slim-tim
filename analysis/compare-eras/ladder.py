import pickle,numpy as np,sys
from PIL import Image
R=pickle.load(open('analysis/compare-eras/runs.pkl','rb'))
def blur1(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
k,f0,f1,step=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
B=np.load('analysis/compare-eras/%s_band.npy'%k); idx=np.load('analysis/compare-eras/%s_idx.npy'%k)
c5=float(np.median([o[2] for o in R[k]])); p=float(np.median([o[3] for o in R[k]]))
# show cells 6..11  (":SS:SS")
x0=max(0,int(round(c5-0.6*p))+4); x1=min(B.shape[2],int(round(c5+5.7*p))+4)
i0=int(np.searchsorted(idx,f0)); i1=int(np.searchsorted(idx,f1))
tiles=[];labels=[]
for s in range(i0,i1-step+1,step):
    m=B[s:s+step].astype(np.float32).mean(0)
    h=m-blur1(m,20)
    h=np.clip(h,0,None); 
    if h.max()>0: h=h/h.max()
    tiles.append(h[:,x0:x1]); labels.append(idx[s])
H,W=tiles[0].shape
can=np.zeros(((H+2)*len(tiles),W))
for i,t in enumerate(tiles): can[i*(H+2):i*(H+2)+H]=t
sc=3
Image.fromarray((np.clip(can,0,1)*255).astype(np.uint8)).resize((W*sc,can.shape[0]*sc),Image.LANCZOS).save('analysis/compare-eras/LADDER_%s.png'%k)
print('rows (top->bottom) start at frames:',labels)
print('saved LADDER_%s.png  step=%d frames  region x=%d..%d'%(k,step,x0,x1))
