import numpy as np, json, glob
from scipy.ndimage import median_filter
print('Loop test: SHARP-SPIKE statistic. For each lag k>8, residual = meanNCC(k) - localmedian(meanNCC, +-25 lags).')
print('A looped overlay gives an isolated spike (z_spike >> 8) at the loop period and its multiples.')
for f in sorted(glob.glob('taskBf_*.json')):
    d=json.load(open(f))
    print('== %s (era %d) span %s rect %s'%(d['video'],d['era'],d['span'],d['rect']))
    for nm in d:
        if not isinstance(d[nm],dict) or 'mean' not in d[nm]: continue
        L=np.array(d[nm]['lag']); mn=np.array(d[nm]['mean']); mx=np.array(d[nm]['max'])
        base=median_filter(mn,size=51,mode='nearest')
        r=mn-base
        sel=L>8
        mad=1.4826*np.median(np.abs(r[sel]-np.median(r[sel])))
        z=r/max(mad,1e-9)
        o=np.argsort(-z[sel])[:6]
        print('   %-40s MAD=%.5f  top spikes: %s'%(nm[:40],mad,
          ' '.join('k=%d:z=%.1f'%(L[sel][i],z[sel][i]) for i in o)))
        # count of lags with NCC==1 (bit-identical frames -> freeze, not loop)
        n1=int((mx>0.9999).sum())
        print('        lags with max single-pair NCC>0.9999 (bit-identical frame pairs): %d of %d  %s'%(
          n1,len(L),('e.g. k='+','.join(map(str,L[mx>0.9999][:12]))) if n1 else ''))
