# RootNik-Style Vulnerability Report Template Guide

## 📄 Overview

The `Vulnerability_Report_Template_RootNik.docx` template has been created to match the exact structure, formatting, and style of your original `WAPT-Rootnik-Technical.docx` report.

## 🎨 Template Structure Analysis

Based on the analysis of your original document, the template includes:

### 1. **Title Section**
- **"Annexure I"** - Bold, 24pt, Blue (RGB: 00B0F0)
- **Web App URL** - Heading 1, 16pt, Blue (RGB: 00B0F0)
  - Placeholder: `{{APP_URL}}`
- Introduction paragraphs - Body Text, 11pt

### 2. **Assessment Findings Section**
- **"Assessment Findings:"** - Heading 1
- **"Summary:"** - Bold, 18pt, Blue (RGB: 00B0F0)
- Summary table with findings overview
  - Finding descriptions
  - Status indicators (HIGH, LOW, etc.)
  - Placeholders: `{{HIGH_FINDINGS_LIST}}`, `{{LOW_FINDINGS_LIST}}`

### 3. **Risk Level Sections**

Each risk level has:
- **Section Heading** - Heading 1, 18pt, Blue (RGB: 00B0F0)
  - "Critical Risk Findings"
  - "High Risk Findings"
  - "Low Risk Findings"
- **Intro Text** - Body Text, 11pt
  - e.g., "RootNik Labs found {{HIGH_COUNT}} high-severity issues..."

### 4. **Vulnerability Details (Per Vulnerability)**

Each vulnerability includes:

#### **A. Vulnerability Title**
- **Format**: Heading 3, Bold, 12pt, Red (RGB: EE0000)
- **Example**: "H1. Broken Access Control on Jira User Mapping"
- **Placeholder**: `{{VULN_ID}}. {{TITLE}}`

#### **B. Vulnerability Details Table**

A 10-row × 2-column table with the following fields:

| Field Label | Placeholder | Description |
|------------|-------------|-------------|
| **Severity:** | `{{RISK_LEVEL}}` | Risk level (HIGH, MEDIUM, LOW) |
| **Remediation Efforts:** | `{{REMEDIATION_EFFORT}}` | Effort required to fix |
| **CVSS:** | `{{CVSS_SCORE}}` | CVSS score and vector |
| **CVE / CWE ID:** | `{{CWE_ID}}` | CVE/CWE identifiers |
| **Summary:** | `{{DESCRIPTION}}` | Vulnerability description |
| **Affected Assets / Parameters:** | `{{AFFECTED_COMPONENTS}}` | Affected URLs/endpoints |
| **Steps to Reproduce:** | `{{POC}}` | Reproduction steps and PoC |
| **Impact:** | `{{IMPACT}}` | Security impact |
| **Recommendations:** | `{{RECOMMENDATION}}` | Fix recommendations |
| **References:** | `{{REFERENCES}}` | External references/links |

## 🎯 Key Features

### **Exact Formatting Match**
- ✅ Blue headings (RGB: 00B0F0) - matches "High Risk Findings" style
- ✅ Red vulnerability titles (RGB: EE0000) - matches "H1." style
- ✅ Proper font sizes (11pt body, 18pt headings, 12pt titles)
- ✅ Heading styles (Heading 1, Heading 3, Body Text)

### **Complete Field Coverage**
The template includes all 10 fields from your original document:
1. Severity
2. Remediation Efforts
3. CVSS
4. CVE / CWE ID
5. Summary
6. Affected Assets / Parameters
7. Steps to Reproduce
8. Impact
9. Recommendations
10. References

### **Structured Organization**
- Clear section separation (Critical/High/Low)
- Summary table for overview
- Individual vulnerability sections
- Page breaks between major sections

## 🔧 How to Use This Template

### **Option 1: Use with Phase 2 API**

1. **Upload to Phase 2 endpoint** (`/api/phase2/generate`):
   ```
   - excel_file: Your vulnerability Excel file
   - template_file: Vulnerability_Report_Template_RootNik.docx
   - poc_folder: Path to your PoC images
   ```

2. **The API will**:
   - Replace all `{{PLACEHOLDERS}}` with actual data
   - Duplicate the vulnerability table for each finding
   - Insert PoC images into "Steps to Reproduce" field
   - Maintain all formatting and colors

### **Option 2: Manual Customization**

1. **Open** `Vulnerability_Report_Template_RootNik.docx` in Microsoft Word
2. **Customize**:
   - Add your company logo
   - Modify colors to match your branding
   - Add additional sections (Methodology, Conclusion, etc.)
   - Adjust page layout, headers, footers
3. **Keep placeholders intact** for API processing

## 📊 Mapping to Excel Schema

The template placeholders map to your Excel columns:

| Excel Column | Template Placeholder |
|--------------|---------------------|
| Vulnerability ID | `{{VULN_ID}}` |
| Title | `{{TITLE}}` |
| Risk Level | `{{RISK_LEVEL}}` |
| CVSS Score | `{{CVSS_SCORE}}` |
| Description | `{{DESCRIPTION}}` |
| Affected Components | `{{AFFECTED_COMPONENTS}}` |
| Recommendation | `{{RECOMMENDATION}}` |
| CWE ID | `{{CWE_ID}}` |
| Impact | `{{IMPACT}}` |
| References | `{{REFERENCES}}` |
| Remediation Effort | `{{REMEDIATION_EFFORT}}` |
| POC_Folder + Steps 1-5 | `{{POC}}` |

## 🖼️ PoC Steps and Images

### **How It Works**

The "Steps to Reproduce" field (`{{POC}}`) will contain:

```
Step 1: We log in to test
[Image: 1.png]

Step 2: we hacked test
[Image: 2.png]

Step 3: We lum some lore IPSUm
[Image: 3.png]

Step 4: IPSUm
[Image: 4.png]

Step 5: IPSUm
[Image: 5.png]
```

### **Image Naming Convention**

For a vulnerability with `POC_Folder` = "H1":
```
poc_images/
└── H1/
    ├── 1.png  ← Step 1 image
    ├── 2.png  ← Step 2 image
    ├── 3.png  ← Step 3 image
    ├── 4.png  ← Step 4 image
    └── 5.png  ← Step 5 image
```

### **Behavior**
- ✅ **Step text always shows** (from Excel Step1-Step5 columns)
- ✅ **Images inserted if found** (from POC_Folder/1.png, 2.png, etc.)
- ✅ **Gracefully skips missing images** (text still appears)

## 🎨 Color Reference

| Element | Color | RGB |
|---------|-------|-----|
| Section Headings | Blue | 00B0F0 |
| Vulnerability Titles | Red | EE0000 |
| Body Text | Black | 000000 |

## 📁 Files

- **`Vulnerability_Report_Template_RootNik.docx`** - The final template (ready to use)
- **`create_rootnik_template.py`** - Python script that generated the template
- **`WAPT-Rootnik-Technical.docx`** - Your original document (used as reference)

## ✅ Template Validation

The template has been created by:

1. **Analyzing** the original WAPT-Rootnik-Technical.docx structure
2. **Extracting** all formatting details:
   - Heading styles and levels
   - Font sizes, colors, and weights
   - Table structure (10 rows × 2 columns)
   - Field labels and order
3. **Recreating** the exact structure with placeholders
4. **Verifying** all formatting matches the original

## 🚀 Next Steps

1. **Test the template** with your Excel file using Phase 2 API
2. **Verify output** matches your expected format
3. **Customize** as needed for your branding
4. **Use** for automated report generation

## 💡 Tips

- The template duplicates the vulnerability table for **each vulnerability**
- Section headings show count: "RootNik Labs found {{HIGH_COUNT}} high-severity issues..."
- Empty or missing fields in Excel will show as empty in the report
- Image insertion is optional - text always appears

## 📞 Support

If the template needs adjustments:
1. Check the Excel data format matches the expected schema
2. Verify placeholder names match exactly (case-sensitive)
3. Ensure PoC folder structure is correct
4. Review the `create_rootnik_template.py` script for customization

---

**Template Created**: February 11, 2026  
**Based On**: WAPT-Rootnik-Technical.docx  
**Format**: Microsoft Word (.docx)  
**Compatibility**: Microsoft Word 2016+, LibreOffice Writer, Google Docs
