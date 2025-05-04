from app.domain.model.message.message_store import IMessageStore
from app.domain.model.message.message import Message


class ListMessagesAction:
    def __init__(self, store: IMessageStore):
        self.store = store

    def execute(self) -> list[Message]:
        return self.store.list()
