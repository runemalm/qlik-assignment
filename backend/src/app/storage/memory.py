from uuid import UUID, uuid4
from typing import Dict
from app.models.message import Message
from app.core.palindrome import is_palindrome
from datetime import datetime


class MessageStore:
    def __init__(self):
        self._messages: Dict[UUID, Message] = {}

    def add_message(self, text: str) -> Message:
        msg = Message(
            id=uuid4(),
            text=text,
            is_palindrome=is_palindrome(text),
            created_at=datetime.utcnow()  # ✅ set timestamp
        )
        self._messages[msg.id] = msg
        return msg

    def list_messages(self) -> list[Message]:
        return list(self._messages.values())

    def get_message(self, message_id: UUID) -> Message | None:
        return self._messages.get(message_id)

    def delete_message(self, message_id: UUID) -> bool:
        return self._messages.pop(message_id, None) is not None
