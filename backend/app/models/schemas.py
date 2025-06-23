from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class UrgencyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class LegalCategory(str, Enum):
    TENANT_RIGHTS = "tenant_rights"
    CONSUMER_PROTECTION = "consumer_protection"
    EMPLOYMENT = "employment"
    FAMILY_LAW = "family_law"
    IMMIGRATION = "immigration"
    CRIMINAL = "criminal"
    CIVIL_RIGHTS = "civil_rights"
    DEBT_COLLECTION = "debt_collection"
    HOUSING = "housing"
    HEALTHCARE = "healthcare"
    OTHER = "other"

class DocumentType(str, Enum):
    DEMAND_LETTER = "demand_letter"
    COMPLAINT_LETTER = "complaint_letter"
    NOTICE = "notice"
    RESPONSE = "response"
    PETITION = "petition"

# Request Models
class LegalIssueCreate(BaseModel):
    description: str = Field(..., min_length=10, max_length=5000)
    location: Optional[str] = Field(None, max_length=100)
    user_email: Optional[EmailStr] = None
    urgency: UrgencyLevel = UrgencyLevel.MEDIUM

class AdviceRequest(BaseModel):
    issue_id: int
    additional_context: Optional[str] = None

class DocumentGenerationRequest(BaseModel):
    issue_id: int
    template_id: int
    document_type: DocumentType
    custom_data: Optional[Dict[str, Any]] = None

class ResourceSearchRequest(BaseModel):
    jurisdiction: str = "US"
    categories: Optional[List[LegalCategory]] = None
    organization_type: Optional[str] = None

# Response Models
class LegalIssueResponse(BaseModel):
    id: int
    description: str
    category: Optional[str]
    urgency: str
    location: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class LegalAdviceResponse(BaseModel):
    id: int
    issue_id: int
    advice: str
    next_steps: Optional[List[str]]
    relevant_laws: Optional[List[str]]
    confidence: float
    model_used: Optional[str]
    generated_at: datetime
    
    class Config:
        from_attributes = True

class DocumentTemplateResponse(BaseModel):
    id: int
    name: str
    category: str
    description: Optional[str]
    required_fields: Optional[List[str]]
    
    class Config:
        from_attributes = True

class GeneratedDocumentResponse(BaseModel):
    id: int
    issue_id: int
    template_id: int
    document_type: str
    file_name: str
    generated_at: datetime
    download_url: str
    
    class Config:
        from_attributes = True

class LegalResourceResponse(BaseModel):
    id: int
    name: str
    organization_type: str
    description: Optional[str]
    website: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    jurisdiction: str
    categories: Optional[List[str]]
    
    class Config:
        from_attributes = True

class AnalysisResponse(BaseModel):
    category: LegalCategory
    confidence: float
    urgency: UrgencyLevel
    suggested_actions: List[str]
    relevant_templates: List[DocumentTemplateResponse]
    estimated_complexity: str  # simple, moderate, complex

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    database_connected: bool
    llm_available: bool

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime

