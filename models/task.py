from sqlalchemy import Column, BigInteger, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Task(Base):
    __tablename__ = "task"

    id = Column(BigInteger, primary_key=True, index=True)

    service_id = Column(BigInteger, ForeignKey("service.id"), nullable=False)

    name = Column(String)
    description = Column(String)
    duration = Column(Integer)
    price = Column(Float)
    mandatory = Column(Boolean, default=True)

    service = relationship("Service", back_populates="tasks")