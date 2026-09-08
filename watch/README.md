# Monitor operation and publication

The public `main` checkout contains code, reports, and reviewed evidence snapshots.
Continuous capture runs in a separate sibling worktree on the local-only
`local/capture` branch. This keeps scheduled capture writes and automatic commits
out of the checkout used to review and publish research.

On the research machine, the capture checkout is `../new-skinny-bob-capture`.
Its cron jobs run the YouTube watcher every 30 minutes, the X watcher every two
minutes, an hourly full X sweep, and the keeper hourly and at boot. The local
viewer at `http://127.0.0.1:8765/timeline/` serves that checkout's current archive.
Run `python3.12 watch/doctor.py` there to check the capture stack.

## What the archive actually holds

Open **http://127.0.0.1:8765/timeline/** on the research machine. The coverage panel
shows the last complete X enumeration, current capture errors, and all known YouTube
videos. Each X entry has source records and reply/quote context. Each YouTube entry
links to its description, metadata, held video and readable comment snapshot.
The public website is a separately reviewed snapshot; its review date is displayed.
An automatic local commit does not update that website or GitHub's `main` files.

| Surface | Preservation and interval |
|---|---|
| X posts, replies, reposts | Official API every two minutes; every delta page is drained before advancing the cursor. Each received page and per-post record is saved before requesting the next page. Full available timeline hourly; recent edit probe every ten minutes. |
| X attachments and context | Download on capture, retry sweep hourly. `x/assets/` maps source URLs to files, retrieval dates, SHA-256 and failures. `x/media/` uses content hashes. Reply/quote media has a separate context owner. Original legacy files remain held; their enumeration-based names do not establish which URL they came from. |
| X profile and following | Profile response/revisions plus avatar and banner files. Sampled counter history. Full public following list hourly and when its counter changes. Pinned-post metadata is requested from the API. |
| YouTube | Raw RSS every 30 minutes, plus watch-page HTML, player responses, description revisions and thumbnails for every qtecqot video ever seen. Best available AVC/audio download, falling back to another available codec. Previously captured AVC corpus files are indexed with their historical source, without pretending they were downloaded again. |
| YouTube comments | Daily extraction including replies when exposed; raw extractor JSON plus a readable local HTML snapshot. Failures retry after six hours, or immediately with `--retry`. |

`youtube/index.json` records each component's success or error. A login page is
retained as a failed observation, never accepted as a captured video. A failed RSS
request retains the last successful channel state for the next comparison.
A mirror 404 records **unavailability**, not a verified deletion. Existing historical
deletion annotations remain in the archive with their original evidence.

This is an archive of observable public material, not a guarantee that every action
was observed. Posts removed between polls can escape capture. Private likes and DMs
are unavailable. Instagram is not configured: an account must be linked to the
uploader before its material can be attributed here. YouTube can omit deleted,
filtered or otherwise unexposed comments even when extraction completes.

The capture machine uses the standalone `uv`-managed `yt-dlp` tool (2026.8.19 at the
September 8 repair). YouTube cookies, when available, live outside the repositories
at `~/.config/qtecqot-watch/youtube-cookies.txt`, mode 600; `YOUTUBE_COOKIES_FILE`
overrides that location. The fourth video's media/comments currently require an
age-verified session. After refreshing the session, run:

```bash
cd ../new-skinny-bob-capture
python3.12 watch/watch.py --quiet --commit --retry
python3.12 watch/doctor.py
```

Regression checks run without credentials or live requests:
`python3.12 -m unittest discover -s watch -p 'test*.py'`.

## What gets backed up

X content/profile/availability events are checkpointed immediately on `local/capture`;
routine observations are batched into hourly checkpoints. X commits include only
`watch/x`, leaving unrelated staged changes alone. YouTube's `--commit` checkpoints
only `watch/youtube`, `watch/snapshots`, `watch/latest.json`, and `watch/CHANGELOG.md`.
The existing home-directory Drive mirror covers both worktrees and their shared
Git objects. A local Git commit alone is not an off-machine backup.

The September 8 cleanup preserved the previous history under
`backup/pre-cleanup-2026-09-08` and saved a separate private recovery directory
under `~/research-backups/qtec-cleanup-2026-09-08`. No capture-history branch was
pushed to GitHub and no published history was rewritten.

## Publishing reviewed work

Work on code and reports in `main`. Review individual captures before copying
them from the capture checkout. Do not merge or push the entire capture branch:
it contains unreviewed source records and media. The keeper refuses publication
from any branch other than `main`; the local capture branch also has a disabled
push destination configured on this machine.

For the timeline website, edit `timeline/publication.json` only after reviewing
the selected entries and media. Run `python3.12 watch/build_public_site.py` with
a new output directory. The builder remains restricted to that inclusion list.
For domain research, use the explicit file list in
[`PUBLICATION-MANIFEST.json`](../analysis/domain-qtecqot/PUBLICATION-MANIFEST.json).
Unselected captures in that directory and the original desktop screenshot stay
local and ignored; tracked reviewed files remain visible to Git.

Update watcher code in the capture worktree explicitly after testing changes in
`main`; a worktree has its own checked-out code. Credentials remain in the existing
user configuration, outside both repositories' tracked files.

## Keeper details

The keeper resolves its repository from its own location and uses Git's worktree
path resolution for the optional `qtecqot-no-autopush` hold file. To hold publication
on `main`, create the path returned by `git rev-parse --git-path qtecqot-no-autopush`.
The viewer process must close file descriptor 9 when launched: otherwise it
inherits the keeper lock and blocks every later keeper run while it remains open.
