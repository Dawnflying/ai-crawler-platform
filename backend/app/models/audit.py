"""
Audit log model
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class AuditLog(Base):
    """Audit log model"""

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    action = Column(String(50), nullable=False)  # create/update/delete/execute
    resource_type = Column(String(50), nullable=False, index=True)  # crawler/task/user
    resource_id = Column(Integer, index=True)
    details = Column(Text)  # JSON format operation details
    ip_address = Column(String(50))
    user_agent = Column(Text)
    created_at = Column(DateTime, server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")
