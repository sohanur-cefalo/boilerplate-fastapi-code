#!/usr/bin/env python3
"""
FastAPI Boilerplate Interactive Shell
====================================

This script provides an interactive Python shell with all database models,
sessions, and CRUD functions pre-loaded for easy database interaction.

Usage:
    python management/shell.py

Features:
- Pre-loaded database session
- All models imported and ready to use
- All CRUD functions available
- Modern SQLAlchemy 2.0 syntax
- Tab completion support
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from app.db.session import SessionLocal, engine, Base
from app.models import User
from app.crud import (
    get_user, get_user_by_email, get_users,
    create_user, update_user, delete_user
)
from app.schemas.user import UserCreate, UserUpdate

# Create database session
db = SessionLocal()

print("""
🚀 FastAPI Boilerplate Interactive Shell
=======================================

✨ Pre-loaded with:
- Database session: `db`
- All models: `User`
- All CRUD functions: `get_user`, `create_user`, etc.
- SQLAlchemy functions: `select`, `func`, `desc`
- Modern SQLAlchemy 2.0 syntax

Quick Examples:
==============

1. Basic Queries (Modern SQLAlchemy 2.0):
   user = db.scalar(select(User))
   users = db.scalars(select(User)).all()
   
2. Filtered Queries:
   active_users = db.scalars(select(User).where(User.is_active == True)).all()
   user_by_email = db.scalar(select(User).where(User.email == "test@example.com"))
   
3. CRUD Operations:
   new_user = create_user(db, UserCreate(name="John", email="john@example.com"))
   user = get_user(db, user_id=1)
   
4. Count Queries:
   user_count = db.scalar(select(func.count(User.id)))
   
5. Ordering:
   users = db.scalars(select(User).order_by(User.created_at.desc())).all()

Type 'help()' for this message again.
Type 'exit()' or 'quit()' to exit.
""")

# Start interactive shell
try:
    import code
    code.interact(local=locals())
finally:
    db.close()
