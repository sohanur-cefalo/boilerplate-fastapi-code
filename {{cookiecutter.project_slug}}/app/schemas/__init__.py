"""
Schemas package
Import all Pydantic schemas here
"""
{% if cookiecutter.include_user_model == "yes" -%}
from .user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    {% if cookiecutter.include_authentication == "jwt" -%}
    UserLogin,
    Token,
    TokenData,
    {% endif -%}
)

__all__ = [
    "UserBase",
    "UserCreate", 
    "UserUpdate",
    "UserResponse",
    {% if cookiecutter.include_authentication == "jwt" -%}
    "UserLogin",
    "Token",
    "TokenData",
    {% endif -%}
]
{% else -%}
# Import your schemas here
# from .your_schema import YourSchema

__all__ = []
{% endif -%}