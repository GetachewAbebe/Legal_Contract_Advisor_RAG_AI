from langchain.embeddings import OpenAIEmbeddings

def get_embeddings_model():
    """Initialize and return the OpenAI embeddings model."""
    return OpenAIEmbeddings()