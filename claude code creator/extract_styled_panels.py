"""Extract styled panel examples from page 4146"""

from wordpress_client import WordPressClient
import json

client = WordPressClient()
page = client.get_page(4146)
panels = page['acf']['panels']

print("=" * 60)
print("STYLED PANEL EXAMPLES FROM PAGE 4146")
print("=" * 60)

# Get hero with styling
hero = panels[0]
print("\n[HERO PANEL]")
print(json.dumps(hero, indent=2))

# Get first two_col_panel with content
for i, panel in enumerate(panels):
    if panel.get('acf_fc_layout') == 'two_col_panel' and panel.get('content_two_col'):
        print(f"\n[TWO_COL_PANEL - Panel {i}]")
        print(f"Reverse: {panel.get('reverse')}")
        print(f"Width: {panel.get('width')}")
        print(f"Image: {panel.get('image_two_col')}")
        print(f"Background: {panel.get('background_colour')}")
        print(f"\nContent (first 800 chars):")
        print(panel.get('content_two_col', '')[:800])
        print("\n...")
        break

# Get first content_panel
for i, panel in enumerate(panels):
    if panel.get('acf_fc_layout') == 'content_panel':
        print(f"\n[CONTENT_PANEL - Panel {i}]")
        print(f"Alignment: {panel.get('alignment')}")
        print(f"Background: {panel.get('background_colour')}")
        print(f"\nContent (first 500 chars):")
        print(panel.get('content_block', '')[:500])
        print("\n...")
        break

# Get small_cta_banner
for i, panel in enumerate(panels):
    if panel.get('acf_fc_layout') == 'small_cta_banner':
        print(f"\n[SMALL_CTA_BANNER - Panel {i}]")
        print(f"Image: {panel.get('image_cta_small')}")
        print(f"Content type: {panel.get('content_type')}")
        print(f"\nContent (first 500 chars):")
        print(panel.get('content_cta_small', '')[:500])
        print("\n...")
        break

print("\n" + "=" * 60)
print("KEY STYLING PATTERNS OBSERVED")
print("=" * 60)
