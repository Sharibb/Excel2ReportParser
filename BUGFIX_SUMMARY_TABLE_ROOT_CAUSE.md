# Summary Table Placeholder Issue - Root Cause Analysis & Fix

## Problem Description

The summary table in the generated Word document was showing placeholder text instead of actual vulnerability data for certain risk levels:

- ✅ **Working**: High Risk Findings, Low Risk Findings
- ❌ **Broken**: Critical Risk Findings, Medium Risk Findings, Info Findings

Placeholders like `{{CRITICAL_FINDINGS_LIST}}`, `{{MEDIUM_FINDINGS_LIST}}`, and `{{INFO_FINDINGS_LIST}}` were not being replaced.

## Root Cause

### The Core Issue: Split Placeholders in Word XML

Word documents store text in XML `<w:t>` elements. A placeholder like `{{CRITICAL_FINDINGS_LIST}}` is often split across multiple text elements:

```xml
<w:t>{{CRITICAL_</w:t>
<w:t>FINDINGS_</w:t>
<w:t>LIST}}</w:t>
```

### The Code Problem

In `word_generator.py`, the `_populate_summary_table()` method had a mismatch:

1. **Detection** (Line 995-996):
   ```python
   row_text = "".join([cell.text for cell in row.cells])
   if placeholder in row_text:  # ✅ This works - concatenates all text
   ```

2. **Replacement** (Original lines 1036-1038):
   ```python
   for run in paragraph.runs:
       if placeholder in run.text:  # ❌ This fails for split placeholders
           run.text = run.text.replace(placeholder, value)
   ```

### Why Some Worked and Others Didn't

- Placeholders that were stored as a single text element worked fine
- Placeholders split across multiple text elements failed
- Whether a placeholder gets split depends on how Word formatted the document (random from user perspective)

## The Solution

Applied the same split-placeholder handling logic that was already working for the main document body to the summary table population.

### Changes Made

**File**: `app/services/phase2/word_generator.py`

**Location 1**: Lines 1031-1070 (Finding replacement with actual data)
- Added two-pass replacement:
  1. First pass: Try simple replacement in individual runs
  2. Second pass: If not replaced, concatenate all runs, replace in full text, consolidate to first run

**Location 2**: Lines 1075-1105 (No findings case - replace with "None")
- Applied same two-pass logic for consistency

### Code Pattern Used

```python
# Try simple replacement first
for run in paragraph.runs:
    if placeholder in run.text:
        run.text = run.text.replace(placeholder, value)
        replaced = True

# If not replaced, handle split placeholders
if not replaced and paragraph.runs:
    full_text = "".join([run.text or "" for run in paragraph.runs])
    
    if placeholder in full_text:
        # Consolidate all text into first run
        full_text = full_text.replace(placeholder, value)
        paragraph.runs[0].text = full_text
        for run in paragraph.runs[1:]:
            run.text = ""
```

## Technical Details

### Why This Pattern Works

1. **Graceful Degradation**: First tries the simple case (non-split) which is faster
2. **Full Coverage**: Falls back to comprehensive handling for split cases
3. **Clean Consolidation**: Puts all text in first run, empties others (preserves formatting of first run)
4. **Logging**: Added debug logs to track when split placeholders are detected

### Related Code

The fix mirrors the existing `_replace_element_text()` method (lines 642-684) which already handled this correctly for the main document body.

## Testing Recommendations

To verify the fix:

1. Generate a report with vulnerabilities at all risk levels (Critical, High, Medium, Low, Info)
2. Check the summary table - all placeholders should be replaced with actual findings
3. Verify the formatting is preserved (colors, bold text, etc.)
4. Test edge cases:
   - Risk levels with no findings (should show "None")
   - Risk levels with 1 finding
   - Risk levels with many findings

## Prevention

To prevent similar issues in future:

1. **Always handle split placeholders** when doing text replacement in Word documents
2. **Use the two-pass pattern**: simple first, then comprehensive
3. **Test with real Word templates** that may have unexpected XML structures
4. **Add logging** for split placeholder detection to catch issues early

## Files Modified

- `app/services/phase2/word_generator.py`: Fixed `_populate_summary_table()` method

## Impact

- **Scope**: Summary table population only
- **Risk**: Low - only affects text replacement logic, doesn't change document structure
- **Backward Compatibility**: Full - fix is purely additive (adds fallback logic)
