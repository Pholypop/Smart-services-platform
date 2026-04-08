from sqlalchemy.orm import Session
from models.location import Location


def create_location(db: Session, data):
    location = Location(**data.dict())

    db.add(location)
    db.commit()
    db.refresh(location)

    return location

def get_location(db: Session, location_id: int):
    return db.query(Location).filter(Location.id == location_id).first()

def get_all_locations(db: Session):
    return db.query(Location).all()

def update_location(db: Session, location_id: int, data):
    location = db.query(Location).filter(Location.id == location_id).first()

    if not location:
        return None

    for key, value in data.dict().items():
        setattr(location, key, value)

    db.commit()
    db.refresh(location)

    return location

def delete_location(db: Session, location_id: int):
    location = db.query(Location).filter(Location.id == location_id).first()

    if not location:
        return False

    db.delete(location)
    db.commit()

    return True

def change_address(db, location_id, address):
    location = db.query(Location).filter(Location.id == location_id).first()

    if not location:
        return None

    location.address = address

    db.commit()
    db.refresh(location)
    return location

def get_full_location(location):
    return f"{location.city}, {location.region}, {location.address}"

