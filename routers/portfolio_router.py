from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.portfolio import PortfolioCreate, PortfolioResponse
from services import portfolio_service

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PortfolioResponse)
def create_portfolio(data: PortfolioCreate, db: Session = Depends(get_db)):
    return portfolio_service.create_portfolio(db, data)

@router.get("/{portfolio_id}", response_model=PortfolioResponse)
def get_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    portfolio = portfolio_service.get_portfolio(db, portfolio_id)

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    return portfolio

@router.get("/", response_model=list[PortfolioResponse])
def get_all_portfolio(db: Session = Depends(get_db)):
    return portfolio_service.get_all_portfolio(db)

@router.put("/{portfolio_id}", response_model=PortfolioResponse)
def update_portfolio(portfolio_id: int, data: PortfolioCreate, db: Session = Depends(get_db)):
    portfolio = portfolio_service.update_portfolio(db, portfolio_id, data)

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    return portfolio

@router.delete("/{portfolio_id}")
def delete_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    success = portfolio_service.delete_portfolio(db, portfolio_id)

    if not success:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    return {"message": "Portfolio deleted"}

@router.patch("/{image_id}/url")
def update_image_url(image_id: int, image_url: str, db: Session = Depends(get_db)):
    image = portfolio_service.update_image_url(db, image_id, image_url)

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    return image

@router.get("/{image_id}/info")
def get_image_info(image_id: int, db: Session = Depends(get_db)):
    image = portfolio_service.get_portfolio(db, image_id)

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    return portfolio_service.get_image_info(image)



