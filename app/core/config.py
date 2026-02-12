"""Configuration management using Pydantic settings."""

from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = Field(default="Vulnerability Report Automation Service")
    app_version: str = Field(default="0.1.0")
    debug: bool = Field(default=False)

    # Server
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    # File Upload
    max_file_size_mb: int = Field(default=50)

    # Directories
    upload_dir: str = Field(default="uploads")
    output_dir: str = Field(default="output")
    template_dir: str = Field(default="templates")
    log_dir: str = Field(default="logs")

    # Logging
    log_level: str = Field(default="INFO")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(message)s"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def upload_path(self) -> Path:
        """Get upload directory as Path object."""
        return Path(self.upload_dir)

    @property
    def output_path(self) -> Path:
        """Get output directory as Path object."""
        return Path(self.output_dir)

    @property
    def template_path(self) -> Path:
        """Get template directory as Path object."""
        return Path(self.template_dir)

    @property
    def log_path(self) -> Path:
        """Get log directory as Path object."""
        return Path(self.log_dir)

    @property
    def max_file_size_bytes(self) -> int:
        """Get maximum file size in bytes."""
        return self.max_file_size_mb * 1024 * 1024

    def ensure_directories(self) -> None:
        """Create required directories if they don't exist."""
        self.upload_path.mkdir(parents=True, exist_ok=True)
        self.output_path.mkdir(parents=True, exist_ok=True)
        self.template_path.mkdir(parents=True, exist_ok=True)
        self.log_path.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()
