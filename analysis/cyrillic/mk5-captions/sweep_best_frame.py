"""
Task 1: sweep every frame 2560-2705, score the caption band by three
independent real metrics, and report a small table. No stacking/averaging is
used as evidence -- the mean-of-caption-frames template exists only as a
yardstick for the leave-one-out NCC score, exactly as specified in the brief.
"""
import numpy as np, json, sys
sys.path.insert(0, '/home/user/new-skinny-bob/analysis/cyrillic/mk5-captions')
from mk5cap_core import get_stack, FRAMES, ROWS, CTRL_ROWS, XRANGE, sl, ncc, OUT

S, FR = get_stack()   # S: (nframes, H, W) uint8-ish float32, cropped to CTRL_ROWS[0]:ROWS[1], XRANGE
idx = {f: i for i, f in enumerate(FR)}

RBAND = sl(ROWS)
RCTRL = sl(CTRL_ROWS)

# caption clearly present per FINDINGS refinement: onset f2603 (abrupt), plateau
# to ~2664, fade over ~35 frames to ~2698. Use 2603-2698 as the CAP set for the
# LOO mean template.
CAP = [f for f in range(2603, 2699) if f in idx]
CAPI = [idx[f] for f in CAP]

def band(i):
    b = S[i][RBAND].astype(np.float64)
    return b - b.mean()

def ctrl(i):
    c = S[i][RCTRL].astype(np.float64)
    return c - c.mean()

MEAN_ALL = S[CAPI][:, RBAND[0], RBAND[1]].mean(0).astype(np.float64)
MEAN_ALL_C = MEAN_ALL - MEAN_ALL.mean()

rows = []
for f in FR:
    i = idx[f]
    b = band(i)
    c = ctrl(i)
    gx = np.gradient(S[i][RBAND].astype(np.float64), axis=1)
    gy = np.gradient(S[i][RBAND].astype(np.float64), axis=0)
    tenengrad = float((gx**2 + gy**2).mean())
    gxc = np.gradient(S[i][RCTRL].astype(np.float64), axis=1)
    gyc = np.gradient(S[i][RCTRL].astype(np.float64), axis=0)
    tenengrad_ctrl = float((gxc**2 + gyc**2).mean())
    rms = float(S[i][RBAND].std())
    rms_ctrl = float(S[i][RCTRL].std())
    if f in CAP:
        loo_sum = MEAN_ALL * len(CAP) - S[i][RBAND[0], RBAND[1]].astype(np.float64)
        loo = loo_sum / (len(CAP) - 1)
        loo_c = loo - loo.mean()
        r_loo = ncc(b, loo_c)
    else:
        r_loo = ncc(b, MEAN_ALL_C)
    rows.append(dict(f=int(f), tenengrad=tenengrad, tenengrad_ctrl=tenengrad_ctrl,
                      tg_ratio=tenengrad/tenengrad_ctrl if tenengrad_ctrl>1e-9 else np.nan,
                      rms=rms, rms_ctrl=rms_ctrl, rms_ratio=rms/rms_ctrl if rms_ctrl>1e-9 else np.nan,
                      r_loo=r_loo, in_cap=(f in CAP)))

rows.sort(key=lambda d: -d['r_loo'])
print('%-6s %6s %9s %9s %7s %7s %7s %5s' % ('frame','r_loo','tenengrad','tg_ratio','rms','rms_c','rms_r','inCAP'))
for d in rows[:20]:
    print('%-6d %6.4f %9.2f %9.3f %7.2f %7.2f %7.3f %5s' % (d['f'], d['r_loo'], d['tenengrad'], d['tg_ratio'], d['rms'], d['rms_ctrl'], d['rms_ratio'], d['in_cap']))
print('...')
for d in rows[-8:]:
    print('%-6d %6.4f %9.2f %9.3f %7.2f %7.2f %7.3f %5s' % (d['f'], d['r_loo'], d['tenengrad'], d['tg_ratio'], d['rms'], d['rms_ctrl'], d['rms_ratio'], d['in_cap']))

json.dump(rows, open(OUT+'sweep_scores.json','w'), indent=1)

# composite rank: average of the three metrics' percentile ranks
import scipy.stats as st
r_loo = np.array([d['r_loo'] for d in rows])
tg = np.array([d['tg_ratio'] for d in rows])
rr = np.array([d['rms_ratio'] for d in rows])
def pct(x):
    return st.rankdata(x)/len(x)
composite = pct(r_loo) + pct(tg) + pct(rr)
best_k = int(np.argmax(composite))
print('\nCOMPOSITE BEST FRAME:', rows[best_k]['f'], 'composite score', composite[best_k])
order = np.argsort(-composite)
print('\nTop 10 by composite (avg percentile of r_loo, tg_ratio, rms_ratio):')
for k in order[:10]:
    d = rows[k]
    print('%-6d composite=%.3f  r_loo=%.4f tg_ratio=%.3f rms_ratio=%.3f inCAP=%s' % (d['f'], composite[k], d['r_loo'], d['tg_ratio'], d['rms_ratio'], d['in_cap']))
