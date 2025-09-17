{% if cookiecutter.include_user_model == "yes" -%}
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema with common fields"""
    name: str
    email: EmailStr
    {% if cookiecutter.include_authentication == "jwt" -%}
    username: str
    {% endif -%}
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for creating a new user"""
    {% if cookiecutter.include_authentication == "jwt" -%}
    password: str
    {% endif -%}
    pass


{% if cookiecutter.include_authentication == "jwt" -%}
class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str
{% endif -%}


class UserUpdate(BaseModel):
    """Schema for updating a user (all fields optional)"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    {% if cookiecutter.include_authentication == "jwt" -%}
    username: Optional[str] = None
    password: Optional[str] = None
    {% endif -%}
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Schema for user response (includes all fields)"""
    id: int
    {% if cookiecutter.include_authentication == "jwt" -%}
    is_superuser: bool
    {% endif -%}
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


{% if cookiecutter.include_authentication == "jwt" -%}
class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data schema"""
    username: Optional[str] = None
{% endif -%}
{% endif -%}