
from src.components.chunker import chunk_text
from src.components.retriever import upsert_chunks, retrieve_chunks
from src.components.generator import generate_answer

def process_contract_and_store(text: str, file_name: str):
    chunks = chunk_text(text)
    # Ensure metadata is a list of dictionaries matching the number of chunks
    metadatas = [{"source": file_name} for _ in chunks]
    upsert_chunks(chunks, metadatas)

def query_contract(question: str):
    return generate_answer(question)