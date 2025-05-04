from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class MessageCreate(BaseModel):
    text: str

class Message(MessageCreate):
    id: UUID
    is_palindrome: bool
    created_at: datetime
