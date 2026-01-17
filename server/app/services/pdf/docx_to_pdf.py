"""
DOCX to PDF Conversion Service

Converts Microsoft Word documents to PDF.

Senior Dev Tip: DOCX conversion is complex because we need to preserve
formatting. For production, consider using LibreOffice or similar tools.
This is a simplified implementation for learning purposes.
"""

from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
import logging

logger = logging.getLogger(__name__)


def convert_docx_to_pdf(input_path: str, output_path: str) -> str:
    """
    Convert a DOCX file to PDF.
    
    Senior Dev Tip: This is a basic implementation. For production apps,
    you might want to use:
    - LibreOffice headless mode (better formatting preservation)
    - Cloud services like CloudConvert API
    - Commercial libraries like Aspose
    
    Args:
        input_path: Path to input DOCX file
        output_path: Path where PDF should be saved
        
    Returns:
        Path to generated PDF file
        
    Raises:
        Exception: If conversion fails
    """
    try:
        # Read DOCX document
        doc = Document(input_path)
        
        # Create PDF
        pdf = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Container for PDF elements
        story = []
        
        # Get default styles
        styles = getSampleStyleSheet()
        normal_style = styles['Normal']
        
        # Process each paragraph in the DOCX
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():  # Skip empty paragraphs
                # Create paragraph for PDF
                p = Paragraph(paragraph.text, normal_style)
                story.append(p)
                story.append(Spacer(1, 0.2 * inch))  # Add spacing
        
        # Build PDF
        pdf.build(story)
        
        logger.info(f"Successfully converted DOCX to PDF: {output_path}")
        return output_path
    
    except Exception as e:
        logger.error(f"Error converting DOCX to PDF: {e}")
        raise Exception(f"DOCX to PDF conversion failed: {str(e)}")
