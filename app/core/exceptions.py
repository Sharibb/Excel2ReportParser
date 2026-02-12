"""Custom exception classes for the application."""

from typing import Any, Dict, Optional


class AppBaseException(Exception):
    """Base exception for all application exceptions."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize base exception.

        Args:
            message: Human-readable error message
            details: Optional dictionary with additional error details
        """
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(AppBaseException):
    """Raised when validation fails."""

    pass


class FileProcessingError(AppBaseException):
    """Raised when file processing fails."""

    pass


class TemplateError(AppBaseException):
    """Raised when template processing fails."""

    pass


class ParsingError(AppBaseException):
    """Raised when document parsing fails."""

    pass


class CorruptedTemplateError(TemplateError):
    """Raised when template structure is corrupted or invalid."""

    pass


class MissingRequiredColumnError(ValidationError):
    """Raised when required Excel columns are missing."""

    pass


class InvalidExcelStructureError(ValidationError):
    """Raised when Excel structure is invalid."""

    pass


class TemplateMismatchError(TemplateError):
    """Raised when template structure doesn't match expected format."""

    pass


class InvalidVulnerabilityFormatError(ValidationError):
    """Raised when vulnerability format is invalid (e.g., H1, M1)."""

    pass
