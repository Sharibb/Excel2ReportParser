"""Diagnostic script to examine template structure"""
from docx import Document
from docx.oxml.ns import qn

doc = Document("/app/test_template.docx")
body = doc.element.body

print("=" * 80)
print("DIAGNOSTIC: Examining paragraphs before tables")
print("=" * 80)

for idx, elem in enumerate(body):
    if elem.tag.endswith('tbl'):  # Table element
        print(f"\n--- TABLE FOUND AT POSITION {idx} ---")
        
        # Look at previous 3 elements
        for offset in range(1, min(4, idx + 1)):
            prev_elem = body[idx - offset]
            if prev_elem.tag.endswith('p'):
                # Get all text
                full_text = ""
                for t_elem in prev_elem.iter(qn('w:t')):
                    if t_elem.text:
                        full_text += t_elem.text
                
                if full_text.strip():
                    print(f"  Paragraph -{offset}: '{full_text[:150]}'")
                    
                    # Check for various patterns
                    patterns = ['{{VULN_ID}}', '{TITLE}}', 'VULN_ID', 'TITLE', '{{', '}}']
                    found_patterns = [p for p in patterns if p in full_text]
                    if found_patterns:
                        print(f"    → Found patterns: {found_patterns}")

print("\n" + "=" * 80)
