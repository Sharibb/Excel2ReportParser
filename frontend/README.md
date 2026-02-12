# Frontend - Vulnerability Report Automation

Flask-based web frontend for the Vulnerability Report Automation Service.

## Features

- **Modern UI**: Clean, responsive Bootstrap 5 interface
- **Phase 1**: Upload Word documents, download Excel files
- **Phase 2**: Upload Excel + Template, download generated Word reports
- **Drag & Drop**: Easy file uploads with drag-and-drop support
- **Progress Indicators**: Real-time feedback during processing
- **Health Monitoring**: Built-in health check endpoint

## Project Structure

```
frontend/
├── app.py                 # Flask application
├── templates/
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Landing page
│   ├── phase1.html       # Phase 1 interface
│   └── phase2.html       # Phase 2 interface
├── uploads/              # Temporary file uploads
├── downloads/            # Generated files for download
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
└── README.md           # This file
```

## Local Development

### Prerequisites

- Python 3.11+
- Backend service running (default: http://localhost:8000)

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables (optional)
export BACKEND_URL=http://localhost:8000
export SECRET_KEY=your-secret-key-here
export PORT=5000
export DEBUG=True

# Run Flask app
python app.py
```

The frontend will be available at `http://localhost:5000`

## Docker Deployment

### Build Image

```bash
docker build -t vuln-report-frontend .
```

### Run Container

```bash
docker run -d \
  -p 5000:5000 \
  -e BACKEND_URL=http://backend:8000 \
  -e SECRET_KEY=change-me-in-production \
  --name frontend \
  vuln-report-frontend
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BACKEND_URL` | `http://localhost:8000` | Backend API URL |
| `SECRET_KEY` | `dev-secret-key...` | Flask secret key (change in production!) |
| `PORT` | `5000` | Port to run on |
| `DEBUG` | `False` | Enable debug mode |

## API Endpoints

### Frontend Routes

- `GET /` - Landing page
- `GET /phase1` - Phase 1 interface
- `GET /phase2` - Phase 2 interface
- `GET /health` - Health check
- `POST /api/phase1/parse` - Process Phase 1 requests
- `POST /api/phase2/generate` - Process Phase 2 requests
- `GET /download/<filename>` - Download generated files

### Backend Integration

The frontend proxies requests to the backend API:

- Phase 1: `POST /api/phase1/parse`
- Phase 2: `POST /api/phase2/generate`

## Usage

### Phase 1: Download Template

1. Navigate to Phase 1 page
2. Click "Download Excel Template"
3. Fill the template with vulnerability data
4. Use the filled template in Phase 2

### Phase 2: Excel → Word

1. Navigate to Phase 2 page
2. Upload Excel data file (.xlsx)
3. Upload Word template (.docx)
4. Optionally provide PoC images folder path
5. Click "Generate Report"
6. Download the generated Word document

## Features

### File Upload

- Drag & drop support
- File type validation
- Size limit: 100MB
- Progress indicators

### Error Handling

- Graceful error messages
- Timeout handling (5 minutes)
- Backend connectivity checks
- Automatic file cleanup

### Security

- File name sanitization
- Path traversal prevention
- MIME type validation
- Size limit enforcement

## Production Considerations

1. **Change Secret Key**: Set unique `SECRET_KEY` in production
2. **HTTPS**: Use reverse proxy (nginx) with SSL/TLS
3. **File Cleanup**: Old files are auto-cleaned (keeps last 10)
4. **Timeouts**: 5-minute timeout for long-running operations
5. **Workers**: Gunicorn with 4 workers by default

## Health Check

The `/health` endpoint returns:

```json
{
  "status": "healthy",
  "frontend": "healthy",
  "backend": "healthy",
  "backend_url": "http://backend:8000"
}
```

Status will be `degraded` if backend is unreachable.

## Troubleshooting

### Backend Connection Failed

- Check `BACKEND_URL` environment variable
- Ensure backend service is running
- Verify network connectivity between containers

### File Upload Fails

- Check file size (max 100MB)
- Verify file extension (.docx, .xlsx, .xls)
- Check disk space in uploads directory

### Timeout Errors

- Increase timeout in `app.py` (currently 300s)
- Check backend performance
- Verify file is not corrupted

## Development

### Adding New Routes

1. Add route in `app.py`
2. Create template in `templates/`
3. Update navigation in `base.html`

### Styling

- Uses Bootstrap 5 CDN
- Custom CSS in `base.html` `<style>` block
- Bootstrap Icons for icons

## License

Part of the Vulnerability Report Automation Service.
