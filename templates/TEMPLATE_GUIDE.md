# Word Template Guide

## Overview

This guide explains how to create Word templates for Phase 2 (Excel → Word generation).

## Template Structure

### Required Placeholders

Your Word template can use the following placeholders:

#### Global Placeholders (used anywhere in the document)

- `{{REPORT_TITLE}}` - Report title
- `{{TOTAL_VULNS}}` - Total vulnerability count
- `{{CRITICAL_COUNT}}` - Critical vulnerability count
- `{{HIGH_COUNT}}` - High vulnerability count
- `{{MEDIUM_COUNT}}` - Medium vulnerability count
- `{{LOW_COUNT}}` - Low vulnerability count
- `{{INFO_COUNT}}` - Informational vulnerability count

#### Vulnerability Table Placeholders

Create a table with these placeholders (the table will be duplicated for each vulnerability):

- `{{VULN_ID}}` - Vulnerability ID (e.g., H1, M2)
- `{{TITLE}}` - Vulnerability title
- `{{DESCRIPTION}}` - Detailed description
- `{{RISK}}` or `{{RISK_LEVEL}}` - Risk severity level
- `{{CVSS}}` or `{{CVSS_SCORE}}` - CVSS score
- `{{AFFECTED}}` or `{{AFFECTED_COMPONENTS}}` - Affected systems
- `{{RECOMMENDATION}}` or `{{REMEDIATION}}` - Fix recommendations
- `{{POC}}` or `{{STEPS}}` - PoC images (if provided)

## Template Example Structure

```
VULNERABILITY REPORT
====================

Summary
-------
Total Vulnerabilities: {{TOTAL_VULNS}}
- Critical: {{CRITICAL_COUNT}}
- High: {{HIGH_COUNT}}
- Medium: {{MEDIUM_COUNT}}
- Low: {{LOW_COUNT}}
- Informational: {{INFO_COUNT}}

Detailed Findings
-----------------

[Create a table with vulnerability placeholders - this will be duplicated for each vulnerability]

+------------------+---------------------------+
| Vulnerability ID | {{VULN_ID}}              |
+------------------+---------------------------+
| Title            | {{TITLE}}                |
+------------------+---------------------------+
| Risk Level       | {{RISK_LEVEL}}           |
+------------------+---------------------------+
| CVSS Score       | {{CVSS_SCORE}}           |
+------------------+---------------------------+
| Description      | {{DESCRIPTION}}          |
+------------------+---------------------------+
| Affected         | {{AFFECTED_COMPONENTS}}  |
+------------------+---------------------------+
| Recommendation   | {{RECOMMENDATION}}       |
+------------------+---------------------------+
| Proof of Concept | {{POC}}                  |
+------------------+---------------------------+
```

## Best Practices

1. **Preserve Formatting**: The template's formatting, styles, and table structure will be preserved exactly as designed.

2. **Use Headings**: Use proper heading styles (Heading 1, Heading 2, etc.) for proper Table of Contents generation.

3. **Table Design**: Design your vulnerability table exactly as you want it to appear. The system will duplicate this table for each vulnerability while preserving all formatting.

4. **PoC Images**: 
   - Mark the cell where images should appear with `{{POC}}` or `{{STEPS}}`
   - Images will be inserted automatically if:
     - Excel has POC_Folder column filled
     - Excel has Step1, Step2, etc. columns with image filenames
     - PoC folder path is provided to the API

5. **Optional Fields**: If a field is optional, provide default text like "N/A" after the placeholder:
   ```
   CVSS Score: {{CVSS_SCORE}}
   ```
   Will become "N/A" if no score is provided.

## Template Validation

The system validates:
- Template is a valid .docx file
- Template is not corrupted
- Template structure can be loaded

The system does NOT require specific placeholders - if you don't include a vulnerability table template, the system will only replace global placeholders.

## Testing Your Template

1. Create your template with placeholders
2. Use Phase 2 API endpoint with sample Excel data
3. Review generated document
4. Adjust template formatting as needed
5. Regenerate until satisfied

## Critical Rules

⚠️ **NEVER** alter these in the template after creation:
- Table structure (rows/columns)
- Cell styles and formatting
- Heading styles
- TOC structure

The system will preserve all of these exactly as designed.
