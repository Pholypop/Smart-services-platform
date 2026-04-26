from sqlalchemy import Column, BigInteger, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from models.provider import provider_category

# ========================================================
# 1. تعريف الجدول الوسيط (Association Table)
# يجب أن يكون معرفاً قبل الكلاسات التي تستخدمه أو الإشارة إليه لاحقاً
# ========================================================


# ========================================================
# 2. موديل ServiceCategory المعدل
# ========================================================
class ServiceCategory(Base):
    __tablename__ = "service_category"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # العلاقة القديمة مع الخدمات (تبقى كما هي)
    services = relationship("Service", back_populates="category", cascade="all, delete")

    # ✅ التعديل الجديد: العلاقة مع المزودين (Many-to-Many)
    # نستخدم secondary للإشارة للجدول الوسيط
    providers = relationship(
    "Provider",
    secondary=provider_category,
    back_populates="categories"
)