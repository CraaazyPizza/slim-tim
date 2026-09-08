import json
import tempfile
import unittest
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

import archive_assets
import build_timeline
import xwatch
import youtube_archive
import watch
import serve_timeline


class ArchiveTests(unittest.TestCase):
    def test_recovered_list_record_can_be_swept(self):
        direct, context = xwatch.media_groups([{"url": "https://pbs.twimg.com/a.jpg"}])
        self.assertEqual(xwatch.media_urls(direct), ["https://pbs.twimg.com/a.jpg"])
        self.assertEqual(context, {})

    def test_local_server_confines_routes_to_archive_trees(self):
        handler = serve_timeline.ArchiveHandler.__new__(serve_timeline.ArchiveHandler)
        self.assertTrue(handler.translate_path("/youtube/videos/a/description.txt").endswith("description.txt"))
        self.assertTrue(handler.translate_path("/youtube/%2e%2e/%2e%2e/.git/config").endswith(".route-not-found"))

    def test_media_reordering_and_edits_cannot_reuse_wrong_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp) / "media"
            urls = ["https://pbs.twimg.com/media/b.jpg", "https://pbs.twimg.com/media/c.jpg"]
            fetch = lambda url: url.encode()
            first = archive_assets.capture(media, "1", urls, fetch)
            edited = archive_assets.capture(media, "1", ["https://pbs.twimg.com/media/a.jpg", *urls], fetch)
            self.assertEqual(first[0]["file"], edited[1]["file"])
            self.assertNotEqual(first[0]["file"], edited[0]["file"])
            for item in edited:
                self.assertEqual((media / item["file"]).read_bytes(), item["url"].encode())

    def test_small_images_request_original_and_timeout_remains_retryable(self):
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp) / "media"
            url = "https://pbs.twimg.com/media/photo?format=png&name=small"
            def fail(url):
                raise TimeoutError()
            item = archive_assets.capture(media, "1", [url], fail)[0]
            self.assertEqual(item["status"], "retry")
            item = archive_assets.capture(media, "1", [url], lambda url: b"image")[0]
            self.assertEqual(item["url"], "https://pbs.twimg.com/media/photo?format=png&name=orig")
            self.assertEqual(item["status"], "held")

    def test_corrupt_existing_asset_is_refetched(self):
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp) / "media"
            fetch = mock.Mock(return_value=b"complete")
            item = archive_assets.capture(media, "1", ["https://pbs.twimg.com/a.jpg"], fetch)[0]
            (media / item["file"]).write_bytes(b"broken!!")
            archive_assets.capture(media, "1", ["https://pbs.twimg.com/a.jpg"], fetch)
            self.assertEqual(fetch.call_count, 2)
            self.assertEqual((media / item["file"]).read_bytes(), b"complete")

    def test_context_media_is_preserved_separately(self):
        rec = {"data": {"id": "1", "attachments": {"media_keys": ["direct"]}},
               "includes": {"media": [{"media_key": "direct", "url": "https://pbs.twimg.com/d.jpg"},
                                      {"media_key": "parent", "url": "https://pbs.twimg.com/p.jpg"}]}}
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(xwatch, "MEDIA", str(Path(tmp) / "media")), \
                mock.patch.object(xwatch, "get", side_effect=lambda url, **kw: url.encode()):
            xwatch.save_media(rec, "1")
            direct = archive_assets.read_manifest(Path(tmp) / "media", "1")["assets"]
            context = archive_assets.read_manifest(Path(tmp) / "media", "1-context")["assets"]
            self.assertEqual(list(direct), ["https://pbs.twimg.com/d.jpg"])
            self.assertEqual(list(context), ["https://pbs.twimg.com/p.jpg"])

    def test_mirror_http_200_without_correct_post_is_rejected(self):
        for payload in ({"code": 404}, {"code": 200}, {"tweet": {"id": "wrong"}}):
            with mock.patch.object(xwatch, "get", return_value=payload):
                self.assertNotEqual(xwatch.fetch_status("qtecqot", "1")[1], 200)

    def test_youtube_description_revision_retains_both_versions(self):
        now = datetime.now(timezone.utc)
        vid = "12345678901"
        def page(description):
            player = {"videoDetails": {"videoId": vid, "channelId": youtube_archive.CHANNEL_ID,
                                       "title": "title", "shortDescription": description}}
            return ("var ytInitialPlayerResponse = " + json.dumps(player) + ";").encode()
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(youtube_archive, "ROOT", Path(tmp)), \
                mock.patch.object(youtube_archive, "fetch", side_effect=[page("before"), page("after")]):
            youtube_archive.capture_video(vid, now)
            youtube_archive.capture_video(vid, now)
            directory = Path(tmp) / "videos" / vid
            self.assertEqual((directory / "description.txt").read_text(), "after")
            self.assertEqual(len(list((directory / "revisions").glob("*.json"))), 2)
            self.assertEqual(len(list((directory / "pages").glob("*.gz"))), 2)

    def test_rss_failure_retains_last_successful_channel(self):
        old = {"channel_title": "qtecqot", "channel_published": "then", "videos": {}}
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(watch, "ROOT", tmp), \
                mock.patch.object(watch, "SNAPS", str(Path(tmp) / "snapshots")), \
                mock.patch.object(watch, "CHANGELOG", str(Path(tmp) / "CHANGELOG.md")), \
                mock.patch.object(watch, "CHANNELS", {"qtecqot": "channel"}), \
                mock.patch.object(watch, "fetch", side_effect=TimeoutError()), \
                mock.patch.object(watch.youtube_archive, "run", return_value=([], {})), \
                mock.patch("sys.argv", ["watch.py", "--quiet"]):
            (Path(tmp) / "latest.json").write_text(json.dumps({"channels": {"qtecqot": old}}))
            watch.main()
            current = json.loads((Path(tmp) / "latest.json").read_text())
            self.assertEqual(current["channels"]["qtecqot"], old)
            self.assertIn("qtecqot", current["errors"])


if __name__ == "__main__":
    unittest.main()
