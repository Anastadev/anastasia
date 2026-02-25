from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional


@dataclass(frozen=True)
class TodoItem:
    id: int
    chat_id: int
    task: str
    date: datetime


class TodoStore:
    def __init__(self, db_path: Optional[str] = None) -> None:
        path = Path(db_path) if db_path else Path.cwd() / "anastasia.sqlite3"
        self._db_path = str(path)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        con = sqlite3.connect(self._db_path)
        con.row_factory = sqlite3.Row
        return con

    def _init_db(self) -> None:
        with self._connect() as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL,
                    task TEXT NOT NULL,
                    date TEXT NOT NULL
                )
                """
            )
            con.execute("CREATE INDEX IF NOT EXISTS idx_todos_chat_date ON todos(chat_id, date)")

    def cleanup_expired(self, chat_id: int, now: Optional[datetime] = None) -> None:
        now_ = now or datetime.now()
        with self._connect() as con:
            con.execute("DELETE FROM todos WHERE chat_id = ? AND date < ?", (chat_id, now_.isoformat()))

    def list(self, chat_id: int) -> list[TodoItem]:
        with self._connect() as con:
            rows = con.execute(
                "SELECT id, chat_id, task, date FROM todos WHERE chat_id = ? ORDER BY date ASC, id ASC",
                (chat_id,),
            ).fetchall()
        return [
            TodoItem(
                id=int(r["id"]),
                chat_id=int(r["chat_id"]),
                task=str(r["task"]),
                date=datetime.fromisoformat(str(r["date"])),
            )
            for r in rows
        ]

    def add(self, chat_id: int, date: datetime, task: str) -> TodoItem:
        with self._connect() as con:
            cur = con.execute(
                "INSERT INTO todos(chat_id, task, date) VALUES (?, ?, ?)",
                (chat_id, task, date.isoformat()),
            )
            todo_id = int(cur.lastrowid)
        return TodoItem(id=todo_id, chat_id=chat_id, task=task, date=date)

    def delete_by_list_index(self, chat_id: int, index_1_based: int) -> None:
        items = self.list(chat_id)
        idx = index_1_based - 1
        if idx < 0 or idx >= len(items):
            return
        todo_id = items[idx].id
        with self._connect() as con:
            con.execute("DELETE FROM todos WHERE chat_id = ? AND id = ?", (chat_id, todo_id))

