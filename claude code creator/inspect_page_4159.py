"""Inspect WordPress page 4159 structure"""

from wordpress_client import WordPressClient
import json

client = WordPressClient()
page = client.get_page(4159)

print("=" * 60)
print("PAGE 4159 STRUCTURE")
print("=" * 60)

print(f"\nTitle: {page.get('title', {}).get('rendered', 'N/A')}")
print(f"Status: {page.get('status', 'N/A')}")
print(f"Modified: {page.get('modified', 'N/A')}")

print("\n" + "=" * 60)
print("CONTENT FIELD")
print("=" * 60)
content = page.get('content', {}).get('rendered', '')
print(f"Length: {len(content)} characters")
print(f"First 500 chars: {content[:500]}")

print("\n" + "=" * 60)
print("ACF FIELDS")
print("=" * 60)
acf = page.get('acf', {})
if acf:
    print(json.dumps(acf, indent=2))
else:
    print("No ACF fields found")

print("\n" + "=" * 60)
print("FULL PAGE STRUCTURE (keys)")
print("=" * 60)
print("Top-level keys:", list(page.keys()))

# Save to file for inspection
with open('page_4159_structure.json', 'w') as f:
    json.dump(page, f, indent=2)
    print("\nFull page data saved to: page_4159_structure.json")
