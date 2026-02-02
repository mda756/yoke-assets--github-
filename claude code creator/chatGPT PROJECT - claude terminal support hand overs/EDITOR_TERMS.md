# Terminology to use (WordPress/ACF)

Use these terms in Claude Code prompts so it edits the correct fields:

- Page Title (WP): top title field.
- ACF Field Group: "Page Builder"
- Flexible Content field: Panels (field name: panels)
- Layout: the block type inside Panels (e.g., hero, content_panel, cta_banner, spacing)
- Sub-fields: fields inside a layout (e.g., heading, subheading, body, buttons, image settings)
- WYSIWYG field: rich text editor used for body copy and bullets.
- Button fields: label + URL + alignment (if alignment field exists).
- Image settings: image size / scale / height / max-height (exact field name UNKNOWN; must be located in layout sub-fields).

Guardrails:
- Do not edit Awards/Testimonial layouts.
- Preserve order of layouts unless specifically required.
