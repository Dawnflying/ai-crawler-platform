"""
Crawler API endpoints
"""
import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.base import get_db
from app.models.user import User
from app.models.crawler import Crawler, CrawlerConfigHistory
from app.schemas.crawler import (
    CrawlerCreate,
    CrawlerUpdate,
    CrawlerResponse,
    CrawlerConfigHistoryResponse
)
from app.core.deps import get_current_user, check_permission

router = APIRouter(prefix="/crawlers", tags=["Crawlers"])


@router.post("", response_model=CrawlerResponse, status_code=status.HTTP_201_CREATED)
async def create_crawler(
    crawler_data: CrawlerCreate,
    current_user: User = Depends(check_permission("crawler:create")),
    db: Session = Depends(get_db)
):
    """Create a new crawler"""
    # Create new crawler
    new_crawler = Crawler(
        name=crawler_data.name,
        description=crawler_data.description,
        type=crawler_data.type,
        config=json.dumps(crawler_data.config),
        tags=json.dumps(crawler_data.tags) if crawler_data.tags else None,
        created_by=current_user.id,
        is_template=crawler_data.is_template,
        template_category=crawler_data.template_category,
        status="inactive",
        version=1
    )

    db.add(new_crawler)
    db.commit()
    db.refresh(new_crawler)

    # Create initial config history
    config_history = CrawlerConfigHistory(
        crawler_id=new_crawler.id,
        config=new_crawler.config,
        version=1,
        change_note="Initial version",
        created_by=current_user.id
    )
    db.add(config_history)
    db.commit()

    return CrawlerResponse(
        id=new_crawler.id,
        name=new_crawler.name,
        description=new_crawler.description,
        type=new_crawler.type,
        status=new_crawler.status,
        config=json.loads(new_crawler.config),
        tags=json.loads(new_crawler.tags) if new_crawler.tags else [],
        created_by=new_crawler.created_by,
        created_at=new_crawler.created_at,
        updated_at=new_crawler.updated_at,
        version=new_crawler.version,
        is_template=new_crawler.is_template,
        template_category=new_crawler.template_category,
        creator_name=current_user.username,
        task_count=0
    )


@router.get("", response_model=List[CrawlerResponse])
async def list_crawlers(
    type: str = Query(None),
    status: str = Query(None),
    is_template: bool = Query(None),
    search: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(check_permission("crawler:view")),
    db: Session = Depends(get_db)
):
    """List crawlers with filters and pagination"""
    query = db.query(Crawler)

    # Apply filters
    if type:
        query = query.filter(Crawler.type == type)
    if status:
        query = query.filter(Crawler.status == status)
    if is_template is not None:
        query = query.filter(Crawler.is_template == is_template)
    if search:
        query = query.filter(
            or_(
                Crawler.name.contains(search),
                Crawler.description.contains(search)
            )
        )

    # Count total
    total = query.count()

    # Apply pagination
    crawlers = query.order_by(Crawler.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    # Build response
    response = []
    for crawler in crawlers:
        task_count = len(crawler.tasks) if crawler.tasks else 0
        creator_name = crawler.creator.username if crawler.creator else None

        response.append(CrawlerResponse(
            id=crawler.id,
            name=crawler.name,
            description=crawler.description,
            type=crawler.type,
            status=crawler.status,
            config=json.loads(crawler.config),
            tags=json.loads(crawler.tags) if crawler.tags else [],
            created_by=crawler.created_by,
            created_at=crawler.created_at,
            updated_at=crawler.updated_at,
            version=crawler.version,
            is_template=crawler.is_template,
            template_category=crawler.template_category,
            creator_name=creator_name,
            task_count=task_count
        ))

    return response


@router.get("/{crawler_id}", response_model=CrawlerResponse)
async def get_crawler(
    crawler_id: int,
    current_user: User = Depends(check_permission("crawler:view")),
    db: Session = Depends(get_db)
):
    """Get crawler by ID"""
    crawler = db.query(Crawler).filter(Crawler.id == crawler_id).first()
    if not crawler:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crawler not found"
        )

    task_count = len(crawler.tasks) if crawler.tasks else 0
    creator_name = crawler.creator.username if crawler.creator else None
    last_execution = None
    if crawler.tasks:
        latest_task = sorted(crawler.tasks, key=lambda x: x.created_at, reverse=True)[0]
        last_execution = latest_task.created_at

    return CrawlerResponse(
        id=crawler.id,
        name=crawler.name,
        description=crawler.description,
        type=crawler.type,
        status=crawler.status,
        config=json.loads(crawler.config),
        tags=json.loads(crawler.tags) if crawler.tags else [],
        created_by=crawler.created_by,
        created_at=crawler.created_at,
        updated_at=crawler.updated_at,
        version=crawler.version,
        is_template=crawler.is_template,
        template_category=crawler.template_category,
        creator_name=creator_name,
        task_count=task_count,
        last_execution=last_execution
    )


@router.put("/{crawler_id}", response_model=CrawlerResponse)
async def update_crawler(
    crawler_id: int,
    crawler_data: CrawlerUpdate,
    current_user: User = Depends(check_permission("crawler:edit")),
    db: Session = Depends(get_db)
):
    """Update crawler"""
    crawler = db.query(Crawler).filter(Crawler.id == crawler_id).first()
    if not crawler:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crawler not found"
        )

    # Update fields
    if crawler_data.name is not None:
        crawler.name = crawler_data.name
    if crawler_data.description is not None:
        crawler.description = crawler_data.description
    if crawler_data.status is not None:
        crawler.status = crawler_data.status
    if crawler_data.tags is not None:
        crawler.tags = json.dumps(crawler_data.tags)

    # If config is updated, increment version and save history
    if crawler_data.config is not None:
        crawler.config = json.dumps(crawler_data.config)
        crawler.version += 1

        # Save config history
        config_history = CrawlerConfigHistory(
            crawler_id=crawler.id,
            config=crawler.config,
            version=crawler.version,
            change_note=crawler_data.change_note or "Updated configuration",
            created_by=current_user.id
        )
        db.add(config_history)

    db.commit()
    db.refresh(crawler)

    return CrawlerResponse(
        id=crawler.id,
        name=crawler.name,
        description=crawler.description,
        type=crawler.type,
        status=crawler.status,
        config=json.loads(crawler.config),
        tags=json.loads(crawler.tags) if crawler.tags else [],
        created_by=crawler.created_by,
        created_at=crawler.created_at,
        updated_at=crawler.updated_at,
        version=crawler.version,
        is_template=crawler.is_template,
        template_category=crawler.template_category,
        creator_name=crawler.creator.username if crawler.creator else None,
        task_count=len(crawler.tasks) if crawler.tasks else 0
    )


@router.delete("/{crawler_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_crawler(
    crawler_id: int,
    current_user: User = Depends(check_permission("crawler:delete")),
    db: Session = Depends(get_db)
):
    """Delete crawler"""
    crawler = db.query(Crawler).filter(Crawler.id == crawler_id).first()
    if not crawler:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crawler not found"
        )

    db.delete(crawler)
    db.commit()

    return None


@router.get("/{crawler_id}/history", response_model=List[CrawlerConfigHistoryResponse])
async def get_crawler_history(
    crawler_id: int,
    current_user: User = Depends(check_permission("crawler:view")),
    db: Session = Depends(get_db)
):
    """Get crawler configuration history"""
    crawler = db.query(Crawler).filter(Crawler.id == crawler_id).first()
    if not crawler:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crawler not found"
        )

    history = db.query(CrawlerConfigHistory).filter(
        CrawlerConfigHistory.crawler_id == crawler_id
    ).order_by(CrawlerConfigHistory.version.desc()).all()

    return [
        CrawlerConfigHistoryResponse(
            id=h.id,
            crawler_id=h.crawler_id,
            config=json.loads(h.config),
            version=h.version,
            change_note=h.change_note,
            created_by=h.created_by,
            created_at=h.created_at
        )
        for h in history
    ]
