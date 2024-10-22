import autogen
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen.agentchat.contrib.vector_store_agent import VectorStoreAgent # type: ignore

llm_config = {"config_list": [{"model": "gpt-4o"}]}
code_execution_config = {"use_docker": False}

# Initialize the assistant agent with the given configurations
config_list = [
    {"model": "gpt-4o", "api_type": "openai"},
]
assistant = RetrieveAssistantAgent(
    name="assistant",
    system_message="You are a knowledgeable contract assistant. Your task is to provide precise and accurate answers to user questions based on the content of the contract document. Always refer to the specific section and clause of the contract where the information is found to support your response.",
    llm_config=llm_config,
    code_execution_config=code_execution_config,
    human_input_mode="NEVER",  # Never ask for human input
)
# Initialize the proxy agent responsible for retrieving documents and handling the Q&A
ragproxyagent = RetrieveUserProxyAgent(
    name="ragproxyagent",
    retrieve_config={
        "task": "qa",
        "docs_path": "data",
        "chunk_token_size": 250,
        "model": config_list[0]["model"],
        "vector_db": "chroma",
        "overwrite": True,
    },
    code_execution_config=code_execution_config,
    human_input_mode="NEVER",  # Never ask for human input
)
# Initialize the vector store agent to manage the document embeddings
vector_store_agent = VectorStoreAgent(
    vector_db="chroma",
    embedding_model="openai",
    embedding_model_config={"name": "text-embedding-ada-002"},
    code_execution_config=code_execution_config,
)
def autogen_bot(file_path, question):
    # Load the contract documents into the vector store
    vector_store_agent.load_documents(path=file_path)

    # Reset the assistant's state (if needed)
    assistant.reset()

    # Initiate the chat with the assistant using the proxy agent
    ragproxyagent.initiate_chat(
        assistant,
        message=ragproxyagent.message_generator,
        problem=question
    )
    return ragproxyagent.last_message()