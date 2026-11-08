from datetime import time
from pydantic import BaseModel, Field

class StaffScheduleCreate(BaseModel):
    day_of_week: int = Field(ge=0, le=6)
    start_time: time
    end_time: time

class StaffScheduleResponse(BaseModel):
    id: str
    staff_id: str
    day_of_week: int
    start_time: time
    end_time: time
    is_active: bool

    model_config = {"from_attributes": True}