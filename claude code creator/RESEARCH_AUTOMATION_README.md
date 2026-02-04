# Research Automation System

## Overview

Modular system to find buying signals for ICPs across multiple sources.

## Quick Start

```bash
# Run full research for an ICP
python research_engine.py medcomms
python research_engine.py biotech
python research_engine.py publishers

# Run specific monitors only
python research_engine.py biotech pain,funding
python research_engine.py medcomms pain,conferences
```

## Signal Priority (Configurable per ICP)

### All ICPs:
1. **Pain discussions** (#1) - Forums, Reddit, G2 reviews, Twitter
2. **Product launches** (#2) - Press releases, company news
3. **Conference activity** (#3) - Event speakers, abstracts

### ICP-Specific:
- **Biotech**: Funding rounds, Phase transitions, FDA calendar
- **Medcomms**: Client wins, digital innovation talks
- **Publishers**: Sponsor partnerships, platform modernization

## Signal Configs

Located in: `research_config/`

Each ICP has:
- Priority signals (weighted 0-1)
- Pain keywords to track
- Intent phrases ("looking for", "need help with")
- Sources to monitor
- Alert thresholds

## Monitors

### 1. Pain Monitor (`monitors/pain_monitor.py`)
- Reddit discussions
- Twitter/X conversations
- G2/Capterra reviews
- Industry forums

### 2. Launch Monitor (Framework ready)
- Press releases (PR Newswire, Business Wire)
- Company news/blogs
- Product announcements

### 3. Conference Monitor (Framework ready)
- Event speaker lists
- Abstract databases
- Conference exhibitors

### 4. Hiring Monitor (Framework ready)
- Company career pages (NOT LinkedIn scraping)
- Job board APIs
- Role growth signals

### 5. Funding Monitor (Framework ready)
- Crunchbase API (requires key)
- Press releases
- Partnership announcements

## Output

Results save to: `research_output/`

Each run creates JSON with:
- All signals found
- Scored prospects
- Evidence/context
- Timestamps

## Customization

### Add New ICP:
1. Copy existing config: `research_config/your_icp_signals.json`
2. Update pain keywords, intent phrases, sources
3. Run: `python research_engine.py your_icp`

### Add New Monitor:
1. Create: `monitors/your_monitor.py`
2. Implement `monitor_signals(config)` method
3. Add to `research_engine.py`

### Adjust Signal Weights:
Edit config file `weight` values (must sum to 1.0)

## Legal & Ethical

✅ Public web search
✅ Public APIs (Reddit, Twitter with auth)
✅ Company career pages
✅ Press releases

❌ LinkedIn scraping (against ToS)
❌ Email harvesting
❌ Unauthorized data collection

## Next Steps

1. **Test monitors** - Run on sample ICPs
2. **Add API keys** - Reddit, Twitter, Crunchbase
3. **Schedule monitoring** - Daily/weekly runs
4. **Build scoring** - Refine prospect scoring
5. **Add alerts** - Notify on high-score signals

## Integration with Apollo

After research identifies prospects:
1. Run: `python research_engine.py biotech`
2. Review: `research_output/biotech_research_*.json`
3. High-score prospects → Apollo search
4. Add to Apollo list → Launch sequence
