import pytest
from uuid import uuid4
from app.infra.storage.memory.memory_message_store import MemoryMessageStore
from app.domain.services.message_service import MessageService
from app.actions.messages.create_message import CreateMessageAction
from app.actions.messages.get_message import GetMessageAction
from app.actions.messages.list_messages import ListMessagesAction
from app.actions.messages.delete_message import DeleteMessageAction
from app.domain.model.errors import MessageNotFoundError


@pytest.fixture
def store():
    return MemoryMessageStore()


@pytest.fixture
def service():
    return MessageService()


def test_create_message_action_creates_and_stores_message(store, service):
    action = CreateMessageAction(store, service)
    message = action.execute("Racecar")

    assert message.text == "Racecar"
    assert message.is_palindrome is True
    assert store.get(message.id) == message


def test_get_message_action_returns_existing_message(store, service):
    message = CreateMessageAction(store, service).execute("Level")
    action = GetMessageAction(store)
    result = action.execute(message.id)

    assert result.id == message.id


def test_get_message_action_raises_on_missing(store):
    action = GetMessageAction(store)
    with pytest.raises(MessageNotFoundError):
        action.execute(uuid4())


def test_list_messages_action_returns_all_messages(store, service):
    CreateMessageAction(store, service).execute("One")
    CreateMessageAction(store, service).execute("Two")
    action = ListMessagesAction(store)

    messages = action.execute()
    assert len(messages) == 2


def test_delete_message_action_removes_existing(store, service):
    message = CreateMessageAction(store, service).execute("Wow")
    action = DeleteMessageAction(store)

    action.execute(message.id)
    assert store.get(message.id) is None


def test_delete_message_action_raises_on_missing(store):
    action = DeleteMessageAction(store)
    with pytest.raises(MessageNotFoundError):
        action.execute(uuid4())
