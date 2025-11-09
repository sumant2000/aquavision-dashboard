import os
import shutil
import uuid
import aiofiles
from fastapi import UploadFile
from datetime import datetime
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Upload configuration
UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
ALLOWED_EXTENSIONS = {".mp4", ".avi", ".mov", ".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB


async def save_upload_file(upload_file: UploadFile, content: bytes) -> str:
    """
    Save uploaded file to temporary directory
    
    Args:
        upload_file: FastAPI UploadFile object
        content: File content bytes
        
    Returns:
        Path to saved file
    """
    try:
        # Create upload directory if it doesn't exist
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(upload_file.filename)[1].lower()
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        logger.info(f"📁 File saved: {unique_filename}")
        return file_path
        
    except Exception as e:
        logger.error(f"❌ Failed to save file: {str(e)}")
        raise e


def cleanup_temp_files(max_age_hours: int = 24):
    """
    Clean up temporary files older than specified hours
    
    Args:
        max_age_hours: Maximum age of files to keep in hours
    """
    try:
        if not os.path.exists(UPLOAD_DIR):
            return
            
        current_time = datetime.now()
        files_removed = 0
        
        for filename in os.listdir(UPLOAD_DIR):
            file_path = os.path.join(UPLOAD_DIR, filename)
            
            if os.path.isfile(file_path):
                file_age = current_time - datetime.fromtimestamp(
                    os.path.getctime(file_path)
                )
                
                if file_age.total_seconds() > (max_age_hours * 3600):
                    os.remove(file_path)
                    files_removed += 1
        
        if files_removed > 0:
            logger.info(f"🧹 Cleaned up {files_removed} temporary files")
            
    except Exception as e:
        logger.error(f"❌ Failed to cleanup files: {str(e)}")


def validate_file_type(filename: str) -> bool:
    """
    Validate file extension
    
    Args:
        filename: Name of the file
        
    Returns:
        True if file type is allowed
    """
    if not filename:
        return False
        
    file_extension = os.path.splitext(filename)[1].lower()
    return file_extension in ALLOWED_EXTENSIONS


def get_file_info(file_path: str) -> dict:
    """
    Get file information
    
    Args:
        file_path: Path to the file
        
    Returns:
        Dictionary with file information
    """
    try:
        stat = os.stat(file_path)
        
        return {
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime),
            "modified": datetime.fromtimestamp(stat.st_mtime),
            "extension": os.path.splitext(file_path)[1].lower()
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get file info: {str(e)}")
        return {}


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def generate_analysis_id() -> str:
    """Generate unique analysis ID"""
    return f"AQV_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"


def generate_farm_id(name: str, location: str) -> str:
    """
    Generate farm ID based on name and location
    
    Args:
        name: Farm name
        location: Farm location
        
    Returns:
        Generated farm ID
    """
    # Clean and format inputs
    clean_name = "".join(c for c in name if c.isalnum())[:10]
    clean_location = "".join(c for c in location if c.isalnum())[:5]
    
    return f"UAE_{clean_location}_{clean_name}_{str(uuid.uuid4())[:6]}".upper()


class ConfigManager:
    """Configuration manager for application settings"""
    
    def __init__(self):
        self.settings = {
            "max_file_size": int(os.getenv("MAX_FILE_SIZE", MAX_FILE_SIZE)),
            "upload_dir": os.getenv("UPLOAD_DIR", UPLOAD_DIR),
            "cleanup_interval": int(os.getenv("CLEANUP_INTERVAL_HOURS", 24)),
            "default_feed_cost": float(os.getenv("DEFAULT_FEED_COST", 4.50)),
            "min_confidence_threshold": float(os.getenv("MIN_CONFIDENCE", 0.7)),
            "max_concurrent_analyses": int(os.getenv("MAX_CONCURRENT", 5))
        }
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.settings.get(key, default)
    
    def update(self, key: str, value):
        """Update configuration value"""
        self.settings[key] = value


# Global configuration instance
config = ConfigManager()