# Landing Page Creation Guide - Medical Societies (and all ICPs)

**Last Updated:** 2026-02-04
**Tested On:** Page 4165 (Society membership DRAFT2)
**Status:** ✅ Working - This is the CORRECT method

---

## Overview

This guide documents the CORRECT way to create landing pages for YokeHealth.com using ACF panels. Follow this exactly to avoid breaking styling, spacing, and images.

---

## Key Learnings from Debugging

### What Went Wrong Initially

1. ❌ Used wrong field names (`content` instead of `content_block`)
2. ❌ Used wrong colors (cyan instead of dark blue for headers)
3. ❌ Missing proper spacers (`<p>&nbsp;</p>`)
4. ❌ No alternating image layout
5. ❌ Center alignment instead of left
6. ❌ Wrong status (pending) blocking publish

### What Works Now

1. ✅ Correct ACF field names from theme
2. ✅ GitHub formatting rules (ACF-HTML-GENERATOR-RULESET-FINAL.txt)
3. ✅ Alternating image/text layout
4. ✅ Left alignment throughout
5. ✅ Proper spacers and closing lines
6. ✅ Status set to "draft" for editing

---

## Required Files and Documentation

### GitHub Knowledge Files (Already Available)

Located in: `chatgpt instructions and knowledge (For ingest by cluade code)/PROJECT  WordPress ACF HTML Block Generator/`

- **ACF-HTML-GENERATOR-RULESET-FINAL.txt** - Mandatory formatting rules
- **ACF-HTML-BLOCK-EXAMPLE-PATTERNS.txt** - Working examples

### Droplet Files (Need to Sync)

- `WORDPRESS_ACF_STRUCTURE.md` - Field reference
- `LANDING_PAGE_CREATION_GUIDE.md` - This file
- `create_landing_page.py` - Template script
- `wordpress_client.py` - Updated with correct methods

---

## Step-by-Step: Create a New Landing Page

### Step 1: Prepare Content

Content must be structured as:
- Hero (title + subtitle)
- 5-7 content sections with:
  - Main heading
  - Sub-paragraphs
  - Bullet list with custom ticks
  - Closing line (italic emphasis)

### Step 2: Choose Images

Available images (alternating left/right):
- 3639 (first - right)
- 3563 (second - left)
- 3569 (third - right)
- 3564 (fourth - left)
- 3604 (fifth - right)
- 894 (sixth - left)
- 3567, 3742, 3663, 3602 (additional)

Pattern: reverse=True (image right), reverse=False (image left), repeat

### Step 3: Use the Template Script

```bash
python create_landing_page.py --icp medical_societies --page-id NEW
```

### Step 4: Verify Before Publishing

1. Check draft preview
2. Verify all images show
3. Verify left alignment
4. Verify spacing looks good
5. Update meeting link to Apollo: `https://app.apollo.io/#/meet/Matt@Yoke/25-min`

### Step 5: Publish

```python
# Set status to "draft" first for review
status = "draft"

# After approval, publish
status = "publish"
```

---

## Formatting Rules (MANDATORY)

From `ACF-HTML-GENERATOR-RULESET-FINAL.txt`:

### 1. Main Heading (Every Section)

```html
<h1><span style="color: #003366;"><strong>HEADING TEXT</strong></span></h1>
```

**Rules:**
- Always `<h1>` (NOT h2, h3)
- Always dark blue `#003366` (NOT cyan #00ffff)
- Always `<strong>` inside span
- No exceptions

### 2. Sub-Header Paragraphs

```html
<h1>...</h1>
<p>First sub-header sentence...</p>
<p>Second sub-header sentence...</p>
```

**Rules:**
- Use normal `<p>` elements
- No `<p>&nbsp;</p>` between sub-headers
- No blank lines between them

### 3. Mandatory Spacer BEFORE List

```html
<p>Last sub-header paragraph</p>
<p>&nbsp;</p>
<ul class="custom-ticks yellow">
```

**Rules:**
- Exactly one `<p>&nbsp;</p>` before first `<ul>`
- No blank lines
- Mandatory - no exceptions

### 4. Lists with Custom Ticks

```html
<ul class="custom-ticks yellow">
  <li><strong>Label:</strong> Description text</li>
  <li><strong>Label:</strong> Description text</li>
</ul>
```

**Rules:**
- Always use class `custom-ticks yellow`
- Use `<strong>` for labels
- No other classes allowed

### 5. Mandatory Spacer AFTER List

```html
</ul>
<p>&nbsp;</p>
<h3><span style="color: #003366;"><em>Closing line</em></span></h3>
```

**Rules:**
- Exactly one `<p>&nbsp;</p>` after last `</ul>`
- Required before closing line
- No exceptions

### 6. Closing Line (Every Section)

```html
<h3><span style="color: #003366;"><em>CLOSING LINE TEXT</em></span></h3>
```

**Rules:**
- Always `<h3>` (NOT p, NOT h1)
- Always dark blue `#003366`
- Always `<em>` inside span
- No alternatives

---

## ACF Panel Structure

### Hero Panel

```python
{
    "acf_fc_layout": "hero",
    "image_positioning": False,
    "hero_image": 4063,  # Image ID
    "hero_title": "Main headline",
    "hero_content": "<h3><span style=\"color: #ffffff;\">Subtitle</span></h3>",
    "hero_button": "Button text",
    "hero_link": "https://app.apollo.io/#/meet/Matt@Yoke/25-min"
}
```

### Two Column Panel (with image)

```python
{
    "acf_fc_layout": "two_col_panel",
    "reverse": True,  # True = image right, False = image left
    "alignment": False,
    "width": "third",  # Image takes 1/3, text takes 2/3
    "image_two_col": 3639,  # Image ID or None
    "background_colour": "",
    "border_colour": "",
    "content_two_col": """HTML content here"""  # Single field, NOT separate columns!
}
```

**Critical:** Use `content_two_col` (NOT separate left/right columns!)

### Content Panel (no image)

```python
{
    "acf_fc_layout": "content_panel",
    "alignment": "left",  # "left", "center", or "right"
    "background_colour": False,
    "content_block": """HTML content here"""  # Use content_BLOCK not content!
}
```

**Critical:** Use `content_block` (NOT `content`!)

### Spacing Panel

```python
{
    "acf_fc_layout": "spacing",
    "spacing_size": "small"  # "small", "medium", or "large"
}
```

**Critical:** Use `spacing_size` (NOT `height`!)

### Small CTA Banner

```python
{
    "acf_fc_layout": "small_cta_banner",
    "reverse_panel": False,
    "content_type": "nobutton",  # or "button"
    "image_cta_small": 2693,
    "content_cta_small": """HTML content""",
    "cta_button_small": "Button text",
    "cta_link_small": "URL"
}
```

---

## Typical Landing Page Structure

```
1. Hero Panel
2. Two-Col Panel (Image RIGHT, reverse=True) - Main pain/problem
3. Spacing (medium)
4. Two-Col Panel (Image LEFT, reverse=False) - Consequence
5. Spacing (large)
6. Two-Col Panel (Image RIGHT, reverse=True) - Solution
7. Spacing (medium)
8. Two-Col Panel (Image LEFT, reverse=False) - What You Get
9. Spacing (medium)
10. Two-Col Panel (Image RIGHT, reverse=True) - How It Works
11. Spacing (medium)
12. Two-Col Panel (Image LEFT, reverse=False) - Why It Works
13. Spacing (medium)
14. Small CTA Banner - Awards/proof
15. Spacing (large)
16. Content Panel (left-aligned) - Final CTA with button
```

---

## Common Mistakes to Avoid

1. ❌ Using `content` instead of `content_block`
2. ❌ Using `height` instead of `spacing_size`
3. ❌ Using cyan (#00ffff) for main headers (should be #003366)
4. ❌ Using False for `image_two_col` (must be integer or None)
5. ❌ Center-aligning everything (use left alignment)
6. ❌ Forgetting spacers before/after lists
7. ❌ Not alternating image position (gets monotonous)
8. ❌ Using separate left/right columns (use single `content_two_col`)
9. ❌ Setting status to "pending" (use "draft" or "publish")
10. ❌ Using wrong meeting link (use Apollo: https://app.apollo.io/#/meet/Matt@Yoke/25-min)

---

## Testing Checklist

Before marking complete:

- [ ] All images display correctly
- [ ] Images alternate left/right down the page
- [ ] All content is left-aligned (not center)
- [ ] Spacing looks consistent (use preview)
- [ ] Custom tick marks show on all lists
- [ ] Headers are dark blue (#003366)
- [ ] Closing lines are italic
- [ ] Meeting link goes to Apollo booking
- [ ] Page status is "draft" for review
- [ ] Preview link works: `https://yokehealth.com/?page_id=XXXX&preview=true`
- [ ] Can publish from WordPress admin

---

## Files Reference

### Working Example
- **Page 4165:** Society membership DRAFT2
- **URL:** https://yokehealth.com/yoke-for-learning-development-medcomms-publishers-2-2-2/
- **Script:** `update_page_4165_FINAL_IMAGES.py`

### Reference Pages
- **Page 4146:** Med-Comms Agency MASTER (41 panels, all layouts)
- **Page 3849:** Med-Comms Agency MASTER (copy)

### Inspection Tools
- `inspect_page_4165.py` - Check page structure
- `inspect_acf_panels.py` - Find available layouts
- `inspect_panel_fields.py` - Get exact field structures

---

## Quick Command Reference

```bash
# Inspect a page
python inspect_page_4165.py

# Create landing page (use template)
python create_landing_page.py --icp medical_societies

# Publish a page
python publish_and_update_link.py

# Check available images
python -c "from wordpress_client import WordPressClient; client = WordPressClient(); page = client.get_page(4146); print([p.get('image_two_col') for p in page['acf']['panels'] if p.get('image_two_col')])"
```

---

## Support Files on Droplet

After syncing, these files will be on droplet at:
`~/yoke-workspace/yoke-assets--github-/claude code creator/`

- `LANDING_PAGE_CREATION_GUIDE.md` (this file)
- `WORDPRESS_ACF_STRUCTURE.md` (field reference)
- `WORDPRESS_UPDATE_LOG.md` (debugging history)
- `wordpress_client.py` (updated client)
- `create_landing_page.py` (template script)
- All inspection tools

---

**Last Tested:** 2026-02-04 on page 4165
**Status:** ✅ Working perfectly
**Next Update:** When new panel types or requirements discovered
