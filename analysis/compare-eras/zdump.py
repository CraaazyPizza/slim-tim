import pickle,numpy as np
C=pickle.load(open('analysis/compare-eras/clusters.pkl','rb'))
LAB={'zb':['0','2','7','4','5','1','1','3'],'rs':['0','5','2','1'],
     'oq':['0','2','1','5','3','4'],'l9':['2','1','0','8','3','5','4','9','7','9','?']}
NAME={'zb':'ZB788_2011','rs':'RsQCX_2011','oq':'Oqw96_2026','l9':'l9RAh_2026'}
CH='0123456789'
ramp=' .:-=+*#%@'
for k in ['zb','rs','oq','l9']:
    for i,c in enumerate(C[k]):
        if i>=len(LAB[k]) or LAB[k][i]!='0': continue
        m=c['mean'].astype(float); m=m/m.max()
        ys,xs=np.nonzero(m>0.25)
        g=m[ys.min():ys.max()+1, xs.min():xs.max()+1]
        print('==== %s  digit 0  n=%d  shape=%s'%(NAME[k],c['n'],g.shape))
        for r in range(0,g.shape[0],2):
            print('   '+''.join(ramp[min(9,int(v*10))] for v in g[r]))
        break
