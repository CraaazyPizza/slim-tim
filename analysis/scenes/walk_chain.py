from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates
FD='/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f%05d.png'
def L(f): return gaussian_filter(np.asarray(Image.open(FD%f).convert('L'),dtype=np.float64),1.0)
P=40
def sub_ncc(I0,I1,cx,cy,srch=14):
    y0,x0=int(round(cy)),int(round(cx))
    if y0-P<2 or x0-P<2 or y0+P>1078 or x0+P>1918: return None
    T=I0[y0-P:y0+P,x0-P:x0+P]
    if T.std()<1.5: return None
    T0=T-T.mean(); n0=np.sqrt((T0*T0).sum())
    C=np.full((2*srch+1,2*srch+1),-2.0)
    for i,dy in enumerate(range(-srch,srch+1)):
        for j,dx in enumerate(range(-srch,srch+1)):
            y,x=y0+dy,x0+dx
            if y-P<0 or x-P<0 or y+P>1080 or x+P>1920: continue
            W=I1[y-P:y+P,x-P:x+P]; W=W-W.mean(); d=np.sqrt((W*W).sum())
            if d<1e-9: continue
            C[i,j]=(T0*W).sum()/(n0*d)
    k=np.unravel_index(np.argmax(C),C.shape)
    if k[0] in (0,2*srch) or k[1] in (0,2*srch): return None
    # parabolic subpixel
    def sp(a,b,c):
        den=(a-2*b+c); return 0.0 if abs(den)<1e-9 else 0.5*(a-c)/den
    ddy=sp(C[k[0]-1,k[1]],C[k[0],k[1]],C[k[0]+1,k[1]])
    ddx=sp(C[k[0],k[1]-1],C[k[0],k[1]],C[k[0],k[1]+1])
    return (cx+(k[1]-srch)+ddx, cy+(k[0]-srch)+ddy, C[k])

f0,f1,STEP=1625,1832,3
# seed grid on f1625, skip the figure column roughly x 560-900 y>400
seeds=[]
for cy in range(90,1010,55):
    for cx in range(370,1580,55):
        seeds.append((cx,cy))
frames=list(range(f0,f1+1,STEP))
I=L(frames[0])
tracks={i:[(seeds[i][0],seeds[i][1])] for i in range(len(seeds))}
alive=set(tracks)
for fi in frames[1:]:
    J=L(fi)
    for i in list(alive):
        cx,cy=tracks[i][-1]
        r=sub_ncc(I,J,cx,cy)
        if r is None or r[2]<0.80: alive.discard(i); continue
        tracks[i].append((r[0],r[1]))
    I=J
print('seeds',len(seeds),'survived full length',len(alive))
out={i:np.array(tracks[i]) for i in alive}
np.save('walk_tracks.npy',np.array([np.c_[np.full(len(frames),i),out[i]] for i in sorted(alive)],dtype=object),allow_pickle=True)
import pickle
pickle.dump({'frames':frames,'tracks':{i:np.array(tracks[i]) for i in alive}},open('walk_tracks.pkl','wb'))
