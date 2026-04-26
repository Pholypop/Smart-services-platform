from sqlalchemy.orm import Session
from models.portfolio import PortfolioImage
from datetime import datetime
import os
import shutil
from uuid import uuid4
from datetime import datetime
from fastapi import UploadFile

def create_portfolio(db: Session, file: UploadFile, provider_id: int):
    
    upload_dir = "static/portfolio_images"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    
    extension = file.filename.split(".")[-1]
    file_name = f"portfolio_{uuid4()}.{extension}"
    file_path = os.path.join(upload_dir, file_name)

    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    
    image_url = f"/{file_path}"
    portfolio = PortfolioImage(
        provider_id=provider_id,
        image_url=image_url,
        uploaded_at=datetime.utcnow()
    )

    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)

    return portfolio

def get_portfolio(db: Session, portfolio_id: int):
    return db.query(PortfolioImage).filter(PortfolioImage.id == portfolio_id).first()

def get_all_portfolio(db: Session):
    return db.query(PortfolioImage).all()

def update_portfolio(db: Session, portfolio_id: int, file: UploadFile = None, data = None):
    portfolio = db.query(PortfolioImage).filter(PortfolioImage.id == portfolio_id).first()

    if not portfolio:
        return None

    
    if file and isinstance(file, UploadFile):
        
        try:
            if portfolio.image_url:
                old_path = portfolio.image_url.lstrip('/')
                if os.path.exists(old_path):
                    os.remove(old_path)
        except Exception as e:
            print(f"Error deleting old file: {e}")

        
        upload_dir = "static/portfolio_images"
        extension = file.filename.split(".")[-1]
        file_name = f"portfolio_{uuid4()}.{extension}"
        file_path = os.path.join(upload_dir, file_name)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        portfolio.image_url = f"/{file_path}"

    
    if data and hasattr(data, 'dict'):
        for key, value in data.dict(exclude_unset=True).items():
            setattr(portfolio, key, value)

    db.commit()
    db.refresh(portfolio)
    return portfolio

def delete_portfolio(db: Session, portfolio_id: int):
    portfolio = db.query(PortfolioImage).filter(PortfolioImage.id == portfolio_id).first()

    if not portfolio:
        return False

    
    try:
        if portfolio.image_url:
            
            actual_path = portfolio.image_url.lstrip('/')
            if os.path.exists(actual_path):
                os.remove(actual_path)
    except Exception as e:
        print(f"Warning: Could not delete file {portfolio.image_url}: {e}")

    db.delete(portfolio)
    db.commit()
    return True

def update_image_url(db: Session, image_id: int, file: UploadFile):
    image = db.query(PortfolioImage).filter(PortfolioImage.id == image_id).first()

    if not image:
        return None

    
    try:
        if image.image_url:
            old_path = image.image_url.lstrip('/')
            if os.path.exists(old_path):
                os.remove(old_path)
    except Exception as e:
        print(f"Error deleting old image: {e}")

    
    upload_dir = "static/portfolio_images"
    extension = file.filename.split(".")[-1]
    file_name = f"portfolio_{uuid4()}.{extension}"
    file_path = os.path.join(upload_dir, file_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    
    image.image_url = f"/{file_path}"

    db.commit()
    db.refresh(image)
    return image

def get_image_info(image):
    return {
        "id": image.id,
        "url": image.image_url,
        "uploaded_at": image.uploaded_at
    }

