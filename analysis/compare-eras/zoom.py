import sys,numpy as np
from PIL import Image
hp=np.load(sys.argv[1]); y0,y1,x0,x1=map(int,sys.argv[2:6]); out=sys.argv[6]
sc=int(sys.argv[7]) if len(sys.argv)>7 else 2
g=hp[y0:y1,x0:x1]
# remove residual row/column bias
g=g-np.median(g,axis=1,keepdims=True)
for pct,tag in [((5,95),'a'),((15,85),'b'),((25,75),'c')]:
    lo,hi=np.percentile(g,pct[0]),np.percentile(g,pct[1])
    v=np.clip((g-lo)/(hi-lo+1e-9),0,1)
    Image.fromarray(((1-v)*255).astype(np.uint8)).resize(((x1-x0)*sc,(y1-y0)*sc),Image.LANCZOS).save('%s_%s.png'%(out,tag))
print('saved',out,'shapes',g.shape)
