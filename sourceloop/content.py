"""Course validation, public-payload redaction, and deterministic note import."""

from __future__ import annotations

import copy
import json
import re
import uuid
from pathlib import Path
from typing import Any


MAX_IMPORT_CHARS = 150_000
MAX_SECTIONS = 8
MAX_SOURCE_CHARS = 5_000
SLUG_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,79}$")
HEADING_PATTERN = re.compile(r"^(#{1,3})\s+(.+?)\s*#*\s*$")
SENTENCE_PATTERN = re.compile(r"(?<=[.!?。！？])\s+")


class ContentValidationError(ValueError):
    """Raised when a course pack violates the expected data contract."""


class ImportValidationError(ValueError):
    """Raised when imported notes cannot become a safe study pack."""


def _bilingual(value: Any, field_name: str) -> None:
    if not isinstance(value, dict):
        raise ContentValidationError(f"{field_name} must be bilingual")
    for language_code in ("en", "zh"):
        text = value.get(language_code)
        if not isinstance(text, str) or not text.strip():
            raise ContentValidationError(f"{field_name}.{language_code} is required")


def _option_map(question: dict[str, Any]) -> dict[str, dict[str, Any]]:
    options = question.get("options")
    if not isinstance(options, list) or len(options) < 2:
        raise ContentValidationError("each question needs at least two options")
    result: dict[str, dict[str, Any]] = {}
    for option in options:
        if not isinstance(option, dict) or not isinstance(option.get("id"), str):
            raise ContentValidationError("each option needs a string id")
        if option["id"] in result:
            raise ContentValidationError("option ids must be unique within a question")
        _bilingual(option.get("text"), "option.text")
        result[option["id"]] = option
    return result


def source_codes_for_lesson(lesson: dict[str, Any]) -> set[str]:
    codes: set[str] = set()
    for block in lesson.get("body", []):
        if isinstance(block, dict) and isinstance(block.get("source"), str):
            codes.add(block["source"])
    for question in lesson.get("questions", []):
        if isinstance(question, dict) and isinstance(question.get("source"), str):
            codes.add(question["source"])
    return codes


def validate_pack(pack: dict[str, Any]) -> None:
    if not isinstance(pack, dict):
        raise ContentValidationError("pack must be an object")
    if pack.get("schema_version") != 1:
        raise ContentValidationError("unsupported schema_version")
    pack_id = pack.get("id")
    if not isinstance(pack_id, str) or not SLUG_PATTERN.fullmatch(pack_id):
        raise ContentValidationError("pack.id must be a safe slug")

    for field_name in ("title", "subtitle", "description", "discipline"):
        _bilingual(pack.get(field_name), field_name)

    sources = pack.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ContentValidationError("pack.sources must be non-empty")
    source_codes: set[str] = set()
    for source in sources:
        if not isinstance(source, dict):
            raise ContentValidationError("each source must be an object")
        code = source.get("code")
        if not isinstance(code, str) or not code or code in source_codes:
            raise ContentValidationError("source codes must be unique")
        source_codes.add(code)
        _bilingual(source.get("label"), "source.label")
        _bilingual(source.get("title"), "source.title")
        _bilingual(source.get("text"), "source.text")

    lessons = pack.get("lessons")
    if not isinstance(lessons, list) or not lessons:
        raise ContentValidationError("pack.lessons must be non-empty")
    lesson_ids: set[str] = set()
    for lesson in lessons:
        if not isinstance(lesson, dict):
            raise ContentValidationError("each lesson must be an object")
        lesson_id = lesson.get("id")
        if not isinstance(lesson_id, str) or not SLUG_PATTERN.fullmatch(lesson_id):
            raise ContentValidationError("lesson.id must be a safe slug")
        if lesson_id in lesson_ids:
            raise ContentValidationError("lesson ids must be unique")
        lesson_ids.add(lesson_id)
        _bilingual(lesson.get("kicker"), "lesson.kicker")
        _bilingual(lesson.get("title"), "lesson.title")
        _bilingual(lesson.get("summary"), "lesson.summary")
        _bilingual(lesson.get("duration"), "lesson.duration")

        body = lesson.get("body")
        if not isinstance(body, list) or not body:
            raise ContentValidationError("each lesson needs reading content")
        for block in body:
            if not isinstance(block, dict) or block.get("kind") not in {
                "lead",
                "paragraph",
                "callout",
            }:
                raise ContentValidationError("unknown lesson block kind")
            _bilingual(block.get("text"), "lesson.body.text")
            if block.get("kind") == "callout":
                _bilingual(block.get("title"), "lesson.body.title")
            block_source = block.get("source")
            if block_source is not None and block_source not in source_codes:
                raise ContentValidationError("lesson block references an unknown source")

        visual = lesson.get("visual")
        if visual is not None and visual.get("type") != "dijkstra":
            raise ContentValidationError("unsupported visual type")

        questions = lesson.get("questions")
        if not isinstance(questions, list):
            raise ContentValidationError("lesson.questions must be a list")
        question_ids: set[str] = set()
        for question in questions:
            if not isinstance(question, dict):
                raise ContentValidationError("each question must be an object")
            question_id = question.get("id")
            if not isinstance(question_id, str) or not SLUG_PATTERN.fullmatch(question_id):
                raise ContentValidationError("question.id must be a safe slug")
            if question_id in question_ids:
                raise ContentValidationError("question ids must be unique within a lesson")
            question_ids.add(question_id)
            _bilingual(question.get("prompt"), "question.prompt")
            _bilingual(question.get("explanation"), "question.explanation")
            _bilingual(question.get("concept"), "question.concept")
            options = _option_map(question)
            if question.get("answer") not in options:
                raise ContentValidationError("question.answer must reference an option")
            if question.get("source") not in source_codes:
                raise ContentValidationError("question references an unknown source")


def load_curated_pack(path: Path | str) -> dict[str, Any]:
    data_path = Path(path)
    try:
        pack = json.loads(data_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ContentValidationError(f"could not load course data: {error}") from error
    validate_pack(pack)
    return pack


def public_pack(pack: dict[str, Any]) -> dict[str, Any]:
    """Return course data that is safe to send before an answer is submitted."""

    result = copy.deepcopy(pack)
    for lesson in result["lessons"]:
        for question in lesson["questions"]:
            question.pop("answer", None)
            question.pop("explanation", None)
    return result


def find_lesson(pack: dict[str, Any], lesson_id: str) -> dict[str, Any] | None:
    for lesson in pack["lessons"]:
        if lesson["id"] == lesson_id:
            return lesson
    return None


def _bilingual_text(text: str) -> dict[str, str]:
    return {"en": text, "zh": text}


def _plain_text(text: str) -> str:
    without_links = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    without_links = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", without_links)
    without_markers = re.sub(r"^\s{0,3}>\s?", "", without_links, flags=re.MULTILINE)
    without_markers = re.sub(r"^\s{0,3}[-*+]\s+", "", without_markers, flags=re.MULTILINE)
    without_markers = without_markers.replace("`", "")
    without_markers = re.sub(r"[*_]{1,3}", "", without_markers)
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in without_markers.splitlines()]
    paragraphs: list[str] = []
    current: list[str] = []
    for line in lines:
        if line:
            current.append(line)
        elif current:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    return "\n\n".join(paragraphs).strip()


def _split_sections(text: str) -> list[tuple[str, str]]:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    sections: list[tuple[str, str]] = []
    current_title = "Overview"
    current_lines: list[str] = []

    def flush_section() -> None:
        body = _plain_text("\n".join(current_lines))
        if body:
            sections.append((current_title, body))

    for line in lines:
        match = HEADING_PATTERN.match(line.strip())
        if match:
            flush_section()
            current_title = _plain_text(match.group(2)) or "Untitled section"
            current_lines = []
        else:
            current_lines.append(line)
    flush_section()
    return sections[:MAX_SECTIONS]


def _sentences(text: str) -> list[str]:
    result: list[str] = []
    for sentence in SENTENCE_PATTERN.split(text.replace("\n", " ")):
        cleaned = re.sub(r"\s+", " ", sentence).strip()
        if len(cleaned) >= 24:
            result.append(cleaned[:320])
    return result


def _rotated_option_order(
    correct_text: str,
    distractors: list[str],
    preferred_index: int,
) -> tuple[list[dict[str, Any]], str]:
    option_texts = list(distractors[:2])
    correct_index = preferred_index % (len(option_texts) + 1)
    option_texts.insert(correct_index, correct_text)
    option_ids = ["a", "b", "c"][: len(option_texts)]
    options = [
        {"id": option_id, "text": _bilingual_text(option_text)}
        for option_id, option_text in zip(option_ids, option_texts)
    ]
    return options, option_ids[correct_index]


def build_import_pack(title: str, text: str) -> dict[str, Any]:
    if not isinstance(title, str) or not isinstance(text, str):
        raise ImportValidationError("title and text must be strings")
    normalized_text = text.replace("\x00", "").strip()
    if not normalized_text:
        raise ImportValidationError("Paste or choose at least one section of notes")
    if len(normalized_text) > MAX_IMPORT_CHARS:
        raise ImportValidationError("Notes are too large; the limit is 150,000 characters")

    clean_title = re.sub(r"\s+", " ", title).strip()[:100]
    sections = _split_sections(normalized_text)
    if not sections:
        raise ImportValidationError("No readable sections were found")
    if not clean_title:
        clean_title = sections[0][0][:100] or "My local notes"

    pack_id = f"import-{uuid.uuid4().hex[:10]}"
    sentences_by_section: list[list[str]] = []
    sources: list[dict[str, Any]] = []

    for section_index, (section_title, section_text) in enumerate(sections, start=1):
        clipped_text = section_text[:MAX_SOURCE_CHARS]
        sentence_list = _sentences(clipped_text)
        sentences_by_section.append(sentence_list)
        source_code = f"S{section_index}"
        sources.append(
            {
                "code": source_code,
                "label": _bilingual_text(f"Local note · Section {section_index}"),
                "title": _bilingual_text(section_title),
                "text": _bilingual_text(clipped_text),
            }
        )

    all_headings = [section_title for section_title, _ in sections]
    lessons: list[dict[str, Any]] = []

    for section_index, (section_title, section_text) in enumerate(sections):
        source_code = f"S{section_index + 1}"
        own_sentences = sentences_by_section[section_index]
        other_sentences = [
            sentence
            for other_index, sentence_list in enumerate(sentences_by_section)
            if other_index != section_index
            for sentence in sentence_list
        ]
        questions: list[dict[str, Any]] = []

        if own_sentences and len(other_sentences) >= 2:
            correct_quote = own_sentences[0]
            options, correct_answer = _rotated_option_order(
                correct_quote,
                other_sentences,
                section_index,
            )
            questions.append(
                {
                    "id": "quote-check",
                    "prompt": _bilingual_text(
                        f"Which sentence appears in the “{section_title}” section?"
                    ),
                    "options": options,
                    "answer": correct_answer,
                    "explanation": _bilingual_text(
                        f"The exact sentence is in source {source_code}. "
                        "The other quotes belong to different sections."
                    ),
                    "source": source_code,
                    "concept": _bilingual_text(f"Exact retrieval: {section_title}"),
                }
            )

        if own_sentences and len(all_headings) >= 2:
            heading_distractors = [
                heading for heading in all_headings if heading != section_title
            ]
            options, correct_answer = _rotated_option_order(
                section_title,
                heading_distractors,
                section_index + 1,
            )
            questions.append(
                {
                    "id": "source-location",
                    "prompt": _bilingual_text(
                        f"“{own_sentences[0]}” Which section is its exact source?"
                    ),
                    "options": options,
                    "answer": correct_answer,
                    "explanation": _bilingual_text(
                        f"This sentence appears in “{section_title}” "
                        f"and is stored as source {source_code}."
                    ),
                    "source": source_code,
                    "concept": _bilingual_text(f"Source location: {section_title}"),
                }
            )

        first_sentence = own_sentences[0] if own_sentences else section_text[:240]
        remaining_text = section_text
        if first_sentence and remaining_text.startswith(first_sentence):
            remaining_text = remaining_text[len(first_sentence) :].strip()
        body: list[dict[str, Any]] = [
            {
                "kind": "lead",
                "text": _bilingual_text(first_sentence),
                "source": source_code,
            }
        ]
        if remaining_text:
            body.append(
                {
                    "kind": "paragraph",
                    "text": _bilingual_text(remaining_text[:3_500]),
                    "source": source_code,
                }
            )

        word_count = len(re.findall(r"\S+", section_text))
        minutes = max(2, min(12, round(word_count / 180)))
        lessons.append(
            {
                "id": f"section-{section_index + 1}",
                "kicker": _bilingual_text(f"{section_index + 1:02d} · Local import"),
                "title": _bilingual_text(section_title),
                "summary": _bilingual_text(
                    f"Study this imported section and check exact return to its source."
                ),
                "duration": _bilingual_text(f"{minutes} min"),
                "body": body,
                "questions": questions,
            }
        )

    pack = {
        "schema_version": 1,
        "id": pack_id,
        "origin": "imported",
        "title": _bilingual_text(clean_title),
        "subtitle": _bilingual_text("Imported local notes with literal source checks."),
        "description": _bilingual_text(
            "Your text remains the source of truth. These checks verify exact "
            "retrieval rather than inventing new explanations."
        ),
        "discipline": _bilingual_text("Local import"),
        "authors": "Local import",
        "license": "User-supplied content",
        "sources": sources,
        "lessons": lessons,
    }
    validate_pack(pack)
    return pack
