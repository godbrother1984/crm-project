"""Pydantic schemas for Pipeline and PipelineStage."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class PipelineStageCreate(BaseModel):
    """Schema for creating a pipeline stage."""

    name: str = Field(..., min_length=1, max_length=255)
    order: int = 0
    probability: float = 0.0
    color: str | None = Field(None, pattern=r"^#[0-9a-fA-F]{6}$")


class PipelineStageRead(BaseModel):
    """Schema for reading a pipeline stage."""

    id: uuid.UUID
    pipeline_id: uuid.UUID
    name: str
    order: int
    probability: float
    color: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PipelineCreate(BaseModel):
    """Schema for creating a pipeline."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=500)
    stages: list[PipelineStageCreate] = []


class PipelineRead(BaseModel):
    """Schema for reading a pipeline with its stages."""

    id: uuid.UUID
    name: str
    description: str | None = None
    stages: list[PipelineStageRead] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
