from sqlalchemy.orm import Session
from models.service import Service
from sqlalchemy.orm import joinedload
from models.service import Service
from models.service import ServiceStatus

def create_service(db: Session, data):
    service = Service(**data.dict())

    db.add(service)
    db.commit()
    db.refresh(service)

    return service


def get_service(db: Session, service_id: int):
    return (
        db.query(Service)
        .options(joinedload(Service.tasks))  # 🔥 Nested
        .filter(Service.id == service_id)
        .first()
    )

def get_all_services(db: Session):
    return db.query(Service).all()

def update_service(db: Session, service_id: int, data):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        return None

    for key, value in data.dict().items():
        setattr(service, key, value)

    db.commit()
    db.refresh(service)

    return service

def delete_service(db: Session, service_id: int):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        return False

    db.delete(service)
    db.commit()

    return True


def publish_service(db: Session, service_id: int):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        return None

    service.status = ServiceStatus.PUBLISHED

    db.commit()
    db.refresh(service)

    return service

def unpublish_service(db, service_id):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        return None

    service.status = ServiceStatus.DRAFT

    db.commit()
    db.refresh(service)
    return service

def deactivate_service(db, service_id):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        return None

    service.is_active = False

    db.commit()
    db.refresh(service)
    return service

def is_published(service):
    return service.status == ServiceStatus.PUBLISHED

def change_status(db, service_id, new_status):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        return None

    service.status = new_status

    db.commit()
    db.refresh(service)
    return service

def add_task_to_service(db, service_id, task_data):
    task = Task(**task_data, service_id=service_id)

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

def remove_task_from_service(db, task_id):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return False

    db.delete(task)
    db.commit()
    return True

def change_category(db, service_id, category_id):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        return None

    service.category_id = category_id

    db.commit()
    db.refresh(service)
    return service

def is_in_category(service, category_id):
    return service.category_id == category_id

def change_price(db, service_id, new_price):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        return None

    service.price = new_price

    db.commit()
    db.refresh(service)

    return service

def calculate_total_price(service):
    total = service.price or 0

    for task in service.tasks:
        if task.price:
            total += task.price

    return total




