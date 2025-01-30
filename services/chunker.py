from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

def chunk_contract(contract_text, chunk_size=500, chunk_overlap=50):
    """Splits contract text into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.create_documents([contract_text])
