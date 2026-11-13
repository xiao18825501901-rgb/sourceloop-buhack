import json
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from tempfile import TemporaryDirectory

from sourceloop.app import create_server
from sourceloop.content import load_curated_pack


DATA_PATH = Path(__file__).resolve().parents[1] / "sourceloop" / "data" / "campus_routes.json"


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = TemporaryDirectory()
        cls.runtime_dir = Path(cls.temp_dir.name) / "runtime"
        cls.server = create_server(
            host="127.0.0.1",
            port=0,
            runtime_dir=cls.runtime_dir,
        )
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_address[1]}"
        cls.pack = load_curated_pack(DATA_PATH)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)
        cls.temp_dir.cleanup()

    def request(self, method, path, body=None, content_type="application/json", raw=None):
        headers = {"Content-Type": content_type, "Origin": self.base_url}
        payload = raw
        if raw is None and body is not None:
            payload = json.dumps(body).encode("utf-8")
        request = urllib.request.Request(
            self.base_url + path,
            data=payload,
            headers=headers,
            method=method,
        )
        try:
            response = urllib.request.urlopen(request, timeout=5)
            return response.status, dict(response.headers), response.read()
        except urllib.error.HTTPError as error:
            return error.code, dict(error.headers), error.read()

    def json_request(self, method, path, body=None, raw=None):
        status, headers, payload = self.request(method, path, body=body, raw=raw)
        return status, headers, json.loads(payload.decode("utf-8"))

    def correct_answers(self, lesson_id):
        lesson = next(
            item for item in self.pack["lessons"] if item["id"] == lesson_id
        )
        return {
            question["id"]: question["answer"] for question in lesson["questions"]
        }

    def test_health_reports_database_ready_with_security_headers(self):
        status, headers, payload = self.json_request("GET", "/api/health")

        self.assertEqual(status, 200)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["database"], "ready")
        self.assertIn("default-src 'self'", headers["Content-Security-Policy"])
        self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
        self.assertNotIn("Access-Control-Allow-Origin", headers)

    def test_public_pack_never_leaks_answers(self):
        status, _, payload = self.json_request("GET", "/api/packs/campus-routes")
        serialized = json.dumps(payload)

        self.assertEqual(status, 200)
        self.assertEqual(payload["pack"]["id"], "campus-routes")
        self.assertNotIn('"answer"', serialized)
        self.assertNotIn('"explanation"', serialized)
        self.assertEqual(payload["review_count"], 0)
        self.assertTrue(payload["pack"]["sources"])
        visual = payload["pack"]["lessons"][1]["visual"]
        self.assertEqual(visual["trace"]["distance"], 9)
        self.assertEqual(visual["trace"]["path"], ["LIB", "CAN", "LAB"])
        self.assertTrue(visual["trace"]["steps"])

    def test_wrong_attempt_creates_one_source_linked_review_item(self):
        answers = self.correct_answers("read-the-network")
        answers["cost-sum"] = "a"

        status, _, attempt = self.json_request(
            "POST",
            "/api/attempts",
            {
                "pack_id": "campus-routes",
                "lesson_id": "read-the-network",
                "answers": answers,
            },
        )

        self.assertEqual(status, 200)
        self.assertEqual(attempt["score"], 2)
        self.assertEqual(attempt["total"], 3)
        self.assertEqual(attempt["review_count"], 1)
        wrong_result = next(
            result for result in attempt["results"] if not result["is_correct"]
        )
        self.assertEqual(wrong_result["source"]["code"], "S2")
        self.assertTrue(wrong_result["explanation"]["en"])

        status, _, review = self.json_request("GET", "/api/review")
        self.assertEqual(status, 200)
        self.assertEqual(len(review["items"]), 1)
        self.assertEqual(review["items"][0]["source"]["code"], "S2")
        self.assertEqual(review["items"][0]["pack_id"], "campus-routes")

    def test_correct_retry_resolves_the_same_review_item(self):
        status, _, attempt = self.json_request(
            "POST",
            "/api/attempts",
            {
                "pack_id": "campus-routes",
                "lesson_id": "read-the-network",
                "answers": self.correct_answers("read-the-network"),
            },
        )

        self.assertEqual(status, 200)
        self.assertEqual(attempt["score"], 3)
        self.assertEqual(attempt["review_count"], 0)

        _, _, review = self.json_request("GET", "/api/review")
        self.assertEqual(review["items"], [])

    def test_import_persists_and_is_publicly_retrievable(self):
        notes = """
# Memory and Retrieval

## Encoding

Encoding forms a memory trace. Attention decides which details enter it.

## Retrieval

Attempting recall before seeing the answer strengthens later access.

## Spacing

Distributed practice separates study episodes across time.
""".strip()

        status, _, result = self.json_request(
            "POST",
            "/api/import",
            {"title": "Imported memory notes", "text": notes},
        )
        self.assertEqual(status, 201)
        pack_id = result["pack_id"]
        self.assertTrue(pack_id.startswith("import-"))

        status, _, response = self.json_request("GET", f"/api/packs/{pack_id}")
        self.assertEqual(status, 200)
        self.assertEqual(response["pack"]["origin"], "imported")
        self.assertEqual(len(response["pack"]["lessons"]), 3)
        self.assertNotIn('"answer"', json.dumps(response))

    def test_missing_answers_fail_before_persisting_an_attempt(self):
        status, _, payload = self.json_request(
            "POST",
            "/api/attempts",
            {
                "pack_id": "campus-routes",
                "lesson_id": "read-the-network",
                "answers": {"cost-sum": "a"},
            },
        )

        self.assertEqual(status, 422)
        self.assertEqual(payload["error"]["code"], "ANSWERS_INCOMPLETE")

    def test_invalid_content_type_is_rejected(self):
        status, _, payload_bytes = self.request(
            "POST",
            "/api/import",
            content_type="text/plain",
            raw=b'{"title":"x","text":"y"}',
        )
        payload = json.loads(payload_bytes.decode("utf-8"))

        self.assertEqual(status, 415)
        self.assertEqual(payload["error"]["code"], "CONTENT_TYPE_REQUIRED")

    def test_unknown_route_returns_json_error(self):
        status, _, payload = self.json_request("GET", "/api/packs/not-real")

        self.assertEqual(status, 404)
        self.assertEqual(payload["error"]["code"], "PACK_NOT_FOUND")

    def test_export_downloads_a_standalone_study_pack(self):
        status, headers, payload = self.request(
            "GET",
            "/api/export/campus-routes?lang=zh",
        )
        body = payload.decode("utf-8")

        self.assertEqual(status, 200)
        self.assertEqual(headers["Content-Type"], "text/html; charset=utf-8")
        self.assertIn("attachment;", headers["Content-Disposition"])
        self.assertIn("校园路线实验室", body)
        self.assertIn('"distance":9', body)
        self.assertNotIn("127.0.0.1", body)
        self.assertTrue(
            (self.runtime_dir / "exports" / "SourceLoop-campus-routes-zh.html").is_file()
        )

    def test_static_path_traversal_is_blocked(self):
        status, _, payload = self.request("GET", "/assets/%2e%2e/app.py")

        self.assertEqual(status, 404)
        self.assertNotIn(b"ThreadingHTTPServer", payload)


if __name__ == "__main__":
    unittest.main()
