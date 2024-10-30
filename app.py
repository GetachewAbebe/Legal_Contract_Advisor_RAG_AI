import streamlit as st
import json
from config import CONTRACT_FILE_PATH, EVALUATION_FILE_PATH, OPENAI_API_KEY
from utils.document import read_docx, chunk_text
from utils.embeddings import get_embeddings_model
from utils.vector_store import initialize_pinecone, upsert_chunks
from utils.answer import query_chunks, generate_answer

st.title("Contract Advisor RAG")

# Initialize
embeddings_model = get_embeddings_model()
index = initialize_pinecone()

# Session state for contract chunks
if 'contract_chunks' not in st.session_state:
    contract_text = read_docx(CONTRACT_FILE_PATH)
    st.session_state.contract_chunks = chunk_text(contract_text)
    upsert_chunks(index, st.session_state.contract_chunks, embeddings_model)
    st.success("Contract document processed and stored successfully.")

# Load evaluation data
try:
    with open(EVALUATION_FILE_PATH, 'r') as f:
        evaluation_data = json.load(f)
except Exception as e:
    st.error(f"Error loading evaluation file: {str(e)}")
    evaluation_data = None

# User input
user_question = st.text_input("Enter your question:")
if st.button("Submit"):
    if user_question:
        try:
            query_vector = embeddings_model.embed_query(user_question)
            context_chunks = query_chunks(index, query_vector)
            context = "\n".join(context_chunks)
            
            answer = generate_answer(context, user_question, evaluation_data)
            st.subheader("Contract Advisor RAG")
            st.write(f"**Question:** {user_question}")
            st.write(f"**Answer:** {answer}")
        except Exception as e:
            st.error(f"Error during query processing: {str(e)}")