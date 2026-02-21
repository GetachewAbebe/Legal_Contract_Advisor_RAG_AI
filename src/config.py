from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    # Model Configuration
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    OPENAI_MODEL_NAME: str = "gpt-3.5-turbo"
    PINECONE_INDEX_NAME: str = "legal-index"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
