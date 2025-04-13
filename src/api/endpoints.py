import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from src.utils.file_parser import extract_text_from_file
from src.rag_pipeline import process_contract_and_store, query_contract

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/upload")
async def upload_contract(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = extract_text_from_file(file.filename, content)
        process_contract_and_store(text, file.filename)
        return {"message": f"{file.filename} uploaded and indexed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask")
async def ask_question(request: QueryRequest):
    try:
        answer = query_contract(request.query)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))