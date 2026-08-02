# Reddit draft for r/qtecqot

Draft 2026-08-02. Replaces the earlier "@qtecqot is quite active on X" draft, which was written
before the deleted posts were recovered.

---

## Title

**Recovered 11 deleted @qtecqot posts. His first post ever named Project SERPO, and he erased it
11 minutes after video 5/8 went live.**

Alternatives, in order of preference:

2. **@qtecqot has deleted 11 of his 19 posts. Here they all are, including the first one, which
   names Project SERPO.**
3. **The @qtecqot X account was never dormant. It posted 30 minutes after signup and got wiped
   the minute the first video dropped.**

Note on the title you suggested: *"is very active on X, has many deleted posts: detailed analysis
of all actions, reveals lots of new connections"* buries the finding behind three clauses and
"lots of new connections" reads as a tease. The deletions and SERPO are the story. Lead with one
concrete verifiable fact and let the post carry the rest.

---

## Image carousel

Order matters. Slide 1 has to work with no text.

| # | file | why |
|---|---|---|
| 1 | `figs/qtecqot-2026-08-02/1_deletions.png` | 19 posts, red vs green, the 11-minute purge marked. Whole story in one frame. |
| 2 | `figs/qtecqot-2026-08-02/2_counters.png` | his own counters dating the purge to the minute. This is the proof, not decoration. |
| 3 | `qtecqot-x-recovered/media/2026-08-02_deleted_fake-copycat-channel.png` | the post he deleted **today**. Screenshot is the only copy in existence. |
| 4 | `figs/qtecqot-2026-08-02/3_clock.png` | our own published time-zone claim, withdrawn. Shows the work is audited. |
| 5 | `qtecqot-x-recovered/media/0731_live_1.jpg` and `_2.jpg` | his AI-detector screenshots, already public, for the readers who only know that part |

Do **not** reuse `figs/qtecqot/clock.png`. It shows the withdrawn reading.

---

## Body

Everything below is checkable. Method, raw records and the negative results are in the repo,
linked at the end.

**The account was never dormant.** The record everyone has been working from says @qtecqot sat
idle from April to late July. It did not. It posted **30 minutes after registration** and has
authored **19 posts**. Eleven of them are deleted. The July "zero posts" everyone saw was the
result of a wipe, not evidence of an unused account.

**How they were recovered.** X exposes no logged-out route to a deleted timeline. Somebody
unconnected to this project was running Twitter API v2 lookups on the account and the Wayback
Machine archived them. Those captures survive the deletions. Enumeration:
`web.archive.org/cdx/search/cdx?url=twitter.com/qtecqot*&output=json`. Each recovered post is
cross-checked four ways: snowflake decode of the status ID against the archived `created_at`
(19 of 19 agree to the second), live state against api.fxtwitter.com, the author's own post
counter carried inside each record, and an independent xAI x_search that returned exactly the 8
surviving IDs and nothing before 28 July.

**His first post ever, deleted, reads:**

```
ivan   compromised, UNK cond.
2026-04-21  15:30:12 UTC

release 5 -8 is triggered

Иван
СЕРПО
раскрытие
```

Russian: *Ivan / SERPO / disclosure*.

**Project SERPO is a real published corpus and it has been sitting in plain sight since 2005.**
Released from 2005-11-02 at serpo.org by a poster calling himself "Anonymous", organised as
numbered **Releases**. Two of them are Chapter 9, "Soviet Contact":

- **Release 26a** is headed, word for word: **`RETIRED KGB MAJOR IVAN WRITES:`**
- **Release 26** contains: *"CAC reported Soviet KGB officials took over 100 PHOTOGRAPHS and
  **one (1) video recording of the occupants**."*

A single KGB video recording of live non-human occupants in Soviet custody, published **five
years before ivan0135 uploaded one in May 2011**. Release 26a describes the occupants as *"no
ears… no hair… identical one-piece flying suits, gray in colour."*

**Where it does not fit, which matters just as much.** Release 26a is a **January 1985**
incident. The Skinny Bob corpus is dated 1942 to 1969. The occupants in 26a are 1.2 m and 100
kg, which is not skinny, they have no thumbs, and all five escape three days later. Different
event. What this establishes is a **shared ancestor for the story**, not a source for the
footage, and nothing about how the footage was made.

**Somebody in this community found this before and it did not stick.** There is a deleted
comment in the 2021 r/UFOs thread on the videos where LinkifyBot preserved a bare `serpo.org`
link. The connection has been touched and lost at least once.

**The deletions are timed to the launch.** Every archived record carries the author's own post,
media and follow counters as they stood the instant he posted:

| post timestamp (UTC) | posts | media | follows |
|---|---|---|---|
| 2026-04-28 05:54 | 1 | 0 | 2 |
| 2026-05-07 06:17 | 2 | 1 | **4** |
| 2026-05-25 09:46 | 3 | 1 | 3 |
| 2026-05-25 09:50 | **1** | **0** | 3 |

Video 5/8 published **09:39:42**. He posted "upload No.1 complete" at 09:46:14. By 09:50:36 the
counter reads 1 post and 0 media. The trigger post, the second post and the announcement were
all gone, replaced by a reworded announcement. **He scrubbed his own opening thread within
eleven minutes of going public.** Second signal in the same table: he was following 4 accounts
on 07 May and 3 by launch, so an account was followed and unfollowed inside that window.

**He is still doing it.** Earlier today he posted a link to `youtube.com/@qtecqot2` captioned
"Fake copycat channel" and deleted it inside about an hour. That handle now 404s with no Wayback
capture and does not appear in YouTube search. Slide 3 is the only surviving copy of that post,
a browser screenshot taken while it was up. One unverified detail worth having: the person who
opened it says the copycat was showing **the same three videos as the real channel**, so it was
a mirror of his own material rather than an empty name-squat.

**The register is worth a look.** 584 words of him, total. In that span: `UNK cond.` (personnel
status shorthand for unknown condition), `ivan compromised` in the intelligence sense,
`Incapacitation presumed`, `release 5 -8 is triggered` of a pre-set condition, `DMS` used a day
before he glossed it as Deadman's Switch, `authorization to distribute`, `the network's cache of
materials`, `recovery site D`, `intermittent contact through electronic means as circumstances
dictated`. Fourteen distinct markers in 584 words. Before anyone runs with that: the SERPO
corpus is written throughout in exactly this register, with glossaries at the head of each
release, so somebody steeped in the source text produces this vocabulary without ever having
held a clearance. And in the same breath he writes "If anyone knows how to completely disable
this feature, please advise me" about YouTube ads.

**We got something wrong and it is in the same post as the findings.** Our published time-zone
analysis used 7 timestamps and reported a clean Central European morning band, "eight for
eight". With all 19 posts, **CEST puts 7 of them in the local small hours**. Moscow 5, US
Pacific 10, US Eastern 11. The only offsets where no post lands in the small hours are UTC+8.5
to +10, and the honest conclusion is not "he is in UTC+9", it is that **the clock no longer
identifies a zone**. Slide 4. The correction is logged in the repo alongside everything else we
have had to withdraw.

**What is not in this post.** One deleted post consists of a personal name and a photo. The
person named is a documented public figure and the name is in the repo, but nothing publicly
connects that material to Skinny Bob in either direction, and asserting a link off one deleted
tweet would be asserting something the evidence does not carry. It is written up in the repo
with the negative searches, and it stays there until content comparison returns something.

**Nothing here says the videos are real or generated.** All of it constrains how the release was
staged and who staged it. That is a separate question from what is in the frames.

---

## Questions for him

He replies, he corrected our tape numbering, and he says he will not disable the channel. So
asking is not pointless. "A question a faker could never answer" is the wrong frame, there is no
such question. The right frame is **cost asymmetry**: ask for things that are trivial if he
holds physical film and impossible otherwise, and ask for several at once.

1. **One over-scanned frame.** Scanned past the image area, showing gate edge, sprocket holes,
   leader, or the reel. A film scan produces this by accident. A generated clip has no source
   for it. Strongest single ask on this list.
2. **The same twenty frames scanned twice, independently.** Same content, different grain, dust
   and registration. Trivial with film in hand, very hard to fake, and testable by anyone.
3. **Ten seconds at source bitrate.** Every negative result anyone has is floored by the thin
   encode he published. Costs him nothing if the material is real and moves the analysis more
   than anything else here.
4. **The frames either side of a cut** he chose to make.
5. **A case number from the burned-in catalog that has never been shown on screen.** Working
   from a real ledger stays consistent, improvising drifts. Worth saying plainly: his "Case 28
   belongs to tape 5, not tape 4" correction **agrees with our independently built ledger**.
   That is a small point in his favour and it should be on the record.
6. **Publish SHA-256 of the next release before releasing it.** Say what it does though: it
   timestamps that a file existed earlier. It is not authentication. Better version is hashes of
   the whole remaining holding he says he has.

And a genuine offer rather than a demand: **the AMA.** He has answered narrow technical
questions already.

---

## Repo

Everything above, with the raw records, the method, the negative results and the corrections log:

**https://github.com/CraaazyPizza/slim-tim**

- all 19 posts with a Wayback link each: `qtecqot-x-recovered/RECOVERED.md`
- how they were recovered and why the set is trusted: `qtecqot-x-recovered/PROVENANCE.md`
- the SERPO lead in full: `qtecqot-x-recovered/SERPO_LEAD.md`
- the register analysis: `qtecqot-x-recovered/REGISTER.md`
- the withdrawn time-zone reading: `analysis/clock-redo/` and `CORRECTIONS.md`
- the full prior dossier: `reports/agent_qtecqot_dossier.md` (§3 is annotated as withdrawn)

Pretty high chance he reads this subreddit, so: hi.

---

## Pre-flight checklist

- [ ] Push the repo first, so every link resolves when the post goes up
- [ ] Crop or blank third-party handles in any screenshot that is not qtecqot or ivan0135
- [ ] Do not use the words *proves, debunked, case closed, hoax*, or *confirms it's fake/real*
- [ ] No em dashes, no semicolons in body prose (`~/PaperMaker9000/RULES_SUPERLIST.md`)
- [ ] Attribute the "they want him dead" framing to him rather than stating it
- [ ] Check `figs/qtecqot/clock.png` is not in the carousel
