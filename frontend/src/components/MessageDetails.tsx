import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getMessage } from '../api/messages';

export default function MessageDetails() {
  const { id } = useParams();
  const [message, setMessage] = useState<any>(null);

  useEffect(() => {
    if (id) {
      getMessage(id).then(setMessage);
    }
  }, [id]);

  if (!message) return <div>Loading...</div>;

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Message Details</h2>
      <p><strong>Text:</strong> {message.text}</p>
      <p><strong>Palindrome:</strong> {message.is_palindrome ? '✅ Yes' : '❌ No'}</p>
      <p><strong>Created at:</strong> {new Date(message.created_at).toLocaleString()}</p>
      <a href="/">← Back</a>
    </div>
  );
}
