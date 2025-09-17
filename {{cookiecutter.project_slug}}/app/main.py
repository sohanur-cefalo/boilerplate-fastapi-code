from fastapi import FastAPI{% if cookiecutter.include_rate_limiting == "yes" %}, Request{% endif %}
{% if cookiecutter.include_cors == "yes" -%}
from fastapi.middleware.cors import CORSMiddleware
{% endif -%}
{% if cookiecutter.include_rate_limiting == "yes" -%}
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
{% endif -%}
from app.core.config import settings
from app.api.v1.api import api_router

{% if cookiecutter.include_rate_limiting == "yes" -%}
# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
{% endif -%}

# Create FastAPI application
app = FastAPI(
    title=settings.project_name,
    description=settings.description,
    version=settings.version,
    debug=settings.debug,
)

{% if cookiecutter.include_rate_limiting == "yes" -%}
# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
{% endif -%}

{% if cookiecutter.include_cors == "yes" -%}
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
{% endif -%}

# Include API router
app.include_router(api_router, prefix=settings.api_v1_str)


@app.get("/")
{% if cookiecutter.include_rate_limiting == "yes" -%}
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
{% endif -%}
def read_root({% if cookiecutter.include_rate_limiting == "yes" %}request: Request{% endif %}):
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.project_name}",
        "version": settings.version,
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "project": settings.project_name}