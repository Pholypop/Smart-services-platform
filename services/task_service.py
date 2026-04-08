from sqlalchemy.orm import Session
from models.task import Task


def create_task(db: Session, data):
    task = Task(**data.dict())

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def get_all_tasks(db: Session):
    return db.query(Task).all()

def update_task(db: Session, task_id: int, data):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return None

    for key, value in data.dict().items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task

def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return False

    db.delete(task)
    db.commit()

    return True

def change_task_price(db, task_id, new_price):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return None

    task.price = new_price

    db.commit()
    db.refresh(task)
    return task

def change_duration(db, task_id, duration):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return None

    task.duration = duration

    db.commit()
    db.refresh(task)
    return task

def mark_mandatory(db, task_id): #*******اجباري
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return None

    task.mandatory = True

    db.commit()
    db.refresh(task)
    return task

def mark_optional(db, task_id):  #خياري
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return None

    task.mandatory = False

    db.commit()
    db.refresh(task)
    return task

def is_mandatory(task):
    return task.mandatory
