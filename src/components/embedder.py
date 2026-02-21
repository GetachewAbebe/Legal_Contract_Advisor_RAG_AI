# src/components/embedder.py

from langchain_openai import OpenAIEmbeddings
from src.config import settings

def get_embedding_model():
    return OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL_NAME,
        openai_api_key=settings.OPENAI_API_KEY
    )
