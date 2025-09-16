# {project_title}

A FastAPI project with SQLAlchemy 2.0, PostgreSQL, and Alembic migrations.

## 🚀 Quick Start

### Full Docker Setup (Everything in Docker)

```bash
# Start everything with Docker
docker-compose up

# Visit http://localhost:8000/docs for API documentation
# Database will be automatically set up!
```

## 🐚 Interactive Shell

Start an interactive Python shell with database access:

```bash
# Standard Python shell
docker-compose exec app python management/shell.py

# Enhanced shell with bpython (recommended)
docker-compose exec app python management/bpython_shell.py

# Enhanced shell with ipython
docker-compose exec app python management/ipython_shell.py
```

This gives you access to:
- Database session (`db`)
- All your models
- CRUD operations
- FastAPI app instance

**Shell Features:**
- **Standard**: Basic Python shell
- **bpython**: Syntax highlighting, autocompletion, auto-indentation
- **ipython**: Advanced features, magic commands, rich display

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (clean database)
docker-compose down -v
```

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
```

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

### 4. Create API Endpoints
Create `app/api/v1/endpoints/products.py`:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.crud.product import get_product, get_products, create_product, update_product, delete_product

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = get_products(db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse)
def create_product_endpoint(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db=db, product=product)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product_endpoint(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = update_product(db, product_id=product_id, product_update=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/{product_id}")
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    success = delete_product(db, product_id=product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {{"message": "Product deleted successfully"}}
```

### 5. Add to API Router
Update `app/api/v1/api.py`:

```python
from fastapi import APIRouter
from app.api.v1.endpoints import users, products

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
```

### 6. Run Migrations
```bash
# Create migration
alembic revision --autogenerate -m "Add products table"

# Apply migration
alembic upgrade head
```

## 🛠️ Development Tools

### Interactive Shell
```bash
# Start interactive shell with database access
docker-compose exec app python management/shell.py
```

### Database Migrations
```bash
# Create new migration
docker-compose exec app alembic revision --autogenerate -m "Description of changes"

# Apply migrations
docker-compose exec app alembic upgrade head

# Rollback migration
docker-compose exec app alembic downgrade -1
```

## 🐳 Docker Commands

### Development
```bash
# Start everything
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Database Management
```bash
# Access database directly
docker-compose exec db psql -U fastapi_user -d fastapi_db

# Backup database
docker-compose exec db pg_dump -U fastapi_user fastapi_db > backup.sql

# Restore database
docker-compose exec -T db psql -U fastapi_user -d fastapi_db < backup.sql
```

## 📚 Documentation

- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🔧 Configuration

The application uses environment variables from `.env` file:

```env
DATABASE_URL=postgresql://fastapi_user:fastapi_password@db:5432/fastapi_db
DEBUG=True
PROJECT_NAME={project_title}
VERSION=1.0.0
```

## 📁 Project Structure

```
{project_name}/
├── app/
│   ├── api/v1/endpoints/     # API endpoints
│   ├── core/                 # Core configuration
│   ├── crud/                 # Database operations
│   ├── db/                   # Database configuration
│   ├── models/               # SQLAlchemy models
│   ├── schemas/              # Pydantic schemas
│   └── main.py               # FastAPI application
├── alembic/                  # Database migrations
├── management/               # Development tools
├── docker-compose.yml        # Docker configuration
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🆘 Troubleshooting

### Container Issues
- Check if containers are running: `docker-compose ps`
- View logs: `docker-compose logs -f`
- Restart services: `docker-compose restart`

### Database Issues
- Check database connection: `docker-compose exec app python -c "from app.db.session import engine; print(engine.url)"`
- Reset database: `docker-compose down -v && docker-compose up`

### Port Conflicts
- Change ports in `docker-compose.yml`
- Check if ports are in use: `lsof -i :8000` or `netstat -tulpn | grep :8000`

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the FastAPI documentation
3. Check SQLAlchemy 2.0 documentation
4. Review Alembic migration documentation

---

**Happy coding! 🚀**
