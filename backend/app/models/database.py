from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class LegalIssue(Base):
    """Model for storing legal issues submitted by users."""
    __tablename__ = "legal_issues"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    urgency = Column(String(20), default="medium")  # low, medium, high
    location = Column(String(100), nullable=True)
    user_email = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    advice_records = relationship("LegalAdvice", back_populates="issue")
    documents = relationship("GeneratedDocument", back_populates="issue")

class LegalAdvice(Base):
    """Model for storing generated legal advice."""
    __tablename__ = "legal_advice"
    
    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(Integer, ForeignKey("legal_issues.id"), nullable=False)
    advice = Column(Text, nullable=False)
    next_steps = Column(Text, nullable=True)  # JSON string of steps
    relevant_laws = Column(Text, nullable=True)  # JSON string of laws
    confidence = Column(Float, default=0.0)
    model_used = Column(String(100), nullable=True)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    issue = relationship("LegalIssue", back_populates="advice_records")

class DocumentTemplate(Base):
    """Model for storing document templates."""
    __tablename__ = "document_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    template_content = Column(Text, nullable=False)
    required_fields = Column(Text, nullable=True)  # JSON string of required fields
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    documents = relationship("GeneratedDocument", back_populates="template")

class GeneratedDocument(Base):
    """Model for storing generated documents."""
    __tablename__ = "generated_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(Integer, ForeignKey("legal_issues.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("document_templates.id"), nullable=False)
    document_type = Column(String(100), nullable=False)  # notice, complaint, demand, etc.
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(200), nullable=False)
    content_data = Column(Text, nullable=True)  # JSON string of filled data
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    issue = relationship("LegalIssue", back_populates="documents")
    template = relationship("DocumentTemplate", back_populates="documents")

class LegalResource(Base):
    """Model for storing legal resources and organizations."""
    __tablename__ = "legal_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    organization_type = Column(String(100), nullable=False)  # legal_aid, court, pro_bono, etc.
    description = Column(Text, nullable=True)
    website = Column(String(500), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    jurisdiction = Column(String(100), nullable=False)
    categories = Column(Text, nullable=True)  # JSON string of legal categories
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

