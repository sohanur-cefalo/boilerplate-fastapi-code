#!/usr/bin/env python3
"""
FastAPI Boilerplate bpython Shell
=================================

Enhanced interactive shell with bpython for superior autocompletion.

Usage:
    python management/bpython_shell.py

Features:
- Excellent tab completion (better than IPython!)
- Syntax highlighting
- Auto-suggestions as you type
- Command history (up/down arrows)
- Inline documentation
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from app.db.session import SessionLocal, engine, Base

# Import models and CRUD operations if they exist
try:
    from app.models import User
    from app.crud import (
        get_user, get_user_by_email, get_users,
        create_user, update_user, delete_user
    )
    from app.schemas.user import UserCreate, UserUpdate
    HAS_USER = True
except ImportError:
    HAS_USER = False

def run_bpython_shell():
    print("🚀 FastAPI Boilerplate bpython Shell")
    print("====================================\n")
    print("✨ Features:")
    print("- Excellent tab completion (better than IPython!)")
    print("- Syntax highlighting")
    print("- Auto-suggestions as you type")
    print("- Command history (up/down arrows)")
    print("- Inline documentation\n")

    shell_namespace = {
        'db': SessionLocal(),
        'select': select,
        'func': func,
        'desc': desc,
        'selectinload': selectinload,
        'Base': Base,
        'engine': engine,
    }
    
    # Add user-related items if User table exists
    if HAS_USER:
        shell_namespace.update({
            'User': User,
            'get_user': get_user,
            'get_user_by_email': get_user_by_email,
            'get_users': get_users,
            'create_user': create_user,
            'update_user': update_user,
            'delete_user': delete_user,
            'UserCreate': UserCreate,
            'UserUpdate': UserUpdate,
        })
        print("👤 User table available")
    else:
        print("📝 Minimal project - no User table")
        print("💡 Add your own models to app/models/ and import them here")

    try:
        import bpython
        bpython.embed(locals_=shell_namespace)
    except ImportError:
        print("❌ bpython not installed. Installing...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "bpython"])
        print("✅ bpython installed. Please run the script again.")
        return

if __name__ == "__main__":
    run_bpython_shell()
