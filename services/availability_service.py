from sqlalchemy.orm import Session
from models.availability import Availability


def create_availability(db: Session, data):
    availability = Availability(**data.dict())

    db.add(availability)
    db.commit()
    db.refresh(availability)

    return availability

def get_availability(db: Session, availability_id: int):
    return db.query(Availability).filter(Availability.id == availability_id).first()

def get_all_availability(db: Session):
    return db.query(Availability).all()

def update_availability(db: Session, availability_id: int, data):
    availability = db.query(Availability).filter(Availability.id == availability_id).first()

    if not availability:
        return None

    for key, value in data.dict().items():
        setattr(availability, key, value)

    db.commit()
    db.refresh(availability)

    return availability

def delete_availability(db: Session, availability_id: int):
    availability = db.query(Availability).filter(Availability.id == availability_id).first()

    if not availability:
        return False

    db.delete(availability)
    db.commit()

    return True

def change_time_slot(db, availability_id, start, end):
    availability = db.query(Availability).filter(Availability.id == availability_id).first()

    if not availability:
        return None

    availability.start_time = start
    availability.end_time = end

    db.commit()
    db.refresh(availability)
    return availability

def mark_available(db, availability_id):
    availability = db.query(Availability).filter(Availability.id == availability_id).first()

    if not availability:
        return None

    availability.is_available = True

    db.commit()
    db.refresh(availability)
    return availability

def mark_unavailable(db, availability_id):
    availability = db.query(Availability).filter(Availability.id == availability_id).first()

    if not availability:
        return None

    availability.is_available = False

    db.commit()
    db.refresh(availability)
    return availability

def is_within_working_hours(availability, time):
    return availability.start_time <= time <= availability.end_time

def is_available_at(availability, time):
    if not availability.is_available:
        return False
    return availability.start_time <= time <= availability.end_time

def overlaps_with(a1, a2):
    return not (a1.end_time <= a2.start_time or a2.end_time <= a1.start_time)



