"""Check what ACF panel layouts are available in the theme"""

from wordpress_client import WordPressClient
import json

client = WordPressClient()

# Get pages with ACF panels
pages_to_check = [4148, 4146, 4141, 3849]

print("=" * 60)
print("ACF PANEL LAYOUTS FOUND IN YOKEHEALTH.COM THEME")
print("=" * 60)

panel_types_found = set()

for page_id in pages_to_check:
    try:
        page = client.get_page(page_id)
        title = page.get('title', {}).get('rendered', 'N/A')
        acf = page.get('acf', {})
        panels = acf.get('panels', [])

        print(f"\nPage {page_id}: {title}")
        print(f"  Panels: {len(panels)}")

        for i, panel in enumerate(panels):
            layout = panel.get('acf_fc_layout', 'unknown')
            panel_types_found.add(layout)
            print(f"  [{i}] {layout}")

            # Show field names for this layout
            field_names = [k for k in panel.keys() if k != 'acf_fc_layout']
            print(f"      Fields: {', '.join(field_names[:5])}{'...' if len(field_names) > 5 else ''}")

    except Exception as e:
        print(f"\nPage {page_id}: ERROR - {e}")

print("\n" + "=" * 60)
print("SUMMARY: Available Panel Layouts")
print("=" * 60)
for layout in sorted(panel_types_found):
    print(f"  - {layout}")
