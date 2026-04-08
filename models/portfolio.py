from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class PortfolioImage(Base):
    __tablename__ = "portfolio_image"

    id = Column(BigInteger, primary_key=True, index=True)

    provider_id = Column(BigInteger, ForeignKey("provider.id"), nullable=False)

    image_url = Column(String, nullable=False)
    uploaded_at = Column(DateTime)

    provider = relationship("Provider", back_populates="portfolio_images")