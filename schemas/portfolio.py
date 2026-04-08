from pydantic import BaseModel
from datetime import datetime


class PortfolioBase(BaseModel):
    image_url: str


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioResponse(PortfolioBase):
    id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True