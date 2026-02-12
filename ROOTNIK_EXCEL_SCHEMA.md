# RootNik Excel Schema Documentation

## 📊 Overview

The `RootNik_Vulnerabilities_Template.xlsx` file is designed to work seamlessly with the `Vulnerability_Report_Template_RootNik.docx` template. It contains all the fields required to generate a complete RootNik-style vulnerability assessment report.

---

## 📋 Excel Schema

### **Column Structure (17 Columns)**

| # | Column Name | Required | Description | Example |
|---|-------------|----------|-------------|---------|
| 1 | **Vulnerability ID** | ✅ Yes | Unique identifier for the vulnerability | `H1`, `H2`, `L1` |
| 2 | **Title** | ✅ Yes | Vulnerability title/name | `Broken Access Control on Jira User Mapping` |
| 3 | **Risk Level** | ✅ Yes | Severity level | `High`, `Medium`, `Low`, `Critical`, `Informational` |
| 4 | **CVSS Score** | ✅ Yes | CVSS score and vector string | `7.1 (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N)` |
| 5 | **CWE ID** | ✅ Yes | CWE identifier(s) | `CWE-284`, `CWE-79, CWE-80` |
| 6 | **Description** | ✅ Yes | Detailed vulnerability description | Full technical description |
| 7 | **Affected Components** | ✅ Yes | URLs, endpoints, or components affected | `https://example.com/vuln` |
| 8 | **Impact** | ✅ Yes | Security impact and consequences | List of potential impacts |
| 9 | **Recommendation** | ✅ Yes | Remediation steps and fixes | Numbered list of recommendations |
| 10 | **References** | ⚠️ Optional | External references and links | URLs separated by newlines |
| 11 | **Remediation Effort** | ✅ Yes | Effort required to fix | `LOW`, `MEDIUM`, `HIGH` |
| 12 | **POC_Folder** | ⚠️ Optional | Folder name for PoC images | `H1`, `H2`, `L1` |
| 13 | **Step1** | ⚠️ Optional | First proof-of-concept step | Step description |
| 14 | **Step2** | ⚠️ Optional | Second proof-of-concept step | Step description |
| 15 | **Step3** | ⚠️ Optional | Third proof-of-concept step | Step description |
| 16 | **Step4** | ⚠️ Optional | Fourth proof-of-concept step | Step description |
| 17 | **Step5** | ⚠️ Optional | Fifth proof-of-concept step | Step description |

---

## 🎯 Field Mapping to Word Template

| Excel Column | Word Template Placeholder | Template Field Name |
|--------------|---------------------------|---------------------|
| Vulnerability ID | `{{VULN_ID}}` | Vulnerability heading |
| Title | `{{TITLE}}` | Vulnerability heading |
| Risk Level | `{{RISK_LEVEL}}` | Severity: |
| CVSS Score | `{{CVSS_SCORE}}` | CVSS: |
| CWE ID | `{{CWE_ID}}` | CVE / CWE ID: |
| Description | `{{DESCRIPTION}}` | Summary: |
| Affected Components | `{{AFFECTED_COMPONENTS}}` | Affected Assets / Parameters: |
| Impact | `{{IMPACT}}` | Impact: |
| Recommendation | `{{RECOMMENDATION}}` | Recommendations: |
| References | `{{REFERENCES}}` | References: |
| Remediation Effort | `{{REMEDIATION_EFFORT}}` | Remediation Efforts: |
| POC_Folder + Steps 1-5 | `{{POC}}` | Steps to Reproduce: |

---

## 📝 Sample Data Included

The template includes 3 sample vulnerabilities:

### **1. H1 - Broken Access Control on Jira User Mapping (High)**
- **CVSS**: 7.1
- **CWE**: CWE-284
- **Description**: Detailed broken access control scenario
- **Impact**: Unauthorized administrative access
- **PoC**: 5 detailed steps with image placeholders

### **2. H2 - CSV Injection on Check-in Report (High)**
- **CVSS**: 7.8
- **CWE**: CWE-1236
- **Description**: CSV injection leading to RCE
- **Impact**: Remote code execution
- **PoC**: 5 detailed steps demonstrating the attack

### **3. L1 - Information Disclosure via Verbose Error Messages (Low)**
- **CVSS**: 3.7
- **CWE**: CWE-209
- **Description**: Verbose error messages revealing sensitive info
- **Impact**: Information leakage aiding reconnaissance
- **PoC**: 3 steps (with empty steps 4 and 5)

---

## 🎨 Formatting Features

### **Header Row (Row 1)**
- **Background**: Blue (`#00B0F0`)
- **Font**: White, Bold, 11pt
- **Alignment**: Center, Wrapped
- **Borders**: Full borders on all cells

### **Risk Level Color Coding**
| Risk Level | Background Color | Font Color | Weight |
|------------|------------------|------------|--------|
| Critical | N/A (not in sample) | Dark Red | Bold |
| High | Light Red (`#FFE6E6`) | Red (`#CC0000`) | Bold |
| Medium | Light Orange (`#FFF4E6`) | Orange (`#FF8C00`) | Bold |
| Low | Light Blue (`#E6F3FF`) | Blue (`#0066CC`) | Bold |
| Informational | Light Gray | Gray | Bold |

### **Cell Formatting**
- **Alignment**: Top-aligned, Wrapped text
- **Borders**: Thin borders on all cells
- **Column Widths**: Optimized for readability
  - ID: 15
  - Title: 40
  - Description: 60
  - Steps: 60

---

## 🖼️ PoC Image Structure

### **POC_Folder Column**
Specifies the folder name where PoC images are stored:
```
H1  → Images in: poc_images/H1/
H2  → Images in: poc_images/H2/
L1  → Images in: poc_images/L1/
```

### **Image Naming Convention**
Images are automatically mapped from Step columns:
```
Step1 → 1.png
Step2 → 2.png
Step3 → 3.png
Step4 → 4.png
Step5 → 5.png
```

### **Expected Folder Structure**
```
poc_images/
├── H1/
│   ├── 1.png  ← Step 1 screenshot
│   ├── 2.png  ← Step 2 screenshot
│   ├── 3.png  ← Step 3 screenshot
│   ├── 4.png  ← Step 4 screenshot
│   └── 5.png  ← Step 5 screenshot
├── H2/
│   ├── 1.png
│   ├── 2.png
│   ├── 3.png
│   ├── 4.png
│   └── 5.png
└── L1/
    ├── 1.png
    ├── 2.png
    └── 3.png
```

When calling Phase 2 API, set `poc_folder` parameter to: `C:/path/to/poc_images`

---

## ✅ Data Validation Rules

### **Risk Level (Column C)**
Valid values:
- `Critical`
- `High`
- `Medium`
- `Low`
- `Informational`

(Case-insensitive, will be normalized)

### **Remediation Effort (Column K)**
Valid values:
- `LOW`
- `MEDIUM`
- `HIGH`

### **CVSS Score (Column D)**
Format: `[score] ([vector])`
Example: `7.1 (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N)`

### **CWE ID (Column E)**
Format: `CWE-[number]` or multiple separated by commas
Examples:
- `CWE-284`
- `CWE-79, CWE-80`
- `CWE-89, CWE-564, CWE-943`

---

## 🚀 Usage Workflow

### **Step 1: Fill in Vulnerability Data**
1. Open `RootNik_Vulnerabilities_Template.xlsx`
2. Replace sample data with your findings
3. Add/remove rows as needed
4. Ensure all required fields are filled

### **Step 2: Prepare PoC Images (Optional)**
1. Create folder structure matching `POC_Folder` values
2. Name images as `1.png`, `2.png`, etc.
3. Place images in respective folders

### **Step 3: Generate Report via API**
1. Go to: `http://localhost:8000/docs`
2. Navigate to `/api/phase2/generate`
3. Upload:
   - **excel_file**: `RootNik_Vulnerabilities_Template.xlsx`
   - **template_file**: `Vulnerability_Report_Template_RootNik.docx`
   - **poc_folder** (optional): `C:/path/to/poc_images`
4. Click **Execute**
5. Download generated report

### **Step 4: Review Generated Report**
- Check all fields populated correctly
- Verify PoC steps and images
- Confirm formatting matches original
- Review table structure

---

## 📐 Column Width Recommendations

| Column | Width | Reason |
|--------|-------|--------|
| A (ID) | 15 | Short identifiers |
| B (Title) | 40 | Long vulnerability names |
| C (Risk) | 12 | Single word values |
| D (CVSS) | 50 | Score + vector string |
| E (CWE) | 15 | Short identifiers |
| F (Description) | 60 | Long paragraphs |
| G (Affected) | 35 | URLs/endpoints |
| H (Impact) | 50 | Bulleted lists |
| I (Recommendation) | 60 | Detailed steps |
| J (References) | 50 | Multiple URLs |
| K (Effort) | 18 | Single word |
| L (POC_Folder) | 15 | Short folder names |
| M-Q (Steps) | 60 | Detailed descriptions |

---

## 💡 Best Practices

### **Writing Descriptions**
- Use complete sentences
- Include technical details
- Explain the root cause
- Describe the attack vector

### **Writing Impact Statements**
- Use bullet points (`•` or `-`)
- List specific consequences
- Prioritize by severity
- Include business impact

### **Writing Recommendations**
- Number the steps (1., 2., 3.)
- Be specific and actionable
- Include code examples if needed
- Reference security standards

### **Writing PoC Steps**
- Be clear and concise
- Include URLs/endpoints
- Specify user roles
- Mention tools used (Burp Suite, etc.)
- Make steps reproducible

### **References**
- Separate multiple URLs with newlines
- Include OWASP links
- Add CWE references
- Link to vendor advisories

---

## 🔧 Customization

### **Adding More Steps**
If you need more than 5 PoC steps:
1. Add columns: `Step6`, `Step7`, etc.
2. Update the API code to handle additional steps
3. Modify the template insertion logic

### **Adding Custom Fields**
To add custom fields:
1. Add column to Excel
2. Add placeholder to Word template (`{{YOUR_FIELD}}`)
3. Update the Pydantic model in `app/models/vulnerability.py`
4. Update the mapping logic in `app/services/phase2/word_generator.py`

### **Changing Risk Levels**
To add custom risk levels:
1. Update the `RiskLevel` enum in `app/models/vulnerability.py`
2. Add color coding in the Excel generator
3. Update the Word template sections

---

## 📊 Excel vs Word Comparison

| Aspect | Excel Template | Word Template |
|--------|----------------|---------------|
| Purpose | Data entry | Report output |
| Structure | Flat table | Hierarchical document |
| Fields | 17 columns | 10 table rows + title |
| Styling | Minimal | Full formatting |
| PoC Steps | Separate columns | Combined with images |
| Risk Levels | Color-coded cells | Section headings |

---

## 🎯 File Information

- **Filename**: `RootNik_Vulnerabilities_Template.xlsx`
- **Size**: ~8KB
- **Rows**: 4 (1 header + 3 sample vulnerabilities)
- **Columns**: 17
- **Format**: Excel 2007+ (.xlsx)
- **Compatibility**: Excel, LibreOffice Calc, Google Sheets

---

## ✅ Quality Checklist

Before generating a report, ensure:

- [ ] All required fields are filled
- [ ] Risk levels use valid values
- [ ] CVSS scores are properly formatted
- [ ] CWE IDs are valid
- [ ] URLs in "Affected Components" are correct
- [ ] PoC steps are clear and reproducible
- [ ] POC_Folder names match your folder structure
- [ ] Images are named correctly (1.png, 2.png, etc.)
- [ ] References are valid URLs
- [ ] No Excel formulas in text fields (security risk)

---

## 🆘 Troubleshooting

### **Issue: Fields not populating in Word**
- ✅ Check Excel column names match exactly
- ✅ Ensure no extra spaces in headers
- ✅ Verify data in required columns

### **Issue: Images not appearing**
- ✅ Check POC_Folder value matches folder name
- ✅ Verify images named as 1.png, 2.png, etc.
- ✅ Ensure poc_folder parameter points to correct directory
- ✅ Check image formats (PNG, JPG supported)

### **Issue: Risk level colors not showing**
- ✅ Use exact values: `High`, `Medium`, `Low`
- ✅ Check for typos or extra spaces
- ✅ Ensure proper capitalization

### **Issue: PoC steps not showing**
- ✅ Verify Step1-Step5 columns have data
- ✅ Check for merged cells in Excel
- ✅ Ensure no hidden characters

---

## 📚 Related Documentation

- **Template Guide**: `ROOTNIK_TEMPLATE_GUIDE.md`
- **API Documentation**: `README.md`
- **Docker Setup**: `DOCKER.md`
- **General Rules**: `.cursor/rules/reportingrules.mdc`

---

**Created**: February 11, 2026  
**Version**: 1.0  
**Compatible With**: `Vulnerability_Report_Template_RootNik.docx`
