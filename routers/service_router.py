from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.service import ServiceCreate, ServiceResponse
from services import service_service
from fastapi import UploadFile, File
import shutil
import os
import uuid
from models.service import ServiceStatus
from schemas.task import TaskCreate


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

#@router.patch("/{service_id}/publish")
#def publish(service_id: int, db: Session = Depends(get_db)):
    return service_service.publish_service(db, service_id)

@router.patch("/{service_id}/unpublish")
def unpublish(service_id: int, db: Session = Depends(get_db)):
    return service_service.unpublish_service(db, service_id)

@router.patch("/{service_id}/deactivate")
def deactivate(service_id: int, db: Session = Depends(get_db)):
    return service_service.deactivate_service(db, service_id)

@router.patch("/{service_id}/status")
def change_status(
    service_id: int,
    status: ServiceStatus,
    db: Session = Depends(get_db)
):
    return service_service.change_status(db, service_id, status)

@router.post("/{service_id}/tasks")
def add_task(service_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    return service_service.add_task_to_service(db, service_id, task.dict())

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

@router.patch("/{service_id}/image")
def update_service_image(
    service_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 📌 التحقق من نوع الملف
    allowed_types = ["image/jpeg", "image/png", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid image type")

    # 📌 قراءة الملف للتحقق من الحجم
    content = file.file.read()
    if len(content) > 2 * 1024 * 1024:  # 2MB
        raise HTTPException(status_code=400, detail="File too large")

    # إعادة المؤشر للبداية
    file.file.seek(0)

    # 📌 إنشاء اسم عشوائي
    import uuid, os, shutil
    file_extension = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_extension}"

    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", file_name)

    # 📌 حذف الصورة القديمة (إن وجدت)
    service = service_service.get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    if service.image_url and os.path.exists(service.image_url):
        os.remove(service.image_url)

    # 📌 حفظ الصورة الجديدة
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 📌 تحديث DB
    updated_service = service_service.updateServiceImage(db, service_id, file_path)

    return updated_service

@router.delete("/{service_id}/image")
def remove_service_image(service_id: int, db: Session = Depends(get_db)):
    return service_service.removeServiceImage(db, service_id)

@router.get("/{service_id}/image")
def get_service_image(service_id: int, db: Session = Depends(get_db)):
    return service_service.getServiceImage(db, service_id)



