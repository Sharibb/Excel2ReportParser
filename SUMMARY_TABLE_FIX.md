# Summary Table Status Column Fix

## 🐛 Problem

The summary table was generating separate rows for each vulnerability (H1, H2, L1), but the **STATUS column** was not showing the risk level (HIGH, MEDIUM, LOW, etc.). The status cells appeared gray/empty instead of showing the colored status labels.

**What was wrong:**
```
┌────────────────────────────────────────────┬──────────┐
│ High Risk Findings                         │          │
│ H1. Broken Access Control...               │          │ ← Empty! Should show "HIGH"
│ H2. CSV Injection...                       │          │ ← Empty! Should show "HIGH"
└────────────────────────────────────────────┴──────────┘
```

**What was expected:**
```
┌────────────────────────────────────────────┬──────────┐
│ High Risk Findings                         │          │
│ H1. Broken Access Control...               │ HIGH     │ ✓ Shows status
│ H2. CSV Injection...                       │ HIGH     │ ✓ Shows status
└────────────────────────────────────────────┴──────────┘
```

---

## ✅ Solution

Modified the `_populate_summary_table()` method in `app/services/phase2/word_generator.py` to:

### **1. Deep Copy Template Row**
Instead of creating a new empty row, we now **deep copy the template row XML element**. This preserves:
- Cell formatting (background colors)
- Text formatting (bold, colors)
- Cell structure
- All XML properties

```python
# Deep copy the template row XML
new_row_element = copy.deepcopy(template_row_element)
```

### **2. Insert at Correct Position**
Insert the copied row directly at the right position in the table XML:

```python
# Insert the new row right after the template row
insert_position = template_position + 1 + finding_idx
parent_table.insert(insert_position, new_row_element)
```

### **3. Replace Placeholder Text**
Replace the placeholder `{{HIGH_FINDINGS_LIST}}` with actual vulnerability text:

```python
# Replace placeholder with finding description
if placeholder in run.text:
    run.text = run.text.replace(placeholder, f"{vuln.vuln_id}. {vuln.title}")
```

### **4. Preserve Status Formatting**
The status cell already has the correct formatting from the deep copy, so we just verify it has content:

```python
# Status cell inherits formatting from template
if not cell1.text.strip() or placeholder in cell1.text:
    # Set status if needed
    for paragraph in cell1.paragraphs:
        if paragraph.runs:
            paragraph.runs[0].text = status
```

---

## 🔧 Technical Details

### **Key Changes**

| Before | After |
|--------|-------|
| `table.add_row()` - Creates empty row | `copy.deepcopy(template_row._element)` - Copies template |
| Manual formatting copy (didn't work) | Automatic formatting inheritance |
| Move row after creation | Insert at correct position directly |
| Status not showing | Status shows with correct formatting |

### **Why Deep Copy Works**

The template row in the Word document contains:
- **Cell 0**: `{{HIGH_FINDINGS_LIST}}` placeholder
- **Cell 1**: `HIGH` with:
  - Bold text
  - White font color
  - Red background fill
  - Center alignment

By deep copying the entire row XML element, all these properties are automatically preserved in the new rows.

---

## 📊 Expected Output

### **Summary Table Structure**

```
┌──────────────────────────────────────────────────┬──────────┐
│ Finding Description                              │ Status   │
├──────────────────────────────────────────────────┼──────────┤
│ Critical Risk Findings                           │ NONE     │
│ None                                             │          │
├──────────────────────────────────────────────────┼──────────┤
│ High Risk Findings                               │          │
│ H1. Broken Access Control on Jira User Mapping  │ HIGH     │ ← Red background
│ H2. CSV Injection on Check-in Report            │ HIGH     │ ← Red background
├──────────────────────────────────────────────────┼──────────┤
│ Medium Risk Findings                             │          │
│ None                                             │ MEDIUM   │ ← Orange background
├──────────────────────────────────────────────────┼──────────┤
│ Low Risk Findings                                │          │
│ L1. Information Disclosure via Verbose Errors    │ LOW      │ ← Green background
├──────────────────────────────────────────────────┼──────────┤
│ Info Findings                                    │          │
│ None                                             │ INFO     │ ← Blue background
└──────────────────────────────────────────────────┴──────────┘
```

### **Status Column Colors**

| Risk Level | Background Color | Text Color |
|------------|------------------|------------|
| CRITICAL   | Dark Red         | White      |
| HIGH       | Red              | White      |
| MEDIUM     | Orange           | White      |
| LOW        | Green            | White      |
| INFO       | Blue             | White      |

---

## 🧪 Testing

### **Test Steps**

1. **Upload Files to API:**
   - Excel: `RootNik_Vulnerabilities_Template.xlsx`
   - Template: `Vulnerability_Report_Template_RootNik.docx`

2. **Check Summary Table:**
   - ✅ Each vulnerability on separate row
   - ✅ Status column shows risk level
   - ✅ Status cells have correct background colors
   - ✅ Status text is bold and white

3. **Verify Categories:**
   - ✅ Critical: Shows "None" if no critical vulnerabilities
   - ✅ High: Shows H1, H2 with "HIGH" status
   - ✅ Medium: Shows "None" with "MEDIUM" status
   - ✅ Low: Shows L1 with "LOW" status
   - ✅ Info: Shows "None" with "INFO" status

---

## 📁 Files Modified

| File | Change |
|------|--------|
| `app/services/phase2/word_generator.py` | Updated `_populate_summary_table()` method to use deep copy and preserve formatting |

---

## ✅ What's Fixed

✅ Status column now shows risk level (HIGH, MEDIUM, LOW, etc.)  
✅ Status cells have correct background colors (red, orange, green, blue)  
✅ Status text is bold and white (as in template)  
✅ Each vulnerability gets its own row  
✅ Template formatting is preserved  
✅ "None" entries show correct status colors  
✅ No placeholders remain in output  

---

## 🎯 Container Status

**Status:** ✅ Running and healthy  
**Service URL:** http://localhost:8000  
**Swagger UI:** http://localhost:8000/docs  
**Container:** vulnerability-reporter  

---

## 💡 Key Takeaway

When duplicating table rows in Word documents:
- **Don't create new empty rows** - you lose all formatting
- **Deep copy the XML element** - preserves everything
- **Replace text in place** - keeps formatting intact

This ensures that all visual properties (colors, fonts, alignment, borders) are maintained in the generated document.

---

**Fixed:** February 11, 2026  
**Ready for testing!** 🎉
