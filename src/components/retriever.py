import os
from langchain_pinecone import PineconeVectorStore as LangchainPinecone
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
api_key = os.getenv("PINECONE_API_KEY")
env = os.getenv("PINECONE_ENVIRONMENT")  # Format: "us-east-1-aws"
index_name = os.getenv("PINECONE_INDEX_NAME")

# Initialize Pinecone client
pc = Pinecone(api_key=api_key)

# Initialize Pinecone index directly (bypassing control plane checks to avoid 500 errors)
index = pc.Index(index_name)

# Set up embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Initialize retriever from existing index
retriever = LangchainPinecone(index, embedding_model, "text").as_retriever()

# Exported functions
def upsert_chunks(texts, metadatas):
    vectorstore = LangchainPinecone(index, embedding_model, "text")
    vectorstore.add_texts(texts=texts, metadatas=metadatas)

def retrieve_chunks(query):
    return retriever.get_relevant_documents(query)
