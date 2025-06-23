from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from app.core.database import get_db
from app.models.database import LegalIssue, LegalAdvice
from app.models.schemas import (
    LegalIssueCreate, LegalIssueResponse, 
    AdviceRequest, LegalAdviceResponse,
    AnalysisResponse, LegalCategory, UrgencyLevel
)
from app.services.llm_service import LLMService
from app.services.legal_analyzer import LegalAnalyzer

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_legal_issue(
    issue_data: LegalIssueCreate,
    db: Session = Depends(get_db)
):
    """
    Analyze a legal issue and provide categorization and initial guidance.
    """
    try:
        # Create legal issue record
        legal_issue = LegalIssue(
            description=issue_data.description,
            location=issue_data.location,
            user_email=issue_data.user_email,
            urgency=issue_data.urgency.value
        )
        db.add(legal_issue)
        db.commit()
        db.refresh(legal_issue)
        
        # Analyze the issue using LLM
        analyzer = LegalAnalyzer()
        analysis = await analyzer.analyze_issue(issue_data.description, issue_data.location)
        
        # Update the issue with analysis results
        legal_issue.category = analysis["category"]
        db.commit()
        
        return AnalysisResponse(
            category=LegalCategory(analysis["category"]),
            confidence=analysis["confidence"],
            urgency=UrgencyLevel(analysis["urgency"]),
            suggested_actions=analysis["suggested_actions"],
            relevant_templates=analysis["relevant_templates"],
            estimated_complexity=analysis["complexity"]
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing legal issue: {str(e)}"
        )

@router.post("/advice", response_model=LegalAdviceResponse)
async def generate_legal_advice(
    advice_request: AdviceRequest,
    db: Session = Depends(get_db)
):
    """
    Generate detailed legal advice for a specific issue.
    """
    try:
        # Get the legal issue
        issue = db.query(LegalIssue).filter(LegalIssue.id == advice_request.issue_id).first()
        if not issue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Legal issue not found"
            )
        
        # Generate advice using LLM
        llm_service = LLMService()
        advice_data = await llm_service.generate_advice(
            issue.description,
            issue.category,
            issue.location,
            advice_request.additional_context
        )
        
        # Create advice record
        legal_advice = LegalAdvice(
            issue_id=issue.id,
            advice=advice_data["advice"],
            next_steps=json.dumps(advice_data["next_steps"]),
            relevant_laws=json.dumps(advice_data["relevant_laws"]),
            confidence=advice_data["confidence"],
            model_used=advice_data["model_used"]
        )
        db.add(legal_advice)
        db.commit()
        db.refresh(legal_advice)
        
        return LegalAdviceResponse(
            id=legal_advice.id,
            issue_id=legal_advice.issue_id,
            advice=legal_advice.advice,
            next_steps=json.loads(legal_advice.next_steps) if legal_advice.next_steps else [],
            relevant_laws=json.loads(legal_advice.relevant_laws) if legal_advice.relevant_laws else [],
            confidence=legal_advice.confidence,
            model_used=legal_advice.model_used,
            generated_at=legal_advice.generated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating legal advice: {str(e)}"
        )

@router.get("/issues", response_model=List[LegalIssueResponse])
async def get_legal_issues(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    db: Session = Depends(get_db)
):
    """
    Get list of legal issues with optional filtering.
    """
    query = db.query(LegalIssue)
    
    if category:
        query = query.filter(LegalIssue.category == category)
    
    issues = query.offset(skip).limit(limit).all()
    return issues

@router.get("/issues/{issue_id}", response_model=LegalIssueResponse)
async def get_legal_issue(
    issue_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific legal issue by ID.
    """
    issue = db.query(LegalIssue).filter(LegalIssue.id == issue_id).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Legal issue not found"
        )
    return issue

@router.get("/issues/{issue_id}/advice", response_model=List[LegalAdviceResponse])
async def get_issue_advice(
    issue_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all advice records for a specific legal issue.
    """
    issue = db.query(LegalIssue).filter(LegalIssue.id == issue_id).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Legal issue not found"
        )
    
    advice_records = db.query(LegalAdvice).filter(LegalAdvice.issue_id == issue_id).all()
    
    # Convert to response format
    response_data = []
    for advice in advice_records:
        response_data.append(LegalAdviceResponse(
            id=advice.id,
            issue_id=advice.issue_id,
            advice=advice.advice,
            next_steps=json.loads(advice.next_steps) if advice.next_steps else [],
            relevant_laws=json.loads(advice.relevant_laws) if advice.relevant_laws else [],
            confidence=advice.confidence,
            model_used=advice.model_used,
            generated_at=advice.generated_at
        ))
    
    return response_data

