import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import toast from "react-hot-toast";
import { Upload, FileCheck, AlertCircle, Loader2 } from "lucide-react";
import { uploadContract } from "../services/api";

export default function FileUpload({ onUploadComplete }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [progress, setProgress] = useState(0);

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      setSuccess(false);
      setProgress(0);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    multiple: false,
    disabled: uploading
  });

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setSuccess(false);
    setProgress(10);

    const interval = setInterval(() => {
      setProgress((prev) => (prev < 90 ? prev + 10 : prev));
    }, 500);

    try {
      await uploadContract(file);
      clearInterval(interval);
      setProgress(100);
      setSuccess(true);
      toast.success("Contract analyzed and indexed!");
      onUploadComplete?.();

      setTimeout(() => {
        setSuccess(false);
        setFile(null);
        setProgress(0);
      }, 3000);
    } catch (error) {
      clearInterval(interval);
      setProgress(0);
      toast.error("Failed to analyze the contract.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div
      {...getRootProps()}
      className={`upload-zone ${isDragActive ? 'drag-active' : ''} ${success ? 'upload-success' : ''}`}
    >
      <input {...getInputProps()} />

      <div className="upload-icon">
        {uploading ? <Loader2 className="animate-spin text-blue-400" size={32} /> :
          success ? <FileCheck className="text-emerald-400" size={32} /> :
            <Upload className={isDragActive ? "text-cyan-400" : "text-slate-400"} size={32} />}
      </div>

      <p className="upload-text">
        {uploading ? "Neural Indexing..." :
          success ? "Legally Indexed & Ready!" :
            file ? file.name :
              isDragActive ? "Drop here..." : "Welcome to the Contract Advisor. Upload a document and ask a question below."}
      </p>

      <div className={`progress-container ${uploading || success ? 'active' : ''}`}>
        <div className="progress-bar" style={{ width: `${progress}%` }}></div>
      </div>

      {file && !success && !uploading && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            handleUpload();
          }}
          className="send-button mt-4"
          style={{ marginTop: '1.5rem', width: '100%', padding: '12px' }}
        >
          Start Legal Analysis
        </button>
      )}
    </div>
  );
}
