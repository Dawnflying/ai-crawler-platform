"""
User model
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    """User model"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    avatar_url = Column(String(500))
    role_id = Column(Integer, ForeignKey("roles.id"), index=True)
    status = Column(String(20), default="active")  # active/inactive
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    last_login_at = Column(DateTime)

    # Relationships
    role = relationship("Role", back_populates="users")
    crawlers = relationship("Crawler", back_populates="creator", foreign_keys="[Crawler.created_by]")
    tasks = relationship("Task", back_populates="creator", foreign_keys="[Task.created_by]")
    audit_logs = relationship("AuditLog", back_populates="user")
