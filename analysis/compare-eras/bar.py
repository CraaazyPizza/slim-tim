import pickle,numpy as np
R=pickle.load(open('analysis/compare-eras/runs.pkl','rb'))
NAME={'zb':('ZB788_2011',440),'rs':('RsQCX_2011',380),'oq':('Oqw96_2026',380),'l9':('l9RAh_2026',340)}
print('Black redaction bar geometry + timecode photometry (band coords -> absolute x)')
for k in ['zb','rs','oq','l9']:
    name,bx=NAME[k]
    B=np.load('analysis/compare-eras/%s_band.npy'%k); runs=np.load('analysis/compare-eras/%s_runs.npy'%k)
    idx=np.load('analysis/compare-eras/%s_idx.npy'%k)
    lens=runs[:,1]-runs[:,0]; order=np.argsort(-lens)
    res=[]
    for oi in order[:14]:
        a,b=runs[oi]
        if b-a<12: continue
        m=B[a:b].astype(np.float32).mean(0)
        # bar = contiguous columns whose whole-column luma is far below the band median
        colmin=m.min(0); colmed=np.median(m,axis=0)
        base=np.median(colmed)
        dark=colmed<base*0.55
        # longest contiguous dark run
        best=(0,None); cur=None
        for x in range(len(dark)):
            if dark[x]: cur=[x,x] if cur is None else [cur[0],x]
            else:
                if cur and cur[1]-cur[0]+1>best[0]: best=(cur[1]-cur[0]+1,tuple(cur))
                cur=None
        if cur and cur[1]-cur[0]+1>best[0]: best=(cur[1]-cur[0]+1,tuple(cur))
        if best[1] is None or best[0]<40: continue
        x0,x1=best[1]
        # vertical extent of the bar
        sub=m[:,x0:x1+1]
        rows=np.nonzero(sub.mean(1)<base*0.6)[0]
        barlum=float(sub.min())
        # timecode ink level vs local background
        res.append((idx[a],idx[b-1],bx+x0,bx+x1,x1-x0+1,(rows.min(),rows.max(),rows.max()-rows.min()+1) if len(rows) else None,barlum,base))
    if not res: print('%-11s no bar detected'%name); continue
    w=np.array([r[4] for r in res]); L=np.array([r[2] for r in res]); Rt=np.array([r[3] for r in res])
    hs=np.array([r[5][2] for r in res if r[5]]); bl=np.array([r[6] for r in res]); bs=np.array([r[7] for r in res])
    print('%-11s n=%d  bar x=%.1f..%.1f  width=%.1f+/-%.1f px  height=%.1f+/-%.1f px'%(name,len(res),L.mean(),Rt.mean(),w.mean(),w.std(),hs.mean() if len(hs) else -1,hs.std() if len(hs) else -1))
    print('             bar luma=%.1f+/-%.1f   local band bg=%.1f+/-%.1f   bar is %.1f%% of bg'%(bl.mean(),bl.std(),bs.mean(),bs.std(),100*bl.mean()/bs.mean()))
