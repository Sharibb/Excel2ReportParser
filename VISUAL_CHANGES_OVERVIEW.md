# 🔄 Visual Overview: Steps Column Update

## 📊 Before & After Comparison

### Excel Template Structure

#### ❌ OLD (Not Supported)
```
┌─────────────┬───────┬───────┬───────┬───────┬───────┬───────┬─────┐
│ POC_Folder  │ Step1 │ Step2 │ Step3 │ Step4 │  ...  │Step10 │     │
├─────────────┼───────┼───────┼───────┼───────┼───────┼───────┼─────┤
│ C1          │ Nav   │ Enter │Submit │Observe│       │       │     │
└─────────────┴───────┴───────┴───────┴───────┴───────┴───────┴─────┘
      ↑
   10 separate columns for steps - rigid and cluttered
```

#### ✅ NEW (Current)
```
┌─────────────┬──────────────────────────────────────────────┬────────┬────────┐
│ POC_Folder  │ Steps                                        │CWE ID  │Impact  │
├─────────────┼──────────────────────────────────────────────┼────────┼────────┤
│ C1          │ Navigate; Enter payload; Submit; Observe     │CWE-89  │Critical│
└─────────────┴──────────────────────────────────────────────┴────────┴────────┘
      ↑
   Single column with semicolon delimiter - clean and flexible
```

---

## 🔗 Step-to-Image Mapping

### How It Works

```
Excel Data:
┌──────────────────────────────────────────────────────────────┐
│ Steps: Navigate to login; Enter payload; Submit; Observe     │
└──────────────────────────────────────────────────────────────┘
                         ↓ Parse by ';'
          ┌──────────────┼──────────────┬──────────┐
          ↓              ↓              ↓          ↓
    Step 1           Step 2         Step 3     Step 4
    Navigate         Enter          Submit     Observe
      ↓                ↓              ↓          ↓
    1.png            2.png          3.png      4.png
```

### In Generated Document

```
╔═══════════════════════════════════════════════════╗
║  Step 1: Navigate to login                        ║
║  [Image: 1.png]                                   ║
║                                                   ║
║  Step 2: Enter payload                            ║
║  [Image: 2.png]                                   ║
║                                                   ║
║  Step 3: Submit                                   ║
║  [Image: 3.png]                                   ║
║                                                   ║
║  Step 4: Observe                                  ║
║  [Image: 4.png]                                   ║
╚═══════════════════════════════════════════════════╝
```

---

## 📁 PoC Folder Structure

### Required Structure (Unchanged)

```
POC.zip
└── POC/
    ├── C1/                    ← Matches POC_Folder column
    │   ├── 1.png             ← Step 1 image
    │   ├── 2.png             ← Step 2 image
    │   ├── 3.png             ← Step 3 image
    │   └── 4.png             ← Step 4 image
    │
    ├── H1/
    │   ├── 1.png
    │   └── 2.png
    │
    └── M1/
        └── 1.png
```

---

## 🔄 Data Flow

### Phase 2/3 Processing

```
1. Excel Input
   ┌─────────────────────────────────────────────────┐
   │ POC_Folder: C1                                  │
   │ Steps: Nav; Enter; Submit; Observe              │
   └─────────────────────────────────────────────────┘
                      ↓
2. Parser
   ┌─────────────────────────────────────────────────┐
   │ steps = ["Nav", "Enter", "Submit", "Observe"]   │
   │ poc_folder = "C1"                               │
   └─────────────────────────────────────────────────┘
                      ↓
3. WordGenerator
   ┌─────────────────────────────────────────────────┐
   │ for idx, step in enumerate(steps, start=1):     │
   │   - Add text: "Step {idx}: {step}"              │
   │   - Find image: C1/{idx}.png                    │
   │   - Insert image if found                       │
   └─────────────────────────────────────────────────┘
                      ↓
4. Output Document
   ╔═══════════════════════════════════════════════╗
   ║ PoC Steps:                                    ║
   ║                                               ║
   ║ Step 1: Nav                                   ║
   ║ [Inserted: C1/1.png]                          ║
   ║                                               ║
   ║ Step 2: Enter                                 ║
   ║ [Inserted: C1/2.png]                          ║
   ║                                               ║
   ║ Step 3: Submit                                ║
   ║ [Inserted: C1/3.png]                          ║
   ║                                               ║
   ║ Step 4: Observe                               ║
   ║ [Inserted: C1/4.png]                          ║
   ╚═══════════════════════════════════════════════╝
```

---

## 📝 Migration Example

### Converting Old Data to New Format

#### Option 1: Excel Formula

```excel
# In new "Steps" column (assuming old Step1-Step10 are in columns I-R):
=TEXTJOIN("; ", TRUE, I2:R2)
```

#### Option 2: Python Script

```python
import pandas as pd

df = pd.read_excel("old.xlsx")
step_cols = [f"Step{i}" for i in range(1, 11)]

df["Steps"] = df[step_cols].apply(
    lambda row: "; ".join([str(v) for v in row if pd.notna(v) and v != ""]),
    axis=1
)

df = df.drop(columns=step_cols)
df.to_excel("new.xlsx", index=False)
```

---

## ✨ Key Improvements

| Aspect | Old Format | New Format |
|--------|-----------|------------|
| **Columns** | 10 separate (Step1-Step10) | 1 consolidated (Steps) |
| **Step Limit** | Max 10 steps | Unlimited |
| **Readability** | Spread across columns | Single cell, easy to read |
| **Delimiter** | N/A (separate columns) | Semicolon (`;`) |
| **Width** | 10 narrow columns | 1 wide column |
| **Metadata** | Limited space | Room for CWE, Impact, etc. |
| **Editing** | Jump between cells | Edit in one place |

---

## 🎯 Quick Examples

### Example 1: Simple Vulnerability

```
POC_Folder: H1
Steps: Login to admin panel; Navigate to users; Click on user profile
```

**Result:**
- Step 1: Login to admin panel → `H1/1.png`
- Step 2: Navigate to users → `H1/2.png`
- Step 3: Click on user profile → `H1/3.png`

### Example 2: SQL Injection

```
POC_Folder: C1
Steps: Open login page; Enter ' OR '1'='1 in username; Submit form; Observe bypass
```

**Result:**
- Step 1: Open login page → `C1/1.png`
- Step 2: Enter ' OR '1'='1 in username → `C1/2.png`
- Step 3: Submit form → `C1/3.png`
- Step 4: Observe bypass → `C1/4.png`

### Example 3: XSS

```
POC_Folder: H2
Steps: Navigate to search; Inject <script>alert(1)</script>; Submit; Observe popup
```

**Result:**
- Step 1: Navigate to search → `H2/1.png`
- Step 2: Inject `<script>alert(1)</script>` → `H2/2.png`
- Step 3: Submit → `H2/3.png`
- Step 4: Observe popup → `H2/4.png`

---

## 📚 Documentation References

| Document | Purpose |
|----------|---------|
| `STEPS_COLUMN_UPDATE.md` | Full technical documentation |
| `MIGRATION_QUICK_GUIDE.md` | Quick migration reference |
| `CHANGES_SUMMARY.txt` | Brief summary of changes |
| `README.md` | Updated main documentation |

---

## ⚡ Quick Commands

```bash
# Generate new template
python generate_new_template.py

# Start Docker stack
docker-compose up -d

# Access services
# Frontend: http://localhost:5000
# Backend:  http://localhost:8000/docs
```

---

**Version:** 2.0  
**Date:** February 12, 2026  
**Status:** ✅ Complete
