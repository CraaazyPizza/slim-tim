#!/usr/bin/env python3.12

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

import xwatch


class XWatchTests(unittest.TestCase):
    def test_semantic_revision_ignores_metrics_but_preserves_text_changes(self):
        first = {"data": {"id": "1", "text": "before", "public_metrics": {"like_count": 1}}}
        metrics_only = {"data": {"id": "1", "text": "before", "public_metrics": {"like_count": 2}}}
        edited = {"data": {"id": "1", "text": "after", "public_metrics": {"like_count": 2}}}
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(xwatch, "REVISIONS", tmp):
            path = Path(tmp) / "current.json"
            fresh, revised = xwatch.write_revisioned(
                str(path), first, "1", datetime.now(timezone.utc), "test")
            self.assertEqual((fresh, revised), (True, False))
            fresh, revised = xwatch.write_revisioned(
                str(path), metrics_only, "1", datetime.now(timezone.utc), "test")
            self.assertEqual((fresh, revised), (False, False))
            fresh, revised = xwatch.write_revisioned(
                str(path), edited, "1", datetime.now(timezone.utc), "test")
            self.assertEqual((fresh, revised), (False, True))
            self.assertEqual(json.loads(path.read_text())["data"]["text"], "after")
            self.assertEqual(len(list((Path(tmp) / "1").glob("*.json"))), 2)

    def test_reply_parent_media_is_not_misattributed(self):
        record = {
            "data": {
                "id": "2", "referenced_posts": [{"type": "replied", "id": "1"}],
                "attachments": {"media_keys": ["direct"]},
            },
            "includes": {
                "posts": [{"id": "1", "attachments": {"media_keys": ["parent"]}}],
                "media": [
                    {"media_key": "direct", "url": "https://pbs.twimg.com/direct.jpg"},
                    {"media_key": "parent", "url": "https://pbs.twimg.com/parent.jpg"},
                ],
            },
        }
        media = xwatch.official_media_record(record)["includes"]["media"]
        self.assertEqual([item["media_key"] for item in media], ["direct"])

    def test_media_download_is_published_atomically(self):
        record = {"url": "https://pbs.twimg.com/media/example.jpg"}
        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(xwatch, "MEDIA", tmp), \
                mock.patch.object(xwatch, "get", return_value=b"complete-image"):
            names = xwatch.save_media(record, "123")
            self.assertEqual(names, ["123_1.jpg"])
            self.assertEqual((Path(tmp) / names[0]).read_bytes(), b"complete-image")
            self.assertEqual(list(Path(tmp).glob("*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
