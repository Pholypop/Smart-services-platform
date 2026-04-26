from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PortfolioBase(BaseModel):
    image_url: str

class PortfolioCreate(PortfolioBase):
    
    pass

class PortfolioUpdate(BaseModel):
   
    image_url: Optional[str] = None

class PortfolioResponse(PortfolioBase):
    id: int
    provider_id: int 
    image_url: str
    uploaded_at: datetime

    class Config:
        from_attributes = True