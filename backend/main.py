from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
from dotenv import load_dotenv

from app.routers import legal, documents, resources, health
from app.core.config import settings
from app.core.database import engine, Base

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="AI-Backed Community Legal Aid Assistant",
    description="A containerized web application that provides free, localized legal advice for common legal issues using AI/LLM technology.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(legal.router, prefix="/api", tags=["legal"])
app.include_router(documents.router, prefix="/api", tags=["documents"])
app.include_router(resources.router, prefix="/api", tags=["resources"])

@app.get("/")
async def root():
    """Root endpoint that serves the frontend or API information."""
    return {
        "message": "AI-Backed Community Legal Aid Assistant API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )

