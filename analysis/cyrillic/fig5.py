"""FIG5: free fit vs stem-constrained fit. Points on the diagonal are self-consistent
(the stretch their stroke weight implies is the stretch the image wants). Points far
below the diagonal only fitted the image by adopting a stretch their own stroke weight
contradicts."""
import json, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
P='/home/user/new-skinny-bob/analysis/cyrillic/'
R=json.load(open(P+'sweep3.json'))
nb=[k for k in R if k.startswith('NULL') and R[k]]
if nb:
    nul=max(max(d['r_free'] for d in R[k]) for k in nb); nsrc='+'.join(nb)+', same 361 candidates'
else:
    F=json.load(open(P+'fixpsf.json')); nul=max(d['r'] for d in F['NULL1']); nsrc='fixed-PSF run'
for TAG in ['best5','f983']:
    rows=[d for d in R[TAG] if np.isfinite(d['r_con'])]
    x=np.array([d['r_free'] for d in rows]); y=np.array([d['r_con'] for d in rows])
    isvar=np.array(['#' in d['spec'] for d in rows])
    fig,ax=plt.subplots(figsize=(10.5,8.4),dpi=170)
    ax.plot([0,0.85],[0,0.85],ls='-',lw=1.4,color='0.55',zorder=1)
    ax.text(0.79,0.805,'self-consistent',fontsize=9.5,color='0.4',rotation=42,ha='center')
    ax.scatter(x[~isvar],y[~isvar],s=17,c='0.62',lw=0,zorder=2,label='static faces (%d)'%(~isvar).sum())
    ax.scatter(x[isvar],y[isvar],s=17,c='#8fb8d8',marker='s',lw=0,zorder=2,
               label='variable-font instances (%d)\n(these can meet the stem constraint at SOME weight\nby construction, so only their height matters)'%isvar.sum())
    HL=[('Roboto Medium','#c0392b',(10,-4)),('Inter w600 opsz14','#c0392b',(10,-14)),
        ('Arimo Bold','#2c3e50',(6,6)),('Liberation Sans Bold','#2c3e50',(6,-16)),
        ('Nimbus Sans Bold','#2c3e50',(6,4)),('Go Bold','#2c3e50',(-52,-16)),
        ('Carlito Bold','#2c3e50',(8,-4)),('PT Sans Bold','#8e44ad',(8,4)),
        ('Fira Sans Bold','#8e44ad',(8,-12)),('DejaVu Sans Bold','#2c3e50',(-96,4)),
        ('Open Sans Semibold','#16a085',(9,-4)),('Golos Text w500','#2980b9',(9,-4)),
        ('Montserrat w600','#2980b9',(9,4)),('Rubik w450','#2980b9',(9,-14))]
    d={r['font']:r for r in rows}
    for n,c,off in HL:
        if n not in d: continue
        r=d[n]
        ax.scatter([r['r_free']],[r['r_con']],s=105,facecolor=c,edgecolor='white',lw=1.4,zorder=6)
        ax.annotate(n,(r['r_free'],r['r_con']),textcoords='offset points',xytext=off,
                    fontsize=9.6,color=c,weight='bold',zorder=7)
    ax.axhline(nul,ls='--',lw=1.5,color='0.4',zorder=3)
    ax.text(0.845,nul+0.008,'best any face reaches on a caption-free frame (%s)'%nsrc,
            fontsize=8.4,color='0.35',ha='right')
    ax.axhspan(0,nul,color='0.9',zorder=0)
    ax.set_xlabel('r with the horizontal stretch FREE  (the old test)',fontsize=12.5)
    ax.set_ylabel('r with the stretch FIXED to what the face\'s own stroke weight implies',fontsize=12.5)
    ax.set_title('One face keeps its fit when the stretch is no longer free\nline 1, %s, %d faces and variable-font instances'%(TAG,len(rows)),
                 fontsize=13.5,weight='bold')
    ax.legend(fontsize=8.4,loc='upper left',framealpha=0.95)
    ax.grid(alpha=0.22); ax.set_xlim(0,0.86); ax.set_ylim(0,0.86)
    fig.tight_layout()
    fig.savefig('/home/user/new-skinny-bob/figs/cyrillic/FIG5_stem_constraint_%s.png'%TAG)
    print('FIG5',TAG,'ok  null =',round(nul,4))
