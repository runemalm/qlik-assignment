from uuid import uuid4
from datetime import datetime
from app.domain.model.message.message import Message
from app.infra.storage.memory.memory_message_store import MemoryMessageStore


def create_fake_message(text: str = "Hello", is_palindrome: bool = False) -> Message:
    return Message(
        id=uuid4(),
        text=text,
        is_palindrome=is_palindrome,
        created_at=datetime.utcnow()
    )


def test_save_and_get_message():
    store = MemoryMessageStore()
    message = create_fake_message("Racecar", is_palindrome=True)
    store.save(message)

    retrieved = store.get(message.id)
    assert retrieved is not None
    assert retrieved.id == message.id
    assert retrieved.text == "Racecar"
    assert retrieved.is_palindrome is True
    assert abs((retrieved.created_at - message.created_at).total_seconds()) < 1


def test_get_non_existing_message():
    store = MemoryMessageStore()
    result = store.get(uuid4())
    assert result is None


def test_list_messages():
    store = MemoryMessageStore()
    msg1 = create_fake_message("A")
    msg2 = create_fake_message("B")
    store.save(msg1)
    store.save(msg2)

    messages = store.list()
    assert len(messages) == 2
    texts = [m.text for m in messages]
    assert "A" in texts
    assert "B" in texts


def test_delete_existing_message():
    store = MemoryMessageStore()
    message = create_fake_message("ToDelete")
    store.save(message)

    deleted = store.delete(message.id)
    assert deleted is True
    assert store.get(message.id) is None


def test_delete_non_existing_message():
    store = MemoryMessageStore()
    deleted = store.delete(uuid4())
    assert deleted is False
