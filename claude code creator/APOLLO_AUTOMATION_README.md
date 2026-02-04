# Apollo Automation System

## Quick Start

### 1. Search for ICP contacts

```bash
# List all ICPs
python apollo_icp_search.py

# Search for specific ICP
python apollo_icp_search.py medcomms
python apollo_icp_search.py biotech
python apollo_icp_search.py "hcp publishers"

# Search with limit
python apollo_icp_search.py medcomms 50
```

### 2. Results

Results are saved to:
`knowledge/client_acquisition/apollo/`

Each search creates a JSON file with:
- All matching contacts
- Contact details (name, title, email, company, LinkedIn)
- Search filters used
- Timestamp

## Available ICPs

1. **medcomms_agencies** - Medcomms agencies (HIGH priority)
2. **hcp_publishers** - HCP Publishers/CPD-CME (HIGH priority)
3. **biotech_prelaunch** - Biotech pre-launch (VERY HIGH priority)
4. **contract_publishers** - Contract publishers (MEDIUM priority)
5. **ime_providers** - IME providers (HIGH priority)
6. **kol_engagement** - KOL engagement companies (MEDIUM priority)
7. **medcomms_kol_series** - Medcomms + KOL series (VERY HIGH priority)
8. **platform_foundation** - Platform foundation buyers (MEDIUM priority)
9. **nontech_startups** - Non-tech startups (LOW priority)
10. **jv_cocreation** - JV/Co-creation partners (MEDIUM priority)
11. **single_product_wedge** - Single-product wedge buyers (LOW priority)
12. **medscape_like_platforms** - Medscape-like platforms (HIGH priority)

## Scripts

- **apollo_client.py** - Base Apollo API client
- **apollo_icp_search.py** - Search for ICP contacts
- **apollo_list_builder.py** - Create and manage lists *(coming)*
- **apollo_sequence_builder.py** - Create sequences *(coming)*
- **apollo_research.py** - Deep prospect research *(coming)*

## Next Steps

After searching:
1. Review results JSON file
2. Create Apollo list
3. Build email sequence
4. Research top prospects
5. Launch cadence

## API Credentials

Uses CREDENTIALS_STORE.json automatically.
No configuration needed.
