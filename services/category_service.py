from sqlalchemy.orm import Session
from models.service_category import ServiceCategory


def create_category(db: Session, data):
    category = ServiceCategory(**data.dict())

    db.add(category)
    db.commit()
    db.refresh(category)

    return category

def get_category(db: Session, category_id: int):
    return db.query(ServiceCategory).filter(ServiceCategory.id == category_id).first()

def get_all_categories(db: Session):
    return db.query(ServiceCategory).all()

def update_category(db: Session, category_id: int, data):
    category = db.query(ServiceCategory).filter(ServiceCategory.id == category_id).first()

    if not category:
        return None

    for key, value in data.dict().items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)

    return category

def delete_category(db: Session, category_id: int):
    category = db.query(ServiceCategory).filter(ServiceCategory.id == category_id).first()

    if not category:
        return False

    db.delete(category)
    db.commit()

    return True

