import numpy as np
from PIL import Image
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
segs={'leader':(925,1040),'s11':(1049,1247),'taxi':(1250,1298),'pace':(1304,2498),'s26':(2502,2568),'color':(2572,2917)}
for k,(a,b) in segs.items():
    st=max(1,(b-a)//120)
    M=None
    for f in range(a,b+1,st):
        x=np.asarray(Image.open(F.format(f)).convert('L')).astype(np.float32)
        M=x if M is None else np.maximum(M,x)
    ref=np.percentile(M,97); thr=0.5*ref
    L=[];R=[];T=[];B=[]
    for y in range(300,800,4):
        r=M[y]; idx=np.where(r>thr)[0]
        if len(idx)>50: L.append(idx[0]); R.append(idx[-1])
    for x in range(700,1200,4):
        c=M[:,x]; idx=np.where(c>thr)[0]
        if len(idx)>50: T.append(idx[0]); B.append(idx[-1])
    print('%-7s thr %5.1f  L %6.1f  R %6.1f  T %6.1f  B %6.1f   W %6.1f  H %6.1f'%(k,thr,np.median(L),np.median(R),np.median(T),np.median(B),np.median(R)-np.median(L),np.median(B)-np.median(T)))
    Image.fromarray(np.clip(M,0,255).astype(np.uint8)).save('max_%s.png'%k)
