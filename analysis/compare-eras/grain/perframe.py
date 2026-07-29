import numpy as np
from lib import *
from scipy.ndimage import gaussian_filter, sobel
# windows: near-static camera, live-action content
W={'OpSTlDJWFFI':[(2920,2958),(1120,1158)],
   'Oqw96jCOP7A':[(1250,1290),(1380,1405)],
   'l9RAhmPHM_A':[(2360,2398),(4260,4298),(1460,1498)],
   'ZB788PtqQvg':[(760,798),(1090,1128)],
   'RsQCXN4o4Ps':[(1180,1218),(880,918)],
   'Xju_CY5ZESA':[(900,938)],
   'a6TLGkrfNKI':[(600,638),(1900,1938)]}
print('%-12s %-4s %-13s %8s %8s %8s %8s %8s'%('video','era','window','r_all','r_flat','rho(|r|,|g|)','frozenfrac','flatnoise_ss'))
for k in V:
    y0,y1,x0,x1=PIC[k]
    for (s,e) in W[k]:
        rs=[];rf=[];rho=[];fz=0;ntot=0
        ss=[]
        prev=None
        for i in range(s,e+1):
            a=F(k,i)[y0:y1,x0:x1]
            if prev is not None:
                r=a-prev
                g=np.abs(sobel(gaussian_filter(prev,1.5),0))+np.abs(sobel(gaussian_filter(prev,1.5),1))
                m=g<np.percentile(g,20)
                rs.append(r.std()); rf.append(r[m].std())
                ar=np.abs(r).ravel(); ag=g.ravel()
                rho.append(np.corrcoef(ar,ag)[0,1])
                ntot+=1; fz+= (np.abs(r).mean()<0.05)
            prev=a
        # also: single-frame HP noise in the same flat areas (static+dynamic)
        a=F(k,(s+e)//2)[y0:y1,x0:x1]
        g=np.abs(sobel(gaussian_filter(a,1.5),0))+np.abs(sobel(gaussian_filter(a,1.5),1))
        m=g<np.percentile(g,20)
        hp=a-gaussian_filter(a,8.0)
        print('%-12s %-4d %5d-%5d   %8.4f %8.4f %8.3f %8.3f %8.4f'%(k,ERA[k],s,e,
          np.mean(rs),np.mean(rf),np.nanmean(rho),fz/max(1,ntot),hp[m].std()))
