#!/usr/bin/env python3.12

import io
import json
import tempfile
import unittest
import urllib.parse
from pathlib import Path

import xapi_client


class Response(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


class XApiClientTests(unittest.TestCase):
    def test_credentials_file_is_parsed_without_shell_evaluation(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "watch.env"
            path.write_text("# comment\nX_BEARER_TOKEN='secret value'\n", encoding="utf-8")
            self.assertEqual(xapi_client.load_env_value("X_BEARER_TOKEN", (path,)), "secret value")

    def test_full_timeline_paginates_and_keeps_reply_context_and_media(self):
        calls = []
        first = {
            "data": [{
                "id": "2000000000000000002", "text": "@somebody reply", "author_id": "42",
                "in_reply_to_user_id": "7", "created_at": "2026-08-15T00:00:00Z",
                "attachments": {"media_keys": ["3_direct"]},
                "referenced_tweets": [{"type": "replied_to", "id": "1999999999999999999"}],
            }],
            "includes": {
                "users": [{"id": "42", "username": "qtecqot"}, {"id": "7", "username": "somebody"}],
                "tweets": [{"id": "1999999999999999999", "author_id": "7",
                            "attachments": {"media_keys": ["3_parent"]}}],
                "media": [{"media_key": "3_direct", "type": "photo", "url": "https://pbs.twimg.com/a.jpg"},
                          {"media_key": "3_parent", "type": "photo", "url": "https://pbs.twimg.com/b.jpg"}],
            },
            "meta": {"newest_id": "2000000000000000002", "oldest_id": "2000000000000000002",
                     "next_token": "next-page"},
        }
        second = {
            "data": [{"id": "2000000000000000001", "text": "older", "author_id": "42"}],
            "includes": {"users": [{"id": "42", "username": "qtecqot"}]},
            "meta": {"newest_id": "2000000000000000001", "oldest_id": "2000000000000000001"},
        }

        def opener(request, timeout):
            calls.append((request, timeout))
            query = urllib.parse.parse_qs(urllib.parse.urlparse(request.full_url).query)
            payload = second if query.get("pagination_token") == ["next-page"] else first
            return Response(json.dumps(payload).encode())

        result = xapi_client.get_user_posts(
            "42", "token", "2026-08-15T01:00:00Z", full_backfill=True, opener=opener)
        self.assertEqual(result.pages, 2)
        self.assertTrue(result.complete)
        self.assertEqual(set(result.records), {"2000000000000000001", "2000000000000000002"})
        record = result.records["2000000000000000002"]
        self.assertEqual(len(record["includes"]["media"]), 2)
        self.assertEqual(len(record["includes"]["tweets"]), 1)
        self.assertNotIn("exclude", urllib.parse.parse_qs(urllib.parse.urlparse(calls[0][0].full_url).query))
        query = urllib.parse.parse_qs(urllib.parse.urlparse(calls[0][0].full_url).query)
        self.assertIn("post.fields", query)
        self.assertNotIn("tweet.fields", query)
        self.assertIn("referenced_posts", query["expansions"][0])
        self.assertEqual(calls[0][0].get_header("Authorization"), "Bearer token")

    def test_current_post_schema_keeps_repost_context(self):
        payload = {
            "data": [{
                "id": "2000000000000000003", "text": "repost wrapper", "author_id": "42",
                "referenced_posts": [{"type": "reposted", "id": "2000000000000000000"}],
            }],
            "includes": {
                "posts": [{
                    "id": "2000000000000000000", "author_id": "8",
                    "attachments": {"media_keys": ["3_video"]},
                }],
                "users": [{"id": "42", "username": "qtecqot"},
                          {"id": "8", "username": "original"}],
                "media": [{"media_key": "3_video", "type": "video",
                           "preview_image_url": "https://pbs.twimg.com/preview.jpg"}],
            },
            "meta": {"newest_id": "2000000000000000003"},
        }

        def opener(_request, timeout):
            self.assertEqual(timeout, 30)
            return Response(json.dumps(payload).encode())

        result = xapi_client.get_user_posts(
            "42", "token", "now", full_backfill=False, opener=opener)
        record = result.records["2000000000000000003"]
        self.assertEqual(record["includes"]["posts"][0]["id"], "2000000000000000000")
        self.assertEqual(record["includes"]["media"][0]["media_key"], "3_video")

    def test_recent_poll_is_one_page_even_if_next_token_exists(self):
        payload = {
            "data": [{"id": "2000000000000000002", "text": "latest", "author_id": "42"}],
            "meta": {"newest_id": "2000000000000000002", "next_token": "ignored"},
        }
        calls = []

        def opener(request, timeout):
            calls.append(request.full_url)
            return Response(json.dumps(payload).encode())

        result = xapi_client.get_user_posts(
            "42", "token", "now", full_backfill=False, max_results=5,
            since_id="2000000000000000001", opener=opener)
        self.assertEqual(len(calls), 1)
        self.assertFalse(result.complete)
        self.assertEqual(result.result_count, 1)
        query = urllib.parse.parse_qs(urllib.parse.urlparse(calls[0]).query)
        self.assertEqual(query["since_id"], ["2000000000000000001"])


if __name__ == "__main__":
    unittest.main()
