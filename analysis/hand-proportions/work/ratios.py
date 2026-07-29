import numpy as np, json, sys, os
os.chdir('/home/user/new-skinny-bob/analysis/hand-proportions'); sys.path.insert(0,'work')

def ratios(T2,T3,T4,C23,C34):
    T2,T3,T4,C23,C34=[np.array(p,float) for p in (T2,T3,T4,C23,C34)]
    Cm=0.5*(C23+C34)
    n=np.linalg.norm
    L4  = n(T4-C34)          # little digit, from the shared D3|D4 cleft
    L3b = n(T3-C34)          # middle digit, from the SAME cleft
    L3a = n(T3-C23)
    L3  = n(T3-Cm)
    L2  = n(T2-C23)
    Wc  = n(C23-C34)
    d34 = n(T3-T4); d23=n(T2-T3)
    # splay angle between the D3 and D4 axes (tip-to-own-cleft vectors)
    v3=(T3-C34)/L3b; v4=(T4-C34)/L4
    ang=np.degrees(np.arccos(np.clip(np.dot(v3,v4),-1,1)))
    return dict(L4=L4,L3b=L3b,L3a=L3a,L3=L3,L2=L2,Wc=Wc,
                R_shared=L4/L3b, R_own=L4/L3, R_L4Wc=L4/Wc, R_L3Wc=L3/Wc,
                R_tip=d34/d23, d34=d34, d23=d23, splay34=ang,
                R_L2L3=L2/L3)
