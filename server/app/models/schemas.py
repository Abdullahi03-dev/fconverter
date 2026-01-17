"""
Pydantic Schemas for Request/Response Validation

Senior Dev Tip: Pydantic schemas provide:
- Automatic validation
- Type safety
- API documentation (shows up in Swagger)
- Serialization/deserialization
- Clear contracts between frontend and backend
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from enum import Enum


class ConversionType(str, Enum):
    """
    Supported conversion types.
    
    Senior Dev Tip: Using Enum ensures type safety and provides
    auto-complete in IDEs and clear API documentation.
    """
    IMAGE_TO_PDF = "image_to_pdf"
    DOCX_TO_PDF = "docx_to_pdf"
    TEXT_TO_PDF = "text_to_pdf"
    PDF_TO_IMAGE = "pdf_to_image"
    # Future conversions can be added here


class ConversionRequest(BaseModel):
    """
    Request schema for file conversion.
    
    This is what the frontend will send to the backend.
    """
    conversion_type: ConversionType = Field(
        ...,
        description="Type of conversion to perform"
    )
    filename: str = Field(
        ...,
        description="Original filename"
    )
    
    class Config:
        # This allows the schema to be used in Swagger UI examples
        json_schema_extra = {
            "example": {
                "conversion_type": "image_to_pdf",
                "filename": "photo.jpg"
            }
        }


class ConversionResponse(BaseModel):
    """
    Response schema for successful conversion.
    
    This is what the backend sends back to the frontend.
    """
    success: bool = Field(default=True, description="Conversion status")
    message: str = Field(..., description="Status message")
    output_filename: str = Field(..., description="Generated file name")
    download_url: str = Field(..., description="URL to download the file")
    file_size: int = Field(..., description="Output file size in bytes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Conversion completed successfully",
                "output_filename": "photo.pdf",
                "download_url": "/api/v1/download/photo.pdf",
                "file_size": 245678
            }
        }


class ErrorResponse(BaseModel):
    """
    Error response schema.
    
    Senior Dev Tip: Consistent error responses make frontend
    error handling much easier.
    """
    success: bool = Field(default=False)
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    detail: Optional[str] = Field(None, description="Additional error details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "InvalidFileType",
                "message": "File type not supported",
                "detail": "Only JPG, PNG files are supported for image_to_pdf"
            }
        }
