# Contributing

Short version: **just put it in.** Setup is in the README — click the Codespaces
badge, install the Claude Code, Codex or Gemini extension if you have a
subscription, and tell it *"commit this and submit it to the repo."* You don't need
to know git.

Prefer your own machine? `git clone`, then `bin/setup`. It pins the same
dependencies the Codespace uses and warns you if your ffmpeg won't reproduce the
published frames.

If you want write access, ask. You'll get it. I'm not vetting anybody.

## The two things I'd ask

**Don't grief it.** No wiping other people's work, no rewriting history, no
force-pushing. `main` is protected against that anyway.

**No personal information about private people.** No real names, no email
addresses, no commenter usernames, no screenshots with account names or
notification text in them. Two public creators who wrote about this material under
their own names are named in the existing documents — that's the whole exception.

This is the one rule I'll revert things over, and it's why some material that
exists isn't in here. If you generate a figure from a screenshot, look at the
whole image before committing — a safety pass on this repo once missed an email
address rendered *inside* an image, and later a real name sitting in a comment-box
placeholder. Text search finds neither.

## What's most useful

1. **A correction.** Something in `FINDINGS.md` is wrong. If you're right it goes
   into `CORRECTIONS.md` with credit, and the withdrawn claim stays visible with
   the reasoning rather than being quietly edited away.
2. **A frame reference.** You can see something in a specific frame — video ID and
   frame number is enough. Highest value for the least effort.
3. **A replication that disagrees.** You re-ran something and got a different
   number. Include your ffmpeg version: 4.4.2 is what produced these results, and
   other builds legitimately differ (see `frames/README.md`).
4. **Something nobody looked at.** `UNFINISHED_BUSINESS.md` is a list of exactly
   that, and the item at the top needs no analysis skill at all: fetching a
   higher-bitrate copy of the videos than the one everything here was measured on.
   `CORPUS_QUALITY.md` explains it in a page.

Half-finished is fine. It's a draft.

## Two habits that make a finding much stronger

**If you say something isn't there, say what you could have seen.** On footage
this soft that's the difference between a result and a guess. The cautionary
example is in the repo: five of five frames returned no five-pointed star — and
then a *real* star injected at 120 px and 35 DN of contrast turned out to be
invisible to an independent observer too. The null was underpowered. Injecting a
synthetic version at graded amplitudes and reporting where detection fails turns
"I saw nothing" into a measurement.

**Look at unmodified frames.** Enhanced, averaged and annotated images are in here
and labelled. Reasoning from those alone is how several claims in this project went
wrong. The convention is that an enhanced image appears beside the frame it came
from, and the caption says what it does *not* show.

## Words this repo doesn't use

> proves · debunked · case closed · confirms it's fake · confirms it's real · hoax

Not squeamishness — each asserts more than the evidence carries. "AI-generated" is
a hypothesis here, not a conclusion. Provenance is undetermined, and a change that
resolves it by assertion rather than measurement will get asked for the
measurement.

## A note on the big files

Extracted frames and multi-gigabyte intermediate arrays aren't in the repo. Frames
regenerate from the source videos with one command — `frames/README.md` has it,
verified byte-identical. The arrays were working state; where a result depends on
one, the report gives the numbers.
