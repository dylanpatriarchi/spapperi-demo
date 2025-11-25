"""
FastAPI application for Spapperi RAG Agent.
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Dict
import logging

from database import init_db, get_db, Document
from document_loader import DocumentLoader
from rag_agent import RAGAgent
from config import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Spapperi RAG Agent API",
    description="AI-powered assistant for Spapperi agricultural machinery company",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get settings
settings = get_settings()

# Initialize RAG agent
rag_agent = RAGAgent()


class QueryRequest(BaseModel):
    """Request model for queries."""
    question: str
    language: str = "en"


class QueryResponse(BaseModel):
    """Response model for queries."""
    question: str
    answer: str
    sources: List[Dict]
    context_used: int


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    database_connected: bool
    documents_loaded: int


@app.on_event("startup")
async def startup_event():
    """Initialize database and load documents on startup."""
    logger.info("Starting up application...")
    
    try:
        # Initialize database
        init_db()
        logger.info("✓ Database initialized")
        
        # Load documents
        db = next(get_db())
        loader = DocumentLoader()
        loader.load_all_documents(db)
        logger.info("✓ Documents loaded")
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise


@app.get("/", response_model=Dict)
async def root():
    """Root endpoint."""
    return {
        "message": "Spapperi RAG Agent API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint."""
    try:
        doc_count = db.query(Document).count()
        return HealthResponse(
            status="healthy",
            database_connected=True,
            documents_loaded=doc_count
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            database_connected=False,
            documents_loaded=0
        )


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest, db: Session = Depends(get_db)):
    """
    Query the RAG agent with a question.
    
    Args:
        request: Query request containing the question
        db: Database session
        
    Returns:
        QueryResponse with answer and sources
    """
    try:
        logger.info(f"Received query: {request.question}")
        result = rag_agent.query(db, request.question)
        logger.info("Query processed successfully")
        return QueryResponse(**result)
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats", response_model=Dict)
async def get_stats(db: Session = Depends(get_db)):
    """Get statistics about the knowledge base."""
    try:
        total_docs = db.query(Document).count()
        sources = db.query(Document.source).distinct().all()
        
        return {
            "total_documents": total_docs,
            "unique_sources": len(sources),
            "sources": [s[0] for s in sources]
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reload-documents")
async def reload_documents(db: Session = Depends(get_db)):
    """Reload all documents (admin endpoint)."""
    try:
        # Delete existing documents
        db.query(Document).delete()
        db.commit()
        
        # Reload documents
        loader = DocumentLoader()
        loader.load_all_documents(db)
        
        return {"message": "Documents reloaded successfully"}
    except Exception as e:
        logger.error(f"Error reloading documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)


