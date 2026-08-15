#!/usr/bin/env python3.12
"""Securely store the official X bearer token without shell-history exposure."""

from __future__ import annotations

import argparse
import getpass
import os
import tempfile
from pathlib import Path

import xapi_client


DESTINATION = Path("~/.config/qtecqot-watch.env").expanduser()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="report whether a token is discoverable without showing it")
    args = parser.parse_args()
    if args.check:
        print("official X bearer token: configured" if xapi_client.bearer_token()
              else "official X bearer token: not configured")
        return

    token = getpass.getpass("Paste the official X Bearer Token (input hidden): ").strip()
    if len(token) < 20 or any(character.isspace() for character in token):
        raise SystemExit("Token was empty or malformed; nothing was written.")
    try:
        lines = DESTINATION.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        lines = []
    lines = [line for line in lines
             if not line.lstrip().startswith(("X_BEARER_TOKEN=", "TWITTER_BEARER_TOKEN="))]
    lines.append(f"X_BEARER_TOKEN={token}")
    DESTINATION.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".qtecqot-watch.", dir=DESTINATION.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write("\n".join(lines) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, DESTINATION)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    print(f"Stored securely at {DESTINATION} (mode 0600); token was not displayed.")


if __name__ == "__main__":
    main()
