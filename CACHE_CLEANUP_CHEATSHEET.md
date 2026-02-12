# 🗑️ Cache Cleanup Cheatsheet

Quick reference for purging cached files in the Vulnerability Reporter service.

---

## 🚀 Quick Commands

### **Method 1: Web UI (Easiest)** ⭐

```
1. Open: http://localhost:8000/docs
2. Find: "Cleanup" section
3. Try: GET /api/cleanup/cache-info (check status)
4. Execute: POST /api/cleanup/purge-cache (delete all)
```

### **Method 2: Python Script**

```bash
docker exec vulnerability-reporter python purge_cache.py
```

### **Method 3: Direct Command**

```bash
docker exec vulnerability-reporter rm -rf /app/uploads/* /app/output/*
```

---

## 📊 Check Cache Status

### **API:**
```bash
curl http://localhost:8000/api/cleanup/cache-info
```

### **Docker:**
```bash
docker exec vulnerability-reporter du -sh /app/uploads /app/output
```

---

## 🔥 Purge Everything

### **API:**
```bash
curl -X POST http://localhost:8000/api/cleanup/purge-cache
```

### **Script (Interactive):**
```bash
docker exec vulnerability-reporter python purge_cache.py
```

### **Script (Auto-confirm):**
```bash
echo "yes" | docker exec -i vulnerability-reporter python purge_cache.py
```

### **Manual:**
```bash
# Delete uploads only
docker exec vulnerability-reporter rm -rf /app/uploads/*

# Delete outputs only
docker exec vulnerability-reporter rm -rf /app/output/*

# Delete both
docker exec vulnerability-reporter rm -rf /app/uploads/* /app/output/*
```

---

## 🔍 Inspect Files

### **List Uploads:**
```bash
docker exec vulnerability-reporter ls -lh /app/uploads
```

### **List Outputs:**
```bash
docker exec vulnerability-reporter ls -lh /app/output
```

### **Count Files:**
```bash
docker exec vulnerability-reporter sh -c "find /app/uploads /app/output -type f | wc -l"
```

### **Total Size:**
```bash
docker exec vulnerability-reporter du -sh /app/uploads /app/output
```

---

## 🎯 Common Scenarios

### **Before Testing:**
```bash
# Clean slate
curl -X POST http://localhost:8000/api/cleanup/purge-cache
```

### **Low Disk Space:**
```bash
# Check what's using space
docker exec vulnerability-reporter du -sh /app/uploads /app/output

# Purge
curl -X POST http://localhost:8000/api/cleanup/purge-cache
```

### **Weekly Maintenance:**
```bash
# Check status first
curl http://localhost:8000/api/cleanup/cache-info

# Purge if needed
curl -X POST http://localhost:8000/api/cleanup/purge-cache
```

### **Nuclear Option (Reset Everything):**
```bash
docker-compose down -v && docker-compose up -d
```

---

## 📋 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/cleanup/cache-info` | GET | Get cache statistics |
| `/api/cleanup/purge-cache` | POST | Delete all cached files |

---

## 🛡️ Safety Notes

✅ **Safe to delete:**
- Uploaded Word/Excel files
- Generated reports
- PoC image folders
- Temporary files

❌ **Never deleted:**
- Application code
- Templates
- Log files
- Configuration

---

## 🔗 Full Documentation

📖 **Detailed Guide:** [`CACHE_CLEANUP_GUIDE.md`](CACHE_CLEANUP_GUIDE.md)

---

**Last Updated:** February 11, 2026
