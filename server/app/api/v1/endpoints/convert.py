from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import FileResponse
from app.models.schemas import ConversionResponse, ConversionType
from app.utils.validators import validate_upload_file
from app.utils.file_utils import (
    save_upload_file,
    generate_unique_filename,
    get_file_size,
    delete_file
)
from app.services.pdf.image_to_pdf import convert_image_to_pdf
from app.services.pdf.docx_to_pdf import convert_docx_to_pdf
from app.services.pdf.text_to_pdf import convert_text_to_pdf
from app.core.config import settings
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("", response_model=ConversionResponse)
async def convert_file(
    file: UploadFile = File(..., description="File to convert"),
    conversion_type: ConversionType = Form(..., description="Type of conversion")
):  
    # Validate the uploaded file
    validate_upload_file(file, conversion_type.value)
    
    # Generate unique filenames
    input_filename = generate_unique_filename(file.filename)
    input_path = os.path.join(settings.upload_dir, input_filename)
    
    # Determine output extension based on conversion type
    if "to_pdf" in conversion_type.value:
        output_ext = ".pdf"
    elif conversion_type == ConversionType.PDF_TO_IMAGE:
        output_ext = ".png"
    else:
        output_ext = ".pdf" 
    
    output_filename = generate_unique_filename(file.filename, output_ext)
    output_path = os.path.join(settings.output_dir, output_filename)
    
    try:
        # Save uploaded file
        await save_upload_file(file, input_path)
        logger.info(f"File uploaded: {input_filename}")
        
        if conversion_type == ConversionType.IMAGE_TO_PDF:
            convert_image_to_pdf(input_path, output_path)
            
        elif conversion_type == ConversionType.DOCX_TO_PDF:
            convert_docx_to_pdf(input_path, output_path)
            
        elif conversion_type == ConversionType.TEXT_TO_PDF:
            convert_text_to_pdf(input_path, output_path)
            
        elif conversion_type == ConversionType.PDF_TO_IMAGE:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="PDF to image conversion coming soon!"
            )
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported conversion type: {conversion_type}"
            )
        
        # Get output file size
        file_size = get_file_size(output_path)
        
        # Return response
        return ConversionResponse(
            success=True,
            message="Conversion completed successfully",
            output_filename=output_filename,
            download_url=f"/api/v1/convert/download/{output_filename}",
            file_size=file_size
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Conversion failed: {str(e)}"
        )
    
    finally:
        # Clean up uploaded file
        # Senior Dev Tip: Always clean up temporary files
        # Use finally to ensure it happens even if errors occur
        delete_file(input_path)


@router.get("/download/{filename}")
async def download_file(filename: str):

    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid filename"
        )
    
    file_path = os.path.join(settings.output_dir, filename)
    
    # Check if file exists
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Return file
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )
