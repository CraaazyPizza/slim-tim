"""Frame bootstrap: is the typeface ranking significant?  Geometry fixed per face
from the best5 fit; the 20 caption frames are resampled 200 times."""
import numpy as np, sys, json
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from fast import *
ALL=json.load(open('fonts.json')); B2=json.load(open('sweepB2.json'))['best5']
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
RB=(902,1002); XB=(430,1615); TXT='Предыдущее сообщение'
def field(fs):
    o=(-RESL[[FR.index(f) for f in fs]].mean(0))[(RB[0]-Y0):(RB[1]-Y0),(XB[0]-X0):(XB[1]-X0)]
    return Field(o,*o.shape)
order=[d['font'] for d in B2][:9]; geo={d['font']:d for d in B2}
rng=np.random.default_rng(7)
draws=[[int(x) for x in rng.choice(CAP,size=10,replace=True)] for _ in range(200)]
BS={n:[] for n in order}
for dr in draws:
    fl=field(dr)
    for n in order:
        d=geo[n]; fp=ALL[n]; A=base_render(fp,TXT,capsize(fp,d['cap']))
        ink=place(A,d['kx'],fl.H,fl.W)
        BS[n].append(max(x[0] for x in fl.match(ink,[d['blur']],dxr=40)))
print('=== FRAME BOOTSTRAP, 200 resamples of 10-of-20 caption frames, geometry fixed ===')
print('%-26s %8s %8s'%('face','mean r','sd'))
for n in order:
    v=np.array(BS[n]); print('%-26s %8.4f %8.4f'%(n,v.mean(),v.std()))
w=order[0]; print('\npaired difference vs %s (same frames, so the pairing removes frame noise):'%w)
for n in order[1:]:
    dd=np.array(BS[w])-np.array(BS[n])
    print('   %-24s dr = %+.4f +- %.4f   %.1f sigma   P(%s wins) = %.2f'%(n,dd.mean(),dd.std(),dd.mean()/max(dd.std(),1e-9),w,(dd>0).mean()))
# how often is each face the top-ranked one across bootstrap draws?
M=np.array([BS[n] for n in order])
win=np.bincount(M.argmax(0),minlength=len(order))
print('\nhow often each face is ranked FIRST across the 200 resamples:')
for i,n in enumerate(order): print('   %-24s %3d / 200'%(n,win[i]))
json.dump({k:[float(x) for x in v] for k,v in BS.items()},open('bootstrap.json','w'),indent=1,ensure_ascii=False)
