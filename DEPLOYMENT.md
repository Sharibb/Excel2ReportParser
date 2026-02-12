# Deployment Guide

## Production Deployment

### Prerequisites

- Python 3.11 or higher
- Poetry (for dependency management)
- Sufficient disk space for uploads and outputs

### Installation Steps

1. **Clone or extract the application**
   ```bash
   cd /path/to/report-excel2doc
   ```

2. **Install Poetry** (if not already installed)
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies**
   ```bash
   poetry install --only main
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env file with your settings
   ```

5. **Create required directories**
   ```bash
   mkdir -p logs uploads output templates static
   ```

6. **Run the application**
   ```bash
   poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

### Production Configuration

#### Environment Variables

Edit `.env` file:

```env
# Production settings
DEBUG=False
HOST=0.0.0.0
PORT=8000

# Security
MAX_FILE_SIZE_MB=100

# Paths (use absolute paths in production)
UPLOAD_DIR=/var/app/uploads
OUTPUT_DIR=/var/app/output
TEMPLATE_DIR=/var/app/templates
LOG_DIR=/var/log/vulnerability-reporter

# Logging
LOG_LEVEL=INFO
```

#### Using Gunicorn (Recommended for Production)

1. **Install Gunicorn**
   ```bash
   poetry add gunicorn
   ```

2. **Run with Gunicorn**
   ```bash
   poetry run gunicorn app.main:app \
     --workers 4 \
     --worker-class uvicorn.workers.UvicornWorker \
     --bind 0.0.0.0:8000 \
     --timeout 300 \
     --access-logfile /var/log/vulnerability-reporter/access.log \
     --error-logfile /var/log/vulnerability-reporter/error.log
   ```

### Systemd Service (Linux)

Create `/etc/systemd/system/vulnerability-reporter.service`:

```ini
[Unit]
Description=Vulnerability Report Automation Service
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/vulnerability-reporter
Environment="PATH=/opt/vulnerability-reporter/.venv/bin"
ExecStart=/opt/vulnerability-reporter/.venv/bin/gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 300
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable vulnerability-reporter
sudo systemctl start vulnerability-reporter
sudo systemctl status vulnerability-reporter
```

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Copy application code
COPY app ./app

# Create required directories
RUN mkdir -p logs uploads output templates static

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t vulnerability-reporter .
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/templates:/app/templates \
  -v $(pwd)/logs:/app/logs \
  --name vulnerability-reporter \
  vulnerability-reporter
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./uploads:/app/uploads
      - ./output:/app/output
      - ./templates:/app/templates
      - ./logs:/app/logs
    environment:
      - DEBUG=False
      - LOG_LEVEL=INFO
      - MAX_FILE_SIZE_MB=100
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

### Nginx Reverse Proxy

Create `/etc/nginx/sites-available/vulnerability-reporter`:

```nginx
server {
    listen 80;
    server_name vulnerability-reporter.example.com;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:8000;
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

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/vulnerability-reporter /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Security Considerations

1. **File Upload Security**
   - Validate file types strictly
   - Limit file sizes
   - Store uploads in separate partition
   - Implement virus scanning if needed

2. **Access Control**
   - Use authentication middleware
   - Implement API keys
   - Use HTTPS in production
   - Configure CORS appropriately

3. **File Cleanup**
   - Implement automatic cleanup of old files
   - Monitor disk usage
   - Set up log rotation

4. **Network Security**
   - Use firewall rules
   - Limit access to trusted networks
   - Use VPN for remote access

## Monitoring

### Health Checks

```bash
# Check service health
curl http://localhost:8000/health

# Check Phase 1 service
curl http://localhost:8000/api/phase1/health

# Check Phase 2 service
curl http://localhost:8000/api/phase2/health
```

### Log Monitoring

```bash
# View application logs
tail -f logs/app.log

# View errors only
grep ERROR logs/app.log

# Monitor in real-time
tail -f logs/app.log | grep -E "ERROR|WARNING"
```

### Performance Monitoring

Consider integrating:
- Prometheus for metrics
- Grafana for dashboards
- Sentry for error tracking
- ELK stack for log aggregation

## Backup

Important directories to backup:
- `/var/app/templates` - Word templates
- `/var/log/vulnerability-reporter` - Logs
- Application configuration

## Troubleshooting

### Common Issues

1. **Permission Errors**
   ```bash
   # Fix directory permissions
   sudo chown -R www-data:www-data /opt/vulnerability-reporter
   sudo chmod -R 755 /opt/vulnerability-reporter
   ```

2. **Port Already in Use**
   ```bash
   # Find process using port
   sudo lsof -i :8000
   # Kill process or change port in .env
   ```

3. **Out of Disk Space**
   ```bash
   # Check disk usage
   df -h
   # Clean old uploads/outputs
   find uploads/ -type f -mtime +7 -delete
   find output/ -type f -mtime +7 -delete
   ```

## Scaling

For high-load scenarios:

1. **Horizontal Scaling**: Run multiple instances behind load balancer
2. **Async Workers**: Increase Gunicorn workers based on CPU cores
3. **Caching**: Implement Redis for session/data caching
4. **Queue System**: Use Celery for background processing
5. **CDN**: Serve static files via CDN

## Support

For issues or questions:
- Check logs in `logs/app.log`
- Review API documentation at `/docs`
- Contact: Security Automation Team
