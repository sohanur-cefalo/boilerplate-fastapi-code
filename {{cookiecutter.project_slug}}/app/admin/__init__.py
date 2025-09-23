from typing import List, Type
from fastapi import FastAPI
from sqladmin import Admin, ModelView
from app.db.session import engine, Base
from app.admin.views import register_custom_model_views
from app.admin.dashboard import register_custom_routes
from sqlalchemy import inspect as sa_inspect


def _import_all_models() -> None:
    """Ensure all models are imported so SQLAlchemy mappers are registered."""
    # Importing app.models triggers submodule imports declared by the user
    # (e.g., from .user import User) which registers mappers on Base.registry
    import importlib  # noqa: F401
    import app.models  # noqa: F401


def discover_models() -> List[Type]:
    """Discover all SQLAlchemy model classes registered on Base."""
    models: List[Type] = []
    for mapper in Base.registry.mappers:
        model_class = mapper.class_
        models.append(model_class)
    return models


def setup_admin(fastapi_app: FastAPI) -> Admin:
    """Initialize SQLAdmin, register views for discovered models, and attach custom hooks."""
    _import_all_models()
    admin_title = f"{getattr(fastapi_app, 'title', 'Application')} Admin"
    admin = Admin(fastapi_app, engine, title=admin_title)

    # Auto-register all models, skipping any that cannot be introspected yet
    for model in discover_models():
        try:
            # Only register models with a detectable primary key
            pk = sa_inspect(model).primary_key
            if not pk:
                continue
            # Let SQLAdmin handle view class generation
            admin.add_view(ModelView, model=model)
        except Exception:
            # Silently skip problematic models (e.g., no PK); user can add custom view in app/admin/views.py
            continue

    # Register any custom ModelViews defined by user
    register_custom_model_views(admin)

    # Attach optional custom admin routes (dashboards, charts)
    register_custom_routes(fastapi_app)

    return admin
