from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship
from database import Base


class Location(Base):
    __tablename__ = "location"

    id = Column(BigInteger, primary_key=True, index=True)
    city = Column(String)
    address = Column(String)
    region = Column(String)

    providers = relationship("Provider", back_populates="location")