import { useState, useEffect } from "react";
import FileUpload from "./components/FileUpload";
import ChatBox from "./components/ChatBox";

function App() {
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode);
  }, [darkMode]);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-white transition-all">
      <div className="max-w-3xl mx-auto px-6 py-10">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-blue-700 dark:text-blue-300">
            🧠 Contract Q&A
          </h1>
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="text-sm bg-gray-200 dark:bg-gray-800 px-3 py-1 rounded"
          >
            {darkMode ? "☀️ Light Mode" : "🌙 Dark Mode"}
          </button>
        </div>

        <div className="bg-white dark:bg-gray-800 shadow-xl rounded-2xl p-6 space-y-6">
          <FileUpload onUploadComplete={() => console.log("Uploaded")} />
          <ChatBox />
        </div>
      </div>
    </div>
  );
}

export default App;
