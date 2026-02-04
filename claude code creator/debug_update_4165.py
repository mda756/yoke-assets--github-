"""Debug why page 4165 isn't updating"""

from wordpress_client import WordPressClient
import json

client = WordPressClient()
page_id = 4165

print("=" * 60)
print("DEBUGGING PAGE UPDATE")
print("=" * 60)

# Get current state
print("\n1. Current page state:")
page = client.get_page(page_id)
print(f"   Status: {page.get('status')}")
print(f"   Modified: {page.get('modified')}")
print(f"   Panels: {len(page.get('acf', {}).get('panels', []))}")

# Try minimal update - just change hero title
print("\n2. Attempting minimal update (hero title only)...")
try:
    result = client.post(
        f"pages/{page_id}",
        data={
            "acf": {
                "panels": [
                    {
                        "acf_fc_layout": "hero",
                        "image_positioning": False,
                        "hero_image": 4063,
                        "hero_title": "TEST UPDATE - Medical Societies CPD",
                        "hero_content": "<h3><span style=\"color: #ffffff;\">Testing if updates work</span></h3>",
                        "hero_button": "Test Button",
                        "hero_link": "/contact"
                    }
                ]
            }
        }
    )

    print(f"   API Response: {result.get('status')}")
    print(f"   Modified: {result.get('modified')}")
    print(f"   ID: {result.get('id')}")

except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()

# Check if it actually changed
print("\n3. Checking if update took effect...")
import time
time.sleep(2)  # Wait a moment

page_after = client.get_page(page_id)
panels_after = page_after.get('acf', {}).get('panels', [])
print(f"   Panels after: {len(panels_after)}")
if panels_after:
    print(f"   Hero title: {panels_after[0].get('hero_title', 'N/A')[:80]}")

print("\n4. Full response from update:")
print(json.dumps(result, indent=2))
