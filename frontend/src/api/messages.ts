const BASE_URL = process.env.REACT_APP_BACKEND_BASE_URL;

export const getMessages = async () => {
  const res = await fetch(`${BASE_URL}/messages`);
  return await res.json();
};

export const postMessage = async (text: string) => {
  await fetch(`${BASE_URL}/messages`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });
};

export const getMessage = async (id: string) => {
  const res = await fetch(`${BASE_URL}/messages/${id}`);
  return await res.json();
};

export const deleteMessage = async (id: string) => {
  await fetch(`${BASE_URL}/messages/${id}`, {
    method: 'DELETE',
  });
};
