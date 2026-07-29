# Skinny Bob, 2026 — my stash

**Disclaimer: Yes, everything was made with AI. Slop-language ahead. Try to focus on the content.**

In 2011 a channel called `ivan0135` posted four short videos that became the
"Skinny Bob" story. In 2026 a channel called `qtecqot` posted three more, saying
they were continuing the same release under a dead man's switch.

I spent a while measuring all seven of them. This is everything I found, plus the
scripts, the figures, and the mistakes. I'm too busy to keep going right now, so:
have at it.

**You do not need to be able to code to use any of this.** Genuinely. See below.

## What I actually found

Short version, and it is deliberately unsatisfying:

- The 2026 soundtrack is a **sample-level copy** of audio published in 2011.
  Same samples, not a similar-sounding bed.
- The 2026 picture and its own audio run on **time bases that disagree** by
  roughly a quarter.
- The hand in the 2026 footage has **digit proportions 26% different** from the
  2011 hand.
- There's a **four-frame insert** at the climax of the May video that nobody
  noticed for two months. I still don't know what it shows.

**None of that tells you whether the footage is real.** It tells you how the
videos were put together. I don't know where the imagery came from and I'm not
going to pretend otherwise.

One thing I got wrong at the very bottom of the stack: I did all of this on a
lower-bitrate copy of the videos than YouTube actually had — same picture size,
about three times less detail — because the download tool picked it silently.
Anything I say is *there* is still there. Anything I say *isn't* there might just
have been too blurry to see.

**The better copy is now in the repo too**, as `videos/2026-avc/` and `videos/2011-avc/`, and
rerunning the soft calls against it is the most useful thing anyone could do here.
One page on it: **[CORPUS_QUALITY.md](CORPUS_QUALITY.md)**. It has already settled
one question — the mysterious fixed dots in the corners turn out to be the
encoder's, and they vanish completely in the better copy, exactly as predicted.

Start with **[FINDINGS.md](FINDINGS.md)** — that's the real writeup.

And **[CORRECTIONS.md](CORRECTIONS.md)** — things I got wrong and then withdrew,
including two of my own headline claims. There are probably more mistakes in here
that I haven't caught. If you find one, brilliant, tell me.

## Getting started — pick whichever one is you

<details open>
<summary><b>🖱️ &nbsp;I don't really code</b> &nbsp;—&nbsp; one click, and you get a Linux machine in a browser tab</summary>

<br>

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/CraaazyPizza/slim-tim?quickstart=1)

1. Click that. You need a free GitHub account. Wait about thirty seconds.
2. You now have **a whole Linux computer running in your browser tab** — not just a
   file viewer. Both copies of all seven videos, every figure and every script are
   already on it, along with Python, ffmpeg, and the `claude`, `codex` and `gemini`
   command-line tools. Nothing to install, nothing to configure, nothing to
   download. You can run things, install things, break things: it isn't your machine
   and it isn't mine, so there is nothing you can wreck. Bin it and click again for
   a fresh one.
3. If you have a **Claude, ChatGPT or Gemini subscription**: click **Extensions** in
   the left sidebar, install **Claude Code**, **Codex** or **Gemini Code Assist**,
   and log in with your account. All three are installed as terminal commands too —
   `claude`, `codex`, `gemini` — so you can just type one. Any of them works; if you
   have a choice, see the note about Gemini and images below.
4. Ask it things. That's it. It can read every file here, pull frames out of the
   videos, run the scripts, and show you what came out.
5. **Found something? Just say: "commit this and submit it to the repo."** The AI
   handles the rest. You do not need to know what a commit or a pull request is —
   see below.

I've tested this and it works. Your login stays yours — that container is your own
Codespace on your own free allowance, so nothing runs on my machine or my tab. Close
the tab when you're bored.

Almost all of my analysis was done exactly this way. You are not behind.

</details>

<details>
<summary><b>⌨️ &nbsp;I have a terminal and opinions about it</b> &nbsp;—&nbsp; clone it, <code>bin/setup</code>, done</summary>

<br>

```bash
git clone https://github.com/CraaazyPizza/slim-tim.git
cd slim-tim
bin/setup
```

`bin/setup` makes a `.venv`, installs the pinned dependencies, and tells you whether
your ffmpeg will reproduce the published frames byte for byte. It touches nothing
outside `.venv` and is safe to re-run. Roughly 500 MB of clone, most of it the
figures and intermediate arrays under `analysis/`.

Both source copies of the videos are already in the clone — you don't need to
download anything from YouTube. If you *do* want to re-fetch, the command is in
[`CORPUS_QUALITY.md`](CORPUS_QUALITY.md).

**Don't want the bulk?** `analysis/` is 368 MB of figures and intermediate arrays.
This skips it and fetches nothing you don't check out:

```bash
git clone --filter=blob:none --sparse https://github.com/CraaazyPizza/slim-tim.git
cd slim-tim
git sparse-checkout set video ivan reports figs frames bin
```

That gets you every document, the scripts, and the videos in about 55 MB. Add more
later with `git sparse-checkout add analysis`, or `git sparse-checkout disable` for
the lot.

**Worth knowing before you run anything:**

- **ffmpeg 4.4.2** produced every published frame. Other builds differ slightly but
  legitimately — 7.x writes an extra `cICP` PNG chunk, 16 bytes a frame. `bin/setup`
  warns you. Details in [`frames/README.md`](frames/README.md).
- **`videos/2026/` and `videos/2026-avc/` are not interchangeable.** Everything in the writeups
  was measured on the thinner AV1 copy. `bin/frames --avc` writes to a separate
  `frames-avc/` tree on purpose. [`CORPUS_QUALITY.md`](CORPUS_QUALITY.md).
- **Frames aren't stored**, they're made on demand: `bin/frames OpSTlDJWFFI 2971 2974`
  takes about ten seconds. All seven videos is ~6 minutes and 5 GB.
- **`analysis/` is a record of what was run, not a library.** No packaging, no tests,
  varying quality. `reports/` is the readable layer over it.

</details>

## Things to paste in and see what happens

```
Read FINDINGS.md and explain it to me like I know nothing about this case.
```
```
What are the three strongest findings in this repo, and what's the weakest?
```
```
Read CORRECTIONS.md. What did they get wrong, and why did they think it at first?
```
```
Run bin/frames to pull frames 2971 to 2974 out of the May 2026 video, and show me.
```
```
Pick any claim in FINDINGS.md and try as hard as you can to refute it.
```
```
What did nobody check? Read UNFINISHED_BUSINESS.md and tell me what's left.
```

That fifth one is the most fun and the most useful.

## One warning, and it matters

**The AI will confidently make things up about these images, and it will sound
certain doing it.** This is not hypothetical — it's in `CORRECTIONS.md`:

- One model identified the mystery insert as a specific Apollo 11 frame at ~95%
  confidence. Wrong.
- Another named a well-known military UAP video at 99%. Also wrong.
- One transcribed Mandarin numerals out of what was synthetic babble with no
  speech in it at all.
- Asked leading questions about low-resolution crops, models will invent a
  five-pointed star that isn't there.

The footage is grainy and low-resolution, which is exactly the condition where
these tools hallucinate hardest. So:

- **Ask neutrally.** "What do you see here?" not "do you see a face here?" The
  second question manufactures a face.
- **Ask twice, in separate chats.** If the answer changes, it was invented.
- **Be most suspicious when it's most confident.** That's the pattern here.
- **Ask for unmodified frames**, not contrast-boosted ones. Enhancement makes
  noise look like structure. Half the wrong calls in this project came from
  somebody reasoning about a brightened crop.

One practical note: **Gemini is noticeably better at actually looking at images**
than the others, in my experience here. If you're asking "what is in this frame",
it's worth a second opinion from a different model — and if two models disagree,
that disagreement is information. Several findings in this repo were settled that
way, and several claims died that way.

This isn't a reason not to use these tools. It's the whole reason the writeup is
careful.

## What's in here

**Start here**

| | |
|---|---|
| `FINDINGS.md` | the writeup. Start here. |
| `CORRECTIONS.md` | what I got wrong, and why I thought it |
| `CORPUS_QUALITY.md` | one page: I measured a worse copy of the videos than I had to |
| `UNFINISHED_BUSINESS.md` | what I didn't get to — the best place to find something to do |

**The material**

| | |
|---|---|
| `videos/` | the source videos. `2011/` and `2026/` are what everything was measured on; `2011-avc/` and `2026-avc/` are the better copies |
| `frames/` | the handful of frames the documents cite. `bin/frames` makes any others |
| `audio/` | audio you can just listen to |
| `figs/` | every figure, sorted by topic |
| `metadata/` | raw YouTube metadata for the channels and videos |
| `community/` | captured public reaction |

**The work**

| | |
|---|---|
| `reports/` | the long write-up behind each finding. `reports/INDEX.md` says what each settles |
| `analysis/` | the scripts, one directory per line of enquiry. `analysis/README.md` maps it |
| `docs/` | deep dives: `TIMELINE.md`, `SKINNY_BOB_DOSSIER.md`, `PIPELINE.md`, `PITFALLS.md` |
| `watch/` | the monitor watching for the next release, and its snapshots |

**Tools and notes for the AI**

| | |
|---|---|
| `bin/frames` | `bin/frames OpSTlDJWFFI 2971 2974` and you have those four frames |
| `bin/setup` | local setup, if you cloned instead of using a Codespace |
| `AGENTS.md` | notes for an AI working here. Short on purpose — worth reading yourself |
| `docs/PITFALLS.md` | the same notes at length: five hallucinations, and the habits that catch them |
| `requirements.txt` | the pinned Python dependencies, same as the Codespace image |

`analysis/` is a record of what was actually run, not a tidy library. Directory
names say what the work was about: `cyrillic/`, `hand-proportions/`,
`timecode-ticks/`, `symbol-panel/`, `corner-dots/`, `compare-eras/`. Some of it is
superseded by later passes, and where I know that, the report says so.

## Adding your own stuff — just do it

This is a shared workspace, not my personal repo that you have to petition. If
you find something, put it in.

**You don't need to know how git works.** In your Codespace, tell the AI:

```
Commit my changes and submit them to the repo.
```

It'll do the whole thing — including forking and opening a pull request if it
turns out you don't have direct write access, which needs no permission from
anyone. If you'd rather push straight to the repo, ask me for write access and
you'll get it. I'm not vetting anybody.

Two things I'd ask, and they're the only two:

- **Don't grief it.** No wiping other people's work, no rewriting the history, no
  force-pushing. The main branch is protected against that anyway, but I'd rather
  say it than rely on the setting.
- **No personal information about private people.** Not their names, not their
  email addresses, not screenshots with account names in them. This is the one
  rule I'll actually revert things over, and it's why some material that exists
  isn't in here.

Write anything else: a note in a file, a script, a figure, a correction, a "this
looks wrong to me and here's why." Half-finished is fine. It's a draft.

If you tell me something in `FINDINGS.md` is wrong and you're right, it goes
in `CORRECTIONS.md` and you get the credit.

One tip that makes any finding much stronger: if you're saying something *isn't*
there, try to work out what you *would* have been able to see. On footage this
soft, "I looked and saw nothing" is weak. "I looked, and I could have spotted a
mark down to this size, and there's nothing" is strong — and that's the difference
between a claim that survives and one that doesn't.

## A gotcha if you re-extract frames yourself

You'll probably get slightly different pixel values than mine, and it can look like
someone's lying. Nobody is — it's the video decoder. Frames decoded from one codec
differ from another by at most 1 in 255, and ffmpeg 7.x writes 16 extra bytes into
every PNG that 4.4.2 doesn't. The Codespace pins **4.4.2** so your frames match mine;
`bin/setup` tells you where you stand locally.

Chasing exactly that difference is how the mysterious fixed dark dots in the corners
of the 2026 videos turned out to be the encoder's rather than something the author
put there. With both copies of the videos now in the repo that's a settled test
rather than a lucky observation: the dots are 2,048 pixels in the AV1 copy and
**completely absent** in the AVC one, in exactly the two 32×32 blocks the tile grid
predicts. `analysis/corner-dots/controls/codec_control.py`, and
[`CORPUS_QUALITY.md`](CORPUS_QUALITY.md).

So: expect small differences between decoders, don't read meaning into them — but do
notice that one of those differences carried a finding.

## Some ground rules

**No naming private people.** Two people are named in here — both public creators
who published about this material under their own names, and only their public
work is discussed. Nobody else, including commenters. Please keep it that way.

I also found a partial email address for the 2026 account through a password-reset
flow. It's deliberately not in here. It identifies an account, not a person, it
tells you nothing useful, and publishing it just hands strangers a starting
point. Nothing was ever sent to it and I contacted nobody.

**It's a draft.** Mistakes are in here. If someone linked you to this as proof of
something, they've overstated it. It's a stash, not a verdict.
