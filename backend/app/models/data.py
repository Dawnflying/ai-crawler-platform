"""
Data models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class CrawlData(Base):
    """Crawled data model"""

    __tablename__ = "crawl_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    crawler_id = Column(Integer, ForeignKey("crawlers.id", ondelete="CASCADE"), nullable=False, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    data = Column(Text, nullable=False)  # JSON format crawled data
    data_hash = Column(String(64), index=True)  # Hash for deduplication
    url = Column(Text)  # Source URL
    status = Column(String(20), default="success")  # success/failed
    error_message = Column(Text)
    created_at = Column(DateTime, server_default=func.now(), index=True)

    # Relationships
    crawler = relationship("Crawler", back_populates="crawl_data")
    task = relationship("Task", back_populates="crawl_data")


class DataSource(Base):
    """Data source configuration model"""

    __tablename__ = "data_sources"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    type = Column(String(50), nullable=False, index=True)  # database/api/file
    config = Column(Text, nullable=False)  # JSON format configuration
    description = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
