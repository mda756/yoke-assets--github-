"""
Landing Page Generator
Generate ICP-specific landing pages using Yoke positioning framework
"""

import json
from pathlib import Path
from wordpress_client import WordPressClient
from datetime import datetime

class LandingPageGenerator:
    """Generate and deploy ICP-specific landing pages"""

    def __init__(self):
        self.wp_client = WordPressClient()
        self.icp_dir = Path(__file__).parent / "knowledge" / "client_acquisition" / "icps"

        # Load proof points
        self.proof_points = {
            "awards": [
                "BEST USE OF TECHNOLOGY - Evcom Excellence Awards",
                "BEST USE OF DIGITAL DATA VISUALIZATION - Communique Awards",
                "INTERACTIVE COMMUNICATIONS FOR HEALTHCARE PROFESSIONALS - PM Society"
            ],
            "clients": ["Abbvie", "Allergan", "Medscape"],
            "deployment_speed": "48-hour white-label deployment",
            "markets": "10+ programmes across 6+ markets"
        }

    def load_icp(self, icp_id):
        """Load ICP definition"""
        icp_files = list(self.icp_dir.glob("*.json"))

        for icp_file in icp_files:
            with open(icp_file, 'r') as f:
                icp = json.load(f)
                if icp_id in icp['id'] or icp_id.lower() in icp['name'].lower():
                    return icp

        raise ValueError(f"ICP not found: {icp_id}")

    def generate_page_content(self, icp):
        """
        Generate landing page content for ICP
        Returns ACF panels array
        """
        messaging = icp.get('messaging', {})
        pain_platform_outcome = messaging.get('pain_to_platform_to_outcome', {})
        two_lever = icp.get('two_lever_framing', {})

        panels = []

        # HERO PANEL
        hero_title = f"Transform {icp['name']}"
        hero_subtitle = messaging.get('elevator_pitch', messaging.get('value_proposition', ''))

        panels.append(
            self.wp_client.build_hero_panel(
                title=hero_title,
                subtitle=hero_subtitle,
                button_text="Book 15-Min Intro",
                button_url="/contact"
            )
        )

        panels.append(self.wp_client.build_spacing_panel("medium"))

        # PAIN → PLATFORM → OUTCOME SECTION
        left_content = f"""<h3>The Challenge</h3>
<p><strong>{pain_platform_outcome.get('pain', '')}</strong></p>

<h3>The Solution</h3>
<p>{pain_platform_outcome.get('platform', '')}</p>"""

        right_content = f"""<h3>The Outcome</h3>
<p><strong>{pain_platform_outcome.get('outcome', '')}</strong></p>

<h3>Two-Lever Impact</h3>
<ul>
<li><strong>Increase:</strong> {two_lever.get('lever_a', '')}</li>
<li><strong>Reduce:</strong> {two_lever.get('lever_b', '')}</li>
</ul>"""

        panels.append(
            self.wp_client.build_two_col_panel(
                left_content=left_content,
                right_content=right_content
            )
        )

        panels.append(self.wp_client.build_spacing_panel("large"))

        # KEY BENEFITS
        benefits_html = "<h2>What You Get</h2>\n<ul>\n"
        for benefit in messaging.get('key_benefits', [])[:5]:
            benefits_html += f"<li>{benefit}</li>\n"
        benefits_html += "</ul>"

        panels.append(
            self.wp_client.build_content_panel(
                content=benefits_html
            )
        )

        panels.append(self.wp_client.build_spacing_panel("medium"))

        # PROOF POINTS
        proof_html = "<h2>Proven Results</h2>\n"
        proof_html += "<h3>Award-Winning Platform</h3>\n<ul>\n"
        for award in self.proof_points['awards']:
            proof_html += f"<li>{award}</li>\n"
        proof_html += "</ul>\n"

        proof_html += f"<h3>Trusted By</h3>\n<p>{', '.join(self.proof_points['clients'])}</p>\n"
        proof_html += f"<p><strong>{self.proof_points['deployment_speed']}</strong></p>\n"
        proof_html += f"<p>{self.proof_points['markets']}</p>"

        panels.append(
            self.wp_client.build_content_panel(
                content=proof_html
            )
        )

        panels.append(self.wp_client.build_spacing_panel("large"))

        # USE CASES
        if messaging.get('use_cases'):
            use_cases_html = "<h2>Use Cases</h2>\n<ul>\n"
            for use_case in messaging.get('use_cases', []):
                use_cases_html += f"<li>{use_case}</li>\n"
            use_cases_html += "</ul>"

            panels.append(
                self.wp_client.build_content_panel(
                    content=use_cases_html
                )
            )

            panels.append(self.wp_client.build_spacing_panel("medium"))

        # CTA PANEL
        panels.append(
            self.wp_client.build_cta_panel(
                heading="Ready to Transform Your Delivery?",
                button_text="Book 15-Min Intro",
                button_url="/contact",
                subtext="See how Yoke can help your team deliver faster with measurable proof"
            )
        )

        return panels

    def create_landing_page(self, icp_id, status="draft"):
        """
        Generate and create landing page for ICP

        Args:
            icp_id: ICP identifier
            status: 'draft' or 'publish'

        Returns:
            Created page details
        """
        # Load ICP
        icp = self.load_icp(icp_id)
        print(f"\nGenerating landing page for: {icp['name']}")

        # Generate content
        panels = self.generate_page_content(icp)
        print(f"Generated {len(panels)} panels")

        # Create page title
        page_title = f"{icp['name']} - Yoke Health"

        # Create page
        print(f"\nCreating WordPress page (status: {status})...")
        try:
            page = self.wp_client.create_page(
                title=page_title,
                acf_panels=panels,
                status=status
            )

            page_id = page['id']
            page_url = page['link']

            print(f"\n✓ Page created successfully!")
            print(f"  Page ID: {page_id}")
            print(f"  URL: {page_url}")
            print(f"  Edit: {self.wp_client.site_url}/wp-admin/post.php?post={page_id}&action=edit")

            # Save metadata
            metadata = {
                'icp_id': icp['id'],
                'icp_name': icp['name'],
                'page_id': page_id,
                'page_url': page_url,
                'created_date': datetime.now().isoformat(),
                'status': status,
                'panels_count': len(panels)
            }

            output_dir = Path(__file__).parent / "knowledge" / "client_acquisition" / "landing_pages" / "generated"
            output_dir.mkdir(exist_ok=True, parents=True)

            output_file = output_dir / f"{icp['id']}_landing_page_{page_id}.json"
            with open(output_file, 'w') as f:
                json.dump(metadata, f, indent=2)

            print(f"\n  Metadata saved: {output_file.name}")

            return metadata

        except Exception as e:
            print(f"\n✗ Error creating page: {e}")
            raise

    def preview_content(self, icp_id):
        """Preview landing page content without creating"""
        icp = self.load_icp(icp_id)
        print(f"\n{'='*60}")
        print(f"Landing Page Preview: {icp['name']}")
        print(f"{'='*60}\n")

        panels = self.generate_page_content(icp)

        for i, panel in enumerate(panels, 1):
            layout = panel.get('acf_fc_layout', 'unknown')
            print(f"{i}. Panel Type: {layout}")

            if layout == "hero":
                print(f"   Title: {panel.get('title', '')}")
                print(f"   Subtitle: {panel.get('subtitle', '')[:100]}...")
            elif layout == "two_col_panel":
                print(f"   Left: {len(panel.get('left_column', {}).get('content', ''))} chars")
                print(f"   Right: {len(panel.get('right_column', {}).get('content', ''))} chars")
            elif layout == "content_panel":
                print(f"   Content: {len(panel.get('content', ''))} chars")
            elif layout == "cta_panel":
                print(f"   Heading: {panel.get('heading', '')}")

            print()


if __name__ == "__main__":
    import sys

    generator = LandingPageGenerator()

    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  Preview: python landing_page_generator.py preview <icp_name>")
        print("  Create:  python landing_page_generator.py create <icp_name> [draft|publish]")
        print("\nExamples:")
        print("  python landing_page_generator.py preview medcomms")
        print("  python landing_page_generator.py create biotech draft")

    elif sys.argv[1] == "preview":
        icp_id = sys.argv[2]
        generator.preview_content(icp_id)

    elif sys.argv[1] == "create":
        icp_id = sys.argv[2]
        status = sys.argv[3] if len(sys.argv) > 3 else "draft"
        generator.create_landing_page(icp_id, status=status)
