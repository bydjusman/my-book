"""
API layer for the RAG chatbot.
Uses FastAPI to create a chat endpoint that internally calls query.py.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from rag_system.query import RAGChatbot
except ImportError:
    logger.error("query.py not found in rag_system directory")
    raise

# Initialize the RAG chatbot
chatbot = RAGChatbot()

# Define request/response models
class ChatRequest(BaseModel):
    message: str

class SourceInfo(BaseModel):
    content_preview: str
    source_file: str
    chunk_id: str

class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceInfo]
    status: str
    error: Optional[str] = None

# Create FastAPI app
app = FastAPI(
    title="Physical AI & Humanoid Robotics Chatbot API",
    description="RAG-based chatbot that answers questions from the textbook content",
    version="1.0.0"
)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint that processes user questions and returns answers based on textbook content.
    """
    try:
        logger.info(f"Received chat request: {request.message}")

        # Process the question using the RAG chatbot
        response = chatbot.query(request.message)

        # Return the response
        return ChatResponse(**response)

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return ChatResponse(
            question=request.message,
            answer="This topic is not covered in the book.",
            sources=[],
            status="error",
            error=str(e)
        )

@app.get("/")
async def root():
    """Root endpoint to check if the API is running"""
    return {
        "message": "Physical AI & Humanoid Robotics Chatbot API",
        "status": "running",
        "endpoints": {
            "POST /chat": "Chat with the textbook-based assistant"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Chatbot API is running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)