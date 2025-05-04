from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_create_and_get_message():
    response = client.post("/messages", json={"text": "Racecar"})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data

    get_response = client.get(f"/messages/{data['id']}")
    assert get_response.status_code == 200
    result = get_response.json()
    assert result["text"] == "Racecar"
    assert result["is_palindrome"] is True

def test_list_messages():
    client.post("/messages", json={"text": "Level"})
    client.post("/messages", json={"text": "Not a palindrome"})

    response = client.get("/messages")
    assert response.status_code == 200
    messages = response.json()
    assert isinstance(messages, list)
    assert len(messages) >= 2

def test_delete_message():
    response = client.post("/messages", json={"text": "Madam"})
    message_id = response.json()["id"]

    delete_response = client.delete(f"/messages/{message_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/messages/{message_id}")
    assert get_response.status_code == 404
