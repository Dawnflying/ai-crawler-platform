"""
Crawler models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Crawler(Base):
    """Crawler configuration model"""

    __tablename__ = "crawlers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    type = Column(String(20), nullable=False, index=True)  # http/api/browser
    status = Column(String(20), default="inactive", index=True)  # active/inactive/error
    config = Column(Text, nullable=False)  # JSON format complete configuration
    tags = Column(Text)  # JSON array of tags
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    version = Column(Integer, default=1)
    is_template = Column(Boolean, default=False, index=True)
    template_category = Column(String(100))

    # Relationships
    creator = relationship("User", back_populates="crawlers", foreign_keys=[created_by])
    config_history = relationship("CrawlerConfigHistory", back_populates="crawler", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="crawler", cascade="all, delete-orphan")
    crawl_data = relationship("CrawlData", back_populates="crawler", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="crawler", cascade="all, delete-orphan")


class CrawlerConfigHistory(Base):
    """Crawler configuration history model"""

    __tablename__ = "crawler_config_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    crawler_id = Column(Integer, ForeignKey("crawlers.id", ondelete="CASCADE"), nullable=False, index=True)
    config = Column(Text, nullable=False)  # Historical configuration JSON
    version = Column(Integer, nullable=False)
    change_note = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    crawler = relationship("Crawler", back_populates="config_history")
