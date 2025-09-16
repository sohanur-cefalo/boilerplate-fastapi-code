#!/usr/bin/env python3
"""
FastAPI Boilerplate Project Starter
===================================

This script helps you quickly set up a new FastAPI project from this boilerplate.

Usage:
    python start_project.py my_new_project

Features:
- Copies boilerplate code to new project directory
- Updates project name in configuration
- Sets up initial git repository
- Provides next steps instructions
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def main():
    # Interactive project name input
    if len(sys.argv) == 2:
        # If project name provided as argument, use it
        project_name = sys.argv[1]
    else:
        # Interactive mode - ask for project name
        print("🚀 FastAPI Project Generator")
        print("=" * 40)
        print("Create a new FastAPI project with SQLAlchemy 2.0")
        print()
        
        # Get project name with default
        default_name = "my-fastapi-project"
        user_input = input(f"📝 Project name [{default_name}]: ").strip()
        
        # Use default if empty
        if not user_input:
            project_name = default_name
            print(f"✅ Using default name: {project_name}")
        else:
            project_name = user_input
            print(f"✅ Using name: {project_name}")
        
        # Validate project name
        if not project_name.replace('-', '').replace('_', '').isalnum():
            print("❌ Project name can only contain letters, numbers, hyphens, and underscores")
            sys.exit(1)
        
        print()
    current_dir = Path(__file__).parent
    project_dir = current_dir.parent / project_name
    
    print(f"🚀 Creating new FastAPI project: {project_name}")
    print(f"📁 Project directory: {project_dir}")
    
    # Check if directory already exists
    if project_dir.exists():
        print(f"❌ Directory {project_dir} already exists!")
        print("Please choose a different project name or remove the existing directory.")
        sys.exit(1)
    
    try:
        # Copy boilerplate code
        print("📋 Copying boilerplate code...")
        shutil.copytree(current_dir, project_dir, ignore=shutil.ignore_patterns(
            '__pycache__', '*.pyc', '.git', '.DS_Store', 'alembic/versions/*.py'
        ))
        
        # Update project name in config
        print("⚙️  Updating project configuration...")
        config_file = project_dir / "app" / "core" / "config.py"
        if config_file.exists():
            content = config_file.read_text()
            content = content.replace(
                'project_name: str = "Your FastAPI Project"',
                f'project_name: str = "{project_name.replace("_", " ").title()}"'
            )
            config_file.write_text(content)
        
        # Create minimalistic project README
        print("📝 Creating project README...")
        readme_file = project_dir / "README.md"
        project_title = project_name.replace('_', ' ').title()
        
        minimal_readme = f"""# {project_title}

A FastAPI project with SQLAlchemy 2.0, PostgreSQL, and Alembic migrations.

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Copy environment file
cp env.example .env

# Edit .env with your database settings
# DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name
# DEBUG=True
# PROJECT_NAME={project_title}
# VERSION=1.0.0
```
> 📋 **Copy these commands** - Click the code block above and press `Ctrl+C` (or `Cmd+C` on Mac)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
> 📋 **Copy this command** - Click the code block above and press `Ctrl+C` (or `Cmd+C` on Mac)

### 3. Setup Database
```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```
> 📋 **Copy these commands** - Click the code block above and press `Ctrl+C` (or `Cmd+C` on Mac)

### 4. Start Development Server
```bash
uvicorn app.main:app --reload
```
> 📋 **Copy this command** - Click the code block above and press `Ctrl+C` (or `Cmd+C` on Mac)

Visit http://localhost:8000/docs for API documentation.

## 📝 Adding New Models

### 1. Create Model
Create a new file in `app/models/` (e.g., `app/models/product.py`):

```python
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    price: Mapped[float] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"Product(id={{self.id}}, name={{self.name}}, price={{self.price}})"
```
> 📋 **Copy this code** - Click the code block above and press `Ctrl+C` (or `Cmd+C` on Mac)

### 2. Create Schema
Create `app/schemas/product.py`:

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
```
> 📋 **Copy this code** - Click the code block above and press `Ctrl+C` (or `Cmd+C` on Mac)

### 3. Create CRUD Operations
Create `app/crud/product.py`:

```python
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.scalar(select(Product).where(Product.id == product_id))

def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    return db.scalars(select(Product).offset(skip).limit(limit)).all()

def create_product(db: Session, product: ProductCreate) -> Product:
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: ProductUpdate) -> Optional[Product]:
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    
    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int) -> bool:
    db_product = get_product(db, product_id)
    if not db_product:
        return False
    
    db.delete(db_product)
    db.commit()
    return True
```
> 📋 **Copy this code** - Click the code block above and press `Ctrl+C` (or `Cmd+C` on Mac)

### 4. Create API Endpoints
Create `app/api/v1/endpoints/products.py`:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.crud import product as product_crud

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return product_crud.get_products(db, skip=skip, limit=limit)

@router.get("/{{product_id}}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return product_crud.create_product(db, product)

@router.put("/{{product_id}}", response_model=ProductResponse)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    product = product_crud.update_product(db, product_id, product_update)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{{product_id}}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    if not product_crud.delete_product(db, product_id):
        raise HTTPException(status_code=404, detail="Product not found")
```
> 📋 **Copy this code** - Click the code block above and press `Ctrl+C` (or `Cmd+C` on Mac)

### 5. Update Imports
Update `app/models/__init__.py`:
```python
from .user import User
from .product import Product

__all__ = ["User", "Product"]
```
> 📋 **Copy this code** - Click the code block above and press `Ctrl+C` (or `Cmd+C` on Mac)

Update `app/schemas/__init__.py`:
```python
from .user import UserBase, UserCreate, UserUpdate, UserResponse
from .product import ProductBase, ProductCreate, ProductUpdate, ProductResponse

__all__ = ["UserBase", "UserCreate", "UserUpdate", "UserResponse", 
           "ProductBase", "ProductCreate", "ProductUpdate", "ProductResponse"]
```
> 📋 **Copy this code** - Click the code block above and press `Ctrl+C` (or `Cmd+C` on Mac)

Update `app/crud/__init__.py`:
```python
from .user import get_user, get_user_by_email, get_users, create_user, update_user, delete_user
from .product import get_product, get_products, create_product, update_product, delete_product

__all__ = ["get_user", "get_user_by_email", "get_users", "create_user", "update_user", "delete_user",
           "get_product", "get_products", "create_product", "update_product", "delete_product"]
```
> 📋 **Copy this code** - Click the code block above and press `Ctrl+C` (or `Cmd+C` on Mac)

Update `app/api/v1/api.py`:
```python
from fastapi import APIRouter
from app.api.v1.endpoints import users, products

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
```
> 📋 **Copy this code** - Click the code block above and press `Ctrl+C` (or `Cmd+C` on Mac)

### 6. Create Migration
```bash
# Create migration for new model
alembic revision --autogenerate -m "Add Product model"

# Apply migration
alembic upgrade head
```
> 📋 **Copy these commands** - Click the code block above and press `Ctrl+C` (or `Cmd+C` on Mac)

## 🐚 Interactive Shell

Use the interactive shell for database exploration:

```bash
# bpython (recommended)
python management/shell_launcher.py bpython

# IPython
python management/shell_launcher.py ipython

# Standard Python
python management/shell_launcher.py standard
```
> 📋 **Copy these commands** - Click the code block above and press `Ctrl+C` (or `Cmd+C` on Mac)

## 🗄️ Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Show migration history
alembic history
```
> 📋 **Copy these commands** - Click the code block above and press `Ctrl+C` (or `Cmd+C` on Mac)

## 🐳 Docker Development

Run the application with Docker (includes PostgreSQL database):

```bash
# Start all services (app + database)
docker-compose up

# Run in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f app
```
> 📋 **Copy these commands** - Click the code block above and press `Ctrl+C` (or `Cmd+C` on Mac)

**Docker automatically:**
- Sets up PostgreSQL database
- Configures environment variables
- Runs database migrations
- Starts the FastAPI application

## 🚀 Production Deployment

```bash
# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000

# With Docker
docker-compose up -d
```
> 📋 **Copy these commands** - Click the code block above and press `Ctrl+C` (or `Cmd+C` on Mac)

---

**Happy coding! 🚀**
"""
        
        readme_file.write_text(minimal_readme)
        
        # Initialize git repository
        print("🔧 Initializing git repository...")
        try:
            subprocess.run(["git", "init"], cwd=project_dir, check=True)
            subprocess.run(["git", "branch", "-m", "main"], cwd=project_dir, check=True)
            subprocess.run(["git", "add", "."], cwd=project_dir, check=True)
            subprocess.run(["git", "commit", "-m", f"Initial commit for {project_title}"], cwd=project_dir, check=True)
            print("✅ Git repository initialized with 'main' branch")
        except subprocess.CalledProcessError:
            print("⚠️  Git initialization failed (git might not be installed)")
        
        print("\n" + "="*60)
        print("🎉 Project created successfully!")
        print("="*60)
        print(f"\n📁 Project location: {project_dir}")
        print(f"\n📝 Project README: {project_dir}/README.md")
        
        # Ask if user wants to start development
        print("\n" + "="*40)
        print("🚀 Next Steps")
        print("="*40)
        
        start_dev = input("\n❓ Start development now? (y/N): ").strip().lower()
        
        if start_dev in ['y', 'yes']:
            print("\n📋 Choose your development method:")
            print("1. Docker (recommended - includes database)")
            print("2. Local development (requires PostgreSQL)")
            
            choice = input("\nEnter choice (1/2) [1]: ").strip()
            
            if choice == "2":
                print("\n🔧 Local development setup:")
                print(f"1. cd {project_dir}")
                print("2. cp env.example .env")
                print("3. Edit .env with your database settings")
                print("4. pip install -r requirements.txt")
                print("5. alembic revision --autogenerate -m 'Initial migration'")
                print("6. alembic upgrade head")
                print("7. uvicorn app.main:app --reload")
                print("\n🌐 Visit http://localhost:8000/docs for API documentation")
            else:
                print("\n🐳 Docker development setup:")
                print(f"1. cd {project_dir}")
                print("2. docker-compose up")
                print("\n🌐 Visit http://localhost:8000/docs for API documentation")
                print("📊 Database will be automatically set up!")
        else:
            print("\n📋 Quick start commands:")
            print(f"1. cd {project_dir}")
            print("2. Read README.md for detailed instructions")
            print("3. Choose Docker or local development")
        
        print("\n📚 Read the project README.md for complete instructions")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error creating project: {e}")
        if project_dir.exists():
            shutil.rmtree(project_dir)
        sys.exit(1)

if __name__ == "__main__":
    main()
