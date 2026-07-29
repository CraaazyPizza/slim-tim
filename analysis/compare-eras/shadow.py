import pickle,numpy as np
R=pickle.load(open('analysis/compare-eras/runs.pkl','rb'))
import numpy as np
NAME={'zb':'ZB788_2011','rs':'RsQCX_2011','oq':'Oqw96_2026','l9':'l9RAh_2026'}
def blur1(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
print('Timecode overlay photometry: ink polarity, contrast, and dark-lobe (shadow/outline) geometry')
for k in ['zb','rs','oq','l9']:
    B=np.load('analysis/compare-eras/%s_band.npy'%k); runs=np.load('analysis/compare-eras/%s_runs.npy'%k)
    idx=np.load('analysis/compare-eras/%s_idx.npy'%k)
    lens=runs[:,1]-runs[:,0]; order=np.argsort(-lens)
    inkc=[];shx=[];shy=[];ratio=[]
    for oi in order[:12]:
        a,b=runs[oi]
        if b-a<12: continue
        m=B[a:b].astype(np.float32).mean(0)
        bg=blur1(m,25)
        h=m-bg
        pos=np.clip(h,0,None); neg=np.clip(-h,0,None)
        if pos.max()<2: continue
        # ink mask = strong positive
        mk=pos>pos.max()*0.5
        if mk.sum()<200: continue
        inkc.append(float((m[mk]-bg[mk]).mean()))
        ratio.append(float(neg.sum()/pos.sum()))
        ys,xs=np.nonzero(mk); pc=(ys.mean(),xs.mean())
        nk=neg>neg.max()*0.5
        if nk.sum()>100:
            ys2,xs2=np.nonzero(nk); nc=(ys2.mean(),xs2.mean())
            shy.append(nc[0]-pc[0]); shx.append(nc[1]-pc[1])
    def s(v): 
        v=np.array(v,float); return '%+.2f +/- %.2f (n=%d)'%(v.mean(),v.std(),len(v)) if len(v) else 'n/a'
    print('%-11s ink-above-bg = %s DN'%(NAME[k],s(inkc)))
    print('            dark-lobe/bright-lobe energy ratio = %s'%s(ratio))
    print('            dark-lobe centroid offset from ink: dx=%s  dy=%s'%(s(shx),s(shy)))
