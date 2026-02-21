from langchain_pinecone import PineconeVectorStore as LangchainPinecone
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from src.config import settings

_index = None
_embedding_model = None
_retriever = None

def get_index():
    global _index
    if _index is None:
        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        _index = pc.Index(settings.PINECONE_INDEX_NAME)
    return _index

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL_NAME,
            openai_api_key=settings.OPENAI_API_KEY
        )
    return _embedding_model

def get_retriever():
    global _retriever
    if _retriever is None:
        _retriever = LangchainPinecone(get_index(), get_embedding_model(), "text").as_retriever()
    return _retriever

# Exported functions
def upsert_chunks(texts, metadatas):
    vectorstore = LangchainPinecone(get_index(), get_embedding_model(), "text")
    vectorstore.add_texts(texts=texts, metadatas=metadatas)

def retrieve_chunks(query):
    return get_retriever().get_relevant_documents(query)
