import { useState } from "react";
import { uploadContract } from "../services/api";

export default function FileUpload({ onUploadComplete }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("📄 Please select a contract file first.");
    setUploading(true);

    try {
      await uploadContract(file);
      alert("✅ Contract uploaded successfully!");
      onUploadComplete?.();
      setFile(null); // reset input
    } catch (error) {
      console.error("Upload error:", error);
      alert("❌ Failed to upload the contract.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:gap-4">
      <input
        type="file"
        accept=".pdf,.doc,.docx"
        onChange={(e) => setFile(e.target.files[0])}
        className="block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-100 file:text-blue-700 hover:file:bg-blue-200"
      />
      <button
        onClick={handleUpload}
        disabled={!file || uploading}
        className={`px-4 py-2 rounded-xl transition text-white ${
          uploading
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-green-600 hover:bg-green-700"
        }`}
      >
        {uploading ? "Uploading..." : "Upload"}
      </button>
      {file && (
        <p className="text-xs text-gray-500 mt-1 truncate w-full sm:w-auto">
          Selected: {file.name}
        </p>
      )}
    </div>
  );
}
