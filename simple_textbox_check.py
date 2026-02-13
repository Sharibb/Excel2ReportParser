"""Simple check for {{POC}} placeholder and text boxes."""

from docx import Document
from lxml import etree

doc = Document('WAPT-Rootnik-Technical.docx')

print("="*80)
print("SEARCHING FOR {{POC}} PLACEHOLDER")
print("="*80)

found_count = 0

# Check all tables
for table_idx, table in enumerate(doc.tables):
    for row_idx, row in enumerate(table.rows):
        for cell_idx, cell in enumerate(row.cells):
            if '{{POC}}' in cell.text or 'POC' in cell.text:
                found_count += 1
                print(f"\n[FOUND #{found_count}] Table {table_idx+1}, Row {row_idx+1}, Cell {cell_idx+1}")
                print(f"  Cell text preview: {cell.text[:150]}")
                
                # Check XML for text box
                cell_xml = etree.tostring(cell._element, encoding='unicode')
                
                if 'txbxContent' in cell_xml:
                    print(f"  [TEXT BOX DETECTED] Cell contains text box structure")
                else:
                    print(f"  [NO TEXT BOX] {{{{POC}}}} is directly in cell")
                
                if 'v:shape' in cell_xml or 'v:textbox' in cell_xml:
                    print(f"  [VML SHAPE DETECTED] Cell contains VML shape/text box")

print(f"\n{'='*80}")
print(f"Total occurrences of '{{{{POC}}}}' or 'POC': {found_count}")
print("="*80)
