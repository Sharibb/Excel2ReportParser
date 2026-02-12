# Phase 3 Quick Start Guide

Get started with Phase 3 in 5 minutes!

## 🎯 What You Need

1. **Excel File** - Vulnerability data (use `All_Risk_Levels_Template.xlsx`)
2. **Word Template** - Report format (use `WAPT-Rootnik-Technical.docx`)
3. **PoC ZIP File** - Screenshots organized in folders

## 📦 Creating the PoC ZIP

### Step 1: Create Folder Structure

```bash
mkdir -p POC/C1 POC/H1 POC/M1 POC/L1
```

### Step 2: Add Screenshots

```bash
# For Critical vulnerability 1 (C1)
cp screenshot1.png POC/C1/1.png
cp screenshot2.png POC/C1/2.png

# For High vulnerability 1 (H1)
cp screenshot3.png POC/H1/1.png
cp screenshot4.png POC/H1/2.png

# And so on...
```

### Step 3: Create ZIP

```bash
zip -r POC.zip POC/
```

**Result**: POC.zip with this structure:
```
POC.zip
└── POC/
    ├── C1/
    │   ├── 1.png
    │   └── 2.png
    ├── H1/
    │   ├── 1.png
    │   └── 2.png
    └── M1/
        └── 1.png
```

## 📝 Preparing Excel File

1. Download template from Phase 1
2. Add your vulnerabilities:
   - Vulnerability ID: C1, H1, M1, L1 (must match folder names!)
   - Title: SQL Injection, XSS, etc.
   - Risk Level: Critical, High, Medium, Low
   - Description, Affected Components, Recommendation
3. Save the file

## 🚀 Using Phase 3

### Option 1: Web Interface

1. **Start Services**:
   ```bash
   docker-compose up -d
   ```

2. **Open Phase 3**:
   ```
   http://localhost:5000/phase3
   ```

3. **Upload Files**:
   - Drag & drop or browse for Excel file
   - Drag & drop or browse for Word template
   - Drag & drop or browse for POC.zip

4. **Generate**:
   - Click "Generate Complete Report with PoCs"
   - Wait for processing (30-60 seconds)

5. **Download**:
   - Click "Download Complete Report"
   - Open in Microsoft Word
   - Verify PoCs are inserted

### Option 2: API Call

```bash
curl -X POST "http://localhost:8000/api/phase3/generate" \
  -F "excel_file=@my_vulns.xlsx" \
  -F "template_file=@template.docx" \
  -F "poc_zip=@POC.zip" \
  --output my_report.docx
```

## ✅ Verification

Check your generated report:

1. **Open in Word** - Should open without errors
2. **Check Summary Table** - All vulnerabilities listed
3. **Check Each Vulnerability Section**:
   - Vulnerability ID and title present
   - Description populated
   - PoC images visible
   - Images match the vulnerability

## 🐛 Troubleshooting

### "Could not find PoC base directory"
**Problem**: ZIP structure incorrect  
**Solution**: Ensure folders named C1, H1, M1 etc. are at ZIP root or under POC/

### "No PoC folder found for vulnerability X"
**Problem**: Folder missing for vulnerability ID  
**Solution**: Add folder X to ZIP, or accept report without that PoC

### Images not appearing
**Problem**: Folder names don't match vulnerability IDs  
**Solution**: Rename folders to match exactly (C1, H1, M1)

### File too large
**Problem**: ZIP > 100MB  
**Solution**: Compress images or split into multiple reports

## 💡 Tips

- **Folder Names**: Must match vulnerability IDs exactly
- **Image Names**: Use 1.png, 2.png, 3.png (sequential numbers)
- **File Format**: PNG or JPG recommended
- **Image Size**: Keep under 5MB per image
- **Case**: C1 and c1 both work (case-insensitive)

## 📚 Next Steps

- Read full documentation: `PHASE3_IMPLEMENTATION.md`
- Compare with Phase 2: See feature comparison on Phase 3 page
- Customize template: Edit Word template for your branding

## 🎉 That's It!

You're now ready to generate complete vulnerability reports with automatic PoC handling using Phase 3!
