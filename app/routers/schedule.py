import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User, UserRole
from app.models.staff import StaffProfile
from app.models.schedule import StaffSchedule
from app.schemas.schedule import StaffScheduleCreate, StaffScheduleResponse

router = APIRouter(prefix="/staff", tags=["Schedules"])


@router.post("/{staff_id}/schedules", response_model=StaffScheduleResponse)
def create_schedule(
    staff_id: uuid.UUID,
    schedule_in: StaffScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in [UserRole.admin, UserRole.staff]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create schedules",
        )

    if current_user.role == UserRole.staff and (not current_user.staff_profile or current_user.staff_profile.id != staff_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
                detail="Staff members can only manage their own schedule",
            )

    staff = db.scalars(select(StaffProfile).where(StaffProfile.id == staff_id)).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    if schedule_in.start_time >= schedule_in.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time must be before end time",
        )

    overlap_query = select(StaffSchedule).where(
        StaffSchedule.staff_id == staff_id,
        StaffSchedule.day_of_week == schedule_in.day_of_week,
        StaffSchedule.is_active == True,
        StaffSchedule.start_time < schedule_in.end_time,
        StaffSchedule.end_time > schedule_in.start_time,
    )

    overlapping_schedule = db.scalars(overlap_query).first()
    if overlapping_schedule:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Schedule overlaps with an existing shift",
        )

    new_schedule = StaffSchedule(
        staff_id=staff_id,
        day_of_week=schedule_in.day_of_week,
        start_time=schedule_in.start_time,
        end_time=schedule_in.end_time,
    )

    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)

    return new_schedule
