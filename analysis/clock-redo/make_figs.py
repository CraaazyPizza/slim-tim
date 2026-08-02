#!/usr/bin/env python3.12
"""Carousel figures for the 2026-08-02 recovery. Dark theme, readable at phone size."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from datetime import datetime, timedelta
import matplotlib.dates as mdates

OUT="figs/qtecqot-2026-08-02/"
BG="#0d1117"; FG="#e6edf3"; RED="#f85149"; GRN="#3fb950"; AMB="#d29922"; BLU="#58a6ff"
plt.rcParams.update({"figure.facecolor":BG,"axes.facecolor":BG,"text.color":FG,
    "axes.labelcolor":FG,"xtick.color":FG,"ytick.color":FG,"axes.edgecolor":"#30363d",
    "font.size":11,"font.family":"DejaVu Sans"})
def U(s): return datetime.strptime(s,"%Y-%m-%dT%H:%M:%S")

POSTS=[("2026-04-28T05:54:16",0,"first post ever: 'Иван СЕРПО раскрытие'"),
("2026-05-07T06:17:03",0,"a personal name + an image"),("2026-05-25T09:46:14",0,"'upload No.1 complete'"),
("2026-05-25T09:50:36",0,""),("2026-06-14T13:20:43",0,""),("2026-06-14T13:23:30",0,""),
("2026-06-14T13:32:03",0,""),("2026-06-15T04:53:33",0,""),("2026-06-15T04:54:05",0,""),
("2026-07-28T07:18:28",1,"'I am not Ivan0135'"),("2026-07-29T08:18:46",1,"'DMS = Deadman's Switch'"),
("2026-07-31T07:21:01",0,""),("2026-07-31T10:15:58",0,""),("2026-07-31T10:18:24",1,"AI-detector screenshots"),
("2026-07-31T22:33:22",1,""),("2026-08-01T02:09:43",1,""),("2026-08-01T03:37:11",1,"'less than 2% of the cache'"),
("2026-08-01T03:45:49",1,""),("2026-08-02T03:24:49",1,"'Case 28 belongs to tape 5'")]
VID=[("2026-05-25T09:39:42","video 5/8"),("2026-06-15T04:23:35","video 6/8"),("2026-07-24T09:14:05","video 7/8")]

# ---------------- fig 1: what survives
fig,ax=plt.subplots(figsize=(12,5.6))
for s,live,lab in POSTS:
    d=U(s); c=GRN if live else RED
    ax.plot([d,d],[0,1],color=c,lw=3,solid_capstyle="butt",zorder=3)
    if lab:
        ax.annotate(lab,(d,1.06),rotation=38,ha="left",va="bottom",fontsize=8.5,color=c)
for s,lab in VID:
    d=U(s); ax.axvline(d,color=BLU,ls=":",lw=1.6,zorder=1)
    ax.annotate(lab,(d,-0.30),ha="center",fontsize=9,color=BLU,weight="bold")
ax.axvspan(U("2026-05-25T09:39:42"),U("2026-05-25T09:50:36"),color=AMB,alpha=.35,zorder=0)
ax.annotate("3 posts erased\n11 min after\nvideo 5/8 went live",(U("2026-05-25T09:45:00"),1.62),
            ha="center",fontsize=9.5,color=AMB,weight="bold")
ax.set_ylim(-0.45,2.5); ax.set_yticks([])
ax.set_xlim(U("2026-04-24T00:00:00"),U("2026-08-06T00:00:00"))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0,interval=1))
for sp in ("top","right","left"): ax.spines[sp].set_visible(False)
ax.set_title("@qtecqot on X: 19 posts recovered, 11 of them deleted",
             fontsize=15,weight="bold",pad=16,loc="left")
ax.legend(handles=[Patch(color=RED,label="deleted (11)"),Patch(color=GRN,label="still up (8)"),
                   Patch(color=BLU,label="YouTube release")],loc="upper left",
          frameon=False,ncol=3,fontsize=10,bbox_to_anchor=(0,0.99))
fig.text(.01,.015,"Recovered from Wayback captures of Twitter API v2 lookups. "
         "Live/deleted state verified against api.fxtwitter.com and the account's own post counter.",
         fontsize=8,color="#8b949e")
fig.tight_layout(rect=[0,.04,1,1]); fig.savefig(OUT+"1_deletions.png",dpi=155); plt.close(fig)

# ---------------- fig 2: the counter table
fig,ax=plt.subplots(figsize=(10.5,4.4)); ax.axis("off")
rows=[["2026-04-28 05:54","1","0","2",""],["2026-05-07 06:17","2","1","4","names a real outside archive"],
      ["2026-05-25 09:46","3","1","3",""],["2026-05-25 09:50","1","0","3","<- 11 min after video 5/8"]]
tb=ax.table(cellText=rows,colLabels=["author's own counters, at the instant he posted",
    "posts","media","follows",""],cellLoc="left",loc="center",
    colWidths=[.28,.09,.09,.10,.44])
tb.auto_set_font_size(False); tb.set_fontsize(11.5); tb.scale(1,2.0)
for (r,c),cell in tb.get_celld().items():
    cell.set_edgecolor("#30363d"); cell.set_facecolor(BG); cell.get_text().set_color(FG)
    if r==0: cell.get_text().set_weight("bold"); cell.set_facecolor("#161b22")
    if r==4 and c in (1,2): cell.get_text().set_color(RED); cell.get_text().set_weight("bold")
    if r==2 and c in (2,3): cell.get_text().set_color(AMB); cell.get_text().set_weight("bold")
    if c==4: cell.get_text().set_color(AMB)
ax.set_title("The purge is timed to the launch, to the minute",fontsize=15,weight="bold",loc="left",pad=2)
fig.text(.012,.05,"Video 5/8 published 09:39:42 UTC. Six minutes later he announced it. Four minutes after that\n"
    "the counter reads 1 post and 0 media: the trigger post, the named-archive post and the announcement,\n"
    "all gone. He was following 4 accounts on 07 May and 3 by launch.",fontsize=9.5,color="#8b949e")
fig.tight_layout(rect=[0,.20,1,1]); fig.savefig(OUT+"2_counters.png",dpi=155); plt.close(fig)

# ---------------- fig 3: the clock, corrected
import numpy as np
X=[U(s) for s,_,_ in POSTS]
offs=np.arange(-12,12.5,.5)
viol=[sum(1 for a in X if not (7.0 <= ((a+timedelta(hours=o)).hour+(a+timedelta(hours=o)).minute/60) < 24.0)) for o in offs]
fig,ax=plt.subplots(figsize=(11,4.6))
ax.bar(offs,viol,width=.42,color=[GRN if v==0 else ("#8b949e" if v<5 else RED) for v in viol])
for lab,o in (("CEST",2),("Moscow",3),("US Eastern",-4),("US Pacific",-7)):
    i=list(offs).index(o); ax.annotate(f"{lab}\n{viol[i]}",(o,viol[i]+.5),ha="center",fontsize=9.5,
        color=RED,weight="bold")
ax.axvspan(8.25,10.25,color=GRN,alpha=.18)
ax.annotate("only offsets with\nzero acts in the\nsmall hours:\nUTC+8.5 to +10",(9.25,8.6),ha="center",
            fontsize=10,color=GRN,weight="bold")
ax.set_xlabel("candidate UTC offset"); ax.set_ylabel("posts in the local small hours")
ax.set_title("The old time-zone read does not survive the other 17 posts",fontsize=15,weight="bold",loc="left",pad=12)
for sp in ("top","right"): ax.spines[sp].set_visible(False)
fig.text(.01,.015,"Each of the 19 posts rendered as a local time under each offset, counting those outside 07:00-24:00. "
    "The published analysis used 7 acts and reported a clean European morning band. With all 19 it is 7 violations.",
    fontsize=8,color="#8b949e")
fig.tight_layout(rect=[0,.05,1,1]); fig.savefig(OUT+"3_clock.png",dpi=155); plt.close(fig)
print("wrote 3 figures to",OUT)
