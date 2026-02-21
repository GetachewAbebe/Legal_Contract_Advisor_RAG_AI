# Removed unused import
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain.retrievers import ContextualCompressionRetriever
from langchain_pinecone import PineconeVectorStore

from src.components.embedder import get_embedding_model
from src.config import settings

embedding_model = get_embedding_model()

from src.components.retriever import index  # assuming your Pinecone index instance is here

# 🧠 Chat model
llm = ChatOpenAI(
    model_name=settings.OPENAI_MODEL_NAME,
    openai_api_key=settings.OPENAI_API_KEY,
    temperature=0
)

# 🧠 Chat memory (optional, helps with context)
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"  # Needed when return_source_documents=True
)

# 🧲 Retriever from Pinecone vector DB
vectorstore = PineconeVectorStore.from_existing_index(
    index_name=settings.PINECONE_INDEX_NAME,               # your Pinecone index name
    embedding=embedding_model,
)
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})  # Fetch more chunks for the reranker

# 🧠 Enhancement 2: Multi-Query Retriever to improve recall
advanced_retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever, llm=llm
)

# 🚀 Phase 1 Modernization: Neural Reranking (CrossEncoder)
# Note: Using a lightweight BGE reranker for fast CPU inference
cross_encoder = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
compressor = CrossEncoderReranker(model=cross_encoder, top_n=4)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=advanced_retriever
)

# 🧠 Prompt template (optional but encouraged)
template = """
You are a legal assistant AI helping users understand contracts.
Use the provided context to answer the user's question.
If the answer isn't in the context, say you don't know.

Context: {context}
Question: {question}
"""

QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

# 🔗 Build the RAG chain
rag_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=compression_retriever, # Phase 1: Using Neural Reranker on top of MultiQuery
    memory=memory, # Enhancement 1: Global session memory is active
    combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT}
)


def generate_answer(query: str) -> str:
    """
    Given a user query, generate a contract-aware answer using RAG with Conversational Memory.
    """
    try:
        result = rag_chain.invoke({"question": query})
        return result["answer"]
    except Exception as e:
        print(f"❌ Error generating answer: {e}")
        return "Sorry, something went wrong while answering your question."

# Alias for tools/compatibility 
generate_answer_with_memory = generate_answer
