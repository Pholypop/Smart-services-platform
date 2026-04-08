from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from schemas.service import ServiceSimple



class AccountStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"


class ProviderBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    bio: str | None = None
    profile_image_url: str | None = None
    experience_years: int | None = None


class ProviderCreate(ProviderBase):
    user_id: int
    location_id: int | None = None


class ProviderResponse(ProviderBase):
    id: int
    user_id: int
    is_verified: bool
    rating_average: float
    trust_score: float
    rating_count: int
    status: AccountStatus
    created_at: datetime

    class Config:
        from_attributes = True

class ProviderResponse(BaseModel):
    id: int
    user_id: int
    first_name: str | None = None
    last_name: str | None = None

    rating_average: float
    trust_score: float

    # 🔥 هنا Nested
    services: list[ServiceSimple] = []

    class Config:
        from_attributes = True