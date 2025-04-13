# src/autogen_agents/contract_tools.py
from src.components.generator import generate_answer_with_memory

def query_contract(question: str) -> str:
    """Tool to query contract using RAG + memory."""
    return generate_answer_with_memory(question)
