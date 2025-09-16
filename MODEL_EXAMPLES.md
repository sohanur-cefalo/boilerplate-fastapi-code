# Model Examples for FastAPI Boilerplate

This document provides comprehensive examples of how to create different types of models using the modern SQLAlchemy 2.0 syntax.

## 📋 Table of Contents

1. [Basic Model](#basic-model)
2. [Model with Relationships](#model-with-relationships)
3. [Model with Enums](#model-with-enums)
4. [Model with JSON Fields](#model-with-json-fields)
5. [Model with Timestamps](#model-with-timestamps)
6. [Model with Soft Delete](#model-with-soft-delete)
7. [Complete Example: Blog System](#complete-example-blog-system)

## 1. Basic Model

```python
# app/models/category.py
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class Category(Base):
    """Category model - Basic example"""
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name})"
```

## 2. Model with Relationships

```python
# app/models/post.py
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class Post(Base):
    """Post model with relationships"""
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    published: Mapped[bool] = mapped_column(default=False)
    view_count: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign Keys
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"))
    
    # Relationships
    author: Mapped["User"] = relationship("User", back_populates="posts")
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="post")

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title}, author_id={self.author_id})"
```

## 3. Model with Enums

```python
# app/models/order.py
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Float, DateTime, Enum, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
import enum

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class PaymentMethod(str, enum.Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"

class Order(Base):
    """Order model with enums"""
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_number: Mapped[str] = mapped_column(String(50), unique=True)
    total_amount: Mapped[float] = mapped_column()
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING)
    payment_method: Mapped[PaymentMethod] = mapped_column(Enum(PaymentMethod))
    notes: Mapped[Optional[str]] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"Order(id={self.id}, order_number={self.order_number}, status={self.status})"
```

## 4. Model with JSON Fields

```python
# app/models/product.py
from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlalchemy import String, Text, Integer, Float, JSON, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class Product(Base):
    """Product model with JSON fields"""
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text)
    price: Mapped[float] = mapped_column()
    stock_quantity: Mapped[int] = mapped_column(default=0)
    
    # JSON fields for flexible data
    attributes: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    tags: Mapped[Optional[List[str]]] = mapped_column(JSON)
    metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"Product(id={self.id}, name={self.name}, price={self.price})"
```

## 5. Model with Timestamps

```python
# app/models/audit_log.py
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class AuditLog(Base):
    """Audit log model with comprehensive timestamps"""
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    table_name: Mapped[str] = mapped_column(String(100))
    record_id: Mapped[int] = mapped_column()
    action: Mapped[str] = mapped_column(String(50))  # INSERT, UPDATE, DELETE
    old_values: Mapped[Optional[str]] = mapped_column(Text)  # JSON string
    new_values: Mapped[Optional[str]] = mapped_column(Text)  # JSON string
    user_id: Mapped[Optional[int]] = mapped_column()
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"AuditLog(id={self.id}, table={self.table_name}, action={self.action})"
```

## 6. Model with Soft Delete

```python
# app/models/comment.py
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class Comment(Base):
    """Comment model with soft delete"""
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text)
    is_approved: Mapped[bool] = mapped_column(default=False)
    
    # Foreign Keys
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    # Soft delete fields
    is_deleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
    author: Mapped["User"] = relationship("User", back_populates="comments")

    def soft_delete(self):
        """Soft delete the comment"""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()

    def __repr__(self):
        return f"Comment(id={self.id}, content={self.content[:50]}...)"
```

## 7. Complete Example: Blog System

Here's a complete example of a blog system with multiple related models:

### User Model (Extended)
```python
# app/models/user.py
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class User(Base):
    """Extended User model for blog system"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(100))
    bio: Mapped[Optional[str]] = mapped_column(String(500))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="author")
    likes: Mapped[List["Like"]] = relationship("Like", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"
```

### Like Model
```python
# app/models/like.py
from datetime import datetime
from sqlalchemy import Integer, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class Like(Base):
    """Like model for posts"""
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="likes")
    post: Mapped["Post"] = relationship("Post", back_populates="likes")
    
    # Ensure one like per user per post
    __table_args__ = (UniqueConstraint('user_id', 'post_id', name='unique_user_post_like'),)

    def __repr__(self):
        return f"Like(id={self.id}, user_id={self.user_id}, post_id={self.post_id})"
```

### Updated Post Model
```python
# app/models/post.py (Updated with likes)
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class Post(Base):
    """Post model with all relationships"""
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    slug: Mapped[str] = mapped_column(String(250), unique=True, index=True)
    content: Mapped[str] = mapped_column(Text)
    excerpt: Mapped[Optional[str]] = mapped_column(String(500))
    featured_image: Mapped[Optional[str]] = mapped_column(String(500))
    published: Mapped[bool] = mapped_column(default=False)
    view_count: Mapped[int] = mapped_column(default=0)
    like_count: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Foreign Keys
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"))
    
    # Relationships
    author: Mapped["User"] = relationship("User", back_populates="posts")
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="post")
    likes: Mapped[List["Like"]] = relationship("Like", back_populates="post")

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title}, author_id={self.author_id})"
```

## 🔧 Usage Examples

### Creating Records
```python
# In your shell or CRUD functions
from app.models import User, Post, Category
from app.schemas.user import UserCreate
from app.schemas.post import PostCreate

# Create user
user_data = UserCreate(
    username="john_doe",
    email="john@example.com",
    full_name="John Doe"
)
user = create_user(db, user_data)

# Create category
category = Category(name="Technology", description="Tech-related posts")
db.add(category)
db.commit()

# Create post
post_data = PostCreate(
    title="My First Post",
    content="This is the content of my first post...",
    author_id=user.id,
    category_id=category.id
)
post = create_post(db, post_data)
```

### Querying with Relationships
```python
# Get posts with author and category
posts = db.scalars(
    select(Post)
    .options(selectinload(Post.author), selectinload(Post.category))
    .where(Post.published == True)
).all()

# Get user with all their posts
user_with_posts = db.scalar(
    select(User)
    .options(selectinload(User.posts))
    .where(User.id == 1)
)

# Get posts with like count
posts_with_likes = db.scalars(
    select(Post)
    .options(selectinload(Post.likes))
    .order_by(Post.like_count.desc())
).all()
```

### Complex Queries
```python
# Get most popular posts
popular_posts = db.scalars(
    select(Post)
    .where(Post.published == True)
    .order_by(Post.like_count.desc(), Post.view_count.desc())
    .limit(10)
).all()

# Get users who have written posts
active_authors = db.scalars(
    select(User)
    .join(Post)
    .where(Post.published == True)
    .distinct()
).all()

# Get posts by category
tech_posts = db.scalars(
    select(Post)
    .join(Category)
    .where(Category.name == "Technology")
    .where(Post.published == True)
).all()
```

## 📝 Migration Commands

After creating your models, don't forget to create and run migrations:

```bash
# Create migration
alembic revision --autogenerate -m "Add blog models"

# Apply migration
alembic upgrade head
```

## 🎯 Best Practices

1. **Always use type hints** with `Mapped[type]`
2. **Use `mapped_column()`** instead of `Column()`
3. **Add `__repr__` methods** for better debugging
4. **Use proper foreign key constraints**
5. **Add indexes** for frequently queried fields
6. **Use enums** for status fields
7. **Add timestamps** for audit trails
8. **Use soft deletes** when data needs to be preserved
9. **Add unique constraints** where appropriate
10. **Use JSON fields** for flexible data storage

This boilerplate provides a solid foundation for building any FastAPI application with modern SQLAlchemy 2.0!
