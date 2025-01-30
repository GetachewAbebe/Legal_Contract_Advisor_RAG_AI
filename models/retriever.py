import os
from pinecone import Pinecone
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)

existing_indexes = pc.list_indexes().names()
if PINECONE_INDEX_NAME not in existing_indexes:
    raise ValueError(f"Pinecone index '{PINECONE_INDEX_NAME}' does not exist.")

embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY)
vector_store = PineconeVectorStore.from_existing_index(PINECONE_INDEX_NAME, embedding_model)

def store_contract_chunks(contract_chunks):
    """Stores contract chunks in Pinecone."""
    PineconeVectorStore.from_documents(contract_chunks, embedding_model, index_name=PINECONE_INDEX_NAME)

def get_retriever():
    """Returns retriever for querying"""
    return vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
