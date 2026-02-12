"""API routes for cleanup operations."""

import shutil
from pathlib import Path
from typing import Dict, Any

from fastapi import APIRouter, HTTPException
from app.core.config import settings
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/purge-cache")
async def purge_cache() -> Dict[str, Any]:
    """
    Purge all cached files (uploads and outputs).
    
    This endpoint will:
    - Delete all files from the uploads directory
    - Delete all files from the output directory
    - Keep the directories themselves
    
    Returns:
        Dictionary with cleanup statistics
    """
    try:
        uploads_dir = settings.upload_path
        output_dir = settings.output_path
        
        deleted_files = 0
        deleted_size = 0
        errors = []
        
        # Clean uploads directory
        if uploads_dir.exists():
            for item in uploads_dir.iterdir():
                try:
                    if item.is_file():
                        size = item.stat().st_size
                        item.unlink()
                        deleted_files += 1
                        deleted_size += size
                        logger.info(f"Deleted upload file: {item.name}")
                    elif item.is_dir():
                        shutil.rmtree(item)
                        logger.info(f"Deleted upload directory: {item.name}")
                except Exception as e:
                    errors.append(f"Failed to delete {item.name}: {str(e)}")
                    logger.error(f"Error deleting {item}: {e}")
        
        # Clean output directory
        if output_dir.exists():
            for item in output_dir.iterdir():
                try:
                    if item.is_file():
                        size = item.stat().st_size
                        item.unlink()
                        deleted_files += 1
                        deleted_size += size
                        logger.info(f"Deleted output file: {item.name}")
                    elif item.is_dir():
                        shutil.rmtree(item)
                        logger.info(f"Deleted output directory: {item.name}")
                except Exception as e:
                    errors.append(f"Failed to delete {item.name}: {str(e)}")
                    logger.error(f"Error deleting {item}: {e}")
        
        # Format size in human-readable format
        if deleted_size < 1024:
            size_str = f"{deleted_size} bytes"
        elif deleted_size < 1024 * 1024:
            size_str = f"{deleted_size / 1024:.2f} KB"
        else:
            size_str = f"{deleted_size / (1024 * 1024):.2f} MB"
        
        result = {
            "status": "success",
            "deleted_files": deleted_files,
            "deleted_size": size_str,
            "deleted_size_bytes": deleted_size,
            "errors": errors if errors else None
        }
        
        logger.info(f"Cache purge completed: {deleted_files} files deleted, {size_str} freed")
        
        return result
        
    except Exception as e:
        logger.error(f"Cache purge failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to purge cache: {str(e)}"
        )


@router.get("/cache-info")
async def get_cache_info() -> Dict[str, Any]:
    """
    Get information about cached files.
    
    Returns:
        Dictionary with cache statistics
    """
    try:
        uploads_dir = settings.upload_path
        output_dir = settings.output_path
        
        def get_dir_stats(directory: Path) -> Dict[str, Any]:
            if not directory.exists():
                return {"files": 0, "size_bytes": 0, "size": "0 bytes"}
            
            file_count = 0
            total_size = 0
            
            for item in directory.rglob("*"):
                if item.is_file():
                    file_count += 1
                    total_size += item.stat().st_size
            
            if total_size < 1024:
                size_str = f"{total_size} bytes"
            elif total_size < 1024 * 1024:
                size_str = f"{total_size / 1024:.2f} KB"
            else:
                size_str = f"{total_size / (1024 * 1024):.2f} MB"
            
            return {
                "files": file_count,
                "size_bytes": total_size,
                "size": size_str
            }
        
        uploads_stats = get_dir_stats(uploads_dir)
        output_stats = get_dir_stats(output_dir)
        
        total_files = uploads_stats["files"] + output_stats["files"]
        total_size = uploads_stats["size_bytes"] + output_stats["size_bytes"]
        
        if total_size < 1024:
            total_size_str = f"{total_size} bytes"
        elif total_size < 1024 * 1024:
            total_size_str = f"{total_size / 1024:.2f} KB"
        else:
            total_size_str = f"{total_size / (1024 * 1024):.2f} MB"
        
        return {
            "uploads": uploads_stats,
            "outputs": output_stats,
            "total": {
                "files": total_files,
                "size_bytes": total_size,
                "size": total_size_str
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get cache info: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get cache info: {str(e)}"
        )
