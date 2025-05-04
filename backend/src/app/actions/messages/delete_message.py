from uuid import UUID
from app.domain.model.message.message_store import IMessageStore
from app.domain.model.errors import MessageNotFoundError


class DeleteMessageAction:
    def __init__(self, store: IMessageStore):
        self.store = store

    def execute(self, message_id: UUID) -> None:
        if not self.store.delete(message_id):
            raise MessageNotFoundError(f"Message with ID {message_id} not found.")
