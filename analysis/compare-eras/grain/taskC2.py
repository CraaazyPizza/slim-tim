import numpy as np, json
from lib import *
from scipy.ndimage import gaussian_filter, grey_closing, grey_opening, label, find_objects, sobel
def tophats(a,size=13,hpsig=5.0):
    hp=a-gaussian_filter(a,hpsig)
    return grey_closing(hp,size=size)-hp, hp-grey_opening(hp,size=size), hp
def blobs(resp,amp,minpx,maxpx):
    L,n=label(resp>amp); out=[]
    for i,sl in enumerate(find_objects(L),1):
        msk=(L[sl]==i); npx=int(msk.sum())
        if npx<minpx or npx>maxpx: continue
        yy,xx=np.nonzero(msk)
        out.append((sl[0].start+yy, sl[1].start+xx, float(resp[sl][msk].max()), npx))
    return out
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
def sample(resp,ys,xs,dy,dx):
    H,W=resp.shape
    yy=ys+dy; xx=xs+dx
    ok=(yy>=0)&(yy<H)&(xx>=0)&(xx<W)
    if ok.sum()==0: return np.nan
    return float(resp[yy[ok],xx[ok]].mean())
MOT=json.load(open('motion.json'))
rng=np.random.default_rng(0)
res={}
for k in ['OpSTlDJWFFI','Oqw96jCOP7A','l9RAhmPHM_A','ZB788PtqQvg','RsQCXN4o4Ps']:
    y0,y1,x0,x1=PIC[k]
    print('==== %s era%d'%(k,ERA[k]),flush=True)
    cand=[m for m in MOT[k] if 8<max(abs(m[1]),abs(m[2]))<38]
    used=[]; agg={'AF':[],'AI':[],'AR':[],'A0':[],'n':0,'pairs':[]}
    for m in cand:
        if len(used)>=8: break
        i=m[0]
        if any(abs(i-u)<10 for u in used): continue
        a=F(k,i)[y0:y1,x0:x1]; b=F(k,i+1)[y0:y1,x0:x1]
        gdy,gdx,pk=phasecorr(a,b)
        if not (6<=max(abs(gdy),abs(gdx))<=40): continue
        bh0,wh0,hp0=tophats(a); bh1,wh1,hp1=tophats(b)
        g=np.abs(sobel(gaussian_filter(a,2.0),0))+np.abs(sobel(gaussian_filter(a,2.0),1))
        gth=np.percentile(g,55)
        allys=[];allxs=[];amps=[]
        for pol,r0 in (('D',bh0),('B',wh0)):
            for ys,xs,pkk,npx in blobs(r0,6.0,8,1200):
                if (g[ys,xs]>gth).mean()>0.3: continue      # skip marks on textured/edge background
                if ys.min()<45 or xs.min()<45 or ys.max()>a.shape[0]-45 or xs.max()>a.shape[1]-45: continue
                allys.append((pol,ys,xs,pkk))
        if len(allys)<6: continue
        used.append(i)
        AF=[];AI=[];AR=[];A0=[]
        for pol,ys,xs,pkk in allys:
            r1=bh1 if pol=='D' else wh1
            r0=bh0 if pol=='D' else wh0
            A0.append(sample(r0,ys,xs,0,0))
            AF.append(sample(r1,ys,xs,0,0))
            AI.append(sample(r1,ys,xs,gdy,gdx))
            rr=[]
            for _ in range(6):
                while True:
                    ry,rx=rng.integers(-40,41,2)
                    if max(abs(ry),abs(rx))>8 and max(abs(ry-gdy),abs(rx-gdx))>8: break
                rr.append(sample(r1,ys,xs,ry,rx))
            AR.append(np.nanmean(rr))
        A0=np.array(A0);AF=np.array(AF);AI=np.array(AI);AR=np.array(AR)
        print('  f%05d->f%05d g=(%+d,%+d) pcpk=%.3f nmarks=%3d | A0(src)=%6.2f  A_frameFixed=%6.2f  A_imageLocked=%6.2f  A_random=%6.2f  || retention_frame=%.2f retention_image=%.2f'%(
          i,i+1,gdy,gdx,pk,len(A0),np.nanmean(A0),np.nanmean(AF),np.nanmean(AI),np.nanmean(AR),
          (np.nanmean(AF)-np.nanmean(AR))/max(1e-9,np.nanmean(A0)-np.nanmean(AR)),
          (np.nanmean(AI)-np.nanmean(AR))/max(1e-9,np.nanmean(A0)-np.nanmean(AR))),flush=True)
        agg['AF']+=list(AF);agg['AI']+=list(AI);agg['AR']+=list(AR);agg['A0']+=list(A0);agg['n']+=len(A0)
        agg['pairs'].append([i,int(gdy),int(gdx),len(A0)])
    if agg['n']:
        A0=np.nanmean(agg['A0']);AF=np.nanmean(agg['AF']);AI=np.nanmean(agg['AI']);AR=np.nanmean(agg['AR'])
        rf=(AF-AR)/(A0-AR); ri=(AI-AR)/(A0-AR)
        print('  AGGREGATE %s: N=%d marks over %d pairs  A0=%.2f AF=%.2f AI=%.2f AR=%.2f  retention_frameFixed=%.3f retention_imageLocked=%.3f'%(
          k,agg['n'],len(agg['pairs']),A0,AF,AI,AR,rf,ri))
        res[k]=dict(n=agg['n'],A0=A0,AF=AF,AI=AI,AR=AR,rf=rf,ri=ri,pairs=agg['pairs'])
json.dump(res,open('taskC2.json','w'),indent=1,default=float)
