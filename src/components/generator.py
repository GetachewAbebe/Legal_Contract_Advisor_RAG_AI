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

# Global Lazy Instances
_rag_chain = None

def get_rag_chain():
    global _rag_chain
    if _rag_chain is None:
        embedding_model = get_embedding_model()
        
        # 🧠 Chat model
        llm = ChatOpenAI(
            model_name=settings.OPENAI_MODEL_NAME,
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=0
        )

        # 🧠 Chat memory
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )

        # 🧲 Retriever from Pinecone vector DB
        vectorstore = PineconeVectorStore.from_existing_index(
            index_name=settings.PINECONE_INDEX_NAME,
            embedding=embedding_model,
        )
        base_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})

        # 🧠 Multi-Query Retriever
        advanced_retriever = MultiQueryRetriever.from_llm(
            retriever=base_retriever, llm=llm
        )

        # 🚀 Neural Reranking (CrossEncoder)
        cross_encoder = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
        compressor = CrossEncoderReranker(model=cross_encoder, top_n=4)

        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=advanced_retriever
        )

        # 🧠 Prompt template
        template = """
        You are a legal assistant AI helping users understand contracts.
        Use the provided context to answer the user's question.
        If the answer isn't in the context, say you don't know.

        Context: {context}
        Question: {question}
        """
        QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

        # 🔗 Build the RAG chain
        _rag_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=compression_retriever,
            memory=memory,
            combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT}
        )
    return _rag_chain


def generate_answer(query: str) -> str:
    """
    Given a user query, generate a contract-aware answer using RAG with Conversational Memory.
    """
    try:
        chain = get_rag_chain()
        result = chain.invoke({"question": query})
        return result["answer"]
    except Exception as e:
        print(f"❌ Error generating answer: {e}")
        return "Sorry, something went wrong while answering your question."

# Alias for tools/compatibility 
generate_answer_with_memory = generate_answer
