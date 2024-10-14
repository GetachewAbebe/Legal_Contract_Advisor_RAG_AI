from data_extractor import extract_text_from_docx

import os
import asyncio
from typing import List, Tuple
from dotenv import load_dotenv
from pinecone import Pinecone as PineconeClient
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone
from data_extractor import extract_text_from_docx
import logging

load_dotenv()
OPENAI_API_KEY = os.getenv("OPEN_AI_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEYS")
PINECONE_INDEX_NAME = "contractadvisor"
NAMESPACE = "Robinson"
MAX_TOKENS = 300
EMBEDDING_MODEL = "text-embedding-ada-002"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def chunk_text(text: str) -> List[str]:
    """
    Chunk input text into segments of approximately MAX_TOKENS tokens.

    Args:
    - text (str): The input text to be chunked.

    Returns:
    - list: List of chunked text segments.
    """
    chunks = []
    current_chunk = ""
    tokens_count = 0
    sentences = text.split(". ")

    for sentence in sentences:
        if tokens_count + len(sentence.split()) > MAX_TOKENS:
            chunks.append(current_chunk.strip())
            current_chunk = ""
            tokens_count = 0
        current_chunk += sentence + ". "
        tokens_count += len(sentence.split())

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

from sentence_transformers import SentenceTransformer
import torch

async def embed_text(chunked_text: List[str]) -> List[List[float]]:
    try:
        model = SentenceTransformer('paraphrase-distilroberta-base-v1')
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model.to(device)
        document_embeddings = model.encode(chunked_text, device=device)
        return document_embeddings
    except Exception as e:
        logger.error(f"Error embedding text: {str(e)}")
        return []

async def vectorize(chunked_text: List[str], document_embeddings: List[List[float]]) -> None:
    try:
        index = PineconeClient(PINECONE_API_KEY).Index(PINECONE_INDEX_NAME)
        upsert_data = [{"id": str(i), "values": embedding} for i, embedding in enumerate(document_embeddings)]
        index.upsert(upsert_data, namespace=NAMESPACE)
    except Exception as e:
        logger.error(f"Error vectorizing text: {str(e)}")

async def process_pdf(pdf_path: str) -> None:
    """
    Extract text from a PDF file, chunk the text, embed the chunks, and vectorize the embeddings.

    Args:
    - pdf_path (str): Path to the PDF file.

    Returns:
    - None
    """
    try:
        result = extract_text_from_docx(pdf_path)
        text = "\n\n".join(result).replace("\n", " ")
        chunked_text = await chunk_text(text)
        document_embeddings = await embed_text(chunked_text)
        await vectorize(chunked_text, document_embeddings)
    except Exception as e:
        logger.error(f"Error processing PDF file: {str(e)}")

if __name__ == "__main__":
    asyncio.run(process_pdf("data/Robinson_Advisory.docx"))
