"""Full generation test with detailed output checking"""
import sys
sys.path.insert(0, '/app')

from pathlib import Path
from app.services.phase2.excel_reader import ExcelReader
from app.services.phase2.word_generator import WordGenerator
from docx import Document

# Read Excel
excel_path = Path("/app/test.xlsx")
template_path = Path("/app/test_template.docx")
output_path = Path("/app/test_output_fresh.docx")

print("=" * 80)
print("GENERATING FRESH DOCUMENT")
print("=" * 80)

reader = ExcelReader(excel_path)
report = reader.read()

print(f"Read {len(report.vulnerabilities)} vulnerabilities from Excel\n")

# Generate document
generator = WordGenerator(template_path)
result = generator.generate(report, output_path, poc_base_path=None)

print(f"Generated: {result}")
print(f"File size: {result.stat().st_size} bytes\n")

# Now check what's actually in the document
print("=" * 80)
print("CHECKING GENERATED DOCUMENT CONTENT")
print("=" * 80)

doc = Document(output_path)

# Find vulnerability tables (skip summary table)
vuln_tables = []
for idx, table in enumerate(doc.tables):
    # Check if this is a vulnerability table (has specific fields)
    first_row_text = " ".join([cell.text for cell in table.rows[0].cells]) if len(table.rows) > 0 else ""
    if any(keyword in first_row_text.lower() for keyword in ['severity', 'cvss', 'cwe', 'summary']):
        vuln_tables.append((idx, table))

print(f"\nFound {len(vuln_tables)} vulnerability tables (excluding summary)\n")

# Check each table
for table_idx, (doc_table_idx, table) in enumerate(vuln_tables[:3], 1):  # Check first 3
    print(f"\n{'='*80}")
    print(f"VULNERABILITY TABLE #{table_idx} (Document table index: {doc_table_idx})")
    print(f"{'='*80}")
    
    # Extract data from table
    data = {}
    for row in table.rows:
        if len(row.cells) >= 2:
            key = row.cells[0].text.strip()
            value = row.cells[1].text.strip()[:200]  # First 200 chars
            if key and value:
                data[key] = value
    
    # Print key fields
    for field in ['Severity', 'CVSS', 'CWE', 'Summary', 'Affected Assets', 'Impact', 'Recommendations']:
        if any(f in data for f in [field, field.lower(), field.upper()]):
            actual_key = next((k for k in data.keys() if field.lower() in k.lower()), field)
            print(f"{field}:")
            print(f"  {data.get(actual_key, 'NOT FOUND')[:150]}...")
            print()

print("\n" + "=" * 80)
print("DONE")
print("=" * 80)
