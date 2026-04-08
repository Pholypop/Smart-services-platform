from pydantic import BaseModel


class LocationBase(BaseModel):
    city: str | None = None
    address: str | None = None
    region: str | None = None


class LocationCreate(LocationBase):
    pass


class LocationResponse(LocationBase):
    id: int

    class Config:
        from_attributes = True