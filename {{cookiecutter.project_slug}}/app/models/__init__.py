"""
Models package
Import all models here to make them discoverable for Alembic
"""
{% if cookiecutter.include_user_model == "yes" -%}
from .user import User

__all__ = ["User"]
{% else -%}
# Import your models here
# from .your_model import YourModel

__all__ = []
{% endif -%}