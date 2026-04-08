from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from schemas.task import TaskResponse



class ServiceStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


class ServiceBase(BaseModel):
    title: str
    description: str | None = None
    price: float | None = None
    currency: str | None = None


class ServiceCreate(ServiceBase):
    provider_id: int
    category_id: int


class ServiceResponse(ServiceBase):
    id: int
    status: ServiceStatus
    rating_average: float
    rating_count: int
    created_at: datetime

    class Config:
        from_attributes = True

class ServiceSimple(BaseModel):
    id: int
    title: str
    price: float | None = None

    class Config:
        from_attributes = True

class ServiceResponse(BaseModel):
    id: int
    title: str

    tasks: list[TaskResponse] = []  # 🔥

    class Config:
        from_attributes = True