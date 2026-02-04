"""Inspect WordPress page 4165 (Draft 2) structure"""

from wordpress_client import WordPressClient
import json

client = WordPressClient()
page = client.get_page(4165)

print("=" * 60)
print("PAGE 4165 STRUCTURE (Draft 2)")
print("=" * 60)

print(f"\nTitle: {page.get('title', {}).get('rendered', 'N/A')}")
print(f"Status: {page.get('status', 'N/A')}")

print("\n" + "=" * 60)
print("ACF PANELS")
print("=" * 60)

acf = page.get('acf', {})
panels = acf.get('panels', [])

print(f"\nTotal panels: {len(panels)}")

for i, panel in enumerate(panels):
    layout = panel.get('acf_fc_layout', 'unknown')
    print(f"\n[{i}] {layout}")

    # Show key fields (not full content)
    if layout == "hero":
        print(f"    hero_title: {panel.get('hero_title', '')[:80]}...")
        print(f"    hero_image: {panel.get('hero_image', 'N/A')}")
        print(f"    hero_button: {panel.get('hero_button', 'N/A')}")
    elif layout == "content_panel":
        print(f"    alignment: {panel.get('alignment', 'N/A')}")
        print(f"    background_colour: {panel.get('background_colour', 'N/A')}")
        content = panel.get('content_block', '')
        print(f"    content_block: {len(content)} chars")
    elif layout == "two_col_panel":
        print(f"    reverse: {panel.get('reverse', 'N/A')}")
        print(f"    width: {panel.get('width', 'N/A')}")
        print(f"    image_two_col: {panel.get('image_two_col', 'N/A')}")
    elif layout == "spacing":
        print(f"    spacing_size: {panel.get('spacing_size', 'N/A')}")
    elif layout == "small_cta_banner":
        print(f"    image_cta_small: {panel.get('image_cta_small', 'N/A')}")
        print(f"    cta_button_small: {panel.get('cta_button_small', 'N/A')}")

# Save full structure for detailed inspection
with open('page_4165_structure.json', 'w') as f:
    json.dump(page, f, indent=2)
    print(f"\n\nFull page data saved to: page_4165_structure.json")
