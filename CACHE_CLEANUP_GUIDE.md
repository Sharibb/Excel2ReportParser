# 🗑️ Cache Cleanup Guide

## Overview

The vulnerability reporter service includes cache management functionality to help you clean up uploaded files, generated outputs, and other cached data. This guide covers all available methods to purge cached files.

---

## 📁 What Gets Cached?

The service caches files in two directories:

1. **`/app/uploads/`** - Uploaded files (Word documents, Excel files, PoC images)
2. **`/app/output/`** - Generated files (Excel reports, Word documents)

Over time, these directories can accumulate files and consume disk space. Use the cleanup options below to maintain your system.

---

## 🔧 Cleanup Methods

### **Method 1: API Endpoints (Recommended)**

The easiest way to manage cache is through the FastAPI web interface.

#### **Step 1: Check Cache Status**

**Endpoint:** `GET /api/cleanup/cache-info`

**URL:** http://localhost:8000/docs#/Cleanup/get_cache_info_api_cleanup_cache_info_get

**What it does:**
- Shows how many files are cached
- Displays total cache size
- Breaks down by uploads and outputs

**Example Response:**
```json
{
  "uploads": {
    "files": 15,
    "size_bytes": 2457600,
    "size": "2.34 MB"
  },
  "outputs": {
    "files": 8,
    "size_bytes": 1048576,
    "size": "1.00 MB"
  },
  "total": {
    "files": 23,
    "size_bytes": 3506176,
    "size": "3.34 MB"
  }
}
```

#### **Step 2: Purge Cache**

**Endpoint:** `POST /api/cleanup/purge-cache`

**URL:** http://localhost:8000/docs#/Cleanup/purge_cache_api_cleanup_purge_cache_post

**What it does:**
- Deletes ALL files from uploads directory
- Deletes ALL files from output directory
- Keeps the directories themselves
- Returns statistics about deleted files

**Example Response:**
```json
{
  "status": "success",
  "deleted_files": 23,
  "deleted_size": "3.34 MB",
  "deleted_size_bytes": 3506176,
  "errors": null
}
```

**How to Use:**
1. Go to: http://localhost:8000/docs
2. Scroll down to **"Cleanup"** section
3. Click on `POST /api/cleanup/purge-cache`
4. Click **"Try it out"**
5. Click **"Execute"**
6. Review the response to see what was deleted

---

### **Method 2: Python Script (Interactive)**

Use the included Python script for interactive command-line cleanup.

#### **Run Locally:**

```bash
python purge_cache.py
```

#### **Run in Docker:**

```bash
docker exec vulnerability-reporter python purge_cache.py
```

#### **What it does:**
- Displays current cache status
- Shows file counts and sizes
- Asks for confirmation before deleting
- Provides detailed progress output
- Shows summary of deleted files

#### **Example Output:**

```
======================================================================
🗑️  CACHE PURGE UTILITY
======================================================================

📊 Current Cache Status:
----------------------------------------------------------------------
Uploads:    15 files  |     2.34 MB
Outputs:     8 files  |     1.00 MB
──────────────────────────────────────────────────────────────────────
Total:      23 files  |     3.34 MB

⚠️  WARNING: This will permanently delete all cached files!
Continue? (yes/no): yes

🧹 Purging cache...
----------------------------------------------------------------------

📁 Cleaning uploads directory...
  ✓ Deleted file: report.docx
  ✓ Deleted file: vulnerabilities.xlsx
  ✓ Deleted directory: H1 (5 files, 512.00 KB)
  ...

📁 Cleaning output directory...
  ✓ Deleted file: report_generated.docx
  ✓ Deleted file: vulnerabilities.xlsx
  ...

======================================================================
✅ PURGE COMPLETE
======================================================================
Files deleted:  23
Space freed:    3.34 MB
```

---

### **Method 3: Manual Docker Commands**

If you prefer direct control, use Docker commands:

#### **Delete Uploads Directory Contents:**

```bash
docker exec vulnerability-reporter sh -c "rm -rf /app/uploads/*"
```

#### **Delete Outputs Directory Contents:**

```bash
docker exec vulnerability-reporter sh -c "rm -rf /app/output/*"
```

#### **Delete Both:**

```bash
docker exec vulnerability-reporter sh -c "rm -rf /app/uploads/* /app/output/*"
```

#### **Check Directory Sizes:**

```bash
docker exec vulnerability-reporter du -sh /app/uploads /app/output
```

---

### **Method 4: Docker Volume Reset (Nuclear Option)**

If you want to completely reset the container and all data:

```bash
# Stop and remove container
docker-compose down

# Remove volumes (this deletes EVERYTHING)
docker-compose down -v

# Start fresh
docker-compose up -d
```

⚠️ **WARNING:** This deletes all data including logs, uploads, and outputs!

---

## 🎯 When to Purge Cache

### **Recommended Times:**

- ✅ **After completing a project** - Clean up test files
- ✅ **Before running tests** - Start with a clean slate
- ✅ **Low disk space** - Free up storage
- ✅ **Weekly maintenance** - Regular housekeeping
- ✅ **Before backups** - Don't backup temporary files
- ✅ **After bulk operations** - Clear out large batches of files

### **What NOT to Worry About:**

- ❌ **Logs directory** - Not included in cache cleanup (kept for debugging)
- ❌ **Templates** - Template files are never deleted
- ❌ **Application code** - Only data files are removed

---

## 📊 Monitoring Cache

### **Using the API:**

```bash
# Check cache info
curl http://localhost:8000/api/cleanup/cache-info
```

### **Using Docker:**

```bash
# List files in uploads
docker exec vulnerability-reporter ls -lh /app/uploads

# List files in output
docker exec vulnerability-reporter ls -lh /app/output

# Check disk usage
docker exec vulnerability-reporter du -sh /app/uploads /app/output
```

---

## 🚀 Quick Reference

| Task | Command |
|------|---------|
| **Check cache size** | http://localhost:8000/api/cleanup/cache-info |
| **Purge via API** | http://localhost:8000/docs → POST /api/cleanup/purge-cache |
| **Purge via script** | `docker exec vulnerability-reporter python purge_cache.py` |
| **Manual cleanup** | `docker exec vulnerability-reporter rm -rf /app/uploads/* /app/output/*` |
| **Full reset** | `docker-compose down -v && docker-compose up -d` |

---

## 🔐 Safety Features

The cache cleanup system includes several safety features:

1. **No Code Deletion** - Only uploads and outputs are affected
2. **Directory Preservation** - Directories themselves are kept (only contents deleted)
3. **Error Handling** - Failed deletions are logged but don't stop the process
4. **Statistics** - You always see what was deleted
5. **Logs Preserved** - Log files are never deleted by cache cleanup

---

## ⚙️ Automation

### **Automatic Cleanup Script**

Create a cron job or scheduled task to run cleanup regularly:

```bash
#!/bin/bash
# Run every Sunday at 2 AM
0 2 * * 0 docker exec vulnerability-reporter python purge_cache.py <<< "yes"
```

### **PowerShell Scheduled Task (Windows):**

```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute "docker" -Argument "exec vulnerability-reporter python purge_cache.py"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 2am
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "CleanupVulnerabilityCache" -Description "Weekly cache cleanup"
```

---

## 🐛 Troubleshooting

### **Problem: Permission Denied**

**Solution:**
```bash
# Run with elevated privileges
docker exec -u root vulnerability-reporter rm -rf /app/uploads/* /app/output/*
```

### **Problem: Container Not Running**

**Solution:**
```bash
# Check container status
docker-compose ps

# Start if stopped
docker-compose up -d
```

### **Problem: "Directory Not Found"**

**Solution:**
```bash
# Recreate directories
docker exec vulnerability-reporter mkdir -p /app/uploads /app/output
```

### **Problem: Some Files Won't Delete**

**Possible Causes:**
- Files are currently in use (wait and retry)
- Permission issues (check file ownership)
- Filesystem errors (check Docker volume health)

**Solution:**
```bash
# Force delete (use with caution)
docker exec vulnerability-reporter sh -c "rm -rf /app/uploads/* /app/output/*"
```

---

## 📝 API Documentation

### **GET /api/cleanup/cache-info**

**Description:** Get information about cached files

**Response:**
```typescript
{
  uploads: {
    files: number,
    size_bytes: number,
    size: string
  },
  outputs: {
    files: number,
    size_bytes: number,
    size: string
  },
  total: {
    files: number,
    size_bytes: number,
    size: string
  }
}
```

### **POST /api/cleanup/purge-cache**

**Description:** Purge all cached files

**Response:**
```typescript
{
  status: "success",
  deleted_files: number,
  deleted_size: string,
  deleted_size_bytes: number,
  errors: string[] | null
}
```

---

## ✅ Best Practices

1. **Check Before Purge** - Always run `cache-info` first to see what you're deleting
2. **Regular Cleanup** - Schedule weekly or monthly cleanups
3. **Save Important Files** - Download generated reports you want to keep before purging
4. **Monitor Logs** - Check application logs after cleanup to ensure no errors
5. **Test in Development** - Try cleanup in dev environment before production

---

## 📚 Related Documentation

- **API Documentation:** http://localhost:8000/docs
- **Docker Guide:** `DOCKER.md`
- **Main README:** `README.md`
- **Comprehensive Fix:** `FINAL_COMPREHENSIVE_FIX.md`

---

## 🎉 Summary

Three easy ways to purge cache:

1. **🌐 Web UI:** http://localhost:8000/docs → Cleanup section
2. **💻 Python Script:** `docker exec vulnerability-reporter python purge_cache.py`
3. **⌨️ Direct Command:** `docker exec vulnerability-reporter rm -rf /app/uploads/* /app/output/*`

**Use Method 1 (Web UI) for the easiest experience!**

---

**Last Updated:** February 11, 2026  
**Version:** 1.0.0
