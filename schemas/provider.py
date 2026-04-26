from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional, List # إضافة List للتعامل مع القوائم
from schemas.service import ServiceSimple
from schemas.portfolio import PortfolioResponse

# افترضنا وجود Schema بسيط للـ Category لعرضه في الرد
# من الأفضل استيراد CategorySimple من ملف الـ schemas الخاص بها إذا وجد
class CategorySimple(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

# =========================
# ENUM
# =========================
class AccountStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"

# =========================
# BASE
# =========================
class ProviderBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    bio: str | None = None
    profile_image_url: str | None = None
    experience_years: int | None = None

class ProviderUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    #profile_image_url: Optional[str] = None
    experience_years: Optional[int] = None
    location_id: Optional[int] = None
    category_ids: Optional[List[int]] = None # لتحديث التخصصات
    is_available: Optional[bool] = None

# =========================
# CREATE (التعديل هنا)
# =========================
class ProviderCreate(ProviderBase):
    user_id: int
    location_id: int | None = None
    # ✅ هذا الحقل هو الذي سيستقبل الـ IDs من الـ Frontend/Auth
    # جعلناه اختياري (Optional) مع قائمة فارغة كقيمة افتراضية لتجنب الـ Errors
    category_ids: List[int] = [] 

# =========================
# RESPONSE (أساسي)
# =========================
class ProviderResponse(ProviderBase):
    id: int
    user_id: int
    is_verified: bool
    rating_average: float
    trust_score: float
    rating_count: int
    status: AccountStatus
    is_available: bool
    created_at: datetime
    updated_at: datetime 
    profile_image_url: Optional[str] = None
   
    portfolio_images: List[PortfolioResponse] = []
    
    categories: List[CategorySimple] = []

    class Config:
        from_attributes = True

# =========================
# RESPONSE WITH SERVICES
# =========================
class ProviderWithServices(BaseModel):
    id: int
    user_id: int
    first_name: str | None = None
    last_name: str | None = None
    rating_average: float
    trust_score: float
    is_available: bool
    
    # ✅ إضافة الأصناف هنا أيضاً مفيد جداً للبحث والفلترة
    categories: List[CategorySimple] = []
    services: list[ServiceSimple] = []

    class Config:
        from_attributes = True