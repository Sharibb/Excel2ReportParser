"""File handling utility functions."""

import re
from pathlib import Path
from typing import BinaryIO

from fastapi import UploadFile

from app.core.config import settings
from app.core.exceptions import ValidationError
from app.core.logging import get_logger

logger = get_logger(__name__)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal and invalid characters.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Remove path components
    filename = Path(filename).name

    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)

    # Remove leading/trailing dots and spaces
    filename = filename.strip(". ")

    # Ensure filename is not empty
    if not filename:
        filename = "unnamed_file"

    return filename


def validate_file_size(file_size: int) -> None:
    """
    Validate that file size is within allowed limits.

    Args:
        file_size: File size in bytes

    Raises:
        ValidationError: If file size exceeds maximum
    """
    max_size = settings.max_file_size_bytes

    if file_size > max_size:
        raise ValidationError(
            f"File size ({file_size} bytes) exceeds maximum allowed "
            f"({max_size} bytes / {settings.max_file_size_mb} MB)",
            details={"file_size": file_size, "max_size": max_size},
        )


def validate_mime_type(filename: str, allowed_types: list[str]) -> None:
    """
    Validate file MIME type based on extension.

    Args:
        filename: Name of the file
        allowed_types: List of allowed extensions (e.g., ['.docx', '.xlsx'])

    Raises:
        ValidationError: If file type is not allowed
    """
    file_ext = Path(filename).suffix.lower()

    if file_ext not in allowed_types:
        raise ValidationError(
            f"File type '{file_ext}' is not allowed. "
            f"Allowed types: {', '.join(allowed_types)}",
            details={"extension": file_ext, "allowed": allowed_types},
        )


async def save_upload_file(upload_file: UploadFile, destination: Path) -> Path:
    """
    Save uploaded file to destination with validation.

    Args:
        upload_file: FastAPI UploadFile object
        destination: Destination path (directory or full file path)

    Returns:
        Path to saved file

    Raises:
        ValidationError: If file validation fails
    """
    try:
        # Sanitize filename
        safe_filename = sanitize_filename(upload_file.filename or "uploaded_file")

        # Determine final path
        if destination.is_dir():
            file_path = destination / safe_filename
        else:
            file_path = destination

        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Read and validate file size
        content = await upload_file.read()
        validate_file_size(len(content))

        # Write file
        with open(file_path, "wb") as f:
            f.write(content)

        logger.info(f"File saved successfully: {file_path}")
        return file_path

    except Exception as e:
        logger.error(f"Failed to save upload file: {e}")
        raise ValidationError(f"Failed to save file: {str(e)}")


def get_file_size(file_obj: BinaryIO) -> int:
    """
    Get size of file object.

    Args:
        file_obj: File object

    Returns:
        File size in bytes
    """
    file_obj.seek(0, 2)  # Seek to end
    size = file_obj.tell()
    file_obj.seek(0)  # Reset to beginning
    return size
