import json
import unittest
from html.parser import HTMLParser
from pathlib import Path

from sourceloop.content import build_import_pack, load_curated_pack
from sourceloop.export import build_offline_export


DATA_PATH = Path(__file__).resolve().parents[1] / "sourceloop" / "data" / "campus_routes.json"


class _DocumentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts = 0
        self.has_main = False

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.scripts += 1
        if tag == "main":
            self.has_main = True


class OfflineExportTests(unittest.TestCase):
    def setUp(self):
        self.pack = load_curated_pack(DATA_PATH)

    def test_export_is_one_standalone_bilingual_document(self):
        english = build_offline_export(self.pack, "en")
        chinese = build_offline_export(self.pack, "zh")
        parser = _DocumentParser()
        parser.feed(english)

        self.assertIn("Campus Routes Lab", english)
        self.assertIn("校园路线实验室", chinese)
        self.assertIn("LIB", english)
        self.assertIn('"path":["LIB","CAN","LAB"]', english)
        self.assertIn('"distance":9', english)
        self.assertTrue(parser.has_main)
        self.assertEqual(parser.scripts, 2)
        self.assertNotIn("localhost", english)
        self.assertNotIn("127.0.0.1", english)
        self.assertNotIn("https://", english)
        self.assertNotIn("<link", english)

    def test_embedded_json_cannot_close_the_script_element(self):
        hostile = build_import_pack(
            'Notes </script><script>alert("x")</script>',
            "# Section one\n\nA literal </script><script>alert(1)</script> note.\n\n"
            "# Section two\n\nAnother complete sentence that remains source text.",
        )
        exported = build_offline_export(hostile, "en")

        self.assertNotIn("</script><script>alert", exported)
        self.assertIn("\\u003c/script>", exported)
        self.assertEqual(exported.count("</script>"), 2)

    def test_exported_answer_key_round_trips(self):
        exported = build_offline_export(self.pack, "en")
        marker = '<script id="pack-data" type="application/json">'
        start = exported.index(marker) + len(marker)
        end = exported.index("</script>", start)
        payload = json.loads(exported[start:end])

        self.assertEqual(payload["id"], self.pack["id"])
        self.assertEqual(
            payload["lessons"][0]["questions"][0]["answer"],
            "b",
        )
        self.assertEqual(payload["lessons"][1]["visual"]["trace"]["distance"], 9)


if __name__ == "__main__":
    unittest.main()
