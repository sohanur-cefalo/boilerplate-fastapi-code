from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings using pydantic-settings"""
    
    # Database
    database_url: str = "postgresql://username:password@localhost:5432/your_database_name"
    
    # Application
    debug: bool = True
    project_name: str = "Your FastAPI Project"
    version: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
settings = Settings()
