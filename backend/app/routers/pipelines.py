"""FastAPI router for Pipelines and Stages."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.pipeline import PipelineCreate, PipelineRead, PipelineStageCreate, PipelineStageRead
from app.services.pipeline_service import PipelineService

router = APIRouter(prefix="/api/v1/pipelines", tags=["pipelines"])


@router.get("", response_model=list[PipelineRead])
async def list_pipelines(db: AsyncSession = Depends(get_db)):
    """List all pipelines with their stages."""
    svc = PipelineService(db)
    pipelines = await svc.list()
    return [PipelineRead.model_validate(p) for p in pipelines]


@router.get("/{pipeline_id}", response_model=PipelineRead)
async def get_pipeline(pipeline_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Get a pipeline with its stages."""
    svc = PipelineService(db)
    pipeline = await svc.get_by_id(pipeline_id)
    if not pipeline:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pipeline not found")
    return pipeline


@router.post("", response_model=PipelineRead, status_code=status.HTTP_201_CREATED)
async def create_pipeline(data: PipelineCreate, db: AsyncSession = Depends(get_db)):
    """Create a new pipeline (with optional stages)."""
    svc = PipelineService(db)
    pipeline = await svc.create(data)
    return pipeline


@router.post("/{pipeline_id}/stages", response_model=PipelineStageRead, status_code=status.HTTP_201_CREATED)
async def add_pipeline_stage(
    pipeline_id: uuid.UUID,
    data: PipelineStageCreate,
    db: AsyncSession = Depends(get_db),
):
    """Add a stage to an existing pipeline."""
    svc = PipelineService(db)
    stage = await svc.add_stage(pipeline_id, data)
    if not stage:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pipeline not found")
    return stage


@router.delete("/{pipeline_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pipeline(pipeline_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Delete a pipeline and all its stages."""
    svc = PipelineService(db)
    deleted = await svc.delete_pipeline(pipeline_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pipeline not found")
