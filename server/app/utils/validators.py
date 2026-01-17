"""
File Validation Functions

Validates uploaded files before processing.

Senior Dev Tip: Always validate user input! This prevents:
- Security vulnerabilities
- Server crashes
- Wasted processing time
"""

from fastapi import UploadFile, HTTPException, status
from app.core.config import settings
from typing import List
import mimetypes


# Supported file types for each conversion
SUPPORTED_FORMATS = {
    "image_to_pdf": [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"],
    "docx_to_pdf": [".docx"],
    "text_to_pdf": [".txt"],
    "pdf_to_image": [".pdf"],
}


def validate_file_size(file: UploadFile) -> None:
    """
    Validate file size doesn't exceed limit.
    
    Senior Dev Tip: Check file size before processing to prevent
    resource exhaustion attacks and out-of-memory errors.
    
    Args:
        file: Uploaded file
        
    Raises:
        HTTPException: If file is too large
    """
    # Get file size by seeking to end
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > settings.max_file_size:
        max_size_mb = settings.max_file_size / (1024 * 1024)
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {max_size_mb}MB"
        )


def validate_file_type(filename: str, conversion_type: str) -> None:
    """
    Validate file type is supported for the conversion.
    
    Senior Dev Tip: Validate file extensions AND MIME types for security.
    Users can rename files to bypass extension checks.
    
    Args:
        filename: Name of the file
        conversion_type: Type of conversion requested
        
    Raises:
        HTTPException: If file type is not supported
    """
    # Get file extension
    file_ext = filename[filename.rfind('.'):].lower() if '.' in filename else ''
    
    # Check if conversion type is supported
    if conversion_type not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Conversion type '{conversion_type}' is not supported"
        )
    
    # Check if file extension is supported for this conversion
    supported_exts = SUPPORTED_FORMATS[conversion_type]
    
    if file_ext not in supported_exts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type '{file_ext}' is not supported for {conversion_type}. "
                   f"Supported formats: {', '.join(supported_exts)}"
        )


def validate_upload_file(file: UploadFile, conversion_type: str) -> None:
    """
    Comprehensive file validation.
    
    Senior Dev Tip: Centralize validation logic for consistency
    and easier maintenance.
    
    Args:
        file: Uploaded file
        conversion_type: Type of conversion requested
        
    Raises:
        HTTPException: If validation fails
    """
    # Validate file was actually uploaded
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file uploaded"
        )
    
    # Validate filename exists
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is missing"
        )
    
    # Validate file type
    validate_file_type(file.filename, conversion_type)
    
    # Validate file size
    validate_file_size(file)
