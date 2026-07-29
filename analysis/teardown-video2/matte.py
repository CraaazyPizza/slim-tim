import numpy as np
from PIL import Image
from scipy import ndimage as nd
D='frames/Oqw96jCOP7A'
def matte(i):
    a=np.asarray(Image.open(f'{D}/f{i:05d}.png').convert('L')).astype(int)
    sv=int(round(np.median(a[0:30,1700:1900])))
    flat=np.abs(a-sv)<=1
    # flood from frame border through flat pixels
    lbl,n=nd.label(flat)
    border=set(lbl[0,:]).union(lbl[-1,:]).union(lbl[:,0]).union(lbl[:,-1]); border.discard(0)
    out=np.isin(lbl,list(border))
    img=~out
    if img.sum()<1000: return None
    ys,xs=np.where(img)
    return sv, xs.min(), xs.max(), ys.min(), ys.max(), img.sum(), img
res={}
frames=list(range(457,2425))
print('frame sv  L    R    T    B   width height area')
rows=[]
for i in frames:
    m=matte(i)
    if m is None: rows.append((i,None)); continue
    sv,L,R,T,B,ar,_=m
    rows.append((i,(sv,L,R,T,B,ar)))
np.save('analysis/teardown-video2/matte_rows.npy',np.array([[r[0]]+ (list(r[1]) if r[1] else [0]*6) for r in rows]))
print('saved',len(rows))
