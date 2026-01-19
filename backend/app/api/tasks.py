"""
Task API endpoints
"""
import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.base import get_db
from app.models.user import User
from app.models.task import Task, TaskLog
from app.models.crawler import Crawler
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskLogResponse
)
from app.core.deps import get_current_user, check_permission

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(check_permission("task:create")),
    db: Session = Depends(get_db)
):
    """Create a new task"""
    # Check if crawler exists
    crawler = db.query(Crawler).filter(Crawler.id == task_data.crawler_id).first()
    if not crawler:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crawler not found"
        )

    # Create new task
    new_task = Task(
        crawler_id=task_data.crawler_id,
        name=task_data.name,
        schedule_type=task_data.schedule_type,
        cron_expression=task_data.cron_expression,
        execute_at=task_data.execute_at,
        config_overrides=json.dumps(task_data.config_overrides) if task_data.config_overrides else None,
        created_by=current_user.id,
        status="pending"
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # If manual execution, queue the task
    if task_data.schedule_type == "manual":
        # TODO: Queue task for execution using Celery
        pass

    return TaskResponse(
        id=new_task.id,
        crawler_id=new_task.crawler_id,
        name=new_task.name,
        status=new_task.status,
        schedule_type=new_task.schedule_type,
        cron_expression=new_task.cron_expression,
        execute_at=new_task.execute_at,
        started_at=new_task.started_at,
        completed_at=new_task.completed_at,
        duration=new_task.duration,
        total_items=new_task.total_items,
        success_items=new_task.success_items,
        failed_items=new_task.failed_items,
        error_message=new_task.error_message,
        config_overrides=json.loads(new_task.config_overrides) if new_task.config_overrides else None,
        created_by=new_task.created_by,
        created_at=new_task.created_at,
        updated_at=new_task.updated_at,
        crawler_name=crawler.name,
        creator_name=current_user.username
    )


@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    crawler_id: int = Query(None),
    status: str = Query(None),
    schedule_type: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(check_permission("task:view")),
    db: Session = Depends(get_db)
):
    """List tasks with filters and pagination"""
    query = db.query(Task)

    # Apply filters
    if crawler_id:
        query = query.filter(Task.crawler_id == crawler_id)
    if status:
        query = query.filter(Task.status == status)
    if schedule_type:
        query = query.filter(Task.schedule_type == schedule_type)

    # Count total
    total = query.count()

    # Apply pagination
    tasks = query.order_by(Task.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    # Build response
    response = []
    for task in tasks:
        crawler_name = task.crawler.name if task.crawler else None
        creator_name = task.creator.username if task.creator else None

        response.append(TaskResponse(
            id=task.id,
            crawler_id=task.crawler_id,
            name=task.name,
            status=task.status,
            schedule_type=task.schedule_type,
            cron_expression=task.cron_expression,
            execute_at=task.execute_at,
            started_at=task.started_at,
            completed_at=task.completed_at,
            duration=task.duration,
            total_items=task.total_items,
            success_items=task.success_items,
            failed_items=task.failed_items,
            error_message=task.error_message,
            config_overrides=json.loads(task.config_overrides) if task.config_overrides else None,
            created_by=task.created_by,
            created_at=task.created_at,
            updated_at=task.updated_at,
            crawler_name=crawler_name,
            creator_name=creator_name
        ))

    return response


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(check_permission("task:view")),
    db: Session = Depends(get_db)
):
    """Get task by ID"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse(
        id=task.id,
        crawler_id=task.crawler_id,
        name=task.name,
        status=task.status,
        schedule_type=task.schedule_type,
        cron_expression=task.cron_expression,
        execute_at=task.execute_at,
        started_at=task.started_at,
        completed_at=task.completed_at,
        duration=task.duration,
        total_items=task.total_items,
        success_items=task.success_items,
        failed_items=task.failed_items,
        error_message=task.error_message,
        config_overrides=json.loads(task.config_overrides) if task.config_overrides else None,
        created_by=task.created_by,
        created_at=task.created_at,
        updated_at=task.updated_at,
        crawler_name=task.crawler.name if task.crawler else None,
        creator_name=task.creator.username if task.creator else None
    )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(check_permission("task:create")),
    db: Session = Depends(get_db)
):
    """Update task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update fields
    if task_data.name is not None:
        task.name = task_data.name
    if task_data.status is not None:
        task.status = task_data.status
    if task_data.error_message is not None:
        task.error_message = task_data.error_message

    db.commit()
    db.refresh(task)

    return TaskResponse(
        id=task.id,
        crawler_id=task.crawler_id,
        name=task.name,
        status=task.status,
        schedule_type=task.schedule_type,
        cron_expression=task.cron_expression,
        execute_at=task.execute_at,
        started_at=task.started_at,
        completed_at=task.completed_at,
        duration=task.duration,
        total_items=task.total_items,
        success_items=task.success_items,
        failed_items=task.failed_items,
        error_message=task.error_message,
        config_overrides=json.loads(task.config_overrides) if task.config_overrides else None,
        created_by=task.created_by,
        created_at=task.created_at,
        updated_at=task.updated_at,
        crawler_name=task.crawler.name if task.crawler else None,
        creator_name=task.creator.username if task.creator else None
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(check_permission("task:create")),
    db: Session = Depends(get_db)
):
    """Delete task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Cannot delete running task
    if task.status == "running":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete running task"
        )

    db.delete(task)
    db.commit()

    return None


@router.get("/{task_id}/logs", response_model=List[TaskLogResponse])
async def get_task_logs(
    task_id: int,
    level: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=500),
    current_user: User = Depends(check_permission("task:view")),
    db: Session = Depends(get_db)
):
    """Get task logs"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    query = db.query(TaskLog).filter(TaskLog.task_id == task_id)

    if level:
        query = query.filter(TaskLog.level == level.upper())

    # Apply pagination
    logs = query.order_by(TaskLog.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return [
        TaskLogResponse(
            id=log.id,
            task_id=log.task_id,
            level=log.level,
            message=log.message,
            details=json.loads(log.details) if log.details else None,
            created_at=log.created_at
        )
        for log in logs
    ]


@router.post("/{task_id}/cancel")
async def cancel_task(
    task_id: int,
    current_user: User = Depends(check_permission("task:create")),
    db: Session = Depends(get_db)
):
    """Cancel a running task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.status not in ["pending", "running"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only cancel pending or running tasks"
        )

    # TODO: Cancel the Celery task
    task.status = "cancelled"
    db.commit()

    return {"message": "Task cancelled successfully"}


@router.post("/{task_id}/execute")
async def execute_task(
    task_id: int,
    current_user: User = Depends(check_permission("task:execute")),
    db: Session = Depends(get_db)
):
    """Execute a task immediately"""
    from app.services.crawler_service import CrawlerService

    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.status == "running":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task is already running"
        )

    # Execute crawler in background
    # For now, execute synchronously for testing
    try:
        service = CrawlerService(db)
        result = service.execute_crawler(task_id)

        if result['success']:
            return {
                "message": "Task executed successfully",
                "total_items": result.get('total_items', 0),
                "success_items": result.get('success_items', 0),
                "failed_items": result.get('failed_items', 0)
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get('error', 'Task execution failed')
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
