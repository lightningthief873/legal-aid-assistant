from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from app.core.database import get_db
from app.models.database import LegalResource
from app.models.schemas import (
    ResourceSearchRequest, LegalResourceResponse, LegalCategory
)

router = APIRouter()

@router.post("/search", response_model=List[LegalResourceResponse])
async def search_legal_resources(
    search_request: ResourceSearchRequest,
    db: Session = Depends(get_db)
):
    """
    Search for legal resources based on jurisdiction and categories.
    """
    query = db.query(LegalResource).filter(
        LegalResource.is_active == True,
        LegalResource.jurisdiction == search_request.jurisdiction
    )
    
    # Filter by organization type if specified
    if search_request.organization_type:
        query = query.filter(LegalResource.organization_type == search_request.organization_type)
    
    resources = query.all()
    
    # Filter by categories if specified
    if search_request.categories:
        filtered_resources = []
        category_values = [cat.value for cat in search_request.categories]
        
        for resource in resources:
            if resource.categories:
                resource_categories = json.loads(resource.categories)
                if any(cat in resource_categories for cat in category_values):
                    filtered_resources.append(resource)
        resources = filtered_resources
    
    # Convert to response format
    response_data = []
    for resource in resources:
        response_data.append(LegalResourceResponse(
            id=resource.id,
            name=resource.name,
            organization_type=resource.organization_type,
            description=resource.description,
            website=resource.website,
            phone=resource.phone,
            email=resource.email,
            address=resource.address,
            jurisdiction=resource.jurisdiction,
            categories=json.loads(resource.categories) if resource.categories else []
        ))
    
    return response_data

@router.get("/resources", response_model=List[LegalResourceResponse])
async def get_legal_resources(
    jurisdiction: str = "US",
    organization_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get legal resources with optional filtering.
    """
    query = db.query(LegalResource).filter(
        LegalResource.is_active == True,
        LegalResource.jurisdiction == jurisdiction
    )
    
    if organization_type:
        query = query.filter(LegalResource.organization_type == organization_type)
    
    resources = query.offset(skip).limit(limit).all()
    
    response_data = []
    for resource in resources:
        response_data.append(LegalResourceResponse(
            id=resource.id,
            name=resource.name,
            organization_type=resource.organization_type,
            description=resource.description,
            website=resource.website,
            phone=resource.phone,
            email=resource.email,
            address=resource.address,
            jurisdiction=resource.jurisdiction,
            categories=json.loads(resource.categories) if resource.categories else []
        ))
    
    return response_data

@router.get("/resources/{resource_id}", response_model=LegalResourceResponse)
async def get_legal_resource(
    resource_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific legal resource by ID.
    """
    resource = db.query(LegalResource).filter(
        LegalResource.id == resource_id,
        LegalResource.is_active == True
    ).first()
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Legal resource not found"
        )
    
    return LegalResourceResponse(
        id=resource.id,
        name=resource.name,
        organization_type=resource.organization_type,
        description=resource.description,
        website=resource.website,
        phone=resource.phone,
        email=resource.email,
        address=resource.address,
        jurisdiction=resource.jurisdiction,
        categories=json.loads(resource.categories) if resource.categories else []
    )

@router.get("/organization-types")
async def get_organization_types(db: Session = Depends(get_db)):
    """
    Get list of available organization types.
    """
    result = db.query(LegalResource.organization_type).distinct().all()
    organization_types = [row[0] for row in result if row[0]]
    
    return {
        "organization_types": organization_types,
        "descriptions": {
            "legal_aid": "Legal aid organizations providing free or low-cost legal services",
            "court": "Court systems and judicial resources",
            "pro_bono": "Pro bono attorney networks and volunteer legal services",
            "government": "Government agencies and public legal resources",
            "nonprofit": "Nonprofit organizations providing legal assistance",
            "bar_association": "Bar associations and professional legal organizations",
            "self_help": "Self-help legal resources and educational materials"
        }
    }

@router.get("/categories")
async def get_legal_categories():
    """
    Get list of supported legal categories.
    """
    categories = [category.value for category in LegalCategory]
    
    return {
        "categories": categories,
        "descriptions": {
            "tenant_rights": "Landlord-tenant disputes, evictions, housing conditions",
            "consumer_protection": "Fraud, scams, unfair business practices",
            "employment": "Workplace issues, discrimination, wage disputes",
            "family_law": "Divorce, custody, domestic relations",
            "immigration": "Immigration status, deportation, asylum",
            "criminal": "Criminal defense, expungement, rights",
            "civil_rights": "Discrimination, civil liberties violations",
            "debt_collection": "Debt disputes, bankruptcy, creditor harassment",
            "housing": "Housing discrimination, accessibility, public housing",
            "healthcare": "Medical bills, insurance disputes, patient rights"
        }
    }

