"""
System configuration model
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class SystemConfig(Base):
    """System configuration model"""

    __tablename__ = "system_configs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=False)  # JSON format value
    description = Column(Text)
    category = Column(String(50), index=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
