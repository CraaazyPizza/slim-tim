import numpy as np
from lib import *
from scipy.ndimage import gaussian_filter, sobel
CARD={'OpSTlDJWFFI':(60,560),'Oqw96jCOP7A':(40,430),'l9RAhmPHM_A':(60,560),
'Xju_CY5ZESA':(200,700),'a6TLGkrfNKI':(200,700)}
print('(1) TEXT-CARD / TITLE sections: does any noise layer animate over a fully static graphic?')
print('%-13s %-5s %-11s %9s %9s %9s %9s'%('video','era','frames','bitdup_fr','HP2_ncc1','HP2_ncc5','absdiff'))
for k,(s,e) in CARD.items():
    y0,y1,x0,x1=PIC[k]; cy=(y0+y1)//2; cx=(x0+x1)//2
    r=(cy-96,cy+96,cx-96,cx+96)
    Xs=[]; dup=0; ad=[]; prev=None
    for i in range(s,e+1):
        a=F(k,i)[r[0]:r[1],r[2]:r[3]]
        if prev is not None:
            dup+= np.array_equal(a,prev); ad.append(np.abs(a-prev).mean())
        prev=a
        h=(a-gaussian_filter(a,2.0)).ravel(); h=h-h.mean(); n=np.linalg.norm(h)
        Xs.append((h/max(n,1e-9)).astype(np.float32))
    X=np.stack(Xs); G=X@X.T
    print('%-13s %-5d %5d-%5d %9.3f %9.4f %9.4f %9.4f    rect y[%d:%d] x[%d:%d]'%(
      k,ERA[k],s,e,dup/(len(X)-1),np.diagonal(G,1).mean(),np.diagonal(G,5).mean(),np.mean(ad),*r))
print()
print('(2) BAND-LIMITED grain amplitude vs luminance  (band = gauss(s=1.2) minus gauss(s=6): ~0.08-0.4 cyc/px)')
PROBE={'OpSTlDJWFFI':[1330,1650,2200,2450,2700,2850],'Oqw96jCOP7A':[650,800,1250,1500,1900,2350],
'l9RAhmPHM_A':[900,1098,2000,3000,3296,4200],'ZB788PtqQvg':[297,534,772,891,1009,1128],
'RsQCXN4o4Ps':[675,825,975,1125,1275,1425],'Xju_CY5ZESA':[389,909,1428,1948,2208],
'a6TLGkrfNKI':[350,700,1000,1400,1752,1986]}
edges=np.array([10,25,45,70,100,135,175,215,256])
hdr='%-13s %-5s'%('video','era')+''.join('%9s'%('%d-%d'%(edges[i],edges[i+1])) for i in range(len(edges)-1))
print(hdr)
for k in V:
    y0,y1,x0,x1=PIC[k]
    num=np.zeros(len(edges)-1); den=np.zeros(len(edges)-1)
    for i in PROBE[k]:
        a=F(k,i)[y0:y1,x0:x1]
        band=gaussian_filter(a,1.2)-gaussian_filter(a,6.0)
        lo=gaussian_filter(a,6.0)
        g=np.abs(sobel(lo,0))+np.abs(sobel(lo,1))
        m=g<np.percentile(g,30)
        b=np.digitize(lo[m],edges)-1; v=band[m]**2
        for j in range(len(edges)-1):
            sel=b==j
            if sel.sum()>800: num[j]+=v[sel].sum(); den[j]+=sel.sum()
    out=np.where(den>0,np.sqrt(num/np.maximum(den,1)),np.nan)
    print('%-13s %-5d'%(k,ERA[k])+''.join(('%9.3f'%o if np.isfinite(o) else '%9s'%'-') for o in out))
