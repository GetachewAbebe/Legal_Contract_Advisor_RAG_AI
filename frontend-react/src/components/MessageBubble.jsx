export default function MessageBubble({ role, text }) {
  const isUser = role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`px-4 py-2 rounded-2xl max-w-sm text-sm shadow ${
          isUser
            ? "bg-blue-500 text-white self-end"
            : "bg-gray-200 text-gray-800 self-start"
        }`}
      >
        <span className="block">{text}</span>
      </div>
    </div>
  );
}
