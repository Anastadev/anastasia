from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class NudeVote:
    message_id: int
    chat_id: int
    url: str
    score: int = 0


class NudeScoreStore:
    def __init__(self, path: Optional[str] = None) -> None:
        self._path = Path(path) if path else Path.cwd() / "nude_scoreboard.json"
        self._data: Dict[str, NudeVote] = {}
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            self._data = {}
            return
        try:
            raw = json.loads(self._path.read_text(encoding="utf-8"))
        except Exception:
            self._data = {}
            return
        self._data = {
            k: NudeVote(**v)
            for k, v in raw.items()
            if isinstance(v, dict) and "message_id" in v and "chat_id" in v and "url" in v
        }

    def _save(self) -> None:
        serializable = {k: asdict(v) for k, v in self._data.items()}
        self._path.write_text(json.dumps(serializable, ensure_ascii=False, indent=2), encoding="utf-8")

    def register_nude(self, chat_id: int, message_id: int, url: str) -> str:
        key = f"{chat_id}:{message_id}"
        self._data[key] = NudeVote(message_id=message_id, chat_id=chat_id, url=url, score=0)
        self._save()
        return key

    def upvote(self, key: str) -> Optional[NudeVote]:
        vote = self._data.get(key)
        if not vote:
            return None
        vote.score += 1
        self._save()
        return vote

    def top(self, limit: int = 5) -> List[NudeVote]:
        return sorted(self._data.values(), key=lambda v: v.score, reverse=True)[:limit]

