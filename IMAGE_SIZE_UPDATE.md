# Image Size Update - Fixed Dimensions

## Changes Made

Updated image insertion to use **fixed dimensions** to match your text box size and prevent table overflow.

### Image Dimensions

**Fixed Size:**
- **Width**: 11.56 cm (4.55 inches)
- **Height**: 6.92 cm (2.72 inches)

This matches the text box dimensions you specified in the layout settings.

### Modified Methods

#### 1. `_insert_images_in_textbox()` (Line 972-991)
**Purpose**: Inserts images INSIDE text boxes

**Changes:**
```python
# OLD: Auto-calculated width, no height constraint
width = self._calculate_image_width(image_path, max_width=5.5)
run.add_picture(str(image_path), width=Inches(width))

# NEW: Fixed dimensions
target_width_cm = 11.56
target_height_cm = 6.92
width_inches = target_width_cm * 0.393701  # ~4.55 inches
height_inches = target_height_cm * 0.393701  # ~2.72 inches
run.add_picture(str(image_path), width=Inches(width_inches), height=Inches(height_inches))
```

**Result**: All images in text boxes will be exactly 11.56cm x 6.92cm

#### 2. `_insert_poc_images()` (Line 831-843)
**Purpose**: Inserts images directly in cell (fallback if no text box)

**Changes:**
```python
# OLD: Auto-calculated width based on max 6 inches
width = self._calculate_image_width(image_path, max_width=6.0)
run.add_picture(str(image_path), width=Inches(width))

# NEW: Fixed dimensions (same as text box)
target_width_cm = 11.56
target_height_cm = 6.92
width_inches = target_width_cm * 0.393701
height_inches = target_height_cm * 0.393701
run.add_picture(str(image_path), width=Inches(width_inches), height=Inches(height_inches))
```

**Result**: Images won't overflow table boundaries

### Benefits

1. **Consistent Sizing**: All PoC images will be the same size
2. **No Overflow**: Images guaranteed to fit within table cells
3. **Text Box Match**: Images match text box dimensions exactly
4. **Predictable Output**: No auto-scaling calculations

### Conversion Reference

```
11.56 cm = 4.55 inches = 327.6 pixels (at 72 DPI)
6.92 cm = 2.72 inches = 195.8 pixels (at 72 DPI)
```

### Aspect Ratio

```
11.56 : 6.92 = 1.67:1 (approximately 16:9.5)
```

If your original images have different aspect ratios, they will be:
- Stretched if narrower
- Compressed if wider
- To maintain quality, use images close to 11.56cm x 6.92cm or 16:9.5 ratio

### Testing

After this change:
1. All images will be inserted at 11.56cm x 6.92cm
2. Images will fit within text box boundaries
3. Images won't overflow table cells
4. Consistent appearance across all vulnerabilities

### If Images Still Don't Appear

If the text box insertion still doesn't work, possible issues:

1. **XPath Detection Failure**
   - The XPath might not be finding the text box
   - Check logs for "No text boxes found" message

2. **Document Relationship Issue**
   - The document might not be properly linked for image insertion
   - This is a python-docx limitation with text boxes

3. **Fallback Behavior**
   - If text box insertion fails, images will be inserted directly in cell
   - They'll still use the correct 11.56cm x 6.92cm dimensions

### Recommended Image Specifications

For best results, prepare your PoC images as:
- **Format**: PNG
- **Dimensions**: 1166 x 698 pixels (or close to 16:9.5 ratio)
- **File size**: < 2MB per image
- **Naming**: 1.png, 2.png, 3.png, etc.

### Next Steps

1. Restart the backend service (if running)
2. Generate a test report
3. Check if images appear in text boxes
4. Verify image dimensions in generated document
5. If images still don't show in text box, check logs for errors

---

**Update Date**: February 12, 2026  
**Status**: ✅ Image dimensions fixed to 11.56cm x 6.92cm
