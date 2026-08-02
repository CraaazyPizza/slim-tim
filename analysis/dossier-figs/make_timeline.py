#!/usr/bin/env python3.12
"""Rebuild figs/qtecqot/timeline.png.

The original read "Nine acts in fourteen weeks, 2026-04-22 to 2026-07-29" and showed two
tweets, because two tweets were all that was visible. The recovery of 11 deleted posts
and the watcher's live capture since take the count to 29 acts, of which 21 are posts.

Post list comes from acts.py, which derives it from raw/ rather than hardcoding it. The
original figure hardcoded its list, which is how three figures ended up saying 19 after
he posted his 20th and 21st.

No script made the original. This reconstructs its design from the image, so treat small
styling differences as expected. The original is at
figs/qtecqot/withdrawn/timeline_9acts_2026-07-29_SUPERSEDED.png.

Run from anywhere: python3.12 analysis/dossier-figs/make_timeline.py
"""
import os
import sys
import re
import textwrap
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from acts import (ROOT, DESC_EDIT, SCREENSHOT_ONLY, VIDEOS,  # noqa: E402
                  X_ACCOUNT_CREATED, YT_CHANNEL_CREATED, posts)

OUT = os.path.join(ROOT, "figs/qtecqot/timeline.png")

FG, DIM, RULE = "#1a1a1a", "#6b6b6b", "#d8d8d8"
BLUE, REDD, AMBER, PURPLE, DEAD = "#2f6fc4", "#c0392b", "#c8901e", "#8e6bb5", "#c0392b"

# Hand-written notes for the acts that carry meaning. Posts not listed here get their own
# first line of text, truncated. Keyed by "YYYY-MM-DDTHH:MM:SS".
def strip_emoji(t):
    """DejaVu Sans has no glyphs for his blue-diamond bullets, so they rendered as tofu."""
    return re.sub(r"\s+", " ", re.sub(r"[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F]", "", t)).strip()


def strip_handles(t):
    """Drop the leading @mentions X prepends to a reply.

    They are not something he typed, and this figure is published: AGENTS.md says never
    name a private individual, and a reply's verbatim text carries the addressee's handle
    into the image where no grep pass would ever find it. Who he replies to is described
    by role in the dossier instead.
    """
    return re.sub(r"^(?:RT\s+)?(?:@\w+[\s,:]*)+", "", t).strip()


NOTES = {
    "2026-04-28T05:54:16": "First post ever. Names СЕРПО, in Russian",
    "2026-05-07T06:17:03": "Names Valerijs Černohajev, with a photo the CDN has since purged",
    "2026-05-25T09:46:14": "“upload No.1 complete”",
    "2026-05-25T09:50:36": "Reworded, and by now the first three posts are gone",
    "2026-07-28T07:18:28": "“I am not Ivan0135… DMS in use, unlike 0135”",
    "2026-07-29T08:18:46": "“Clarification: DMS = Deadman's Switch”",
    "2026-06-14T13:23:30": "“he is confirmed real. continuation of series on my Youtube. "
                           "There are others survivors”",
    "2026-07-31T07:21:01": "A “SKINNY BOB FACTS” thread by a self-described former "
                           "intelligence analyst. Reposted, then deleted",
    "2026-07-31T10:18:24": "Two AI-detector screenshots, reading 5% and 0%",
    "2026-08-01T02:09:43": "The same thread again, reposted a second time and left up",
    "2026-07-31T22:33:22": "An emoji, nothing else — his shortest post",
    "2026-08-01T03:37:11": "“less than 2% of the network's cache of materials”",
    "2026-08-02T03:24:49": "“Case 28 belongs to tape 5, not tape 4” — agrees with our ledger",
    "2026-08-02T13:05:32": "“7 tapes… tape 01 case 01 to tape 07 case 40. A minor indexing error in 2011”",
    "2026-08-02T13:12:34": "“the next release will contain content from Tape 7 and will be in color”",
}


LABEL = {"original": "Post", "reply": "Reply to another account",
         "self-reply": "Reply on his own thread", "repost": "Repost of another account"}


def build():
    rows = []
    rows.append((YT_CHANNEL_CREATED, "reg", "YouTube channel created",
                 "UCw1EA-KJud9OmMA5p7_MWgw", "second"))
    rows.append((X_ACCOUNT_CREATED, "reg", "X account @qtecqot created",
                 "empty bio, empty location, default avatar", "millisecond"))
    for ts, vid, label, secs in VIDEOS:
        rows.append((ts, "vid", f"{label} published — {vid}", f"{secs} s", "second"))
    rows.append((DESC_EDIT, "edit", "Video 3 description edited",
                 "adds the “Official venue” block and the x.com/qtecqot link", "second"))
    for ts, sid, text, is_live, (k, _to) in posts():
        key = ts.strftime("%Y-%m-%dT%H:%M:%S")
        note = NOTES.get(key) or strip_handles(strip_emoji(text))
        kind = "post" if is_live else "gone"
        # A reader on Reddit read the old figure as covering only his originals, because
        # every row said "Post" and nothing said otherwise. Seven of these are replies.
        rows.append((ts, kind, LABEL[k] + ("" if is_live else ", since deleted"), note, sid))
    # The two YouTube comments cannot be resolved to an instant. Placed at the midpoint of
    # their window and drawn hollow, exactly as the original did for its unresolved tweet.
    #
    # Shown as two rows, not one. They are not the same kind of act: one is a top-level
    # comment and the other is a nested reply carrying the single most load-bearing
    # sentence he has written. Collapsing them to "Two YouTube comments" hid that, the
    # same way 22 rows reading "Post" hid the X replies.
    rows.append((datetime(2026, 5, 28, 12, 0, 0), "cmt", "YouTube comment, top level",
                 "“Continuation of series:” and a link to video 5, on ivan0135's "
                 "RsQCXN4o4Ps. 6 likes", "3-day window"))
    rows.append((datetime(2026, 5, 28, 12, 1, 0), "cmt",
                 "YouTube comment, nested reply — the one that decoded the counter",
                 "“5 of 8 completed.” Nested under a stranger's plea, so invisible in "
                 "newest-first sort", "3-day window"))
    # The one post with no machine record. posts() cannot see it, so it is added by hand.
    rows.extend(SCREENSHOT_ONLY)
    return sorted(rows)


ROWS = build()
n_posts = sum(1 for r in ROWS if r[1] in ("post", "gone", "post-gone"))
n_gone = sum(1 for r in ROWS if r[1] in ("gone", "post-gone"))

STYLE = {"reg": (BLUE, "o"), "vid": (REDD, "o"), "edit": (AMBER, "o"),
         "post": (FG, "s"), "gone": (DEAD, "s"), "cmt": (PURPLE, "o"),
         "post-gone": (DEAD, "s")}
# Kinds whose instant is a window, not a timestamp. Drawn hollow.
HOLLOW = {"cmt", "post-gone"}

RH = 0.46                       # inches per row
# 2.55 gave the subtitle one line, and the composition of the 22 posts does not fit on
# one line at this width — it ran off the right edge. 0.30 in more header, two lines.
H = 2.85 + RH * len(ROWS)
fig = plt.figure(figsize=(15.0, H), dpi=140, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)


def fy(row_i):
    """Row index -> figure y."""
    return 1 - (1.72 + RH * (row_i + 0.5)) / H


ax.text(.035, 1 - 0.36 / H, "Every public act by qtecqot", fontsize=25,
        weight="bold", color=FG, va="center")
KINDS = [p[4][0] for p in posts()]
n_reply = sum(1 for k in KINDS if k in ("reply", "self-reply"))
n_other = sum(1 for k in KINDS if k == "reply")
n_rt = sum(1 for k in KINDS if k == "repost")
n_orig = n_posts - n_reply - n_rt

ax.text(.035, 1 - 0.66 / H,
        f"{len(ROWS)} acts, 2026-04-22 to {ROWS[-1][0]:%Y-%m-%d}, "
        f"of which {n_posts} are X posts and {n_gone} of those he deleted.\n"
        f"Replies are in: {n_orig} originals, {n_reply} replies of which {n_other} to "
        f"another account, {n_rt} reposts.   Hollow marker = timestamp not machine-read.",
        fontsize=12.5, color=DIM, va="top", linespacing=1.5)

for x, lab in ((.108, "date"), (.196, "UTC"), (.284, "act")):
    ax.text(x, 1 - 1.46 / H, lab, fontsize=11, color=DIM, va="center")
ax.text(.965, 1 - 1.46 / H, "precision", fontsize=11, color=DIM, va="center", ha="right")
ax.plot([.030, .965], [1 - 1.60 / H] * 2, color="#b0b0b0", lw=.9)

SPINE = .266
ax.plot([SPINE, SPINE], [fy(0) + .012, fy(len(ROWS) - 1) - .012], color="#222222", lw=1.6,
        zorder=1)

for i, (ts, kind, title, note, extra) in enumerate(ROWS):
    y = fy(i)
    colour, marker = STYLE[kind]
    hollow = kind in HOLLOW
    if i:
        ax.plot([.030, .965], [y + RH / H / 2] * 2, color=RULE, lw=.5, zorder=0)

    datestr = "27–29 May" if kind == "cmt" else f"{ts:%d %b}"
    ax.text(.180, y, datestr, fontsize=12, weight="bold", color=FG,
            ha="right", va="center")
    stamp = "unresolved" if kind in HOLLOW else f"{ts:%H:%M:%S}"
    ax.text(.252, y, stamp, fontsize=11.5, color=DIM, va="center", ha="right",
            family="DejaVu Sans Mono")
    ax.plot([SPINE], [y], marker=marker, ms=(8.5 if marker == "o" else 7.5),
            color=("white" if hollow else colour), mec=colour, mew=1.8, zorder=3)

    ax.text(.284, y + .0062, title, fontsize=12.5, weight="bold",
            color=(DEAD if kind == "gone" else FG), va="center")
    ax.text(.284, y - .0082, textwrap.shorten(note, 92, placeholder="…"), fontsize=11,
            color=DIM, va="center")
    prec = extra if kind in ("reg", "vid", "edit", "cmt", "post-gone") else "millisecond"
    ax.text(.965, y, prec, fontsize=10.5, color=DIM, va="center", ha="right",
            style="italic")

# The two annotations the original carried, both still true.
i_yt = next(i for i, r in enumerate(ROWS) if r[0] == YT_CHANNEL_CREATED)
i_x = next(i for i, r in enumerate(ROWS) if r[0] == X_ACCOUNT_CREATED)
ax.annotate("", xy=(.104, fy(i_yt)), xytext=(.104, fy(i_x)),
            arrowprops=dict(arrowstyle="<->", color="#1a7f5a", lw=1.4))
ax.text(.096, (fy(i_yt) + fy(i_x)) / 2, "6 days apart,\n181 s apart in\ntime-of-day",
        fontsize=10, weight="bold", color="#1a7f5a", ha="right", va="center",
        linespacing=1.5)

i_ed = next(i for i, r in enumerate(ROWS) if r[0] == DESC_EDIT)
ax.annotate("", xy=(.104, fy(i_ed)), xytext=(.104, fy(i_ed + 1)),
            arrowprops=dict(arrowstyle="<->", color=AMBER, lw=1.4))
ax.text(.096, (fy(i_ed) + fy(i_ed + 1)) / 2, "11 minutes", fontsize=10.5, weight="bold",
        color=AMBER, ha="right", va="center")

# What a reader should not assume is here. Asked directly whether the figure holds
# "literally everything", the answer is no, and the gaps are worth printing on it.
fig.text(.030, 0.62 / H,
         "Not on this figure, and not because they are unimportant:  "
         "the 12 deletions themselves — only two are datable, the 25 May purge and the "
         "02 Aug one above, the rest are known only as “gone by” a later check.  "
         "Follow and unfollow events — the follow counter moved 2 to 4 to 3 across the "
         "first three posts and those changes are recorded per-post in PROVENANCE.md, "
         "not as instants.  Profile edits, likes, and anything X does not expose "
         "logged out.",
         fontsize=10, color=DIM, va="center", wrap=True)

fig.savefig(OUT, facecolor="white")
plt.close(fig)
print(f"wrote {OUT}: {len(ROWS)} acts, {n_posts} posts, {n_gone} deleted")
