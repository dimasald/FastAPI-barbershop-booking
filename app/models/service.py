import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import String, Integer, Numeric, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.staff import StaffProfile

staff_services = Table(
    "staff_services",
    Base.metadata,
    Column("staff_id", ForeignKey("staff_profiles.id", ondelete="CASCADE"), primary_key=True),
    Column("service_id", ForeignKey("services.id", ondelete="CASCADE"), primary_key=True)
)

class Service(Base):
    __tablename__ = "services"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), index=True)
    duration_minutes: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Numeric(10, 2))

    staff_members: Mapped[List["StaffProfile"]] = relationship(
        secondary=staff_services, back_populates="services"
    )