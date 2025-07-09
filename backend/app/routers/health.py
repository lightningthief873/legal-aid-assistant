from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import os

from app.core.database import get_db
from app.core.config import settings
from app.models.schemas import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint to verify system status.
    """
    try:
        # Test database connection using SQLAlchemy 2.0+ syntax
        db.execute(text("SELECT 1"))
        database_connected = True
    except Exception as e:
        print(f"Database connection error: {e}")
        database_connected = False
    
    # Test LLM availability
    llm_available = bool(settings.openai_api_key) or settings.use_local_llm
    
    return HealthResponse(
        status="healthy" if database_connected and llm_available else "degraded",
        timestamp=datetime.utcnow(),
        version=settings.app_version,
        database_connected=database_connected,
        llm_available=llm_available
    )

@router.get("/info")
async def app_info():
    """
    Get application information and configuration.
    """
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "AI-Backed Community Legal Aid Assistant",
        "features": [
            "Legal issue analysis and categorization",
            "AI-powered legal advice generation",
            "Document template generation",
            "Local legal resource lookup",
            "PDF document creation"
        ],
        "supported_categories": [
            "tenant_rights",
            "consumer_protection", 
            "employment",
            "family_law",
            "immigration",
            "criminal",
            "civil_rights",
            "debt_collection",
            "housing",
            "healthcare"
        ],
        "api_docs": "/api/docs"
    }