from app.domain.model.message.message import Message
from uuid import uuid4
from datetime import datetime

class MessageService:
    def create_message(self, text: str) -> Message:
        return Message(
            id=uuid4(),
            text=text,
            is_palindrome=self._is_palindrome(text),
            created_at=datetime.utcnow()
        )

    def _is_palindrome(self, text: str) -> bool:
        cleaned = ''.join(c.lower() for c in text if c.isalnum())
        return cleaned == cleaned[::-1]
