"""
Task models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Task(Base):
    """Task model"""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    crawler_id = Column(Integer, ForeignKey("crawlers.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    status = Column(String(20), default="pending", index=True)  # pending/running/completed/failed/cancelled
    schedule_type = Column(String(20), default="manual")  # manual/cron/once
    cron_expression = Column(String(100))
    execute_at = Column(DateTime, index=True)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    duration = Column(Integer)  # seconds
    total_items = Column(Integer, default=0)
    success_items = Column(Integer, default=0)
    failed_items = Column(Integer, default=0)
    error_message = Column(Text)
    config_overrides = Column(Text)  # JSON format task configuration overrides
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    created_at = Column(DateTime, server_default=func.now(), index=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    crawler = relationship("Crawler", back_populates="tasks")
    creator = relationship("User", back_populates="tasks", foreign_keys=[created_by])
    logs = relationship("TaskLog", back_populates="task", cascade="all, delete-orphan")
    crawl_data = relationship("CrawlData", back_populates="task", cascade="all, delete-orphan")
    alert_records = relationship("AlertRecord", back_populates="task")


class TaskLog(Base):
    """Task log model"""

    __tablename__ = "task_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    level = Column(String(20), nullable=False, index=True)  # DEBUG/INFO/WARNING/ERROR
    message = Column(Text, nullable=False)
    details = Column(Text)  # JSON format detailed information
    created_at = Column(DateTime, server_default=func.now(), index=True)

    # Relationships
    task = relationship("Task", back_populates="logs")
