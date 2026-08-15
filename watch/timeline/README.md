# Offline @qtecqot timeline

Use <http://127.0.0.1:8765/timeline/>. The loopback-only server also exposes the raw source
records linked from the viewer; it does not expose arbitrary repository files. `index.html` can
still be opened directly and has no external JavaScript/network dependencies beyond local media. External
X and Wayback links are optional conveniences and are not required to browse the copy.

The watcher rebuilds it after every pass. A manual rebuild is also safe:

```bash
cd /home/user/new-skinny-bob/watch
python3.12 build_timeline.py
```

The generator reads:

- `x/state.json` for live/deleted state and observation bounds;
- `x/raw/*.json` for watcher captures and current engagement;
- `x/api_raw/*.json` for official X API timeline records, including replies;
- `x/metrics/*.json` and `x/revisions/*` for throttled engagement history and semantic edits;
- `x/health.json` for current per-leg health rather than mere cron freshness;
- `../qtecqot-x-recovered/raw/*.json` for the recovered Twitter API v2 records;
- `manual_entries.json` for the screenshot-only 2 August deletion whose status ID is unknown.
- `annotations.json` for manually verified relationships or caveats that cannot be safely
  derived from a single record, such as a probable delete-and-repost pair.

Run `python3.12 doctor.py` for a read-only terminal health audit. `keeper.sh` restarts the local
viewer after reboot and reports a fresh-but-degraded watcher as degraded.

Official reply coverage needs an app-only bearer token. Store it without chat/shell-history
exposure with `python3.12 configure_x_token.py`; the helper writes mode-0600 configuration outside
the repository. Never paste credentials into this archive or commit them.

`data.json` is the normalized dataset used by the page. The HTML embeds the same data, so opening
the page through `file://` works without a local web server.

The GitHub Pages edition is a separate, fail-closed build. `timeline/publication.json` explicitly
lists every reviewed entry ID and media hash that may ship; a newly captured post cannot appear
publicly until it is reviewed and added there. Build it into a new or empty directory with:

```bash
python3.12 build_public_site.py /tmp/qtecqot-public
```

The public build deduplicates media by SHA-256, omits local raw-record links and remote avatars,
and emits `publication-manifest.json` enumerating exactly what was included.

Authorship is deliberately conservative. Third-party records observed while enumerating the
account's timeline are labelled as repost/timeline content; they are never rendered as words
authored by @qtecqot. Media included by the API on a reply is not treated as the reply author's
attachment unless the reply itself carries the matching media key.
