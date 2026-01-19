"""
Pydantic schemas package
"""
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserPasswordUpdate,
    UserInDB,
    UserResponse,
    Token,
    TokenData,
    LoginRequest,
)
from app.schemas.crawler import (
    CrawlerBase,
    CrawlerCreate,
    CrawlerUpdate,
    CrawlerInDB,
    CrawlerResponse,
    CrawlerConfigHistoryResponse,
    CrawlerListQuery,
)
from app.schemas.task import (
    TaskBase,
    TaskCreate,
    TaskUpdate,
    TaskInDB,
    TaskResponse,
    TaskLogResponse,
    TaskListQuery,
)

__all__ = [
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserPasswordUpdate",
    "UserInDB",
    "UserResponse",
    "Token",
    "TokenData",
    "LoginRequest",
    # Crawler schemas
    "CrawlerBase",
    "CrawlerCreate",
    "CrawlerUpdate",
    "CrawlerInDB",
    "CrawlerResponse",
    "CrawlerConfigHistoryResponse",
    "CrawlerListQuery",
    # Task schemas
    "TaskBase",
    "TaskCreate",
    "TaskUpdate",
    "TaskInDB",
    "TaskResponse",
    "TaskLogResponse",
    "TaskListQuery",
]
