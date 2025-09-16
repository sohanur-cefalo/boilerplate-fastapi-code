# FastAPI Boilerplate with SQLAlchemy 2.0

A production-ready FastAPI boilerplate with modern SQLAlchemy 2.0, PostgreSQL, and Alembic migrations. Perfect for starting new projects quickly!

## 🚀 Quick Start (One Command)

```bash
git clone https://github.com/sohanur-cefalo/boilerplate-fastapi-code.git my-new-project && cd my-new-project
```

Then follow the setup instructions below!

## 🎯 How to Use This Repository

This boilerplate provides **two ways** to start your FastAPI project:

### Option 1: Quick Start with User Table (Recommended for most projects)
- Includes a complete User model with CRUD operations
- Ready-to-use authentication foundation
- Perfect for user-based applications
- **Start here if you need user management**

### Option 2: Minimal Start (Clean slate)
- No pre-built models or endpoints
- Just the core FastAPI + SQLAlchemy setup
- Perfect for API-only services or custom architectures
- **Start here if you want complete control**

Both options include the same modern tech stack and project structure!

## 🤔 Which Option Should I Choose?

### Choose **Option 1 (With User Table)** if:
- ✅ You're building a user-based application
- ✅ You need authentication or user management
- ✅ You want to get started quickly with a working example
- ✅ You're learning FastAPI and want to see a complete model implementation
- ✅ You plan to add user features later

### Choose **Option 2 (Minimal Setup)** if:
- ✅ You're building a microservice or API-only service
- ✅ You have specific architectural requirements
- ✅ You want complete control over your data models
- ✅ You're building a non-user-based application (e.g., data processing, IoT)
- ✅ You prefer to build everything from scratch

**Not sure?** Start with **Option 1** - you can always remove the User table later using the cleanup instructions!

## 🚀 Quick Project Creation

### Method 1: Clone and Use Script (Recommended)
```bash
# Clone this boilerplate
git clone https://github.com/sohanur-cefalo/boilerplate-fastapi-code.git my-awesome-api
cd my-awesome-api

# Use the included script to create a fresh project
python start_project.py my_fresh_project

# This will:
# - Copy all boilerplate code to 'my_fresh_project' directory
# - Update project name in configuration
# - Initialize git repository
# - Provide next steps instructions
```

### Method 2: Direct Clone
```bash
# Clone directly to your project name
git clone https://github.com/sohanur-cefalo/boilerplate-fastapi-code.git my-awesome-api
cd my-awesome-api

# Follow the setup instructions below
```

Then follow the setup instructions in your new project directory!

## 🚀 Features

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy 2.0** - Latest ORM with `Mapped` annotations and type safety
- **PostgreSQL** - Production-ready database
- **Alembic** - Database migrations
- **Pydantic** - Data validation and settings
- **Interactive Shells** - bpython, IPython, and standard Python shells
- **Type Safety** - Full type hints throughout
- **Modular Structure** - Clean, scalable architecture

## 📁 Project Structure

### Option 1: With User Table (Default)
```
boilerplate-fastapi-code/
├── app/
│   ├── core/
│   │   └── config.py          # Application settings
│   ├── db/
│   │   └── session.py         # Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py            # ✅ User model (ready to use)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py            # ✅ User Pydantic schemas
│   ├── crud/
│   │   ├── __init__.py
│   │   └── user.py            # ✅ User CRUD operations
│   ├── api/
│   │   └── v1/
│   │       ├── api.py         # API router (includes users)
│   │       └── endpoints/
│   │           └── users.py   # ✅ User API endpoints
│   └── main.py                # FastAPI app
├── management/                # Interactive shells
├── alembic/                   # Database migrations
├── requirements.txt
├── env.example
└── README.md
```

### Option 2: Minimal Setup (After cleanup)
```
boilerplate-fastapi-code/
├── app/
│   ├── core/
│   │   └── config.py          # Application settings
│   ├── db/
│   │   └── session.py         # Database connection
│   ├── models/
│   │   └── __init__.py        # Empty - ready for your models
│   ├── schemas/
│   │   └── __init__.py        # Empty - ready for your schemas
│   ├── crud/
│   │   └── __init__.py        # Empty - ready for your CRUD
│   ├── api/
│   │   └── v1/
│   │       ├── api.py         # API router (no endpoints)
│   │       └── endpoints/     # Empty - ready for your endpoints
│   └── main.py                # FastAPI app
├── management/                # Interactive shells
├── alembic/                   # Database migrations
├── requirements.txt
├── env.example
└── README.md
```

### Key Differences:
- **Option 1**: Includes complete User model with CRUD and API endpoints
- **Option 2**: Clean slate with empty model/schema/crud/endpoint directories
- **Both**: Same core structure, database setup, and management tools

## 🚀 Quick Start

Choose your preferred setup option:

### Option 1: With User Table (Ready-to-go)

Perfect if you need user management, authentication, or user-based features.

#### 1. Clone and Setup
```bash
# Clone this boilerplate
git clone https://github.com/sohanur-cefalo/boilerplate-fastapi-code.git my-new-project
cd my-new-project

# Install dependencies
pip install -r requirements.txt
```

#### 2. Configure Database
```bash
# Copy environment file
cp env.example .env

# Edit .env with your database settings
DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name
DEBUG=True
PROJECT_NAME=My New Project
VERSION=1.0.0
```

#### 3. Run Migrations
```bash
# Create initial migration (includes User table)
alembic revision --autogenerate -m "Initial migration with User table"

# Apply migrations
alembic upgrade head
```

#### 4. Start the Application
```bash
# Development server
uvicorn app.main:app --reload

# Visit http://localhost:8000/docs for API documentation
# Test the User API at http://localhost:8000/api/v1/users/
```

**You're ready!** Your API includes:
- Complete User CRUD operations
- User authentication foundation
- Interactive API documentation
- Database migrations

---

### Option 2: Minimal Setup (Clean slate)

Perfect if you want to build your own models and don't need the User table.

#### 1. Clone and Setup
```bash
# Clone this boilerplate
git clone https://github.com/sohanur-cefalo/boilerplate-fastapi-code.git my-new-project
cd my-new-project

# Install dependencies
pip install -r requirements.txt
```

#### 2. Configure Database
```bash
# Copy environment file
cp env.example .env

# Edit .env with your database settings
DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name
DEBUG=True
PROJECT_NAME=My New Project
VERSION=1.0.0
```

#### 3. Remove User Table (Optional)
If you want a completely clean start, remove the user-related files:

```bash
# Remove user-related files
rm app/models/user.py
rm app/schemas/user.py
rm app/crud/user.py
rm app/api/v1/endpoints/users.py

# Update imports in __init__.py files
# (See detailed instructions below)
```

#### 4. Run Migrations
```bash
# Create initial migration (no User table)
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

#### 5. Start the Application
```bash
# Development server
uvicorn app.main:app --reload

# Visit http://localhost:8000/docs for API documentation
```

**You're ready!** Your API includes:
- Clean FastAPI + SQLAlchemy setup
- No pre-built models
- Ready for your custom models
- Interactive API documentation

## 🧹 Detailed Cleanup Instructions (Option 2)

If you chose the minimal setup and want to remove the User table completely, follow these detailed steps:

### Step 1: Remove User Files
```bash
# Remove user-related files
rm app/models/user.py
rm app/schemas/user.py
rm app/crud/user.py
rm app/api/v1/endpoints/users.py
```

### Step 2: Update Import Files

**Update `app/models/__init__.py`:**
```python
# Remove User import
# from .user import User

# Update __all__ list
__all__ = []
```

**Update `app/schemas/__init__.py`:**
```python
# Remove User schema imports
# from .user import UserBase, UserCreate, UserUpdate, UserResponse

# Update __all__ list
__all__ = []
```

**Update `app/crud/__init__.py`:**
```python
# Remove User CRUD imports
# from .user import get_user, get_user_by_email, get_users, create_user, update_user, delete_user

# Update __all__ list
__all__ = []
```

**Update `app/api/v1/api.py`:**
```python
from fastapi import APIRouter
# Remove users import
# from app.api.v1.endpoints import users

api_router = APIRouter()

# Remove users router
# api_router.include_router(users.router, prefix="/users", tags=["users"])
```

### Step 3: Clean Database (if already migrated)
```bash
# Drop all tables and recreate
alembic downgrade base
alembic upgrade head
```

### Step 4: Verify Clean Setup
```bash
# Start the application
uvicorn app.main:app --reload

# Visit http://localhost:8000/docs
# You should only see the root and health endpoints
```

## 👥 What's Included with User Table (Option 1)

If you choose to keep the User table, you get a complete user management system:

### User Model Features
- **ID**: Primary key with auto-increment
- **Name**: User's full name (required)
- **Email**: Unique email address with validation
- **Active Status**: Boolean flag for user activation
- **Timestamps**: Created and updated timestamps
- **Type Safety**: Full SQLAlchemy 2.0 type annotations

### API Endpoints
- `GET /api/v1/users/` - List all users (with pagination)
- `GET /api/v1/users/{user_id}` - Get specific user
- `POST /api/v1/users/` - Create new user
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

### Pydantic Schemas
- **UserBase**: Common fields for all user operations
- **UserCreate**: Schema for creating new users
- **UserUpdate**: Schema for updating users (all fields optional)
- **UserResponse**: Schema for API responses (includes all fields)

### CRUD Operations
- Complete database operations for all user actions
- Email uniqueness validation
- Proper error handling
- Type-safe database queries

### Ready for Extension
The User model is designed to be easily extended with:
- Authentication (JWT tokens, OAuth)
- User roles and permissions
- User profiles and preferences
- Password hashing
- Email verification

## 🎯 What's Included with Minimal Setup (Option 2)

If you choose the minimal setup, you get a clean foundation:

### Core Infrastructure
- **FastAPI Application**: Ready-to-run FastAPI app
- **SQLAlchemy 2.0**: Latest ORM with type safety
- **Database Connection**: PostgreSQL with connection pooling
- **Alembic Migrations**: Database migration system
- **Environment Configuration**: Pydantic-based settings
- **Interactive Shells**: bpython, IPython, and standard Python

### Project Structure
- **Modular Architecture**: Clean separation of concerns
- **Empty Directories**: Ready for your models, schemas, CRUD, and endpoints
- **Type Hints**: Full type safety throughout
- **Modern Python**: Uses latest Python features and best practices

### Ready for Your Models
The minimal setup gives you:
- Clean database session management
- Migration system ready for your models
- API router ready for your endpoints
- Shell tools for database exploration
- No assumptions about your data model

### Perfect For
- **Microservices**: API-only services
- **Custom Architectures**: When you have specific design requirements
- **Learning**: Understanding FastAPI + SQLAlchemy from scratch
- **Clean Slate**: Starting with your own models and business logic

## 📝 Creating New Models

### 1. Create the Model

Create a new file in `app/models/` (e.g., `app/models/product.py`):

```python
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class Product(Base):
    """Product model example"""
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    price: Mapped[float] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"Product(id={self.id}, name={self.name}, price={self.price})"
```

### 2. Create Pydantic Schemas

Create `app/schemas/product.py`:

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ProductBase(BaseModel):
    """Base product schema"""
    name: str
    description: Optional[str] = None
    price: float
    is_active: bool = True

class ProductCreate(ProductBase):
    """Schema for creating a product"""
    pass

class ProductUpdate(BaseModel):
    """Schema for updating a product"""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None

class ProductResponse(ProductBase):
    """Schema for product response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
```

### 3. Create CRUD Operations

Create `app/crud/product.py`:

```python
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

def get_product(db: Session, product_id: int) -> Optional[Product]:
    """Get product by ID"""
    return db.scalar(select(Product).where(Product.id == product_id))

def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    """Get all products with pagination"""
    return db.scalars(select(Product).offset(skip).limit(limit)).all()

def create_product(db: Session, product: ProductCreate) -> Product:
    """Create new product"""
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: ProductUpdate) -> Optional[Product]:
    """Update product"""
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
    """Delete product"""
    db_product = get_product(db, product_id)
    if not db_product:
        return False
    
    db.delete(db_product)
    db.commit()
    return True
```

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
    """Get all products with pagination"""
    return product_crud.get_products(db, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get product by ID"""
    product = product_crud.get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create new product"""
    return product_crud.create_product(db, product)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    """Update product"""
    product = product_crud.update_product(db, product_id, product_update)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete product"""
    if not product_crud.delete_product(db, product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
```

### 5. Update Imports and Router

Update `app/models/__init__.py`:
```python
from .user import User
from .product import Product

__all__ = ["User", "Product"]
```

Update `app/schemas/__init__.py`:
```python
from .user import UserBase, UserCreate, UserUpdate, UserResponse
from .product import ProductBase, ProductCreate, ProductUpdate, ProductResponse

__all__ = ["UserBase", "UserCreate", "UserUpdate", "UserResponse", 
           "ProductBase", "ProductCreate", "ProductUpdate", "ProductResponse"]
```

Update `app/crud/__init__.py`:
```python
from .user import get_user, get_user_by_email, get_users, create_user, update_user, delete_user
from .product import get_product, get_products, create_product, update_product, delete_product

__all__ = ["get_user", "get_user_by_email", "get_users", "create_user", "update_user", "delete_user",
           "get_product", "get_products", "create_product", "update_product", "delete_product"]
```

Update `app/api/v1/api.py`:
```python
from fastapi import APIRouter
from app.api.v1.endpoints import users, products

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
```

### 6. Create and Run Migration

```bash
# Create migration for new model
alembic revision --autogenerate -m "Add Product model"

# Apply migration
alembic upgrade head
```

## 🐚 Interactive Shells

The boilerplate includes three interactive shells for database exploration:

### bpython (Recommended)
```bash
python management/shell_launcher.py bpython
```
- Best autocompletion
- Syntax highlighting
- Auto-suggestions

### IPython
```bash
python management/shell_launcher.py ipython
```
- Good balance of features
- Magic commands
- Rich display

### Standard Python
```bash
python management/shell_launcher.py standard
```
- Basic Python shell
- No additional dependencies

### Shell Features

All shells come pre-loaded with:
- Database session: `db`
- All models: `User`, `Product`, etc.
- All CRUD functions: `get_user`, `create_user`, etc.
- SQLAlchemy functions: `select`, `func`, `desc`
- Modern SQLAlchemy 2.0 syntax

### Example Shell Usage

```python
# Get all users
users = db.scalars(select(User)).all()

# Get active users
active_users = db.scalars(select(User).where(User.is_active == True)).all()

# Create new user
new_user = create_user(db, UserCreate(name="John", email="john@example.com"))

# Get user by ID
user = get_user(db, user_id=1)

# Count users
user_count = db.scalar(select(func.count(User.id)))

# Order by creation date
users = db.scalars(select(User).order_by(User.created_at.desc())).all()
```

## 🗄️ Database Migrations

### Creating Migrations

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Create empty migration for custom changes
alembic revision -m "Custom migration"
```

### Applying Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific migration
alembic upgrade <revision_id>

# Rollback to previous migration
alembic downgrade -1

# Rollback to specific migration
alembic downgrade <revision_id>
```

### Migration History

```bash
# Show migration history
alembic history

# Show current migration
alembic current

# Show pending migrations
alembic show head
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name

# Application
DEBUG=True
PROJECT_NAME=Your FastAPI Project
VERSION=1.0.0
```

### Settings

All settings are managed in `app/core/config.py` using `pydantic-settings`:

```python
class Settings(BaseSettings):
    database_url: str = "postgresql://username:password@localhost:5432/your_database_name"
    debug: bool = True
    project_name: str = "Your FastAPI Project"
    version: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
```

## 🚀 API Endpoints

The boilerplate includes a complete User API:

- `GET /api/v1/users/` - List all users
- `GET /api/v1/users/{user_id}` - Get user by ID
- `POST /api/v1/users/` - Create new user
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

Visit `http://localhost:8000/docs` for interactive API documentation.

## 🧪 SQLAlchemy 2.0 Features

This boilerplate uses the latest SQLAlchemy 2.0 features:

### Type Annotations
```python
id: Mapped[int] = mapped_column(primary_key=True)
name: Mapped[str] = mapped_column(String(100))
email: Mapped[Optional[str]] = mapped_column(String(255))
```

### Modern Query Syntax
```python
# Get single record
user = db.scalar(select(User).where(User.id == 1))

# Get multiple records
users = db.scalars(select(User)).all()

# With relationships
user_with_posts = db.scalar(
    select(User).options(selectinload(User.posts))
)
```

### Relationships
```python
# One-to-many
posts: Mapped[List["Post"]] = relationship("Post", back_populates="user")

# Many-to-one
user: Mapped["User"] = relationship("User", back_populates="posts")
```

## 📚 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🎉 Ready to Start?

### For User-Based Applications:
1. Clone this repository: `git clone https://github.com/sohanur-cefalo/boilerplate-fastapi-code.git my-project`
2. Run `python start_project.py your_project_name`
3. Follow Option 1 setup instructions
4. Start building your user management features!

### For Custom Applications:
1. Clone this repository: `git clone https://github.com/sohanur-cefalo/boilerplate-fastapi-code.git my-project`
2. Run `python start_project.py your_project_name`
3. Follow Option 2 setup instructions
4. Start building your custom models!

### What You Get Either Way:
- ✅ Production-ready FastAPI + SQLAlchemy 2.0 setup
- ✅ PostgreSQL database with migrations
- ✅ Type-safe code throughout
- ✅ Interactive development shells
- ✅ Clean, modular architecture
- ✅ Comprehensive documentation
- ✅ Ready for deployment

---

**Happy coding! 🚀**
