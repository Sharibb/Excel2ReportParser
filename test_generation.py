"""Test script to debug word generation"""
import sys
sys.path.insert(0, '/app')

from pathlib import Path
from app.services.phase2.excel_reader import ExcelReader
from app.services.phase2.word_generator import WordGenerator
from app.core.logging import LoggerSetup

# Setup logging
LoggerSetup.setup()

print("=" * 70)
print("TESTING WORD GENERATION")
print("=" * 70)

# Read Excel
excel_path = Path("/app/test.xlsx")
template_path = Path("/app/test_template.docx")
output_path = Path("/app/test_output.docx")

print(f"\n1. Reading Excel from: {excel_path}")
reader = ExcelReader(excel_path)
report = reader.read()

print(f"\n2. Vulnerabilities found: {len(report.vulnerabilities)}")
for vuln in report.vulnerabilities:
    print(f"   - {vuln.vuln_id}: {vuln.title} ({vuln.risk_level})")

print(f"\n3. Counts:")
print(f"   Critical: {report.critical_count}")
print(f"   High: {report.high_count}")
print(f"   Medium: {report.medium_count}")
print(f"   Low: {report.low_count}")
print(f"   Info: {report.info_count}")

print(f"\n4. Generating Word document...")
print(f"   Template: {template_path}")
print(f"   Output: {output_path}")

generator = WordGenerator(template_path)
result = generator.generate(report, output_path, poc_base_path=None)

print(f"\n5. Generation complete!")
print(f"   Output file: {result}")
print(f"   File exists: {result.exists()}")
print(f"   File size: {result.stat().st_size} bytes")

print("\n" + "=" * 70)
print("CHECK THE LOGS ABOVE FOR PLACEHOLDER REPLACEMENT DETAILS")
print("=" * 70)
