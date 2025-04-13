import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000", // Match your FastAPI backend
});

// Upload contract file
export const uploadContract = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/upload", formData);
};

// Ask a question
export const askQuestion = (question) => {
  return api.post("/ask", { question });
};
