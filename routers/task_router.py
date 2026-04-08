from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.task import TaskCreate, TaskResponse
from services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TaskResponse)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db, data)

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
