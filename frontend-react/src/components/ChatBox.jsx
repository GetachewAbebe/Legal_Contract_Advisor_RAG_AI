import { useState } from "react";
import { askQuestion } from "../services/api";
import MessageBubble from "./MessageBubble";

export default function ChatBox() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);

  const sendQuestion = async () => {
    if (!query.trim()) return;

    setMessages((prev) => [...prev, { role: "user", text: query }]);
    setQuery("");
    setIsTyping(true); // Start typing indicator

    try {
      const res = await askQuestion(query);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: res.data.answer },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: "❌ Failed to get response." },
      ]);
    } finally {
      setIsTyping(false); // Stop typing indicator
    }
  };

  return (
    <div>
      <div className="space-y-3 max-h-[50vh] overflow-y-auto pr-2 mb-3">
        {messages.map((m, i) => (
          <MessageBubble key={i} role={m.role} text={m.text} />
        ))}
        {isTyping && (
          <div className="animate-pulse text-gray-500">🤖 AI is typing...</div>
        )}
      </div>

      <div className="flex gap-2">
        <input
          className="w-full border rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
          type="text"
          placeholder="Ask a question about the contract..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          onClick={sendQuestion}
          className="bg-blue-600 text-white px-4 py-2 rounded-xl hover:bg-blue-700 transition"
        >
          Ask
        </button>
      </div>
    </div>
  );
}
