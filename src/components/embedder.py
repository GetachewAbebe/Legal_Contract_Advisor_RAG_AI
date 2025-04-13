# src/components/embedder.py

import os
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings

load_dotenv()

def get_embedding_model():
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
