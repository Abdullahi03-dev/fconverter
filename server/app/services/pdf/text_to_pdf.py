"""
Text to PDF Conversion Service

Converts plain text files to PDF.

Senior Dev Tip: This is one of the simpler conversions, but we still
need to handle encoding, line wrapping, and formatting properly.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
import logging

logger = logging.getLogger(__name__)


def convert_text_to_pdf(input_path: str, output_path: str) -> str:
    """
    Convert a text file to PDF.
    
    Senior Dev Tip: Handle different text encodings gracefully.
    UTF-8 is standard, but users might upload files in other encodings.
    
    Args:
        input_path: Path to input text file
        output_path: Path where PDF should be saved
        
    Returns:
        Path to generated PDF file
        
    Raises:
        Exception: If conversion fails
    """
    try:
        # Read text file with encoding detection
        # Senior Dev Tip: Try UTF-8 first, fall back to other encodings
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
        except UnicodeDecodeError:
            # Try with latin-1 as fallback
            with open(input_path, 'r', encoding='latin-1') as f:
                text_content = f.read()
        
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
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Create a monospace style for code/text
        # Senior Dev Tip: Monospace fonts preserve formatting for code
        code_style = ParagraphStyle(
            'Code',
            parent=styles['Normal'],
            fontName='Courier',
            fontSize=10,
            leading=12,
            leftIndent=0,
            rightIndent=0,
            alignment=TA_LEFT
        )
        
        # Split text into lines and add to PDF
        lines = text_content.split('\n')
        
        for line in lines:
            # Use Preformatted to preserve spacing
            if line.strip():
                p = Preformatted(line, code_style)
                story.append(p)
            else:
                # Add spacing for empty lines
                story.append(Spacer(1, 0.1 * inch))
        
        # Build PDF
        pdf.build(story)
        
        logger.info(f"Successfully converted text to PDF: {output_path}")
        return output_path
    
    except Exception as e:
        logger.error(f"Error converting text to PDF: {e}")
        raise Exception(f"Text to PDF conversion failed: {str(e)}")
