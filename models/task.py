from sqlalchemy import Column, BigInteger, String, Integer, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Task(Base):
    __tablename__ = "task"

    id = Column(BigInteger, primary_key=True, index=True)

    service_id = Column(BigInteger, ForeignKey("service.id", ondelete="CASCADE"), nullable=False)

    name = Column(String)
    description = Column(String)
    duration = Column(Integer)
    price = Column(Float)
    mandatory = Column(Boolean, default=True)
    id = Column(BigInteger, primary_key=True)
    image_url = Column(String, nullable=True)
    #updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    service = relationship("Service", back_populates="tasks")