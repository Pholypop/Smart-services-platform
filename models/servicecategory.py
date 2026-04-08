from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship
from database import Base


class ServiceCategory(Base):
    __tablename__ = "service_category"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    services = relationship("Service", back_populates="category")