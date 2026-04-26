from pydantic import BaseModel

class LocationBase(BaseModel):
    city: str | None = None
    address: str | None = None
    region: str | None = None

class LocationCreate(LocationBase):
    # يمكنك إجبار المستخدم هنا على إدخال المدينة
    city: str 

class LocationUpdate(LocationBase):
    # جميع الحقول اختيارية للسماح بالتحديث الجزئي
    pass

class LocationResponse(LocationBase):
    id: int

    class Config:
        from_attributes = True