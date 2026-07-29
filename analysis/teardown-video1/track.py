import numpy as np, sys
from PIL import Image, ImageFilter
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
def enh(f):
    im=Image.open(F.format(f)).convert('L')
    a=np.asarray(im).astype(np.float32)
    bg=np.asarray(im.filter(ImageFilter.GaussianBlur(9))).astype(np.float32)
    return a-bg
def track(frames,box,ref,R=12):
    T=enh(ref)[box[1]:box[3],box[0]:box[2]]
    T=T-T.mean(); Tn=np.sqrt((T*T).sum())
    out=[]
    for f in frames:
        E=enh(f); best=(-2,0,0); grid=np.zeros((2*R+1,2*R+1))
        for i,dy in enumerate(range(-R,R+1)):
            for j,dx in enumerate(range(-R,R+1)):
                P=E[box[1]+dy:box[3]+dy, box[0]+dx:box[2]+dx]
                P=P-P.mean(); v=float((T*P).sum()/(Tn*np.sqrt((P*P).sum())+1e-9))
                grid[i,j]=v
                if v>best[0]: best=(v,dy,dx)
        v,dy,dx=best; i=dy+R; j=dx+R
        def sub(a,b,c):
            d=a-2*b+c
            return 0.0 if abs(d)<1e-9 else 0.5*(a-c)/d
        sy=sub(grid[i-1,j],grid[i,j],grid[i+1,j]) if 0<i<2*R else 0
        sx=sub(grid[i,j-1],grid[i,j],grid[i,j+1]) if 0<j<2*R else 0
        out.append((f,dx+sx,dy+sy,v))
    return out
if __name__=='__main__':
    fr=eval(sys.argv[1]); box=eval(sys.argv[2]); ref=int(sys.argv[3])
    r=track(fr,box,ref)
    for f,dx,dy,v in r: print(f,'%.2f %.2f %.3f'%(dx,dy,v))
    a=np.array([(f,dx,dy) for f,dx,dy,v in r])
    np.save(sys.argv[4],a)
    print('dx std %.2f range %.2f ; dy std %.2f range %.2f'%(a[:,1].std(),a[:,1].ptp(),a[:,2].std(),a[:,2].ptp()))
