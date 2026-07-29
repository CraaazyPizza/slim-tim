import pickle,numpy as np
C=pickle.load(open('analysis/compare-eras/clusters.pkl','rb'))
LAB={'zb':['0','2','7','4','5','1','1','3'],'rs':['0','5','2','1'],
     'oq':['0','2','1','5','3','4'],'l9':['2','1','0','8','3','5','4','9','7','9','?']}
NAME={'zb':'ZB788_2011','rs':'RsQCX_2011','oq':'Oqw96_2026','l9':'l9RAh_2026'}
print('Interior-brightness profile of the digit "0" (and "8" for calibration).')
print('Values = mean brightness of the central 34%% of glyph width, per relative height,')
print('normalised so ring brightness (row 8%% of height, full width) = 1.00\n')
for ch in ['0','8']:
    for k in ['zb','rs','oq','l9']:
        cs=[c for i,c in enumerate(C[k]) if i<len(LAB[k]) and LAB[k][i]==ch]
        if not cs: continue
        c=max(cs,key=lambda x:x['n'])
        m=c['mean'].astype(float); m=m/m.max()
        ys,xs=np.nonzero(m>0.25)
        g=m[ys.min():ys.max()+1, xs.min():xs.max()+1]
        H,W=g.shape
        c0=int(W*0.33); c1=int(W*0.67)
        interior=g[:,c0:c1].mean(1)
        ring=g[int(H*0.06):int(H*0.12)+1,:].mean()
        prof=interior/ring
        # sample at 11 relative heights
        idxs=[int(round(H*f)) for f in np.linspace(0.10,0.90,17)]
        s=' '.join('%.2f'%prof[min(H-1,i)] for i in idxs)
        mid=prof[int(H*0.45):int(H*0.56)].mean()
        upq=prof[int(H*0.22):int(H*0.33)].mean()
        loq=prof[int(H*0.67):int(H*0.78)].mean()
        print('%-11s "%s" n=%-3d H=%d W=%d'%(NAME[k],ch,c['n'],H,W))
        print('    profile(h=10%%..90%%): %s'%s)
        print('    interior@mid=%.3f  @upper-quartile=%.3f  @lower-quartile=%.3f   mid/quartiles=%.2f  => %s'%(
            mid,upq,loq,mid/((upq+loq)/2),
            'STROKE CROSSES CENTRE (slashed/barred)' if mid/((upq+loq)/2)>1.6 else 'CENTRE OPEN (plain counter)'))
    print()
