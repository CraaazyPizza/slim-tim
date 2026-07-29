import pickle,numpy as np
from PIL import Image
R=pickle.load(open('analysis/compare-eras/runs.pkl','rb'))
for k in ['zb','rs','oq','l9']:
    outs=R[k][:4]
    tiles=[]
    for P,groups,c5,p,i0,i1,n in outs:
        v=np.clip(P,0,1); tiles.append(v); print(k,'f%d-%d n=%d pitch=%.3f'%(i0,i1,n,p))
    H=max(t.shape[0] for t in tiles); W=max(t.shape[1] for t in tiles)
    can=np.zeros(((H+4)*len(tiles),W))
    for i,t in enumerate(tiles): can[i*(H+4):i*(H+4)+t.shape[0],:t.shape[1]]=t
    Image.fromarray((can*255).astype(np.uint8)).resize((W*3,can.shape[0]*3),Image.LANCZOS).save('analysis/compare-eras/D_%s.png'%k)
    print('  saved D_%s.png'%k)
