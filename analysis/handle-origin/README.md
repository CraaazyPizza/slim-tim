# Handle-origin checks — 2026-09-08

Read [the report](../../reports/qtecqot-handle-2026-09-08.md). No meaning was established.

Included files are explicitly selected: two scripts, their two JSON outputs,
selected public YouTube description fields, and this README. No screenshots,
account credentials, private identifiers or raw third-party profile collections
are included. The local capture timeline used for the text audit is not included.

## Reproduce

The letter experiment uses Python 3.12 standard library only. Fetch
`https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt` into a
scratch location. The script checks SHA-256
`3ed0c94610d8bcf7c11bbb49c56aa49c7234d32b66824df91f554169e572da48`
and stops if the dictionary changes.

```sh
python3.12 analysis/handle-origin/check_handle.py /tmp/qtecqot-words-alpha.txt
```

Optionally add `--timeline ../new-skinny-bob-capture/watch/timeline/data.json` for
the held-text checks. This input is local and changes as captures arrive. Its hash,
generation time and selected status IDs are recorded in the existing result file.
That file is not a claim to hold every public post ever made.

The binary probes require PyCryptodome 3.23.0, added through `uv add` to the shared
tools project's `pyproject.toml` and `uv.lock`. No system Python installation is used.

```sh
uv run --project /home/user/tools/devpc-python python \
  /home/user/new-skinny-bob/analysis/handle-origin/probe_red_pill.py \
  /home/user/new-skinny-bob/analysis/handle-origin/video-description-2026-09-08.json
```

Each command writes JSON to stdout. The report documents positive controls and
the recognition limits. A negative dictionary or plaintext-filter result is not
an exhaustive failure to decode; a valid padding byte is not a successful decode.
