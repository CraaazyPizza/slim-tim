import numpy as np, json, sys, os
os.chdir('/home/user/new-skinny-bob/analysis/hand-proportions'); sys.path.insert(0,'work')
from pipeline import row_track, cleft_level
from caps import find_caps, cap_tip
from PIL import Image
from scipy import ndimage as ndi

FR='/home/user/new-skinny-bob/frames/l9RAhmPHM_A/f{:05d}.png'
HOLD=23; SM=7     # scaled from the 2011 settings by the 1.9x size ratio

def measure(nfr, frac, capthr=55, cap_box=(280,470,480,1080), seeds=None):
    img=np.asarray(Image.open(FR.format(nfr)).convert('L')).astype(float)
    caps=[c for c in find_caps(img,cap_box,capthr) if 180<c['area']<1000 and max(c['h'],c['w'])<48]
    caps.sort(key=lambda c:c['cx'])
    if seeds is not None:
        f=[]
        for sx,sy in seeds:
            d=[( (c['cx']-sx)**2+(c['cy']-sy)**2, c) for c in caps]
            d.sort(key=lambda z:z[0])
            if not d or d[0][0]>55**2: return None
            f.append(d[0][1])
    else:
        if len(caps)<3: return None
        f=caps[-3:]
    f.sort(key=lambda c:c['cx'])
    # provisional distal direction from the two groove tracks (iterate once)
    d=np.array([0.42,-0.91]); d/=np.linalg.norm(d)
    for it in range(2):
        tips=[cap_tip(c,d) for c in f]
        res={'frame':nfr,'tips':{f'T{i+2}':[float(t[0]),float(t[1])] for i,t in enumerate(tips)}}
        dirs=[]
        ok=True
        for k,(i,j) in enumerate([(0,1),(1,2)]):
            ys=int(max(f[i]['cy']+f[i]['h']/2, f[j]['cy']+f[j]['h']/2)+20)
            xs0=0.5*(f[i]['cx']+f[j]['cx'])
            y,x,vs,vf=row_track(img, ys, ys+235, xs0, -1, halfwin=42, follow=16)
            if len(y)<60: ok=False; break
            yy,idx,g0,V,thr=cleft_level(y,vs,vf,frac,HOLD,SM)
            key=['C23','C34'][k]
            res[key]=[float(x[idx]),float(yy)]
            res[key+'_prof']={'y':y.tolist(),'x':x.tolist(),'V':(-V).tolist(),'thr':(-thr).tolist()}
            # groove direction from a robust fit over the open part
            m=slice(0,max(10,idx))
            A=np.stack([y[m].astype(float),np.ones(m.stop-m.start)],1)
            c0,*_=np.linalg.lstsq(A,x[m],rcond=None)
            dd=np.array([-c0[0],-1.0]); dd/=np.linalg.norm(dd); dirs.append(dd)
        if not ok: return None
        d=np.mean(dirs,0); d/=np.linalg.norm(d)
    res['dirs']=[list(map(float,v)) for v in dirs]
    res['d']=list(map(float,d))
    res['caps']=[[float(c['cx']),float(c['cy']),int(c['area'])] for c in f]
    return res

if __name__=='__main__':
    frames=[int(a) for a in sys.argv[2:]] if len(sys.argv)>2 else [3866]
    frac=float(sys.argv[1])
    for n in frames:
        r=measure(n,frac)
        if r is None: print(n,'FAIL'); continue
        print(n, {k:np.round(v,1).tolist() if isinstance(v,list) else v
                  for k,v in r.items() if k in ('C23','C34','d')}, r['tips'])
