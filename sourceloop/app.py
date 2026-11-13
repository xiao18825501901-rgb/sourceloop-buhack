"""Loopback HTTP application for SourceLoop."""

from __future__ import annotations

import json
import logging
import re
import urllib.parse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from sourceloop import __version__
from sourceloop.content import (
    ContentValidationError,
    ImportValidationError,
    build_import_pack,
    find_lesson,
    load_curated_pack,
    public_pack,
)
from sourceloop.export import build_offline_export
from sourceloop.graph import shortest_path_trace
from sourceloop.store import Store


LOGGER = logging.getLogger("sourceloop")
PACKAGE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_PATH = PACKAGE_DIR / "data" / "campus_routes.json"
DEFAULT_STATIC_DIR = PACKAGE_DIR / "static"
MAX_BODY_BYTES = 256 * 1024
SECURITY_HEADERS = {
    "Content-Security-Policy": (
        "default-src 'self'; script-src 'self'; style-src 'self'; "
        "img-src 'self' data:; connect-src 'self'; font-src 'self'; "
        "base-uri 'none'; form-action 'self'; frame-ancestors 'none'; "
        "object-src 'none'"
    ),
    "Referrer-Policy": "no-referrer",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
}
CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".webp": "image/webp",
}


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str):
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message


class SourceLoopApplication:
    def __init__(
        self,
        *,
        runtime_dir: Path | str,
        data_path: Path | str = DEFAULT_DATA_PATH,
        static_dir: Path | str = DEFAULT_STATIC_DIR,
        export_builder: Any | None = None,
    ):
        self.runtime_dir = Path(runtime_dir)
        self.static_dir = Path(static_dir)
        self.curated_pack = load_curated_pack(data_path)
        self.store = Store(self.runtime_dir)
        self.export_builder = export_builder

    def resolve_pack(self, pack_id: str) -> dict[str, Any]:
        if pack_id == self.curated_pack["id"]:
            return self.curated_pack
        imported_pack = self.store.get_imported_pack(pack_id)
        if imported_pack is None:
            raise ApiError(404, "PACK_NOT_FOUND", "That study pack was not found.")
        return imported_pack

    def _pack_summary(self, pack: dict[str, Any], stats: dict[str, Any]) -> dict[str, Any]:
        practice_lessons = sum(
            1 for lesson in pack["lessons"] if lesson["id"] in stats
        )
        return {
            "id": pack["id"],
            "origin": pack["origin"],
            "title": pack["title"],
            "subtitle": pack["subtitle"],
            "discipline": pack["discipline"],
            "lesson_count": len(pack["lessons"]),
            "practiced_lessons": practice_lessons,
        }

    def list_packs(self) -> list[dict[str, Any]]:
        stats = self.store.attempt_stats()
        summaries = [self._pack_summary(self.curated_pack, stats.get(self.curated_pack["id"], {}))]
        for imported_summary in self.store.list_imported_summaries():
            imported_pack = self.store.get_imported_pack(imported_summary["id"])
            if imported_pack is not None:
                summaries.append(
                    self._pack_summary(
                        imported_pack,
                        stats.get(imported_summary["id"], {}),
                    )
                )
        return summaries

    def bootstrap(self) -> dict[str, Any]:
        packs = self.list_packs()
        return {
            "version": __version__,
            "default_pack_id": self.curated_pack["id"],
            "packs": packs,
            "review_count": self.store.review_count(),
        }

    def client_pack(self, pack_id: str) -> dict[str, Any]:
        pack = public_pack(self.resolve_pack(pack_id))
        for lesson in pack["lessons"]:
            visual = lesson.get("visual")
            if visual is not None and visual.get("type") == "dijkstra":
                visual["trace"] = shortest_path_trace(
                    visual,
                    visual["start"],
                    visual["goal"],
                )
        stats = self.store.attempt_stats().get(pack_id, {})
        pack["progress"] = stats
        return {
            "pack": pack,
            "review_count": self.store.review_count(),
        }

    def import_pack(self, title: Any, text: Any) -> tuple[int, dict[str, Any]]:
        if not isinstance(title, str) or not isinstance(text, str):
            raise ApiError(
                422,
                "IMPORT_FIELDS_INVALID",
                "Course title and notes must both be text.",
            )
        try:
            pack = build_import_pack(title, text)
        except ImportValidationError as error:
            raise ApiError(422, "IMPORT_INVALID", str(error)) from error
        self.store.save_imported_pack(pack)
        summary = self._pack_summary(pack, {})
        return 201, {"pack_id": pack["id"], "pack": summary}

    def submit_attempt(self, payload: dict[str, Any]) -> dict[str, Any]:
        pack_id = payload.get("pack_id")
        lesson_id = payload.get("lesson_id")
        answers = payload.get("answers")
        if not isinstance(pack_id, str) or not isinstance(lesson_id, str):
            raise ApiError(422, "ATTEMPT_INVALID", "Pack and lesson are required.")
        if not isinstance(answers, dict) or not all(
            isinstance(question_id, str) and isinstance(option_id, str)
            for question_id, option_id in answers.items()
        ):
            raise ApiError(422, "ANSWERS_INVALID", "Answers must map questions to options.")

        pack = self.resolve_pack(pack_id)
        lesson = find_lesson(pack, lesson_id)
        if lesson is None:
            raise ApiError(404, "LESSON_NOT_FOUND", "That lesson was not found.")
        questions = lesson.get("questions", [])
        if not questions:
            raise ApiError(
                422,
                "NO_PRACTICE",
                "This reading pack does not contain practice checks.",
            )

        expected_ids = {question["id"] for question in questions}
        if set(answers) != expected_ids:
            raise ApiError(
                422,
                "ANSWERS_INCOMPLETE",
                "Answer every check before submitting.",
            )

        source_map = {source["code"]: source for source in pack["sources"]}
        results: list[dict[str, Any]] = []
        score = 0
        for question in questions:
            selected_option = answers[question["id"]]
            valid_options = {option["id"] for option in question["options"]}
            if selected_option not in valid_options:
                raise ApiError(
                    422,
                    "OPTION_INVALID",
                    "An answer option was not valid for its question.",
                )
            is_correct = selected_option == question["answer"]
            score += int(is_correct)
            results.append(
                {
                    "question_id": question["id"],
                    "prompt": question["prompt"],
                    "selected_option": selected_option,
                    "correct_option": question["answer"],
                    "is_correct": is_correct,
                    "explanation": question["explanation"],
                    "source": source_map[question["source"]],
                    "concept": question["concept"],
                }
            )

        attempt_id = self.store.create_attempt(
            pack_id=pack_id,
            lesson_id=lesson_id,
            lesson_title=lesson["title"],
            answers=answers,
            score=score,
            total=len(questions),
            results=results,
        )
        return {
            "attempt_id": attempt_id,
            "score": score,
            "total": len(questions),
            "percent": round(score / len(questions) * 100),
            "results": results,
            "review_count": self.store.review_count(),
        }

    def review_payload(self) -> dict[str, Any]:
        items = self.store.list_review_items()
        return {"items": items, "review_count": len(items)}

    def resolve_review(self, item_id: int) -> dict[str, Any]:
        resolved = self.store.resolve_review_item(item_id)
        if not resolved:
            raise ApiError(
                404,
                "REVIEW_NOT_FOUND",
                "That review item was already resolved or does not exist.",
            )
        return {"resolved": True, "review_count": self.store.review_count()}

    def export_pack(self, pack_id: str, language: str) -> tuple[str, bytes]:
        if self.export_builder is None:
            raise ApiError(501, "EXPORT_UNAVAILABLE", "Export is not available yet.")
        pack = self.resolve_pack(pack_id)
        safe_language = language if language in {"en", "zh"} else "en"
        filename = f"SourceLoop-{pack_id}-{safe_language}.html"
        html = self.export_builder(pack, safe_language)
        output_path = self.store.export_dir / filename
        output_path.write_text(html, encoding="utf-8")
        return filename, html.encode("utf-8")


class SourceLoopHTTPServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], application: SourceLoopApplication):
        super().__init__(address, SourceLoopRequestHandler)
        self.application = application


class SourceLoopRequestHandler(BaseHTTPRequestHandler):
    server: SourceLoopHTTPServer
    protocol_version = "HTTP/1.1"

    def _send_common_headers(self) -> None:
        for name, value in SECURITY_HEADERS.items():
            self.send_header(name, value)

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self._send_common_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_error(self, error: ApiError) -> None:
        self._send_json(
            error.status,
            {
                "error": {
                    "code": error.code,
                    "message": error.message,
                    "retryable": error.status >= 500,
                }
            },
        )

    def _send_bytes(
        self,
        status: int,
        body: bytes,
        content_type: str,
        *,
        cache_control: str = "no-store",
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        self.send_response(status)
        self._send_common_headers()
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", cache_control)
        self.send_header("Content-Length", str(len(body)))
        for name, value in (extra_headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict[str, Any]:
        content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
        if content_type != "application/json":
            raise ApiError(
                415,
                "CONTENT_TYPE_REQUIRED",
                "Requests must use application/json.",
            )
        raw_length = self.headers.get("Content-Length")
        if raw_length is None:
            raise ApiError(411, "CONTENT_LENGTH_REQUIRED", "Content-Length is required.")
        try:
            content_length = int(raw_length)
        except ValueError as error:
            raise ApiError(400, "CONTENT_LENGTH_INVALID", "Invalid Content-Length.") from error
        if content_length < 0 or content_length > MAX_BODY_BYTES:
            raise ApiError(413, "REQUEST_TOO_LARGE", "The request body is too large.")
        raw = self.rfile.read(content_length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ApiError(400, "JSON_INVALID", "The JSON body could not be read.") from error
        if not isinstance(payload, dict):
            raise ApiError(400, "JSON_INVALID", "The JSON body must be an object.")
        return payload

    def do_GET(self) -> None:
        parsed = urllib.parse.urlsplit(self.path)
        request_path = urllib.parse.unquote(parsed.path)
        try:
            if request_path == "/api/health":
                self._send_json(
                    200,
                    {
                        "status": "ok",
                        "database": "ready" if self.server.application.store.healthcheck() else "error",
                        "version": __version__,
                    },
                )
                return
            if request_path == "/api/bootstrap":
                self._send_json(200, self.server.application.bootstrap())
                return
            pack_match = re.fullmatch(r"/api/packs/([a-z0-9-]+)", request_path)
            if pack_match:
                self._send_json(
                    200,
                    self.server.application.client_pack(pack_match.group(1)),
                )
                return
            if request_path == "/api/review":
                self._send_json(200, self.server.application.review_payload())
                return
            export_match = re.fullmatch(r"/api/export/([a-z0-9-]+)", request_path)
            if export_match:
                language = urllib.parse.parse_qs(parsed.query).get("lang", ["en"])[0]
                filename, body = self.server.application.export_pack(
                    export_match.group(1),
                    language,
                )
                self._send_bytes(
                    200,
                    body,
                    "text/html; charset=utf-8",
                    cache_control="no-store",
                    extra_headers={
                        "Content-Disposition": f'attachment; filename="{filename}"'
                    },
                )
                return
            if request_path == "/":
                self._serve_static("index.html")
                return
            asset_match = re.fullmatch(r"/assets/([A-Za-z0-9._-]+)", request_path)
            if asset_match:
                self._serve_static(asset_match.group(1))
                return
            if request_path == "/favicon.svg":
                self._serve_static("favicon.svg")
                return
            raise ApiError(404, "NOT_FOUND", "The requested resource was not found.")
        except ApiError as error:
            self._send_error(error)
        except Exception:
            LOGGER.exception("Unhandled GET failure")
            self._send_error(
                ApiError(500, "INTERNAL_ERROR", "The local server could not complete the request.")
            )

    def _serve_static(self, filename: str) -> None:
        static_root = self.server.application.static_dir.resolve()
        candidate = (static_root / filename).resolve()
        if not candidate.is_relative_to(static_root) or not candidate.is_file():
            raise ApiError(404, "NOT_FOUND", "The requested file was not found.")
        content_type = CONTENT_TYPES.get(candidate.suffix.lower())
        if content_type is None:
            raise ApiError(404, "NOT_FOUND", "The requested file type is not served.")
        body = candidate.read_bytes()
        self._send_bytes(200, body, content_type, cache_control="public, max-age=60")

    def do_POST(self) -> None:
        parsed = urllib.parse.urlsplit(self.path)
        request_path = urllib.parse.unquote(parsed.path)
        try:
            if request_path == "/api/import":
                payload = self._read_json()
                status, result = self.server.application.import_pack(
                    payload.get("title", ""),
                    payload.get("text", ""),
                )
                self._send_json(status, result)
                return
            if request_path == "/api/attempts":
                payload = self._read_json()
                self._send_json(200, self.server.application.submit_attempt(payload))
                return
            review_match = re.fullmatch(r"/api/review/(\d+)/resolve", request_path)
            if review_match:
                self._read_json()
                self._send_json(
                    200,
                    self.server.application.resolve_review(int(review_match.group(1))),
                )
                return
            raise ApiError(404, "NOT_FOUND", "The requested endpoint was not found.")
        except ApiError as error:
            self._send_error(error)
        except ContentValidationError:
            LOGGER.exception("Course validation failed")
            self._send_error(
                ApiError(500, "CONTENT_INVALID", "The local course data is not valid.")
            )
        except Exception:
            LOGGER.exception("Unhandled POST failure")
            self._send_error(
                ApiError(500, "INTERNAL_ERROR", "The local server could not complete the request.")
            )

    def log_message(self, message_format: str, *args: Any) -> None:
        LOGGER.info("%s - %s", self.address_string(), message_format % args)


def create_server(
    *,
    host: str = "127.0.0.1",
    port: int = 8765,
    runtime_dir: Path | str | None = None,
    data_path: Path | str = DEFAULT_DATA_PATH,
    static_dir: Path | str = DEFAULT_STATIC_DIR,
    export_builder: Any | None = None,
) -> SourceLoopHTTPServer:
    resolved_runtime = Path(runtime_dir) if runtime_dir else PACKAGE_DIR.parent / "runtime"
    application = SourceLoopApplication(
        runtime_dir=resolved_runtime,
        data_path=data_path,
        static_dir=static_dir,
        export_builder=export_builder or build_offline_export,
    )
    return SourceLoopHTTPServer((host, port), application)
