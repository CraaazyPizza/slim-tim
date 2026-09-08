# What could “qtecqot” mean?

Investigated 2026-09-08. **Unresolved.** There is a new, exact-spelling radio-code
hypothesis and a separately testable password hypothesis. Neither has supplied an
independent link to the intended meaning. The footage's provenance is undetermined.

## 1. The Quetzalcoatl suggestion has a traceable source, but no derivation

A [Reddit comment](https://www.reddit.com/r/qtecqot/comments/1wacb1j/comment/p8jtq7k/)
reads only “Quetzalcoatl?” It replies to a guess about an ancient American language.
This is a source for the suggestion, not an explanation of the handle. It may be the
comment the investigator had in mind; that identification was not established.

General web searches for the two strings together missed it. Reddit's native
comment search found it. This is a demonstrated search-coverage failure: the first
pass's lack of a search result must not become a claim of no prior discussion.

The [Nahuatl Dictionary](https://nahuatl.wired-humanities.org/content/quetzalcoatl)
records *quetzalcoatl*, *quetzalcouatl*, and *quetzalcohuatl*. The ordinary spelling
has one q, and e precedes the first t. The handle has two q's and t precedes e.
Removing vowels gives `qtzlctl`; alternating letters gives `qezlot` or `utacal`.
None of these exact operations produces the handle.

A deliberately distorted or misremembered allusion remains possible. It cannot be
tested as an exact abbreviation without an independently motivated rule explaining
the deletions, changed order, and extra q. General ancient-astronaut associations
do not supply that rule.

## 2. New candidate: QTE C QOT

All seven letters can be partitioned, unchanged and in order, into defined
radiocommunications signals:

| Part | Established meaning | Limitation |
|---|---|---|
| QTE | True bearing of a station relative to another | A compass direction referenced to true north, not a statement about truthfulness |
| C | Affirmative; can give certain preceding Q groups an affirmative sense | Does not supply a missing numerical bearing |
| QOT | Whether a call is heard and the delay before traffic can be exchanged | Answer/advice form includes an expected delay |

Primary source: [ITU-R M.1172](https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1172-0-199510-I!!PDF-E.pdf),
Annex 1 introduction paragraph 3, QTE and QOT entries, and Section II entry C.
The document also specifies that questions take a question indicator. It does not
define the concatenated string `QTECQOT` as a phrase.

This is a more constrained candidate than inventing seven words whose initials
fit. It explains both q's without a spelling repair. The account's status-report
vocabulary makes a communications reference conceivable.

**It is not a decoded sentence.** “QTE C” is awkward: an affirmative answer does
not answer a request for a bearing. QOT also lacks its delay. A username could
borrow signals loosely, but accepting that adds an assumption. Many Q codes concern
communication, so a broad thematic fit is easy to obtain. There is no basis here
for identifying the operator as a radio professional, military member, or mariner.

Alternative `QTC + QOT` costs a deleted e, so the exact `QTE C QOT` partition is
preferable for investigation. No established source was found defining the whole
concatenation. That statement is limited to the searches and references examined.

## 3. New test surface: the “red pill” description block

The original channel's fourth 2026 upload,
[`bg1BmaF6AJA`](https://www.youtube.com/watch?v=bg1BmaF6AJA), actually contains the
following end to its description, verified directly from the public watch page:

```text
blue pill:
¯\_(ツ)_/¯

red pill:
aRgyjPiynAbJQ1KPAIWoBZuxgKuzBX4a
qfk8XaJsLcfJSI2ymo5AbwWPJE+muMC
8ZP2GBHHHh9cgdNjIbDp/xFp5xPk91F0
u8llj3X7mpTzGzMdA0+bLalGKr4BHYY4k
```

This is not an attribution based on a reupload. The retrieved player response
identified channel `UCw1EA-KJud9OmMA5p7_MWgw`. The selected public fields are held in
[`video-description-2026-09-08.json`](../analysis/handle-origin/video-description-2026-09-08.json).
A [Reddit discussion](https://www.reddit.com/r/qtecqot/comments/1vxxxxc/a_new_video_has_been_released_by_qtecqot/)
had already noticed the block; another commenter suggested the adjacent shrug as
a possible key. This report does not claim those observations as new.

Joining the four lines gives **128 Base64 characters, decoding to 96 bytes**.
Decoded SHA-256:
`48cd09a278502fee33b38159ec08e82f2097d2141947f491759a70cc286c30ad`.
It does not decode directly into UTF-8 prose and does not begin with the OpenSSL
`Salted__` header. Its size is compatible with several encryption layouts, but
does not identify encryption, AES, or any particular format.

This creates a useful hypothesis: **the handle might function as a key rather
than as a word to decode.** A successful decryption with a justified format and
coherent, independently checkable output would be much stronger than resemblance.
Quetzalcoatl and the shrug are also testable password candidates.

### Bounded probes actually run

Thirty explicitly listed candidate passwords, including the two proposed names
and their case/spelling variants, `ivan0135`, SERPO, the exact UTF-8 shrug, and
other terms from the presentation. Candidate recipes include:

- AES ECB/CBC/CFB/OFB with zero-padding, repetition, MD5/SHA-derived keys and
  selected fixed or prefixed IV layouts;
- AES GCM/EAX with prefixed 12/16-byte nonces and two 16-byte tag locations;
- unsalted OpenSSL EVP-style derivation with MD5/SHA-256;
- PBKDF2-HMAC-SHA1/SHA256 at 1,000/10,000/100,000 iterations, with explicitly
  enumerated empty/prefixed-salt and derived/prefixed-IV CBC layouts;
- repeating XOR, RC4, and selected DES/Blowfish layouts.

**6,840 plaintext candidates and 3,360 authenticated-decryption attempts produced
no retained hit.** These are recipe counts, not independent statistical trials.
There were **52 padding-valid checks** among the candidate outputs. None passed
the text filter: padding validity alone would have manufactured false leads.

Positive controls recovered a synthetic SHA256-password/AES-CBC message and
authenticated a synthetic AES-GCM message. The unauthenticated recognition floor
requires UTF-8 text of at least 16 characters with at least 95% printable characters
(including whitespace). Binary/compressed plaintext, shorter text, missing bytes,
other encodings, other derivations, or an untested layout may be missed. These
failures **do not rule out any candidate password across all encryption methods**.

Exact code, recipes, controls and results:
[`probe_red_pill.py`](../analysis/handle-origin/probe_red_pill.py),
[`red-pill-results.json`](../analysis/handle-origin/red-pill-results.json).

## 4. Re-running and extending the old letter tests

The earlier dossier listed failed transformations without a retained executable
test package. This pass records a finite experiment using a hash-pinned copy of
[`dwyl/english-words/words_alpha.txt`](https://github.com/dwyl/english-words).
It contains 370,105 entries; it is a word list, not a complete linguistic lexicon.

- All 312 invertible affine letter maps, including Caesar and Atbash, in both
  forward and reversed order: **624 recipes, no exact dictionary match**.
- Anagrams and T9 `7832768`: no exact match in this dictionary.
- Russian keyboard mapping gives `йеусйще`; the script also records Dvorak,
  Colemak, horizontal QWERTY shifts and QWERTY/alphabet ordinal maps.
- Twelve explicit letter keys in Vigenere forward/reverse and Beaufort operations,
  plus ten digit keys in both Gronsfeld directions: no exact dictionary match.
  Date keys longer than seven characters can produce identical outputs because
  only the first seven positions are used. They are not independent evidence.

The pattern is `A B C D A E B`. **Sixty dictionary entries share it**, including
`traitor`, `tractor`, `astrals`, `ceviche`, `recurse`, and `remorse`. Thus even an
apparently relevant English output is not unique. A freely chosen substitution key
is insufficient to identify the intended plaintext. No particular person is
implicated by any dictionary entry.

Known synthetic Caesar/affine/reversed-affine encodings of `contact` were recovered;
the T9 control also passed. The negative results apply only to exact dictionary
membership within these finite families. They say nothing conclusive about private
mnemonics, other languages, misspellings, or an unconstrained cipher.

Code and outputs: [`check_handle.py`](../analysis/handle-origin/check_handle.py),
[`results.json`](../analysis/handle-origin/results.json).

## 5. Account-text check and remaining uncertainty

The local capture timeline examined contained 54 entries. Excluding reposts and
manual entries left **44 authored X text records, 869 whitespace-separated words**,
with the latest authored record dated 2026-09-06. Selected topic terms for the two
name hypotheses produced no literal match; a within-post word-initial search did
not produce the handle. The exact regex, selected IDs, source generation time and
SHA-256 are in `results.json`. No text or media was copied from that archive into
this report without separate selection.

The scope is held text. It excludes words rendered inside pictures, untranscribed
audio, uncaptured deletions, and unstated personal associations. It is not a
semantic detector and supplies no strong evidence against either allusion.

The recovered April 28 first post already carries `qtecqot`; the older claim that
the string first appeared publicly on May 25 is superseded by that record. An
empty memory.lol response was re-observed on September 8, but cannot establish an
absence of earlier aliases or accounts outside that service's coverage.

## Assessment

The most useful new direction is testing candidate meanings as keys against the
actual description block. The exact-spelling radio partition deserves retention
as a hypothesis, with its grammatical problems attached. Quetzalcoatl remains a
possible private allusion without a derivation. An opaque alias or private mnemonic
remains an adequate null explanation; the evidence does not establish randomness.

A persuasive result would need a rule grounded outside the seven-letter handle
and a check on a second artifact. The work here found no such result. None of the
name hypotheses changes the assessment of the footage's provenance.
