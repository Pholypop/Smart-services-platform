from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from database import SessionLocal, engine, Base
from models.provider import Provider
from models.portfolio import PortfolioImage
from models.service import Service
from models.task import Task
from models.location import Location
from models.service_category import ServiceCategory
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request


from routers import (
    provider_router, service_router, task_router, 
    location_router, portfolio_router, category_router
)




Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],  

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(provider_router.router)
app.include_router(service_router.router)
app.include_router(task_router.router)
app.include_router(location_router.router)
app.include_router(portfolio_router.router)
app.include_router(category_router.router)


@app.get("/")
def root():
    return {"message": "API is working 🚀"}

