from langchain_pinecone import PineconeVectorStore as LangchainPinecone
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from src.config import settings

# Initialize Pinecone client
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

# Initialize Pinecone index directly (bypassing control plane checks to avoid 500 errors)
index = pc.Index(settings.PINECONE_INDEX_NAME)

# Set up embeddings
embedding_model = OpenAIEmbeddings(
    model=settings.EMBEDDING_MODEL_NAME,
    openai_api_key=settings.OPENAI_API_KEY
)

# Initialize retriever from existing index
retriever = LangchainPinecone(index, embedding_model, "text").as_retriever()

# Exported functions
def upsert_chunks(texts, metadatas):
    vectorstore = LangchainPinecone(index, embedding_model, "text")
    vectorstore.add_texts(texts=texts, metadatas=metadatas)

def retrieve_chunks(query):
    return retriever.get_relevant_documents(query)
