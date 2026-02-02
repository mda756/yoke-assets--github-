# Field mapping template (fill once from ACF UI)

Goal: make the REST API payload exact and safe.

1) Confirm page ID
- Page ID: 4148

2) Confirm ACF container
- Flexible content field name: panels (CONFIRMED from ACF Field Group)
- Layout names present on page 4148 (list in order):
  1) ______________________
  2) ______________________
  3) ______________________
  ...

3) Identify layouts to NOT change
- Awards layout name(s): ______________________
- Testimonials layout name(s): ______________________
(Leave these untouched in API payloads.)

4) For each layout you WILL edit, capture sub-field names (not labels)
Example:
- hero layout:
  - heading field name: ______________________
  - subheading field name: ______________________
  - body/intro field name: ______________________
- content_panel layout:
  - title field name: ______________________
  - body field name: ______________________
- cta layout:
  - title field name: ______________________
  - body field name: ______________________
  - button label field name: ______________________
  - button url field name: ______________________

How to get these:
WP Admin → Custom Fields → Field Groups → Page Builder → Panels → open each layout → note “Name” for each field.
