"""Pydantic schemas for Deal."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class DealCreate(BaseModel):
    """Schema for creating a new deal."""

    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    value: float = Field(default=0.0, ge=0)
    currency: str = "USD"
    stage_id: uuid.UUID
    contact_id: uuid.UUID
    assigned_to: uuid.UUID | None = None
    probability: float | None = Field(None, ge=0, le=100)


class DealUpdate(BaseModel):
    """Schema for updating a deal. All fields optional."""

    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    value: float | None = Field(None, ge=0)
    currency: str | None = None
    stage_id: uuid.UUID | None = None
    contact_id: uuid.UUID | None = None
    assigned_to: uuid.UUID | None = None
    probability: float | None = Field(None, ge=0, le=100)


class DealStageUpdate(BaseModel):
    """Move a deal to a different stage."""

    stage_id: uuid.UUID
    probability: float | None = Field(None, ge=0, le=100)


class DealRead(BaseModel):
    """Schema for reading a deal."""

    id: uuid.UUID
    title: str
    description: str | None = None
    value: float
    currency: str
    stage_id: uuid.UUID
    contact_id: uuid.UUID
    assigned_to: uuid.UUID | None = None
    probability: float | None = None
    closed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
