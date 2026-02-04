"""
Apollo ICP Search
Search Apollo for contacts matching ICP criteria
"""

import json
from pathlib import Path
from apollo_client import ApolloClient
from datetime import datetime

class ICPSearcher:
    """Search Apollo using ICP definitions"""

    def __init__(self):
        self.client = ApolloClient()
        self.icp_dir = Path(__file__).parent / "knowledge" / "client_acquisition" / "icps"

    def load_icp(self, icp_id):
        """Load ICP definition from JSON file"""
        # Try exact ID match first
        icp_files = list(self.icp_dir.glob(f"*{icp_id}*.json"))

        if not icp_files:
            # Try fuzzy match by name
            icp_files = list(self.icp_dir.glob("*.json"))

        for icp_file in icp_files:
            with open(icp_file, 'r') as f:
                icp = json.load(f)
                if icp_id in icp['id'] or icp_id.lower() in icp['name'].lower():
                    return icp

        raise ValueError(f"ICP not found: {icp_id}")

    def list_icps(self):
        """List all available ICPs"""
        icps = []
        for icp_file in self.icp_dir.glob("*.json"):
            with open(icp_file, 'r') as f:
                icp = json.load(f)
                icps.append({
                    'id': icp['id'],
                    'name': icp['name'],
                    'priority': icp.get('priority', 'medium'),
                    'file': icp_file.name
                })
        return sorted(icps, key=lambda x: x['name'])

    def build_apollo_filters(self, icp):
        """Convert ICP criteria to Apollo API filters"""
        filters = {
            "page": 1,
            "per_page": 100
        }

        criteria = icp.get('criteria', {})
        apollo_filters = icp.get('apollo_filters', {})

        # Job titles
        if criteria.get('job_titles'):
            filters["person_titles"] = criteria['job_titles']

        # Company size
        if criteria.get('company_size'):
            # Parse "10-500 employees" format
            size = criteria['company_size'].lower()
            if '-' in size:
                min_size, max_size = size.split('-')
                min_size = int(min_size.strip())
                max_size = int(max_size.split()[0].strip())

                # Apollo size ranges
                if min_size <= 10 and max_size >= 50:
                    filters["organization_num_employees_ranges"] = ["1,10", "11,50"]
                elif min_size <= 50 and max_size >= 200:
                    filters["organization_num_employees_ranges"] = ["11,50", "51,200"]
                elif min_size <= 200 and max_size >= 1000:
                    filters["organization_num_employees_ranges"] = ["51,200", "201,500", "501,1000"]
                elif max_size > 1000:
                    filters["organization_num_employees_ranges"] = ["1001,5000", "5001,10000", "10001+"]

        # Keywords
        if apollo_filters.get('keywords_include'):
            filters["q_keywords"] = " OR ".join(apollo_filters['keywords_include'])

        # Locations
        if criteria.get('location'):
            filters["person_locations"] = criteria['location']

        # Departments
        if apollo_filters.get('departments'):
            filters["person_departments"] = apollo_filters['departments']

        return filters

    def search_icp(self, icp_id, max_results=100, save_results=True):
        """
        Search Apollo for contacts matching ICP

        Args:
            icp_id: ICP identifier (ID or name substring)
            max_results: Maximum number of results to return
            save_results: Save results to JSON file

        Returns:
            Dict with search results and metadata
        """
        # Load ICP
        icp = self.load_icp(icp_id)
        print(f"\nSearching Apollo for: {icp['name']}")
        print(f"Priority: {icp.get('priority', 'medium')}")

        # Build filters
        filters = self.build_apollo_filters(icp)
        filters['per_page'] = min(max_results, 100)

        print(f"\nApollo Filters:")
        print(json.dumps(filters, indent=2))

        # Search
        print(f"\nSearching Apollo...")
        try:
            response = self.client.search_people(**filters)

            people = response.get('people', [])
            total = response.get('pagination', {}).get('total_entries', 0)

            print(f"\nFound {len(people)} results (Total available: {total})")

            # Format results
            results = {
                'icp_id': icp['id'],
                'icp_name': icp['name'],
                'search_date': datetime.now().isoformat(),
                'filters_used': filters,
                'total_available': total,
                'results_returned': len(people),
                'contacts': []
            }

            for person in people:
                contact = {
                    'id': person.get('id'),
                    'name': person.get('name'),
                    'title': person.get('title'),
                    'email': person.get('email'),
                    'company': person.get('organization', {}).get('name'),
                    'company_size': person.get('organization', {}).get('estimated_num_employees'),
                    'location': person.get('city'),
                    'linkedin': person.get('linkedin_url'),
                    'phone': person.get('phone_numbers', [{}])[0].get('raw_number') if person.get('phone_numbers') else None
                }
                results['contacts'].append(contact)

            # Save results
            if save_results:
                output_dir = Path(__file__).parent / "knowledge" / "client_acquisition" / "apollo"
                output_dir.mkdir(exist_ok=True, parents=True)

                output_file = output_dir / f"{icp['id']}_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(output_file, 'w') as f:
                    json.dump(results, f, indent=2)

                print(f"\nResults saved to: {output_file.name}")

            return results

        except Exception as e:
            print(f"\nError searching Apollo: {e}")
            raise

    def print_results_summary(self, results):
        """Print summary of search results"""
        print(f"\n{'='*60}")
        print(f"ICP: {results['icp_name']}")
        print(f"Total found: {results['total_available']}")
        print(f"Returned: {results['results_returned']}")
        print(f"{'='*60}\n")

        for i, contact in enumerate(results['contacts'][:10], 1):
            print(f"{i}. {contact['name']}")
            print(f"   Title: {contact['title']}")
            print(f"   Company: {contact['company']} ({contact['company_size']} employees)")
            print(f"   Location: {contact['location']}")
            print(f"   Email: {contact['email']}")
            print()


if __name__ == "__main__":
    import sys

    searcher = ICPSearcher()

    if len(sys.argv) < 2:
        print("\nAvailable ICPs:")
        print("="*60)
        for icp in searcher.list_icps():
            print(f"- {icp['name']} ({icp['priority']})")
            print(f"  ID: {icp['id']}")
            print()

        print("\nUsage: python apollo_icp_search.py <icp_name>")
        print("Example: python apollo_icp_search.py medcomms")

    else:
        icp_id = sys.argv[1]
        max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 100

        results = searcher.search_icp(icp_id, max_results=max_results)
        searcher.print_results_summary(results)
