# Text Box PoC Image Insertion Feature

## Overview

The Word generator now supports inserting PoC images **inside text boxes** in your Word templates. This provides better control over image placement and formatting within your vulnerability report templates.

## How It Works

### Template Setup

1. In your Word template, create a text box where you want the PoC images to appear
2. Inside the text box, add the placeholder: `{{POC}}`
3. The generator will automatically:
   - Detect the text box with the `{{POC}}` placeholder
   - Insert all PoC images inside the text box
   - Add step text outside the text box (in the table cell)

### Visual Example

**Template Structure:**
```
┌─────────────────────────────────────────────┐
│ Vulnerability Table Cell                    │
│                                             │
│ ┌─────────────────────────────────────┐   │
│ │ Text Box                             │   │
│ │ {{POC}}                              │   │
│ └─────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

**After Processing:**
```
┌─────────────────────────────────────────────┐
│ Vulnerability Table Cell                    │
│                                             │
│ Step 1: Navigate to login page             │
│ Step 2: Enter malicious payload            │
│ Step 3: Submit form                        │
│                                             │
│ ┌─────────────────────────────────────┐   │
│ │ Text Box                             │   │
│ │ [Image: 1.png]                       │   │
│ │                                       │   │
│ │ [Image: 2.png]                       │   │
│ │                                       │   │
│ │ [Image: 3.png]                       │   │
│ └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

## Implementation Details

### Code Flow

1. **Detection Phase**
   ```python
   _insert_poc_in_textbox(cell, vuln)
   ```
   - Searches cell's XML for `w:txbxContent` elements (text boxes)
   - Checks for VML text boxes (`v:textbox//w:txbxContent`)
   - Scans text box content for `{{POC}}` placeholder

2. **Insertion Phase**
   ```python
   _insert_images_in_textbox(txbx_content, vuln)
   ```
   - Clears the `{{POC}}` placeholder
   - Creates new paragraph elements in text box
   - Inserts images using python-docx's `add_picture()` method
   - Adds spacing between images

3. **Fallback Mode**
   - If no text box is found, uses the original method
   - Inserts step text AND images in the table cell directly

### Step Text Handling

When a text box is found:
- **Step text** → Added to table cell (outside text box)
- **Images** → Inserted inside text box

```python
def _insert_step_text_only(cell, vuln):
    # Adds: "Step 1: Navigate...", "Step 2: Enter...", etc.
    # WITHOUT images (images go in text box)
```

## Benefits

### ✅ Better Layout Control
- Images contained in a defined area
- Consistent positioning across pages
- Professional appearance

### ✅ Flexible Formatting
- Text box can have borders, backgrounds, shading
- Easy to style independently from cell content
- Better control over image arrangement

### ✅ Backward Compatible
- Works with existing templates (without text boxes)
- Fallback to original behavior if no text box found
- No breaking changes to current functionality

## Usage

### Phase 2 & Phase 3

No changes needed in your workflow:

1. **Create/Update Template**
   - Add a text box in the PoC cell
   - Type `{{POC}}` inside the text box
   - Style the text box as desired (border, fill, etc.)

2. **Generate Report**
   - Upload Excel data, Word template, PoC images
   - Generator automatically detects text box
   - Images inserted inside text box

### Template Design Tips

1. **Text Box Size**
   - Make the text box wide enough for images (5-6 inches recommended)
   - Leave adequate height or set to "auto-fit"

2. **Text Box Formatting**
   - Add borders for visual separation
   - Use light background fill if desired
   - Ensure proper margins/padding

3. **Image Width**
   - Maximum width: 5.5 inches (auto-calculated)
   - Maintains aspect ratio
   - Scales larger images automatically

## Technical Details

### XML Structure

Text boxes in Word documents use this XML structure:

```xml
<w:p>
  <w:r>
    <w:pict>
      <v:shape>
        <v:textbox>
          <w:txbxContent>
            <w:p>
              <w:r>
                <w:t>{{POC}}</w:t>
              </w:r>
            </w:p>
          </w:txbxContent>
        </v:textbox>
      </v:shape>
    </w:pict>
  </w:r>
</w:p>
```

### Detection XPath

The generator uses XPath to find text boxes:

```python
# Standard text boxes
textboxes = tc.xpath('.//w:txbxContent', namespaces=tc.nsmap)

# VML text boxes
vml_textboxes = tc.xpath('.//v:textbox//w:txbxContent', namespaces=tc.nsmap)
```

### Image Insertion

Images are inserted using python-docx's native method:

```python
# Create paragraph in text box
p_elem = OxmlElement('w:p')
temp_para = Paragraph(p_elem, self.document)

# Add image
run = temp_para.add_run()
run.add_picture(str(image_path), width=Inches(width))

# Append to text box
txbx_content.append(p_elem)
```

## Examples

### Example 1: SQL Injection with Text Box

**Excel Data:**
```
Vuln ID: C1
Steps: Navigate to login; Enter ' OR '1'='1; Submit; Observe
POC_Folder: C1
```

**Template:**
```
┌────────────────────────────────────┐
│ Steps to Reproduce:                │
│ ┌────────────────────────────┐    │
│ │ {{POC}}                     │    │
│ └────────────────────────────┘    │
└────────────────────────────────────┘
```

**Generated Output:**
```
┌────────────────────────────────────┐
│ Steps to Reproduce:                │
│                                    │
│ Step 1: Navigate to login          │
│ Step 2: Enter ' OR '1'='1          │
│ Step 3: Submit                     │
│ Step 4: Observe                    │
│                                    │
│ ┌────────────────────────────┐    │
│ │ [Login Page Screenshot]     │    │
│ │                             │    │
│ │ [SQL Injection Input]       │    │
│ │                             │    │
│ │ [Form Submission]           │    │
│ │                             │    │
│ │ [Bypass Result]             │    │
│ └────────────────────────────┘    │
└────────────────────────────────────┘
```

### Example 2: Without Text Box (Fallback)

**Template (Old Style):**
```
┌────────────────────────────────────┐
│ Steps to Reproduce:                │
│ {{POC}}                            │
└────────────────────────────────────┘
```

**Generated Output:**
```
┌────────────────────────────────────┐
│ Steps to Reproduce:                │
│                                    │
│ Step 1: Navigate to login          │
│ [Login Page Screenshot]            │
│                                    │
│ Step 2: Enter ' OR '1'='1          │
│ [SQL Injection Input]              │
│                                    │
│ Step 3: Submit                     │
│ [Form Submission]                  │
│                                    │
│ Step 4: Observe                    │
│ [Bypass Result]                    │
└────────────────────────────────────┘
```

## Modified Files

- ✅ `app/services/phase2/word_generator.py`
  - Added `_insert_poc_in_textbox()` method
  - Added `_insert_step_text_only()` method
  - Added `_insert_images_in_textbox()` method
  - Modified `_populate_table()` to use text box detection
  - Added `from docx.oxml.ns import qn` import

## Testing

### Manual Test Steps

1. **Create Test Template**
   - Open `WAPT-Rootnik-Technical.docx`
   - Find the PoC cell
   - Insert → Text Box
   - Type `{{POC}}` in text box
   - Save template

2. **Prepare Test Data**
   - Use `All_Risk_Levels_Template.xlsx`
   - Ensure C1 vulnerability has steps
   - Create `POC/C1/1.png`, `POC/C1/2.png`, etc.

3. **Generate Report**
   - Phase 2: Upload Excel + Template + PoC folder path
   - Phase 3: Upload Excel + Template + POC.zip
   - Verify images appear inside text box
   - Verify step text appears outside text box

### Expected Results

- ✅ Text box detected correctly
- ✅ `{{POC}}` placeholder cleared
- ✅ Images inserted inside text box
- ✅ Step text added outside text box
- ✅ Proper spacing between images
- ✅ Images scaled to fit text box (max 5.5")

## Troubleshooting

### Issue: Text box not detected

**Symptom**: Images appear in cell directly, not in text box

**Solution**: 
- Verify text box contains exactly `{{POC}}`
- Check text box is in the correct table cell
- Ensure text box is a proper Word text box (Insert → Text Box)

### Issue: Images too large for text box

**Symptom**: Images overflow text box boundaries

**Solution**:
- Images are auto-scaled to 5.5" max width
- Increase text box width in template
- Check image resolution (high-res images scale better)

### Issue: No images inserted

**Symptom**: Text box remains empty

**Solution**:
- Verify PoC folder path is correct
- Check image files exist and are named correctly (1.png, 2.png, etc.)
- Check console logs for errors
- Verify `poc_base_path` is provided

## Future Enhancements

Potential improvements for future versions:

- [ ] Support for multiple text boxes per cell
- [ ] Configurable max image width per text box
- [ ] Option to include step text inside text box
- [ ] Support for other placeholders in text boxes ({{DESCRIPTION}}, etc.)
- [ ] Auto-resize text box based on content

## Changelog

**Version 2.1** - February 12, 2026
- ✅ Added text box detection for PoC images
- ✅ Implemented `{{POC}}` placeholder in text boxes
- ✅ Separate step text and image insertion
- ✅ Backward compatible with non-text-box templates

---

**Status**: ✅ IMPLEMENTED
**Compatibility**: Phase 2 & Phase 3
**Breaking Changes**: None (backward compatible)
