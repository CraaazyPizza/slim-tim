#!/usr/bin/env python3.12
"""Serve the offline timeline and all of its local evidence on localhost.

The generated page lives under watch/, while recovered API records live beside
watch/. SimpleHTTPServer rooted at either directory therefore leaves some source
links broken. This small server keeps the short /timeline/ URL and explicitly maps
only the three archive trees the viewer uses.
"""

from __future__ import annotations

import argparse
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlsplit


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)


class ArchiveHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path: str) -> str:
        clean = unquote(urlsplit(path).path)
        if clean == "/":
            clean = "/timeline/"
        if clean == "/timeline":
            clean = "/timeline/"
        if clean.startswith("/timeline/"):
            relative = os.path.join("watch", clean.lstrip("/"))
        elif clean.startswith("/x/"):
            relative = os.path.join("watch", clean.lstrip("/"))
        elif clean.startswith("/qtecqot-x-recovered/"):
            relative = clean.lstrip("/")
        else:
            return os.path.join(REPO, ".route-not-found")
        target = os.path.realpath(os.path.join(REPO, relative))
        if os.path.commonpath((REPO, target)) != REPO:
            return os.path.join(REPO, ".route-not-found")
        return target

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bind", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.bind, args.port), ArchiveHandler)
    print(f"@qtecqot offline timeline: http://{args.bind}:{args.port}/timeline/", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
