from uuid import UUID
from typing import Dict
from app.domain.model.message.message import Message
from app.domain.model.message.message_store import IMessageStore


class MemoryMessageStore(IMessageStore):
    def __init__(self):
        self._messages: Dict[UUID, Message] = {}

    def save(self, message: Message) -> None:
        self._messages[message.id] = message

    def list(self) -> list[Message]:
        return list(self._messages.values())

    def get(self, message_id: UUID) -> Message | None:
        return self._messages.get(message_id)

    def delete(self, message_id: UUID) -> bool:
        return self._messages.pop(message_id, None) is not None
