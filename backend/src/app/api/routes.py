from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from app.models.message import MessageCreate, Message
from app.dependencies import get_store
from app.storage.memory import MessageStore

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("", response_model=Message)
def create_message(message: MessageCreate, store: MessageStore = Depends(get_store)):
    return store.add_message(message.text)

@router.get("", response_model=list[Message])
def list_messages(store: MessageStore = Depends(get_store)):
    return store.list_messages()

@router.get("/{message_id}", response_model=Message)
def get_message(message_id: UUID, store: MessageStore = Depends(get_store)):
    msg = store.get_message(message_id)
    if msg is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg

@router.delete("/{message_id}", status_code=204)
def delete_message(message_id: UUID, store: MessageStore = Depends(get_store)):
    if not store.delete_message(message_id):
        raise HTTPException(status_code=404, detail="Message not found")
