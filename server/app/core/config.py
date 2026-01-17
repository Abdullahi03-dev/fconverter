"""
Configuration settings for the File Converter API.

This module uses Pydantic Settings to manage environment variables
and application configuration. It's a best practice for managing
config in a type-safe way.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Union
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Senior Dev Tip: Using Pydantic Settings gives you:
    - Type validation
    - Environment variable parsing
    - Default values
    - Documentation in one place
    """
    
    # App Info
    app_name: str = "File Converter API"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False, description="Debug mode")
    
    # Server Config
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    
    # CORS Settings - using default list, not from env
    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]
    
    # File Upload Limits (in bytes)
    max_file_size: int = Field(
        default=10 * 1024 * 1024,  # 10MB for free tier
        description="Maximum file size in bytes"
    )
    
    # File Storage Paths
    upload_dir: str = Field(default="uploads", description="Upload directory")
    output_dir: str = Field(default="outputs", description="Output directory")
    
    # File Cleanup
    cleanup_after_minutes: int = Field(
        default=30,
        description="Delete files after X minutes"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create a global settings instance
# This is a singleton pattern - one instance shared across the app
settings = Settings()


def get_settings() -> Settings:
    """
    Dependency injection function for FastAPI.
    
    Senior Dev Tip: This allows you to easily mock settings in tests
    and follows the Dependency Inversion Principle.
    """
    return settings


# Ensure upload and output directories exist
os.makedirs(settings.upload_dir, exist_ok=True)
os.makedirs(settings.output_dir, exist_ok=True)
