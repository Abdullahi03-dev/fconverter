"""
Image to PDF Conversion Service

Converts various image formats to PDF.

Senior Dev Tip: Separating business logic into service modules
keeps your endpoints clean and makes testing easier.
"""

from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import ImageReader
import os
import logging

logger = logging.getLogger(__name__)


def convert_image_to_pdf(input_path: str, output_path: str) -> str:
    """
    Convert an image file to PDF.
    
    Senior Dev Tip: This function handles the actual conversion logic.
    It's pure business logic - no HTTP concerns, making it testable.
    
    Args:
        input_path: Path to input image file
        output_path: Path where PDF should be saved
        
    Returns:
        Path to generated PDF file
        
    Raises:
        Exception: If conversion fails
    """
    try:
        # Open the image
        img = Image.open(input_path)
        
        # Convert RGBA to RGB if necessary (PDFs don't support transparency)
        if img.mode == 'RGBA':
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get image dimensions
        img_width, img_height = img.size
        
        # Calculate PDF page size to fit image
        # Senior Dev Tip: Maintain aspect ratio for better output
        aspect_ratio = img_height / img_width
        
        # Use A4 size as base, adjust to fit image
        page_width = 595  # A4 width in points
        page_height = page_width * aspect_ratio
        
        # Create PDF
        c = canvas.Canvas(output_path, pagesize=(page_width, page_height))
        
        # Draw image on PDF (fill entire page)
        c.drawImage(
            input_path,
            0, 0,
            width=page_width,
            height=page_height,
            preserveAspectRatio=True
        )
        
        # Save PDF
        c.save()
        
        logger.info(f"Successfully converted image to PDF: {output_path}")
        return output_path
    
    except Exception as e:
        logger.error(f"Error converting image to PDF: {e}")
        raise Exception(f"Image to PDF conversion failed: {str(e)}")
