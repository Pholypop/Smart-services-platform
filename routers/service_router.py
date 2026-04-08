from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.service import ServiceCreate, ServiceResponse
from services import service_service

router = APIRouter(prefix="/services", tags=["Services"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ServiceResponse)
def create_service(data: ServiceCreate, db: Session = Depends(get_db)):
    service = service_service.create_service(db, data)
    return service

@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = service_service.get_service(db, service_id)

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return service

@router.get("/", response_model=list[ServiceResponse])
def get_all_services(db: Session = Depends(get_db)):
    return service_service.get_all_services(db)

@router.put("/{service_id}", response_model=ServiceResponse)
def update_service(service_id: int, data: ServiceCreate, db: Session = Depends(get_db)):
    service = service_service.update_service(db, service_id, data)

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return service

@router.delete("/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    success = service_service.delete_service(db, service_id)

    if not success:
        raise HTTPException(status_code=404, detail="Service not found")

    return {"message": "Service deleted"}

@router.patch("/{service_id}/publish", response_model=ServiceResponse)
def publish_service(service_id: int, db: Session = Depends(get_db)):
    service = service_service.publish_service(db, service_id)

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return service

@router.patch("/{service_id}/change-price")
def change_price(service_id: int, new_price: float, db: Session = Depends(get_db)):
    service = service_service.change_price(db, service_id, new_price)

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return service

@router.get("/{service_id}/total-price")
def get_total_price(service_id: int, db: Session = Depends(get_db)):
    service = service_service.get_service(db, service_id)

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    total = service_service.calculate_total_price(service)

    return {"total_price": total}

@router.patch("/{service_id}/publish")
def publish(service_id: int, db: Session = Depends(get_db)):
    return service_service.publish_service(db, service_id)

@router.patch("/{service_id}/unpublish")
def unpublish(service_id: int, db: Session = Depends(get_db)):
    return service_service.unpublish_service(db, service_id)

@router.patch("/{service_id}/deactivate")
def deactivate(service_id: int, db: Session = Depends(get_db)):
    return service_service.deactivate_service(db, service_id)

@router.patch("/{service_id}/status")
def change_status(service_id: int, status: str, db: Session = Depends(get_db)):
    return service_service.change_status(db, service_id, status)

@router.post("/{service_id}/tasks")
def add_task(service_id: int, task: dict, db: Session = Depends(get_db)):
    return service_service.add_task_to_service(db, service_id, task)

@router.delete("/tasks/{task_id}")
def remove_task(task_id: int, db: Session = Depends(get_db)):
    success = service_service.remove_task_from_service(db, task_id)

    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task removed"}

@router.patch("/{service_id}/category")
def change_category(service_id: int, category_id: int, db: Session = Depends(get_db)):
    return service_service.change_category(db, service_id, category_id)

@router.get("/{service_id}/is-published")
def is_published(service_id: int, db: Session = Depends(get_db)):
    service = service_service.get_service(db, service_id)

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return {"is_published": service_service.is_published(service)}

@router.get("/{service_id}/is-in-category")
def is_in_category(service_id: int, category_id: int, db: Session = Depends(get_db)):
    service = service_service.get_service(db, service_id)

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return {
        "is_in_category": service_service.is_in_category(service, category_id)
    }



