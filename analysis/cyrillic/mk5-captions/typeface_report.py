import json, numpy as np
OUT = '/home/user/new-skinny-bob/analysis/cyrillic/mk5-captions/'
rows = json.load(open(OUT+'typeface_stage1.json'))
rows.sort(key=lambda d: -d['r'])
print('n fonts fit:', len(rows))
print('%-45s %7s %5s %5s %6s' % ('font','r','cap','size','kx'))
for d in rows[:40]:
    print('%-45s %7.4f %5d %5d %6.2f' % (d['font'][:45], d['r'], d['cap'], d['size'], d['kx']))

rs = np.array([d['r'] for d in rows])
kxs = np.array([d['kx'] for d in rows])
print('\nr distribution: min=%.4f p25=%.4f median=%.4f p75=%.4f max=%.4f'%(rs.min(),np.percentile(rs,25),np.median(rs),np.percentile(rs,75),rs.max()))
print('top-20 kx values:', kxs[:20])
print('top-20 kx mean=%.3f std=%.3f'%(kxs[:20].mean(), kxs[:20].std()))
print('all kx mean=%.3f std=%.3f'%(kxs.mean(), kxs.std()))

# does r separate meaningfully from the field, or is top a tie?
top = rs[0]; rest = rs[1:]
print('\ntop r=%.4f; #fonts within 0.01 of top: %d; within 0.02: %d; within 0.05: %d (of %d)'%(
    top, (rs>=top-0.01).sum(), (rs>=top-0.02).sum(), (rs>=top-0.05).sum(), len(rs)))
