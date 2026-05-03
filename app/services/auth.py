# app/services/auth.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, UserRole
import os
import bcrypt as _bcrypt

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-change-in-production-2024")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours


def hash_password(password: str) -> str:
    """Hash a password using bcrypt directly."""
    salt = _bcrypt.gensalt(rounds=12)
    return _bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain password against a bcrypt hash."""
    try:
        return _bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user_from_token(token: str, db: Session) -> Optional[User]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            return None
        return db.query(User).filter(User.email == email, User.is_active == True).first()
    except JWTError:
        return None


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=302, headers={"Location": "/login"})
    user = get_current_user_from_token(token, db)
    if not user:
        raise HTTPException(status_code=302, headers={"Location": "/login"})
    return user


def get_optional_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    token = request.cookies.get("access_token")
    if not token:
        return None
    return get_current_user_from_token(token, db)


# Role-based permission helpers
def require_admin(user: User) -> bool:
    return user.role == UserRole.ADMIN


def require_manager_or_admin(user: User) -> bool:
    return user.role in [UserRole.ADMIN, UserRole.MANAGER]


def can_manage_user(user: User, target_user: User) -> bool:
    """Check if user can manage another user."""
    if user.role == UserRole.ADMIN:
        return True
    if user.role == UserRole.MANAGER:
        # Managers can only manage regular users, not other managers or admins
        return target_user.role == UserRole.USER
    return False


def can_view_all_data(user: User) -> bool:
    """Check if user can view all users' data."""
    return user.role in [UserRole.ADMIN, UserRole.MANAGER]


def get_accessible_users_query(user: User, db: Session):
    """Get query for users that the current user can access."""
    if user.role == UserRole.ADMIN:
        return db.query(User)
    elif user.role == UserRole.MANAGER:
        # Managers can see all users except other managers and admins
        return db.query(User).filter(User.role == UserRole.USER)
    else:
        # Regular users only see themselves
        return db.query(User).filter(User.id == user.id)