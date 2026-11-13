from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User, UserRole
from app.models.staff import StaffProfile
from app.schemas.staff import StaffScheduleCreate, StaffScheduleResponse
from app.core.security import hash_password
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/admin", tags=["Admin Management"])

@router.post("/staff", response_model=StaffScheduleResponse)
def create_staff(
    staff_in: StaffScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found"
        )

    email_normalized = staff_in.email.strip().lower()
    
    existing_user = db.scalars(select(User.id).where(User.email == email_normalized)).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    new_user = User(
        email=email_normalized,
        full_name=staff_in.full_name,
        hashed_password=hash_password(staff_in.password),
        role=UserRole.staff
    )
    
    new_profile = StaffProfile(
        specialization=staff_in.specialization,
        bio=staff_in.bio,
        user=new_user
    )

    try:
        db.add(new_user)
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to create staff due to database error")

    return new_profile