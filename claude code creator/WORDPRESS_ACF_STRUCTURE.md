# WordPress ACF Panel Structure for YokeHealth.com

**Last Updated:** 2026-02-04
**Theme:** Yoke Health Custom Theme
**Page Tested:** 4159 (Society membership DRAFT)

## Important Discovery

The YokeHealth.com WordPress theme uses **specific ACF field names** that differ from generic ACF panel builders. The `wordpress_client.py` helper methods (`build_hero_panel()`, `build_content_panel()`, etc.) use INCORRECT field names and must be updated or not used.

## Verified Panel Layouts

These panel types are confirmed to work with the theme:

### 1. hero
```python
{
    "acf_fc_layout": "hero",
    "image_positioning": False,  # Boolean
    "hero_image": 4063,  # Image ID (integer)
    "hero_title": "Title text",  # String
    "hero_content": "<p>HTML content</p>",  # HTML string
    "hero_button": "Button text",  # String
    "hero_link": "/contact"  # URL string
}
```

### 2. content_panel
```python
{
    "acf_fc_layout": "content_panel",
    "alignment": "left",  # "left", "center", or "right"
    "background_colour": False,  # False or color string
    "content_block": "<h2>HTML content</h2><p>Text</p>"  # HTML string
}
```
**CRITICAL:** Use `content_block` NOT `content`!

### 3. two_col_panel
```python
{
    "acf_fc_layout": "two_col_panel",
    "reverse": False,  # Boolean
    "alignment": False,  # False or alignment value
    "width": "half",  # "half", "third", etc.
    "image_two_col": None,  # Image ID (integer) or None (NOT False!)
    "background_colour": "",  # Color string or empty
    "border_colour": "",  # Color string or empty
    "content_two_col": "<h2>HTML</h2><p>Text</p>"  # HTML string - NOT separate columns!
}
```
**CRITICAL:**
- `image_two_col` must be integer or None, NOT False!
- Uses single `content_two_col` field, NOT separate left/right columns!

### 4. spacing
```python
{
    "acf_fc_layout": "spacing",
    "spacing_size": "medium"  # "small", "medium", or "large"
}
```
**CRITICAL:** Use `spacing_size` NOT `height`!

### 5. small_cta_banner
```python
{
    "acf_fc_layout": "small_cta_banner",
    "reverse_panel": False,  # Boolean
    "content_type": "button",  # "button", "nobutton", etc.
    "image_cta_small": 4063,  # Image ID (integer)
    "content_cta_small": "<h2>Title</h2><p>Content</p>",  # HTML string
    "cta_button_small": "Button text",  # String
    "cta_link_small": "/contact"  # URL string
}
```

### 6. twentyfour_image
```python
{
    "acf_fc_layout": "twentyfour_image",
    "image": 1234  # Image ID (integer)
}
```

### 7. testimonial
```python
{
    "acf_fc_layout": "testimonial",
    "testimonials": []  # Array of testimonial objects
}
```

### 8. twentyfour_packery_image_layout
```python
{
    "acf_fc_layout": "twentyfour_packery_image_layout",
    "section_id": "gallery",  # String
    "header": "Gallery Title",  # String
    "images": []  # Array of image IDs
}
```

### 9. twentyfour_awards_panel
```python
{
    "acf_fc_layout": "twentyfour_awards_panel",
    "title": "Awards",  # String
    "sub_title": "Subtitle",  # String
    "header": "Header",  # String
    "awards": [],  # Array of award objects
    "button_label": "Learn More",  # String
}
```

## Common Mistakes to Avoid

1. ❌ Using `content` instead of `content_block` in content_panel
2. ❌ Using `height` instead of `spacing_size` in spacing
3. ❌ Using `False` instead of `None` for optional image fields
4. ❌ Using `title` and `subtitle` instead of `hero_title` and `hero_content` in hero
5. ❌ Expecting separate `left_column` and `right_column` in two_col_panel
6. ❌ Using generic `button` object instead of specific button fields

## Working Update Script

See: `update_society_page_FINAL.py`

This script successfully updated page 4159 with 19 ACF panels using the correct structure.

## wordpress_client.py Status

**NEEDS UPDATE:** The helper methods in `wordpress_client.py` use incorrect field names and should be updated or avoided. For now, manually construct panel dictionaries using the structures above.

## Testing a Page Update

1. Always test with minimal panels first (just hero)
2. Use `inspect_page_4159.py` to verify the update
3. Check the modified timestamp in the API response
4. Preview the page in WordPress admin to see visual changes

## References

- Page 4146 and 3849: Med-Comms Agency pages with 41 panels showing all layout types
- `inspect_acf_panels.py`: Script to discover available panel layouts
- `inspect_panel_fields.py`: Script to get exact field structures
