from typing import List, Type
from fastapi import FastAPI
from sqladmin import Admin, ModelView
from app.db.session import engine, Base
from app.admin.views import register_custom_model_views
from app.admin.dashboard import register_custom_routes
from sqlalchemy import inspect as sa_inspect
import importlib


def _import_all_models() -> None:
    # Ensure models package is imported without binding a local name 'app'
    importlib.import_module('app.models')


def discover_models() -> List[Type]:
    models: List[Type] = []
    for mapper in Base.registry.mappers:
        model_class = mapper.class_
        models.append(model_class)
    return models


def setup_admin(fastapi_app: FastAPI) -> Admin:
    _import_all_models()
    admin_title = f"{getattr(fastapi_app, 'title', 'Application')} Admin"
    admin = Admin(app=fastapi_app, engine=engine, title=admin_title)

    for model in discover_models():
        try:
            if not sa_inspect(model).primary_key:
                continue
            admin.add_view(ModelView, model=model)
        except Exception:
            continue

    register_custom_model_views(admin)
    register_custom_routes(fastapi_app)
    return admin
