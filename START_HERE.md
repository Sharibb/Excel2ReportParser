# 🚀 START HERE

Welcome! This guide will get you running in 3 minutes.

---

## Step 1: Install Dependencies (1 minute)

```bash
# Install Poetry (if you don't have it)
# Windows PowerShell:
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Install project dependencies
poetry install
```

---

## Step 2: Start the Service (30 seconds)

```bash
poetry run uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## Step 3: Test It! (1 minute)

### Option A: Using Your Browser (Easiest)

1. Open: **http://localhost:8000/docs**

2. You'll see interactive API documentation

3. **Test Phase 1** (Word → Excel):
   - Expand `/api/phase1/parse`
   - Click "Try it out"
   - Click "Choose File" and select `WAPT-Rootnik-Technical.docx`
   - Click "Execute"
   - Click "Download file" to get your Excel

4. **Test Phase 2** (Excel → Word):
   - First, create a simple template (see below)
   - Expand `/api/phase2/generate`
   - Click "Try it out"
   - Upload the Excel from step 3
   - Upload your template
   - Click "Execute"
   - Download your generated report!

### Option B: Using Command Line

```bash
# Phase 1: Parse your Word document
curl -X POST "http://localhost:8000/api/phase1/parse" ^
  -F "docx_file=@WAPT-Rootnik-Technical.docx" ^
  --output vulnerabilities.xlsx

# Phase 2: Generate Word report (after creating template)
curl -X POST "http://localhost:8000/api/phase2/generate" ^
  -F "excel_file=@vulnerabilities.xlsx" ^
  -F "template_file=@my_template.docx" ^
  --output final_report.docx
```

---

## Quick Template Creation

Create a Word document named `my_template.docx` with this content:

```
VULNERABILITY ASSESSMENT REPORT

Executive Summary
-----------------
Total Vulnerabilities: {{TOTAL_VULNS}}

Risk Distribution:
• Critical: {{CRITICAL_COUNT}}
• High: {{HIGH_COUNT}}
• Medium: {{MEDIUM_COUNT}}
• Low: {{LOW_COUNT}}
• Informational: {{INFO_COUNT}}

Detailed Findings
=================

[Create a 2-column table:]

┌──────────────────────┬────────────────────────────┐
│ Vulnerability ID     │ {{VULN_ID}}               │
├──────────────────────┼────────────────────────────┤
│ Title                │ {{TITLE}}                 │
├──────────────────────┼────────────────────────────┤
│ Risk Level           │ {{RISK_LEVEL}}            │
├──────────────────────┼────────────────────────────┤
│ CVSS Score           │ {{CVSS_SCORE}}            │
├──────────────────────┼────────────────────────────┤
│ Description          │ {{DESCRIPTION}}           │
├──────────────────────┼────────────────────────────┤
│ Affected Components  │ {{AFFECTED_COMPONENTS}}   │
├──────────────────────┼────────────────────────────┤
│ Recommendation       │ {{RECOMMENDATION}}        │
├──────────────────────┼────────────────────────────┤
│ Proof of Concept     │ {{POC}}                   │
└──────────────────────┴────────────────────────────┘
```

**Important:** The table above will be automatically duplicated for each vulnerability!

---

## What Just Happened?

### Phase 1 (Word → Excel)
✅ Parsed your Word document
✅ Extracted all vulnerabilities
✅ Created structured Excel file
✅ Ready for editing or Phase 2

### Phase 2 (Excel → Word)
✅ Read Excel data
✅ Found template table
✅ Duplicated table for each vulnerability
✅ Replaced all placeholders
✅ Generated professional report

---

## Next Steps

### 1. Explore the Excel File
Open `vulnerabilities.xlsx` and check:
- All vulnerabilities extracted correctly?
- Data looks accurate?
- Want to add PoC images? Add POC_Folder and Step1, Step2... columns

### 2. Customize Your Template
- Add your company logo
- Change colors and fonts
- Modify table layout
- Add additional sections

See: `templates/TEMPLATE_GUIDE.md` for details

### 3. Add PoC Images (Optional)

Structure your images like this:
```
poc_images/
├── H1_SQLInjection/
│   ├── 1.png
│   ├── 2.png
│   └── 3.png
├── M1_XSS/
│   ├── 1.png
│   └── 2.png
```

In Excel, add:
- Column `POC_Folder`: `H1_SQLInjection`
- Column `Step1`: `1.png`
- Column `Step2`: `2.png`
- Column `Step3`: `3.png`

Then run Phase 2 with:
```bash
curl -X POST "http://localhost:8000/api/phase2/generate" ^
  -F "excel_file=@vulnerabilities.xlsx" ^
  -F "template_file=@my_template.docx" ^
  -F "poc_folder=poc_images" ^
  --output final_report.docx
```

---

## Troubleshooting

### "Module not found" error
```bash
# Make sure you installed dependencies
poetry install
```

### "Port already in use"
```bash
# Use a different port
poetry run uvicorn app.main:app --reload --port 8001
```

### "File too large"
Edit `.env` (create from `.env.example`):
```
MAX_FILE_SIZE_MB=100
```

### Generated document looks wrong
- Check your template has correct placeholders
- Verify Excel has required columns
- Check logs: `logs/app.log`

---

## 📚 Full Documentation

- **Quick Start**: `QUICKSTART.md` - Detailed getting started
- **API Reference**: `API.md` - All endpoints and examples
- **Template Guide**: `templates/TEMPLATE_GUIDE.md` - Create templates
- **Excel Format**: `templates/SAMPLE_EXCEL_FORMAT.md` - Excel structure
- **Testing**: `TESTING.md` - How to test
- **Deployment**: `DEPLOYMENT.md` - Production deployment
- **Project Summary**: `PROJECT_SUMMARY.md` - What's included

---

## 🎯 Common Workflows

### Workflow 1: Standardize Multiple Reports
```bash
# Convert all reports to Excel
for file in *.docx; do
  curl -X POST "http://localhost:8000/api/phase1/parse" \
    -F "docx_file=@$file" \
    --output "${file%.docx}.xlsx"
done

# Manually combine Excel files if needed
# Then generate standardized report
curl -X POST "http://localhost:8000/api/phase2/generate" \
  -F "excel_file=@combined.xlsx" \
  -F "template_file=@standard_template.docx" \
  --output standardized_report.docx
```

### Workflow 2: Quick Data Extraction
```bash
# Just need the data in Excel format?
curl -X POST "http://localhost:8000/api/phase1/parse" \
  -F "docx_file=@report.docx" \
  --output data.xlsx

# Edit in Excel, share with team, import to other tools
```

### Workflow 3: Rebranding Reports
```bash
# Extract data
curl -X POST "http://localhost:8000/api/phase1/parse" \
  -F "docx_file=@old_report.docx" \
  --output data.xlsx

# Generate with new template
curl -X POST "http://localhost:8000/api/phase2/generate" \
  -F "excel_file=@data.xlsx" \
  -F "template_file=@new_brand_template.docx" \
  --output rebranded_report.docx
```

---

## 🎉 You're Ready!

The system is now running and ready to process your vulnerability reports.

**Need Help?**
- Check the logs: `logs/app.log`
- Visit API docs: http://localhost:8000/docs
- Read the guides in the project root

**Happy Automating! 🚀**
