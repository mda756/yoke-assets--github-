"""Get exact field structure for content_panel and two_col_panel"""

from wordpress_client import WordPressClient
import json

client = WordPressClient()
page = client.get_page(4146)

panels = page.get('acf', {}).get('panels', [])

print("=" * 60)
print("EXACT FIELD STRUCTURES")
print("=" * 60)

# Find first content_panel
for panel in panels:
    if panel.get('acf_fc_layout') == 'content_panel':
        print("\ncontent_panel structure:")
        print(json.dumps(panel, indent=2))
        break

# Find first two_col_panel
for panel in panels:
    if panel.get('acf_fc_layout') == 'two_col_panel':
        print("\ntwo_col_panel structure:")
        print(json.dumps(panel, indent=2))
        break

# Find first spacing
for panel in panels:
    if panel.get('acf_fc_layout') == 'spacing':
        print("\nspacing structure:")
        print(json.dumps(panel, indent=2))
        break

# Find small_cta_banner
for panel in panels:
    if panel.get('acf_fc_layout') == 'small_cta_banner':
        print("\nsmall_cta_banner structure:")
        print(json.dumps(panel, indent=2))
        break
