from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.provider import ProviderCreate, ProviderResponse
from services import provider_service


router = APIRouter(prefix="/providers", tags=["Providers"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProviderResponse)
def create_provider(data: ProviderCreate, db: Session = Depends(get_db)):
    provider = provider_service.create_provider(db, data)
    return provider

@router.get("/{provider_id}", response_model=ProviderResponse)
def get_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = provider_service.get_provider(db, provider_id)

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    return provider

@router.get("/", response_model=list[ProviderResponse])
def get_all_providers(db: Session = Depends(get_db)):
    return provider_service.get_all_providers(db)

@router.put("/{provider_id}", response_model=ProviderResponse)
def update_provider(provider_id: int, data: ProviderCreate, db: Session = Depends(get_db)):
    provider = provider_service.update_provider(db, provider_id, data)

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    return provider

@router.delete("/{provider_id}")
def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    success = provider_service.delete_provider(db, provider_id)

    if not success:
        raise HTTPException(status_code=404, detail="Provider not found")

    return {"message": "Provider deleted successfully"}

@router.patch("/{provider_id}/verify", response_model=ProviderResponse)
def verify_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = provider_service.verify_identity(db, provider_id)

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    return provider

@router.get("/{provider_id}/full-name")
def get_full_name(provider_id: int, db: Session = Depends(get_db)):
    provider = provider_service.get_provider(db, provider_id)

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    return {
        "full_name": provider_service.get_full_name(provider)
    }

@router.patch("/{provider_id}/profile-image")
def update_profile_image(
    provider_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    
    provider =  provider_service.update_profile_image(db, provider_id, file)

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    return provider


@router.post("/{provider_id}/portfolio")
def add_portfolio(
    provider_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    
    image = provider_service.add_portfolio_image(db, provider_id, file)
    
    
    if not image:
        
        raise HTTPException(
            status_code=404, 
            detail=f"Provider with id {provider_id} not found"
        )
    
    
    return image

@router.delete("/portfolio/{image_id}")
def remove_portfolio(image_id: int, db: Session = Depends(get_db)):
    success = provider_service.remove_portfolio_image(db, image_id)

    if not success:
        raise HTTPException(status_code=404, detail="Image not found")

    return {"message": "Image removed"}

@router.get("/{provider_id}/is-experienced")
def is_experienced(provider_id: int, db: Session = Depends(get_db)):
    provider = provider_service.get_provider(db, provider_id)

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    return {
        "is_experienced": provider_service.is_experienced(provider)
    }

@router.get("/{provider_id}/availability") # غيرت id لـ provider_id للاتساق
def read_availability(provider_id: int, db: Session = Depends(get_db)):
    provider = provider_service.get_provider(db, provider_id) # استخدم الـ service دائماً

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    return {
        "is_available": provider.is_available,
        "status_text": "Available" if provider.is_available else "Not available"
    }


@router.patch("/{provider_id}/availability") 
def update_availability(provider_id: int, status: bool, db: Session = Depends(get_db)):
    provider = provider_service.set_availability(db, provider_id, status)

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    return {
        "is_available": provider.is_available,
        "status_text": "Available" if provider.is_available else "Not available"
    }


#****** # الدالة هاذي عندها علاقة مع القروب تاع دوموندار ****
#@router.get("/{provider_id}/negotiations")
#def get_negotiations(provider_id: int, db: Session = Depends(get_db)):
   # return provider_service.get_provider_negotiations(db, provider_id)

# @router.put(
#     "/{provider_id}/demandes/{demande_id}/negotiation",
#     response_model=NegotiationResponse
# )
# def respond_negotiation(
#     provider_id: int,
#     demande_id: int,
#     data: NegotiationStatusUpdate,
#     db: Session = Depends(get_db)
# ):
#     return provider_service.provider_respond_negotiation(
#         db,
#         demande_id,
#         provider_id,
#         data
#     )