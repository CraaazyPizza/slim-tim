import numpy as np, json, sys, os
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/hand-proportions/work')
from scipy import ndimage as ndi
from PIL import Image

# ---------------- generic helpers -------------------------------------------
def bilin(img,x,y):
    return ndi.map_coordinates(img,[np.asarray(y,float),np.asarray(x,float)],order=1,mode='nearest')

def row_track(img, y0, y1, x_start, sign, halfwin, follow, smooth=1.5):
    ys=[];xs=[];vs=[];vf=[]
    x=float(x_start)
    for y in range(int(y0),int(y1)+1):
        row=ndi.gaussian_filter1d(img[y].astype(float),smooth); w=row*sign
        lo=int(max(0,x-follow)); hi=int(min(len(row)-1,x+follow))
        j=lo+int(np.argmax(w[lo:hi+1]))
        L=max(0,j-halfwin); R=min(len(row)-1,j+halfwin)
        if j-L<5 or R-j<5: break
        jl=L+int(np.argmin(w[L:j])); jr=j+int(np.argmin(w[j:R+1]))
        ys.append(y);xs.append(j);vs.append(w[j]);vf.append(0.5*(w[jl]+w[jr]))
        x=0.55*x+0.45*j
    return np.array(ys),np.array(xs,float),np.array(vs,float),np.array(vf,float)

def cleft_level(y,vs,vf,frac,hold,sm):
    V=ndi.uniform_filter1d(vs,sm); F=ndi.uniform_filter1d(vf,3*sm)
    npl=max(6,int(len(V)*0.40)); g0=float(np.median(V[:npl]))
    thr=F+frac*(g0-F)
    idx=None
    for i in range(npl//2,len(V)-1):
        if V[i]<thr[i] and (V[i:i+hold]<thr[i:i+hold]).all(): idx=i;break
    if idx is None: idx=len(V)-1
    a=V[idx-1]-thr[idx-1]; b=V[idx]-thr[idx]
    f=a/(a-b) if a!=b else 0.0
    yy=y[idx-1]+f*(y[idx]-y[idx-1])
    return yy,idx,g0,V,thr

def transverse_width(img, c, n, sign, hw, frac=0.5, smooth=1.5):
    """width of the digit (material) at half contrast, along transverse direction n."""
    ts=np.arange(-hw,hw+1e-9,0.5)
    v=ndi.gaussian_filter1d(bilin(img,c[0]+ts*n[0],c[1]+ts*n[1]),smooth)*sign
    j=int(np.argmin(np.abs(ts)))
    # material is the LOW side for sign=+1 image where feature bright? here: material = extremum opposite
    # we pass sign so that material is a MINIMUM of v
    core=v[max(0,j-6):j+7].min()
    L=v[:j].max() if j>2 else v[0]; R=v[j:].max() if j<len(v)-3 else v[-1]
    half_l=0.5*(core+L); half_r=0.5*(core+R)
    i=j
    while i>0 and v[i]<half_l: i-=1
    li=ts[i]
    i=j
    while i<len(v)-1 and v[i]<half_r: i+=1
    ri=ts[i]
    return float(ri-li)

def groove_dir(img, p, sigma=3.0, win=25):
    """local ridge direction from the structure tensor (eigvec of the SMALL eigenvalue)."""
    y0=int(p[1]-win); y1=int(p[1]+win); x0=int(p[0]-win); x1=int(p[0]+win)
    s=ndi.gaussian_filter(img[y0:y1,x0:x1].astype(float),sigma)
    gy,gx=np.gradient(s)
    Jxx=(gx*gx).mean(); Jyy=(gy*gy).mean(); Jxy=(gx*gy).mean()
    J=np.array([[Jxx,Jxy],[Jxy,Jyy]])
    w,v=np.linalg.eigh(J)
    return v[:,0]      # smallest eigenvalue -> along the ridge

def march_track(img, p0, d, sign, halfwin, follow, step=1.0, nsteps=400, smooth=1.5):
    d=np.array(d,float); d/=np.linalg.norm(d); n=np.array([-d[1],d[0]])
    ts=np.arange(-halfwin,halfwin+1e-9,0.5)
    S=[];P=[];vs=[];vf=[]
    p=np.array(p0,float)
    for k in range(nsteps):
        v=ndi.gaussian_filter1d(bilin(img,p[0]+ts*n[0],p[1]+ts*n[1]),smooth)*sign
        c=int(np.argmin(np.abs(ts)))
        lo=max(0,c-int(follow*2)); hi=min(len(v)-1,c+int(follow*2))
        j=lo+int(np.argmax(v[lo:hi+1]))
        if j<6 or j>len(v)-7: break
        jl=int(np.argmin(v[:j])); jr=j+int(np.argmin(v[j:]))
        q=p+ts[j]*n
        S.append(k*step);P.append(q.copy());vs.append(v[j]);vf.append(0.5*(v[jl]+v[jr]))
        p=q+step*d
    return np.array(S),np.array(P),np.array(vs,float),np.array(vf,float)

def best_dir(img, p0, nominal, sign, halfwin, follow, span=55, nprobe=45, probe=70, step=1.0):
    a0=np.arctan2(nominal[1],nominal[0])
    best=None
    for a in np.linspace(a0-np.radians(span), a0+np.radians(span), nprobe):
        d=np.array([np.cos(a),np.sin(a)])
        S,P,vs,vf=march_track(img,p0,d,sign,halfwin,follow,step=step,nsteps=probe)
        if len(S)<probe*0.8: continue
        sc=float(np.mean(vs-vf))
        if best is None or sc>best[0]: best=(sc,d)
    return None if best is None else best[1]
