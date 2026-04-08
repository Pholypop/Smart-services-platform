from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.availability import AvailabilityCreate, AvailabilityResponse
from services import availability_service

router = APIRouter(prefix="/availability", tags=["Availability"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AvailabilityResponse)
def create_availability(data: AvailabilityCreate, db: Session = Depends(get_db)):
    return availability_service.create_availability(db, data)

@router.get("/{availability_id}", response_model=AvailabilityResponse)
def get_availability(availability_id: int, db: Session = Depends(get_db)):
    availability = availability_service.get_availability(db, availability_id)

    if not availability:
        raise HTTPException(status_code=404, detail="Availability not found")

    return availability

@router.get("/", response_model=list[AvailabilityResponse])
def get_all_availability(db: Session = Depends(get_db)):
    return availability_service.get_all_availability(db)

@router.put("/{availability_id}", response_model=AvailabilityResponse)
def update_availability(availability_id: int, data: AvailabilityCreate, db: Session = Depends(get_db)):
    availability = availability_service.update_availability(db, availability_id, data)

    if not availability:
        raise HTTPException(status_code=404, detail="Availability not found")

    return availability

@router.delete("/{availability_id}")
def delete_availability(availability_id: int, db: Session = Depends(get_db)):
    success = availability_service.delete_availability(db, availability_id)

    if not success:
        raise HTTPException(status_code=404, detail="Availability not found")

    return {"message": "Availability deleted"}

@router.patch("/{availability_id}/time-slot")
def change_time_slot(
    availability_id: int,
    start_time: str,
    end_time: str,
    db: Session = Depends(get_db)
):
    from datetime import time

    start = time.fromisoformat(start_time)
    end = time.fromisoformat(end_time)

    availability = availability_service.change_time_slot(db, availability_id, start, end)

    if not availability:
        raise HTTPException(status_code=404, detail="Availability not found")

    return availability

@router.patch("/{availability_id}/available")
def mark_available(availability_id: int, db: Session = Depends(get_db)):
    availability = availability_service.mark_available(db, availability_id)

    if not availability:
        raise HTTPException(status_code=404, detail="Availability not found")

    return availability

@router.patch("/{availability_id}/unavailable")
def mark_unavailable(availability_id: int, db: Session = Depends(get_db)):
    availability = availability_service.mark_unavailable(db, availability_id)

    if not availability:
        raise HTTPException(status_code=404, detail="Availability not found")

    return availability

@router.get("/{availability_id}/within-hours")
def is_within_hours(availability_id: int, time_str: str, db: Session = Depends(get_db)):
    from datetime import time

    availability = availability_service.get_availability(db, availability_id)

    if not availability:
        raise HTTPException(status_code=404, detail="Availability not found")

    t = time.fromisoformat(time_str)

    return {
        "within_hours": availability_service.is_within_working_hours(availability, t)
    }

@router.get("/{availability_id}/is-available")
def is_available_at(availability_id: int, time_str: str, db: Session = Depends(get_db)):
    from datetime import time

    availability = availability_service.get_availability(db, availability_id)

    if not availability:
        raise HTTPException(status_code=404, detail="Availability not found")

    t = time.fromisoformat(time_str)

    return {
        "is_available": availability_service.is_available_at(availability, t)
    }

@router.get("/{availability_id}/overlaps")
def overlaps_with(
    availability_id: int,
    other_id: int,
    db: Session = Depends(get_db)
):
    a1 = availability_service.get_availability(db, availability_id)
    a2 = availability_service.get_availability(db, other_id)

    if not a1 or not a2:
        raise HTTPException(status_code=404, detail="Availability not found")

    return {
        "overlaps": availability_service.overlaps_with(a1, a2)
    }


