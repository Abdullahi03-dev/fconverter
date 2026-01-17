from fastapi import APIRouter
from app.api.v1.endpoints import health, convert

# Create the main API router for v1
api_router = APIRouter()

api_router.include_router(
    health.router,
    prefix="/health",
    tags=["Health"]
)

api_router.include_router(
    convert.router,
    prefix="/convert",
    tags=["Conversion"]
)
