import numpy as np, json, sys
from lib import *
from scipy.ndimage import gaussian_filter, grey_closing, grey_opening, label, find_objects, sobel
SPAN={'OpSTlDJWFFI':(1040,2900),'Oqw96jCOP7A':(460,2400),'l9RAhmPHM_A':(900,4300),
      'ZB788PtqQvg':(60,1150),'RsQCXN4o4Ps':(400,1490)}
def phasecorr(a,b,maxsh=48):
    a=a-a.mean(); b=b-b.mean()
    w=np.outer(np.hanning(a.shape[0]),np.hanning(a.shape[1]))
    A=np.fft.fft2(a*w); B=np.fft.fft2(b*w)
    R=A*np.conj(B); R/=np.maximum(np.abs(R),1e-9)
    c=np.fft.fftshift(np.real(np.fft.ifft2(R)))
    cy,cx=np.array(c.shape)//2
    m=np.full(c.shape,-9.0); m[cy-maxsh:cy+maxsh+1,cx-maxsh:cx+maxsh+1]=c[cy-maxsh:cy+maxsh+1,cx-maxsh:cx+maxsh+1]
    iy,ix=np.unravel_index(np.argmax(m),m.shape)
    return iy-cy,ix-cx,float(c[iy,ix])
def tophats(a,size=13,hpsig=5.0):
    hp=a-gaussian_filter(a,hpsig)
    return grey_closing(hp,size=size)-hp, hp-grey_opening(hp,size=size)
def blobs(resp,amp,minpx,maxpx):
    L,n=label(resp>amp); out=[]
    for i,sl in enumerate(find_objects(L),1):
        msk=(L[sl]==i); npx=int(msk.sum())
        if npx<minpx or npx>maxpx: continue
        yy,xx=np.nonzero(msk)
        out.append((sl[0].start+yy, sl[1].start+xx, float(resp[sl][msk].max())))
    return out
def samp(resp,ys,xs,dy,dx):
    H,W=resp.shape; yy=ys+dy; xx=xs+dx
    ok=(yy>=0)&(yy<H)&(xx>=0)&(xx<W)
    return float(resp[yy[ok],xx[ok]].mean()) if ok.any() else np.nan
rng=np.random.default_rng(1)
res={}
for k in SPAN:
    y0,y1,x0,x1=PIC[k]
    s,e=SPAN[k]; e=min(e,nframes(k)-2)
    print('==== %s era%d  picture rect y[%d:%d] x[%d:%d]'%(k,ERA[k],y0,y1,x0,x1),flush=True)
    fd=np.load('fulldiff_%s.npy'%k)
    # candidate pairs: sizeable inter-frame change, spaced out
    cand=[i for i in range(s,e) if 0.8<fd[i-1]<12]
    rng.shuffle(cand)
    used=[]; A0=[];AF=[];AI=[];AR=[];AB=[]; pairs=[]
    for i in cand:
        if len(used)>=12: break
        if any(abs(i-u)<12 for u in used): continue
        a=F(k,i)[y0:y1,x0:x1]
        b=F(k,i+1)[y0:y1,x0:x1]
        gdy,gdx,pk=phasecorr(a,b)
        if not (7<=max(abs(gdy),abs(gdx))<=40): continue
        bh0,wh0=tophats(a); bh1,wh1=tophats(b)
        g=np.abs(sobel(gaussian_filter(a,2.0),0))+np.abs(sobel(gaussian_filter(a,2.0),1))
        gth=np.percentile(g,70)
        marks=[]
        for pol,r0 in (('D',bh0),('B',wh0)):
            for ys,xs,pkk in blobs(r0,5.0,6,1500):
                if (g[ys,xs]>gth).mean()>0.4: continue
                if ys.min()<45 or xs.min()<45 or ys.max()>a.shape[0]-45 or xs.max()>a.shape[1]-45: continue
                marks.append((pol,ys,xs,pkk))
        if len(marks)<4: continue
        used.append(i)
        a0=[];af=[];ai=[];ar=[];ab=[]
        for pol,ys,xs,pkk in marks:
            r0=bh0 if pol=='D' else wh0; r1=bh1 if pol=='D' else wh1
            a0.append(samp(r0,ys,xs,0,0)); af.append(samp(r1,ys,xs,0,0)); ai.append(samp(r1,ys,xs,gdy,gdx))
            rr=[]
            for _ in range(8):
                while True:
                    ry,rx=rng.integers(-40,41,2)
                    if max(abs(ry),abs(rx))>8 and max(abs(ry-gdy),abs(rx-gdx))>8: break
                rr.append(samp(r1,ys,xs,ry,rx))
            ar.append(np.nanmean(rr))
            # best-of-search: is the mark anywhere in the next frame?
            bb=max(samp(r1,ys,xs,dy,dx) for dy in range(-40,41,4) for dx in range(-40,41,4))
            ab.append(bb)
        a0=np.array(a0);af=np.array(af);ai=np.array(ai);ar=np.array(ar);ab=np.array(ab)
        m0,mf,mi,mr,mb=[np.nanmean(v) for v in (a0,af,ai,ar,ab)]
        print('  f%05d->f%05d g=(%+3d,%+3d) pcpk=%.3f n=%3d | A_src=%5.2f A_frame=%5.2f A_image=%5.2f A_rand=%5.2f A_bestof=%5.2f || ret_frame=%+.3f ret_image=%+.3f'%(
            i,i+1,gdy,gdx,pk,len(a0),m0,mf,mi,mr,mb,(mf-mr)/max(1e-9,m0-mr),(mi-mr)/max(1e-9,m0-mr)),flush=True)
        A0+=list(a0);AF+=list(af);AI+=list(ai);AR+=list(ar);AB+=list(ab)
        pairs.append([i,int(gdy),int(gdx),len(a0)])
    if A0:
        m0,mf,mi,mr,mb=[float(np.nanmean(v)) for v in (A0,AF,AI,AR,AB)]
        rf=(mf-mr)/(m0-mr); ri=(mi-mr)/(m0-mr); rb=(mb-mr)/(m0-mr)
        # bootstrap CI on rf-ri
        A0a,AFa,AIa,ARa=map(np.array,(A0,AF,AI,AR))
        bs=[]
        for _ in range(2000):
            j=rng.integers(0,len(A0a),len(A0a))
            d0=A0a[j].mean()-ARa[j].mean()
            bs.append(((AFa[j].mean()-ARa[j].mean())-(AIa[j].mean()-ARa[j].mean()))/max(1e-9,d0))
        lo,hi=np.percentile(bs,[2.5,97.5])
        print('  AGGREGATE %s: Nmarks=%d over %d pairs | A_src=%.2f A_frame=%.2f A_image=%.2f A_rand=%.2f A_bestof=%.2f'%(k,len(A0),len(pairs),m0,mf,mi,mr,mb))
        print('     retention_FRAME-FIXED=%.3f  retention_IMAGE-LOCKED=%.3f  retention_BESTOFSEARCH=%.3f  diff(frame-image)=%.3f [95%%CI %.3f..%.3f]'%(rf,ri,rb,rf-ri,lo,hi),flush=True)
        res[k]=dict(n=len(A0),pairs=pairs,A_src=m0,A_frame=mf,A_image=mi,A_rand=mr,A_best=mb,rf=rf,ri=ri,rb=rb,ci=[float(lo),float(hi)])
json.dump(res,open('taskC3.json','w'),indent=1,default=float)
