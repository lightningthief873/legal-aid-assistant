from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import json
import os

from app.core.database import get_db
from app.core.config import settings
from app.models.database import DocumentTemplate, GeneratedDocument, LegalIssue
from app.models.schemas import (
    DocumentTemplateResponse, DocumentGenerationRequest,
    GeneratedDocumentResponse, DocumentType
)
from app.services.document_generator import DocumentGenerator

router = APIRouter()

@router.get("/templates", response_model=List[DocumentTemplateResponse])
async def get_document_templates(
    category: str = None,
    db: Session = Depends(get_db)
):
    """
    Get available document templates, optionally filtered by category.
    """
    query = db.query(DocumentTemplate).filter(DocumentTemplate.is_active == True)
    
    if category:
        query = query.filter(DocumentTemplate.category == category)
    
    templates = query.all()
    
    response_data = []
    for template in templates:
        response_data.append(DocumentTemplateResponse(
            id=template.id,
            name=template.name,
            category=template.category,
            description=template.description,
            required_fields=json.loads(template.required_fields) if template.required_fields else []
        ))
    
    return response_data

@router.get("/templates/{template_id}", response_model=DocumentTemplateResponse)
async def get_document_template(
    template_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific document template by ID.
    """
    template = db.query(DocumentTemplate).filter(
        DocumentTemplate.id == template_id,
        DocumentTemplate.is_active == True
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document template not found"
        )
    
    return DocumentTemplateResponse(
        id=template.id,
        name=template.name,
        category=template.category,
        description=template.description,
        required_fields=json.loads(template.required_fields) if template.required_fields else []
    )

@router.post("/generate", response_model=GeneratedDocumentResponse)
async def generate_document(
    request: DocumentGenerationRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a legal document based on a template and issue data.
    """
    try:
        # Verify the legal issue exists
        issue = db.query(LegalIssue).filter(LegalIssue.id == request.issue_id).first()
        if not issue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Legal issue not found"
            )
        
        # Verify the template exists
        template = db.query(DocumentTemplate).filter(
            DocumentTemplate.id == request.template_id,
            DocumentTemplate.is_active == True
        ).first()
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document template not found"
            )
        
        # Generate the document
        doc_generator = DocumentGenerator()
        document_data = await doc_generator.generate_document(
            template=template,
            issue=issue,
            document_type=request.document_type,
            custom_data=request.custom_data
        )
        
        # Create document record
        generated_doc = GeneratedDocument(
            issue_id=issue.id,
            template_id=template.id,
            document_type=request.document_type.value,
            file_path=document_data["file_path"],
            file_name=document_data["file_name"],
            content_data=json.dumps(document_data["content_data"])
        )
        db.add(generated_doc)
        db.commit()
        db.refresh(generated_doc)
        
        return GeneratedDocumentResponse(
            id=generated_doc.id,
            issue_id=generated_doc.issue_id,
            template_id=generated_doc.template_id,
            document_type=generated_doc.document_type,
            file_name=generated_doc.file_name,
            generated_at=generated_doc.generated_at,
            download_url=f"/api/documents/{generated_doc.id}/download"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating document: {str(e)}"
        )

@router.get("/documents/{document_id}/download")
async def download_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Download a generated document by ID.
    """
    document = db.query(GeneratedDocument).filter(GeneratedDocument.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    file_path = document.file_path
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document file not found"
        )
    
    return FileResponse(
        path=file_path,
        filename=document.file_name,
        media_type="application/pdf"
    )

@router.get("/issues/{issue_id}/documents", response_model=List[GeneratedDocumentResponse])
async def get_issue_documents(
    issue_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all generated documents for a specific legal issue.
    """
    issue = db.query(LegalIssue).filter(LegalIssue.id == issue_id).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Legal issue not found"
        )
    
    documents = db.query(GeneratedDocument).filter(GeneratedDocument.issue_id == issue_id).all()
    
    response_data = []
    for doc in documents:
        response_data.append(GeneratedDocumentResponse(
            id=doc.id,
            issue_id=doc.issue_id,
            template_id=doc.template_id,
            document_type=doc.document_type,
            file_name=doc.file_name,
            generated_at=doc.generated_at,
            download_url=f"/api/documents/{doc.id}/download"
        ))
    
    return response_data

@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a generated document.
    """
    document = db.query(GeneratedDocument).filter(GeneratedDocument.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Delete the file if it exists
    if os.path.exists(document.file_path):
        try:
            os.remove(document.file_path)
        except Exception:
            pass  # Continue even if file deletion fails
    
    # Delete the database record
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}

