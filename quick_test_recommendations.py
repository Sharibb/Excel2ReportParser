import sys
sys.path.insert(0, '/app')

from docx import Document
from app.services.phase2.excel_reader import ExcelReader
from app.services.phase2.word_generator import WordGenerator
from pathlib import Path

# Generate fresh
print("Generating document...")
reader = ExcelReader(Path('/app/test.xlsx'))
report = reader.read()
gen = WordGenerator(Path('/app/test_template.docx'))
gen.generate(report, Path('/app/final_test.docx'))

# Check tables
print("\nChecking Recommendations in each vulnerability table:")
print("=" * 80)
doc = Document('/app/final_test.docx')

for idx, table in enumerate(doc.tables[1:], 1):  # Skip summary table
    if len(table.rows) > 8:
        rec_text = table.rows[8].cells[1].text[:100]
        print(f"\nTable {idx} Recommendations:")
        print(f"  {rec_text}...")
        if idx >= 5:  # Check first 5
            break

print("\n" + "=" * 80)
