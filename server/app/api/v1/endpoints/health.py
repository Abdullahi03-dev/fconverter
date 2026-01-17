
from fastapi import APIRouter
from datetime import datetime
from app.core.config import settings
import os

router = APIRouter()


@router.get("")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.app_version,
        "upload_dir_exists": os.path.exists(settings.upload_dir),
        "output_dir_exists": os.path.exists(settings.output_dir),
    }
