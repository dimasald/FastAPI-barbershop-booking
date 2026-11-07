import uuid
from typing import TYPE_CHECKING
from datetime import time
from sqlalchemy import Integer, Time, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.staff import StaffProfile

class StaffSchedule(Base):
    __tablename__ = "staff_schedules"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    staff_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("staff_profiles.id", ondelete="CASCADE"))
    day_of_week: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    staff: Mapped["StaffProfile"] = relationship(back_populates="schedules")