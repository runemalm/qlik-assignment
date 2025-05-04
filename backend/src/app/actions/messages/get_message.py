from uuid import UUID
from app.domain.model.message.message_store import IMessageStore
from app.domain.model.message.message import Message
from app.domain.model.errors import MessageNotFoundError

class GetMessageAction:
    def __init__(self, store: IMessageStore):
        self.store = store

    def execute(self, message_id: UUID) -> Message:
        message = self.store.get(message_id)
        if message is None:
            raise MessageNotFoundError(f"Message with ID {message_id} not found.")
        return message
