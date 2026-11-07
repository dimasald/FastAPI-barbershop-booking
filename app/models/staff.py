import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.service import Service
    from app.models.schedule import StaffSchedule


class StaffProfile(Base):
    __tablename__ = "staff_profiles"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    specialization: Mapped[str] = mapped_column(String(100))
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(back_populates="staff_profile")
    services: Mapped[List["Service"]] = relationship(
        secondary="staff_services", back_populates="staff_members")
    
    schedules: Mapped[List["StaffSchedule"]] = relationship(
        back_populates="staff", cascade="all, delete-orphan"
    )