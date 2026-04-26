from models.provider import Provider
from schemas.provider import ProviderCreate
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
#from models.demande import Demande, Negotiation, DemandeStatus, NegotiationStatus 
from datetime import datetime
from models.service_category import ServiceCategory
from models.portfolio import PortfolioImage
from fastapi import HTTPException
import os
import shutil
from uuid import uuid4
from fastapi import UploadFile




def create_provider(db: Session, data: ProviderCreate):
    # 1. استخراج الـ IDs قبل تحويل البيانات لـ Model
    category_ids = data.category_ids
    
    # 2. تحويل البيانات لموديل مع استثناء الـ IDs الخاصة بالأصناف
    # لأنها غير موجودة في جدول الـ Provider نفسه
    provider_data = data.dict(exclude={'category_ids'})
    provider = Provider(**provider_data)

    # 3. جلب كائنات الأصناف من قاعدة البيانات وربطها بالمزود
    if category_ids:
        db_categories = db.query(ServiceCategory).filter(ServiceCategory.id.in_(category_ids)).all()
        provider.categories = db_categories  # SQLAlchemy سيهتم بملء الجدول الوسيط تلقائياً

    db.add(provider)
    db.commit()
    db.refresh(provider)

    return provider

def get_provider(db: Session, provider_id: int):
    return (
        db.query(Provider)
        .options(joinedload(Provider.services))  # 🔥 مهم
        .filter(Provider.id == provider_id)
        .first()
    )

def get_all_providers(db: Session):
    return db.query(Provider).all()

def update_provider(db: Session, provider_id: int, data: ProviderCreate):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()

    if not provider:
        return None
    
    update_data = data.dict(exclude_unset=True, exclude={'category_ids'})

    # تحديث الحقول العادية
    for key, value in data.dict(exclude={'category_ids'}).items():
        setattr(provider, key, value)

    # تحديث الأصناف (ManyToMany Update)
    if data.category_ids is not None:
        db_categories = db.query(ServiceCategory).filter(ServiceCategory.id.in_(data.category_ids)).all()
        provider.categories = db_categories

    db.commit()
    db.refresh(provider)

    return provider

def delete_provider(db: Session, provider_id: int):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()

    if not provider:
        return False

    db.delete(provider)
    db.commit()

    return True

def verify_identity(db: Session, provider_id: int):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()

    if not provider:
        return None

    provider.is_verified = True

    db.commit()
    db.refresh(provider)

    return provider

def get_full_name(provider):
    return f"{provider.first_name} {provider.last_name}"

def update_profile_image(db, provider_id, file: UploadFile):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        return None

    
    upload_dir = "static/profile_images"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    
    extension = file.filename.split(".")[-1]
    file_name = f"{uuid4()}.{extension}"
    file_path = os.path.join(upload_dir, file_name)

    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    
    
    provider.profile_image_url = f"/static/profile_images/{file_name}"

    db.commit()
    db.refresh(provider)
    return provider
 
 

def add_portfolio_image(db, provider_id, file: UploadFile):

    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        return None
    
    upload_dir = "static/portfolio_images"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    
    extension = file.filename.split(".")[-1]
    file_name = f"portfolio_{uuid4()}.{extension}"
    file_path = os.path.join(upload_dir, file_name)

    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    
    image_url = f"/{file_path}" 
    image = PortfolioImage(provider_id=provider_id, image_url=image_url)

    db.add(image)
    db.commit()
    db.refresh(image)

    return image

def remove_portfolio_image(db, image_id):
    
    image = db.query(PortfolioImage).filter(PortfolioImage.id == image_id).first()

    if not image:
        return False

    try:
        
        
        if image.image_url:
            
            file_path = image.image_url.lstrip('/') 
            if os.path.exists(file_path):
                os.remove(file_path)

        
        db.delete(image)
        db.commit()
        return True

    except Exception as e:
        print(f"Error deleting file: {e}")
        
        db.rollback()
        return False

def is_experienced(provider, min_years=3):
    return (provider.experience_years or 0) >= min_years

def set_availability(db, provider_id: int, status: bool):  
    provider = db.get(Provider, provider_id)  

    if not provider:
        
     raise HTTPException(status_code=404, detail="Provider not found")
    
    provider.is_available = status
    db.commit()
    return provider

def get_availability(db, provider_id: int):
    provider = db.get(Provider, provider_id)
    return provider.is_available


   # هاذو الدوال عندهم علاقة مع جماعة demand****************************
#def get_provider_negotiations(db: Session, provider_id: int):
    
   
    
    return (
        db.query(Demande)
        .options(
            joinedload(Demande.tasks),
            joinedload(Demande.negotiation)
        )
        .filter(
            Demande.provider_id == provider_id,
            Demande.negotiation != None
        )
        .order_by(Demande.created_at.desc())
        .all()
    ) 

#def provider_respond_negotiation(db: Session, demande_id: int, provider_id: int, data):
    
   

    demande = (
        db.query(Demande)
        .filter(
            Demande.id == demande_id,
            Demande.provider_id == provider_id
        )
        .first()
    )

    if not demande:
        raise ValueError("الطلب غير موجود أو لا يخص هذا provider")

    nego = demande.negotiation

    if not nego:
        raise ValueError("لا توجد مفاوضة على هذا الطلب")

    # قبول
    if data.status == NegotiationStatus.ACCEPTED:
        nego.status = NegotiationStatus.ACCEPTED
        demande.status = DemandeStatus.ACCEPTED

    # رفض
    elif data.status == NegotiationStatus.REJECTED:
        nego.status = NegotiationStatus.REJECTED
        demande.status = DemandeStatus.REJECTED

    # Counter offer
    elif data.status == NegotiationStatus.COUNTER:
        if data.counter_budget is None:
            raise ValueError("يجب إرسال counter_budget")

        nego.counter_budget = data.counter_budget
        nego.counter_message = data.counter_message
        nego.status = NegotiationStatus.COUNTER

        demande.status = DemandeStatus.NEGOTIATING

    nego.updated_at = datetime.utcnow()
    demande.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(nego)

    return nego




