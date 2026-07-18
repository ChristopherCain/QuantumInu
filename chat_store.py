from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from threading import Lock
from typing import Any

from config import MAX_HISTORY_MESSAGES


@dataclass
class ConversationStore:
    conversations: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    lock: Lock = field(default_factory=Lock)

    def get(self, conversation_id: str) -> list[dict[str, Any]]:
        with self.lock:
            return deepcopy(self.conversations.get(conversation_id, []))

    def append_turn(
        self,
        conversation_id: str,
        question: str,
        answer: str,
        sources: list[dict[str, str]],
    ) -> None:
        with self.lock:
            history = self.conversations.setdefault(conversation_id, [])
            history.extend(
                [
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": answer, "sources": sources},
                ]
            )
            self.conversations[conversation_id] = history[-MAX_HISTORY_MESSAGES:]

    def clear(self, conversation_id: str) -> None:
        with self.lock:
            self.conversations.pop(conversation_id, None)
