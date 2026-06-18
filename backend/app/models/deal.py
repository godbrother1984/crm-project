"""Deal / Opportunity model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Deal(Base):
    __tablename__ = "deals"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    value: Mapped[float] = mapped_column(Float, default=0.0)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    stage_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("pipeline_stages.id"), nullable=False
    )
    contact_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("contacts.id"), nullable=False
    )
    assigned_to: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("users.id")
    )
    probability: Mapped[float | None] = mapped_column(Float, default=0.0)  # 0-100
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # relationships
    contact = relationship("Contact", back_populates="deals")
    stage = relationship("PipelineStage", back_populates="deals")
    assignee = relationship("User", back_populates="deals")
    activities = relationship("Activity", back_populates="deal", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Deal {self.title} ${self.value}>"
