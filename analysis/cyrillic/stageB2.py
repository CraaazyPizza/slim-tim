"""Stage B part 2: the other observations, the nulls, and the frame bootstrap."""
import numpy as np, sys, json, time
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from fast import *
ALL=json.load(open('fonts.json'))
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
                if best is None or r>best[0]: best=(r,cap,s,float(kx),bl,int(dx),int(dy))
    return best
FACES=['Nimbus Sans Bold','Arimo Bold','Roboto Medium','Go Bold','Liberation Sans Bold','Roboto Bold',
       'Carlito Bold','Lato Bold','Open Sans Semibold','DejaVu Sans Book','DejaVu Sans Bold',
       'Noto Sans Regular','Cantarell Bold','Nimbus Mono PS Bold','Liberation Serif Bold']
FACES=[f for f in FACES if f in ALL]
KX=np.round(np.arange(1.12,1.57,0.04),2); BL=[1.0,1.6,2.2,2.8,3.6,4.6,5.8]; CAPS=[52,54]
OBS={'best5':field([983,973,974,984,981]),'stack20':field(CAP),
     'NULL20_1010':field(list(range(1010,1030))),'NULL1_f1020':field([1020])}
res={}; t0=time.time()
for tag,fl in OBS.items():
    rows=[]
    for n in FACES:
        b=best_of(fl,ALL[n],CAPS,KX,BL)
        rows.append(dict(font=n,r=b[0],cap=b[1],size=b[2],kx=b[3],blur=b[4],dx=b[5],dy=b[6]))
    rows.sort(key=lambda d:-d['r']); res[tag]=rows
    print('\n=== %s (%.0fs) ==='%(tag,time.time()-t0))
    print('%-30s %7s %6s %5s %5s'%('face','r','cap','kx','blur'))
    for d in rows: print('%-30s %7.4f %6.1f %5.2f %5.1f'%(d['font'],d['r'],d['cap'],d['kx'],d['blur']))
    sys.stdout.flush()
json.dump(res,open('sweepB2.json','w'),indent=1,ensure_ascii=False)
# --------- frame bootstrap at fixed per-face geometry
B=json.load(open('sweepB.json'))['f983']
geo={d['font']:d for d in B if d['font'] in FACES}
order=[d['font'] for d in B if d['font'] in FACES][:8]
rng=np.random.default_rng(7)
draws=[[int(x) for x in rng.choice(CAP,size=10,replace=True)] for _ in range(150)]
BS={n:[] for n in order}
for dr in draws:
    fl=field(dr)
    for n in order:
        d=geo[n]; fp=ALL[n]; Aa=base_render(fp,TXT,capsize(fp,d['cap']))
        ink=place(Aa,d['kx'],fl.H,fl.W)
        BS[n].append(max(x[0] for x in fl.match(ink,[d['blur']],dxr=40)))
print('\n=== FRAME BOOTSTRAP (150 resamples of 10 of the 20 caption frames; geometry fixed) ===')
print('%-30s %8s %8s'%('face','mean r','sd'))
for n in order:
    v=np.array(BS[n]); print('%-30s %8.4f %8.4f'%(n,v.mean(),v.std()))
w=order[0]; print('\npaired differences vs %s:'%w)
for n in order[1:]:
    dd=np.array(BS[w])-np.array(BS[n])
    print('   %-28s dr = %+.4f +- %.4f  (%.1f sigma, P(%s wins) = %.2f)'%(n,dd.mean(),dd.std(),dd.mean()/max(dd.std(),1e-9),w,(dd>0).mean()))
json.dump({k:[float(x) for x in v] for k,v in BS.items()},open('bootstrap.json','w'),indent=1,ensure_ascii=False)
