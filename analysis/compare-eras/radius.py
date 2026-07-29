import sys,os,numpy as np
from PIL import Image
def fit(fd,label,f0,f1,step):
    files=sorted([f for f in os.listdir(fd) if f.endswith('.png')])
    MX=None
    for i in range(f0,f1+1,step):
        a=np.asarray(Image.open(os.path.join(fd,files[i-1])).convert('L'),dtype=np.float32)
        MX=a if MX is None else np.maximum(MX,a)
    H,W=MX.shape
    # matte level from the frame corners
    corner=np.concatenate([MX[:40,:40].ravel(),MX[:40,-40:].ravel(),MX[-40:,:40].ravel(),MX[-40:,-40:].ravel()])
    lo=np.median(corner); hi=np.percentile(MX,97)
    m=MX>(lo+hi)/2
    ys=np.nonzero(m.mean(1)>0.5)[0]; xs=np.nonzero(m.mean(0)>0.5)[0]
    T,Bo,L,Rt=ys.min(),ys.max(),xs.min(),xs.max()
    # for each of 4 corners, fit a circle to the boundary in the corner region
    rads=[]
    for name,fy,fx in [('TL',1,1),('TR',1,-1),('BL',-1,1),('BR',-1,-1)]:
        pts=[]
        for k in range(0,120):
            y = T+k if fy>0 else Bo-k
            if y<0 or y>=H: break
            row=m[y]
            if fx>0:
                idx=np.nonzero(row[L:L+200])[0]
                if len(idx)==0: continue
                x=L+idx.min()
            else:
                idx=np.nonzero(row[Rt-200:Rt+1])[0]
                if len(idx)==0: continue
                x=Rt-200+idx.max()
            pts.append((y,x))
        # radius: the corner arc satisfies (x-(L+r))^2+(y-(T+r))^2=r^2 on the inside
        # estimate r as the offset where the boundary becomes straight (inset -> 0)
        ins=[abs(x-(L if fx>0 else Rt)) for y,x in pts]
        r=None
        for j,v in enumerate(ins):
            if v<=1.0: r=j; break
        # least-squares circle fit on the arc portion
        arc=[(y,x) for (y,x),v in zip(pts,ins) if v>1.0]
        rr=None
        if len(arc)>=6:
            A=[];b=[]
            for y,x in arc:
                A.append([2*x,2*y,1]); b.append(x*x+y*y)
            A=np.array(A,float); b=np.array(b,float)
            sol,*_=np.linalg.lstsq(A,b,rcond=None)
            cx,cy,c=sol
            rr=np.sqrt(max(0,c+cx*cx+cy*cy))
        rads.append((name,r,None if rr is None else round(float(rr),1),len(arc)))
    print('%-12s picture x%d..%d (w=%d) y%d..%d (h=%d) aspect=%.4f  matte=%.1f%% of frame'%(
        label,L,Rt,Rt-L+1,T,Bo,Bo-T+1,(Rt-L+1)/(Bo-T+1),100*(1-((Rt-L+1)*(Bo-T+1))/(W*H))))
    print('              corner radii (straight-onset px, circle-fit px, npts): %s'%rads)
fit('frames/ZB788PtqQvg','ZB788_2011',140,1180,6)
fit('frames/RsQCXN4o4Ps','RsQCX_2011',600,1500,6)
fit('frames/Oqw96jCOP7A','Oqw96_2026',650,2500,10)
fit('frames/l9RAhmPHM_A','l9RAh_2026',430,4390,20)
fit('frames/OpSTlDJWFFI','OpSTl_2026',900,2990,12)
