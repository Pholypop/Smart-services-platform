from models.provider import Provider
from schemas.provider import ProviderCreate
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload


def create_provider(db: Session, data: ProviderCreate):
    provider = Provider(**data.dict())

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

    for key, value in data.dict().items():
        setattr(provider, key, value)

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

def update_profile_image(db, provider_id, image_url):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        return None

    provider.profile_image_url = image_url

    db.commit()
    db.refresh(provider)
    return provider

def add_portfolio_image(db, provider_id, image_url):
    image = PortfolioImage(provider_id=provider_id, image_url=image_url)

    db.add(image)
    db.commit()
    db.refresh(image)

    return image

def remove_portfolio_image(db, image_id):
    image = db.query(PortfolioImage).filter(PortfolioImage.id == image_id).first()

    if not image:
        return False

    db.delete(image)
    db.commit()
    return True

def is_experienced(provider, min_years=3):
    return (provider.experience_years or 0) >= min_years



