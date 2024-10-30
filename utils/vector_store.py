import uuid
from pinecone import Pinecone, ServerlessSpec
from config import PINECONE_API_KEY, INDEX_NAME, VECTOR_DIMENSION

def initialize_pinecone():
    """Initialize and return the Pinecone client and index."""
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    if INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=INDEX_NAME,
            dimension=VECTOR_DIMENSION,
            metric='cosine',
            spec=ServerlessSpec(cloud='aws', region='us-east-1')
        )
    
    return pc.Index(INDEX_NAME)

def upsert_chunks(index, chunks, embeddings_model):
    """Upsert document chunks with embeddings into Pinecone."""
    upsert_data = []
    for i, chunk in enumerate(chunks):
        vector = embeddings_model.embed_query(chunk)
        if vector:
            vector_id = str(uuid.uuid4())
            metadata = {"text": chunk, "chunk_index": i, "original_length": len(chunk)}
            upsert_data.append((vector_id, vector, metadata))
    
    if upsert_data:
        index.upsert(upsert_data)