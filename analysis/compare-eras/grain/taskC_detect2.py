import numpy as np
from lib import *
from scipy.ndimage import gaussian_filter, grey_closing, grey_opening, label, find_objects
def detect(a,amp=6.0,size=11,minpx=4,maxpx=2000):
    hp=a-gaussian_filter(a,5.0)
    bh=grey_closing(hp,size=size)-hp
    wh=hp-grey_opening(hp,size=size)
    out=[]
    for pol,m in (('D',bh>amp),('B',wh>amp)):
        L,n=label(m)
        objs=find_objects(L)
        for i,sl in enumerate(objs,1):
            npx=int((L[sl]==i).sum())
            if npx<minpx or npx>maxpx: continue
            reg=(bh if pol=='D' else wh)[sl]*(L[sl]==i)
            pk=float(reg.max())
            yy,xx=np.nonzero(L[sl]==i)
            cy=sl[0].start+yy.mean(); cx=sl[1].start+xx.mean()
            h=sl[0].stop-sl[0].start; w=sl[1].stop-sl[1].start
            out.append((pol,cy,cx,npx,pk,h,w))
    return out
if __name__=='__main__':
    FR={'OpSTlDJWFFI':[1650,2200,2450,2700,2850],'Oqw96jCOP7A':[650,800,1250,1500,1900],
    'l9RAhmPHM_A':[900,1098,2000,3296,4200],'ZB788PtqQvg':[297,534,772,1009,1128],
    'RsQCXN4o4Ps':[675,975,1275,1425],'Xju_CY5ZESA':[389,1428,2208],'a6TLGkrfNKI':[350,1000,1752,1986]}
    for k in V:
        y0,y1,x0,x1=PIC[k]
        print('== %s era%d'%(k,ERA[k]))
        for f in FR[k]:
            a=F(k,f)[y0:y1,x0:x1]
            m=detect(a)
            nd=[x for x in m if x[0]=='D']; nb=[x for x in m if x[0]=='B']
            def st(l):
                if not l: return 'none'
                return 'n=%d medsize=%d medpk=%.1f maxpk=%.1f medAR=%.2f'%(len(l),int(np.median([x[3] for x in l])),
                  np.median([x[4] for x in l]),max(x[4] for x in l),np.median([max(x[5],x[6])/max(1,min(x[5],x[6])) for x in l]))
            print('   f%05d DARK: %s'%(f,st(nd)))
            print('           BRT : %s'%st(nb))
