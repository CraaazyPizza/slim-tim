import numpy as np, json
from lib import *
def phasecorr(a,b,maxsh=None):
    a=a-a.mean(); b=b-b.mean()
    w=np.outer(np.hanning(a.shape[0]),np.hanning(a.shape[1]))
    A=np.fft.fft2(a*w); B=np.fft.fft2(b*w)
    R=A*np.conj(B); R/=np.maximum(np.abs(R),1e-9)
    c=np.real(np.fft.ifft2(R))
    c=np.fft.fftshift(c)
    cy,cx=np.array(c.shape)//2
    if maxsh:
        m=np.zeros_like(c,bool); m[cy-maxsh:cy+maxsh+1,cx-maxsh:cx+maxsh+1]=True
        c=np.where(m,c,-9)
    iy,ix=np.unravel_index(np.argmax(c),c.shape)
    # subpixel parabolic
    def sp(v0,v1,v2):
        d=(v0-v2)/(2*(v0-2*v1+v2)) if (v0-2*v1+v2)!=0 else 0
        return np.clip(d,-1,1)
    dy=iy-cy+sp(c[iy-1,ix],c[iy,ix],c[iy+1,ix]); dx=ix-cx+sp(c[iy,ix-1],c[iy,ix],c[iy,ix+1])
    return dy,dx,float(c[iy,ix])
out={}
for k in V:
    a=np.load('thumb_%s.npy'%k,mmap_mode='r')
    y0,y1,x0,x1=[v//4 for v in PIC[k]]
    rows=[]
    for i in range(1,len(a)-1):
        pass
    # sample: compute for all consecutive pairs but on small crop, subsample step 1 in chosen span
    SPAN={'OpSTlDJWFFI':(1500,2400),'Oqw96jCOP7A':(600,1500),'l9RAhmPHM_A':(1000,1900),
    'ZB788PtqQvg':(200,1100),'RsQCXN4o4Ps':(600,1450),'Xju_CY5ZESA':(200,1100),'a6TLGkrfNKI':(200,1100)}
    s,e=SPAN[k]
    for i in range(s,min(e,len(a)-1)):
        p=np.array(a[i-1][y0:y1,x0:x1],dtype=np.float64); q=np.array(a[i][y0:y1,x0:x1],dtype=np.float64)
        if np.abs(q-p).mean()<0.05: continue
        dy,dx,pk=phasecorr(p,q,maxsh=12)
        rows.append((i,dy*4,dx*4,pk,float(np.abs(q-p).mean())))
    rows.sort(key=lambda r:-(r[1]**2+r[2]**2))
    good=[r for r in rows if r[3]>0.06 and (r[1]**2+r[2]**2)>25 and (abs(r[1])<40 and abs(r[2])<40)]
    print('== %s era%d  pairs computed=%d  |motion|>5px & pk>0.06: %d'%(k,ERA[k],len(rows),len(good)))
    for r in good[:8]: print('    f%05d->f%05d  dy=%+7.2f dx=%+7.2f  pcpeak=%.3f  meanabsdiff=%.3f'%(r[0],r[0]+1,r[1],r[2],r[3],r[4]))
    out[k]=good[:60]
json.dump(out,open('motion.json','w'))
