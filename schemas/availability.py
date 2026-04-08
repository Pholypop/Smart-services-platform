from pydantic import BaseModel
from datetime import time


class AvailabilityBase(BaseModel):
    day_of_week: str | None = None
    start_time: time | None = None
    end_time: time | None = None
    is_available: bool = True


class AvailabilityCreate(AvailabilityBase):
    pass


class AvailabilityResponse(AvailabilityBase):
    id: int

    class Config:
        from_attributes = True