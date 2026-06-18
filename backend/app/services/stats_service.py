"""Stats / dashboard summary service."""

from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contact import Contact
from app.models.deal import Deal
from app.models.pipeline import PipelineStage
from app.models.activity import Activity


class StatsService:
    """Aggregated statistics for the CRM dashboard."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def summary(self) -> dict:
        """Return a dashboard summary with key metrics."""
        # Total contacts
        total_contacts = (
            await self.db.execute(select(func.count(Contact.id)))
        ).scalar_one()

        # New contacts last 30 days
        thirty_days_ago = datetime.now(UTC) - timedelta(days=30)
        new_contacts = (
            await self.db.execute(
                select(func.count(Contact.id)).where(
                    Contact.created_at >= thirty_days_ago
                )
            )
        ).scalar_one()

        # Total deals
        total_deals = (
            await self.db.execute(select(func.count(Deal.id)))
        ).scalar_one()

        # Pipeline value (sum of all deals)
        pipeline_value = (
            await self.db.execute(
                select(func.coalesce(func.sum(Deal.value), 0))
            )
        ).scalar_one()

        # Deals by stage
        stages_result = await self.db.execute(
            select(PipelineStage.id, PipelineStage.name)
        )
        deals_by_stage = {}
        for stage_id, stage_name in stages_result:
            count = (
                await self.db.execute(
                    select(func.count(Deal.id)).where(Deal.stage_id == stage_id)
                )
            ).scalar_one()
            deals_by_stage[str(stage_id)] = {"name": stage_name, "count": count}

        # Pending activities
        pending_activities = (
            await self.db.execute(
                select(func.count(Activity.id)).where(Activity.done == False)  # noqa: E712
            )
        ).scalar_one()

        return {
            "total_contacts": total_contacts,
            "new_contacts_30d": new_contacts,
            "total_deals": total_deals,
            "pipeline_value": float(pipeline_value),
            "deals_by_stage": deals_by_stage,
            "pending_activities": pending_activities,
        }
