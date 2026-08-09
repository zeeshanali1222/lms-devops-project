"""
models.py - ORM models for the auth microservice.
"""
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, Boolean

from app.database import Base


class User(Base):
    """A registered user account.

    Passwords are never stored in plain text - only the bcrypt hash.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
