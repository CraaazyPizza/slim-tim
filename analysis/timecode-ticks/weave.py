"""Adjudication of the "zero film weave" claim (FINDINGS section 3).

Claim: phase correlation of frames 950-1005 of video 1 returns exactly (0,0) on all 55
frames => no gate jitter at all.

Tests run here:
  T1  what the frames 950-1005 actually contain (are they featureless? duplicated?)
  T2  integer-argmax phase correlation, as originally done
  T3  sub-pixel phase correlation (parabolic peak fit) on the same frames
  T4  the same estimator on a matched control: the 2011 files, which nobody claims are
      synthetic-bordered
  T5  INJECTION TEST - shift a real frame by a known sub-pixel amount and see whether the
      estimator recovers it.  If it cannot, (0,0) means nothing.
"""
import numpy as np
from PIL import Image
np.set_printoptions(precision=3,suppress=True)

def L(fd,i,sz=None):
    im=Image.open('%s/f%05d.png'%(fd,i)).convert('L')
    a=np.asarray(im).astype(np.float64)
    return a

def han(sh):
    return np.outer(np.hanning(sh[0]),np.hanning(sh[1]))

def pc(a,b,sub=True,window=True):
    if window:
        w=han(a.shape); a=(a-a.mean())*w; b=(b-b.mean())*w
    else:
        a=a-a.mean(); b=b-b.mean()
    A=np.fft.fft2(a); B=np.fft.fft2(b)
    R=A*np.conj(B); m=np.abs(R); m[m==0]=1
    r=np.fft.ifft2(R/m).real
    k=np.unravel_index(np.argmax(r),r.shape)
    peak=r[k]
    dy,dx=k[0],k[1]
    if dy>a.shape[0]//2: dy-=a.shape[0]
    if dx>a.shape[1]//2: dx-=a.shape[1]
    if not sub: return float(dy),float(dx),float(peak)
    def par(v0,v1,v2):
        d=(v0-2*v1+v2)
        return 0.0 if d==0 else 0.5*(v0-v2)/d
    y,x=k
    ym,yp=r[(y-1)%r.shape[0],x],r[(y+1)%r.shape[0],x]
    xm,xp=r[y,(x-1)%r.shape[1]],r[y,(x+1)%r.shape[1]]
    return float(dy)+par(ym,peak,yp), float(dx)+par(xm,peak,xp), float(peak)

print('=== T1  what is in v1 f950-1005 ?')
fd='frames/OpSTlDJWFFI'
prev=None
stats=[]
for i in range(948,1008):
    a=L(fd,i)
    stats.append((i,a.mean(),a.std(),0 if prev is None else np.abs(a-prev).mean(),
                  0 if prev is None else float((a==prev).mean())))
    prev=a
print(' frame   mean    sd     |diff|  frac-identical-px')
for s in stats[1::6]: print(' %5d  %6.1f %6.2f  %6.3f   %.4f'%s)
d=np.array([s[3] for s in stats[1:]]); ident=np.array([s[4] for s in stats[1:]])
print(' over f949-1007: mean |frame diff| %.3f DN   median frac of pixels bit-identical to previous frame %.3f'%(d.mean(),np.median(ident)))
a=L(fd,975)
print(' f975 full-frame sd %.2f ;  sd inside the bright leader field (y 300-800, x 500-1400) = %.2f'%(
      a.std(), a[300:800,500:1400].std()))
print(' f975 gradient energy: |grad| mean full %.3f, inside leader field %.3f'%(
      np.abs(np.gradient(a)).mean(), np.abs(np.gradient(a[300:800,500:1400])).mean()))

print('\n=== T2/T3  phase correlation on v1 f950-1005, integer vs sub-pixel')
def sweep(fd,lo,hi,roi=None,tag=''):
    ii=[];sub=[]
    prev=None
    for i in range(lo,hi+1):
        a=L(fd,i)
        if roi: a=a[roi[0]:roi[1],roi[2]:roi[3]]
        if prev is not None:
            ii.append(pc(a,prev,sub=False)[:2]); sub.append(pc(a,prev,sub=True)[:2])
        prev=a
    ii=np.array(ii); sub=np.array(sub)
    print(' %-42s n=%d  integer: %d/%d pairs exactly (0,0)   sub-pixel: sd dy %.4f dx %.4f  max|d| %.3f'%(
        tag,len(ii),int(((ii==0).all(1)).sum()),len(ii),sub[:,0].std(),sub[:,1].std(),np.abs(sub).max()))
    return ii,sub
sweep(fd,950,1005,None,'v1 f950-1005 FULL FRAME')
sweep(fd,950,1005,(300,800,500,1400),'v1 f950-1005 leader field only')
sweep(fd,1600,1655,None,'v1 f1600-1655 (moving b/w picture) FULL')

print('\n=== T4  matched control: 2011 files, same estimator')
sweep('frames/RsQCXN4o4Ps',1131,1186,None,'2011 RsQCX f1131-1186 FULL')
sweep('frames/ZB788PtqQvg',186,241,None,'2011 ZB788 f186-241 FULL')
sweep('frames/Xju_CY5ZESA',400,455,None,'2011 Xju f400-455 FULL')

print('\n=== T5  INJECTION TEST: can the estimator see a shift at all?')
from scipy import ndimage
base=L(fd,975); base2=L(fd,1600)
for nm,img in (('v1 f975 (bright leader)',base),('v1 f1600 (real picture)',base2)):
    print('  %s'%nm)
    for s in (0.10,0.25,0.5,1.0,2.0):
        sh=ndimage.shift(img,(0.0,s),order=3,mode='nearest')
        dy,dx,_=pc(sh,img,sub=True)
        dyi,dxi,_=pc(sh,img,sub=False)
        print('     injected dx=%+.2f px -> sub-pixel estimate dx=%+.3f (err %+.3f) ; integer estimate dx=%+.0f'%(
              s,dx,dx-s,dxi))
