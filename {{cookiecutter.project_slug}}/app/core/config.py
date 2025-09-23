from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings using pydantic-settings"""
    
    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./app.db"
    )
    
    # Application
    debug: bool = {% if cookiecutter.development_environment != "full_docker" %}True{% else %}False{% endif %}
    project_name: str = "{{cookiecutter.project_name}}"
    version: str = "{{cookiecutter.version}}"
    description: str = "{{cookiecutter.project_short_description}}"
    
    # API Configuration
    api_v1_str: str = "/api/v1"
    {% if cookiecutter.include_cors == "yes" -%}
    
    # CORS
    backend_cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:{{cookiecutter.api_port}}",
    ]
    {% endif -%}
    {% if cookiecutter.include_authentication != "none" -%}
    
    # Security
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    {% endif -%}
    {% if cookiecutter.include_rate_limiting == "yes" -%}
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    {% endif -%}
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
settings = Settings()