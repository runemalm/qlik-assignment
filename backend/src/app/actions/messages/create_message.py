from app.domain.services.message_service import MessageService
from app.domain.model.message.message_store import IMessageStore
from app.domain.model.message.message import Message


class CreateMessageAction:
    def __init__(self, store: IMessageStore, service: MessageService):
        self.store = store
        self.service = service

    def execute(self, text: str) -> Message:
        message = self.service.create_message(text)
        self.store.save(message)
        return message
