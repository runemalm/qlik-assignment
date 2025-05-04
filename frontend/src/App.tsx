import { Routes, Route } from 'react-router-dom';
import MessageList from './components/MessageList';
import MessageDetails from './components/MessageDetails';

function App() {
  return (
    <Routes>
      <Route path="/" element={<MessageList />} />
      <Route path="/messages/:id" element={<MessageDetails />} />
    </Routes>
  );
}

export default App;
