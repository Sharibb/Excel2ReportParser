"""Phase 3 API routes: Excel + Template + PoC ZIP → Word generation."""

from pathlib import Path
from typing import Annotated, Optional
import uuid

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.exceptions import AppBaseException
from app.core.logging import get_logger
from app.services.phase2.excel_reader import ExcelReader
from app.services.phase2.word_generator import WordGenerator
from app.services.phase3.zip_handler import ZipHandler
from app.utils.file_utils import save_upload_file, sanitize_filename, validate_mime_type

logger = get_logger(__name__)
router = APIRouter(prefix="/phase3", tags=["Phase 3 - Excel + Template + PoC ZIP"])


@router.post("/generate")
async def generate_word_with_poc_zip(
    excel_file: Annotated[UploadFile, File(description="Excel file with vulnerability data")],
    template_file: Annotated[UploadFile, File(description="Word template (.docx) file")],
    poc_zip: Annotated[UploadFile, File(description="ZIP file containing PoC folders")],
) -> FileResponse:
    """
    Generate Word vulnerability report from Excel data, template, and PoC ZIP.

    Args:
        excel_file: Uploaded Excel file with vulnerability data
        template_file: Uploaded Word template file
        poc_zip: ZIP file containing PoC folders (POC/C1,H1,M1/1.png,2.png...)

    Returns:
        Generated Word document with PoC images inserted

    Raises:
        HTTPException: If processing fails
    """
    temp_excel_path: Path | None = None
    temp_template_path: Path | None = None
    temp_zip_path: Path | None = None
    output_docx_path: Path | None = None
    extraction_dir: Path | None = None
    zip_handler: ZipHandler | None = None

    try:
        logger.info(
            f"Received Phase 3 generate request - Excel: {excel_file.filename}, "
            f"Template: {template_file.filename}, ZIP: {poc_zip.filename}"
        )

        # Validate file types
        if excel_file.filename:
            validate_mime_type(excel_file.filename, [".xlsx", ".xls"])
        if template_file.filename:
            validate_mime_type(template_file.filename, [".docx"])
        if poc_zip.filename:
            validate_mime_type(poc_zip.filename, [".zip"])

        # Save uploaded files
        safe_excel_name = sanitize_filename(excel_file.filename or "data.xlsx")
        safe_template_name = sanitize_filename(template_file.filename or "template.docx")
        safe_zip_name = sanitize_filename(poc_zip.filename or "poc.zip")

        temp_excel_path = await save_upload_file(
            excel_file, settings.upload_path / safe_excel_name
        )
        temp_template_path = await save_upload_file(
            template_file, settings.upload_path / safe_template_name
        )
        temp_zip_path = await save_upload_file(
            poc_zip, settings.upload_path / safe_zip_name
        )

        # Create unique extraction directory
        extraction_id = str(uuid.uuid4())
        extraction_dir = settings.upload_path / f"poc_extracted_{extraction_id}"

        # Extract ZIP file
        logger.info(f"Extracting PoC ZIP file: {temp_zip_path}")
        zip_handler = ZipHandler(temp_zip_path, extraction_dir)
        poc_base_path = zip_handler.extract()

        # List found PoC folders
        poc_folders = zip_handler.list_poc_folders()
        logger.info(f"Found {len(poc_folders)} PoC folders: {poc_folders}")

        # Read Excel file
        reader = ExcelReader(temp_excel_path)
        report = reader.read()

        logger.info(
            f"Read {report.total_count} vulnerabilities from Excel: "
            f"C:{report.critical_count}, H:{report.high_count}, "
            f"M:{report.medium_count}, L:{report.low_count}, I:{report.info_count}"
        )

        # Map PoC folders to vulnerabilities
        vulnerabilities_with_pocs = 0
        for vuln in report.vulnerabilities:
            # Try to find PoC folder for this vulnerability
            poc_folder_path = zip_handler.get_poc_folder_path(vuln.vuln_id)

            if poc_folder_path:
                # Set the PoC folder name (relative to base path)
                vuln.poc_folder = poc_folder_path.name
                vulnerabilities_with_pocs += 1
                logger.info(
                    f"Mapped PoC folder '{poc_folder_path.name}' to vulnerability {vuln.vuln_id}"
                )
            else:
                logger.warning(
                    f"No PoC folder found for vulnerability {vuln.vuln_id} in ZIP"
                )

        logger.info(
            f"Mapped PoC folders for {vulnerabilities_with_pocs}/{report.total_count} vulnerabilities"
        )

        # Generate Word document
        output_filename = Path(safe_template_name).stem + "_generated_with_pocs.docx"
        output_docx_path = settings.output_path / output_filename

        generator = WordGenerator(temp_template_path)
        output_docx_path = generator.generate(report, output_docx_path, poc_base_path)

        logger.info(f"Successfully generated Word document with PoCs at: {output_docx_path}")

        # Return Word file
        return FileResponse(
            path=str(output_docx_path),
            filename=output_filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    except AppBaseException as e:
        logger.error(f"Application error during Phase 3 generation: {e.message}")
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error during Phase 3 generation: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to generate document: {str(e)}"
        )
    finally:
        # Cleanup temporary files
        for temp_path in [temp_excel_path, temp_template_path, temp_zip_path]:
            if temp_path and temp_path.exists():
                try:
                    temp_path.unlink()
                    logger.debug(f"Cleaned up temporary file: {temp_path}")
                except Exception as e:
                    logger.warning(f"Failed to cleanup temp file: {e}")

        # Cleanup extracted ZIP contents
        if zip_handler:
            try:
                zip_handler.cleanup()
            except Exception as e:
                logger.warning(f"Failed to cleanup extracted ZIP: {e}")


@router.get("/health")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint for Phase 3 service.

    Returns:
        Status dictionary
    """
    return {"status": "healthy", "service": "phase3"}
