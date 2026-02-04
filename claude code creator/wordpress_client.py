"""
WordPress API Client with ACF Support
Client for YokeHealth.com WordPress site
"""

import requests
import json
from pathlib import Path
from base64 import b64encode

class WordPressClient:
    """WordPress REST API client with ACF field support"""

    def __init__(self):
        """Initialize WordPress client from credentials store"""
        creds_path = Path(__file__).parent / "CREDENTIALS_STORE.json"
        with open(creds_path, 'r') as f:
            creds = json.load(f)
            wp_creds = creds['services']['wordpress_yokehealth']

        self.site_url = wp_creds['site_url']
        self.api_url = wp_creds['api_url']
        self.username = wp_creds['username']
        self.app_password = wp_creds['app_password'].replace(' ', '')

        # Basic auth header
        auth_string = f"{self.username}:{self.app_password}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = b64encode(auth_bytes).decode('ascii')

        self.headers = {
            "Authorization": f"Basic {auth_b64}",
            "Content-Type": "application/json"
        }

    def _request(self, method, endpoint, **kwargs):
        """Make authenticated request to WordPress API"""
        url = f"{self.api_url}/{endpoint}"

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"WordPress API Error: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            raise

    def get(self, endpoint, params=None):
        """GET request"""
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint, data=None):
        """POST request"""
        return self._request("POST", endpoint, json=data)

    def patch(self, endpoint, data=None):
        """PATCH request"""
        return self._request("PATCH", endpoint, json=data)

    def delete(self, endpoint):
        """DELETE request"""
        return self._request("DELETE", endpoint)

    # Page operations

    def get_page(self, page_id):
        """Get page by ID"""
        return self.get(f"pages/{page_id}")

    def create_page(self, title, acf_panels=None, status="draft", **page_data):
        """
        Create new WordPress page with ACF fields

        Args:
            title: Page title
            acf_panels: List of ACF panel objects
            status: 'draft' or 'publish'
            **page_data: Additional page fields

        Returns:
            Created page object
        """
        data = {
            "title": title,
            "status": status,
            **page_data
        }

        # Add ACF panels if provided
        if acf_panels:
            data["acf"] = {
                "panels": acf_panels
            }

        return self.post("pages", data=data)

    def update_page(self, page_id, acf_panels=None, **update_data):
        """
        Update existing page

        Args:
            page_id: Page ID
            acf_panels: List of ACF panel objects
            **update_data: Fields to update

        Returns:
            Updated page object
        """
        data = update_data.copy()

        # Add ACF panels if provided
        if acf_panels:
            data["acf"] = {
                "panels": acf_panels
            }

        return self.post(f"pages/{page_id}", data=data)

    def list_pages(self, per_page=10, status="any"):
        """List pages"""
        params = {
            "per_page": per_page,
            "status": status
        }
        return self.get("pages", params=params)

    # ACF Panel builders

    def build_hero_panel(self, title, subtitle, button_text=None, button_url=None):
        """Build hero panel"""
        panel = {
            "acf_fc_layout": "hero",
            "title": title,
            "subtitle": subtitle
        }

        if button_text and button_url:
            panel["button"] = {
                "title": button_text,
                "url": button_url,
                "target": ""
            }

        return panel

    def build_two_col_panel(self, left_content, right_content, left_title=None, right_title=None):
        """Build two-column panel"""
        return {
            "acf_fc_layout": "two_col_panel",
            "left_column": {
                "title": left_title or "",
                "content": left_content
            },
            "right_column": {
                "title": right_title or "",
                "content": right_content
            }
        }

    def build_content_panel(self, content, title=None):
        """Build single content panel"""
        return {
            "acf_fc_layout": "content_panel",
            "title": title or "",
            "content": content
        }

    def build_cta_panel(self, heading, button_text, button_url, subtext=None):
        """Build call-to-action panel"""
        panel = {
            "acf_fc_layout": "cta_panel",
            "heading": heading,
            "button": {
                "title": button_text,
                "url": button_url,
                "target": ""
            }
        }

        if subtext:
            panel["subtext"] = subtext

        return panel

    def build_spacing_panel(self, height="medium"):
        """Build spacing panel"""
        return {
            "acf_fc_layout": "spacing",
            "height": height  # small, medium, large
        }


if __name__ == "__main__":
    # Test connection
    client = WordPressClient()
    print("WordPress client initialized successfully")
    print(f"Site: {client.site_url}")

    # List recent pages
    try:
        pages = client.list_pages(per_page=5)
        print(f"\nRecent pages ({len(pages)}):")
        for page in pages:
            print(f"  - {page['title']['rendered']} (ID: {page['id']})")
    except Exception as e:
        print(f"Error listing pages: {e}")
