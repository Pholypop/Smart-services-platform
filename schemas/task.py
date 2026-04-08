from pydantic import BaseModel


class TaskBase(BaseModel):
    name: str | None = None
    description: str | None = None
    duration: int | None = None
    price: float | None = None
    mandatory: bool = True


class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int

    class Config:
        from_attributes = True