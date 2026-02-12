# API Reference

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. In production, consider implementing:
- API Keys
- OAuth 2.0
- JWT tokens
- Basic Auth

## Common Response Codes

| Code | Description                |
|------|----------------------------|
| 200  | Success                    |
| 400  | Bad Request / Validation Error |
| 404  | Not Found                  |
| 422  | Unprocessable Entity       |
| 500  | Internal Server Error      |

## Endpoints

### Health Checks

#### Global Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "vulnerability-report-automation"
}
```

#### Service Information

```http
GET /info
```

**Response:**
```json
{
  "app_name": "Vulnerability Report Automation Service",
  "version": "0.1.0",
  "debug": false,
  "max_file_size_mb": 50,
  "endpoints": {
    "phase1_parse": "/api/phase1/parse",
    "phase2_generate": "/api/phase2/generate"
  }
}
```

---

### Phase 1: Word to Excel

#### Parse Word Document

Extract vulnerability data from Word document and generate Excel file.

```http
POST /api/phase1/parse
```

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `docx_file` (file, required): Word document (.docx)

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/phase1/parse" \
  -H "Content-Type: multipart/form-data" \
  -F "docx_file=@report.docx" \
  --output vulnerabilities.xlsx
```

**Python Example:**
```python
import requests

with open('report.docx', 'rb') as f:
    files = {'docx_file': f}
    response = requests.post(
        'http://localhost:8000/api/phase1/parse',
        files=files
    )
    
    with open('vulnerabilities.xlsx', 'wb') as out:
        out.write(response.content)
```

**Response:**
- Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- Body: Excel file (binary)

**Error Response:**
```json
{
  "detail": "File type '.txt' is not allowed. Allowed types: .docx"
}
```

#### Phase 1 Health Check

```http
GET /api/phase1/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "phase1"
}
```

---

### Phase 2: Excel to Word

#### Generate Word Document

Generate Word document from Excel data using template.

```http
POST /api/phase2/generate
```

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `excel_file` (file, required): Excel file with vulnerability data (.xlsx)
  - `template_file` (file, required): Word template (.docx)
  - `poc_folder` (string, optional): Path to PoC images folder

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/phase2/generate" \
  -H "Content-Type: multipart/form-data" \
  -F "excel_file=@vulnerabilities.xlsx" \
  -F "template_file=@template.docx" \
  -F "poc_folder=/path/to/poc_images" \
  --output generated_report.docx
```

**Python Example:**
```python
import requests

with open('vulnerabilities.xlsx', 'rb') as excel, \
     open('template.docx', 'rb') as template:
    
    files = {
        'excel_file': excel,
        'template_file': template
    }
    data = {
        'poc_folder': '/path/to/poc_images'  # Optional
    }
    
    response = requests.post(
        'http://localhost:8000/api/phase2/generate',
        files=files,
        data=data
    )
    
    with open('generated_report.docx', 'wb') as out:
        out.write(response.content)
```

**JavaScript Example:**
```javascript
const formData = new FormData();
formData.append('excel_file', excelFileInput.files[0]);
formData.append('template_file', templateFileInput.files[0]);
formData.append('poc_folder', '/path/to/poc_images');

fetch('http://localhost:8000/api/phase2/generate', {
  method: 'POST',
  body: formData
})
.then(response => response.blob())
.then(blob => {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'generated_report.docx';
  a.click();
});
```

**Response:**
- Content-Type: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
- Body: Word document (binary)

**Error Response:**
```json
{
  "detail": "Missing required columns: Vulnerability ID, Title"
}
```

#### Phase 2 Health Check

```http
GET /api/phase2/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "phase2"
}
```

---

## Error Handling

### Error Response Format

```json
{
  "detail": "Human-readable error message"
}
```

### Common Errors

#### File Type Not Allowed

**Status:** 400

```json
{
  "detail": "File type '.txt' is not allowed. Allowed types: .docx"
}
```

#### File Too Large

**Status:** 400

```json
{
  "detail": "File size (52428800 bytes) exceeds maximum allowed (50000000 bytes / 50 MB)"
}
```

#### Missing Required Columns

**Status:** 400

```json
{
  "detail": "Missing required columns: Vulnerability ID, Title, Description"
}
```

#### Invalid Vulnerability ID

**Status:** 400

```json
{
  "detail": "Invalid vulnerability ID format: 'X1'. Expected format: [C|H|M|L|I]<number> (e.g., H1, M2)"
}
```

#### Corrupted Template

**Status:** 400

```json
{
  "detail": "File is not a valid Word document (corrupted or wrong format)"
}
```

#### Internal Server Error

**Status:** 500

```json
{
  "detail": "Failed to process document: Unexpected error occurred"
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production:

- Implement rate limiting middleware
- Recommended: 100 requests per minute per IP
- Use tools like: slowapi, fastapi-limiter

---

## File Size Limits

**Default Limits:**
- Maximum file size: 50 MB
- Configurable via `MAX_FILE_SIZE_MB` environment variable

**To Change:**
```bash
# In .env file
MAX_FILE_SIZE_MB=100
```

---

## Interactive Documentation

### Swagger UI

Visit: `http://localhost:8000/docs`

Features:
- Try endpoints directly
- View request/response schemas
- Download OpenAPI specification

### ReDoc

Visit: `http://localhost:8000/redoc`

Features:
- Alternative documentation view
- Clean, readable format
- Export to PDF

---

## OpenAPI Specification

Download the OpenAPI (Swagger) specification:

```http
GET /openapi.json
```

Use this for:
- Code generation
- API testing tools
- Import into Postman/Insomnia

---

## Best Practices

### File Uploads

1. **Validate file type** before upload
2. **Check file size** to avoid timeout
3. **Use descriptive filenames** for tracking
4. **Handle errors gracefully** with try-catch

### Error Handling

```python
try:
    response = requests.post(url, files=files)
    response.raise_for_status()  # Raises exception for 4xx/5xx
    
    with open('output.docx', 'wb') as f:
        f.write(response.content)
        
except requests.exceptions.HTTPError as e:
    print(f"API Error: {e.response.json()['detail']}")
except requests.exceptions.ConnectionError:
    print("Failed to connect to server")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Large Files

For large files, increase timeout:

```python
response = requests.post(
    url,
    files=files,
    timeout=300  # 5 minutes
)
```

### Concurrent Requests

The API handles concurrent requests. For batch processing:

```python
from concurrent.futures import ThreadPoolExecutor
import requests

def process_file(filepath):
    with open(filepath, 'rb') as f:
        files = {'docx_file': f}
        response = requests.post(url, files=files)
        return response.content

# Process multiple files concurrently
with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(process_file, file_list)
```

---

## Versioning

Current version: `0.1.0`

API versioning may be added in future releases:
- `/api/v1/phase1/parse`
- `/api/v2/phase1/parse`

---

## Support

For issues or questions:
- Check logs: `logs/app.log`
- Review documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health
