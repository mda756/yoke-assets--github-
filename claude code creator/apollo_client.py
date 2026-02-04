"""
Apollo.io API Client
Base client for all Apollo API operations
"""

import requests
import json
from pathlib import Path

class ApolloClient:
    """Base Apollo API client with authentication"""

    def __init__(self, api_key=None):
        """Initialize Apollo client with API key from credentials store"""
        if api_key:
            self.api_key = api_key
        else:
            # Load from CREDENTIALS_STORE.json
            creds_path = Path(__file__).parent / "CREDENTIALS_STORE.json"
            with open(creds_path, 'r') as f:
                creds = json.load(f)
                self.api_key = creds['services']['apollo_io']['api_key']

        self.base_url = "https://api.apollo.io/v1"
        self.headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def _request(self, method, endpoint, **kwargs):
        """Make authenticated request to Apollo API"""
        url = f"{self.base_url}/{endpoint}"

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
            print(f"Apollo API Error: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            raise

    def get(self, endpoint, params=None):
        """GET request"""
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint, data=None, json_data=None):
        """POST request"""
        return self._request("POST", endpoint, data=data, json=json_data)

    def patch(self, endpoint, data=None, json_data=None):
        """PATCH request"""
        return self._request("PATCH", endpoint, data=data, json=json_data)

    def delete(self, endpoint):
        """DELETE request"""
        return self._request("DELETE", endpoint)

    # Core Apollo API methods

    def search_people(self, **filters):
        """
        Search for people in Apollo

        Common filters:
        - person_titles: List of job titles
        - person_seniorities: List of seniorities
        - organization_num_employees_ranges: List of company size ranges
        - q_keywords: Keyword search
        - person_locations: List of locations
        - organization_industry_tag_ids: List of industry IDs
        """
        return self.post("mixed_people/api_search", json_data=filters)

    def get_person(self, person_id):
        """Get person details by ID"""
        return self.get(f"people/{person_id}")

    def create_contact(self, **contact_data):
        """Create new contact in Apollo"""
        return self.post("contacts", json_data=contact_data)

    def update_contact(self, contact_id, **update_data):
        """Update existing contact"""
        return self.patch(f"contacts/{contact_id}", json_data=update_data)

    def create_list(self, name, **list_data):
        """Create new Apollo list"""
        data = {"name": name, **list_data}
        return self.post("emailer_campaigns/contact_lists", json_data=data)

    def add_to_list(self, list_id, contact_ids):
        """Add contacts to list"""
        data = {
            "contact_ids": contact_ids if isinstance(contact_ids, list) else [contact_ids]
        }
        return self.post(f"emailer_campaigns/contact_lists/{list_id}/add_contacts", json_data=data)

    def get_sequences(self):
        """Get all email sequences"""
        return self.get("emailer_campaigns")

    def create_sequence(self, name, **sequence_data):
        """Create new email sequence"""
        data = {"name": name, **sequence_data}
        return self.post("emailer_campaigns", json_data=data)

    def add_to_sequence(self, sequence_id, contact_ids):
        """Add contacts to sequence"""
        data = {
            "contact_ids": contact_ids if isinstance(contact_ids, list) else [contact_ids],
            "emailer_campaign_id": sequence_id
        }
        return self.post("emailer_campaigns/add_contact_ids", json_data=data)

    def enrich_person(self, email=None, first_name=None, last_name=None, domain=None):
        """Enrich person data"""
        data = {}
        if email:
            data["email"] = email
        if first_name:
            data["first_name"] = first_name
        if last_name:
            data["last_name"] = last_name
        if domain:
            data["domain"] = domain

        return self.post("people/match", json_data=data)


if __name__ == "__main__":
    # Test connection
    client = ApolloClient()
    print("Apollo client initialized successfully")
    print(f"API Key: {client.api_key[:10]}...")
