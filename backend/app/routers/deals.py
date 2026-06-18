"""FastAPI router for Deals CRUD."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.deal import DealCreate, DealRead, DealStageUpdate, DealUpdate
from app.services.deal_service import DealService

router = APIRouter(prefix="/api/v1/deals", tags=["deals"])


@router.get("", response_model=dict)
async def list_deals(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    stage_id: uuid.UUID | None = Query(None),
    contact_id: uuid.UUID | None = Query(None),
    assigned_to: uuid.UUID | None = Query(None),
    sort_by: str = Query("created_at", pattern=r"^(title|value|probability|created_at|updated_at|closed_at)$"),
    sort_desc: bool = Query(True),
    db: AsyncSession = Depends(get_db),
):
    """List deals with filters and pagination."""
    svc = DealService(db)
    deals, total = await svc.list(
        skip=skip, limit=limit, stage_id=stage_id,
        contact_id=contact_id, assigned_to=assigned_to,
        sort_by=sort_by, sort_desc=sort_desc,
    )
    return {
        "items": [DealRead.model_validate(d) for d in deals],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/{deal_id}", response_model=DealRead)
async def get_deal(deal_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Get a single deal by ID."""
    svc = DealService(db)
    deal = await svc.get_by_id(deal_id)
    if not deal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")
    return deal


@router.post("", response_model=DealRead, status_code=status.HTTP_201_CREATED)
async def create_deal(data: DealCreate, db: AsyncSession = Depends(get_db)):
    """Create a new deal."""
    svc = DealService(db)
    deal = await svc.create(data)
    return deal


@router.put("/{deal_id}", response_model=DealRead)
async def update_deal(deal_id: uuid.UUID, data: DealUpdate, db: AsyncSession = Depends(get_db)):
    """Update an existing deal."""
    svc = DealService(db)
    deal = await svc.update(deal_id, data)
    if not deal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")
    return deal


@router.patch("/{deal_id}/stage", response_model=DealRead)
async def move_deal_stage(
    deal_id: uuid.UUID,
    data: DealStageUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Move a deal to a different pipeline stage."""
    svc = DealService(db)
    deal = await svc.update_stage(deal_id, data)
    if not deal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")
    return deal


@router.delete("/{deal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_deal(deal_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Delete a deal."""
    svc = DealService(db)
    deleted = await svc.delete(deal_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")
