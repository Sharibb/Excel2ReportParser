# 🔐 Vulnerability Report Automation Service

> **Production-grade FastAPI service for automating vulnerability report processing**

Transform your vulnerability reporting workflow with automated parsing, standardization, and professional report generation.

---

## ⚡ Quick Start

### 🐳 With Docker (Recommended)

**Get the full stack running with web UI:**

```bash
# Start both frontend and backend
docker-compose up -d

# Open your browser
# Frontend: http://localhost:5000
# Backend API: http://localhost:8000/docs
```

### 🐍 Backend Only (Development)

**Run just the API service:**

```bash
# Install dependencies
poetry install

# Start the service
poetry run uvicorn app.main:app --reload

# Open your browser
# http://localhost:8000/docs
```

👉 **New here?** Start with [`QUICKSTART.md`](QUICKSTART.md) for Docker setup

---

## ✨ Features

### 📥 Phase 1: Download Excel Template

**Get the standardized Excel template for vulnerability reporting:**

- ✅ Pre-configured columns for all fields
- ✅ Support for all risk levels (Critical, High, Medium, Low, Info)
- ✅ CVSS score and CWE ID columns
- ✅ PoC folder and steps tracking
- ✅ Affected components and recommendations
- ✅ Ready-to-fill format
- ✅ Compatible with Phase 2

**What You Get:** `All_Risk_Levels_Template.xlsx`  
**Next Step:** Fill with your data and use in Phase 2

### 📄 Phase 2: Excel → Word Generation

**Generate professional reports from Excel data:**

- ✅ Ingest structured Excel files
- ✅ Populate Word templates with data
- ✅ **Duplicate tables WITHOUT recreating them** (preserves formatting)
- ✅ Insert PoC images from manual folder path
- ✅ **NEW: Insert PoC images inside text boxes** (better layout control)
- ✅ Replace placeholders intelligently
- ✅ Maintain all template styles and formatting
- ✅ Support custom branding and layouts

**Input:** Excel data + Word template + PoC folder path (optional)  
**Output:** Professional Word report ready for delivery

### ⭐ Phase 3: Complete Report with PoC ZIP

**Automated report generation with ZIP-based PoC handling:**

- ✅ All Phase 2 features included
- ✅ Upload PoC screenshots as ZIP file
- ✅ Automatic ZIP extraction
- ✅ Automatic PoC folder mapping to vulnerability IDs
- ✅ No manual path specification needed
- ✅ Self-contained portable packages
- ✅ One-click complete report generation

**Input:** Excel data + Word template + PoC ZIP file  
**Output:** Professional Word report with all PoCs automatically inserted

**ZIP Structure:**
```
POC.zip
└── POC/
    ├── C1/     (Critical 1)
    │   ├── 1.png   ← Step 1 image
    │   └── 2.png   ← Step 2 image
    ├── H1/     (High 1)
    │   └── 1.png   ← Step 1 image
    └── M1/     (Medium 1)
        └── 1.png   ← Step 1 image
```

**How PoC Mapping Works:**
- Each step in Excel (delimited by `;`) maps to a numbered image
- Step 1 text → `1.png`, Step 2 text → `2.png`, etc.
- Example Excel row: `Steps: Navigate; Enter payload; Submit`
  - Generates: "Step 1: Navigate" + `1.png`, "Step 2: Enter payload" + `2.png`, "Step 3: Submit" + `3.png`

---

## 🎯 Use Cases

1. **Standardize Multiple Reports**  
   Convert various report formats into a single standardized template

2. **Quick Data Extraction**  
   Extract vulnerability data from Word docs into Excel for analysis

3. **Rebranding Reports**  
   Apply new company branding to existing vulnerability data

4. **Add PoC Images**  
   Automatically insert proof-of-concept screenshots into reports

5. **Batch Processing**  
   Process multiple reports programmatically

---

## 🏗️ Architecture

**Full-stack application with clean separation:**

```
┌─────────────────────────────────────────┐
│         Frontend (Flask)                │
│    Web UI • File uploads • Downloads    │
│         http://localhost:5000           │
└──────────────┬──────────────────────────┘
               │ REST API
┌──────────────▼──────────────────────────┐
│         Backend (FastAPI)               │
│  Phase 1 & 2 • Processing • Validation  │
│         http://localhost:8000           │
└─────────────────────────────────────────┘
```

**Backend Structure (FastAPI):**

```
app/
├── main.py                      # FastAPI application
├── api/routes/                  # API endpoints
│   ├── phase1.py               # Word → Excel
│   ├── phase2.py               # Excel → Word
│   └── cleanup.py              # Cache management
├── services/                    # Business logic
│   ├── phase1/                 # Parsing services
│   │   ├── word_parser.py
│   │   └── excel_generator.py
│   └── phase2/                 # Generation services
│       ├── excel_reader.py
│       └── word_generator.py
├── core/                        # Core functionality
│   ├── config.py               # Settings
│   ├── logging.py              # Structured logging
│   └── exceptions.py           # Custom errors
├── models/                      # Data models
│   └── vulnerability.py        # Pydantic schemas
└── utils/                       # Utilities
    ├── file_utils.py
    └── validators.py
```

**Frontend Structure (Flask):**

```
frontend/
├── app.py                       # Flask application
├── templates/                   # HTML templates
│   ├── base.html               # Base layout
│   ├── index.html              # Landing page
│   ├── phase1.html             # Phase 1 UI
│   └── phase2.html             # Phase 2 UI
├── uploads/                     # Temporary uploads
├── downloads/                   # Generated files
└── Dockerfile                   # Container config
```

**Key Principles:**
- ✅ Microservices architecture
- ✅ Separation of concerns
- ✅ RESTful API design
- ✅ Type safety (Pydantic)
- ✅ Comprehensive logging
- ✅ Graceful error handling
- ✅ Docker containerization

📖 **Learn more:** [`DOCKER_DEPLOYMENT.md`](DOCKER_DEPLOYMENT.md)

---

## 🚀 Installation & Setup

### Option 1: Docker (Recommended)

**Full-stack with web UI:**

#### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+

#### Installation

```bash
# 1. Create required directories
mkdir -p uploads output templates logs
mkdir -p frontend/uploads frontend/downloads

# 2. Start services
docker-compose up -d

# 3. Access application
# Frontend: http://localhost:5000
# Backend:  http://localhost:8000
# API Docs: http://localhost:8000/docs
```

📖 **Docker guide:** [`QUICKSTART.md`](QUICKSTART.md) and [`DOCKER_DEPLOYMENT.md`](DOCKER_DEPLOYMENT.md)

### Option 2: Local Development

**Backend only (Python):**

#### Prerequisites
- Python 3.11+
- Poetry (recommended) or pip

#### Installation

```bash
# 1. Install Poetry (if needed)
curl -sSL https://install.python-poetry.org | python3 -

# 2. Install dependencies
poetry install

# 3. Run the backend
poetry run uvicorn app.main:app --reload

# 4. (Optional) Run frontend separately
cd frontend
pip install -r requirements.txt
python app.py
```

### Configuration (Optional)

```bash
# Copy environment template
cp .env.example .env

# Edit settings
nano .env
```

**Default settings work out of the box!**

---

## 📡 API Endpoints

### Web Interface (Frontend)

**Access the user-friendly web interface:**

- **Landing Page:** http://localhost:5000
- **Phase 1 (Get Templates):** http://localhost:5000/phase1
- **Phase 2 (Excel + Template + Manual PoC):** http://localhost:5000/phase2
- **Phase 3 (Excel + Template + PoC ZIP):** http://localhost:5000/phase3
- **Health Check:** http://localhost:5000/health

Features:
- ✅ Drag & drop file uploads
- ✅ Progress indicators
- ✅ Direct file downloads
- ✅ Responsive Bootstrap UI
- ✅ Real-time error messages

### Backend API Documentation

Visit **http://localhost:8000/docs** for interactive API testing

### Phase 1: Parse Word Document

```http
POST /api/phase1/parse
```

**Upload:** Word document (.docx)  
**Returns:** Excel file with extracted vulnerabilities

**Example:**
```bash
curl -X POST "http://localhost:8000/api/phase1/parse" \
  -F "docx_file=@report.docx" \
  --output vulnerabilities.xlsx
```

### Phase 2: Generate Word Report

```http
POST /api/phase2/generate
```

**Upload:**
- Excel file (.xlsx)
- Template file (.docx)
- PoC folder path (optional)

**Returns:** Generated Word document

**Example:**
```bash
curl -X POST "http://localhost:8000/api/phase2/generate" \
  -F "excel_file=@vulnerabilities.xlsx" \
  -F "template_file=@template.docx" \
  -F "poc_folder=./poc_images" \
  --output final_report.docx
```

### Phase 3: Generate with PoC ZIP

```http
POST /api/phase3/generate
```

**Upload:**
- Excel file (.xlsx)
- Template file (.docx)
- PoC ZIP file (.zip with C1/, H1/, M1/ folders)

**Returns:** Generated Word document with all PoCs

**Example:**
```bash
curl -X POST "http://localhost:8000/api/phase3/generate" \
  -F "excel_file=@vulnerabilities.xlsx" \
  -F "template_file=@template.docx" \
  -F "poc_zip=@poc_screenshots.zip" \
  --output complete_report.docx
```

### Cache Management

```http
GET /api/cleanup/cache-info
POST /api/cleanup/purge-cache
```

**Check cache status:**
```bash
curl "http://localhost:8000/api/cleanup/cache-info"
```

**Purge all cached files:**
```bash
curl -X POST "http://localhost:8000/api/cleanup/purge-cache"
```

🗑️ **Cache cleanup guide:** [`CACHE_CLEANUP_GUIDE.md`](CACHE_CLEANUP_GUIDE.md)

📖 **Full API reference:** [`API.md`](API.md)

---

## 📊 Excel Schema

### Required Columns

| Column | Description | Example |
|--------|-------------|---------|
| Vulnerability ID | Format: [C\|H\|M\|L\|I]<number> | H1, M2, L3 |
| Title | Short vulnerability name | SQL Injection |
| Description | Detailed description | The application... |
| Risk Level | Severity level | High, Medium, Low |
| Affected Components | Systems affected | Login API |
| Recommendation | Fix instructions | Use parameterized... |

### Optional Columns

| Column | Description | Example |
|--------|-------------|---------|
| CVSS Score | Score 0.0-10.0 | 7.5 |
| POC_Folder | PoC image folder | H1_SQLi |
| Steps | Semicolon-delimited steps | Navigate; Enter payload; Submit; Observe |
| CWE ID | CWE reference | CWE-89 |
| Impact | Security impact | Complete authentication bypass |
| References | External links | https://owasp.org/... |

📖 **Detailed schema:** [`templates/SAMPLE_EXCEL_FORMAT.md`](templates/SAMPLE_EXCEL_FORMAT.md)  
📖 **Migration guide:** [`STEPS_COLUMN_UPDATE.md`](STEPS_COLUMN_UPDATE.md)

---

## 📝 Template Guide

### Creating Templates

1. Design your Word template
2. Add placeholders: `{{VULN_ID}}`, `{{TITLE}}`, etc.
3. Create vulnerability table (will be duplicated)
4. Upload to Phase 2 API

**Available Placeholders:**

**Global:**
- `{{TOTAL_VULNS}}`, `{{HIGH_COUNT}}`, `{{MEDIUM_COUNT}}`, etc.

**Per Vulnerability:**
- `{{VULN_ID}}`, `{{TITLE}}`, `{{DESCRIPTION}}`
- `{{RISK_LEVEL}}`, `{{CVSS_SCORE}}`
- `{{AFFECTED_COMPONENTS}}`, `{{RECOMMENDATION}}`
- `{{POC}}` (for images - can be in text boxes for better control)

📖 **Template guide:** [`templates/TEMPLATE_GUIDE.md`](templates/TEMPLATE_GUIDE.md)  
📖 **Text box feature:** [`TEXTBOX_POC_FEATURE.md`](TEXTBOX_POC_FEATURE.md)

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
poetry run pytest

# With coverage
poetry run pytest --cov=app

# Specific test
poetry run pytest tests/test_word_parser.py
```

### Manual Testing

```bash
# Start server
poetry run uvicorn app.main:app --reload

# Visit interactive docs
# http://localhost:8000/docs
```

📖 **Testing guide:** [`TESTING.md`](TESTING.md)

---

## 🚢 Deployment

### Docker Deployment (Recommended)

**Deploy full stack with one command:**

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Services:**
- Frontend: http://localhost:5000
- Backend: http://localhost:8000
- Healthchecks: Automatic monitoring
- Volumes: Persistent data storage

### Production Considerations

1. **Change secret keys** in `.env`
2. **Use HTTPS** with reverse proxy (nginx)
3. **Enable firewall** rules
4. **Monitor logs** in `./logs/`
5. **Backup volumes** regularly

📖 **Deployment guide:** [`DOCKER_DEPLOYMENT.md`](DOCKER_DEPLOYMENT.md)

### Manual Backend Deployment

```bash
# Using Gunicorn (backend only)
poetry run gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [`QUICKSTART.md`](QUICKSTART.md) | 🎯 **Start here** - Docker setup in 5 minutes |
| [`DOCKER_DEPLOYMENT.md`](DOCKER_DEPLOYMENT.md) | 🐳 Complete Docker deployment guide |
| [`frontend/README.md`](frontend/README.md) | 🌐 Frontend documentation |
| [`API.md`](API.md) | Complete API reference |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | System architecture and design |
| [`TESTING.md`](TESTING.md) | Testing guide and strategies |
| [`PROJECT_SUMMARY.md`](PROJECT_SUMMARY.md) | What's included in this project |
| [`CACHE_CLEANUP_GUIDE.md`](CACHE_CLEANUP_GUIDE.md) | 🗑️ Cache management and cleanup |
| [`BUGFIX_SUMMARY_TABLE_ROOT_CAUSE.md`](BUGFIX_SUMMARY_TABLE_ROOT_CAUSE.md) | 🐛 Recent bug fixes |
| [`templates/TEMPLATE_GUIDE.md`](templates/TEMPLATE_GUIDE.md) | How to create Word templates |
| [`templates/SAMPLE_EXCEL_FORMAT.md`](templates/SAMPLE_EXCEL_FORMAT.md) | Excel format specification |

---

## 🛡️ Security Features

- ✅ File type validation
- ✅ File size limits
- ✅ Path traversal prevention
- ✅ Filename sanitization
- ✅ MIME type checking
- ✅ Secure temporary file handling
- ✅ Input validation (Pydantic)

---

## 🎯 Key Features

### What Makes This Special

1. **Template Safety**  
   NEVER recreates tables - duplicates at XML level preserving all formatting

2. **Flexible Parsing**  
   Extracts from tables AND text sections

3. **Graceful Degradation**  
   Continues processing even with missing optional data

4. **Production Ready**  
   Comprehensive logging, error handling, validation

5. **Developer Friendly**  
   Clean code, type hints, extensive documentation

6. **Cross-Platform**  
   Works on Windows, Linux, macOS

---

## 🤝 Contributing

This is an internal security tooling project. For improvements:

1. Follow PEP8 style guidelines
2. Add type hints to all functions
3. Write tests for new features
4. Update documentation
5. Log appropriately

---

## 📄 License

Internal Security Tooling - Proprietary

---

## 🆘 Support

- **Logs:** Check `logs/app.log` for details
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

---

## 🎉 Summary

**You have a complete, production-grade full-stack system that:**

✅ **Web UI** - Modern Flask frontend with drag & drop  
✅ **REST API** - FastAPI backend with comprehensive endpoints  
✅ **Phase 1** - Parses Word vulnerability reports to Excel  
✅ **Phase 2** - Generates Word reports from Excel using templates  
✅ **Template Safety** - Preserves all formatting perfectly  
✅ **PoC Images** - Handles screenshots automatically  
✅ **Validation** - Validates all inputs rigorously  
✅ **Logging** - Comprehensive logging for debugging  
✅ **Docker** - Fully containerized and orchestrated  
✅ **Health Checks** - Built-in monitoring  
✅ **Best Practices** - Clean code, type hints, modular design  
✅ **Documentation** - Extensive guides and references  
✅ **Production Ready** - Deploy with confidence  

**Happy Automating! 🚀**

---

## 🚀 Quick Commands

```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f

# Check health
curl http://localhost:5000/health

# Stop everything
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```
