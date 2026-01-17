from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.config import settings
from app.api.v1.router import api_router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create FastAPI app instance
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A powerful file converter API supporting multiple formats",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc UI
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with user-friendly messages"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "detail": exc.errors(),
            "message": "Please check your request data"
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Something went wrong. Please try again later."
        }
    )


# Startup Event
@app.on_event("startup")
async def startup_event():
    """
    Runs when the server starts.
    
    Senior Dev Tip: Use this for:
    - Database connections
    - Cache initialization
    - Background task setup
    """
    # logger.info(f" {settings.app_name} v{settings.app_version} starting...")
    # logger.info(f" Upload directory: {settings.upload_dir}")
    # logger.info(f" Output directory: {settings.output_dir}")
    # logger.info(f"📏 Max file size: {settings.max_file_size / (1024*1024)}MB")


# Shutdown Event
@app.on_event("shutdown")
async def shutdown_event():
    pass
    # logger.info(" Shutting down gracefully...")


# Include API Router
app.include_router(api_router, prefix="/api/v1")


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/api/v1/health"
    }
