# src/autogen_agents/agents.py
from autogen import AssistantAgent, UserProxyAgent
from autogen.agentchat.contrib.agent_with_tools import AssistantAgentWithTools
from src.autogen_agents.contract_tools import query_contract

def get_agents():
    # Define assistant with function tool
    assistant = AssistantAgentWithTools(
        name="ContractExpertTool",
        llm_config={"config_list": [{"model": "gpt-3.5-turbo"}]},
        tools=[
            {
                "name": "query_contract",
                "description": "Answer contract questions using the RAG pipeline.",
                "function": query_contract,
            }
        ]
    )

    # User Proxy to simulate input
    user_proxy = UserProxyAgent(
        name="User",
        human_input_mode="TERMINAL",  # or CHAT for UI-based interface
        max_consecutive_auto_reply=5,
        system_message="You are a legal user chatting with a contract assistant."
    )

    return user_proxy, assistant
