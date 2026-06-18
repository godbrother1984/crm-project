"""Deal business logic."""

import uuid

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.deal import Deal
from app.schemas.deal import DealCreate, DealUpdate, DealStageUpdate


class DealService:
    """CRUD operations for deals."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        stage_id: uuid.UUID | None = None,
        contact_id: uuid.UUID | None = None,
        assigned_to: uuid.UUID | None = None,
        sort_by: str = "created_at",
        sort_desc: bool = True,
    ) -> tuple[list[Deal], int]:
        """List deals with pagination and filters."""
        query = select(Deal)

        if stage_id:
            query = query.where(Deal.stage_id == stage_id)
        if contact_id:
            query = query.where(Deal.contact_id == contact_id)
        if assigned_to:
            query = query.where(Deal.assigned_to == assigned_to)

        count_q = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_q)).scalar_one()

        sort_col = getattr(Deal, sort_by, Deal.created_at)
        order = sort_col.desc() if sort_desc else sort_col.asc()
        query = query.order_by(order).offset(skip).limit(limit)

        result = await self.db.execute(query)
        deals = list(result.scalars().all())
        return deals, total

    async def get_by_id(self, deal_id: uuid.UUID) -> Deal | None:
        """Get a single deal by ID."""
        result = await self.db.execute(select(Deal).where(Deal.id == deal_id))
        return result.scalar_one_or_none()

    async def create(self, data: DealCreate) -> Deal:
        """Create a new deal."""
        deal = Deal(**data.model_dump())
        self.db.add(deal)
        await self.db.flush()
        return deal

    async def update(self, deal_id: uuid.UUID, data: DealUpdate) -> Deal | None:
        """Update a deal."""
        deal = await self.get_by_id(deal_id)
        if not deal:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(deal, field, value)
        await self.db.flush()
        await self.db.refresh(deal)
        return deal

    async def update_stage(self, deal_id: uuid.UUID, data: DealStageUpdate) -> Deal | None:
        """Move a deal to a different stage."""
        deal = await self.get_by_id(deal_id)
        if not deal:
            return None
        deal.stage_id = data.stage_id
        if data.probability is not None:
            deal.probability = data.probability
        await self.db.flush()
        await self.db.refresh(deal)
        return deal

    async def delete(self, deal_id: uuid.UUID) -> bool:
        """Delete a deal."""
        deal = await self.get_by_id(deal_id)
        if not deal:
            return False
        await self.db.delete(deal)
        await self.db.flush()
        return True
