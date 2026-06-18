"""Pipeline business logic."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.pipeline import Pipeline, PipelineStage
from app.schemas.pipeline import PipelineCreate, PipelineStageCreate


class PipelineService:
    """CRUD for pipelines and stages."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list(self) -> list[Pipeline]:
        """List all pipelines with their stages."""
        result = await self.db.execute(
            select(Pipeline)
            .options(selectinload(Pipeline.stages))
            .order_by(Pipeline.name)
        )
        return list(result.scalars().all())

    async def get_by_id(self, pipeline_id: uuid.UUID) -> Pipeline | None:
        result = await self.db.execute(
            select(Pipeline)
            .options(selectinload(Pipeline.stages))
            .where(Pipeline.id == pipeline_id)
        )
        return result.scalar_one_or_none()

    async def create(self, data: PipelineCreate) -> Pipeline:
        """Create a pipeline with optional stages."""
        stages = [
            PipelineStage(**s.model_dump()) for s in data.stages
        ]
        pipeline = Pipeline(name=data.name, description=data.description, stages=stages)
        self.db.add(pipeline)
        await self.db.flush()
        return pipeline

    async def add_stage(self, pipeline_id: uuid.UUID, data: PipelineStageCreate) -> PipelineStage | None:
        """Add a stage to an existing pipeline."""
        pipeline = await self.get_by_id(pipeline_id)
        if not pipeline:
            return None
        stage = PipelineStage(pipeline_id=pipeline_id, **data.model_dump())
        self.db.add(stage)
        await self.db.flush()
        return stage

    async def delete_pipeline(self, pipeline_id: uuid.UUID) -> bool:
        pipeline = await self.get_by_id(pipeline_id)
        if not pipeline:
            return False
        await self.db.delete(pipeline)
        await self.db.flush()
        return True
