"""Activity business logic."""

import uuid

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityUpdate


class ActivityService:
    """CRUD operations for activities."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        contact_id: uuid.UUID | None = None,
        deal_id: uuid.UUID | None = None,
        activity_type: str | None = None,
        done: bool | None = None,
        sort_by: str = "created_at",
        sort_desc: bool = True,
    ) -> tuple[list[Activity], int]:
        """List activities with filters."""
        query = select(Activity)

        if contact_id:
            query = query.where(Activity.contact_id == contact_id)
        if deal_id:
            query = query.where(Activity.deal_id == deal_id)
        if activity_type:
            query = query.where(Activity.activity_type == activity_type)
        if done is not None:
            query = query.where(Activity.done == done)

        count_q = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_q)).scalar_one()

        sort_col = getattr(Activity, sort_by, Activity.created_at)
        order = sort_col.desc() if sort_desc else sort_col.asc()
        query = query.order_by(order).offset(skip).limit(limit)

        result = await self.db.execute(query)
        activities = list(result.scalars().all())
        return activities, total

    async def get_by_id(self, activity_id: uuid.UUID) -> Activity | None:
        result = await self.db.execute(
            select(Activity).where(Activity.id == activity_id)
        )
        return result.scalar_one_or_none()

    async def create(self, data: ActivityCreate) -> Activity:
        activity = Activity(**data.model_dump())
        self.db.add(activity)
        await self.db.flush()
        return activity

    async def update(self, activity_id: uuid.UUID, data: ActivityUpdate) -> Activity | None:
        activity = await self.get_by_id(activity_id)
        if not activity:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(activity, field, value)
        await self.db.flush()
        await self.db.refresh(activity)
        return activity

    async def delete(self, activity_id: uuid.UUID) -> bool:
        activity = await self.get_by_id(activity_id)
        if not activity:
            return False
        await self.db.delete(activity)
        await self.db.flush()
        return True
