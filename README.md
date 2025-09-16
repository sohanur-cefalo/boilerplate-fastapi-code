# FastAPI Boilerplate with SQLAlchemy 2.0

A production-ready FastAPI boilerplate with modern SQLAlchemy 2.0, PostgreSQL, and Alembic migrations. Perfect for starting new projects quickly!

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

```
boilerplate-fastapi-code/
├── app/
│   ├── core/
│   │   └── config.py          # Application settings
│   ├── db/
│   │   └── session.py         # Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py            # Example User model
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py            # Pydantic schemas
│   ├── crud/
│   │   ├── __init__.py
│   │   └── user.py            # Database operations
│   ├── api/
│   │   └── v1/
│   │       ├── api.py         # API router
│   │       └── endpoints/
│   │           └── users.py   # API endpoints
│   └── main.py                # FastAPI app
├── management/
│   ├── shell.py               # Standard Python shell
│   ├── bpython_shell.py       # bpython shell (recommended)
│   ├── ipython_shell.py       # IPython shell
│   └── shell_launcher.py      # Shell launcher
├── alembic/                   # Database migrations
├── requirements.txt
├── env.example
└── README.md
```

## 🛠️ Quick Start

### 1. Clone and Setup

```bash
# Clone this boilerplate
git clone <your-repo-url> my-new-project
cd my-new-project

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Database

```bash
# Copy environment file
cp env.example .env

# Edit .env with your database settings
DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name
DEBUG=True
PROJECT_NAME=My New Project
VERSION=1.0.0
```

### 3. Run Migrations

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 4. Start the Application

```bash
# Development server
uvicorn app.main:app --reload

# Visit http://localhost:8000/docs for API documentation
```

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

---

**Happy coding! 🚀**
