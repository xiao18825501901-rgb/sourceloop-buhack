import json
import unittest
from pathlib import Path

from sourceloop.content import (
    ContentValidationError,
    ImportValidationError,
    build_import_pack,
    load_curated_pack,
    public_pack,
    source_codes_for_lesson,
)


DATA_PATH = Path(__file__).resolve().parents[1] / "sourceloop" / "data" / "campus_routes.json"


class CuratedContentTests(unittest.TestCase):
    def setUp(self):
        self.pack = load_curated_pack(DATA_PATH)

    def test_every_question_points_to_a_real_source_and_option(self):
        source_codes = {source["code"] for source in self.pack["sources"]}

        for lesson in self.pack["lessons"]:
            for question in lesson["questions"]:
                self.assertIn(question["source"], source_codes)
                option_ids = {option["id"] for option in question["options"]}
                self.assertIn(question["answer"], option_ids)
                self.assertTrue(question["explanation"]["en"])
                self.assertTrue(question["explanation"]["zh"])

    def test_lesson_citations_only_reference_existing_sources(self):
        source_codes = {source["code"] for source in self.pack["sources"]}

        for lesson in self.pack["lessons"]:
            self.assertTrue(source_codes_for_lesson(lesson) <= source_codes)

    def test_public_pack_removes_answers_and_explanations(self):
        client_pack = public_pack(self.pack)
        payload = json.dumps(client_pack)

        self.assertNotIn('"answer"', payload)
        self.assertNotIn('"explanation"', payload)
        self.assertEqual(
            len(client_pack["lessons"][0]["questions"]),
            len(self.pack["lessons"][0]["questions"]),
        )

    def test_invalid_pack_is_rejected(self):
        broken = json.loads(json.dumps(self.pack))
        broken["lessons"][0]["questions"][0]["source"] = "S999"

        with self.assertRaises(ContentValidationError):
            from sourceloop.content import validate_pack

            validate_pack(broken)


class MarkdownImportTests(unittest.TestCase):
    def test_builds_section_lessons_and_literal_quote_checks(self):
        notes = """
# Memory and Retrieval

## Encoding

Encoding is the first step in forming a memory. Attention decides which details enter the trace.

## Retrieval practice

Trying to recall an answer before seeing it strengthens later access to that answer.

## Spacing

Spacing distributes study episodes across time instead of crowding them into one block.
""".strip()

        pack = build_import_pack("Memory & Retrieval", notes)

        self.assertEqual(pack["origin"], "imported")
        self.assertEqual(len(pack["lessons"]), 3)
        self.assertEqual(len(pack["sources"]), 3)
        self.assertTrue(all(lesson["questions"] for lesson in pack["lessons"]))
        self.assertTrue(
            any(
                "Trying to recall" in option["text"]["en"]
                for lesson in pack["lessons"]
                for question in lesson["questions"]
                for option in question["options"]
            )
        )

    def test_one_section_remains_reading_only(self):
        pack = build_import_pack(
            "One note",
            "# A single idea\n\nThis section has no other section to use as a distractor.",
        )

        self.assertEqual(len(pack["lessons"]), 1)
        self.assertEqual(pack["lessons"][0]["questions"], [])

    def test_import_keeps_html_shaped_text_as_plain_data(self):
        note = "# Safety\n\nA <script>alert(1)</script> string stays literal text."

        pack = build_import_pack("Safety note", note)

        self.assertIn("<script>", pack["sources"][0]["text"]["en"])
        self.assertNotIn("eval(", json.dumps(pack))

    def test_empty_or_oversized_input_is_rejected(self):
        with self.assertRaises(ImportValidationError):
            build_import_pack("Empty", "   ")
        with self.assertRaises(ImportValidationError):
            build_import_pack("Too large", "x" * (150_001))


if __name__ == "__main__":
    unittest.main()
