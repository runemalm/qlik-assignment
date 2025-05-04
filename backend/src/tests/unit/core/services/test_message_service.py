import pytest
from app.domain.services.message_service import MessageService
from app.domain.model.message.message import Message


def test_create_message_sets_fields_correctly():
    service = MessageService()
    message = service.create_message("Racecar")

    assert isinstance(message, Message)
    assert message.text == "Racecar"
    assert message.is_palindrome is True
    assert message.id is not None
    assert message.created_at is not None


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Racecar", True),
        ("A man, a plan, a canal, Panama", True),
        ("No lemon, no melon", True),
        ("Was it a car or a cat I saw?", True),
        ("Not a palindrome", False),
        ("", True),  # edge case: empty string
        (" ", True),  # edge case: space only
        ("12321", True),
        ("12345", False),
    ],
)
def test_create_message_sets_correct_palindrome_flag(text, expected):
    service = MessageService()
    message = service.create_message(text)
    assert message.is_palindrome == expected
