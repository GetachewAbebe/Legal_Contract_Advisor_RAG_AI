from fastapi import FastAPI
from src.api.endpoints import router as api_router
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Contract Q&A - RAG System")
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)