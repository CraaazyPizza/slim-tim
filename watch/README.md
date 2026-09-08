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

## What gets backed up

X captures are checkpointed on `local/capture`; automatic commits include only
`watch/x`, leaving unrelated staged changes alone. YouTube snapshots and rolling
state remain in the capture checkout and can be checkpointed there separately.
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
