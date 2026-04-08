from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.servicecategory import CategoryCreate, CategoryResponse
from services import category_service

router = APIRouter(prefix="/categories", tags=["Categories"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CategoryResponse)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    return category_service.create_category(db, data)

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = category_service.get_category(db, category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category

@router.get("/", response_model=list[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):
    return category_service.get_all_categories(db)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, data: CategoryCreate, db: Session = Depends(get_db)):
    category = category_service.update_category(db, category_id, data)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    success = category_service.delete_category(db, category_id)

    if not success:
        raise HTTPException(status_code=404, detail="Category not found")

    return {"message": "Category deleted"}


