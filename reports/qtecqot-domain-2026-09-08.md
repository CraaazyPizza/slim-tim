# qtecqot.com and detomaso.org — public inspection, 2026-09-08

Later [Facebook and Zzuss findings](qtecqot-facebook-zzuss-2026-09-08.md) resolve
the comment date and document the page's previous name and matching website code.

The concrete finding is a hosting relationship: `qtecqot.com` and
`qtecqot.detomaso.org` serve byte-identical HTML and logo files, and the live TLS
certificate covers both. This does not establish who operates the qtecqot YouTube
channel. Footage provenance remains undetermined.

Evidence was fetched on 2026-09-08, approximately 09:04–09:08 UTC, and is stored in
`analysis/domain-qtecqot/2026-09-08/`. Request manifests give exact URLs, response
codes, and collection times. These are local research captures, not a publication
bundle; inspect and select individual files before publishing.

## Verified dates

| Event | UTC | Qualification |
|---|---|---|
| detomaso.org historical homepage | 2001-11-16 | Wayback capture advertises Pantera Owners Club of America. Historical content is not evidence of current ownership. |
| detomaso.org historical registry placeholder | 2024-02-28 and 2025-01-22 | Both captures advertise a DeTomaso automobile registry as coming soon. |
| detomaso.org current registration event | 2026-05-29 11:17:11.912 | Current PIR RDAP record; older captures imply an earlier history. A later registration cycle is a plausible interpretation, not a verified ownership history. |
| qtecqot.com registration | 2026-08-06 13:17:08 | Both Verisign and registrar RDAP agree. |
| Latest qtecqot video publication | 2026-08-25 03:14:43 | Live YouTube RSS, video `bg1BmaF6AJA`. Registration precedes this by 18 days, 13:57:35, rather than exactly two weeks. |
| detomaso.org RDAP last changed | 2026-09-05 06:48:41.770 | Does not identify which registry field changed. |
| Live qtecqot TLS certificate valid from | 2026-09-05 07:11:30 | This certificate's validity start, not the site's first launch. |
| qtecqot.com RDAP last changed | 2026-09-05 07:41:10 | Does not identify which registry field changed. |
| Car placeholder image Last-Modified | 2026-09-05 08:48:36 | Server-supplied file timestamp; not an authenticated creation date. |
| qtecqot logo Last-Modified | 2026-09-06 11:31:46 | Same qualification; copying, deployment or editing can change it. |

The September 5 events suggest setup activity around that day. They do not date
the original creation of the artwork or establish when the site first existed.

Primary records:
[qtecqot registry RDAP](https://rdap.verisign.com/com/v1/domain/qtecqot.com),
[registrar RDAP](https://rdap.instra.com/domain/QTECQOT.COM),
[detomaso registry RDAP](https://rdap.publicinterestregistry.org/rdap/domain/detomaso.org),
[YouTube RSS](https://www.youtube.com/feeds/videos.xml?channel_id=UCw1EA-KJud9OmMA5p7_MWgw).

## Hosting connection

The fetched Let's Encrypt YR1 certificate has these subject alternative names:

```
*.qtecqot.com
qtecqot.com
qtecqot.detomaso.org
www.qtecqot.detomaso.org
```

The certificate expires 2026-12-04 07:11:29 UTC. The original certificate and a
decoded text copy are saved as `certificate.pem` and `certificate.txt`.

The root HTML from qtecqot.com, www.qtecqot.com, qtecqot.detomaso.org, and
qtecqot.com/index.php is identical: 1,940 bytes, SHA-256
`346f27834a2a877ab0fbac2c4de3fae281278b953c40ff72e40a4c201c942792`.
The logo is identical at the qtecqot.com and qtecqot.detomaso.org addresses too.

All three checked names—qtecqot.com, qtecqot.detomaso.org, detomaso.org—resolve to
84.75.144.0. Both parent domains use ns1.naca1.armadaservers.com and
ns2.naca1.armadaservers.com. Reverse DNS gives naca1.armadaservers.com. Both
registrars are Instra Corporation Pty Ltd. The response headers advertise nginx
and, for qtecqot's HTML, PHP/8.3.33. These headers are server assertions.

**Interpretation:** this is consistent with an additional domain configured under
a cPanel account whose primary domain is detomaso.org. cPanel documents the
automatic `addon.primarydomain` subdomain arrangement. This is an inference from
the observed arrangement, not access to the server's configuration. A webmaster
or service provider could manage sites for different people. Same IP or same
registrar alone would be weak evidence; the matching subdomain, certificate and
file hashes are the more specific observations.

Reference: [cPanel domain and virtual-host handling](https://docs.cpanel.net/knowledge-base/cpanel-product/how-your-server-handles-domains-and-virtual-hosts/).

## Logo metadata and encoding

The user's attached `logo.png` is byte-identical to the file fetched from
[the live site](https://qtecqot.com/i/logo.png).

| Property | Result |
|---|---|
| File size | 30,611 bytes |
| Dimensions | 343 × 270 |
| Pixel format | 8-bit RGBA, non-interlaced |
| SHA-256 | `edbcd32c5028c8f65dce41af73e2c4b60c27da2aa1d28f824c6da48e39341f59` |
| Chunk sequence | IHDR, IDAT × 4, IEND |
| IDAT lengths | 8192, 8192, 8192, 5942 bytes |
| Chunk CRCs | All valid |
| Bytes after IEND | 0 |
| Metadata chunks | None in the complete parsed chunk stream |
| Pixel channels | R = G = B in all 92,610 pixels |
| Alpha | 255 in all 92,610 pixels; completely opaque |
| Intensity range | 0–243 |
| Scanline filter | Sub (type 1) for all 270 rows |
| Zlib header | 78 5e |
| Decompressed size | 370,710 bytes, exactly the expected scanlines |
| Unused bytes after compressed stream | 0 |

There are no embedded text, EXIF, XMP, ICC, creation-time, or software-name chunks.
That is an exhaustive structural observation about this PNG, not a claim that it
has no possible pixel-encoded message. No steganographic absence claim is made.
The filter and chunking choices are insufficient to attribute an editor or
generator. An editor/exporter can omit metadata without a separate stripping step.

The logo resembles the lower panel mark in original AVC frame 1694 of
`l9RAhmPHM_A`. An unmodified frame was decoded with ffmpeg 4.4.2 and saved as
`interior-avc-f01694.png`. This inspection does not establish exact artwork identity,
copy direction, a script reading, or access to unpublished footage. The July 24
video already predates the August 6 domain registration, leaving reconstruction
from public footage as an available explanation. No new independent vision
assessment or quantitative matching experiment was performed in this pass.

## Page content and bounded endpoint checks

The homepage contains inline CSS, a Google Fonts stylesheet for Cormorant Garamond,
one image, a Coming Soon heading, and a link from that image to
`https://www.youtube.com/@qtecqot`. The 1,940-byte captured HTML contains no script
elements or analytics identifiers. This observation covers the captured document,
not all possible server content or behavior.

HTTP redirects to HTTPS. `/index.php` serves the homepage. `/index.html`,
`/robots.txt`, `/sitemap.xml`, `/favicon.ico`, and `/.well-known/security.txt`
returned 404. `/i/` returned 403. These are results for those exact requests only;
they are not evidence that no other pages/files exist. No authentication attempts,
exploitation, port scans or directory brute forcing were performed.

The apex has MX `0 qtecqot.com` and SPF allowing A, MX, 84.75.144.0, and
spf.antispamcloud.com with soft fail. These are configuration records, not evidence
of actual email use. The queried AAAA and CAA responses contained no answers for
those types; DNS results are a time-specific snapshot.

The four video descriptions in the fetched YouTube RSS contain zero literal
`qtecqot.com` references. Some explicitly link to x.com/qtecqot. This does not
cover the channel About page, comments, community posts, or the X account.
The website's outgoing YouTube link is therefore not reciprocal authentication
within the inspected RSS material.

## detomaso.org content and history

The current page is a 270-byte HTML wrapper around `/i/comingsoon.jpg`, titled
DeTomaso Registry — Coming Soon. The image advertises an automobile registry and
shows a blue car. It is a 1000 × 838, 129,352-byte baseline JPEG with a JFIF 1.01
header declaring 96 DPI. Pillow reports no EXIF fields; the parsed pre-scan
segments consist of JFIF, quantization/frame/Huffman headers, and scan start.
This does not identify its creator or establish whether generative tools were used.

Historical source pages were downloaded, not inferred from search snippets:

- [2001 homepage](https://web.archive.org/web/20011116204102/http://detomaso.org:80/): Pantera Owners Club of America.
- [2024 homepage](https://web.archive.org/web/20240228182647/https://www.detomaso.org/): a DeTomaso automobile registry advertised as coming soon.
- [2025 homepage](https://web.archive.org/web/20250122175232/https://detomaso.org/): the same registry proposition and coming-soon wording.

The old pages make the automotive theme historically grounded. They do not
establish continuity of ownership across the current 2026 registration event.

## Search coverage and unresolved evidence

The Wayback CDX query for `qtecqot.com/*`, filtered to status 200, returned an empty
array. The urlscan public search returned total 0. The crt.sh wildcard query
returned an empty array; exact qtecqot.com and wildcard detomaso.org requests
returned HTTP 404. These services did not supply certificate history for this
pass. The live certificate is saved directly from the TLS handshake. None of
these results establishes that earlier certificates or captures do not exist.

Web searches for the exact qtecqot domain and the domain pair did not produce a
usable indexed source. Search-engine coverage cannot establish first appearance.

The contributor supplied a Facebook lead during inspection: the page at
`facebook.com/detomaso.org` reportedly commented on reel `1745964936337693` that a
blurred photo shown on a phone was reportedly a still from a qtecqot video. The
comment URL's base64 parameter decodes to
`comment:122128116518775502_27872056109118076`. This encoding contains identifiers,
not a decoded publication date or ownership attestation.

Both supplied Facebook URLs failed in the browsing tool with cache-miss errors.
The contributor subsequently supplied `chrome_yQEypwwsdS.png`, which visibly shows the
DeTomaso.org comment, Facebook's **2w** label, and a page hover card explicitly
listing **detomaso.org** as its website. The card describes a vehicle registry.
This establishes a declared page-to-domain association in the supplied screenshot;
it does not authenticate who controls the domain. The screenshot contains unrelated
private information and is not copied into a publication bundle.

**Correction:** the rounded 2w label cannot establish an exact August 25 date or
the comment's order relative to the August 21 X post. The earlier conversational
estimate was too specific. A later browser pass recovered the actual tooltip:
August 23 at 01:18 UTC, to minute precision; see the linked follow-up report.
No private individual has been identified or contacted.

### Follow-up: the remembered X post exists in the archive

The contributor supplied the Facebook reel's caption: it discusses the older Alien Interview
footage and a podcast guest's assertions about a Groom Lake audiovisual technician.
This is supplied context, not independently retrieved Facebook content.

The existing local archive contains qtecqot post
[2090935518397907328](https://x.com/qtecqot/status/2090935518397907328), dated
**2026-08-21 22:54:09 UTC**:

> When the overlap of this event and #skinnybob are revealed, it will blow people's minds.

`watch/x/api_raw/2090935518397907328.json` records that text, date, and author ID
2048996761101078528 in an official-API response. The parallel
`watch/x/raw/2090935518397907328.json` capture identifies the quoted post as
2090858872151961737, published at 17:49:36 UTC the same day. The quoted post
discusses the same podcast guest's Alien Interview statements and the alleged
Groom Lake audiovisual technician. The official-API capture inspected here does
not itself expand the quote relationship; that context comes from the parallel
capture. A live browser fetch of the qtecqot post returned a cache-miss error.

This supports the contributor's recollection that qtecqot publicly discussed that interview
story. The qtecqot text does not identify the blurred phone image. A Facebook
comment repeating the subject after August 21 could follow publicly available
discussion; it would not, by itself, establish privileged knowledge or shared
account control. The later Facebook report resolves the comment date; the exact target image
remains unverified.

## What would distinguish the remaining explanations

An authenticated link or acknowledgement from the established qtecqot channel
would materially strengthen official affiliation. A verified, dated Facebook
comment plus an explicit website link would strengthen the connection between
that Facebook page and the domain project, but still would not establish footage
authorship. Registration and hosting history could narrow the September setup
timeline. The current evidence is compatible with a creator-run site, a researcher
or fan site, or a site managed for someone else.

The [extended archaeology report](qtecqot-domain-archaeology-2026-09-08.md) adds
the second live certificate, historical server record, archived asset changes,
the supplied ViewDNS history, and the correction identifying the shared August
IP as registrar parking infrastructure.

## Published evidence

See the [evidence index](../analysis/domain-qtecqot/README.md) for the selected
public files and hashes. Some acquisition paths above refer to the larger local
research collection; only files enumerated in the publication manifest are included.
