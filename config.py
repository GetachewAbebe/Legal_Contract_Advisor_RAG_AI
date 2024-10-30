import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
CONTRACT_FILE_PATH = "/path/to/contract.docx"  # Change this path
EVALUATION_FILE_PATH = "/path/to/evaluation.json"  # Change this path
INDEX_NAME = "contractadvisor"
VECTOR_DIMENSION = 1536  # Dimensionality of OpenAI embeddings