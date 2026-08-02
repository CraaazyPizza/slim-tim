#!/usr/bin/env bash
#
# Keeper for the @qtecqot watcher. Answers one question: if this box dies, what is lost?
#
# The watcher itself (watch/xwatch.py, */2 in cron) captures posts before they are
# deleted. Three things have to hold for that to still mean something tomorrow:
#
#   1. the schedule survives a rebuild   -- already handled, see "Not here" below
#   2. cron is actually running          -- ensure_cron
#   3. the captures leave this disk      -- flush, and it is the one that was missing
#
# On (3): xwatch --commit commits to the local repo and stops there. Its own docstring
# said "get the capture off this box", which was not true -- nothing pushed. Between
# manual pushes every capture lived on one disk, and the material this watcher exists
# to catch is material that exists nowhere else. The 2026-08-02 copycat post is the
# proof: deleted inside an hour, absent from Wayback, fxtwitter and x_search, and the
# only copy in the world is a screenshot in this repo.
#
# Also (4): a job that fires every two minutes and fails every time looks identical to
# a job that has nothing to do. check_health prints the difference.
#
# Not here, on purpose:
#
#   * Reinstalling the crontab. stateDevMachine/autopush.sh already snapshots the live
#     crontab hourly into system/crontab.txt, that repo is pushed to GitHub, and its
#     setup.sh reinstalls it on a fresh box. The schedule is already survivable; this
#     script would only duplicate it badly.
#   * Merging, rebasing or force-pushing. flush pushes only when it is a clean
#     fast-forward. If history has diverged it says so and leaves the commits alone --
#     an unattended script resolving a divergence is how work gets destroyed. The
#     commits are still safe locally and in the daily rclone mirror to Drive.
#
# Usage:  keeper.sh [boot]     "boot" forces a catch-up pass regardless of staleness.
# Cron:   see the @reboot and hourly lines in crontab.

REPO="/home/user/new-skinny-bob"
LOG="$REPO/watch/x/keeper.log"
LOCK="$REPO/watch/x/.keeper.lock"
CHECKLOG="$REPO/watch/x/check.log"
PUBLISH_BRANCH="main"           # where this repo's work actually lives
STALE_MIN=10                    # a */2 job silent this long is not idle, it is broken

GIT=/usr/bin/git
PY=/usr/bin/python3.12
SYSTEMCTL=/usr/bin/systemctl

MODE="${1:-periodic}"

exec >> "$LOG" 2>&1
say() { echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') [$MODE] $*"; }

# Never let two keepers, or a keeper and its own catch-up pass, touch the repo at once.
# -n: if another one holds the lock, this run is redundant, so drop it rather than queue.
exec 9>"$LOCK"
if ! /usr/bin/flock -n 9; then
  say "another keeper holds the lock, skipping"
  exit 0
fi

# --- 2. is cron alive -------------------------------------------------------------
ensure_cron() {
  if $SYSTEMCTL is-active --quiet cron; then
    return 0
  fi
  say "!! cron is not active -- starting it"
  if sudo -n $SYSTEMCTL start cron 2>/dev/null; then
    say "cron started"
  else
    say "!! could not start cron (no passwordless sudo?) -- the watcher is DOWN"
  fi
  # enable is idempotent and cheap; without it a reboot brings the box back mute.
  sudo -n $SYSTEMCTL enable cron >/dev/null 2>&1 || true
}

# --- 4. is the watcher succeeding, not merely firing -------------------------------
# check.log gets one line per pass whatever the outcome, so its mtime is the honest
# liveness signal. A stale one means cron is not firing OR every fire is crashing;
# either way the catch-up below is the right response.
minutes_since_check() {
  if [ ! -f "$CHECKLOG" ]; then echo 99999; return; fi
  local mtime now
  mtime=$(stat -c %Y "$CHECKLOG" 2>/dev/null || echo 0)
  now=$(date +%s)
  echo $(( (now - mtime) / 60 ))
}

catch_up() {
  local age=$1
  say "running a --full catch-up pass (last check ${age} min ago)"
  # --full re-checks every known id including the deleted ones and sweeps media, which
  # is what you want after a gap: it cannot recover a post deleted during the downtime,
  # but it re-establishes ground truth instead of assuming nothing moved.
  cd "$REPO" || return 1
  $PY watch/xwatch.py --quiet --full --commit
  say "catch-up pass exited $?"
}

# --- 3. get the captures off this disk ---------------------------------------------
flush() {
  cd "$REPO" || return 1

  # GITHUB_TOKEN resolves to the wrong account on this box. Cron does not have it in
  # its environment today, but unset it anyway so this keeps working if that changes.
  unset GITHUB_TOKEN

  local ahead
  if ! $GIT fetch --quiet origin "$PUBLISH_BRANCH" 2>/dev/null; then
    say "!! fetch failed -- offline? commits stay local, Drive mirror is the fallback"
    return 1
  fi
  ahead=$($GIT rev-list --count "origin/$PUBLISH_BRANCH"..HEAD 2>/dev/null || echo 0)
  if [ "$ahead" = "0" ]; then
    return 0
  fi

  # Fast-forward only. If origin has commits we do not, something else is publishing
  # here and reconciling it is a human's job.
  if ! $GIT merge-base --is-ancestor "origin/$PUBLISH_BRANCH" HEAD 2>/dev/null; then
    say "!! $ahead local commit(s) unpushed, but origin/$PUBLISH_BRANCH has diverged."
    say "!! NOT resolving that automatically. Run: git fetch && git rebase origin/$PUBLISH_BRANCH"
    return 1
  fi

  if $GIT push --quiet origin "HEAD:$PUBLISH_BRANCH" 2>/dev/null; then
    say "pushed $ahead commit(s) to origin/$PUBLISH_BRANCH"
  else
    say "!! push failed with $ahead commit(s) pending -- credentials or network"
    return 1
  fi
}

# --- run ---------------------------------------------------------------------------
ensure_cron

AGE=$(minutes_since_check)
if [ "$MODE" = "boot" ] || [ "$AGE" -ge "$STALE_MIN" ]; then
  catch_up "$AGE"
else
  say "watcher healthy (last check ${AGE} min ago)"
fi

flush
