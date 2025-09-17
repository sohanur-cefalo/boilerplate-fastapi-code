{% if cookiecutter.include_user_model == "yes" -%}
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
{% if cookiecutter.include_authentication == "jwt" -%}
from passlib.context import CryptContext
{% endif -%}
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

{% if cookiecutter.include_authentication == "jwt" -%}
# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)
{% endif -%}


def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.scalar(select(User).where(User.id == user_id))


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.scalar(select(User).where(User.email == email))


{% if cookiecutter.include_authentication == "jwt" -%}
def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get user by username"""
    return db.scalar(select(User).where(User.username == username))


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Authenticate user with username and password"""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
{% endif -%}


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get all users with pagination"""
    return db.scalars(select(User).offset(skip).limit(limit)).all()


def create_user(db: Session, user: UserCreate) -> User:
    """Create new user"""
    user_data = user.model_dump()
    {% if cookiecutter.include_authentication == "jwt" -%}
    # Hash the password
    if "password" in user_data:
        hashed_password = get_password_hash(user_data.pop("password"))
        user_data["hashed_password"] = hashed_password
    {% endif -%}
    
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Update user"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    {% if cookiecutter.include_authentication == "jwt" -%}
    # Hash the password if provided
    if "password" in update_data:
        hashed_password = get_password_hash(update_data.pop("password"))
        update_data["hashed_password"] = hashed_password
    {% endif -%}
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """Delete user"""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True
{% endif -%}