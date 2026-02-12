"""ZIP file handler for PoC image extraction."""

import zipfile
import shutil
from pathlib import Path
from typing import Optional

from app.core.exceptions import ValidationError
from app.core.logging import get_logger

logger = get_logger(__name__)


class ZipHandler:
    """Handler for extracting and managing PoC ZIP files."""

    def __init__(self, zip_path: Path, extract_to: Path) -> None:
        """
        Initialize ZIP handler.

        Args:
            zip_path: Path to ZIP file
            extract_to: Directory to extract contents to
        """
        self.zip_path = zip_path
        self.extract_to = extract_to
        self.poc_base_path: Optional[Path] = None

    def extract(self) -> Path:
        """
        Extract ZIP file and return base PoC path.

        Returns:
            Path to extracted PoC base directory

        Raises:
            ValidationError: If ZIP is invalid or extraction fails
        """
        try:
            logger.info(f"Extracting ZIP file: {self.zip_path}")

            # Validate ZIP file
            if not zipfile.is_zipfile(self.zip_path):
                raise ValidationError(f"Invalid ZIP file: {self.zip_path}")

            # Create extraction directory
            self.extract_to.mkdir(parents=True, exist_ok=True)

            # Extract ZIP
            with zipfile.ZipFile(self.zip_path, "r") as zip_ref:
                # Get list of files
                file_list = zip_ref.namelist()
                logger.info(f"ZIP contains {len(file_list)} files")

                # Extract all files
                zip_ref.extractall(self.extract_to)

            logger.info(f"Successfully extracted ZIP to: {self.extract_to}")

            # Find the PoC base directory
            # Expected structure: POC/C1,C2,H1,H2/1.png,2.png
            # or direct structure: C1,C2,H1,H2/1.png,2.png
            poc_base = self._find_poc_base_directory()

            if not poc_base:
                raise ValidationError(
                    "Could not find PoC base directory. Expected structure: "
                    "POC/C1,C2,H1/ or C1,C2,H1/ at ZIP root"
                )

            self.poc_base_path = poc_base
            logger.info(f"PoC base directory: {poc_base}")

            return poc_base

        except zipfile.BadZipFile as e:
            logger.error(f"Bad ZIP file: {e}")
            raise ValidationError(f"Corrupted ZIP file: {str(e)}")
        except Exception as e:
            logger.error(f"Failed to extract ZIP: {e}")
            raise ValidationError(f"ZIP extraction failed: {str(e)}")

    def _find_poc_base_directory(self) -> Optional[Path]:
        """
        Find the base directory containing PoC folders.

        Looks for a directory containing folders named like vulnerability IDs
        (C1, H1, M1, L1, I1, etc.)

        Returns:
            Path to PoC base directory or None if not found
        """
        # Check if there's a "POC" directory
        poc_dir = self.extract_to / "POC"
        if poc_dir.exists() and poc_dir.is_dir():
            # Check if it contains vulnerability-like folders
            if self._contains_vulnerability_folders(poc_dir):
                return poc_dir

        # Check if extract_to itself contains vulnerability folders
        if self._contains_vulnerability_folders(self.extract_to):
            return self.extract_to

        # Search one level deep
        for item in self.extract_to.iterdir():
            if item.is_dir() and self._contains_vulnerability_folders(item):
                return item

        return None

    def _contains_vulnerability_folders(self, directory: Path) -> bool:
        """
        Check if directory contains folders named like vulnerability IDs.

        Args:
            directory: Directory to check

        Returns:
            True if contains vulnerability-like folders
        """
        try:
            # Look for folders matching vulnerability ID pattern (C1, H1, M2, L3, I1, etc.)
            import re

            vuln_pattern = re.compile(r"^[CHML I][0-9]+$", re.IGNORECASE)

            folders = [
                item.name
                for item in directory.iterdir()
                if item.is_dir() and vuln_pattern.match(item.name)
            ]

            logger.debug(
                f"Found {len(folders)} vulnerability folders in {directory}: {folders[:5]}"
            )

            # Consider it valid if we find at least 1 vulnerability folder
            return len(folders) >= 1

        except Exception as e:
            logger.debug(f"Error checking directory {directory}: {e}")
            return False

    def cleanup(self) -> None:
        """Clean up extracted files."""
        try:
            if self.extract_to.exists():
                shutil.rmtree(self.extract_to)
                logger.info(f"Cleaned up extracted files: {self.extract_to}")
        except Exception as e:
            logger.warning(f"Failed to cleanup extracted files: {e}")

    def get_poc_folder_path(self, vuln_id: str) -> Optional[Path]:
        """
        Get path to PoC folder for a specific vulnerability ID.

        Args:
            vuln_id: Vulnerability ID (e.g., "H1", "M2", "C1")

        Returns:
            Path to PoC folder or None if not found
        """
        if not self.poc_base_path:
            return None

        # Try exact match first
        poc_folder = self.poc_base_path / vuln_id
        if poc_folder.exists() and poc_folder.is_dir():
            return poc_folder

        # Try case-insensitive match
        vuln_id_upper = vuln_id.upper()
        for item in self.poc_base_path.iterdir():
            if item.is_dir() and item.name.upper() == vuln_id_upper:
                return item

        logger.debug(f"PoC folder not found for vulnerability: {vuln_id}")
        return None

    def list_poc_folders(self) -> list[str]:
        """
        List all PoC folders found in the ZIP.

        Returns:
            List of PoC folder names
        """
        if not self.poc_base_path:
            return []

        try:
            folders = [
                item.name for item in self.poc_base_path.iterdir() if item.is_dir()
            ]
            return sorted(folders)
        except Exception as e:
            logger.error(f"Failed to list PoC folders: {e}")
            return []
