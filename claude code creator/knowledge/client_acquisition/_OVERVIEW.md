# Client Acquisition Ecosystem

## How Everything Connects

```
ICP (Ideal Customer Profile)
    ↓
Apollo Searches & Sequences
    ↓
Clients (prospects/leads)
    ↓
Landing Pages (personalized)
    ↓
Conversion
```

## Folder Structure

- **icps/** - ICP definitions (JSON)
- **clients/active/** - Active prospects and clients (JSON)
- **clients/archived/** - Closed/inactive clients (JSON)
- **landing_pages/templates/** - Reusable templates
- **landing_pages/generated/** - Client-specific generated pages
- **apollo/** - Campaign and sequence data
- **workflow_rules.md** - Business logic and decision rules

## Data Flow

1. ICP defines target audience characteristics
2. Apollo uses ICP to find and sequence prospects
3. Clients are created from Apollo results
4. Landing pages generated based on client data + ICP
5. All data cross-referenced by IDs
