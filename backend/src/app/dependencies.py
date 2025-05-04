from app.storage.memory import MessageStore

store = MessageStore()

def get_store():
    return store
