"""
CRUD operations package
Import all CRUD operations here
"""
{% if cookiecutter.include_user_model == "yes" -%}
from .user import (
    get_user,
    get_user_by_email,
    {% if cookiecutter.include_authentication == "jwt" -%}
    get_user_by_username,
    authenticate_user,
    {% endif -%}
    get_users,
    create_user,
    update_user,
    delete_user,
)

__all__ = [
    "get_user",
    "get_user_by_email",
    {% if cookiecutter.include_authentication == "jwt" -%}
    "get_user_by_username",
    "authenticate_user",
    {% endif -%}
    "get_users",
    "create_user",
    "update_user",
    "delete_user",
]
{% else -%}
# Import your CRUD operations here
# from .your_crud import your_crud_operations

__all__ = []
{% endif -%}