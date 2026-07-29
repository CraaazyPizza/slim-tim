import numpy as np, json
from PIL import Image
D='/home/user/new-skinny-bob/frames/l9RAhmPHM_A'
PITCH=42.667; X0C=475.5; Y0,Y1=938,1000
def cellq(a,k):
    c=X0C+PITCH*k; x0=int(round(c-16)); x1=x0+32
    p=a[Y0:Y1,x0:x1]
    lo=np.percentile(p,15); hi=np.percentile(p,97)
    return np.clip((p-lo)/max(hi-lo,1.0),0,1)
def load(i): return np.array(Image.open(f'{D}/f{i:05d}.png').convert('L')).astype(np.float32)
# templates from cell 11 (shape identical for all digit cells since monospace)
TR={0:[2257,1777],1:[2302,3727],2:[637,1282],3:[682,2392],4:[727,2437],
    5:[772,2497],6:[997,2557],7:[1657,3697],8:[1687,2857],9:[1732,2242]}
T=[]
for d,fs in TR.items():
    for f in fs: T.append((d,cellq(load(f),11)))
Tarr=np.stack([t for _,t in T]); Tlab=np.array([d for d,_ in T])
def clas(q):
    e=((Tarr-q[None])**2).mean(axis=(1,2))
    j=e.argmin(); return int(Tlab[j]), float(e[j])
# subpixel edge on a profile
def crossing(prof, xs, lvl):
    for j in range(len(xs)-1):
        a0,b0=prof[j],prof[j+1]
        if (a0-lvl)*(b0-lvl)<0:
            return xs[j]+(lvl-a0)/(b0-a0)*(xs[j+1]-xs[j])
    return None
out={}
for i in range(457,4262):
    a=load(i)
    ds=[clas(cellq(a,k)) for k in (1,2,4,5,7,8,10,11)]
    # gate edges using matte level 28.5 and 50% between matte and interior
    matte=28.5
    row=a[300:800,:].mean(axis=0)
    col=a[:,500:1300].mean(axis=1)
    inL=row[380:520].mean(); inR=row[1250:1400].mean()
    inT=col[350:500].mean(); inB=col[650:800].mean()
    L=crossing(row[240:400][::-1], list(range(399,239,-1)), (matte+inL)/2)
    R=crossing(row[1450:1620], list(range(1450,1620)), (matte+inR)/2)
    Tp=crossing(col[20:200][::-1], list(range(199,19,-1)), (matte+inT)/2)
    B=crossing(col[980:1079], list(range(980,1079)), (matte+inB)/2)
    out[i]=dict(d=[x[0] for x in ds], e=[round(x[1],4) for x in ds],
                g=[None if v is None else round(float(v),3) for v in (L,R,Tp,B)],
                lev=[round(float(x),2) for x in (inL,inR,inT,inB)])
json.dump(out,open('/home/user/new-skinny-bob/analysis/teardown-video3/full.json','w'))
print('ok')
