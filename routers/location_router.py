from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.location import LocationCreate, LocationResponse
from services import location_service

router = APIRouter(prefix="/locations", tags=["Locations"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=LocationResponse)
def create_location(data: LocationCreate, db: Session = Depends(get_db)):
    return location_service.create_location(db, data)

@router.get("/{location_id}", response_model=LocationResponse)
def get_location(location_id: int, db: Session = Depends(get_db)):
    location = location_service.get_location(db, location_id)

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    return location

@router.get("/", response_model=list[LocationResponse])
def get_all_locations(db: Session = Depends(get_db)):
    return location_service.get_all_locations(db)

@router.put("/{location_id}", response_model=LocationResponse)
def update_location(location_id: int, data: LocationCreate, db: Session = Depends(get_db)):
    location = location_service.update_location(db, location_id, data)

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    return location

@router.delete("/{location_id}")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    success = location_service.delete_location(db, location_id)

    if not success:
        raise HTTPException(status_code=404, detail="Location not found")

    return {"message": "Location deleted"}

@router.patch("/{location_id}/address")
def change_address(location_id: int, address: str, db: Session = Depends(get_db)):
    location = location_service.change_address(db, location_id, address)

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    return location

@router.get("/{location_id}/full")
def get_full_location(location_id: int, db: Session = Depends(get_db)):
    location = location_service.get_location(db, location_id)

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    return {
        "full_location": location_service.get_full_location(location)
    }



