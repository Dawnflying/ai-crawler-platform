"""
Crawler schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class CrawlerBase(BaseModel):
    """Base crawler schema"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    type: str = Field(..., pattern="^(http|api|browser)$")
    tags: Optional[List[str]] = None


class CrawlerCreate(CrawlerBase):
    """Crawler creation schema"""
    config: Dict[str, Any]
    is_template: bool = False
    template_category: Optional[str] = None


class CrawlerUpdate(BaseModel):
    """Crawler update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(active|inactive|error)$")
    config: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    change_note: Optional[str] = None


class CrawlerInDB(CrawlerBase):
    """Crawler in database schema"""
    id: int
    status: str
    config: Dict[str, Any]
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    version: int
    is_template: bool
    template_category: Optional[str] = None

    class Config:
        from_attributes = True


class CrawlerResponse(CrawlerInDB):
    """Crawler response schema"""
    creator_name: Optional[str] = None
    task_count: int = 0
    last_execution: Optional[datetime] = None


class CrawlerConfigHistoryResponse(BaseModel):
    """Crawler config history response schema"""
    id: int
    crawler_id: int
    config: Dict[str, Any]
    version: int
    change_note: Optional[str] = None
    created_by: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CrawlerListQuery(BaseModel):
    """Crawler list query schema"""
    type: Optional[str] = None
    status: Optional[str] = None
    created_by: Optional[int] = None
    is_template: Optional[bool] = None
    search: Optional[str] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
