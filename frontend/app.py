import streamlit as st
import requests

st.title("📜 Contract Q&A - Ask Your Contract")

# Upload contract
st.subheader("📁 Upload Contract File")
uploaded_file = st.file_uploader("Upload a .txt, .pdf or .docx file")

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    res = requests.post("http://localhost:8000/upload", files=files)
    st.write(res.json())

# Ask question
st.subheader("💬 Ask a Question")
question = st.text_input("Enter your question")
if st.button("Ask"):
    if question:
        res = requests.post("http://localhost:8000/ask", json={"query": question})
        st.write("Answer:", res.json().get("answer"))