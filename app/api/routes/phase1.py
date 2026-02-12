"""Phase 1 API routes: Word → Excel parsing."""

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.exceptions import AppBaseException
from app.core.logging import get_logger
from app.services.phase1.word_parser import WordParser
from app.services.phase1.excel_generator import ExcelGenerator
from app.utils.file_utils import save_upload_file, sanitize_filename, validate_mime_type

logger = get_logger(__name__)
router = APIRouter(prefix="/phase1", tags=["Phase 1 - Word to Excel"])


@router.post("/parse")
async def parse_word_to_excel(
    docx_file: Annotated[UploadFile, File(description="Word document (.docx) to parse")],
) -> FileResponse:
    """
    Parse Word vulnerability report and generate Excel file.

    Args:
        docx_file: Uploaded .docx file

    Returns:
        Generated Excel file

    Raises:
        HTTPException: If processing fails
    """
    temp_docx_path: Path | None = None
    output_excel_path: Path | None = None

    try:
        logger.info(f"Received parse request for file: {docx_file.filename}")

        # Validate file type
        if docx_file.filename:
            validate_mime_type(docx_file.filename, [".docx"])

        # Save uploaded file
        safe_filename = sanitize_filename(docx_file.filename or "report.docx")
        temp_docx_path = settings.upload_path / safe_filename

        temp_docx_path = await save_upload_file(docx_file, temp_docx_path)

        # Parse Word document
        parser = WordParser(temp_docx_path)
        report = parser.parse()

        logger.info(
            f"Parsed {report.total_count} vulnerabilities: "
            f"C:{report.critical_count}, H:{report.high_count}, "
            f"M:{report.medium_count}, L:{report.low_count}, I:{report.info_count}"
        )

        # Generate Excel file
        output_filename = Path(safe_filename).stem + "_vulnerabilities.xlsx"
        output_excel_path = settings.output_path / output_filename

        generator = ExcelGenerator()
        output_excel_path = generator.generate(report, output_excel_path)

        # Return Excel file
        return FileResponse(
            path=str(output_excel_path),
            filename=output_filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    except AppBaseException as e:
        logger.error(f"Application error during parsing: {e.message}")
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error during parsing: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")
    finally:
        # Cleanup temporary file (keep output file for download)
        if temp_docx_path and temp_docx_path.exists():
            try:
                temp_docx_path.unlink()
                logger.debug(f"Cleaned up temporary file: {temp_docx_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temp file: {e}")


@router.get("/health")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint for Phase 1 service.

    Returns:
        Status dictionary
    """
    return {"status": "healthy", "service": "phase1"}
