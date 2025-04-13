import os
from langchain_community.vectorstores import Pinecone
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

from src.components.embedder import get_embedding_model

embedding_model = get_embedding_model()


from src.components.retriever import index  # assuming your Pinecone index instance is here

# 🔐 Load API key
openai_api_key = os.getenv("OPENAI_API_KEY")
index_name = os.getenv("PINECONE_INDEX_NAME")  # ✅ Read the index name from env
# 🧠 Chat model
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    openai_api_key=openai_api_key,
    temperature=0
)

# 🧠 Chat memory (optional, helps with context)
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 🧲 Retriever from Pinecone vector DB
retriever = Pinecone.from_existing_index(
    index_name=index_name,               # your Pinecone index name
    embedding=embedding_model,
    namespace="contracts"                # optional: change based on user/project
).as_retriever()

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
    retriever=retriever,
    memory=memory,
    combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT}
)


def generate_answer(query: str) -> str:
    """
    Given a user query, generate a contract-aware answer using RAG.
    """
    try:
        result = rag_chain.invoke({"question": query})
        return result["answer"]
    except Exception as e:
        print(f"❌ Error generating answer: {e}")
        return "Sorry, something went wrong while answering your question."
