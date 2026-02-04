"""
Update Society Membership Draft Page (ID 4159) - MINIMAL TEST
Start with just the hero panel to test ACF structure
"""

from wordpress_client import WordPressClient

def main():
    """Update just the hero panel to test"""
    client = WordPressClient()
    page_id = 4159

    print(f"Updating page {page_id} with minimal ACF structure (hero only)...")

    # Build just ONE hero panel using exact structure from existing page
    panels = []

    panels.append({
        "acf_fc_layout": "hero",
        "image_positioning": False,
        "hero_image": 4063,
        "hero_title": "Your Members Pay for CPD. Can You Identify Their Gaps AND Prove You're Closing Them?",
        "hero_content": "<p>Most societies track credits. But you can't identify which clinical gaps exist, create pathways to close them, or prove it's working. Our system does all three-and better engagement drives better insights, which drives more effective gap closure.</p>",
        "hero_button": "Book a 30-Minute Meeting",
        "hero_link": "/contact"
    })

    print(f"Created {len(panels)} ACF panel")

    # Update page
    try:
        result = client.post(
            f"pages/{page_id}",
            data={
                "acf": {
                    "panels": panels
                },
                "status": "draft"
            }
        )

        print("SUCCESS: Page updated!")
        print(f"View at: https://yokehealth.com/?page_id={page_id}&preview=true")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
