# Docker Deployment Guide

Complete guide for running the Vulnerability Report Automation Service in Docker.

---

## Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and start the service
docker-compose up -d

# Check if it's running
docker-compose ps

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

**Service will be available at: http://localhost:8000**

### Option 2: Using Docker Commands

```bash
# Build the image
docker build -t vulnerability-reporter .

# Run the container
docker run -d \
  --name vulnerability-reporter \
  -p 8000:8000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/templates:/app/templates \
  -v $(pwd)/logs:/app/logs \
  vulnerability-reporter

# Check if it's running
docker ps

# View logs
docker logs -f vulnerability-reporter

# Stop the container
docker stop vulnerability-reporter

# Remove the container
docker rm vulnerability-reporter
```

---

## Verify Deployment

### Check Health

```bash
# Using curl
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","service":"vulnerability-report-automation"}
```

### Access API Documentation

Open your browser and visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Test the API

```bash
# Phase 1: Parse Word document
curl -X POST "http://localhost:8000/api/phase1/parse" \
  -F "docx_file=@WAPT-Rootnik-Technical.docx" \
  --output vulnerabilities.xlsx

# Phase 2: Generate Word report
curl -X POST "http://localhost:8000/api/phase2/generate" \
  -F "excel_file=@vulnerabilities.xlsx" \
  -F "template_file=@template.docx" \
  --output final_report.docx
```

---

## Configuration

### Environment Variables

Edit `docker-compose.yml` to customize settings:

```yaml
environment:
  - APP_NAME=Your Custom Name
  - DEBUG=False
  - MAX_FILE_SIZE_MB=100
  - LOG_LEVEL=INFO
```

### Volume Mounts

The following directories are mounted for persistent data:

| Container Path | Host Path | Purpose |
|----------------|-----------|---------|
| `/app/uploads` | `./uploads` | Temporary file uploads |
| `/app/output` | `./output` | Generated files |
| `/app/templates` | `./templates` | Word templates |
| `/app/logs` | `./logs` | Application logs |

---

## Docker Commands Reference

### Building

```bash
# Build image
docker build -t vulnerability-reporter .

# Build with no cache
docker build --no-cache -t vulnerability-reporter .

# Build with specific tag
docker build -t vulnerability-reporter:v1.0.0 .
```

### Running

```bash
# Run in foreground
docker run -p 8000:8000 vulnerability-reporter

# Run in background (detached)
docker run -d -p 8000:8000 vulnerability-reporter

# Run with custom name
docker run -d --name my-reporter -p 8000:8000 vulnerability-reporter

# Run with environment variables
docker run -d \
  -p 8000:8000 \
  -e DEBUG=True \
  -e MAX_FILE_SIZE_MB=200 \
  vulnerability-reporter
```

### Managing Containers

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Stop container
docker stop vulnerability-reporter

# Start container
docker start vulnerability-reporter

# Restart container
docker restart vulnerability-reporter

# Remove container
docker rm vulnerability-reporter

# Remove container forcefully
docker rm -f vulnerability-reporter
```

### Logs and Debugging

```bash
# View logs
docker logs vulnerability-reporter

# Follow logs in real-time
docker logs -f vulnerability-reporter

# View last 100 lines
docker logs --tail 100 vulnerability-reporter

# Execute command in running container
docker exec -it vulnerability-reporter bash

# Execute Python command
docker exec vulnerability-reporter python -c "print('Hello')"
```

### Images

```bash
# List images
docker images

# Remove image
docker rmi vulnerability-reporter

# Remove unused images
docker image prune

# View image details
docker inspect vulnerability-reporter
```

---

## Docker Compose Commands

### Basic Operations

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart services
docker-compose restart

# View status
docker-compose ps
```

### Logs

```bash
# View logs
docker-compose logs

# Follow logs
docker-compose logs -f

# View logs for specific service
docker-compose logs app

# Tail last 50 lines
docker-compose logs --tail=50
```

### Building

```bash
# Build images
docker-compose build

# Build without cache
docker-compose build --no-cache

# Build and start
docker-compose up --build
```

### Scaling (if needed)

```bash
# Run multiple instances
docker-compose up --scale app=3
```

---

## Production Deployment

### Using Docker Compose in Production

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  app:
    image: vulnerability-reporter:latest
    container_name: vulnerability-reporter-prod
    ports:
      - "8000:8000"
    volumes:
      - /var/app/uploads:/app/uploads
      - /var/app/output:/app/output
      - /var/app/templates:/app/templates
      - /var/log/vulnerability-reporter:/app/logs
    environment:
      - DEBUG=False
      - LOG_LEVEL=WARNING
      - MAX_FILE_SIZE_MB=100
    restart: always
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

Run with:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Behind Nginx Reverse Proxy

Create nginx configuration:

```nginx
upstream vulnerability_reporter {
    server localhost:8000;
}

server {
    listen 80;
    server_name your-domain.com;
    
    client_max_body_size 100M;
    
    location / {
        proxy_pass http://vulnerability_reporter;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts for large file processing
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
}
```

### Using Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.prod.yml vuln-reporter

# List services
docker service ls

# Scale service
docker service scale vuln-reporter_app=3

# View logs
docker service logs vuln-reporter_app

# Remove stack
docker stack rm vuln-reporter
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check container logs
docker logs vulnerability-reporter

# Check if port is already in use
netstat -an | grep 8000  # Linux/Mac
netstat -an | findstr 8000  # Windows

# Run with different port
docker run -p 8001:8000 vulnerability-reporter
```

### Permission Errors

```bash
# Fix volume permissions
sudo chown -R 1000:1000 uploads output templates logs

# Or run container as root (not recommended)
docker run --user root -p 8000:8000 vulnerability-reporter
```

### Out of Disk Space

```bash
# Clean up unused containers
docker container prune

# Clean up unused images
docker image prune

# Clean up everything
docker system prune -a
```

### High Memory Usage

```bash
# Limit container memory
docker run -m 2g -p 8000:8000 vulnerability-reporter

# In docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 2G
```

### Cannot Access Service

```bash
# Check if container is running
docker ps

# Check container IP
docker inspect vulnerability-reporter | grep IPAddress

# Test from inside container
docker exec vulnerability-reporter curl http://localhost:8000/health

# Check firewall rules
sudo ufw status  # Linux
```

---

## Performance Optimization

### Multi-Stage Build (Optional)

For smaller image size, use multi-stage build:

```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
RUN mkdir -p logs uploads output templates static
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using Gunicorn for Production

Modify Dockerfile CMD:

```dockerfile
CMD ["gunicorn", "app.main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "300"]
```

And install gunicorn:

```bash
poetry add gunicorn
```

---

## Monitoring

### Health Checks

Built-in health check runs every 30 seconds:

```bash
# Check health manually
docker exec vulnerability-reporter curl http://localhost:8000/health

# View health status
docker inspect vulnerability-reporter | grep Health
```

### Resource Usage

```bash
# View resource usage
docker stats vulnerability-reporter

# Continuous monitoring
docker stats
```

### Logging

```bash
# View application logs
docker logs -f vulnerability-reporter

# View logs from mounted volume
tail -f ./logs/app.log
```

---

## Backup and Restore

### Backup Data

```bash
# Backup volumes
tar -czf backup-$(date +%Y%m%d).tar.gz uploads output templates

# Backup container
docker commit vulnerability-reporter vulnerability-reporter-backup
docker save vulnerability-reporter-backup > vulnerability-reporter-backup.tar
```

### Restore Data

```bash
# Restore volumes
tar -xzf backup-20260211.tar.gz

# Restore container
docker load < vulnerability-reporter-backup.tar
```

---

## Security Best Practices

1. **Run as Non-Root User** ✅ (Already implemented)
2. **Use Health Checks** ✅ (Already implemented)
3. **Limit Resources** - Set memory/CPU limits
4. **Use Secrets** - For sensitive data
5. **Regular Updates** - Update base image regularly
6. **Scan for Vulnerabilities**:
   ```bash
   docker scan vulnerability-reporter
   ```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Build Docker image
      run: docker build -t vulnerability-reporter .
    
    - name: Run tests
      run: docker run vulnerability-reporter pytest
    
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker tag vulnerability-reporter myregistry/vulnerability-reporter:latest
        docker push myregistry/vulnerability-reporter:latest
```

---

## Summary

**Running the service in Docker:**

```bash
# Quick start
docker-compose up -d

# Access at
http://localhost:8000/docs

# Stop
docker-compose down
```

**That's it! Your vulnerability report automation service is now running in Docker! 🐳🚀**
