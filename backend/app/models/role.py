"""
Role model
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Role(Base):
    """Role model"""

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)  # admin/developer/viewer
    display_name = Column(String(100), nullable=False)
    description = Column(Text)
    permissions = Column(Text)  # JSON format permission list
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    users = relationship("User", back_populates="role")
