"""
Task schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class TaskBase(BaseModel):
    """Base task schema"""
    name: str = Field(..., min_length=1, max_length=200)
    crawler_id: int


class TaskCreate(TaskBase):
    """Task creation schema"""
    schedule_type: str = Field("manual", pattern="^(manual|cron|once)$")
    cron_expression: Optional[str] = None
    execute_at: Optional[datetime] = None
    config_overrides: Optional[Dict[str, Any]] = None


class TaskUpdate(BaseModel):
    """Task update schema"""
    name: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(pending|running|completed|failed|cancelled)$")
    error_message: Optional[str] = None


class TaskInDB(TaskBase):
    """Task in database schema"""
    id: int
    status: str
    schedule_type: str
    cron_expression: Optional[str] = None
    execute_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration: Optional[int] = None
    total_items: int
    success_items: int
    failed_items: int
    error_message: Optional[str] = None
    config_overrides: Optional[Dict[str, Any]] = None
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskResponse(TaskInDB):
    """Task response schema"""
    crawler_name: Optional[str] = None
    creator_name: Optional[str] = None


class TaskLogResponse(BaseModel):
    """Task log response schema"""
    id: int
    task_id: int
    level: str
    message: str
    details: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TaskListQuery(BaseModel):
    """Task list query schema"""
    crawler_id: Optional[int] = None
    status: Optional[str] = None
    schedule_type: Optional[str] = None
    created_by: Optional[int] = None
    search: Optional[str] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
