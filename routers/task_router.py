from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.task import TaskCreate, TaskResponse
from services import task_service
import shutil
import os
import uuid
from models.task import Task


router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#@router.post("/", response_model=TaskResponse)
#def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    #return task_service.create_task(db, data)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = task_service.get_task(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@router.get("/", response_model=list[TaskResponse])
def get_all_tasks(db: Session = Depends(get_db)):
    return task_service.get_all_tasks(db)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, data: TaskCreate, db: Session = Depends(get_db)):
    task = task_service.update_task(db, task_id, data)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    success = task_service.delete_task(db, task_id)

    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted"}

@router.patch("/{task_id}/price")
def change_task_price(task_id: int, new_price: float, db: Session = Depends(get_db)):
    task = task_service.change_task_price(db, task_id, new_price)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@router.patch("/{task_id}/duration")
def change_duration(task_id: int, duration: int, db: Session = Depends(get_db)):
    task = task_service.change_duration(db, task_id, duration)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@router.patch("/{task_id}/mandatory")
def mark_mandatory(task_id: int, db: Session = Depends(get_db)):
    task = task_service.mark_mandatory(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@router.patch("/{task_id}/optional")
def mark_optional(task_id: int, db: Session = Depends(get_db)):
    task = task_service.mark_optional(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@router.get("/{task_id}/is-mandatory")
def is_mandatory(task_id: int, db: Session = Depends(get_db)):
    task = task_service.get_task(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "is_mandatory": task_service.is_mandatory(task)
    }

@router.patch("/{task_id}/image")
def update_task_image(
    task_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    allowed_types = ["image/jpeg", "image/png", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid image type")

    content = file.file.read()
    if len(content) > 2 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")

    file.file.seek(0)

    import uuid, os, shutil
    file_extension = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_extension}"

    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", file_name)

    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.image_url and os.path.exists(task.image_url):
        os.remove(task.image_url)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    updated_task = task_service.updateImage(db, task_id, file_path)

    return task
    

@router.delete("/{task_id}/image")
def remove_task_image(task_id: int, db: Session = Depends(get_db)):
    success = task_service.removeImage(db, task_id)

    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task image removed successfully"}

@router.get("/{task_id}/image")
def get_task_image(task_id: int, db: Session = Depends(get_db)):
    image = task_service.getImage(db, task_id)

    if not image:
        raise HTTPException(status_code=404, detail="Task not found")

    return image


