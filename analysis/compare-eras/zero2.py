import pickle,numpy as np
C=pickle.load(open('analysis/compare-eras/clusters.pkl','rb'))
LAB={'zb':['0','2','7','4','5','1','1','3'],'rs':['0','5','2','1'],
     'oq':['0','2','1','5','3','4'],'l9':['2','1','0','8','3','5','4','9','7','9','?']}
NAME={'zb':'ZB788_2011','rs':'RsQCX_2011','oq':'Oqw96_2026','l9':'l9RAh_2026'}
def get(k,ch):
    best=None
    for i,c in enumerate(C[k]):
        if i<len(LAB[k]) and LAB[k][i]==ch:
            if best is None or c['n']>best['n']: best=c
    return best
print('=== 0 vs 8 outer-silhouette test (threshold = 50%% of the OUTLINE level, not global max) ===')
for k in ['zb','rs','oq','l9']:
    for ch in ['0','8']:
        c=get(k,ch)
        if c is None: continue
        m=c['mean'].astype(float)
        ys,xs=np.nonzero(m>m.max()*0.25)
        r0,r1,c0,c1=ys.min(),ys.max(),xs.min(),xs.max()
        g=m[r0:r1+1,c0:c1+1]
        # outline level: median of the top-row ink (pure outline, no interior mark)
        toprow=g[1:4].max(0); lvl=np.median(toprow[toprow>toprow.max()*0.4])
        ink=g>lvl*0.5
        H=g.shape[0]
        wid=[]
        for r in range(H):
            x=np.nonzero(ink[r])[0]
            wid.append(x.max()-x.min()+1 if len(x) else 0)
        wid=np.array(wid)
        q1,mid,q3=wid[int(H*0.25)],wid[int(H*0.5)],wid[int(H*0.75)]
        print('  %-11s %s n=%-3d H=%d  outerW @25%%=%2d @50%%=%2d @75%%=%2d   ratio=%.3f  %s'%(
            NAME[k],ch,c['n'],H,q1,mid,q3,mid/((q1+q3)/2),
            'no waist -> ZERO' if mid/((q1+q3)/2)>0.95 else 'waist -> EIGHT'))
print()
print('=== zero interior mark: match against ideal SLASH / HORIZ-BAR / CENTRE-DOT models ===')
def models(H,W):
    ys,xs=np.mgrid[0:H,0:W]
    yn=(ys-(H-1)/2)/max(1,(H-1)/2); xn=(xs-(W-1)/2)/max(1,(W-1)/2)
    out={}
    # slash: bright where |y + x*k| small  (lower-left to upper-right => y = -x)
    out['slash_/']=np.exp(-((yn+xn)**2)/(2*0.28**2))
    out['slash_\\']=np.exp(-((yn-xn)**2)/(2*0.28**2))
    out['horiz_bar']=np.exp(-(yn**2)/(2*0.28**2))
    out['centre_dot']=np.exp(-((yn**2+xn**2))/(2*0.35**2))
    out['vert_bar']=np.exp(-(xn**2)/(2*0.28**2))
    return out
for k in ['zb','rs','oq','l9']:
    c=get(k,'0')
    if c is None: continue
    m=c['mean'].astype(float)
    ys,xs=np.nonzero(m>m.max()*0.25)
    r0,r1,c0,c1=ys.min(),ys.max(),xs.min(),xs.max()
    g=m[r0:r1+1,c0:c1+1]
    toprow=g[1:4].max(0); lvl=np.median(toprow[toprow>toprow.max()*0.4])
    # stroke width from top outline thickness
    colmid=g[:,g.shape[1]//2]
    sw=int(max(3,round((colmid>lvl*0.5).sum()/2)))
    pad=sw+1
    inner=g[pad:g.shape[0]-pad, pad:g.shape[1]-pad]
    if inner.size<40: print(NAME[k],'inner too small'); continue
    z=inner-inner.mean()
    M=models(*inner.shape)
    sc={}
    for nm,mod in M.items():
        mo=mod-mod.mean()
        d=np.sqrt((z*z).sum()*(mo*mo).sum())
        sc[nm]=float((z*mo).sum()/d) if d>0 else 0
    order=sorted(sc.items(),key=lambda t:-t[1])
    print('  %-11s n=%-3d inner=%dx%d strokeW~%d  best=%s'%(NAME[k],c['n'],inner.shape[0],inner.shape[1],sw,order[0][0]))
    print('        '+'  '.join('%s=%+.3f'%(nm,v) for nm,v in sorted(sc.items(),key=lambda t:-t[1])))
