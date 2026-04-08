import models
from fastapi import FastAPI
from routers import provider_router
from routers import service_router
from routers import task_router
from routers import location_router
from routers import availability_router
from routers import portfolio_router
from routers import category_router
app = FastAPI()

app.include_router(provider_router.router)
app.include_router(service_router.router)
app.include_router(task_router.router)
app.include_router(location_router.router)
app.include_router(availability_router.router)
app.include_router(portfolio_router.router)
app.include_router(category_router.router)
@app.get("/")
def root():
    return {"message": "API is working 🚀"}