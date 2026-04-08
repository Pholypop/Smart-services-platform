from sqlalchemy import Column, BigInteger, String, Boolean, Time, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Availability(Base):
    __tablename__ = "availability"

    id = Column(BigInteger, primary_key=True, index=True)

    provider_id = Column(BigInteger, ForeignKey("provider.id"), nullable=False)

    day_of_week = Column(String)
    start_time = Column(Time)
    end_time = Column(Time)
    is_available = Column(Boolean, default=True)

    provider = relationship("Provider", back_populates="availabilities")