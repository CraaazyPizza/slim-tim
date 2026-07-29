import numpy as np, sys, json
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
OFFC=np.r_[np.arange(300-X0,430-X0), np.arange(1625-X0,1750-X0)]
def clean(X):
    Y=-X; return Y - Y[:,OFFC].mean(1,keepdims=True)
ci=[FR.index(f) for f in CAP]
NUL=clean(RESL[[FR.index(f) for f in range(1005,1050)]].mean(0))
def sig(fs): return clean(RESL[[FR.index(f) for f in fs]].mean(0)) - NUL
OB={'f983':sig([983]),'best5':sig([983,973,974,984,981]),'stack20':sig(CAP)}
def rp(X,xs,rows=(905,1005)):
    return np.arange(rows[0],rows[1]), X[(rows[0]-Y0):(rows[1]-Y0),(xs[0]-X0):(xs[1]-X0)].mean(1)
def cross(ys,p,frac,rising,lo,hi,plateau):
    """sub-pixel crossing of frac*plateau within [lo,hi]"""
    m=(ys>=lo)&(ys<=hi); yy=ys[m]; pp=p[m]; t=frac*plateau
    for i in range(len(pp)-1):
        if rising and pp[i]<t<=pp[i+1]: return yy[i]+(t-pp[i])/(pp[i+1]-pp[i])
        if (not rising) and pp[i]>t>=pp[i+1]: return yy[i]+(pp[i]-t)/(pp[i]-pp[i+1])
    return np.nan
out={}
for tag,X in OB.items():
    ys,pP=rp(X,(452,504)); _,po=rp(X,(1176,1220)); _,poo=rp(X,(1238,1280)); _,pb=rp(X,(1296,1338))
    capbar=pP[(ys>=925)&(ys<=929)].mean()
    capTop=cross(ys,pP,0.5,True,912,932,capbar)
    stemlev=pP[(ys>=948)&(ys<=968)].mean()
    base=cross(ys,pP,0.5,False,966,985,stemlev)
    res={}
    for nm,pr in [('o1',po),('o2',poo)]:
        top=pr[(ys>=940)&(ys<=944)].mean(); bot=pr[(ys>=966)&(ys<=972)].mean()
        xt=cross(ys,pr,0.5,True,930,944,top); xb=cross(ys,pr,0.5,False,970,984,bot)
        res[nm]=(xt,xb)
    xt=np.mean([res[k][0] for k in res]); xb=np.mean([res[k][1] for k in res])
    print('%-8s capTop %.2f  base(П) %.2f  CAP %.2f | o top %.2f  o bot %.2f  o height %.2f | xh/cap %.3f'
          %(tag,capTop,base,base-capTop,xt,xb,xb-xt,(xb-xt)/(base-capTop)))
    out[tag]=dict(capTop=capTop,base=base,cap=base-capTop,otop=xt,obot=xb,oh=xb-xt)
json.dump(out,open('vmet.json','w'),indent=1)
