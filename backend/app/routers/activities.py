"""FastAPI router for Activities CRUD."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.activity import ActivityCreate, ActivityRead, ActivityUpdate
from app.services.activity_service import ActivityService

router = APIRouter(prefix="/api/v1/activities", tags=["activities"])


@router.get("", response_model=dict)
async def list_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    contact_id: uuid.UUID | None = Query(None),
    deal_id: uuid.UUID | None = Query(None),
    activity_type: str | None = Query(None, pattern=r"^(note|call|email|meeting|task)$"),
    done: bool | None = Query(None),
    sort_by: str = Query("created_at", pattern=r"^(subject|activity_type|created_at|updated_at|due_at)$"),
    sort_desc: bool = Query(True),
    db: AsyncSession = Depends(get_db),
):
    """List activities with filters."""
    svc = ActivityService(db)
    activities, total = await svc.list(
        skip=skip, limit=limit, contact_id=contact_id,
        deal_id=deal_id, activity_type=activity_type, done=done,
        sort_by=sort_by, sort_desc=sort_desc,
    )
    return {
        "items": [ActivityRead.model_validate(a) for a in activities],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/{activity_id}", response_model=ActivityRead)
async def get_activity(activity_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Get a single activity."""
    svc = ActivityService(db)
    activity = await svc.get_by_id(activity_id)
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
    return activity


@router.post("", response_model=ActivityRead, status_code=status.HTTP_201_CREATED)
async def create_activity(data: ActivityCreate, db: AsyncSession = Depends(get_db)):
    """Create a new activity."""
    svc = ActivityService(db)
    activity = await svc.create(data)
    return activity


@router.put("/{activity_id}", response_model=ActivityRead)
async def update_activity(
    activity_id: uuid.UUID,
    data: ActivityUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an activity."""
    svc = ActivityService(db)
    activity = await svc.update(activity_id, data)
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
    return activity


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(activity_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Delete an activity."""
    svc = ActivityService(db)
    deleted = await svc.delete(activity_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
