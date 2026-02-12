# Docker Deployment Guide

Complete guide for deploying the Vulnerability Report Automation Service with Docker.

## Architecture

```
┌─────────────────────────────────────────────┐
│                                             │
│  User Browser                               │
│                                             │
└───────────────┬─────────────────────────────┘
                │ HTTP :5000
                ▼
┌─────────────────────────────────────────────┐
│                                             │
│  Frontend Service (Flask)                   │
│  - Web UI                                   │
│  - File upload interface                    │
│  - Drag & drop support                      │
│                                             │
└───────────────┬─────────────────────────────┘
                │ HTTP :8000
                ▼
┌─────────────────────────────────────────────┐
│                                             │
│  Backend Service (FastAPI)                  │
│  - Phase 1: Word → Excel parsing            │
│  - Phase 2: Excel → Word generation         │
│  - Document processing logic                │
│                                             │
└─────────────────────────────────────────────┘
```

## Quick Start

### 1. Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 2GB+ available RAM
- 5GB+ available disk space

### 2. Clone and Setup

```bash
# Navigate to project directory
cd ReportExcel2Doc

# Create environment file (optional)
cp .env.example .env
# Edit .env and set SECRET_KEY and other variables

# Create required directories
mkdir -p uploads output templates logs
mkdir -p frontend/uploads frontend/downloads
```

### 3. Build and Run

```bash
# Build and start all services
docker-compose up -d

# Check logs
docker-compose logs -f

# Check status
docker-compose ps
```

### 4. Access Services

- **Frontend**: http://localhost:5000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 5. Stop Services

```bash
# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop, remove containers, and volumes
docker-compose down -v
```

## Services

### Backend (FastAPI)

**Container Name**: `vuln-report-backend`  
**Port**: 8000  
**Image**: Built from root `Dockerfile`

**Endpoints**:
- `GET /` - Service info
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation
- `POST /api/phase1/parse` - Parse Word to Excel
- `POST /api/phase2/generate` - Generate Word from Excel

**Volumes**:
- `./uploads` → `/app/uploads` - Temporary file uploads
- `./output` → `/app/output` - Generated outputs
- `./templates` → `/app/templates` - Template storage
- `./logs` → `/app/logs` - Application logs

### Frontend (Flask)

**Container Name**: `vuln-report-frontend`  
**Port**: 5000  
**Image**: Built from `frontend/Dockerfile`

**Routes**:
- `GET /` - Landing page
- `GET /phase1` - Phase 1 interface
- `GET /phase2` - Phase 2 interface
- `GET /health` - Health check

**Volumes**:
- `./frontend/uploads` → `/app/uploads` - Temporary uploads
- `./frontend/downloads` → `/app/downloads` - Downloads

## Configuration

### Environment Variables

#### Backend Service

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | `Vulnerability Report...` | Application name |
| `APP_VERSION` | `0.1.0` | Version number |
| `DEBUG` | `False` | Debug mode |
| `HOST` | `0.0.0.0` | Bind host |
| `PORT` | `8000` | Bind port |
| `MAX_FILE_SIZE_MB` | `100` | Max upload size |
| `LOG_LEVEL` | `INFO` | Logging level |

#### Frontend Service

| Variable | Default | Description |
|----------|---------|-------------|
| `BACKEND_URL` | `http://backend:8000` | Backend API URL |
| `SECRET_KEY` | `change-me...` | Flask secret key |
| `PORT` | `5000` | Frontend port |
| `DEBUG` | `False` | Debug mode |

### Customization

Edit `docker-compose.yml` to customize:

```yaml
services:
  backend:
    environment:
      - MAX_FILE_SIZE_MB=200  # Increase upload limit
      - LOG_LEVEL=DEBUG       # Enable debug logging
  
  frontend:
    environment:
      - SECRET_KEY=your-secret-key-here  # Change secret
```

## Health Checks

Both services include health checks:

```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend health
curl http://localhost:5000/health

# Docker health status
docker-compose ps
```

Expected response:
```json
{
  "status": "healthy",
  "service": "vulnerability-report-automation"
}
```

## Logs

### View Logs

```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100

# Application logs (backend)
tail -f logs/app.log
```

## Troubleshooting

### Services Won't Start

```bash
# Check if ports are in use
netstat -an | grep -E "5000|8000"

# Check Docker resources
docker stats

# View detailed error logs
docker-compose logs backend
docker-compose logs frontend
```

### Frontend Can't Connect to Backend

1. Check if backend is running:
   ```bash
   docker-compose ps backend
   curl http://localhost:8000/health
   ```

2. Check network connectivity:
   ```bash
   docker-compose exec frontend curl http://backend:8000/health
   ```

3. Verify `BACKEND_URL` in docker-compose.yml

### File Upload Issues

1. Check volume permissions:
   ```bash
   ls -la uploads/ output/ logs/
   ```

2. Check disk space:
   ```bash
   df -h
   ```

3. Check file size limits in docker-compose.yml

### Performance Issues

1. Check resource usage:
   ```bash
   docker stats
   ```

2. Increase resources:
   ```yaml
   services:
     backend:
       deploy:
         resources:
           limits:
             cpus: '2'
             memory: 2G
   ```

## Production Deployment

### Security Checklist

- [ ] Change `SECRET_KEY` in .env
- [ ] Set `DEBUG=False`
- [ ] Use HTTPS with reverse proxy (nginx)
- [ ] Restrict CORS origins in backend
- [ ] Use Docker secrets for sensitive data
- [ ] Enable firewall rules
- [ ] Regular security updates

### Reverse Proxy (nginx)

```nginx
# /etc/nginx/sites-available/vuln-report

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Increase timeouts for long-running operations
        proxy_read_timeout 300s;
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
    }
}
```

### Monitoring

```bash
# Resource usage
docker stats --no-stream

# Container health
docker-compose ps

# Log monitoring
docker-compose logs -f | grep ERROR
```

### Backup

```bash
# Backup volumes
tar -czf backup-$(date +%Y%m%d).tar.gz \
  uploads/ output/ templates/ logs/

# Backup with Docker
docker run --rm \
  -v $(pwd):/backup \
  -v vuln-report_data:/data \
  alpine tar czf /backup/data-backup.tar.gz /data
```

## Scaling

### Horizontal Scaling

```yaml
services:
  backend:
    deploy:
      replicas: 3
    
  frontend:
    deploy:
      replicas: 2
```

### Load Balancing

Use nginx or HAProxy to distribute traffic:

```nginx
upstream backend {
    server localhost:8000;
    server localhost:8001;
    server localhost:8002;
}

upstream frontend {
    server localhost:5000;
    server localhost:5001;
}
```

## Maintenance

### Update Images

```bash
# Pull latest images
docker-compose pull

# Rebuild services
docker-compose build --no-cache

# Restart with new images
docker-compose up -d
```

### Clean Up

```bash
# Remove stopped containers
docker-compose rm

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Full cleanup
docker system prune -a --volumes
```

## Development

### Local Development with Docker

```bash
# Use override file
cp docker-compose.yml docker-compose.override.yml

# Edit override for development
services:
  backend:
    environment:
      - DEBUG=True
    volumes:
      - ./app:/app/app  # Mount source code
    command: uvicorn app.main:app --reload --host 0.0.0.0
  
  frontend:
    environment:
      - DEBUG=True
    volumes:
      - ./frontend:/app  # Mount source code
    command: flask run --host 0.0.0.0 --reload

# Run with override
docker-compose up
```

### Debugging

```bash
# Execute commands in container
docker-compose exec backend bash
docker-compose exec frontend bash

# View environment variables
docker-compose exec backend env
docker-compose exec frontend env

# Check Python packages
docker-compose exec backend pip list
docker-compose exec frontend pip list
```

## Support

For issues and questions:

1. Check logs: `docker-compose logs`
2. Verify health: `curl http://localhost:5000/health`
3. Check resources: `docker stats`
4. Review configuration: `docker-compose config`

## References

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
