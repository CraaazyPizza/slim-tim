import numpy as np, json, sys
from lib import *
from taskC_detect2 import detect
from scipy.ndimage import gaussian_filter, shift as ndshift
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
def track(hp0,hp1,cy,cx,half=20,srch=45):
    y,x=int(round(cy)),int(round(cx))
    if y-half<0 or x-half<0 or y+half+1>hp0.shape[0] or x+half+1>hp0.shape[1]: return None
    t=hp0[y-half:y+half+1,x-half:x+half+1]
    t=t-t.mean(); tn=np.linalg.norm(t)
    if tn<1e-6: return None
    best=(-2,0,0); vals={}
    for dy in range(-srch,srch+1):
        for dx in range(-srch,srch+1):
            yy=y+dy; xx=x+dx
            if yy-half<0 or xx-half<0 or yy+half+1>hp1.shape[0] or xx+half+1>hp1.shape[1]: continue
            q=hp1[yy-half:yy+half+1,xx-half:xx+half+1]
            q=q-q.mean(); qn=np.linalg.norm(q)
            if qn<1e-6: continue
            v=float((t*q).sum()/(tn*qn))
            vals[(dy,dx)]=v
            if v>best[0]: best=(v,dy,dx)
    return best,vals
MOT=json.load(open('motion.json'))
NPAIR=6
res={}
for k in ['OpSTlDJWFFI','Oqw96jCOP7A','l9RAhmPHM_A','ZB788PtqQvg','RsQCXN4o4Ps']:
    y0,y1,x0,x1=PIC[k]
    cand=[m for m in MOT[k] if 8<max(abs(m[1]),abs(m[2]))<38][:40]
    used=[]; rows=[]
    print('==== %s era%d'%(k,ERA[k]),flush=True)
    for m in cand:
        if len(used)>=NPAIR: break
        i=m[0]
        if any(abs(i-u)<8 for u in used): continue
        a=F(k,i)[y0:y1,x0:x1]; b=F(k,i+1)[y0:y1,x0:x1]
        gdy,gdx,pk=phasecorr(a,b)
        if max(abs(gdy),abs(gdx))<6 or max(abs(gdy),abs(gdx))>40: continue
        hp0=a-gaussian_filter(a,5.0); hp1=b-gaussian_filter(b,5.0)
        mk=[x for x in detect(a,amp=8.0,size=13,minpx=8,maxpx=1500)]
        # keep marks on locally flat background: low std of blurred image nearby
        lo=gaussian_filter(a,5.0)
        sel=[]
        for pol,cy,cx,npx,pkk,h,w in mk:
            yy,xx=int(cy),int(cx)
            if yy<30 or xx<30 or yy>a.shape[0]-30 or xx>a.shape[1]-30: continue
            loc=lo[yy-25:yy+26,xx-25:xx+26]
            if loc.std()>4.0: continue
            sel.append((pol,cy,cx,npx,pkk))
        sel=sorted(sel,key=lambda t:-t[4])[:25]
        n0=n_img=n_amb=0; dlist=[]
        for pol,cy,cx,npx,pkk in sel:
            r=track(hp0,hp1,cy,cx)
            if r is None: continue
            (v,dy,dx),vals=r
            v0=vals.get((0,0),-2); vg=vals.get((int(round(gdy)),int(round(gdx))),-2)
            # also allow +-1 tolerance around each hypothesis
            v0=max([vals.get((yy,xx),-2) for yy in(-1,0,1) for xx in(-1,0,1)])
            vg=max([vals.get((int(round(gdy))+yy,int(round(gdx))+xx),-2) for yy in(-1,0,1) for xx in(-1,0,1)])
            dlist.append((dy,dx,v,v0,vg,pkk))
            if v<0.35: n_amb+=1
            elif abs(dy)<=2 and abs(dx)<=2: n0+=1
            elif abs(dy-gdy)<=3 and abs(dx-gdx)<=3: n_img+=1
            else: n_amb+=1
        if len(dlist)<5: continue
        used.append(i)
        v0m=np.median([d[3] for d in dlist]); vgm=np.median([d[4] for d in dlist])
        print('  pair f%05d->f%05d global(dy,dx)=(%+d,%+d) pcpk=%.3f  marks tracked=%d | frame-fixed=%d image-locked=%d ambig=%d | medNCC@zero=%.3f medNCC@global=%.3f'%(
          i,i+1,gdy,gdx,pk,len(dlist),n0,n_img,n_amb,v0m,vgm),flush=True)
        rows.append(dict(f=i,g=[int(gdy),int(gdx)],n=len(dlist),zero=n0,img=n_img,amb=n_amb,v0=float(v0m),vg=float(vgm),
                         disp=[[int(d[0]),int(d[1]),float(d[2])] for d in dlist]))
    res[k]=rows
    if rows:
        tz=sum(r['zero'] for r in rows); ti=sum(r['img'] for r in rows); ta=sum(r['amb'] for r in rows)
        print('  TOTAL %s: frame-fixed=%d image-locked=%d ambiguous=%d  -> image-locked frac of decided = %.3f'%(k,tz,ti,ta, ti/max(1,ti+tz)))
json.dump(res,open('taskC.json','w'),indent=1)
