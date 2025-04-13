
from src.components.chunker import chunk_text
from src.components.retriever import upsert_chunks, retrieve_chunks
from src.components.generator import generate_answer

def process_contract_and_store(text: str, file_name: str):
    chunks = chunk_text(text)
    upsert_chunks(chunks, file_name)

def query_contract(question: str):
    chunks = retrieve_chunks(question)
    return generate_answer(question, chunks)