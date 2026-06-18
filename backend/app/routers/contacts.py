"""FastAPI router for Contacts CRUD."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.contact import ContactCreate, ContactRead, ContactSummary, ContactUpdate
from app.services.contact_service import ContactService

router = APIRouter(prefix="/api/v1/contacts", tags=["contacts"])


@router.get("", response_model=dict)
async def list_contacts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: str | None = Query(None),
    sort_by: str = Query("created_at", pattern=r"^(first_name|last_name|email|company|created_at|updated_at)$"),
    sort_desc: bool = Query(True),
    db: AsyncSession = Depends(get_db),
):
    """List contacts with pagination, search, and sorting."""
    svc = ContactService(db)
    contacts, total = await svc.list(
        skip=skip, limit=limit, search=search, sort_by=sort_by, sort_desc=sort_desc,
    )
    return {
        "items": [ContactSummary.model_validate(c) for c in contacts],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/{contact_id}", response_model=ContactRead)
async def get_contact(
    contact_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get a single contact by ID."""
    svc = ContactService(db)
    contact = await svc.get_by_id(contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("", response_model=ContactRead, status_code=status.HTTP_201_CREATED)
async def create_contact(
    data: ContactCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new contact."""
    svc = ContactService(db)
    contact = await svc.create(data)
    return contact


@router.put("/{contact_id}", response_model=ContactRead)
async def update_contact(
    contact_id: uuid.UUID,
    data: ContactUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an existing contact."""
    svc = ContactService(db)
    contact = await svc.update(contact_id, data)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    contact_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a contact."""
    svc = ContactService(db)
    deleted = await svc.delete(contact_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
