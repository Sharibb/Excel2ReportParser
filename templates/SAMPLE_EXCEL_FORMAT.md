# Sample Excel Format

## Required Columns

The Excel file must contain these columns (case-sensitive):

| Column Name          | Required | Description                                    | Example           |
|---------------------|----------|------------------------------------------------|-------------------|
| Vulnerability ID    | Yes      | Unique identifier (format: [C|H|M|L|I]<number>)| H1, M2, L3        |
| Title               | Yes      | Short vulnerability title                      | SQL Injection     |
| Description         | Yes      | Detailed description                           | The application....|
| Risk Level          | Yes      | Severity level                                 | High, Medium, Low |
| CVSS Score          | No       | CVSS score (0.0-10.0)                         | 7.5               |
| Affected Components | Yes      | Systems/components affected                    | Login API         |
| Recommendation      | Yes      | Remediation steps                              | Use parameterized...|
| POC_Folder          | No       | Folder name for PoC images                     | H1_SQL_Injection  |
| Step1               | No       | First PoC image filename                       | 1.png             |
| Step2               | No       | Second PoC image filename                      | 2.png             |
| Step3               | No       | Third PoC image filename                       | 3.png             |
| ...                 | No       | Up to Step10                                   | ...               |

## Sample Data

```csv
Vulnerability ID,Title,Description,Risk Level,CVSS Score,Affected Components,Recommendation,POC_Folder,Step1,Step2,Step3
H1,SQL Injection in Login,"SQL injection vulnerability allows attackers to bypass authentication",High,8.5,Login API,Use parameterized queries,H1_SQLi,login_normal.png,injection_test.png,bypass_success.png
M1,Cross-Site Scripting,"Reflected XSS in search parameter",Medium,6.2,Search Feature,Sanitize all user inputs,M1_XSS,search_page.png,xss_payload.png,
L1,Information Disclosure,"Server version exposed in headers",Low,3.1,Web Server,Remove server version headers,,,
```

## Risk Level Values

Accepted values (case-insensitive):
- `Critical` or `CRITICAL`
- `High` or `HIGH`
- `Medium` or `MEDIUM` or `Med`
- `Low` or `LOW`
- `Informational` or `INFO` or `I`

## Vulnerability ID Format

Format: `[PREFIX][NUMBER]`

Prefixes:
- `C` = Critical
- `H` = High
- `M` = Medium
- `L` = Low
- `I` = Informational

Examples:
- `H1` = First High severity vulnerability
- `M3` = Third Medium severity vulnerability
- `L10` = Tenth Low severity vulnerability

## PoC Image Structure

If including PoC images:

1. **POC_Folder**: Name of folder containing images for this vulnerability
2. **Step1-Step10**: Image filenames in order

Example directory structure:
```
poc_images/
├── H1_SQLi/
│   ├── login_normal.png
│   ├── injection_test.png
│   └── bypass_success.png
├── M1_XSS/
│   ├── search_page.png
│   └── xss_payload.png
└── L1_Info/
    └── headers.png
```

When calling Phase 2 API, provide path to `poc_images/` folder.

## Best Practices

1. **Consistent Naming**: Use consistent vulnerability ID format
2. **Complete Data**: Fill all required fields
3. **Clear Descriptions**: Write clear, actionable descriptions
4. **Numbered Steps**: Use sequential numbering (Step1, Step2, not Step1, Step3)
5. **Image Formats**: Use PNG or JPG for PoC images
6. **One Sheet**: Keep all vulnerabilities in first sheet
7. **Header Row**: First row must be headers exactly as shown

## Validation

The system will validate:
- Required columns present
- Vulnerability ID format correct
- CVSS scores in range 0.0-10.0
- Risk levels match accepted values

The system will warn (but continue) for:
- Missing PoC folder
- Missing PoC images
- Empty optional fields
