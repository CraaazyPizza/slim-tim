# Dossier figure scripts

The three figures in `figs/qtecqot/` that `reports/agent_qtecqot_dossier.md` embeds. Unlike
most of `analysis/`, **these do rerun**, from any working directory, with no absolute paths:

```bash
python3.12 analysis/dossier-figs/acts.py            # print the act list, check nothing
python3.12 analysis/dossier-figs/make_timeline.py   # -> figs/qtecqot/timeline.png
python3.12 analysis/dossier-figs/make_counter.py    # -> figs/qtecqot/counter.png
python3.12 analysis/clock-redo/make_dossier_clock.py  # -> figs/qtecqot/clock.png
```

The clock one lives in `analysis/clock-redo/` next to the recompute it came out of, but it
imports `acts.py` from here, so all three read the same list.

## acts.py is the point

Every one of these figures used to carry its own typed copy of qtecqot's post timestamps.
On 2026-08-02 he posted twice more, the watcher captured both, and all three figures went
on printing **19** while `raw/` held 21. No single script was wrong. The duplication was.

`acts.py` reads `qtecqot-x-recovered/raw/` and `watch/x/raw/` at run time, so a new post
propagates by rerunning rather than by someone remembering which files to edit. Two things
it does that a naive glob does not:

- **Filters out other people's posts.** `watch/x/raw/` holds records he reposted, which
  carry the original author's handle. `2082824913815998748` is Eddie Abbott's thread.
  Counting it would have given 22 instead of 21.
- **Takes his text, not the longest text.** A reply record contains what it replies to and
  a repost record contains the whole reposted thread, both longer than anything he writes.
  Taking the longest string attributed a stranger's reply to him in the first draft.

## Where derivation stops

`posts()` is only as complete as `raw/`, and one real post is not in `raw/` at all: the
"Fake copycat channel" card of 2026-08-02, deleted within the hour, with no status ID, no
Wayback capture, no fxtwitter record and no `x_search` hit. A browser screenshot is the only
copy that exists. It is listed by hand in `acts.py` as `SCREENSHOT_ONLY` and drawn hollow.

So the current totals are **29 acts, 22 posts, 12 deleted**.

## What the timeline still does not show

Printed on the figure itself, and repeated here because it is the honest limit:

- **The deletions.** Twelve posts are marked deleted, but the deletion *events* are not
  plotted. Only two are datable: the 25 May purge, where three posts vanished inside four
  minutes, and the 02 Aug copycat post. For the rest we know only "gone by" some later check.
- **Follows and unfollows.** The follow counter moved 2 to 4 to 3 across the first three
  posts. Those are recorded per-post in `PROVENANCE.md` as counter states, not as instants,
  so they cannot be placed on a time axis.
- **Profile edits, likes, and anything X does not expose to a logged-out reader.**

## Reconstruction, not recovery

No script in this repo ever generated the original `timeline.png`, `counter.png` or
`clock.png`. They arrived in the initial commit as PNGs. These scripts rebuild that design
from the images, so small styling differences are expected. Every original is preserved
byte-identical under `figs/qtecqot/withdrawn/`.

`figs/qtecqot-2026-08-02/` is deliberately **not** regenerated. That carousel is what was
published to Reddit at n=19, and it is left standing as the record of what was posted.
