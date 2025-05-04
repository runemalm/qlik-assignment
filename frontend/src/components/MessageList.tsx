import { useEffect, useRef, useState } from 'react';
import { getMessages, postMessage, deleteMessage } from '../api/messages';
import { Link } from 'react-router-dom';

type Message = {
  id: string;
  text: string;
  is_palindrome: boolean;
  created_at: string;
};

export default function MessageList() {
  const [text, setText] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const inputRef = useRef<HTMLInputElement>(null); // 👈 create ref

  const fetchMessages = async () => {
    const data = await getMessages();
    setMessages(data);
  };

  const handleSubmit = async () => {
    if (!text.trim()) return;
    await postMessage(text.trim());
    setText('');
    fetchMessages();
    inputRef.current?.focus(); // 👈 refocus input after submit
  };

  const handleDelete = async (id: string) => {
    await deleteMessage(id);
    fetchMessages();
  };

  useEffect(() => {
    fetchMessages();
    inputRef.current?.focus(); // 👈 auto-focus on load
  }, []);

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Palindrome Checker</h1>

      <div style={{ marginBottom: '1rem' }}>
        <input
          ref={inputRef} // 👈 attach ref to input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              e.preventDefault();
              handleSubmit();
            }
          }}
          placeholder="Enter a message"
          style={{ marginRight: '0.5rem', padding: '0.5rem' }}
        />
        <button onClick={handleSubmit}>Submit</button>
      </div>

      <h2>Messages</h2>
      {messages.length === 0 ? (
        <p>No messages yet. Try entering a message above ⬆️</p>
      ) : (
        <ul style={{ listStyleType: 'none', padding: 0 }}>
          {messages.map((msg) => (
            <li key={msg.id} style={{ marginBottom: '0.5rem' }}>
              <Link to={`/messages/${msg.id}`} style={{ marginRight: '1rem' }}>
                {msg.text} → {msg.is_palindrome ? '✅' : '❌'}
              </Link>
              <button onClick={() => handleDelete(msg.id)} style={{ color: 'red' }}>
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
