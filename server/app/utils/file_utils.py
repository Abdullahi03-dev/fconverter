"""
File Utility Functions

Helper functions for file operations.

Senior Dev Tip: Utility modules keep your code DRY (Don't Repeat Yourself).
These functions can be reused across different endpoints.
"""

import os
import uuid
import aiofiles
from pathlib import Path
from typing import Optional
from fastapi import UploadFile
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


def generate_unique_filename(original_filename: str, extension: Optional[str] = None) -> str:
    """
    Generate a unique filename to avoid collisions.
    
    Senior Dev Tip: Using UUIDs prevents file overwrites and
    makes filenames unpredictable (security benefit).
    
    Args:
        original_filename: Original file name
        extension: Optional extension override
        
    Returns:
        Unique filename with extension
    """
    if extension is None:
        # Extract extension from original filename
        extension = Path(original_filename).suffix
    
    # Generate unique ID
    unique_id = str(uuid.uuid4())
    
    # Combine: uuid + extension
    return f"{unique_id}{extension}"


async def save_upload_file(upload_file: UploadFile, destination: str) -> str:
    """
    Save an uploaded file to disk asynchronously.
    
    Senior Dev Tip: Using async file I/O prevents blocking the event loop,
    allowing the server to handle other requests while writing files.
    
    Args:
        upload_file: FastAPI UploadFile object
        destination: Full path where file should be saved
        
    Returns:
        Path to saved file
    """
    try:
        async with aiofiles.open(destination, 'wb') as f:
            # Read and write in chunks to handle large files efficiently
            while chunk := await upload_file.read(1024 * 1024):  # 1MB chunks
                await f.write(chunk)
        
        logger.info(f"File saved: {destination}")
        return destination
    
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        raise


def get_file_size(filepath: str) -> int:
    """
    Get file size in bytes.
    
    Args:
        filepath: Path to file
        
    Returns:
        File size in bytes
    """
    return os.path.getsize(filepath)


def delete_file(filepath: str) -> bool:
    """
    Delete a file safely.
    
    Senior Dev Tip: Always handle file deletion errors gracefully.
    Don't let cleanup failures crash your app.
    
    Args:
        filepath: Path to file to delete
        
    Returns:
        True if deleted, False otherwise
    """
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"File deleted: {filepath}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error deleting file {filepath}: {e}")
        return False


def cleanup_old_files(directory: str, max_age_minutes: int = 30):
    """
    Delete files older than specified age.
    
    Senior Dev Tip: Implement cleanup to prevent disk space issues.
    This can be run as a background task or cron job.
    
    Args:
        directory: Directory to clean
        max_age_minutes: Maximum file age in minutes
    """
    import time
    
    now = time.time()
    max_age_seconds = max_age_minutes * 60
    
    try:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            
            if os.path.isfile(filepath):
                file_age = now - os.path.getmtime(filepath)
                
                if file_age > max_age_seconds:
                    delete_file(filepath)
                    logger.info(f"Cleaned up old file: {filename}")
    
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")
