from sqlalchemy import Column, BigInteger, String, Boolean, Float, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum


class ServiceStatus(enum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


class Service(Base):
    __tablename__ = "service"

    id = Column(BigInteger, primary_key=True, index=True)

    provider_id = Column(BigInteger, ForeignKey("provider.id"), nullable=False)

    title = Column(String, nullable=False)
    description = Column(String)

    status = Column(Enum(ServiceStatus), default=ServiceStatus.DRAFT)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    deleted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    price = Column(Float)
    rating_average = Column(Float, default=0)
    rating_count = Column(Integer, default=0)

    currency = Column(String)
    category_id = Column(BigInteger, ForeignKey("service_category.id"), nullable=False)

    publication_date = Column(DateTime)

    # العلاقات
    provider = relationship("Provider", back_populates="services")
    tasks = relationship("Task", back_populates="service")
    category = relationship("ServiceCategory", back_populates="services")