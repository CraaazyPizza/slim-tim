# "Skinny Bob" (ivan0135, 2011) — Factual Dossier

Compiled 2026-07-26. Sourcing key used throughout:

- **[F]** = Verified fact (primary source directly retrieved/quoted: YouTube API/RSS data, archive.org mirrors, or a directly-fetched page reproduced verbatim).
- **[C]** = Widely-repeated community claim, sourced to a named forum contributor or site but not independently re-verifiable by me against a primary document.
- **[S]** = Speculation / unverified / explicitly flagged by sources themselves as unconfirmed.

Where a claim's category is disputed between researchers or sources, that's noted explicitly. Access limitations: Reddit (including r/SkinnyBob directly) and AboveTopSecret/GodlikeProductions forum pages returned HTTP 403 to direct fetch in this research session; material from those venues is reported second-hand via sources (chiefly skinnybob.info) that quote them, and is flagged accordingly.

---

## 1. The ivan0135 YouTube Channel — Verified Primary-Source Data

**[F]** Channel: handle `@ivan0135`, channel ID `UCC5AjFfZHRvILhJfWw5UcDw`, created **2011-04-14T01:08:36 UTC** (per YouTube's own RSS/channel feed). Exactly **four videos**, no others, ever uploaded; no posts, replies, or activity after the fourth upload (2011-05-18). This was independently confirmed by two separate research passes pulling live YouTube API/RSS data and cross-checked against archive.org's June 2024 yt-dlp mirror of each video (item IDs `youtube-<videoID>`), which matched exactly.

**[F]** Channel "About" section (self-reported, i.e. this is Ivan's own unverified claim, not external evidence): creator states they are **"from Russia,"** **"born in 1969."** Note the 1969 figure conspicuously matches the *end year* of the claimed 1942–1969 footage range — several sources flag this as possibly not a coincidence, but this is speculation, not documented.

### 1.1 Video table

| # | Video ID | Title (exact) | Upload (UTC) | Length | Views (as of 2026-07-26 live pull) | Views (archive.org snapshot, 2024-06-01) |
|---|---|---|---|---|---|---|
| 1 | `ZB788PtqQvg` | "Disclosure leaked ufo alien case video confidential documents old footage" | 2011-04-14 02:04:26 | 0:48 | 677,249 | 513,616 |
| 2 | `RsQCXN4o4Ps` | "alien grey extraterrestrial zeta reticuli ufo leaked footage" (the "Skinny Bob" clip proper) | 2011-05-02 05:21:51 | 1:00 | 1,485,759 | 1,026,200 |
| 3 | `Xju_CY5ZESA` | "Ivan0135 about ALIEN and UFO documents" (text-only reply video) | 2011-05-09 05:09:51 | 1:44 | 346,193 | 244,272 |
| 4 | `a6TLGkrfNKI` | "alien grey extraterrestrial zeta reticuli tape 06 - family vacation" | 2011-05-18 00:35:43 | 1:34 | 702,382 | 541,180 |

Total views ≈3.21M (2026 pull) / ≈2.33M (2024 archive snapshot). **[C]** Multiple 2020s retrospective blogs/wikis cite "over 1.9 million views" combined — likely a stale figure from whichever date that source was written; **no contemporaneous 2011/2012 news-reported view count could be found** — flagged as a genuine research gap, not a fact I can supply.

Archive.org mirrors: `archive.org/details/youtube-ZB788PtqQvg`, `-RsQCXN4o4Ps`, `-Xju_CY5ZESA`, `-a6TLGkrfNKI`.

### 1.2 Verbatim descriptions and on-screen text

**Important methodological finding [F], independently confirmed twice:** Video 2's YouTube **description field is empty (`""`/`null`)**, both live and in the 2024 archive snapshot. The famous "Tape 05 / Case 25 / Skinny Bob" catalog text that gets reproduced everywhere as if it were a YouTube description is actually **burned into the video image itself as title cards**, not stored as metadata. This matters for the dossier: two of the four videos (2 and 3) carry their real textual content as in-video captions, not description-box text, while videos 1 and 4 carry it in the description box proper. Below, description-field text and on-screen/caption text are labeled separately.

**Video 1 (`ZB788PtqQvg`) — YouTube description field, verbatim [F]:**
```
Leaked air force ufo footage. Confidential. Classified document.1942-1969.

Relevant information:

The video contains a sample edited fragments of tapes 01, 03 and 04 

Tape duration: 180 min
Total recorded duration: 1.260 min

Tape 01: 
Case 07/Tin bird 00:08:41 - 00:08:47
Tape 03:
Case 15/Flying twin 00:27:11 - 00:27:13
Case 15/Flying twin 00:27:34 - 00:27:39
Tape 04:
Case 23/Blue boys 00:42:50 - 00:42:51
Case 23/Blue boys 00:48:09 - 00:48:16
Case 24/Blue boys meeting 00:47:30 - 00:47:32
Case 24/Blue boys meeting 00:56:12 - 00:56:14
Case 24/Blue boys meeting 00:58:26 - 00:58:28
```

**Video 2 (`RsQCXN4o4Ps`) — description field: empty.** On-screen title-card text, reconstructed frame-by-frame from archive.org thumbnails **[F, high confidence, but see caveat]**:
- @~1s: *"Filtrate for declassification and dissemination through the Internet and media. 7 video tapes with material recorded between 1942-1969. Material containing UFO incidents, recovery and study of extraterrestrial life forms."*
- @~14s: *"Due to the importance of these documents, maintain the anonymity of the sources."*
- @~18–24s: *"The video contains a sample edited fragments of video tape 05. Tape duration: 180 min. Total recorded duration: 1.260 min."*
- @~25s+: footage with an on-screen tape/case counter reading **"25 00:08:46," "25 00:08:48"**.
- @~55s: counter reads **"26 00:55:10"** over a different (circular-aperture) shot.
- **★ CORRECTED 2026-07-29 — [S] flag removed, now [F].** This entry previously said the
  *numbers* were on-screen but that the words "Skinny Bob" and "How to drive" were **not**
  confirmed as on-screen text and were "fan/community cataloging" / "fan-applied". **That is
  wrong.** A title card at **f501–575 (t ≈ 20.0–23.0 s)** of `RsQCXN4o4Ps` carries the case
  *names* in ivan0135's own hand, plainly legible at native resolution with no enhancement:

  > ```
  > Tape 05 edited fragments:
  > Case 25/skinny Bob 00:08:42 - 00:08:50
  > Case 25/skinny Bob 00:27:36 - 00:27:45
  > Case 26/How to drive 00:55:07 - 00:55:12
  > ```

  Read directly from the primary file and independently transcribed character-for-character
  by the `gemini` CLI. Note the lowercase "s" in "skinny Bob" — his own inconsistency, and a
  detail no fan cataloguer would introduce.

  **Why this matters beyond the correction:** the `Case NN/name` scheme — number, slash,
  human-readable case name — is **ivan0135's own 2011 authoring convention**, not a later
  community invention. Every argument about whether the 2026 videos "extend the 2011 case
  scheme" (see `reports/agent_catalog_ledger.md` and §11.6/§18) is therefore comparing
  qtecqot's ledger against a *documented in-corpus convention* rather than against fan
  practice. It also means the string "skinny Bob" is primary-source text from 2011.

**Video 3 (`Xju_CY5ZESA`) — YouTube description field, verbatim [F]:**
```
Ivan0135:

In  response to posts about the Documents:

http://www.youtube.com/watch?v=RsQCXN4o4Ps&feature=channel_video_title
http://www.youtube.com/watch?v=ZB788PtqQvg&feature=channel_video_title
```
(Note the double space in "In  response" — present in the real source text.)

**Video 3 — full on-screen text (the "reply to skeptics"), reconstructed frame-by-frame from archive.org thumbnails [F]:**
> Ivan0135:
>
> In response to posts about the Documents:
>
> The material is an edited compilation of the documents that we have.
>
> Your opinion and the conclusion you draw from this material do not depend on us.
>
> Maybe you are looking in the wrong direction.
>
> You are the ones who reject this material.
>
> Sources will not be revealed.
>
> Information that may involve any agency or people will not be disclosed.
>
> There is not any reference which may link the material to any organization that is working today in the material exposed.
>
> However, you are speculating and making conjectures about its origins.
>
> The material does not belong to any film, video game, television series or other commercial products that have been revealed to date or which are currently in production.
>
> No one who is out of this may prove to be the owner of this material.
>
> No one who is out of this can prove he has in his possession the original material.
>
> The revelation of further material will depend on the events and people.
>
> You are the ones who create your own misinformation.

**Video 4 (`a6TLGkrfNKI`) — YouTube description field, verbatim [F]:**
```
Tape 06
Family vacation

From the first contact in 1942, a series of diplomatic visits to discuss matters of mutual concern were planned.

Under the treaty 23/04, these meetings would take place in secrecy, a limited number of special agents would escort visitors and they would only meet high ranking officers.

According to the document 072 / E, at the meeting of 1961 there was an incident involving 3 subjects due to the violation of the agreement by the officers at the military base when they discovered that their arrival was been filmed with a hidden device without their consent.

Under the treaty 23/04, the meetings would be confidential and filming or taking photographs would not be allowed.

After the incident, the treaty was revised.
```

### 1.3 Ivan's own SEO/tag keywords (across the uploads) **[C]**

Reported (via skinnybob.info's synthesis, not independently re-verified against raw YouTube tag data by this research since the API tools used didn't expose tags): *"ufo, crash accident, alien, extraterrestrial, life, et, zeta, reticuli, grey, desclassified, top, secret, cosmic, sighting, leaked, disclosure, confidential, autopsy, intelligence, service, rosswel, incident, new, mexico, South, Africa, Kalahari, Desert, army, navy, air, force, defense, agency, department, abduction, old, footage, 1947, space, aliens, flying, military, video, airplanes, interview"* — note the misspellings **"rosswel"** (Roswell) and **"desclassified"** (declassified), and tags split into single words ("top"/"secret" as separate tags). Both misspellings are flagged as the weakest-sourced textual claim in this dossier — no researcher could independently pull raw tag metadata to re-confirm them; they come through secondary aggregation of skinnybob.info/checktheevidence.com summaries.

### 1.4 Post-upload silence and later contact claims

**[F]** After 2011-05-18, ivan0135 never posted again and never publicly responded to comments — described by multiple independent retrospectives as "a digital artifact frozen in 2011."

**[C, single-source, unverified]** A 2014 email exchange reported by a YouTuber using the handle "Will" / channel **PLANETunderATTACK**: he says he emailed an address affiliated with the footage on **2014-06-17** and got a reply on **2014-06-19**. Reply, quoted verbatim by skinnybob.info (source redacted the correspondent's name):
> "We were sent that footage to release from a source... I know its the original source because the original version is not available to anyone. that's why you wont find it anywhere on the internet. We released the footage using several sock channels on Youtube and other sites, we did it this way to make sure the info got out even if our channel, website etc was terminated."

Additional claims from this same exchange: the full uncropped original is **only 12 minutes long** (never publicly released) and shows the alien examining "star maps" at a table with government officials "in clothes of the time"; the alien's real clothing was a "dull silver type ski suit with a utility belt and dull silform footwear," swapped for human clothing before release for analysis purposes. **skinnybob.info itself explicitly labels this "purely anecdotal and unverifiable."** It also directly contradicts the "1,260 minutes total recorded" figure in the official video descriptions (~100x discrepancy), a contradiction the site says has "never [been] reconciled."

**[C, unverified, low confidence]** A low-quality aggregator (mysterylores.com) claims the ivan0135 account once "liked" a fan comment ("Skinny Bob is a cutie. Too cute to be fake.") — the same article says this was likely a misreading of a YouTube UI feature. Uncorroborated elsewhere.

---

## 2. skinnybob.info — the Community Resource

**[F]** The site is **live** (single static HTML page, anchor-link navigation only — there is no true separate forum/FAQ/timeline on the domain; those "pages" are the same index.html). Meta description: *"A forensic analysis of allegedly leaked UFO and alien footage."* Source code is public: **github.com/skinnybobinfo/website** (CC0-1.0 license).

**[F]** Site timeline (from GitHub API + Wayback CDX + the site's own RSS feed):
- Launched **2022-03-30** (RSS: "Initial publication... The website is skinnybob.info is online," dated 2022-03-30T03:07:31 UTC). First Wayback capture: 2022-03-31.
- Actively maintained since: 66 commits from 2022-03-30 to 2026-03-12 (most recent at research time), all by GitHub user `skinnybobinfo`. Sample commit messages: "Socorro footprints and Blue Boys name resolution," "Hoax theory section extended," "Riviere Rouge images," "CREM alphabet," "Crash stabilization clips, Kingman historic."
- **Caveat:** the on-page countdown timer some secondary sources cite ("unsuccessful for N years and counting") is JS-computed from Ivan's **2011-04-13 first-upload timestamp**, not from the site's own 2022 launch — don't confuse site age with case age.

**[F]** No real name is given for the operator anywhere; referred to only as "the editor." Site quote: *"The editor attempts, on a best effort basis, to curate what he believes to be the consensus among an abstract investigative body formed by contributing volunteers on various platforms."* Explicit disclaimer: *"The claims and statements made on this website do not necessarily reflect the opinion of other individuals or groups participating in this investigation, specifically the extensively sourced r/SkinnyBob community on Reddit."* Contact via an obfuscated image-based email and a Curve25519 public key.

**[F]** The site draws almost all of its analysis from named **r/SkinnyBob** Reddit contributors, credited throughout: u/RedDwarfBee, u/Data_Pure, u/Jazzlike_Squirrel, u/BrooklynRobot, u/Shtudi, u/rorz_1978, u/chester20080, u/toukoqouko, u/ShinePsychological87, u/AndrewEire, u/pepperonihotdog, u/Anon2World, u/MantisAwakening, u/SirRobertSlim, u/Agronut420, u/GenshinKaigi, u/AlienAnonymoose, u/SuccessfulRadish3, u/_aTokenOfMyExtreme_, u/ItsTheBS, u/SoCalledLife, u/LM-LFC98, and an unregistered contributor "Ralph."

**Site sections** (all one page, anchor IDs): Foreword, Status, Disclaimer, Ivan, Original videos, Visual effects, Audio effects, Tin bird, Flying twin, Blue boys, Blue boys meeting, Skinny Bob, How to drive, Handprint, Family vacation, Messages, Comparison, Arguments, Leak theory, Hoax theory, FAQ, Next steps, Feedback. Dense per-section content is folded into the relevant thematic sections below (§3–§5) rather than repeated in full here.

**[F] Notable standalone content not covered elsewhere in this dossier:**
- **Reward offer**: Reddit user **u/RedDwarfBee is personally offering $5,000–$30,000** for additional footage or background information (linked Reddit T&C thread) — this is a bounty, distinct from any cost-to-fake estimate (see §3.4).
- **Comparison cases** the site treats as parallel/reference material: a **1997 documentary "Area 51: The Alien Interview"** (IMDb tt0404780) with "remarkably similar" staged scenes (alien-at-table interrogation, symbol chart, white-coated physician, hidden-camera framing); the **2011 *Super 8* viral marketing campaign** (film-reel mail packages, June 2011, ~1 month after the "family vacation" upload); and a **1992 Rivière-Rouge, Canada "frozen alien corpse"** photo set (YouTube channel Etrangesvideos), which the site says is "not... debunked so far."
- **Pro/con authenticity table**: Pros listed — unresolved for a decade+, no credible authorship claim, no commercial exploitation, "essentially flawless" footage quality, no analyst consensus on hoax technique, geographically risky reveal choices. Cons listed — occasional jerky movement, stereotype-conforming symbols/aliens, "convenient" staged body placement, child-sized physique compatible with a human-in-costume, close aesthetic parallels to the 1997 documentary.
- **Leak theory**: speculates a whistleblower/theft leak from a government/military archive, explicitly raising the contemporaneous **2011 Pentagon breach and RSA hack** as a possible (speculative) provenance route.
- **FAQ** rejects both AI upscaling and manual/ML colorization as analysis-polluting, on the stated grounds that both fabricate unfounded detail not present in the source.

---

## 3. Technical Analyses and Debunks

### 3.1 The Andrew Johnson (checktheevidence.com) Analysis **[F]**

Source: Andrew Johnson, **"'Skinny Bob' – Alleged Grey-Alien Video Leaked in 2011 – Analysis,"** posted 2019-10-31, `checktheevidence.com/wordpress/2019/10/31/skinny-bob-alleged-grey-alien-video-leaked-in-2011-analysis/`. **Johnson's overall stance is credulous/pro-authenticity — a debunk-of-the-debunkers, not a skeptical takedown.**

- **Colour information**: Johnson concludes only Video 4 ("family vacation") has meaningful color: *"It is difficult to be sure whether this video is black and white or colour. However, capturing and enhancing the video suggests that there is some colour information in the video, although it is quite minimal."* He reads this as supportive of authenticity: *"This might explain why this video probably has colour information in it. It also appears to have been captured differently, which to my way of thinking, lends support to the idea that it is genuine. Why fake such short clips in 2 different ways?"*
- **CRT/scanline artifacts**: On videos 1–2, he describes a "ghosting" effect: *"This sort of effect is/was often seen on a badly-tuned TV or when a monitor is connected to an (analogue) video source with poor quality cabling, resulting in signal reflections – which cause the ghosting."* On banding, after boosting luminance/saturation: *"this more clearly shows coloured banding of the sort seen on old-style CRT analogue TV screens. Video 4 – the 'family vacation' does not appear to exhibit any such banding and so was not captured from a TV screen."* His conclusion: **"It is almost certain that videos 1 & 2 were captured from a TV screen."**
- **Which clips differed**: Videos 1–2 (TV-screen-sourced, monochrome, continuous "old projector" rattle audio) vs. Video 4 (color, no CRT banding, no projector-noise audio) — Johnson uses this inconsistency as a pro-authenticity argument ("why fake it two different ways"), the inverse of the inference a skeptic typically draws from the same data point.
- Johnson quotes VFX artist **Ben Philips's** SFX assessment in full (sourced from `reddit.com/r/AliensAndUFOs/comments/bibcmh/skinny_bob_analysis/`) and links a debunking video, **"Skinny Bob The Truth Revealed – Paranormal (un)Explained #28"** (`youtube.com/watch?v=vZMdgju8t9Q&t=1544`), which discusses the stock-grain-library claim at timecode 25:44.

### 3.2 The Stock Footage / Film-Grain Library Claim **[C, two distinct products, both named]**

- **Grain/damage overlay → Pond5**: Reddit's **u/BrooklynRobot** "tracked down the exact film damage overlay Ivan used... available as a stock video clip on the Internet" (per skinnybob.info). Metabunk poster Alphadunk (post #56, `metabunk.org/threads/skinny-bob-videos.11760/page-2`, 2021-08-17): *"The case for the grain overlay from **pond5** is rock solid IMO. There is really no question that is the exact overlay used."*
- **"Old Movie" compositing effects → Sapphire (Boris FX)**: credited to Reddit's **u/Jazzlike_Squirrel**. skinnybob.info: *"u/Jazzlike_Squirrel found the Software that was likely used to apply not only the film damage but other post-processing effects as well: Sapphire Plug-ins for After Effects by Boris FX."* Corroborated on Metabunk by Eiskind: *"The Old Movie effects are from Sapphire for BorisFX... These include the ghosting effect from the first UFO clip, the pillar boxes, the diagonal Rainbow Moire pattern etc."*
- **Anachronistic font**: u/BrooklynRobot also identified the embedded timecode font as Microsoft **Consolas**, released **2006** — used as proof the timecode overlay was digitally added, not a period-correct filming artifact.
- Eiskind additionally notes the intensity of "old film" filtering **decreases steadily across the four videos** — an inconsistency also separately noted by Andrew Johnson (§3.1), though the two camps read it in opposite evidentiary directions.
- A separate, **unrelated** small-time hoaxer using the handle **"351NOVA"/"Mr351Nova"** made prior fake alien-footage videos using **Windows Movie Maker** — Metabunk consensus treats this as a distinct, lower-quality hoaxer, not the same production (see §4.3 for the disputed identity theory linking him to ivan0135 anyway).

### 3.3 Frame-Level Tracking of Damage vs. Camera Motion **[C, both from skinnybob.info's own analysis, credited to named contributors]**

- **Lens flare argument for digitally-added camera shake**: *"There is a faint lense flare effect moving across the screen... such flares are generated inside the camera housing and depend on the angle a bright light source... is hitting the lense system. The clip above has been motion stabilized, resulting in the flares moving pretty much linearly. If the camera was actually shaking like the original clip suggests, the flares would jump all around the place. So it turns out that this seemingly minor and overlooked effect is a proof for artificially introduced camera shake as a post-processing effect."* This builds on smoke/motion analysis by u/RedDwarfBee/u/Shtudi.
- **Missing parallax in the Skinny Bob body-scan shot**: *"Pivoting the camera (A) should cause perspective distortion (B). Moving the camera vertically (C) should cause parallax (D). The problem is that we neither see perspective distortion nor parallax."* u/RedDwarfBee built physical/3D camera-rig mockups to test this. The site's own conclusion is agnostic, not a hard debunk: *"The reason could be that the camera is simply set up in a way that these effects become small enough to be unrecognizable."*

### 3.4 SFX-Professional Cost Assessment **[F for direct quotes, C for the attribution theory]**

**Ben Philips** (IMDb spelling: "Philips," `imdb.com/name/nm1592943/`), working creature/VFX-effects artist, Reddit handle **u/Bedeekinben**.

**2011 statement** (quoted in full by both checktheevidence.com and Metabunk, originally posted to `reddit.com/r/AliensAndUFOs/comments/bibcmh/skinny_bob_analysis/`):
> "I work in special effects, creature effects and visual effects for the film industry. IMDB me… Ben Philips. I and those I work with could fake this. The problem is I would need a small crew and would have to spend a lot of prep time and money to pull it off."

Shot-by-shot in 2011: the UFO-over-boat shot is *"digital composition using filmed footage and composited UFO with fantastic tracking"*; the walking alien *"could be entirely digital but I think not because the camera shake isn't added as an effect... a makeup (mask) and performer or a digital edit with a CG alien"*; the crash site is *"a physical effect shot… a location build or a miniature model"*; the autopsy *"would require a model alien and performers."* 2011 conclusion: *"if Skinny Bob was faked he's either an animatronic puppet or CGI… or a blend of both… it was done by a multidisciplinary team of effects professionals"* — no dollar figure given at this stage.

**2019 revised statement** (via Metabunk page 2, sourced to Phillips's own April 2019 Reddit post and a later investigative writeup by a co-researcher, `reddit.com/r/SkinnyBob/comments/rhl40z/`, reposted in full by Metabunk user gabelewis on 2022-05-25): Philips revised his estimate upward, from "a couple of people" (2011) to **an entire production team at a cost of £220,000**, and said an NDA would have been necessary for anyone involved. Quote: *"It's very rare for somebody with the talent to be able to create the Skinny Bob clips not to have owned up to it. It's extremely convincing work…"* Proposed method: **"a digitally augmented puppet"** — *"an animatronic puppet, maybe augmented with a bit of digital editing"* — and *"If it's digital I can confidently say it's not hand animated. It's been motion captured or rotoscoped."*

**A speculative attribution theory (explicitly NOT a confirmed identification)**: the Metabunk/Reddit investigator argues Philips himself may be the footage's creator — citing that he re-uploaded Ivan's videos within 6 days of the last original upload, has decades of prop/model work (including a 1990s Roswell-anniversary exhibit with life-size alien models and a 25-foot saucer prop), collects movie puppets (hypothesizing a modified *Mars Attacks!* puppet as a starting point), and made design choices (jumpsuit style, a "Bedeekin" alien alter-ego) that visually resemble Skinny Bob. **This is circumstantial and speculative, not proven.**

**Do not conflate**: u/RedDwarfBee's **$5,000–$30,000 reward offer** (§2) is a bounty for information, entirely separate from Philips's **£220,000 cost-to-fake estimate**.

**A second, independent VFX opinion**, from **Richard Allan** (Post-Production Technical Instructor, Staffordshire University), 2011: *"this alien has too much detail to have been filmed on a cine camera in the 1940s to 1960s timeframe! Look at the veins in the forehead, and the tendons in the neck – there's no way a camera of that era would have picked out that level of detail in that lighting. The 'alien' is a CGI model, with the footage 'distressed' to make it look authentic."*

### 3.5 Alien Anatomy, Blink Rate, Zeta Reticuli, and the 1942–1969 Dating

**Blink/eyelid mechanics — the most contentious anatomical detail [C, disputed even among skeptics themselves]:**
- Metabunk poster **Fin**: *"the blinking is actually the WORST part of this and the most obvious hallmark of CG. When the blink takes place anyone who's ever UV wrapped a head will surely see the issue where the eyebrow part of the skull is stretching, rather than the LID extending… This is a classic UV wrapping/stretching issue!!"*
- Countered by Metabunk poster **gabelewis**: *"it appears that the eyelid is folding under the eyebrow… brow/lid combos like this are not unheard of in nature."*
- skinnybob.info's own reverse-playback test, testing whether Ivan reversed footage for dramatic effect: *"Judging based on human and animal eyelids, the muscle contraction for closing the lid should generally be faster than the relaxation for opening it again."*
- **[S, flagged as low-confidence]**: A Substack post ("Revisiting 'Skinny Bob,'" `uapf.substack.com`, credited to "Jimmy/UAP Files") claims blink-detection tooling (an unnamed "IMG-Detect" tool) found blinks *"minimal and flat, almost like a switch toggling rather than muscles moving"* and returned "1% probability AI-generated." This uses anachronistic 2020s AI-detection terminology on 2011-era footage with no disclosed methodology and could not be corroborated elsewhere — treat as unverified/likely unreliable.

**Other anatomical details [C], via skinnybob.info, credited to named contributors:** black fingernails ("part of obscure, old UFO lore from 1995," per u/Jazzlike_Squirrel); individually-shaped head crests present on other depicted aliens but absent on Skinny Bob himself (noted by contributor "Ralph"); possible forehead bruising/lesions that appear to progress across autopsy frames; an interactive height calculator on the site estimating Skinny Bob at roughly 4'8"–5'6" from hand/body proportions in the autopsy scene; posture identified as classical "contrapposto"; a "stadiometer"-like height-measuring device visible in frame but not matching any known vintage model exactly.

**Zeta Reticuli / dating — clarified as Ivan's own framing, not independent findings [F]:** "Zeta Reticuli" appears only in ivan0135's own video titles/tags — it is Ivan's claim, not a conclusion independently derived by any analyst. (Pre-existing, unrelated background: the Grey-alien/Zeta Reticuli association in general UFO lore originates from Betty Hill's 1961 star-map account, interpreted by schoolteacher Marjorie Fish around 1969 — well-established prior lore, not something skinnybob.info or Metabunk derived from this footage.)

**The 1942–1969 range** is Ivan's own claimed span, stated verbatim in the primary-source text: *"Leaked air force ufo footage. Confidential. Classified document. 1942-1969"* and *"7 video tapes with material recorded between 1942-1969."* **No source ties the "1969" endpoint to any specific historical incident** (it is not connected to Roswell, which is 1947) — the endpoint appears to be an unexplained, self-stated upper bound with no external justification offered anywhere in the sources reviewed. The "Blue Boys" naming (§5.1) creates mild internal tension with this range since Project Blue Book (the likely namesake) only began in 1952 — mid-range, so not a hard contradiction, but flagged by skinnybob.info as suspicious of retrofitted naming.

---

## 4. Provenance and Authorship Theories

**No Wikipedia article exists** for Skinny Bob (`en.wikipedia.org/wiki/Skinny_Bob` returns 404). **No confession has ever surfaced** — this is a consistent negative finding across every source consulted; skinnybob.info explicitly lists "no credible claims of authorship so far" as evidence in the pro-authenticity column of its arguments table.

### 4.1 Claimed geographic/national/linguistic origin

- **[F]** Self-claim only: the channel's own About text says the creator is "from Russia," born 1969 (unverified self-report, not external evidence).
- **[F]** Video 1 opens on a still frame of the KGB insignia, visually reinforcing a Soviet/Russian framing.
- **[C]** The "180 min" tape-duration claim is argued by skinnybob.info to imply **PAL (European) video standard** rather than NTSC (120 min, US) — offered as circumstantial evidence of non-US/European origin, with the explicit caveat that this only holds if "tape" means Video8/Hi8/Digital8 format; VHS/Betamax would invalidate the inference.
- **[C, cuts against the Russian self-claim]**: Reddit's **u/toukoqouko** argued the "desclassified" misspelling more plausibly mirrors Spanish *desclasificado* / Portuguese *desclassificado* than any Russian-language artifact — i.e., linguistic evidence suggesting a Spanish/Portuguese speaker instead of a Russian one.
- **[C]** Reddit's **u/Data_Pure** proposed the upload dates (Apr 13/14, May 2, 9, 18 2011) were deliberately chosen to align with notable dates in Soviet history, jointly with "Ivan" and the KGB logo, to manufacture a Russian-origin impression.
- **[C]** Metabunk poster **FatPhil** separately notes "stiltedness of the English" suggesting a non-native speaker, and flags that the videos appeared in a Russian UFO documentary within roughly a year of upload — hedged explicitly as possibly coincidental re-use rather than proof of authorship.
- **No Estonian-origin claim could be located anywhere**, despite targeted searching — this appears either genuinely absent from the documented record, or confined to inaccessible venues (Reddit/AboveTopSecret full-text search) that could not be verified in this session. **No IP-geolocation claim of any kind** (Estonian, Russian, or otherwise) appears in any accessible source.

### 4.2 The name "Ivan" and the "0135" suffix

- **[C]** Community treatment of "Ivan" leans toward reading it as a deliberate staged signal (paired with the KGB logo and the Soviet-anniversary date theory) rather than a genuine biographical detail; skinnybob.info itself hedges: *"We can't verify if the channel creator and/or uploader is in fact a single individual and really named Ivan. For the sake of simplicity however, we continue to refer to the uploader as Ivan..."*
- **[S]** UFO commentator **Christopher Calder** (OpEdNews) argues the opposite: *"My strong suspicion is that Ivan0135 and compatriots are American citizens with current or past ties to the United States Military, Los Alamos National Laboratory, the CIA, or the NSA,"* and *"The use of the name 'Ivan' may be a simple misdirection to help obfuscate true identity."* Explicitly his own unsupported suspicion.
- **[S, could not confirm the claim even exists]**: no substantive community theory decoding "0135" could be found. It matches none of the tape (01,03,04,05,06) or case (07,15,23,24,25,26) numbers used in the videos. A claim that "0135" encodes GPS coordinates "pointing to West Africa" surfaced in a search-summary but could not be traced to any actual source page — flag as possibly a search-engine confabulation rather than a real documented theory. The mundane default (an arbitrary YouTube-assigned disambiguation suffix) is never explicitly argued for anywhere but remains the unfalsified null hypothesis.

### 4.3 Named individuals proposed as ivan0135

**[C, disputed, actively denied]** The one concrete named lead: **"351NOVA" / "Mr351Nova"**, a prior small-time hoaxer who circulated black-and-white "Area 51 light-being" footage with a blinking-eyed alien, cited (via Metabunk and AboveTopSecret discussion) as stylistically similar. "Mr351Nova" posted a denial on GodlikeProductions: *"This person is slandering me across the net based on a hunch! ... if you look at both sets of videos you can see my old videos were made with windows movie maker, ivan0135 videos are completely professional."* Skeptical rebuttal from poster "Nilbog": *"To me that sounds like what I would say if my previous hoax attempt was exposed and I was liking that my latest one has a lot of people fooled."* Poster "NilbogBackwards": *"I'm 95% sure 'Mr351nova' is involved with Skinny Bob... his youtube channel has changed a lot over the years and so has his name."* 351NOVA is separately documented (Metabunk poster MclachlanM) to have cycled through several handles over the years and to have reused existing TV-documentary clips in his other videos. The specific personal names given in that thread are not reproduced here: the accusation was denied, was never resolved, and naming a private individual on the strength of an unresolved fifteen-year-old forum hunch is not something this document does. **Status: never resolved, disputed, denied by the accused.**

No other real-named individual is proposed anywhere in the accessible record as the person behind ivan0135 (Calder's theory names an institutional affiliation, not a person; the Ben Philips attribution theory in §3.4 is about who *could have made* similar-looking hoax footage generally, developed independently of the 351NOVA lead).

### 4.4 ARG / viral-marketing / art-project connections

- **[C]** The *Super 8* (2011) viral marketing campaign is the one concrete, sourced stylistic parallel: skinnybob.info notes shared elements ("projector rattling, the erratic camera movements and the general 1950s top secret government vibe") and speculates, explicitly as speculation, *"It is possible that Ivan's clips were extracted from a production like this and the movie it was intended to be a trailer for got cancelled."* No direct evidentiary link (credits, personnel, studio confirmation) is offered.
- **[S]** ARG-industry professional **Andrea Phillips** (established transmedia designer, author of *A Creator's Guide to Transmedia Storytelling*, credits include Perplex City, Sony's *The 2012 Experience*, HBO's *Maester's Path*) wrote a multi-part investigative blog series on the case (`secret.works/blog/mddcj21dr7qr32x67kbgzoi57buj7c`) but **explicitly does not claim any personal/professional connection to its creation** — she presents herself as an outside investigator. Her professional background is circumstantially interesting but is not evidence of ARG origin.
- **[S]** A generic, unattributed "student film project" guess recurs across casual commentary with no named film school, filmmaker, or specific project ever proposed.
- No connection to any named art-school thesis or known hoax-collective was found.

### 4.5 Statements from ivan0135 about identity/location

Fully covered verbatim in §1.2 and §1.4 above. The most direct self-statement remains the Video 3 on-screen reply. skinnybob.info notes an internal tension: Ivan put a KGB insignia in Video 1, yet Video 3 claims "There is not any reference which may link the material to any organization that is working today" — read either as self-contradiction or as a deliberate "working today" qualifier implying historical-but-not-current KGB/FSB involvement.

---

## 5. Documented Textual Slip-ups and Catalog Inconsistencies

### 5.1 Anachronisms

- **[C]** "Blue Boys" / "Blue Boys meeting" (Cases 23–24) are argued to derive from **"Little Blue Boys,"** a colloquial nickname (per a cited 1971 Loren E. Gross NICAP report) for U.S. Air Force **Project Blue Book** staff. Problem: Blue Book began in **1952**, and these cases are bundled under the claimed 1942–1969 blanket range with no indication they postdate 1952 specifically — flagged by skinnybob.info as a chronological red flag (with three floated explanations: post-1952 recording, an unknown precursor project, or Ivan unknowingly coining the phrase independently).
- **[C]** Polyethylene plastic, hypothesized present in the "Flying twin" footage, was only industrially available in England from the late 1930s — creates mild tension with any claim the footage originates in the earliest years of the 1942–1969 range. Flagged as "uncertain," not a hard debunk.
- **[S, thinly sourced, could not verify original]** A "CREM alphabet from Reticuli" is said to trace to a 1991 publication (*UFO Afrinews No. 4*), attributed to "Judy Fältskog aka James Van Greunen," and is compared to symbols in the "How to drive" case — if true, an alphabet postdating the claimed 1942-69 window by decades. Could not independently confirm the 1991 publication or named creator.
- **[C]** The **KGB insignia in Video 1 is reportedly lifted from a 1998 hoax documentary**, *The Secret KGB UFO Files* (IMDb tt0224072) — itself separately debunked as a commercial hoax (cited sources: a Komsomolskaya Pravda article and an archived page at `web.archive.org/web/20130324061532/http://boris-shurinov.info/uftnt/tnt2.htm`). This is a provenance anachronism (1998 material presented as if part of an "original" 1940s-60s archive).
- **[C]** The embedded timecode font is Microsoft **Consolas**, released 2006 — treated as decisive proof the timecode graphic was digitally added in post-production, not a period artifact (also covered in §3.2).

### 5.2 Spelling/grammar patterns

All directly verified from the live, primary-source description text pulled in this research (§1.2) unless flagged otherwise:

- **[F]** *"their arrival was been filmed"* (Video 4 description) — a textbook double-auxiliary error, the single cleanest documented grammatical tell in the corpus, confirmed directly from the primary source.
- **[F]** *"1.260 min"* (Videos 1 and 2) — uses a period as a thousands separator (1,260 written as "1.260"), standard in Spanish, Portuguese, German, Russian, and much of continental Europe but nonstandard in English. Directly confirmed from primary text; one of the strongest non-Anglophone-author textual tells available.
- **[C, unable to independently verify]** *"desclassified"* and *"rosswel"* (tag misspellings) — repeatedly cited across secondary sources (checktheevidence.com/skinnybob.info-derived synthesis) but I could not directly pull raw YouTube tag data to reconfirm them myself; flag as widely-repeated-but-not-independently-reverified in this pass.
- **[F]** *"Filtrate for declassification and dissemination..."* (Video 2 on-screen text) — "Filtrate" is an unusual, likely non-native word choice in this context (possible mistranslation of Spanish/Portuguese "filtrar/filtrado" = "to leak/leaked," though no source made this specific etymological claim explicitly — that connection is inference, not a documented community claim).
- **[F]** The double space in *"In  response"* (Video 3 description) — a minor but real, directly-confirmed typo.
- **[C]** General characterization repeated across secondary sources: missing articles and stilted phrasing throughout the on-screen texts, consistent with a non-native English author.

### 5.3 Within-catalog inconsistencies (directly confirmed from primary-source text)

- **[F]** Case numbers increase monotonically without repeats across the shown material — Case 07 (Tape 01) → Case 15 (Tape 03) → Cases 23–24 (Tape 04) → Cases 25–26 (Tape 05) — but with large unexplained gaps (no Cases 1–6, 8–14, 16–22 ever shown). Consistent with Ivan's own framing that these are merely "sample edited fragments," so gaps alone aren't a hard contradiction — but **[C]** skinnybob.info flags that **Tapes 02 and 07 are never sampled at all** across any of the four videos, out of 7 claimed total tapes.
- **[F]** **Tape 06 ("Family vacation") breaks the cataloging convention entirely** — it carries no "Case NN" number at all, unlike every other cataloged clip (Tapes 01/03/04/05 all use "Case NN/Name" format).
- **[F]** Duration math: "Tape duration: 180 min" × 7 claimed tapes = 1,260 minutes, exactly matching the stated "Total recorded duration: 1.260 min" in both Video 1 and Video 2 — implying every one of the seven 180-minute tapes is claimed to be recorded to exact full capacity with zero slack, which skinnybob.info calls suspiciously precise for a claimed real archival log.
- **[C, self-described as unverifiable by its own source]** The "12 minutes" total-footage claim from the 2014 "Will"/PLANETunderATTACK email (§1.4) directly contradicts the 1,260-minute figure — a ~100x discrepancy skinnybob.info says was "never reconciled," while itself flagging the email as anecdotal.
- **[F]** Self-contradiction on organizational ties: Video 1 opens with a KGB insignia image; Video 3's on-screen text states "There is not any reference which may link the material to any organization" — a direct textual/visual tension (see also §4.5).

### 5.4 References to real historical UFO incidents

- **[F]** **None of the four actual video descriptions/on-screen texts mention "Roswell" by name.** The Roswell connection commonly made in press/fan coverage ("a classic Roswell Grey") is entirely a **third-party framing layered on afterward** — e.g. reupload titles like "ROSWELL: Declassified Footage shows 'Skinny Bob'" — not something in Ivan's own primary text. This is itself a notable inconsistency between the popular framing of the case and its actual source material.
- **[F]** No connection to Kecksburg or Rendlesham appears in any source reviewed — a genuine absence, reported as such per the research brief.
- **[F]** Some third-party reupload titles graft in unrelated fringe-ufology terms not present in Ivan's own text (e.g. "Emerther," "Council of Five") — again a marketing/reupload-layer addition, not something from the primary source.

### 5.5 Community-compiled red-flags summary

skinnybob.info functions as the closest thing to a formal checklist. Items it explicitly frames as suspicious/contradictory: the "suspiciously specific" document/treaty numbers ("072/E," "23/04"); the 1,260-vs-12-minute contradiction; the KGB-logo-vs-"no organizational link" self-contradiction; the 2006 Consolas font on 1940s-60s claimed footage; non-native English phrasing including "was been filmed" and the European "1.260 min" notation; the "Blue Boys"/Project Blue Book (1952) naming tension; and the missing Tape 02/07 content plus Tape 06's non-conforming catalog entry.

---

## 6. Access Limitations (for transparency)

- Reddit (including r/SkinnyBob directly) returned HTTP 403 on all direct-fetch and MCP-tool attempts in this research session; all Reddit-sourced material above is relayed second-hand via sites (chiefly skinnybob.info, Metabunk) that quote specific posts/usernames.
- AboveTopSecret.com and GodlikeProductions.com forum threads returned HTTP 403 to direct fetch; content from those venues is relayed via secondary sources that quote them, not independently re-verified against the original thread text.
- YouTube's channel "About" page (JS-rendered), country setting, subscriber count, and raw tag metadata were not obtainable with the tools available this session.
- No contemporaneous (2011/2012) news-reported view-count figures could be located.

## 7. Key Source URLs

- Primary videos: `youtube.com/watch?v=ZB788PtqQvg`, `=RsQCXN4o4Ps`, `=Xju_CY5ZESA`, `=a6TLGkrfNKI`; channel `youtube.com/@ivan0135` (ID `UCC5AjFfZHRvILhJfWw5UcDw`)
- Archive.org mirrors: `archive.org/details/youtube-ZB788PtqQvg` (and `-RsQCXN4o4Ps`, `-Xju_CY5ZESA`, `-a6TLGkrfNKI`)
- `https://skinnybob.info/` — community clearinghouse (source: `github.com/skinnybobinfo/website`)
- `https://www.checktheevidence.com/wordpress/2019/10/31/skinny-bob-alleged-grey-alien-video-leaked-in-2011-analysis/` — Andrew Johnson
- `https://www.metabunk.org/threads/skinny-bob-videos.11760/` and `/page-2`
- `https://www.reddit.com/r/AliensAndUFOs/comments/bibcmh/skinny_bob_analysis/` — Ben Philips, 2011
- `https://www.reddit.com/r/SkinnyBob/comments/rhl40z/` — Philips attribution investigation (reposted in full on Metabunk)
- `https://www.imdb.com/name/nm1592943/` — Ben Philips
- `https://www.youtube.com/watch?v=vZMdgju8t9Q&t=1544` — "Skinny Bob The Truth Revealed – Paranormal (un)Explained #28"
- `https://secret.works/blog/mddcj21dr7qr32x67kbgzoi57buj7c` — Andrea Phillips
- `https://www.opednews.com/populum/page.php?f=Skinny-Bob-The-Forgotten-by-Christopher-Calder-Extraterrestrial_Extraterrestrial-Life_Physics-200624-688.html` — Christopher Calder
- `https://weirddarkness.com/the-skinny-on-skinny-bob/`
- `https://theghostinmymachine.com/2018/07/23/mini-post-skinny-bob-mystery-ivan0135-youtube-roswell-aliens-ufo/`
- `https://extraterrestrials.fandom.com/wiki/Skinny_Bob`
- `https://mysteriesunexplained.com/the-skinny-bob-mystery/`
- `https://uapf.substack.com` — "Revisiting 'Skinny Bob'" (low-confidence source, flagged above)
