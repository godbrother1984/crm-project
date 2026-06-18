"""Pydantic schemas for Contact."""

import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class ContactCreate(BaseModel):
    """Schema for creating a new contact."""

    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=50)
    company: str | None = Field(None, max_length=255)
    job_title: str | None = Field(None, max_length=255)
    source: str | None = Field(None, max_length=100)
    notes: str | None = None


class ContactUpdate(BaseModel):
    """Schema for updating an existing contact. All fields optional."""

    first_name: str | None = Field(None, min_length=1, max_length=100)
    last_name: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=50)
    company: str | None = Field(None, max_length=255)
    job_title: str | None = Field(None, max_length=255)
    source: str | None = Field(None, max_length=100)
    notes: str | None = None


class ContactRead(BaseModel):
    """Schema for reading a contact (API response)."""

    id: uuid.UUID
    first_name: str
    last_name: str
    email: str | None = None
    phone: str | None = None
    company: str | None = None
    job_title: str | None = None
    source: str | None = None
    notes: str | None = None
    lifetime_value: float = 0.0
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ContactSummary(BaseModel):
    """Lightweight contact summary for list views."""

    id: uuid.UUID
    first_name: str
    last_name: str
    email: str | None = None
    company: str | None = None
    lifetime_value: float = 0.0
    created_at: datetime

    model_config = {"from_attributes": True}
