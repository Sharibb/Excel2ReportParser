"""Flask frontend for Vulnerability Report Automation Service."""

import os
import requests
from pathlib import Path
from flask import (
    Flask,
    render_template,
    request,
    send_file,
    flash,
    redirect,
    url_for,
    jsonify,
)
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
UPLOAD_FOLDER = Path("./uploads")
DOWNLOAD_FOLDER = Path("./downloads")
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = {"docx", "xlsx", "xls"}

# Create Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["DOWNLOAD_FOLDER"] = DOWNLOAD_FOLDER

# Ensure directories exist
UPLOAD_FOLDER.mkdir(exist_ok=True)
DOWNLOAD_FOLDER.mkdir(exist_ok=True)


def allowed_file(filename: str, extensions: set[str]) -> bool:
    """Check if file has allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in extensions


def cleanup_old_files(directory: Path, max_files: int = 10) -> None:
    """Clean up old files to prevent disk bloat."""
    try:
        files = sorted(directory.glob("*"), key=lambda x: x.stat().st_mtime, reverse=True)
        for old_file in files[max_files:]:
            old_file.unlink()
    except Exception:
        pass  # Ignore cleanup errors


@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    """Handle file too large errors."""
    flash("File too large! Maximum size is 100MB.", "error")
    return redirect(url_for("index"))


@app.route("/")
def index():
    """Landing page with service selection."""
    return render_template("index.html", backend_url=BACKEND_URL)


@app.route("/phase1")
def phase1():
    """Phase 1: Download Excel template page."""
    return render_template("phase1.html")


@app.route("/phase2")
def phase2():
    """Phase 2: Excel to Word generation page."""
    return render_template("phase2.html")


@app.route("/api/phase1/download-excel-template")
def phase1_download_excel_template():
    """Download the Excel template for Phase 1."""
    try:
        template_path = Path(__file__).parent / "All_Risk_Levels_Template.xlsx"
        
        if not template_path.exists():
            return jsonify({"error": "Excel template file not found"}), 404
        
        return send_file(
            template_path,
            as_attachment=True,
            download_name="All_Risk_Levels_Template.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    except Exception as e:
        return jsonify({"error": f"Download error: {str(e)}"}), 500


@app.route("/api/phase1/download-word-template")
def phase1_download_word_template():
    """Download the Word demo template for Phase 1."""
    try:
        template_path = Path(__file__).parent / "WAPT-Rootnik-Technical.docx"
        
        if not template_path.exists():
            return jsonify({"error": "Word template file not found"}), 404
        
        return send_file(
            template_path,
            as_attachment=True,
            download_name="WAPT-Rootnik-Technical.docx",
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    except Exception as e:
        return jsonify({"error": f"Download error: {str(e)}"}), 500


@app.route("/api/phase2/generate", methods=["POST"])
def phase2_generate():
    """Handle Phase 2: Generate Word document from Excel."""
    try:
        # Validate file uploads
        if "excel_file" not in request.files or "template_file" not in request.files:
            return jsonify({"error": "Both Excel and template files are required"}), 400

        excel_file = request.files["excel_file"]
        template_file = request.files["template_file"]
        poc_folder = request.form.get("poc_folder", "").strip()

        if excel_file.filename == "" or template_file.filename == "":
            return jsonify({"error": "Please select both files"}), 400

        if not allowed_file(excel_file.filename, {"xlsx", "xls"}):
            return jsonify({"error": "Excel file must be .xlsx or .xls"}), 400

        if not allowed_file(template_file.filename, {"docx"}):
            return jsonify({"error": "Template must be .docx"}), 400

        # Save uploaded files
        excel_filename = secure_filename(excel_file.filename)
        template_filename = secure_filename(template_file.filename)
        
        excel_path = UPLOAD_FOLDER / excel_filename
        template_path = UPLOAD_FOLDER / template_filename

        excel_file.save(excel_path)
        template_file.save(template_path)

        # Prepare request to backend
        with open(excel_path, "rb") as ef, open(template_path, "rb") as tf:
            files = {
                "excel_file": (excel_filename, ef, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
                "template_file": (template_filename, tf, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
            }
            
            data = {}
            if poc_folder:
                data["poc_folder"] = poc_folder

            response = requests.post(
                f"{BACKEND_URL}/api/phase2/generate",
                files=files,
                data=data,
                timeout=300,  # 5 minutes timeout
            )

        # Cleanup uploaded files
        excel_path.unlink()
        template_path.unlink()

        if response.status_code == 200:
            # Save downloaded Word file
            output_filename = Path(template_filename).stem + "_generated.docx"
            output_path = DOWNLOAD_FOLDER / output_filename
            
            with open(output_path, "wb") as f:
                f.write(response.content)

            # Cleanup old files
            cleanup_old_files(DOWNLOAD_FOLDER)

            return jsonify({
                "success": True,
                "message": "Word document generated successfully!",
                "download_url": url_for("download_file", filename=output_filename),
            })
        else:
            error_detail = response.json().get("detail", "Unknown error")
            return jsonify({"error": f"Backend error: {error_detail}"}), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timeout. File processing took too long."}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to connect to backend: {str(e)}"}), 503
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route("/download/<filename>")
def download_file(filename):
    """Download generated file."""
    try:
        file_path = DOWNLOAD_FOLDER / secure_filename(filename)
        if not file_path.exists():
            flash("File not found or expired", "error")
            return redirect(url_for("index"))
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
        )
    except Exception as e:
        flash(f"Download error: {str(e)}", "error")
        return redirect(url_for("index"))


@app.route("/health")
def health():
    """Health check endpoint."""
    try:
        # Check backend connectivity
        backend_response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        backend_healthy = backend_response.status_code == 200
    except Exception:
        backend_healthy = False

    return jsonify({
        "status": "healthy" if backend_healthy else "degraded",
        "frontend": "healthy",
        "backend": "healthy" if backend_healthy else "unhealthy",
        "backend_url": BACKEND_URL,
    }), 200 if backend_healthy else 503


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=os.getenv("DEBUG", "False").lower() == "true",
    )
