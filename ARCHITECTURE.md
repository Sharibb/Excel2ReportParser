# System Architecture

## Overview

The Vulnerability Report Automation Service is built with a modular, layered architecture following clean code principles.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
│  (Browser, cURL, Python scripts, Postman, etc.)             │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      FASTAPI APPLICATION                     │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API ROUTES LAYER                        │  │
│  │  • /api/phase1/parse                                 │  │
│  │  • /api/phase2/generate                              │  │
│  │  • /health, /info, /docs                             │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                          │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │            VALIDATION LAYER                          │  │
│  │  • File type validation                              │  │
│  │  • File size validation                              │  │
│  │  • Pydantic models                                   │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                          │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │            SERVICES LAYER                            │  │
│  │                                                       │  │
│  │  Phase 1 Services:        Phase 2 Services:         │  │
│  │  • WordParser             • ExcelReader             │  │
│  │  • ExcelGenerator         • WordGenerator           │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                          │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │            CORE LAYER                                │  │
│  │  • Configuration (Settings)                          │  │
│  │  • Logging (Structured)                              │  │
│  │  • Exceptions (Custom)                               │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    EXTERNAL LIBRARIES                        │
│  • python-docx (Word processing)                            │
│  • openpyxl (Excel processing)                              │
│  • Pillow (Image processing)                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### Phase 1: Word → Excel

```
┌──────────────┐
│  Word File   │
│  (.docx)     │
└──────┬───────┘
       │
       │ Upload via API
       ▼
┌──────────────────────┐
│  Phase1 Route        │
│  /api/phase1/parse   │
└──────┬───────────────┘
       │
       │ 1. Validate file
       │ 2. Save temporarily
       ▼
┌──────────────────────┐
│  WordParser          │
│  Service             │
│                      │
│  • Load document     │
│  • Find tables       │
│  • Extract vulns     │
│  • Parse sections    │
│  • Deduplicate       │
└──────┬───────────────┘
       │
       │ VulnerabilityReport
       │ (Pydantic model)
       ▼
┌──────────────────────┐
│  ExcelGenerator      │
│  Service             │
│                      │
│  • Create workbook   │
│  • Add headers       │
│  • Write rows        │
│  • Format cells      │
└──────┬───────────────┘
       │
       │ Save to output/
       ▼
┌──────────────────────┐
│  Excel File          │
│  (.xlsx)             │
│                      │
│  Downloaded by user  │
└──────────────────────┘
```

### Phase 2: Excel → Word

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Excel File  │    │  Template    │    │  PoC Images  │
│  (.xlsx)     │    │  (.docx)     │    │  (optional)  │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                    │
       │                   │                    │
       └───────────────────┴────────────────────┘
                           │
                           │ Upload via API
                           ▼
                  ┌─────────────────────┐
                  │  Phase2 Route       │
                  │  /api/phase2/       │
                  │  generate           │
                  └─────────┬───────────┘
                            │
                            │ 1. Validate files
                            │ 2. Save temporarily
                            ▼
                  ┌─────────────────────┐
                  │  ExcelReader        │
                  │  Service            │
                  │                     │
                  │  • Load workbook    │
                  │  • Validate schema  │
                  │  • Parse rows       │
                  │  • Create models    │
                  └─────────┬───────────┘
                            │
                            │ VulnerabilityReport
                            ▼
                  ┌─────────────────────┐
                  │  WordGenerator      │
                  │  Service            │
                  │                     │
                  │  • Load template    │
                  │  • Find table       │
                  │  • Deep copy XML    │
                  │  • Duplicate table  │
                  │  • Replace text     │
                  │  • Insert images    │
                  └─────────┬───────────┘
                            │
                            │ Save to output/
                            ▼
                  ┌─────────────────────┐
                  │  Generated Word     │
                  │  (.docx)            │
                  │                     │
                  │  Downloaded by user │
                  └─────────────────────┘
```

---

## Module Responsibilities

### API Layer (`app/api/routes/`)

**Responsibilities:**
- Handle HTTP requests/responses
- Validate request parameters
- Call appropriate services
- Return formatted responses
- Handle file uploads/downloads
- Cleanup temporary files

**Does NOT:**
- Contain business logic
- Parse documents directly
- Generate files directly

### Services Layer (`app/services/`)

**Responsibilities:**
- Implement business logic
- Parse documents
- Generate files
- Transform data
- Coordinate operations

**Does NOT:**
- Handle HTTP directly
- Know about FastAPI
- Manage file uploads

### Core Layer (`app/core/`)

**Responsibilities:**
- Application configuration
- Logging setup
- Exception definitions
- Cross-cutting concerns

**Does NOT:**
- Contain business logic
- Parse documents

### Models Layer (`app/models/`)

**Responsibilities:**
- Define data structures
- Validate data
- Transform between formats
- Type safety

**Does NOT:**
- Contain business logic
- Know about services

### Utils Layer (`app/utils/`)

**Responsibilities:**
- Reusable utility functions
- File operations
- Validation helpers
- Common operations

**Does NOT:**
- Contain business logic specific to phases

---

## Key Design Patterns

### 1. Dependency Injection

Services are instantiated with their dependencies:

```python
# Service receives dependencies
parser = WordParser(docx_path)
report = parser.parse()

# Service is independent of how it's called
generator = ExcelGenerator()
generator.generate(report, output_path)
```

### 2. Single Responsibility

Each class has one clear purpose:

- `WordParser`: Only parses Word documents
- `ExcelGenerator`: Only generates Excel files
- `WordGenerator`: Only generates Word documents
- `ExcelReader`: Only reads Excel files

### 3. Strategy Pattern

Different parsing strategies for vulnerabilities:

- Table-based extraction
- Section-based extraction
- Automatic deduplication

### 4. Template Method

Word generation follows a template:

1. Validate template
2. Find vulnerability table
3. Clone table XML
4. Populate with data
5. Insert images
6. Replace placeholders

### 5. Factory Pattern

Pydantic models act as factories:

```python
# Create from Excel row
excel_row = VulnerabilityExcelRow(**row_data)
vulnerability = excel_row.to_vulnerability()
```

---

## Error Handling Strategy

```
┌─────────────────────────────────────────────────────────┐
│                    Error Hierarchy                       │
│                                                          │
│  AppBaseException (base)                                │
│  ├── ValidationError                                    │
│  │   ├── MissingRequiredColumnError                    │
│  │   ├── InvalidVulnerabilityFormatError               │
│  │   └── InvalidExcelStructureError                    │
│  ├── FileProcessingError                                │
│  ├── ParsingError                                       │
│  └── TemplateError                                      │
│      ├── CorruptedTemplateError                        │
│      └── TemplateMismatchError                         │
└─────────────────────────────────────────────────────────┘

Error Handling Rules:
├── Critical Errors → Fail Fast
│   • Corrupted template
│   • Missing required columns
│   • Invalid Excel structure
│
└── Recoverable Errors → Log & Continue
    • Missing PoC images
    • Missing optional fields
    • Minor formatting issues
```

---

## Security Layers

```
┌─────────────────────────────────────────────────────────┐
│  1. Input Validation                                     │
│     • File type checking                                 │
│     • MIME type validation                               │
│     • File size limits                                   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│  2. Path Security                                        │
│     • Filename sanitization                              │
│     • Path traversal prevention                          │
│     • Secure temp file storage                           │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│  3. Content Validation                                   │
│     • Document structure validation                      │
│     • Excel schema validation                            │
│     • Template integrity checks                          │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│  4. Resource Management                                  │
│     • Automatic file cleanup                             │
│     • Memory limits                                      │
│     • Processing timeouts                                │
└─────────────────────────────────────────────────────────┘
```

---

## Logging Strategy

```
┌─────────────────────────────────────────────────────────┐
│                    Log Levels                            │
│                                                          │
│  DEBUG    → Detailed diagnostic information             │
│             • Template structure details                 │
│             • Table parsing steps                        │
│                                                          │
│  INFO     → General operational events                   │
│             • File uploaded                              │
│             • Parsing completed                          │
│             • N vulnerabilities extracted                │
│                                                          │
│  WARNING  → Recoverable issues                          │
│             • Missing PoC image                          │
│             • Optional field empty                       │
│             • Minor format inconsistency                 │
│                                                          │
│  ERROR    → Serious problems                            │
│             • Parsing failed                             │
│             • Template corrupted                         │
│             • File processing error                      │
│                                                          │
│  CRITICAL → System-level failures                       │
│             • Cannot write to disk                       │
│             • Out of memory                              │
└─────────────────────────────────────────────────────────┘

Log Output:
├── File: logs/app.log
├── Format: timestamp - module - level - message
└── Rotation: Implement in production
```

---

## Configuration Management

```
┌─────────────────────────────────────────────────────────┐
│              Configuration Sources                       │
│                                                          │
│  1. .env file (highest priority)                        │
│     ↓                                                    │
│  2. Environment variables                                │
│     ↓                                                    │
│  3. Default values in Settings class                     │
│                                                          │
│  Managed by: Pydantic Settings                          │
│  Type-safe: Yes                                         │
│  Validated: Yes                                         │
└─────────────────────────────────────────────────────────┘

Key Settings:
├── Application
│   ├── APP_NAME
│   ├── APP_VERSION
│   └── DEBUG
├── Server
│   ├── HOST
│   └── PORT
├── Files
│   ├── MAX_FILE_SIZE_MB
│   ├── UPLOAD_DIR
│   ├── OUTPUT_DIR
│   └── TEMPLATE_DIR
└── Logging
    ├── LOG_LEVEL
    └── LOG_FORMAT
```

---

## Scalability Considerations

### Horizontal Scaling

```
┌──────────────┐
│ Load Balancer│
└──────┬───────┘
       │
       ├─────────┬─────────┬─────────┐
       ▼         ▼         ▼         ▼
   ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
   │App    │ │App    │ │App    │ │App    │
   │Instance│ │Instance│ │Instance│ │Instance│
   └───────┘ └───────┘ └───────┘ └───────┘
```

**Considerations:**
- Stateless design (no shared state)
- Shared file storage (NFS, S3)
- Session management (if auth added)

### Vertical Scaling

**CPU:**
- Increase Gunicorn workers
- Formula: `workers = (2 * CPU_cores) + 1`

**Memory:**
- Monitor per-request memory usage
- Implement file streaming for large files

**Disk:**
- Separate partition for uploads/outputs
- Implement cleanup jobs

---

## Performance Optimization

### Current Optimizations

1. **Minimal Document Loading**
   - Load document once
   - Reuse parsed structure

2. **Efficient XML Cloning**
   - Deep copy at XML level
   - Preserve all attributes

3. **Streaming Where Possible**
   - File uploads streamed
   - File downloads streamed

4. **Early Validation**
   - Fail fast on invalid input
   - Avoid unnecessary processing

### Future Optimizations

1. **Caching**
   - Cache parsed templates
   - Cache validation results

2. **Async Processing**
   - Background job queue (Celery)
   - Async file I/O

3. **Batch Processing**
   - Process multiple files
   - Parallel processing

---

## Testing Strategy

```
┌─────────────────────────────────────────────────────────┐
│                    Test Pyramid                          │
│                                                          │
│                    ╱╲                                    │
│                   ╱  ╲  E2E Tests                       │
│                  ╱────╲  (Manual, Integration)          │
│                 ╱      ╲                                 │
│                ╱────────╲  API Tests                     │
│               ╱          ╲  (pytest, TestClient)        │
│              ╱────────────╲                              │
│             ╱              ╲  Unit Tests                 │
│            ╱────────────────╲  (pytest, mocks)          │
│           ╱__________________╲                           │
│                                                          │
└─────────────────────────────────────────────────────────┘

Coverage Goals:
├── Unit Tests: 80%+
├── Integration Tests: Key workflows
└── E2E Tests: Critical paths
```

---

## Deployment Architecture

### Development

```
Developer Machine
├── Poetry venv
├── Uvicorn (reload mode)
└── SQLite (if DB added)
```

### Production

```
┌──────────────┐
│    Nginx     │  (Reverse Proxy, SSL)
└──────┬───────┘
       │
┌──────▼───────┐
│  Gunicorn    │  (WSGI Server)
│  + Uvicorn   │  (ASGI Workers)
│  Workers     │
└──────┬───────┘
       │
┌──────▼───────┐
│  FastAPI App │
└──────┬───────┘
       │
┌──────▼───────┐
│  File System │
│  (Shared)    │
└──────────────┘
```

---

## Monitoring & Observability

### Metrics to Track

1. **Request Metrics**
   - Request count
   - Response time
   - Error rate

2. **Business Metrics**
   - Files processed
   - Vulnerabilities extracted
   - Success rate

3. **System Metrics**
   - CPU usage
   - Memory usage
   - Disk usage

4. **Application Metrics**
   - Log error count
   - Processing time per file
   - Queue depth (if async)

### Recommended Tools

- **Prometheus**: Metrics collection
- **Grafana**: Dashboards
- **Sentry**: Error tracking
- **ELK Stack**: Log aggregation

---

## Summary

This architecture provides:

✅ **Modularity**: Clear separation of concerns
✅ **Scalability**: Stateless, horizontally scalable
✅ **Maintainability**: Clean code, well-documented
✅ **Reliability**: Comprehensive error handling
✅ **Security**: Multiple validation layers
✅ **Performance**: Optimized processing
✅ **Observability**: Structured logging
✅ **Testability**: Dependency injection, mocking

The system is production-ready and follows industry best practices for enterprise applications.
