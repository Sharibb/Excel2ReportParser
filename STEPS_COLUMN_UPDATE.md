# Steps Column Update - Semicolon-Delimited Format

## Overview

This update consolidates the PoC steps from 10 separate columns (Step1, Step2, ..., Step10) into a single "Steps" column using semicolon (`;`) as a delimiter. This simplifies the Excel template structure and improves data management.

## Changes Made

### 1. Excel Template Structure

**Before:**
```
| ... | POC_Folder | Step1 | Step2 | Step3 | Step4 | Step5 | Step6 | Step7 | Step8 | Step9 | Step10 |
```

**After:**
```
| ... | POC_Folder | Steps | CWE ID | Impact | References | Remediation Effort |
```

### 2. Steps Format

Steps are now stored in a single cell, separated by semicolons:

**Example:**
```
Navigate to login page; Enter ' OR '1'='1 in username field; Submit the form; Observe successful bypass
```

Each step description is separated by a semicolon (`;`), and the system will automatically parse them as individual steps.

### 3. PoC Image Mapping

The image mapping logic remains the same:
- **Step 1** → `1.png`
- **Step 2** → `2.png`
- **Step 3** → `3.png`
- And so on...

The system automatically extracts step numbers from the delimited string and maps them to corresponding image files in the PoC folder.

### 4. Modified Files

#### Backend Changes

1. **`app/models/vulnerability.py`**
   - Changed `VulnerabilityExcelRow` model
   - Removed: `step1`, `step2`, ..., `step10` fields
   - Added: Single `steps` field (Optional[str])
   - Updated `to_vulnerability()` method to parse semicolon-delimited string

2. **`app/services/phase1/excel_generator.py`**
   - Updated `HEADERS` list to include single "Steps" column
   - Added columns: "CWE ID", "Impact", "References", "Remediation Effort"
   - Modified `_add_vulnerabilities()` to join steps with `"; "` delimiter
   - Updated `_apply_formatting()` for new column widths

3. **`app/services/phase2/excel_reader.py`**
   - No changes needed (automatically handles new format through updated model)

4. **`app/services/phase2/word_generator.py`**
   - No changes needed (already uses step index for image mapping)

#### Frontend Changes

No frontend changes required - the frontend templates and routes remain unchanged.

#### Template Files

1. **`All_Risk_Levels_Template.xlsx`** (root directory)
   - Regenerated with new column structure
   - Contains example vulnerabilities with semicolon-delimited steps

2. **`frontend/All_Risk_Levels_Template.xlsx`**
   - Updated to match root template

### 5. Usage Examples

#### Creating Excel Data

```excel
Vulnerability ID: C1
Title: SQL Injection
Steps: Navigate to login; Enter malicious payload; Submit form; Observe bypass
POC_Folder: C1
```

With this format, the system will:
1. Parse 4 steps from the semicolon-delimited string
2. Look for `C1/1.png`, `C1/2.png`, `C1/3.png`, `C1/4.png` in the PoC folder
3. Insert each step text followed by its corresponding image (if found)

#### Example Step Text in Generated Document

```
Step 1: Navigate to login
[Image: 1.png]

Step 2: Enter malicious payload
[Image: 2.png]

Step 3: Submit form
[Image: 3.png]

Step 4: Observe bypass
[Image: 4.png]
```

### 6. Migration Guide

If you have existing Excel files with the old format (Step1-Step10 columns), you can convert them:

#### Option 1: Manual Conversion
1. Create a new "Steps" column
2. For each row, concatenate Step1, Step2, ... Step10 with `"; "` between non-empty values
3. Delete the old Step1-Step10 columns

#### Option 2: Excel Formula
In the new "Steps" column, use a formula like:
```excel
=TEXTJOIN("; ", TRUE, I2:R2)
```
(Assuming Step1-Step10 are in columns I-R)

### 7. Benefits

1. **Simplified Structure**: Single column instead of 10 separate columns
2. **Flexible Step Count**: Not limited to exactly 10 steps
3. **Better Data Management**: Easier to read and edit in Excel
4. **Consistent Format**: Steps are clearly delimited
5. **Additional Metadata**: Room for CWE ID, Impact, References, and Remediation Effort

### 8. Validation

The system automatically validates:
- ✓ Semicolon delimiter parsing
- ✓ Trimming whitespace around each step
- ✓ Handling empty steps
- ✓ Maintaining step order for image mapping

### 9. Backward Compatibility

**Important**: This is a breaking change. Old Excel templates with Step1-Step10 columns will NOT work with the updated system. You must use the new template format.

## Testing

To test the new format:

1. **Generate New Template**:
   ```bash
   python generate_new_template.py
   ```

2. **Use Template in Phase 2**:
   - Upload the new Excel template with semicolon-delimited steps
   - Upload a Word template
   - Verify steps are correctly parsed and inserted

3. **Use Template in Phase 3**:
   - Upload the new Excel template
   - Upload a Word template
   - Upload a ZIP with PoC folders (C1/1.png, C1/2.png, etc.)
   - Verify images are correctly mapped to steps

## Files Generated

- `All_Risk_Levels_Template.xlsx` (root)
- `frontend/All_Risk_Levels_Template.xlsx`
- `generate_new_template.py` (script to regenerate template)

## Quick Reference

### Delimiter
- **Character**: Semicolon (`;`)
- **With spacing**: `"; "` (semicolon + space for readability)

### Example Row
```csv
C1, SQL Injection, ..., C1, Navigate to login; Enter payload; Submit; Observe result, CWE-89, ...
```

### Parsing Logic
```python
steps = [step.strip() for step in steps_string.split(";") if step.strip()]
```

### Image Mapping
```python
for idx, step_text in enumerate(steps, start=1):
    image_filename = f"{idx}.png"  # 1.png, 2.png, 3.png, ...
```

## Support

If you encounter any issues with the new format:
1. Verify your Excel file has a "Steps" column (not Step1, Step2, etc.)
2. Check that steps are separated by semicolons
3. Ensure PoC images are named with numbers (1.png, 2.png, etc.)
4. Check the logs for parsing errors

---

**Last Updated**: February 12, 2026
**Version**: 2.0
