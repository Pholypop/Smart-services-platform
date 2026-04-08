from sqlalchemy import Column, BigInteger, String, Boolean, Float, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum


class AccountStatus(enum.Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"


class Provider(Base):
    __tablename__ = "provider"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, nullable=False)

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

    location_id = Column(BigInteger, ForeignKey("location.id"))

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # العلاقات
    location = relationship("Location", back_populates="providers")
    services = relationship("Service", back_populates="provider")
    availabilities = relationship("Availability", back_populates="provider")
    portfolio_images = relationship("PortfolioImage", back_populates="provider")