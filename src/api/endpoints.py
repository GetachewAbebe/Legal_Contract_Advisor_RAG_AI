import os
import logging
import asyncio
import traceback
from fastapi import APIRouter, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from src.utils.file_parser import extract_text_from_file
from src.rag_pipeline import process_contract_and_store, query_contract
from src.langgraph_agent.graph import run_chat_langgraph

logger = logging.getLogger(__name__)
router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/upload")
async def upload_contract(file: UploadFile = File(...)):
    try:
        logger.info(f"Starting upload for file: {file.filename}")
        content = await file.read()
        text = extract_text_from_file(file.filename, content)
        process_contract_and_store(text, file.filename)
        logger.info(f"Successfully processed and stored contract: {file.filename}")
        return {"message": f"{file.filename} uploaded and indexed successfully."}
    except Exception as e:
        logger.error(f"Error processing upload for {file.filename}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask")
async def ask_question(request: QueryRequest):
    try:
        logger.info(f"Processing ask query: {request.query}")
        answer = query_contract(request.query)
        return {"answer": answer}
    except Exception as e:
        logger.error("Error processing ask query", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws/chat")
async def websocket_langgraph_chat(websocket: WebSocket):
    await websocket.accept()
    client_addr = websocket.client
    logger.info(f"🔌 [WS] Client connected: {client_addr}")
    
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"📥 [WS Recv] Query: {data}")
            
            try:
                app, initial_state = run_chat_langgraph(data)
                
                # Stream events from LangGraph
                # We use stream() to get updates after each node runs
                for output in app.stream(initial_state):
                    # Output is a dict with the node name as key
                    for node_name, state_update in output.items():
                        logger.debug(f"  --> [LangGraph Node Finished]: {node_name}")
                        
                        # Get the latest message added by this node
                        if "messages" in state_update and state_update["messages"]:
                            latest_msg = state_update["messages"][0]
                            
                            # Hide the internal 'APPROVED' message from the LegalCritic to avoid cluttering the chat
                            if latest_msg.name == "LegalCritic" and latest_msg.content.strip() == "APPROVED":
                                continue
                                
                            # Send message to frontend
                            await websocket.send_json({
                                "type": "message",
                                "content": latest_msg.content,
                                "name": latest_msg.name or node_name
                            })
                            
                logger.info("✅ [WS Done] Graph execution finished for query.")
                
            except Exception as e:
                logger.error("❌ [WS] error processing query inside websocket", exc_info=True)
                
                try:
                    await websocket.send_json({
                        "type": "message",
                        "content": f"⚠️ An error occurred while processing your query: {str(e)}",
                        "name": "System"
                    })
                except Exception:
                    pass

    except WebSocketDisconnect:
        logger.info(f"🔌 [WS] Client disconnected: {client_addr}")