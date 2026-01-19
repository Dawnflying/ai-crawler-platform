"""
Alert models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Alert(Base):
    """Alert configuration model"""

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    type = Column(String(50), nullable=False)  # task_failed/task_slow/data_empty
    condition = Column(Text, nullable=False)  # JSON format alert condition
    notification_channels = Column(Text, nullable=False)  # JSON array: email/webhook/sms
    enabled = Column(Boolean, default=True, index=True)
    crawler_id = Column(Integer, ForeignKey("crawlers.id", ondelete="CASCADE"), index=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    crawler = relationship("Crawler", back_populates="alerts")
    records = relationship("AlertRecord", back_populates="alert", cascade="all, delete-orphan")


class AlertRecord(Base):
    """Alert record model"""

    __tablename__ = "alert_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    alert_id = Column(Integer, ForeignKey("alerts.id", ondelete="CASCADE"), nullable=False, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="SET NULL"), index=True)
    level = Column(String(20), nullable=False)  # info/warning/critical
    title = Column(String(500), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(20), default="pending", index=True)  # pending/sent/failed
    sent_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now(), index=True)

    # Relationships
    alert = relationship("Alert", back_populates="records")
    task = relationship("Task", back_populates="alert_records")
