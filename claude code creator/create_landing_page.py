"""
Landing Page Creator Template - Medical Societies
Use this as template for all future ICP landing pages

Based on working page 4165 structure
"""

from wordpress_client import WordPressClient
import sys

# Apollo meeting link (update if changed)
MEETING_LINK = "https://app.apollo.io/#/meet/Matt@Yoke/25-min"

# Available images for alternating layout
IMAGES = [3639, 3563, 3569, 3564, 3604, 894, 3567, 3742]

def create_landing_page(icp_name, page_id=None):
    """
    Create a landing page using the correct structure

    Args:
        icp_name: Name of the ICP (for content lookup)
        page_id: Existing page ID to update, or None to create new
    """
    client = WordPressClient()

    print(f"Creating landing page for: {icp_name}")

    panels = []

    # HERO PANEL
    panels.append({
        "acf_fc_layout": "hero",
        "image_positioning": False,
        "hero_image": 4063,
        "hero_title": "YOUR MAIN HEADLINE HERE",
        "hero_content": "<h3><span style=\"color: #ffffff;\">Your subtitle here</span></h3>",
        "hero_button": "Book a 30-Minute Meeting",
        "hero_link": MEETING_LINK
    })

    # SECTION 1 - Problem (Image RIGHT)
    panels.append({
        "acf_fc_layout": "two_col_panel",
        "reverse": True,
        "alignment": False,
        "width": "third",
        "image_two_col": IMAGES[0],
        "background_colour": "",
        "border_colour": "",
        "content_two_col": """<h1><span style="color: #003366;"><strong>Section 1 Heading</strong></span></h1>
<p>Sub-paragraph 1</p>
<p>Sub-paragraph 2</p>
<p>&nbsp;</p>
<ul class="custom-ticks yellow">
<li><strong>Point 1:</strong> Description</li>
<li><strong>Point 2:</strong> Description</li>
<li><strong>Point 3:</strong> Description</li>
</ul>
<p>&nbsp;</p>
<h3><span style="color: #003366;"><em>Closing line with emphasis</em></span></h3>"""
    })

    panels.append({"acf_fc_layout": "spacing", "spacing_size": "medium"})

    # SECTION 2 - Consequence (Image LEFT)
    panels.append({
        "acf_fc_layout": "two_col_panel",
        "reverse": False,
        "alignment": False,
        "width": "third",
        "image_two_col": IMAGES[1],
        "background_colour": "",
        "border_colour": "",
        "content_two_col": """<h1><span style="color: #003366;"><strong>Section 2 Heading</strong></span></h1>
<p>Sub-paragraph</p>
<p>&nbsp;</p>
<ul class="custom-ticks yellow">
<li><strong>Point 1:</strong> Description</li>
<li><strong>Point 2:</strong> Description</li>
</ul>
<p>&nbsp;</p>
<h3><span style="color: #003366;"><em>Closing line</em></span></h3>"""
    })

    panels.append({"acf_fc_layout": "spacing", "spacing_size": "large"})

    # SECTION 3 - Solution (Image RIGHT)
    panels.append({
        "acf_fc_layout": "two_col_panel",
        "reverse": True,
        "alignment": False,
        "width": "third",
        "image_two_col": IMAGES[2],
        "background_colour": "",
        "border_colour": "",
        "content_two_col": """<h1><span style="color: #003366;"><strong>Section 3 Heading</strong></span></h1>
<p>Sub-paragraph</p>
<p>&nbsp;</p>
<ul class="custom-ticks yellow">
<li><strong>Point 1:</strong> Description</li>
<li><strong>Point 2:</strong> Description</li>
</ul>
<p>&nbsp;</p>
<h3><span style="color: #003366;"><em>Closing line</em></span></h3>"""
    })

    panels.append({"acf_fc_layout": "spacing", "spacing_size": "medium"})

    # PROOF BANNER
    panels.append({
        "acf_fc_layout": "small_cta_banner",
        "reverse_panel": False,
        "content_type": "nobutton",
        "image_cta_small": 2693,
        "content_cta_small": """<h2><span style="color: #f79801;">Proven Platform</span></h2>
<strong><span style="color: #f79801;">3 MAJOR INDUSTRY AWARDS</span></strong>
<span style="font-weight: 400;">Recognition text</span>""",
        "cta_button_small": "",
        "cta_link_small": ""
    })

    panels.append({"acf_fc_layout": "spacing", "spacing_size": "large"})

    # FINAL CTA
    panels.append({
        "acf_fc_layout": "content_panel",
        "alignment": "left",
        "background_colour": False,
        "content_block": f"""<h1><span style="color: #003366;"><strong>See It In Action</strong></span></h1>
<p>Book a meeting to see:</p>
<p>&nbsp;</p>
<ul class="custom-ticks yellow">
<li>Feature 1</li>
<li>Feature 2</li>
<li>Feature 3</li>
</ul>
<p>&nbsp;</p>
<p><a class="button" href="{MEETING_LINK}">Book Your 30-Minute Meeting</a></p>"""
    })

    print(f"Created {len(panels)} panels")

    # Update or create page
    if page_id:
        print(f"Updating existing page {page_id}...")
        result = client.post(
            f"pages/{page_id}",
            data={
                "acf": {"panels": panels},
                "status": "draft"
            }
        )
    else:
        print("Creating new page...")
        result = client.post(
            "pages",
            data={
                "title": f"{icp_name} - Yoke Health",
                "status": "draft",
                "acf": {"panels": panels}
            }
        )

    print(f"SUCCESS!")
    print(f"Page ID: {result['id']}")
    print(f"Status: {result['status']}")
    print(f"Preview: https://yokehealth.com/?page_id={result['id']}&preview=true")
    print(f"Edit: https://yokehealth.com/wp-admin/post.php?post={result['id']}&action=edit")

    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_landing_page.py <icp_name> [page_id]")
        print("Example: python create_landing_page.py medical_societies")
        print("Example: python create_landing_page.py medical_societies 4165")
        sys.exit(1)

    icp_name = sys.argv[1]
    page_id = int(sys.argv[2]) if len(sys.argv) > 2 else None

    create_landing_page(icp_name, page_id)
