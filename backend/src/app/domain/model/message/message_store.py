from typing import Protocol, List
from uuid import UUID
from app.domain.model.message.message import Message


class IMessageStore(Protocol):
    def save(self, message: Message) -> None:
        ...

    def list(self) -> List[Message]:
        ...

    def get(self, message_id: UUID) -> Message | None:
        ...

    def delete(self, message_id: UUID) -> bool:
        ...
