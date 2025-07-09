from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application settings
    app_name: str = "AI-Backed Community Legal Aid Assistant"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database settings
    database_url: str = "sqlite:///./legal_aid.db"
    
    # OpenAI settings
    openai_api_key: Optional[str] = "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"
    openai_model: str = "gpt-3.5-turbo"
    openai_max_tokens: int = 1000
    openai_temperature: float = 0.7
    
    # Alternative LLM settings (for local models)
    use_local_llm: bool = False
    local_llm_url: Optional[str] = None
    
    # Security settings
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Rate limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # 1 hour
    
    # PDF generation settings
    pdf_output_dir: str = "./generated_documents"
    
    # Legal resources settings
    default_jurisdiction: str = "US"
    enable_resource_lookup: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create global settings instance
settings = Settings()

# Ensure PDF output directory exists
os.makedirs(settings.pdf_output_dir, exist_ok=True)

