# src/autogen_agents/chat_entry.py
from autogen import GroupChat, GroupChatManager
from src.autogen_agents.agents import get_agents

def run_chat():
    user_proxy, assistant = get_agents()

    group_chat = GroupChat(
        agents=[user_proxy, assistant],
        messages=[],
        max_round=10
    )

    manager = GroupChatManager(groupchat=group_chat)

    user_proxy.initiate_chat(manager, message="Who are the parties in this contract?")
