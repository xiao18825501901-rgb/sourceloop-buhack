"""SQLite persistence for local imports, attempts, and the review loop."""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


SCHEMA = """
CREATE TABLE IF NOT EXISTS imported_packs (
    id TEXT PRIMARY KEY,
    title_en TEXT NOT NULL,
    title_zh TEXT NOT NULL,
    data_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pack_id TEXT NOT NULL,
    lesson_id TEXT NOT NULL,
    score INTEGER NOT NULL,
    total INTEGER NOT NULL,
    answers_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS review_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pack_id TEXT NOT NULL,
    lesson_id TEXT NOT NULL,
    question_id TEXT NOT NULL,
    lesson_title_json TEXT NOT NULL,
    concept_json TEXT NOT NULL,
    prompt_json TEXT NOT NULL,
    source_json TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open',
    attempts INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(pack_id, lesson_id, question_id)
);

CREATE INDEX IF NOT EXISTS review_items_open_idx
    ON review_items(status, updated_at DESC);
CREATE INDEX IF NOT EXISTS attempts_lesson_idx
    ON attempts(pack_id, lesson_id, created_at DESC);
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Store:
    def __init__(self, runtime_dir: Path | str):
        self.runtime_dir = Path(runtime_dir)
        self.database_dir = self.runtime_dir / "database"
        self.export_dir = self.runtime_dir / "exports"
        self.upload_dir = self.runtime_dir / "uploads"
        self.cache_dir = self.runtime_dir / "cache"
        self.log_dir = self.runtime_dir / "logs"
        for directory in (
            self.database_dir,
            self.export_dir,
            self.upload_dir,
            self.cache_dir,
            self.log_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)
        self.database_path = self.database_dir / "sourceloop.sqlite3"

        with self._connect() as connection:
            connection.executescript(SCHEMA)

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path, timeout=5)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA busy_timeout = 5000")
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def healthcheck(self) -> bool:
        with self._connect() as connection:
            row = connection.execute("SELECT 1 AS ready").fetchone()
        return bool(row and row["ready"] == 1)

    def save_imported_pack(self, pack: dict[str, Any]) -> None:
        created_at = utc_now()
        data_json = json.dumps(pack, ensure_ascii=False, separators=(",", ":"))
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO imported_packs
                    (id, title_en, title_zh, data_json, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    pack["id"],
                    pack["title"]["en"],
                    pack["title"]["zh"],
                    data_json,
                    created_at,
                ),
            )

    def list_imported_summaries(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, title_en, title_zh, created_at
                FROM imported_packs
                ORDER BY created_at DESC
                """
            ).fetchall()
        return [
            {
                "id": row["id"],
                "title": {"en": row["title_en"], "zh": row["title_zh"]},
                "created_at": row["created_at"],
                "origin": "imported",
            }
            for row in rows
        ]

    def get_imported_pack(self, pack_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT data_json FROM imported_packs WHERE id = ?",
                (pack_id,),
            ).fetchone()
        if row is None:
            return None
        return json.loads(row["data_json"])

    def create_attempt(
        self,
        *,
        pack_id: str,
        lesson_id: str,
        lesson_title: dict[str, str],
        answers: dict[str, str],
        score: int,
        total: int,
        results: list[dict[str, Any]],
    ) -> int:
        timestamp = utc_now()
        answers_json = json.dumps(answers, ensure_ascii=False, separators=(",", ":"))
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO attempts
                    (pack_id, lesson_id, score, total, answers_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (pack_id, lesson_id, score, total, answers_json, timestamp),
            )
            attempt_id = int(cursor.lastrowid)

            for result in results:
                if result["is_correct"]:
                    connection.execute(
                        """
                        UPDATE review_items
                        SET status = 'resolved', updated_at = ?
                        WHERE pack_id = ? AND lesson_id = ? AND question_id = ?
                          AND status = 'open'
                        """,
                        (
                            timestamp,
                            pack_id,
                            lesson_id,
                            result["question_id"],
                        ),
                    )
                    continue

                connection.execute(
                    """
                    INSERT INTO review_items
                        (
                            pack_id, lesson_id, question_id, lesson_title_json,
                            concept_json, prompt_json, source_json,
                            status, attempts, created_at, updated_at
                        )
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'open', 1, ?, ?)
                    ON CONFLICT(pack_id, lesson_id, question_id) DO UPDATE SET
                        lesson_title_json = excluded.lesson_title_json,
                        concept_json = excluded.concept_json,
                        prompt_json = excluded.prompt_json,
                        source_json = excluded.source_json,
                        status = 'open',
                        attempts = review_items.attempts + 1,
                        updated_at = excluded.updated_at
                    """,
                    (
                        pack_id,
                        lesson_id,
                        result["question_id"],
                        json.dumps(lesson_title, ensure_ascii=False),
                        json.dumps(result["concept"], ensure_ascii=False),
                        json.dumps(result["prompt"], ensure_ascii=False),
                        json.dumps(result["source"], ensure_ascii=False),
                        timestamp,
                        timestamp,
                    ),
                )
        return attempt_id

    def review_count(self) -> int:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT COUNT(*) AS count FROM review_items WHERE status = 'open'"
            ).fetchone()
        return int(row["count"])

    def list_review_items(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, pack_id, lesson_id, question_id, lesson_title_json,
                       concept_json, prompt_json, source_json, attempts, updated_at
                FROM review_items
                WHERE status = 'open'
                ORDER BY updated_at DESC, id DESC
                """
            ).fetchall()
        return [
            {
                "id": row["id"],
                "pack_id": row["pack_id"],
                "lesson_id": row["lesson_id"],
                "question_id": row["question_id"],
                "lesson_title": json.loads(row["lesson_title_json"]),
                "concept": json.loads(row["concept_json"]),
                "prompt": json.loads(row["prompt_json"]),
                "source": json.loads(row["source_json"]),
                "attempts": row["attempts"],
                "updated_at": row["updated_at"],
            }
            for row in rows
        ]

    def resolve_review_item(self, item_id: int) -> bool:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE review_items
                SET status = 'resolved', updated_at = ?
                WHERE id = ? AND status = 'open'
                """,
                (utc_now(), item_id),
            )
            resolved = cursor.rowcount == 1
        return resolved

    def attempt_stats(self) -> dict[str, dict[str, dict[str, int]]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT pack_id, lesson_id, COUNT(*) AS attempts,
                       MAX(score) AS best_score, MAX(total) AS total
                FROM attempts
                GROUP BY pack_id, lesson_id
                """
            ).fetchall()
        stats: dict[str, dict[str, dict[str, int]]] = {}
        for row in rows:
            stats.setdefault(row["pack_id"], {})[row["lesson_id"]] = {
                "attempts": int(row["attempts"]),
                "best_score": int(row["best_score"]),
                "total": int(row["total"]),
            }
        return stats
