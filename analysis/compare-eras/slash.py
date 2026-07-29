import pickle,numpy as np
C=pickle.load(open('analysis/compare-eras/clusters.pkl','rb'))
LAB={'zb':['0','2','7','4','5','1','1','3'],'rs':['0','5','2','1'],
     'oq':['0','2','1','5','3','4'],'l9':['2','1','0','8','3','5','4','9','7','9','?']}
NAME={'zb':'ZB788_2011','rs':'RsQCX_2011','oq':'Oqw96_2026','l9':'l9RAh_2026'}
print('Slash-vs-dot test on digit "0": x-centroid of interior brightness vs height.')
print('A "/" slash gives x decreasing as y increases (negative slope). A centred dot gives slope ~0.')
print('Calibrated against digit "8" whose mid bar is horizontal (slope ~0).\n')
for ch in ['0','8']:
  for k in ['zb','rs','oq','l9']:
    cs=[c for i,c in enumerate(C[k]) if i<len(LAB[k]) and LAB[k][i]==ch]
    if not cs: continue
    c=max(cs,key=lambda x:x['n'])
    m=c['mean'].astype(float); m=m/m.max()
    ys,xs=np.nonzero(m>0.25)
    g=m[ys.min():ys.max()+1, xs.min():xs.max()+1]
    H,W=g.shape
    # interior = strip away the ring: use columns 28%..72%, rows 25%..75%
    c0,c1=int(W*0.28),int(W*0.72); r0,r1=int(H*0.25),int(H*0.75)
    reg=g[r0:r1,c0:c1].copy()
    reg=reg-np.percentile(reg,20); reg=np.clip(reg,0,None)
    rows=[];cxs=[];wts=[]
    for r in range(reg.shape[0]):
        w=reg[r]
        if w.sum()<=1e-6: continue
        rows.append(r+r0); cxs.append(float((w*np.arange(len(w))).sum()/w.sum())+c0); wts.append(float(w.sum()))
    rows=np.array(rows,float); cxs=np.array(cxs); wts=np.array(wts)
    if len(rows)<8: print(NAME[k],ch,'insufficient'); continue
    # weight by row energy so the slash band dominates
    sel=wts>np.percentile(wts,55)
    A=np.vstack([rows[sel],np.ones(sel.sum())]).T
    coef,res,_,_=np.linalg.lstsq(A,cxs[sel],rcond=None)
    slope=coef[0]
    pred=A@coef; ss=((cxs[sel]-cxs[sel].mean())**2).sum(); r2=1-((cxs[sel]-pred)**2).sum()/max(ss,1e-9)
    ang=np.degrees(np.arctan2(1.0,-slope))  # angle of stroke from horizontal
    print('%-11s "%s" n=%-3d  slope dx/dy=%+.3f  R2=%.3f  => stroke angle %.1f deg from horizontal  (%s)'%(
        NAME[k],ch,c['n'],slope,r2,ang,
        'DIAGONAL "/" slash' if slope<-0.25 else ('DIAGONAL "\\\\"' if slope>0.25 else 'horizontal bar / centred dot')))
  print()
