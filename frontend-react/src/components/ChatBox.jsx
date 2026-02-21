import { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import { Copy, CheckCircle2, Scale, FileText, Search, Bot, Info, Download, Eraser } from "lucide-react";
import toast from "react-hot-toast";

export default function ChatBox() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const ws = useRef(null);
  const messagesEndRef = useRef(null);

  // Setup WebSocket connection with auto-reconnect
  const reconnectTimeout = useRef(null);
  const reconnectDelay = useRef(1000);
  const intentionalClose = useRef(false);

  useEffect(() => {
    const connect = () => {
      console.log("🔌 [WS] Attempting to connect...");
      intentionalClose.current = false;
      const wsUrl = import.meta.env.VITE_WS_URL || "ws://localhost:8000/ws/chat";
      const socket = new WebSocket(wsUrl);

      socket.onopen = () => {
        console.log("✅ [WS] Connected to Backend");
        reconnectDelay.current = 1000; // Reset backoff on success
        toast.success("Connected to Legal AI");
      };

      socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log("📥 [WS Incoming]", data);

          if (data.type === "message") {
            const content = typeof data.content === 'string' ? data.content.trim() : "";

            if (content && content !== "TERMINATE") {
              setMessages((prev) => [...prev, {
                role: "agent",
                text: data.content,
                name: data.name || "LegalWorker"
              }]);
            }
            setIsTyping(false);
          }
        } catch (err) {
          console.error("❌ [WS] Parse Error:", err);
        }
      };

      socket.onclose = (event) => {
        console.log("🔌 [WS] Disconnected", event.code, event.reason);
        setIsTyping(false);
        ws.current = null;

        // Auto-reconnect unless we closed intentionally (component unmount)
        if (!intentionalClose.current) {
          const delay = reconnectDelay.current;
          console.log(`🔄 [WS] Reconnecting in ${delay}ms...`);
          reconnectTimeout.current = setTimeout(() => {
            reconnectDelay.current = Math.min(reconnectDelay.current * 2, 10000);
            connect();
          }, delay);
        }
      };

      socket.onerror = (error) => {
        console.error("❌ [WS] Connection Error:", error);
        // Don't show toast on every error — onclose handles reconnect
      };

      ws.current = socket;
    };

    connect();

    return () => {
      intentionalClose.current = true;
      if (reconnectTimeout.current) clearTimeout(reconnectTimeout.current);
      if (ws.current) ws.current.close();
    };
  }, []);

  // Auto scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendQuestion = () => {
    if (!query.trim()) return;
    if (!ws.current || ws.current.readyState !== WebSocket.OPEN) {
      toast.error("Not connected to backend. Reconnecting...");
      return;
    }

    // Echo user message to UI
    setMessages((prev) => [...prev, { role: "user", text: query }]);

    // Send over socket
    ws.current.send(query);

    setQuery("");
    setIsTyping(true);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    toast.success("Copied to clipboard!");
  };

  const downloadAnalysis = (text, name) => {
    const filename = `${name || 'Legal_Analysis'}_${new Date().getTime()}.txt`;
    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    toast.success("Analysis exported as .txt");
  };

  const clearChat = () => {
    if (window.confirm("Are you sure you want to clear the current conversation history?")) {
      setMessages([{ role: "agent", name: "System", text: "Conversation history cleared. READY for new input." }]);
      toast.success("History cleared");
    }
  };

  const getBadgeClass = (name) => {
    if (name === "LegalCritic") return "critic-badge";
    if (name === "LegalWorker") return "worker-badge";
    if (name === "ContractExpertTool") return "expert-badge";
    return "agent-badge";
  };

  const getAgentIcon = (name) => {
    const size = 16;
    if (name === "LegalCritic") return <Scale size={size} />;
    if (name === "LegalWorker") return <FileText size={size} />;
    if (name === "ContractExpertTool") return <Search size={size} />;
    if (name === "System") return <Info size={size} />;
    return <Bot size={size} />;
  };

  return (
    <div className="chat-container">
      <div className="chat-window">
        {messages.map((m, i) => (
          <div key={i} className={`chat-message ${m.role === 'user' ? 'user' : 'agent'}`}>
            {m.role === 'agent' ? (
              <div className="agent-layout">
                <div className="agent-avatar-col">
                  <div className={`avatar-circle ${getBadgeClass(m.name)}`}>
                    {getAgentIcon(m.name)}
                  </div>
                </div>
                <div className="message-col">
                  <div className="agent-name-label">{m.name}</div>
                  <div className="message-bubble">
                    <div className="relative group">
                      <ReactMarkdown>{m.text}</ReactMarkdown>
                      <div className="msg-actions">
                        <button
                          onClick={() => copyToClipboard(m.text)}
                          className="msg-action-btn"
                          title="Copy"
                        >
                          <Copy size={12} />
                        </button>
                        <button
                          onClick={() => downloadAnalysis(m.text, m.name)}
                          className="msg-action-btn"
                          title="Download"
                        >
                          <Download size={12} />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="message-bubble">
                {m.text}
              </div>
            )}
          </div>
        ))}
        {isTyping && (
          <div className="chat-message agent">
            <div className="agent-layout">
              <div className="agent-avatar-col">
                <div className="avatar-circle worker-badge">
                  <Bot size={14} className="animate-pulse" />
                </div>
              </div>
              <div className="message-col">
                <div className="agent-name-label">AI is thinking...</div>
                <div className="message-bubble">
                  <div className="typing-dots">
                    <div className="dot"></div>
                    <div className="dot"></div>
                    <div className="dot"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <input
          className="chat-input"
          type="text"
          placeholder="Ask a question about the contract..."
          value={query}
          onKeyDown={(e) => e.key === "Enter" && sendQuestion()}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          onClick={clearChat}
          className="clear-button"
          title="Clear History"
          disabled={messages.length <= 1}
        >
          <Eraser size={18} />
        </button>
        <button
          onClick={sendQuestion}
          disabled={isTyping}
          className="send-button"
        >
          Send
        </button>
      </div>

      <footer className="chat-footer">
        <p>
          <span className="font-bold">Disclaimer:</span> This AI provides legal analysis based on your provided document.
          It is for informational purposes only and does not constitute official legal advice.
        </p>
      </footer>
    </div>
  );
}
