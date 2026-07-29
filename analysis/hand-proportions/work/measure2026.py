import numpy as np, sys, os, json
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/hand-proportions/work')
from PIL import Image
from scipy import ndimage as ndi
from caps import find_caps, cap_tip
from rowsep import row_track, cleft_level

FR='/home/user/new-skinny-bob/frames/l9RAhmPHM_A/f{:05d}.png'

def ridge_axis(img, x0, y0, y1, follow=14, halfwin=0):
    """track the bright ridge of a digit shaft from y0 to y1, return fitted line."""
    xs=[];ys=[]; x=float(x0)
    for y in range(int(y0),int(y1)+1):
        row=ndi.gaussian_filter1d(img[y].astype(float),1.5)
        lo=int(max(0,x-follow)); hi=int(min(len(row)-1,x+follow))
        j=lo+int(np.argmax(row[lo:hi+1]))
        xs.append(j);ys.append(y); x=0.5*x+0.5*j
    xs=np.array(xs,float);ys=np.array(ys,float)
    A=np.stack([ys,np.ones_like(ys)],1)
    c,*_=np.linalg.lstsq(A,xs,rcond=None)      # x = c0*y + c1
    d=np.array([-c[0],-1.0]); d/=np.linalg.norm(d)   # distal direction (up)
    return c, d, (xs,ys)

def measure(nfr, capthr=55, cap_box=(330,520,560,1010), frac=0.5, verbose=False):
    img=np.asarray(Image.open(FR.format(nfr)).convert('L')).astype(float)
    caps=find_caps(img,cap_box,capthr)
    caps=[c for c in caps if c['area']>250 and max(c['h'],c['w'])<45]
    caps.sort(key=lambda c:c['cx'])
    if len(caps)<3: return None
    fing=caps[-3:]           # the three finger caps (thumb is leftmost / excluded by size)
    out={'frame':nfr}
    axes=[];tips=[]
    for i,c in enumerate(fing):
        ytop=int(c['cy']+c['h']/2+6)
        cc,d,_=ridge_axis(img, c['cx'], ytop, ytop+110)
        axes.append((cc,d))
        tips.append(cap_tip(c,d))
    out['tips']={f'T{i+2}':[float(t[0]),float(t[1])] for i,t in enumerate(tips)}
    out['axes']=[[float(cc[0]),float(cc[1]),float(d[0]),float(d[1])] for cc,d in axes]
    # grooves
    for k,(i,j) in enumerate([(0,1),(1,2)]):
        ys=int(max(fing[i]['cy']+fing[i]['h']/2, fing[j]['cy']+fing[j]['h']/2)+22)
        xi=axes[i][0][0]*ys+axes[i][0][1]; xj=axes[j][0][0]*ys+axes[j][0][1]
        xs0=0.5*(xi+xj)
        y,x,vs,vf=row_track(img, ys, ys+230, xs0, -1, halfwin=42, follow=16)
        if len(y)<40: return None
        yy,idx,g0,V,thr=cleft_level(y,vs,vf,frac=frac)
        key=['C23','C34'][k]
        out[key]=[float(x[idx]),float(yy)]
        out[key+'_prof']=dict(y=y.tolist(),x=x.tolist(),V=(-V).tolist(),thr=(-thr).tolist(),g0=float(-g0))
        if verbose: print(key,'start',ys,round(xs0,1),'->',out[key])
    return out

if __name__=='__main__':
    r=measure(3866, verbose=True)
    print(json.dumps({k:v for k,v in r.items() if not k.endswith('_prof')},indent=1,default=str))
