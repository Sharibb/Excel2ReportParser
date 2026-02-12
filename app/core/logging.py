"""Structured file-based logging configuration."""

import logging
import sys
from pathlib import Path
from typing import Optional

from app.core.config import settings


class LoggerSetup:
    """Setup and configure application logging."""

    _initialized: bool = False

    @classmethod
    def setup(cls, log_file: Optional[str] = None) -> None:
        """
        Configure logging with file and console handlers.

        Args:
            log_file: Optional custom log filename. Defaults to app.log
        """
        if cls._initialized:
            return

        # Ensure log directory exists
        settings.log_path.mkdir(parents=True, exist_ok=True)

        # Determine log file path
        if log_file is None:
            log_file = "app.log"

        log_file_path = settings.log_path / log_file

        # Create formatter
        formatter = logging.Formatter(settings.log_format)

        # File handler
        file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # Console handler (for errors and above)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.ERROR if not settings.debug else logging.DEBUG)
        console_handler.setFormatter(formatter)

        # Root logger configuration
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, settings.log_level.upper()))
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

        cls._initialized = True

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get a logger instance for a specific module.

        Args:
            name: Logger name (typically __name__ of the module)

        Returns:
            Configured logger instance
        """
        return logging.getLogger(name)


def get_logger(name: str) -> logging.Logger:
    """
    Convenience function to get a logger.

    Args:
        name: Logger name (typically __name__ of the module)

    Returns:
        Configured logger instance
    """
    return LoggerSetup.get_logger(name)
