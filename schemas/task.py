from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    name: str | None = None
    description: str | None = None
    duration: int | None = None
    price: float | None = None
    mandatory: bool = True
    image_url: str | None = None

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    price: Optional[float] = None
    mandatory: Optional[bool] = None
    image_url: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int

    class Config:
        from_attributes = True