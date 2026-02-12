# All Risk Levels Excel Template Guide

## 📄 File Created

**`All_Risk_Levels_Template.xlsx`**

This comprehensive Excel template contains sample vulnerabilities for **ALL risk levels** to test the complete functionality of your RootNik template.

---

## 📊 What's Inside

### **8 Sample Vulnerabilities Covering All Risk Levels:**

| ID | Title | Risk Level | CVSS |
|----|-------|------------|------|
| **C1** | SQL Injection in Login Form | Critical | 9.8 |
| **H1** | Broken Access Control on Jira User Mapping | High | 7.1 |
| **H2** | Cross-Site Scripting (XSS) in User Profile | High | 7.4 |
| **M1** | Insufficient Rate Limiting on Password Reset | Medium | 5.3 |
| **M2** | Insecure Direct Object Reference (IDOR) | Medium | 6.5 |
| **L1** | Information Disclosure via Verbose Errors | Low | 3.7 |
| **L2** | Missing Security Headers | Low | 3.1 |
| **I1** | Outdated JavaScript Libraries | Informational | 0.0 |

---

## 🎯 Purpose

This template is designed to test:

1. ✅ **Section-based processing** - Each vulnerability appears in its correct section
2. ✅ **Automatic sorting** - Vulnerabilities are sorted by risk level regardless of Excel order
3. ✅ **All risk levels** - Critical, High, Medium, Low, and Informational sections
4. ✅ **Complete data** - All 17 columns filled with realistic data
5. ✅ **Proper formatting** - Color-coded risk levels, formatted headers

---

## 📋 Expected Output in Generated Report

When you use this Excel file with Phase 2 API, you should see:

### **Critical Risk Findings Section**
```
C1. SQL Injection in Login Form
[Table with C1 data]
```

### **High Risk Findings Section**
```
H1. Broken Access Control on Jira User Mapping
[Table with H1 data]

H2. Cross-Site Scripting (XSS) in User Profile
[Table with H2 data]
```

### **Medium Risk Findings Section**
```
M1. Insufficient Rate Limiting on Password Reset
[Table with M1 data]

M2. Insecure Direct Object Reference (IDOR) in Document Access
[Table with M2 data]
```

### **Low Risk Findings Section**
```
L1. Information Disclosure via Verbose Error Messages
[Table with L1 data]

L2. Missing Security Headers
[Table with L2 data]
```

### **Info Findings Section**
```
I1. Outdated JavaScript Libraries Detected
[Table with I1 data]
```

---

## 🚀 How to Use

### **Step 1: Prepare Your Template**

Your Word template should have sections for all risk levels:

```
Document Structure:
├── Critical Risk Findings
│   ├── Paragraph: "RootNik Labs found {{CRITICAL_COUNT}}..."
│   ├── Heading: {{VULN_ID}}. {{TITLE}}
│   └── Table with placeholders
├── High Risk Findings
│   ├── Paragraph: "RootNik Labs found {{HIGH_COUNT}}..."
│   ├── Heading: {{VULN_ID}}. {{TITLE}}
│   └── Table with placeholders
├── Medium Risk Findings
│   ├── Paragraph: "RootNik Labs found {{MEDIUM_COUNT}}..."
│   ├── Heading: {{VULN_ID}}. {{TITLE}}
│   └── Table with placeholders
├── Low Risk Findings
│   ├── Paragraph: "RootNik Labs found {{LOW_COUNT}}..."
│   ├── Heading: {{VULN_ID}}. {{TITLE}}
│   └── Table with placeholders
└── Info Findings
    ├── Paragraph: "RootNik Labs found {{INFO_COUNT}}..."
    ├── Heading: {{VULN_ID}}. {{TITLE}}
    └── Table with placeholders
```

### **Step 2: Run Phase 2 API**

1. Go to: http://localhost:8000/docs
2. Find endpoint: `/api/phase2/generate`
3. Upload files:
   - **excel_file**: `All_Risk_Levels_Template.xlsx`
   - **template_file**: `Vulnerability_Report_Template_RootNik.docx`
   - **poc_folder** (optional): Path to PoC images
4. Click **Execute**
5. Download the generated report

### **Step 3: Verify Output**

Open the generated document and verify:

✅ **Critical section** has ONLY C1  
✅ **High section** has ONLY H1 and H2  
✅ **Medium section** has ONLY M1 and M2  
✅ **Low section** has ONLY L1 and L2  
✅ **Info section** has ONLY I1  

✅ **All headings replaced**: "C1. SQL Injection..." (NOT `{{VULN_ID}}`)  
✅ **All counts correct**: "found 1 critical-severity", "found 2 high-severity"  
✅ **All table fields populated**: No placeholders remaining  

---

## 🧪 Test Scenarios

### **Test 1: Verify Section Separation**
- ✅ C1 appears ONLY in Critical section
- ✅ H1, H2 appear ONLY in High section
- ✅ M1, M2 appear ONLY in Medium section
- ✅ L1, L2 appear ONLY in Low section
- ✅ I1 appears ONLY in Info section

### **Test 2: Verify Sorting**
Even though Excel has them in order (C1, H1, H2, M1, M2, L1, L2, I1), you can rearrange them randomly:
```
Row 2: L1
Row 3: H2
Row 4: M1
Row 5: C1
Row 6: I1
Row 7: M2
Row 8: L2
Row 9: H1
```

The output should STILL have them organized correctly in sections!

### **Test 3: Verify Missing Sections**
Delete C1 from Excel and regenerate. The Critical section template should be removed from the output.

### **Test 4: Verify All Fields**
Check that each vulnerability table has all 10 fields populated:
1. Severity
2. Remediation Efforts
3. CVSS
4. CVE / CWE ID
5. Summary (Description)
6. Affected Assets / Parameters
7. Steps to Reproduce (PoC steps)
8. Impact
9. Recommendations
10. References (as blue hyperlinks)

---

## 📝 Vulnerability Details

### **C1: SQL Injection (Critical)**
- **Type**: Injection flaw
- **CVSS**: 9.8 (Critical)
- **Steps**: 5 detailed PoC steps
- **Comprehensive**: Full description, impact, and remediation

### **H1: Broken Access Control (High)**
- **Type**: Authorization flaw
- **CVSS**: 7.1
- **Steps**: 5 detailed PoC steps
- **Real scenario**: Based on actual Jira mapping vulnerability

### **H2: Cross-Site Scripting (High)**
- **Type**: XSS vulnerability
- **CVSS**: 7.4
- **Steps**: 5 detailed PoC steps
- **Stored XSS**: In user profile field

### **M1: Rate Limiting (Medium)**
- **Type**: Availability/DoS
- **CVSS**: 5.3
- **Steps**: 4 PoC steps
- **Common issue**: Password reset flooding

### **M2: IDOR (Medium)**
- **Type**: Access control
- **CVSS**: 6.5
- **Steps**: 4 PoC steps
- **Privacy risk**: Unauthorized document access

### **L1: Verbose Errors (Low)**
- **Type**: Information disclosure
- **CVSS**: 3.7
- **Steps**: 3 PoC steps
- **Common finding**: Debug mode in production

### **L2: Security Headers (Low)**
- **Type**: Missing security controls
- **CVSS**: 3.1
- **Steps**: 3 PoC steps
- **Best practice**: CSP, X-Frame-Options, etc.

### **I1: Outdated Libraries (Informational)**
- **Type**: Dependency management
- **CVSS**: 0.0
- **Steps**: 4 PoC steps
- **Technical debt**: jQuery 2.x, Bootstrap 3.x

---

## 🎨 Visual Features

### **Color Coding**

| Risk Level | Background | Text Color |
|------------|------------|------------|
| Critical | Dark Red (#8B0000) | White |
| High | Light Red (#FFE6E6) | Red (#CC0000) |
| Medium | Light Orange (#FFF4E6) | Orange (#FF8C00) |
| Low | Light Blue (#E6F3FF) | Blue (#0066CC) |
| Informational | Light Gray (#F0F0F0) | Gray (#666666) |

### **Formatting**

- ✅ **Header row**: Blue background, white text, bold
- ✅ **Frozen panes**: Header row stays visible when scrolling
- ✅ **Wrapped text**: All cells wrap for readability
- ✅ **Borders**: All cells have borders
- ✅ **Column widths**: Optimized for content

---

## 💡 Customization

### **To Add Your Own Vulnerabilities:**

1. Open the Excel file
2. Keep the header row (Row 1)
3. Add new rows with your vulnerability data
4. Use these risk levels: `Critical`, `High`, `Medium`, `Low`, or `Informational`
5. Fill in all 17 columns
6. Save and use with Phase 2 API

### **To Remove Vulnerabilities:**

Simply delete the rows you don't want. The system will automatically:
- Remove empty sections from the template
- Update counts
- Reorganize the document

---

## 📁 Files

| File | Purpose |
|------|---------|
| **`All_Risk_Levels_Template.xlsx`** | ✅ **Use this for testing!** |
| `generate_comprehensive_excel.py` | Python script that created it |
| `ALL_RISK_LEVELS_GUIDE.md` | This guide |

---

## ✅ Quick Test Checklist

Before final use, test with this Excel file and verify:

- [ ] Critical section shows C1 only
- [ ] High section shows H1, H2 only
- [ ] Medium section shows M1, M2 only
- [ ] Low section shows L1, L2 only
- [ ] Info section shows I1 only
- [ ] All headings show ID and Title (e.g., "C1. SQL Injection...")
- [ ] All paragraph counts correct (e.g., "found 1 critical", "found 2 high")
- [ ] All table fields populated
- [ ] References are blue hyperlinks
- [ ] Font is Tahoma throughout
- [ ] No {{PLACEHOLDERS}} remaining

---

## 🎯 Summary

This comprehensive template contains:
- ✅ **1 Critical** vulnerability
- ✅ **2 High** vulnerabilities
- ✅ **2 Medium** vulnerabilities
- ✅ **2 Low** vulnerabilities
- ✅ **1 Informational** finding

**Total: 8 realistic, well-documented vulnerabilities to test your complete RootNik template workflow!**

---

**Ready to test?** Upload `All_Risk_Levels_Template.xlsx` to the Phase 2 API now! 🚀

**API URL:** http://localhost:8000/docs  
**Endpoint:** `/api/phase2/generate`

---

**Created:** February 11, 2026  
**File Size:** ~11 KB  
**Format:** Excel 2007+ (.xlsx)
