# Testing Guide

## Manual Testing

### Prerequisites

1. Start the application:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

2. Access API documentation: http://localhost:8000/docs

### Test Phase 1: Word → Excel

1. **Prepare Test Document**
   - Use your existing `WAPT-Rootnik-Technical.docx` file
   - Or create a new Word document with vulnerability data

2. **Test via API Documentation**
   - Navigate to http://localhost:8000/docs
   - Find `/api/phase1/parse` endpoint
   - Click "Try it out"
   - Upload your .docx file
   - Click "Execute"
   - Download the generated Excel file

3. **Test via cURL**
   ```bash
   curl -X POST "http://localhost:8000/api/phase1/parse" \
     -H "Content-Type: multipart/form-data" \
     -F "docx_file=@WAPT-Rootnik-Technical.docx" \
     --output vulnerabilities.xlsx
   ```

4. **Verify Results**
   - Open generated Excel file
   - Check all vulnerabilities are extracted
   - Verify data accuracy
   - Check column headers match template

### Test Phase 2: Excel → Word

1. **Prepare Test Files**
   - Excel file (from Phase 1 or create manually)
   - Word template with placeholders
   - PoC images folder (optional)

2. **Create Simple Template**
   
   Create `test_template.docx` with content:
   ```
   VULNERABILITY REPORT
   
   Total Vulnerabilities: {{TOTAL_VULNS}}
   Critical: {{CRITICAL_COUNT}}
   High: {{HIGH_COUNT}}
   Medium: {{MEDIUM_COUNT}}
   Low: {{LOW_COUNT}}
   
   FINDINGS
   
   [Create a table:]
   | Field          | Value                    |
   |----------------|--------------------------|
   | ID             | {{VULN_ID}}             |
   | Title          | {{TITLE}}               |
   | Risk           | {{RISK_LEVEL}}          |
   | CVSS           | {{CVSS_SCORE}}          |
   | Description    | {{DESCRIPTION}}         |
   | Affected       | {{AFFECTED_COMPONENTS}} |
   | Recommendation | {{RECOMMENDATION}}      |
   | PoC            | {{POC}}                 |
   ```

3. **Test via API Documentation**
   - Navigate to http://localhost:8000/docs
   - Find `/api/phase2/generate` endpoint
   - Click "Try it out"
   - Upload Excel file
   - Upload template file
   - (Optional) Provide PoC folder path
   - Click "Execute"
   - Download generated Word document

4. **Test via cURL**
   ```bash
   curl -X POST "http://localhost:8000/api/phase2/generate" \
     -H "Content-Type: multipart/form-data" \
     -F "excel_file=@vulnerabilities.xlsx" \
     -F "template_file=@test_template.docx" \
     -F "poc_folder=./poc_images" \
     --output generated_report.docx
   ```

5. **Verify Results**
   - Open generated Word document
   - Check all vulnerabilities appear
   - Verify formatting is preserved
   - Check PoC images are inserted (if provided)
   - Verify counts are correct

## Automated Testing

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov-report=html

# Run specific test file
poetry run pytest tests/test_word_parser.py

# Run with verbose output
poetry run pytest -v

# Run specific test
poetry run pytest tests/test_word_parser.py::test_parse_vulnerability_table
```

### Test Structure

Create test files in `tests/` directory:

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_word_parser.py      # Phase 1 parsing tests
├── test_excel_generator.py  # Phase 1 Excel generation tests
├── test_excel_reader.py     # Phase 2 Excel reading tests
├── test_word_generator.py   # Phase 2 Word generation tests
├── test_validators.py       # Validation tests
├── test_api_phase1.py       # Phase 1 API tests
└── test_api_phase2.py       # Phase 2 API tests
```

### Sample Test File

Create `tests/conftest.py`:

```python
"""Shared test fixtures."""

import pytest
from pathlib import Path
from fastapi.testclient import TestClient

from app.main import app
from app.models.vulnerability import Vulnerability, RiskLevel


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def sample_vulnerability():
    """Sample vulnerability for testing."""
    return Vulnerability(
        vuln_id="H1",
        title="SQL Injection",
        description="SQL injection in login form",
        risk_level=RiskLevel.HIGH,
        cvss_score=8.5,
        affected_components="Login API",
        recommendation="Use parameterized queries",
    )


@pytest.fixture
def test_data_dir():
    """Test data directory."""
    return Path(__file__).parent / "test_data"
```

Create `tests/test_api_phase1.py`:

```python
"""Tests for Phase 1 API endpoints."""

import pytest
from pathlib import Path


def test_health_check(client):
    """Test Phase 1 health check endpoint."""
    response = client.get("/api/phase1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_parse_endpoint_no_file(client):
    """Test parse endpoint without file."""
    response = client.post("/api/phase1/parse")
    assert response.status_code == 422  # Validation error


def test_parse_endpoint_invalid_file(client):
    """Test parse endpoint with invalid file type."""
    files = {"docx_file": ("test.txt", b"not a docx", "text/plain")}
    response = client.post("/api/phase1/parse", files=files)
    assert response.status_code == 400
```

## Integration Testing

### End-to-End Test

1. **Phase 1 → Phase 2 Flow**
   ```bash
   # Step 1: Parse Word to Excel
   curl -X POST "http://localhost:8000/api/phase1/parse" \
     -F "docx_file=@test_report.docx" \
     --output test_data.xlsx
   
   # Step 2: Generate Word from Excel
   curl -X POST "http://localhost:8000/api/phase2/generate" \
     -F "excel_file=@test_data.xlsx" \
     -F "template_file=@template.docx" \
     --output final_report.docx
   
   # Step 3: Verify final document
   # Open final_report.docx and verify content
   ```

## Performance Testing

### Load Testing with Apache Bench

```bash
# Install apache2-utils
sudo apt-get install apache2-utils

# Test Phase 1 endpoint (adjust file path)
ab -n 10 -c 2 -p request.txt -T 'multipart/form-data; boundary=----WebKitFormBoundary' \
  http://localhost:8000/api/phase1/parse
```

### Load Testing with Locust

Create `locustfile.py`:

```python
from locust import HttpUser, task, between

class VulnerabilityReportUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def health_check(self):
        self.client.get("/health")
    
    @task
    def parse_document(self):
        files = {
            'docx_file': ('test.docx', open('test.docx', 'rb'), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        }
        self.client.post("/api/phase1/parse", files=files)
```

Run:
```bash
poetry add --group dev locust
poetry run locust -f locustfile.py
```

## Testing Checklist

### Phase 1 Testing
- [ ] Parse document with tables
- [ ] Parse document with sections
- [ ] Extract vulnerability IDs correctly
- [ ] Handle missing fields gracefully
- [ ] Generate valid Excel file
- [ ] Excel has correct column headers
- [ ] All vulnerabilities extracted
- [ ] Counts calculated correctly

### Phase 2 Testing
- [ ] Read Excel with all columns
- [ ] Read Excel with missing optional columns
- [ ] Validate required columns
- [ ] Load template successfully
- [ ] Find vulnerability table template
- [ ] Duplicate table correctly
- [ ] Preserve table formatting
- [ ] Replace all placeholders
- [ ] Insert PoC images
- [ ] Handle missing PoC images gracefully
- [ ] Generate valid Word document
- [ ] Template structure unchanged

### API Testing
- [ ] Health checks respond
- [ ] File upload validation works
- [ ] File size limits enforced
- [ ] MIME type validation works
- [ ] Error responses are structured
- [ ] Files are cleaned up after processing
- [ ] Concurrent requests handled

### Security Testing
- [ ] Path traversal prevented
- [ ] Invalid file types rejected
- [ ] File size limits work
- [ ] No code execution in documents
- [ ] Temporary files cleaned up
- [ ] Errors don't leak sensitive info

## Continuous Integration

### GitHub Actions

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install Poetry
      run: pip install poetry
    
    - name: Install dependencies
      run: poetry install
    
    - name: Run tests
      run: poetry run pytest --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## Troubleshooting Tests

### Common Issues

1. **Import Errors**
   - Ensure you're in the project root
   - Run `poetry install`
   - Check Python path

2. **File Not Found**
   - Use `Path(__file__).parent` for relative paths
   - Ensure test data files exist

3. **Async Errors**
   - Install `pytest-asyncio`
   - Mark async tests with `@pytest.mark.asyncio`

4. **Fixture Errors**
   - Check fixture names match
   - Ensure `conftest.py` is in correct location
