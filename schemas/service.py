from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from schemas.task import TaskResponse
from typing import List , Optional



class ServiceStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


# =========================
# BASE
# =========================

class ServiceBase(BaseModel):
    title: str
    description: str | None = None
    price: float | None = None
    currency: str | None = None
    image_url: str | None = None   


# =========================
# CREATE
# =========================

class ServiceCreate(ServiceBase):
    provider_id: int
    category_id: int

class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    status: Optional[ServiceStatus] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None
    image_url: Optional[str] = None


# =========================
# SIMPLE (للـ lists)
# =========================

class ServiceSimple(BaseModel):
    id: int
    title: str
    price: float | None = None
    image_url: str | None = None  

    class Config:
        from_attributes = True


# =========================
# FULL RESPONSE
# =========================

class ServiceResponse(ServiceBase):
    id: int
    status: ServiceStatus
    rating_average: float
    rating_count: int
    created_at: datetime | None
    updated_at: datetime | None

    tasks: List[TaskResponse] = []   # 🔥

    class Config:
        from_attributes = True