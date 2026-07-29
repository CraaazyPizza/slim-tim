import sys,numpy as np
def blur(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
for pre,label in [('analysis/compare-eras/zb','ZB788 2011'),('analysis/compare-eras/rs','RsQCX 2011'),
                  ('analysis/compare-eras/oq','Oqw96 2026'),('analysis/compare-eras/l9','l9RAh 2026')]:
    B=np.load(pre+'_band.npy'); idx=np.load(pre+'_idx.npy'); runs=np.load(pre+'_runs.npy')
    lens=runs[:,1]-runs[:,0]; order=np.argsort(-lens)
    pitches=[];heights=[];widths=[];colh=[];strokes=[];used=[]
    for o in order:
        a,b=runs[o]
        if b-a<10: continue
        m=B[a:b].astype(np.float32).mean(0)
        h=(m-blur(m,20))[4:-4,4:-4]
        P=np.clip(h,0,None)
        if P.max()<=0: continue
        P=P/P.max()
        hh=(P>0.30).sum(0)
        groups=[];cur=None
        for x in range(P.shape[1]):
            if hh[x]>0: cur=[x,x] if cur is None else [cur[0],x]
            else:
                if cur and cur[1]-cur[0]>=5: groups.append(tuple(cur))
                cur=None
        if cur and cur[1]-cur[0]>=5: groups.append(tuple(cur))
        if len(groups)!=11: continue
        # colons must be groups index 5 and 8 in an 11-group '/XX XX:XX:XX' layout
        def cen(g):
            x0,x1=g; sub=P[:,x0:x1+1]; w=sub.sum(0); xs=np.arange(x0,x1+1)
            return float((w*xs).sum()/w.sum())
        g5,g8=groups[5],groups[8]
        w5,w8=g5[1]-g5[0]+1,g8[1]-g8[0]+1
        if not(8<=w5<=20 and 8<=w8<=20): continue
        c5,c8=cen(g5),cen(g8)
        p=(c8-c5)/3.0
        if not(38<p<50): continue
        pitches.append(p); used.append('f%d-%d'%(idx[a],idx[b-1]))
        # digit metrics: groups that are wide (digits)
        dg=[g for i,g in enumerate(groups) if i not in (0,5,8)]
        hs=[];ws=[];st=[]
        for x0,x1 in dg:
            sub=P[:,x0:x1+1]
            sub=sub/sub.max()
            rows=np.nonzero(sub.max(1)>0.5)[0]
            if len(rows)<5: continue
            hs.append(rows.max()-rows.min()+1)
            colsn=np.nonzero(sub.max(0)>0.5)[0]
            ws.append(colsn.max()-colsn.min()+1)
            # stroke width: mean run length of ink along rows
            mask=sub>0.5
            rl=[]
            for r in range(mask.shape[0]):
                run=0
                for v in mask[r]:
                    if v: run+=1
                    else:
                        if run: rl.append(run); run=0
                if run: rl.append(run)
            if rl: st.append(np.median(rl))
        if hs: heights.append(np.mean(hs)); widths.append(np.mean(ws)); strokes.append(np.mean(st))
        for g in (g5,g8):
            sub=P[:,g[0]:g[1]+1]; sub=sub/sub.max()
            rows=np.nonzero(sub.max(1)>0.5)[0]
            if len(rows): colh.append(rows.max()-rows.min()+1)
    def st_(v): 
        v=np.array(v,dtype=float); return '%.3f +/- %.3f (n=%d)'%(v.mean(),v.std(),len(v)) if len(v) else 'n/a'
    print('%-11s pitch=%s'%(label,st_(pitches)))
    print('            digitH=%s  digitW=%s'%(st_(heights),st_(widths)))
    print('            strokeW=%s  colonInkH=%s'%(st_(strokes),st_(colh)))
    print('            runs=%s'%(','.join(used[:12])))
