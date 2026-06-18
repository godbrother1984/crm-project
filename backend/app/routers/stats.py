"""FastAPI router for Dashboard / Stats."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.stats_service import StatsService

router = APIRouter(prefix="/api/v1/stats", tags=["stats"])


@router.get("/summary", response_model=dict)
async def get_dashboard_summary(db: AsyncSession = Depends(get_db)):
    """Get CRM dashboard summary statistics."""
    svc = StatsService(db)
    return await svc.summary()
