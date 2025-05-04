from app.domain.model.message.message_store import IMessageStore
from app.infra.storage.memory.memory_message_store import MemoryMessageStore
from app.domain.services.message_service import MessageService

message_store = MemoryMessageStore()
message_service = MessageService()

def get_message_store() -> IMessageStore:
    return message_store

def get_message_service() -> MessageService:
    return message_service
