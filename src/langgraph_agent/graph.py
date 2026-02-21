import os
import operator
import logging
from typing import Annotated, TypedDict, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

# Import the existing RAG pipeline function
from src.rag_pipeline import query_contract

logger = logging.getLogger(__name__)

# 1. Define the State
class AgentState(TypedDict):
    query: str
    context: str
    summary: str
    critique_feedback: str
    revision_count: int
    messages: Annotated[Sequence[BaseMessage], operator.add]

# 2. Define the Nodes

def retrieve_node(state: AgentState):
    """Retrieves legal context using the existing RAG pipeline."""
    query = state["query"]
    logger.info(f"🔍 [LangGraph] Retrieving context for: '{query}'")
    
    try:
        context = query_contract(query)
    except Exception as e:
        logger.error(f"Error retrieving context for query: {query}", exc_info=True)
        context = f"Error retrieving context: {str(e)}"
        
    return {
        "context": context,
        "messages": [AIMessage(content=f"I have retrieved the relevant contract clauses.", name="ContractExpertTool")]
    }

def summarize_node(state: AgentState):
    """Synthesizes the retrieved context into a legal summary."""
    logger.info("✍️ [LangGraph] Generating legal summary...")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    query = state["query"]
    context = state["context"]
    feedback = state.get("critique_feedback", "")
    
    system_msg = (
        "You are the Legal Synthesizer. You review extracted contract information and provide a clear, "
        "professional legal summary answering the user's question."
    )
    
    prompt = f"User Question: {query}\n\nContract Context:\n{context}\n"
    if feedback:
        prompt += f"\nCritique Feedback to address:\n{feedback}\n"
        
    response = llm.invoke([
        SystemMessage(content=system_msg),
        HumanMessage(content=prompt)
    ])
    
    summary = response.content
    return {
        "summary": summary,
        "messages": [AIMessage(content=summary, name="LegalWorker")]
    }

def critique_node(state: AgentState):
    """Critiques the summary for hallucinations or missing details."""
    logger.info("🧐 [LangGraph] Critiquing the summary...")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    query = state["query"]
    context = state["context"]
    summary = state["summary"]
    
    system_msg = (
        "You are the Senior Legal Critic. Strictly review the LegalWorker's summary against the raw contract context. "
        "If it hallucinates, misses crucial details, or contradicts the text, point out the error and politely ask for a rewrite. "
        "If it is perfect and factually sound, reply with exactly 'APPROVED'."
    )
    
    prompt = (
        f"User Question: {query}\n"
        f"Raw Contract Context:\n{context}\n\n"
        f"LegalWorker Summary to Review:\n{summary}\n"
    )
    
    response = llm.invoke([
        SystemMessage(content=system_msg),
        HumanMessage(content=prompt)
    ])
    
    critique = response.content
    return {
        "critique_feedback": critique,
        "revision_count": state.get("revision_count", 0) + 1,
        "messages": [AIMessage(content=critique, name="LegalCritic")]
    }

# 3. Define Conditional Edges

def should_continue(state: AgentState):
    """Decides whether to cycle back for a rewrite or end."""
    critique = state["critique_feedback"]
    revisions = state.get("revision_count", 0)
    
    if "APPROVED" in critique.upper() or revisions >= 3:
        return END
    return "summarize"

# 4. Build the Graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("summarize", summarize_node)
workflow.add_node("critique", critique_node)

# Add edges
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "summarize")
workflow.add_edge("summarize", "critique")
workflow.add_conditional_edges("critique", should_continue)

# Compile
app = workflow.compile()

def run_chat_langgraph(message: str):
    """Entry point for the backend to run the graph."""
    logger.info(f"🚀 [LangGraph] Starting graph execution for: '{message}'")
    
    initial_state = {
        "query": message,
        "context": "",
        "summary": "",
        "critique_feedback": "",
        "revision_count": 0,
        "messages": [HumanMessage(content=message, name="User")]
    }
    
    # We will stream the events back to the websocket in endpoints.py
    # This just returns the compiled app and initial state
    return app, initial_state
