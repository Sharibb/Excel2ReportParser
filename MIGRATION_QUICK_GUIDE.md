# Quick Migration Guide: Steps Column Update

## What Changed?

### Old Format (❌ No longer supported)
```
POC_Folder | Step1      | Step2           | Step3        | Step4
-----------+------------+-----------------+--------------+------------------
C1         | Navigate   | Enter payload   | Submit       | Observe
```

### New Format (✅ Current)
```
POC_Folder | Steps
-----------+----------------------------------------------------------
C1         | Navigate; Enter payload; Submit; Observe
```

## Quick Actions

### 1. Get New Template
```bash
# Download from Phase 1 in the web interface
# OR generate locally:
python generate_new_template.py
```

### 2. Convert Existing Data

#### In Excel
1. Insert new column "Steps" after "POC_Folder"
2. Use formula (adjust column letters as needed):
   ```excel
   =TEXTJOIN("; ", TRUE, I2:R2)
   ```
3. Copy and paste values to remove formula
4. Delete old Step1-Step10 columns

#### Example Python Script
```python
import pandas as pd

# Read old format
df = pd.read_excel("old_template.xlsx")

# Combine steps
step_cols = [f"Step{i}" for i in range(1, 11)]
df["Steps"] = df[step_cols].apply(
    lambda row: "; ".join([str(val) for val in row if pd.notna(val) and val != ""]),
    axis=1
)

# Drop old columns
df = df.drop(columns=step_cols)

# Save new format
df.to_excel("new_template.xlsx", index=False)
```

### 3. Update PoC Images

Ensure your PoC images are named correctly:
```
POC/
├── C1/
│   ├── 1.png  ← Step 1
│   ├── 2.png  ← Step 2
│   ├── 3.png  ← Step 3
│   └── 4.png  ← Step 4
└── H1/
    ├── 1.png  ← Step 1
    └── 2.png  ← Step 2
```

## Testing Checklist

- [ ] Excel file has "Steps" column (not Step1-Step10)
- [ ] Steps are separated by semicolons (`;`)
- [ ] PoC images are named 1.png, 2.png, 3.png, etc.
- [ ] Phase 2 generates document correctly
- [ ] Phase 3 inserts PoC images correctly

## Example Data

### Valid Steps Format
```
Navigate to login page; Enter ' OR '1'='1; Click submit; Observe unauthorized access
```

### Invalid Steps Format
```
Navigate to login page. Enter ' OR '1'='1. Click submit. Observe unauthorized access
(Uses periods instead of semicolons - will be treated as single step)
```

## Common Issues

### Issue: Steps not parsing correctly
**Solution**: Ensure semicolons are used as delimiters, not commas or periods

### Issue: Images not appearing
**Solution**: Check that:
1. PoC_Folder matches the folder name in ZIP
2. Images are named 1.png, 2.png, etc. (not step1.png)
3. ZIP structure is: `POC/C1/1.png` or `C1/1.png`

### Issue: Old template not working
**Solution**: Download and use the new template. Old format is not supported.

## Need Help?

Check the full documentation: `STEPS_COLUMN_UPDATE.md`

---

**Quick Summary**: Use single "Steps" column with semicolon delimiters. Images map to step numbers (1.png → Step 1).
