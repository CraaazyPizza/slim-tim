# Website archaeology — 2026-09-08

**Later update:** [Facebook browser access and the Zzuss predecessor](qtecqot-facebook-zzuss-2026-09-08.md)
resolve the comment date, recover the page-name history and connect the older
shopping-site code to the automotive frontend. Earlier unresolved-date statements
below describe the stage before that acquisition.

This extends [the initial domain report](qtecqot-domain-2026-09-08.md).
Evidence and request manifests are stored under
`analysis/domain-qtecqot/archaeology-2026-09-08/`. Raw captures are local research
material, not a reviewed publication bundle. Footage provenance remains undetermined.

The strongest result remains a specific current hosting relationship. The new
work strengthens that result, establishes a longer automotive-site history, and
identifies a false lead: the shared August IP is registrar parking infrastructure.

## Both live certificates link the projects

[Cert Spotter's public endpoint](https://api.certspotter.com/v1/issuances?domain=detomaso.org&include_subdomains=true&expand=dns_names&expand=issuer)
returned these records:

| Validity start UTC | Issuer | Names |
|---|---|---|
| 2025-12-16 00:00:00 | Sectigo | *.detomaso.org, detomaso.org |
| 2026-02-08 00:00:00 | Sectigo | *.detomaso.org, detomaso.org |
| 2026-09-05 06:12:12 | Let's Encrypt YR1 | *.detomaso.org, detomaso.org, www.qtecqot.detomaso.org |
| 2026-09-05 07:11:30 | Let's Encrypt YR1 | *.qtecqot.com, qtecqot.com, qtecqot.detomaso.org, www.qtecqot.detomaso.org |

The detomaso.org TLS endpoint directly served the third certificate, whose
SHA-256 fingerprint matches the returned entry:
`415f32ff8ca4f51f1b8d7437360fcf2fc56c42b08b526b74061c668e5b991c7c`.
The qtecqot certificate was already obtained in the first pass. This means the
connection is present in the car site's certificate as well as the qtecqot site's.
The September validity starts are 59 minutes, 18 seconds apart: consistent with
related provisioning, but not exact issuance or logging times.

The returned set is not assumed to contain every historical certificate.
The two older certificates establish earlier certificate activity for the car
domain, not continuity of its operator across its current May 2026 registration.

DNS controls queried `research-control-20260908` beneath each domain. Both A-record
queries returned NXDOMAIN. Thus the observed qtecqot subdomain is not explained
by a blanket A-record wildcard at either parent in these checks. Its explicit
appearance in the certificates remains the more specific evidence.

Both domains advertise identical SPF strings and analogous self-addressed MX
records. These may be hosting defaults and carry little extra attribution weight.

## The shared August IP is a parking server

The contributor supplied ViewDNS IP-history tables after the browsing tool could not open
the service. These are user-transcribed service results, not a direct API capture.

| Domain | IP | Provider in supplied table | Last seen |
|---|---|---|---|
| qtecqot.com | 198.50.252.64 | OVH SAS, Canada | 2026-08-07 |
| detomaso.org | 198.50.252.64 | OVH SAS, Canada | 2026-08-10 |
| detomaso.org | 65.21.178.24 | Hetzner, Finland | 2026-03-13 |
| detomaso.org | 217.160.0.41 | IONOS, Germany | 2026-02-27 |
| detomaso.org | 74.208.236.189 | IONOS, United States | 2026-02-20 |
| detomaso.org | 74.208.236.215 | IONOS, United States | 2025-12-19 |
| detomaso.org | 65.60.61.97 | SINGLEHOP, United States | 2024-12-27 |
| detomaso.org | 91.195.240.117 | SEDO, Germany | 2023-11-26 |

The supplied car-domain table has 22 entries, including earlier Aruba and
Internap addresses. A structured transcription retains all 22 domain-hosting rows
and excludes unrelated information pasted from the site's footer.

**Retraction of the immediate conversational inference:** the shared August IP
was initially described as materially strengthening an early joint-administration
link. A control check showed why that inference was too strong:

- [ARIN RDAP](https://rdap.arin.net/registry/ip/198.50.252.64) assigns the
  198.50.252.64–198.50.252.71 customer block to **Instra Corporation Pty Ltd**.
- Public HTTP requests for each domain, resolving it to 198.50.252.64, return
  **Domain parked by OnlyDomains**. Both responses were saved, with headers.
- Both domains already share Instra as registrar.

The historical IP match is therefore compatible with ordinary registrar parking
for unrelated customers. It does not establish a shared hosting account in August.
The current response from the old IP is not a historical August page capture:
parking at the historical observation dates is a supported interpretation, not
directly observed historical content.

ViewDNS reports **last seen**, not first seen, exact migration time or continuous
occupancy. Its table also omits the current 84.75.144.0 address. We cannot turn its
rows into a complete day-by-day timeline. Server country does not locate an operator.

## Direct evidence of an older server

Common Crawl collection CC-MAIN-2025-43 records a homepage response at
**2025-10-09 11:03:14 UTC** with:

```
WARC-IP-Address: 74.208.236.215
WARC-Target-URI: https://detomaso.org/
WARC-Date: 2025-10-09T11:03:14Z
```

The index-provided WARC object was retrieved with an HTTP Range request for
2,633 bytes at offset 211175730. The original compressed and decompressed records
are saved. ARIN labels the enclosing network `1AN1-NETWORK`. Current DNS resolves
the site to 84.75.144.0, so the serving IP changed between the observations.
This agrees with the supplied ViewDNS history's inclusion of the old address.

The October Wayback capture is the **same underlying Common Crawl observation**,
not an independent second witness. Both indexes carry payload digest
`IB6PA2IB7BBUEUPQGJHCZFVH5BYGJ74Y`.
The recovered 4,689-byte HTML is byte-identical to the Wayback response, and its
computed base32 SHA-1 matches that recorded digest (`warc-integrity.json`).

A few public requests using the historical domain Host header against the old
server did not recover the missing artwork: root returned 403, the old stylesheet
path returned 404, and the old `/i/logo.png` path redirected to `/logo.png`, which
returned 404. No neighbouring virtual hosts, credentials or private files were queried.

## The car-registry branding has a development history

The wildcard Wayback query returned 178 distinct status-200 URLs after collapsing
by URL key. Many belong to the 2001–2002 car-club site. A separate query since 2023
returned 11 monthly-collapsed root observations from February 2024 to October
2025, plus asset and service records. These are counts for specified queries,
not claims of complete coverage.

The fetched 2024 and 2025 stylesheets differ, with additions for cart, search and
other buttons. The root source retains a commented-out logo labelled
**Shopping made Smooth**. February 2024 keywords include shopping, marketplace,
auctions and portal terms; January 2025 keywords instead describe cars. The later
description also includes **Celebrating Legends!**, wording visible in the contributor's
Facebook screenshot.
Comparing the January and October 2025 root HTML shows only a background-gradient
colour change; those two captures do not demonstrate new site functionality.

The June 2024 `/i/favicon.ico` response is a 16×16 GIF containing an A-like mark.
The July 2025 response is a 16×16 ICO with a DeTomaso-style badge. Original files
and lossless PNG extractions are saved. The tiny earlier mark is not attributed
to a specific company or person.

These details fit adaptation from a shopping-oriented codebase and subsequent
editing of the automotive project. Searches for the wording and distinctive CSS
selectors did not identify an original template. The code does not identify a
developer or connect them to footage production.

The current car homepage is a different implementation: a short HTML wrapper
around one JPEG. The old CSS, favicon and commented-out logo paths return 404
on the current host. Those endpoint checks are not evidence that every old asset
has been removed. Older branding could have been retained by a later operator;
current registration data prevents assuming uninterrupted ownership.

## Social evidence and dates

the contributor's supplied screenshot shows the DeTomaso.org Facebook page commenting on
qtecqot footage and explicitly listing detomaso.org as its website. This is a
declared association, beyond merely sharing a name. The **2w** label is rounded.
It does not establish an August 25 date or whether the comment followed the
August 21 qtecqot X post. That earlier date estimate is withdrawn.

A search-provider result for a [Nevada Coin Mart review page](https://nevadacoinmart.com/reviews/facebook-reviews/page/9/)
lists a DeTomaso.org review dated January 3, 2025. This establishes what the
secondary page presents, not the original Facebook post date, historical display
name or page-ID continuity. Direct curl access returned 403. It is a low-weight
lead; no private person's identity, location or transactions are inferred.

## Coverage limits and remaining discriminators

Common Crawl supplied the October 2025 record and no-capture responses for several
later queried collections. Seven queries returned 503: 2026-08, 2026-04, 2025-51,
2025-47, 2025-38, 2025-33 and 2025-30. Those are service failures, not negatives.
The latest collection query for qtecqot.com returned no captures, and public
urlscan returned total 0 for the car domain. Query manifests retain the scope.

The user-supplied IP histories resolve part of the historical-DNS access gap.
Historical nameserver/WHOIS changes could still narrow continuity. The later
Facebook report supplies Page Transparency and the exact displayed comment time. A verified reciprocal
endorsement from the established qtecqot accounts would address official affiliation.

A [similar lower-panel mark in the July 24 footage](../analysis/domain-qtecqot/2026-09-08/interior-avc-f01694.png)
predates domain registration by about 13 days. An exact match to the website logo
has not been established. Domain registration itself precedes the latest
video, but none of the inspected records dates the **custom logo page** before
that release. A clean reconstruction from public footage remains possible.

The strongest working inference is coordinated current administration of the
car-registry and qtecqot websites. The evidence does not yet distinguish the
video uploader's own site from an enthusiast's project or third-party management.

## Published evidence

See the [evidence index](../analysis/domain-qtecqot/README.md) for the selected
public files and hashes. Some acquisition paths above refer to the larger local
research collection; only files enumerated in the publication manifest are included.
