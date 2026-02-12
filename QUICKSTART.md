# Quick Start Guide

Get the Vulnerability Report Automation Service running in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- 2GB+ RAM available
- Ports 5000 and 8000 available

## Steps

### 1. Clone/Navigate to Project

```bash
cd ReportExcel2Doc
```

### 2. Create Required Directories

```bash
# Backend directories
mkdir -p uploads output templates logs

# Frontend directories
mkdir -p frontend/uploads frontend/downloads
```

### 3. Start Services

```bash
# Build and start all services
docker-compose up -d

# This will:
# - Build the backend (FastAPI) container
# - Build the frontend (Flask) container
# - Start both services
# - Create a shared network
```

### 4. Wait for Services to Start

```bash
# Watch the logs
docker-compose logs -f

# Wait for these messages:
# backend  | Application startup complete
# frontend | Booting worker with pid: ...

# Or check health
curl http://localhost:5000/health
curl http://localhost:8000/health
```

### 5. Access the Application

Open your browser and go to:

**http://localhost:5000**

You should see the landing page with two options:
- Phase 1: Word → Excel
- Phase 2: Excel → Word

## Usage

### Phase 1: Parse Word Document

1. Click "Start Phase 1" or navigate to http://localhost:5000/phase1
2. Upload a .docx vulnerability report
3. Click "Parse Document"
4. Download the generated Excel file

### Phase 2: Generate Word Report

1. Click "Start Phase 2" or navigate to http://localhost:5000/phase2
2. Upload Excel file with vulnerability data
3. Upload Word template file
4. Optionally provide PoC images folder path
5. Click "Generate Report"
6. Download the generated Word document

## Verify Everything Works

### Check Services

```bash
# Check container status
docker-compose ps

# Should show:
# NAME                     STATUS              PORTS
# vuln-report-backend      Up (healthy)        0.0.0.0:8000->8000/tcp
# vuln-report-frontend     Up (healthy)        0.0.0.0:5000->5000/tcp
```

### Check Health Endpoints

```bash
# Frontend health
curl http://localhost:5000/health

# Backend health
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/docs
```

## Stop Services

```bash
# Stop services (keeps data)
docker-compose stop

# Stop and remove containers (keeps volumes)
docker-compose down

# Stop, remove everything including volumes
docker-compose down -v
```

## Troubleshooting

### Port Already in Use

If ports 5000 or 8000 are already in use:

```bash
# Edit docker-compose.yml and change ports:
services:
  frontend:
    ports:
      - "5001:5000"  # Change host port to 5001
  backend:
    ports:
      - "8001:8000"  # Change host port to 8001
```

### Services Won't Start

```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Frontend Can't Connect to Backend

```bash
# Check backend is running
curl http://localhost:8000/health

# Check network connectivity
docker-compose exec frontend curl http://backend:8000/health

# Should return: {"status": "healthy", ...}
```

## Next Steps

- Read [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for production deployment
- Check [frontend/README.md](frontend/README.md) for frontend details
- Visit http://localhost:8000/docs for API documentation

## File Locations

### Backend
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Logs**: `./logs/app.log`
- **Uploads**: `./uploads/`
- **Output**: `./output/`

### Frontend
- **Web UI**: http://localhost:5000
- **Uploads**: `./frontend/uploads/`
- **Downloads**: `./frontend/downloads/`

## Common Commands

```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Rebuild after code changes
docker-compose up -d --build

# Check resource usage
docker stats

# Execute commands in container
docker-compose exec backend bash
docker-compose exec frontend bash

# View environment variables
docker-compose exec backend env
```

## Need Help?

1. Check the logs: `docker-compose logs`
2. Check service status: `docker-compose ps`
3. Check health: `curl http://localhost:5000/health`
4. Read [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for detailed troubleshooting

---

**That's it! You're ready to automate vulnerability reports!** 🚀
