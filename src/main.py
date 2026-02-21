import logging
import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings

# --- Structured Logging Setup ---
# Configure standard logging format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 🤐 Suppress verbose AI model loading logs for a cleaner terminal experience
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.WARNING) # Reduce httpx noise

from src.api.endpoints import router as api_router

app = FastAPI(
    title="Contract Advisor AI - Multi-Agent RAG",
    version="1.0.0"
)

# CORS Setup using robust configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.method} {request.url}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error. Please contact support if the issue persists."},
    )

@app.get("/health")
def health_check():
    return {"status": "online", "version": "1.0.0"}

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on {settings.HOST}:{settings.PORT}")
    uvicorn.run("src.main:app", host=settings.HOST, port=settings.PORT, reload=True)