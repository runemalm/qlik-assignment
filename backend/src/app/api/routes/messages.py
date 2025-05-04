from fastapi import APIRouter, Depends
from uuid import UUID
from app.domain.model.message.message import MessageCreate, Message
from app.dependencies import get_message_store, get_message_service
from app.actions.messages.create_message import CreateMessageAction
from app.actions.messages.get_message import GetMessageAction
from app.actions.messages.list_messages import ListMessagesAction
from app.actions.messages.delete_message import DeleteMessageAction
from app.domain.services.message_service import MessageService
from app.domain.model.message.message_store import IMessageStore

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("", response_model=Message, status_code=201)
def create_message(
    message: MessageCreate,
    store: IMessageStore = Depends(get_message_store),
    service: MessageService = Depends(get_message_service),
):
    return CreateMessageAction(store, service).execute(message.text)


@router.get("", response_model=list[Message])
def list_messages(store: IMessageStore = Depends(get_message_store)):
    return ListMessagesAction(store).execute()


@router.get("/{message_id}", response_model=Message)
def get_message(message_id: UUID, store: IMessageStore = Depends(get_message_store)):
    return GetMessageAction(store).execute(message_id)


@router.delete("/{message_id}", status_code=204)
def delete_message(message_id: UUID, store: IMessageStore = Depends(get_message_store)):
    DeleteMessageAction(store).execute(message_id)
