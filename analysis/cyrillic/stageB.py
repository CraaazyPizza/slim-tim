"""STAGE B: shortlist refined on the full line-1 window, several observations and
nulls, plus a frame-bootstrap so face-vs-face differences get an error bar."""
import numpy as np, sys, json, time
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from fast import *
ALL=json.load(open('fonts.json')); A=json.load(open('sweepA.json'))
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
RB=(902,1002); XB=(430,1615); TXT='Предыдущее сообщение'
def field(fs):
    o=(-RESL[[FR.index(f) for f in fs]].mean(0))[(RB[0]-Y0):(RB[1]-Y0),(XB[0]-X0):(XB[1]-X0)]
    return Field(o,*o.shape)
def best_of(fl,fp,caps,kxs,bls):
    best=None
    for cap in caps:
        s=capsize(fp,cap); Aa=base_render(fp,TXT,s)
        for kx in kxs:
            ink=place(Aa,kx,fl.H,fl.W)
            for r,bl,dx,dy in fl.match(ink,bls,dxr=40):
                if best is None or r>best[0]: best=(r,cap,s,float(kx),bl,dx,dy)
    return best
TOP=[d['font'] for d in A[:34]]
for m in ['Roboto Medium','Roboto Regular','DejaVu Sans Bold','DejaVu Sans Book','Liberation Sans Bold',
          'Liberation Sans Regular','Arimo Bold','Arimo Regular','Open Sans Regular','Open Sans Semibold',
          'Open Sans Bold','Noto Sans Regular','Noto Sans Bold','Lato Bold','Carlito Bold','Cantarell Bold',
          'Nimbus Sans Bold','FreeSans Bold','URW Gothic Demi','Comfortaa Bold','DejaVu Serif Book',
          'Liberation Serif Bold','Nimbus Mono PS Bold','Cousine Bold']:
    if m in ALL and m not in TOP: TOP.append(m)
KX=np.round(np.arange(1.12,1.57,0.04),2); BL=[1.0,1.6,2.2,2.8,3.6,4.6,5.8]; CAPS=[52,54]
OBS={'f983':field([983]),'best5':field([983,973,974,984,981]),'stack20':field(CAP),
     'NULL20_1010':field(list(range(1010,1030))),'NULL1_f1020':field([1020])}
t0=time.time(); res={}
for tag,fl in OBS.items():
    rows=[]
    for n in TOP:
        b=best_of(fl,ALL[n],CAPS,KX,BL)
        rows.append(dict(font=n,file=ALL[n],r=b[0],cap=b[1],size=b[2],kx=b[3],blur=b[4],dx=b[5],dy=b[6]))
    rows.sort(key=lambda d:-d['r']); res[tag]=rows
    rr=np.array([d['r'] for d in rows])
    print('\n=== STAGE B %s (%.0fs) === n=%d  field median %.4f sd %.4f'%(tag,time.time()-t0,len(rows),np.median(rr),rr.std()))
    print('%-40s %7s %6s %5s %5s %6s %5s'%('face','r','cap','kx','blur','dx','dy'))
    for d in rows: print('%-40s %7.4f %6.1f %5.2f %5.1f %6d %5d'%(d['font'],d['r'],d['cap'],d['kx'],d['blur'],d['dx'],d['dy']))
    sys.stdout.flush(); json.dump(res,open('sweepB.json','w'),indent=1,ensure_ascii=False)
# ---------------- bootstrap: same geometry, resampled caption frames
print('\n=== FRAME BOOTSTRAP (200 resamples of the 20 caption frames, geometry fixed per face) ===')
rng=np.random.default_rng(7)
top=[d for d in res['best5'][:10]]
draws=[list(rng.choice(CAP,size=10,replace=True)) for _ in range(200)]
BS={d['font']:[] for d in top}
for dr in draws:
    fl=field(dr)
    for d in top:
        fp=ALL[d['font']]; s=capsize(fp,d['cap']); Aa=base_render(fp,TXT,s)
        ink=place(Aa,d['kx'],fl.H,fl.W)
        r=max(x[0] for x in fl.match(ink,[d['blur']],dxr=40))
        BS[d['font']].append(r)
print('%-40s %8s %8s'%('face','mean r','sd'))
for d in top:
    v=np.array(BS[d['font']]); print('%-40s %8.4f %8.4f'%(d['font'],v.mean(),v.std()))
w=top[0]['font']
print('\npaired differences vs the winner (%s):'%w)
for d in top[1:]:
    dd=np.array(BS[w])-np.array(BS[d['font']])
    print('   %-38s  dr = %+.4f +- %.4f   (%.1f sigma, P(win)=%.2f)'%(
        d['font'],dd.mean(),dd.std(),dd.mean()/max(dd.std(),1e-9),(dd>0).mean()))
json.dump({k:list(map(float,v)) for k,v in BS.items()},open('bootstrap.json','w'),indent=1,ensure_ascii=False)
