{% if cookiecutter.include_user_model == "yes" -%}
from datetime import datetime
from typing import Optional
{% if cookiecutter.include_authentication == "jwt" -%}
from sqlalchemy import String, DateTime, func, Boolean
{% else -%}
from sqlalchemy import String, DateTime, func
{% endif -%}
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class User(Base):
    """User model{% if cookiecutter.include_authentication != "none" %} with authentication support{% endif %}"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    {% if cookiecutter.include_authentication == "jwt" -%}
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    {% endif -%}
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    {% if cookiecutter.include_authentication == "jwt" -%}
    hashed_password: Mapped[str] = mapped_column(String(255))
    {% endif -%}
    is_active: Mapped[bool] = mapped_column(default=True)
    {% if cookiecutter.include_authentication == "jwt" -%}
    is_superuser: Mapped[bool] = mapped_column(default=False)
    {% endif -%}
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"
{% endif -%}