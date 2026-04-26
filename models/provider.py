from sqlalchemy import Column, BigInteger, String, Boolean, Float, Integer, DateTime, ForeignKey, Enum , Table
from sqlalchemy.orm import relationship
from database import Base
import enum
from datetime import datetime



class AccountStatus(enum.Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"

# =========================
# ASSOCIATION TABLE 🔥
# =========================

provider_category = Table(
    "provider_category",
    Base.metadata,
    Column("provider_id", BigInteger, ForeignKey("provider.id"), primary_key=True),
    Column("category_id", BigInteger, ForeignKey("service_category.id"), primary_key=True),
)


class Provider(Base):
    __tablename__ = "provider"

    id = Column(BigInteger, primary_key=True, index=True)
    
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False  )
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    bio = Column(String)

    profile_image_url = Column(String)

    is_verified = Column(Boolean, default=False)
    experience_years = Column(Integer)

    rating_average = Column(Float, default=0)
    trust_score = Column(Float, default=0)
    rating_count = Column(Integer, default=0)

    status = Column(Enum(AccountStatus), default=AccountStatus.PENDING)

    # ✅ الجديد
    is_available = Column(Boolean, default=True)

    location_id = Column(BigInteger, ForeignKey("location.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقات
    location = relationship("Location", back_populates="providers")
    services = relationship("Service", back_populates="provider")
    portfolio_images = relationship("PortfolioImage", back_populates="provider", cascade="all, delete")
    

    categories = relationship(
    "ServiceCategory",
    secondary=provider_category,
    back_populates="providers"
)