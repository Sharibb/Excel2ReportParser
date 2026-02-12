# How to Create a Template for Phase 2

## The Issue

Phase 2 requires a **template file** with **placeholders**, not your original report.

## Option 1: Create Template in Word (Recommended)

1. **Open a new Word document**

2. **Add this content:**

```
VULNERABILITY ASSESSMENT REPORT
================================

Executive Summary
-----------------

Total Vulnerabilities Found: {{TOTAL_VULNS}}

Risk Distribution:
• Critical: {{CRITICAL_COUNT}}
• High: {{HIGH_COUNT}}
• Medium: {{MEDIUM_COUNT}}
• Low: {{LOW_COUNT}}
• Informational: {{INFO_COUNT}}

Detailed Findings
=================

[Create a 2-column table below - this is CRUCIAL]
```

3. **Create a table** (Insert → Table → 2 columns, 8 rows):

| Field | Value |
|-------|-------|
| Vulnerability ID | {{VULN_ID}} |
| Title | {{TITLE}} |
| Risk Level | {{RISK_LEVEL}} |
| CVSS Score | {{CVSS_SCORE}} |
| Description | {{DESCRIPTION}} |
| Affected Components | {{AFFECTED_COMPONENTS}} |
| Recommendation | {{RECOMMENDATION}} |
| Proof of Concept | {{POC}} |

4. **Save as:** `my_template.docx`

5. **Upload this template** to Phase 2 instead of your original report

## Option 2: Quick Template (I'll Create It)

I can create a basic template for you automatically. Would you like me to:
1. Create a simple template with placeholders?
2. Create a template that matches your original document's style?

## Important Placeholders

### Global Placeholders (anywhere in document):
- `{{TOTAL_VULNS}}` - Total vulnerability count
- `{{CRITICAL_COUNT}}`, `{{HIGH_COUNT}}`, `{{MEDIUM_COUNT}}`, `{{LOW_COUNT}}`, `{{INFO_COUNT}}`
- `{{REPORT_TITLE}}`

### Table Placeholders (in vulnerability table):
- `{{VULN_ID}}` - Vulnerability ID (e.g., H1, M2)
- `{{TITLE}}` - Vulnerability title
- `{{DESCRIPTION}}` - Detailed description
- `{{RISK_LEVEL}}` or `{{RISK}}` - Risk severity
- `{{CVSS_SCORE}}` or `{{CVSS}}` - CVSS score
- `{{AFFECTED_COMPONENTS}}` or `{{AFFECTED}}` - Affected systems
- `{{RECOMMENDATION}}` or `{{REMEDIATION}}` - Fix instructions
- `{{POC}}` or `{{STEPS}}` - PoC images (if provided)

## How It Works

1. **Phase 2 finds the table** with placeholders in your template
2. **Duplicates that table** for each vulnerability
3. **Replaces placeholders** with actual data from Excel
4. **Preserves all formatting** from your template

## Testing Your Template

1. Create template with placeholders
2. Upload to Phase 2 with your Excel file
3. Check the generated document
4. Adjust template formatting as needed
5. Regenerate

## Common Mistakes

❌ **Using original report as template** - No placeholders!
❌ **Missing table** - No table to duplicate
❌ **Wrong placeholder names** - Won't be replaced
❌ **No table in template** - Vulnerabilities won't appear

✅ **Correct: Template with placeholders in a table**
✅ **Correct: Use {{PLACEHOLDER}} format**
✅ **Correct: One table that will be duplicated**

---

**Need help? Let me know and I can create a template for you!**
