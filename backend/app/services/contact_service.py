"""Contact business logic."""

import uuid

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate


class ContactService:
    """CRUD operations for contacts."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        search: str | None = None,
        sort_by: str = "created_at",
        sort_desc: bool = True,
    ) -> tuple[list[Contact], int]:
        """List contacts with pagination, search, and sorting."""
        query = select(Contact)

        if search:
            like = f"%{search}%"
            query = query.where(
                Contact.first_name.ilike(like)
                | Contact.last_name.ilike(like)
                | Contact.email.ilike(like)
                | Contact.company.ilike(like)
            )

        # count total before pagination
        count_q = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_q)).scalar_one()

        # sorting
        sort_col = getattr(Contact, sort_by, Contact.created_at)
        order = sort_col.desc() if sort_desc else sort_col.asc()
        query = query.order_by(order).offset(skip).limit(limit)

        result = await self.db.execute(query)
        contacts = list(result.scalars().all())
        return contacts, total

    async def get_by_id(self, contact_id: uuid.UUID) -> Contact | None:
        """Get a single contact by ID."""
        result = await self.db.execute(
            select(Contact).where(Contact.id == contact_id)
        )
        return result.scalar_one_or_none()

    async def create(self, data: ContactCreate) -> Contact:
        """Create a new contact."""
        contact = Contact(**data.model_dump())
        self.db.add(contact)
        await self.db.flush()
        return contact

    async def update(self, contact_id: uuid.UUID, data: ContactUpdate) -> Contact | None:
        """Update an existing contact. Returns None if not found."""
        contact = await self.get_by_id(contact_id)
        if not contact:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(contact, field, value)
        await self.db.flush()
        await self.db.refresh(contact)
        return contact

    async def delete(self, contact_id: uuid.UUID) -> bool:
        """Delete a contact. Returns True if deleted, False if not found."""
        contact = await self.get_by_id(contact_id)
        if not contact:
            return False
        await self.db.delete(contact)
        await self.db.flush()
        return True
