"""Pydantic schemas for Activity."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ActivityCreate(BaseModel):
    """Schema for creating a new activity."""

    activity_type: str = Field(
        default="note",
        pattern=r"^(note|call|email|meeting|task)$",
    )
    subject: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    contact_id: uuid.UUID | None = None
    deal_id: uuid.UUID | None = None
    done: bool = False
    due_at: datetime | None = None


class ActivityUpdate(BaseModel):
    """Schema for updating an activity."""

    activity_type: str | None = Field(
        None, pattern=r"^(note|call|email|meeting|task)$"
    )
    subject: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    done: bool | None = None
    due_at: datetime | None = None
    done_at: datetime | None = None


class ActivityRead(BaseModel):
    """Schema for reading an activity."""

    id: uuid.UUID
    activity_type: str
    subject: str
    description: str | None = None
    contact_id: uuid.UUID | None = None
    deal_id: uuid.UUID | None = None
    done: bool
    due_at: datetime | None = None
    done_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
