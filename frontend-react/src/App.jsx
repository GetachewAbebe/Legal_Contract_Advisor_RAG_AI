import { useState, useEffect } from "react";
import { Toaster } from "react-hot-toast";
import { Trash2, PlusCircle, History, BriefcaseBusiness } from "lucide-react";
import FileUpload from "./components/FileUpload";
import ChatBox from "./components/ChatBox";

function App() {
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode);
  }, [darkMode]);

  return (
    <div className="app-container">
      <Toaster position="top-right" reverseOrder={false} />

      <div className="bg-blobs">
        <div className="blob blob-1"></div>
        <div className="blob blob-2"></div>
        <div className="blob blob-3"></div>
      </div>

      <aside className="sidebar">
        <div className="sidebar-header">
          <History size={20} className="mr-2" />
          <span>Sessions</span>
        </div>
        <button className="new-chat-btn" onClick={() => window.location.reload()}>
          <PlusCircle size={18} />
          <span>New Chat</span>
        </button>
        <div className="history-list">
          <p className="history-item active">Current Contract</p>
        </div>

        <div className="history-list">
          <p className="history-item active">Current Contract</p>
        </div>

        <div className="sidebar-upload">
          <FileUpload onUploadComplete={() => console.log("Uploaded")} />
        </div>
      </aside>

      <main className="main-content">
        <header className="header">
          <div className="header-left">
            <div className="logo-icon">
              <BriefcaseBusiness size={32} className="text-cyan-400" />
            </div>
            <div>
              <h1 className="title">Contract Advisor AI</h1>
              <p className="subtitle">
                Multi-Agent Legal Intelligence Platform
              </p>
            </div>
          </div>
        </header>

        <section className="glass-card chat-area">
          <ChatBox />
        </section>
      </main>
    </div>
  );
}

export default App;
