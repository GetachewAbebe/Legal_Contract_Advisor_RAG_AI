import streamlit as st
import requests
import os

API_URL = "http://127.0.0.1:8000"

st.title("📜 Legal Contract Q&A")
st.write("Upload a contract and ask legal questions.")

# Contract Upload Section
st.subheader("📂 Upload Contract File")
uploaded_file = st.file_uploader("Upload a contract (PDF or TXT)", type=["pdf", "txt"])

if uploaded_file:
    with st.spinner("Uploading and processing the contract..."):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(f"{API_URL}/upload_contract/", files=files)
        if response.status_code == 200:
            st.success("✅ Contract uploaded and stored successfully!")
        else:
            st.error("❌ Failed to upload contract.")

# Contract Q&A Section
st.subheader("💬 Ask a Question about the Contract")
question = st.text_input("Enter your legal question:")

if question:
    response = requests.get(f"{API_URL}/ask/", params={"question": question})
    if response.status_code == 200:
        answer = response.json().get("answer", "No answer found.")
        st.write("### 📌 Answer:")
        st.write(answer)
    else:
        st.error("❌ Error retrieving response.")
