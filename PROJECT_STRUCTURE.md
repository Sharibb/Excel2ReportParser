# Project Structure

Complete overview of the Vulnerability Report Automation Service project structure.

## 📁 Root Directory

```
ReportExcel2Doc/
│
├── 📁 app/                          # Backend FastAPI application
├── 📁 frontend/                     # Frontend Flask application
├── 📁 uploads/                      # Backend temporary uploads
├── 📁 output/                       # Backend generated files
├── 📁 templates/                    # Word templates storage
├── 📁 logs/                         # Application logs
│
├── 📄 docker-compose.yml            # Docker orchestration
├── 📄 Dockerfile                    # Backend container
├── 📄 pyproject.toml                # Python dependencies (Poetry)
├── 📄 poetry.lock                   # Locked dependencies
│
├── 📄 .env.example                  # Environment variables template
├── 📄 .dockerignore                 # Docker ignore patterns
├── 📄 .gitignore                    # Git ignore patterns
│
├── 📘 README.md                     # Main documentation
├── 📘 QUICKSTART.md                 # Quick start guide
├── 📘 DOCKER_DEPLOYMENT.md          # Docker deployment guide
├── 📘 PROJECT_STRUCTURE.md          # This file
├── 📘 BUGFIX_SUMMARY_TABLE_ROOT_CAUSE.md  # Bug fix documentation
│
└── 📁 various test scripts/         # Development and testing scripts
```

## 🔧 Backend Structure (`/app`)

```
app/
│
├── 📄 main.py                       # FastAPI application entry point
├── 📄 __init__.py
│
├── 📁 api/                          # API layer
│   ├── 📄 __init__.py
│   └── 📁 routes/                   # API endpoints
│       ├── 📄 __init__.py
│       ├── 📄 phase1.py            # Phase 1: Word → Excel
│       ├── 📄 phase2.py            # Phase 2: Excel → Word
│       └── 📄 cleanup.py           # Cache management
│
├── 📁 services/                     # Business logic layer
│   ├── 📄 __init__.py
│   ├── 📁 phase1/                  # Phase 1 services
│   │   ├── 📄 __init__.py
│   │   ├── 📄 word_parser.py       # Word document parsing
│   │   └── 📄 excel_generator.py   # Excel generation
│   └── 📁 phase2/                  # Phase 2 services
│       ├── 📄 __init__.py
│       ├── 📄 excel_reader.py      # Excel data reading
│       └── 📄 word_generator.py    # Word document generation
│
├── 📁 models/                       # Data models
│   ├── 📄 __init__.py
│   └── 📄 vulnerability.py         # Pydantic models
│
├── 📁 core/                         # Core functionality
│   ├── 📄 __init__.py
│   ├── 📄 config.py                # Configuration management
│   ├── 📄 logging.py               # Logging setup
│   └── 📄 exceptions.py            # Custom exceptions
│
└── 📁 utils/                        # Utility functions
    ├── 📄 __init__.py
    ├── 📄 file_utils.py            # File handling utilities
    └── 📄 validators.py            # Input validation
```

## 🌐 Frontend Structure (`/frontend`)

```
frontend/
│
├── 📄 app.py                        # Flask application
├── 📄 requirements.txt              # Python dependencies
├── 📄 Dockerfile                    # Frontend container
├── 📄 .dockerignore                 # Docker ignore patterns
├── 📘 README.md                     # Frontend documentation
│
├── 📁 templates/                    # HTML templates
│   ├── 📄 base.html                # Base layout with nav
│   ├── 📄 index.html               # Landing page
│   ├── 📄 phase1.html              # Phase 1 interface
│   └── 📄 phase2.html              # Phase 2 interface
│
├── 📁 uploads/                      # Temporary file uploads
└── 📁 downloads/                    # Generated files for download
```

## 🐳 Docker Configuration

### docker-compose.yml

Orchestrates two services:

```yaml
services:
  backend:                           # FastAPI service
    - Port: 8000
    - Volumes: uploads, output, templates, logs
    - Health check: /health endpoint
  
  frontend:                          # Flask service
    - Port: 5000
    - Depends on: backend
    - Health check: /health endpoint
  
networks:
  app-network:                       # Shared network
```

### Backend Dockerfile

- Base: `python:3.11-slim`
- Package manager: Poetry
- User: Non-root (appuser)
- Exposed port: 8000
- Command: `uvicorn app.main:app`

### Frontend Dockerfile

- Base: `python:3.11-slim`
- Package manager: pip
- User: Non-root (appuser)
- Exposed port: 5000
- Command: `gunicorn app:app`

## 📊 Data Flow

### Phase 1: Word → Excel

```
User (Frontend)
    │
    ├─ Upload: report.docx
    ▼
Frontend (Flask)
    │
    ├─ POST /api/phase1/parse
    ▼
Backend (FastAPI)
    │
    ├─ Save to uploads/
    ├─ WordParser.parse()
    ├─ ExcelGenerator.generate()
    ├─ Save to output/
    ▼
Frontend
    │
    ├─ Receive Excel file
    ▼
User
    │
    └─ Download: report_vulnerabilities.xlsx
```

### Phase 2: Excel → Word

```
User (Frontend)
    │
    ├─ Upload: data.xlsx + template.docx
    ├─ Optional: POC folder path
    ▼
Frontend (Flask)
    │
    ├─ POST /api/phase2/generate
    ▼
Backend (FastAPI)
    │
    ├─ Save to uploads/
    ├─ ExcelReader.read()
    ├─ WordGenerator.generate()
    │   ├─ Load template
    │   ├─ Duplicate tables (XML level)
    │   ├─ Replace placeholders
    │   └─ Insert POC images
    ├─ Save to output/
    ▼
Frontend
    │
    ├─ Receive Word file
    ▼
User
    │
    └─ Download: template_generated.docx
```

## 🔄 File Lifecycle

### Temporary Files (Auto-cleanup)

```
uploads/              # Cleaned after processing
  ├─ backend/         # Backend API uploads (deleted after use)
  └─ frontend/        # Frontend uploads (deleted after forwarding)

downloads/            # Cleaned by frontend (keeps last 10)
  └─ *.xlsx, *.docx   # Generated files for user download
```

### Persistent Files

```
output/               # Backend generated files (persistent)
  ├─ *_vulnerabilities.xlsx
  └─ *_generated.docx

templates/            # User templates (persistent)
  └─ *.docx

logs/                 # Application logs (persistent)
  └─ app.log
```

## 🔌 API Endpoints

### Frontend Routes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Landing page |
| GET | `/phase1` | Phase 1 interface |
| GET | `/phase2` | Phase 2 interface |
| GET | `/health` | Frontend health check |
| POST | `/api/phase1/parse` | Proxy to backend |
| POST | `/api/phase2/generate` | Proxy to backend |
| GET | `/download/<filename>` | Download generated files |

### Backend API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Service info |
| GET | `/health` | Backend health check |
| GET | `/info` | Service configuration |
| GET | `/docs` | Interactive API docs |
| POST | `/api/phase1/parse` | Parse Word → Excel |
| GET | `/api/phase1/health` | Phase 1 health |
| POST | `/api/phase2/generate` | Generate Excel → Word |
| GET | `/api/phase2/health` | Phase 2 health |
| GET | `/api/cleanup/cache-info` | Cache information |
| POST | `/api/cleanup/purge-cache` | Purge cache |

## 🔐 Security Layers

### Frontend Security

- ✅ File type validation
- ✅ File size limits (100MB)
- ✅ Filename sanitization
- ✅ MIME type checking
- ✅ CSRF protection (Flask)
- ✅ Secure file handling

### Backend Security

- ✅ Path traversal prevention
- ✅ Input validation (Pydantic)
- ✅ File type validation
- ✅ CORS configuration
- ✅ Request size limits
- ✅ Error sanitization

## 📝 Configuration Files

### Environment Variables

```bash
# Backend
APP_NAME=Vulnerability Report Automation Service
APP_VERSION=0.1.0
DEBUG=False
HOST=0.0.0.0
PORT=8000
MAX_FILE_SIZE_MB=100
LOG_LEVEL=INFO

# Frontend
BACKEND_URL=http://backend:8000
SECRET_KEY=change-me-in-production
PORT=5000
```

### pyproject.toml (Backend)

- Package management: Poetry
- Python version: ^3.11
- Key dependencies:
  - fastapi
  - uvicorn
  - python-docx
  - openpyxl
  - pydantic
  - python-multipart

### requirements.txt (Frontend)

- Package management: pip
- Key dependencies:
  - Flask
  - requests
  - Werkzeug
  - gunicorn

## 🏃 Running the Project

### Development Mode

```bash
# Backend only
poetry run uvicorn app.main:app --reload

# Frontend only
cd frontend && python app.py

# Both with Docker
docker-compose up
```

### Production Mode

```bash
# With Docker Compose (recommended)
docker-compose up -d

# Manual
# Backend: gunicorn + uvicorn workers
# Frontend: gunicorn + flask app
```

## 📦 Volumes

### Docker Volumes

```yaml
Backend volumes:
  - ./uploads:/app/uploads          # Temporary uploads
  - ./output:/app/output            # Generated files
  - ./templates:/app/templates      # Templates
  - ./logs:/app/logs                # Logs

Frontend volumes:
  - ./frontend/uploads:/app/uploads    # Temporary uploads
  - ./frontend/downloads:/app/downloads # Downloads
```

## 🔍 Monitoring

### Health Checks

```bash
# Frontend
curl http://localhost:5000/health
# Returns: {status, frontend, backend, backend_url}

# Backend
curl http://localhost:8000/health
# Returns: {status, service}

# Docker health
docker-compose ps
```

### Logs

```bash
# Docker logs
docker-compose logs -f

# Application logs
tail -f logs/app.log

# Service-specific
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 🧪 Testing

### Test Scripts

```
project_root/
├── test_full_generation.py      # Full Phase 2 test
├── test_generation.py           # Generation test
├── diagnose_*.py                # Diagnostic scripts
├── debug_*.py                   # Debug utilities
└── check_*.py                   # Validation scripts
```

## 📚 Documentation Files

```
project_root/
├── README.md                          # Main documentation
├── QUICKSTART.md                      # 5-minute setup
├── DOCKER_DEPLOYMENT.md               # Docker guide
├── PROJECT_STRUCTURE.md               # This file
├── BUGFIX_SUMMARY_TABLE_ROOT_CAUSE.md # Bug fixes
├── QUICK_FIX_SUMMARY.txt             # Recent fixes
└── frontend/
    └── README.md                      # Frontend docs
```

## 🎯 Key Design Patterns

### Backend

- **Layered Architecture**: API → Services → Core
- **Dependency Injection**: Services injected into routes
- **Repository Pattern**: Data access abstraction
- **Factory Pattern**: Model creation
- **Exception Handling**: Custom exception hierarchy

### Frontend

- **MVC Pattern**: Models (backend) → Views (templates) → Controller (app.py)
- **Proxy Pattern**: Frontend proxies to backend API
- **Template Inheritance**: base.html → specific pages

## 🚀 Deployment Checklist

- [ ] Set `SECRET_KEY` in environment
- [ ] Set `DEBUG=False`
- [ ] Configure CORS properly
- [ ] Set up HTTPS (reverse proxy)
- [ ] Configure firewall rules
- [ ] Set up log rotation
- [ ] Configure backup strategy
- [ ] Test health checks
- [ ] Monitor resource usage
- [ ] Set up alerts

## 📊 Performance Considerations

### Backend

- Workers: Configured in uvicorn/gunicorn
- Async: FastAPI endpoints are async
- Connection pooling: Not needed (stateless)
- Caching: File-based (uploads/output)

### Frontend

- Workers: 4 gunicorn workers default
- Static files: Served by Flask
- Session: File-based (Flask)
- Cleanup: Auto-cleanup old files

## 🔄 CI/CD Considerations

### Build

```bash
# Backend
docker build -t backend:latest .

# Frontend
docker build -t frontend:latest ./frontend

# Both
docker-compose build
```

### Test

```bash
# Backend tests
poetry run pytest

# Integration tests
# Start services and run test suite
```

### Deploy

```bash
# Production
docker-compose -f docker-compose.prod.yml up -d

# With registry
docker tag backend registry.example.com/backend:latest
docker push registry.example.com/backend:latest
```

---

## Summary

This project follows a clean microservices architecture with:

✅ **Separation of Concerns**: Frontend (UI) ↔ Backend (Logic)  
✅ **Containerization**: Each service in its own container  
✅ **Orchestration**: Docker Compose for multi-service management  
✅ **Modularity**: Clean code structure with clear responsibilities  
✅ **Documentation**: Comprehensive docs at every level  
✅ **Production Ready**: Health checks, logging, error handling  
✅ **Developer Friendly**: Easy setup, clear structure, good docs  

**Navigate the codebase with confidence!** 🎯
