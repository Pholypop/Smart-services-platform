from sqlalchemy.orm import Session
from models.portfolio import PortfolioImage


def create_portfolio(db: Session, data):
    portfolio = PortfolioImage(**data.dict())

    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)

    return portfolio

def get_portfolio(db: Session, portfolio_id: int):
    return db.query(PortfolioImage).filter(PortfolioImage.id == portfolio_id).first()

def get_all_portfolio(db: Session):
    return db.query(PortfolioImage).all()

def update_portfolio(db: Session, portfolio_id: int, data):
    portfolio = db.query(PortfolioImage).filter(PortfolioImage.id == portfolio_id).first()

    if not portfolio:
        return None

    for key, value in data.dict().items():
        setattr(portfolio, key, value)

    db.commit()
    db.refresh(portfolio)

    return portfolio

def delete_portfolio(db: Session, portfolio_id: int):
    portfolio = db.query(PortfolioImage).filter(PortfolioImage.id == portfolio_id).first()

    if not portfolio:
        return False

    db.delete(portfolio)
    db.commit()

    return True

def update_image_url(db, image_id, url):
    image = db.query(PortfolioImage).filter(PortfolioImage.id == image_id).first()

    if not image:
        return None

    image.image_url = url

    db.commit()
    db.refresh(image)
    return image

def get_image_info(image):
    return {
        "id": image.id,
        "url": image.image_url,
        "uploaded_at": image.uploaded_at
    }

