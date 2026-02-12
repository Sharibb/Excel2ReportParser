"""Phase 2 API routes: Excel → Word generation."""

from pathlib import Path
from typing import Annotated, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.exceptions import AppBaseException
from app.core.logging import get_logger
from app.services.phase2.excel_reader import ExcelReader
from app.services.phase2.word_generator import WordGenerator
from app.utils.file_utils import save_upload_file, sanitize_filename, validate_mime_type
from app.utils.validators import validate_poc_folder

logger = get_logger(__name__)
router = APIRouter(prefix="/phase2", tags=["Phase 2 - Excel to Word"])


@router.post("/generate")
async def generate_word_from_excel(
    excel_file: Annotated[UploadFile, File(description="Excel file with vulnerability data")],
    template_file: Annotated[UploadFile, File(description="Word template (.docx) file")],
    poc_folder: Annotated[
        Optional[str], Form(description="Path to PoC images folder (optional)")
    ] = None,
) -> FileResponse:
    """
    Generate Word vulnerability report from Excel data and template.

    Args:
        excel_file: Uploaded Excel file with vulnerability data
        template_file: Uploaded Word template file
        poc_folder: Optional path to PoC images folder

    Returns:
        Generated Word document

    Raises:
        HTTPException: If processing fails
    """
    temp_excel_path: Path | None = None
    temp_template_path: Path | None = None
    output_docx_path: Path | None = None
    poc_base_path: Path | None = None

    try:
        logger.info(
            f"Received generate request - Excel: {excel_file.filename}, "
            f"Template: {template_file.filename}"
        )

        # Validate file types
        if excel_file.filename:
            validate_mime_type(excel_file.filename, [".xlsx", ".xls"])
        if template_file.filename:
            validate_mime_type(template_file.filename, [".docx"])

        # Save uploaded files
        safe_excel_name = sanitize_filename(excel_file.filename or "data.xlsx")
        safe_template_name = sanitize_filename(template_file.filename or "template.docx")

        temp_excel_path = await save_upload_file(
            excel_file, settings.upload_path / safe_excel_name
        )
        temp_template_path = await save_upload_file(
            template_file, settings.upload_path / safe_template_name
        )

        # Validate PoC folder if provided
        if poc_folder:
            try:
                poc_base_path = validate_poc_folder(poc_folder)
                logger.info(f"Using PoC folder: {poc_base_path}")
            except Exception as e:
                logger.warning(f"PoC folder validation failed: {e}. Continuing without images.")
                poc_base_path = None

        # Read Excel file
        reader = ExcelReader(temp_excel_path)
        report = reader.read()

        logger.info(
            f"Read {report.total_count} vulnerabilities from Excel: "
            f"C:{report.critical_count}, H:{report.high_count}, "
            f"M:{report.medium_count}, L:{report.low_count}, I:{report.info_count}"
        )

        # Generate Word document
        output_filename = Path(safe_template_name).stem + "_generated.docx"
        output_docx_path = settings.output_path / output_filename

        generator = WordGenerator(temp_template_path)
        output_docx_path = generator.generate(report, output_docx_path, poc_base_path)

        # Return Word file
        return FileResponse(
            path=str(output_docx_path),
            filename=output_filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    except AppBaseException as e:
        logger.error(f"Application error during generation: {e.message}")
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error during generation: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to generate document: {str(e)}"
        )
    finally:
        # Cleanup temporary files (keep output file for download)
        for temp_path in [temp_excel_path, temp_template_path]:
            if temp_path and temp_path.exists():
                try:
                    temp_path.unlink()
                    logger.debug(f"Cleaned up temporary file: {temp_path}")
                except Exception as e:
                    logger.warning(f"Failed to cleanup temp file: {e}")


@router.get("/health")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint for Phase 2 service.

    Returns:
        Status dictionary
    """
    return {"status": "healthy", "service": "phase2"}
