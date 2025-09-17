from fastapi import APIRouter
{% if cookiecutter.include_user_model == "yes" -%}
from app.api.v1.endpoints import users
{% endif -%}

api_router = APIRouter()

{% if cookiecutter.include_user_model == "yes" -%}
# Include user endpoints
api_router.include_router(users.router, prefix="/users", tags=["users"])
{% endif -%}

# Add your additional routers here
# api_router.include_router(your_router.router, prefix="/your-endpoint", tags=["your-tag"])