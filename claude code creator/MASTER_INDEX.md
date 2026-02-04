# CLAUDE CODE - MASTER SYSTEM INDEX

**Last Updated:** 2026-02-04 12:00 GMT
**Session:** Strategic pivot to Medical Societies CPD
**Status:** Active - Perpetual context system operational

---

## 🎯 CURRENT PRIORITY

**#1 ICP: Medical Societies CPD (icp_013)** ⭐
- **Score:** 10/10 (PERFECT - First ICP to achieve this)
- **Model:** Portal-based SaaS (not event logistics)
- **Why:** Regulatory pain validated (GMC revalidation), competitor gap confirmed (LMS track completion not outcomes), 10x larger market, standard CPD templates, perfect proof match
- **Target:** UK medical specialty societies (100-500 members to start)
- **Next Action:** Research 5-10 target societies + landing page + 7-day outreach test

**Strategic Pivot:** 2026-02-04
- **From:** KOL Series (event-based, service-heavy, £1-2M market ceiling)
- **To:** Medical Societies CPD (portal-based, true SaaS scale, £5-15M potential)
- **Reason:** Portal model = exponential growth (one setup = 1000s members) vs linear (per-event support)

**Active Prospects:** None yet (research phase)

---

## 📊 SYSTEM STATE

### ICPs Built: 13/13 ✓
All ICPs scored with new methodology (competitor gap, failure moment, no-custom filter)

**Top 5 by Score:**
1. **Medical Societies CPD** (10/10) ⭐ - Portal SaaS, regulatory pain, VALIDATED
2. **KOL Series** (9/10) - Event-based (deprioritized for scale reasons)
3. **HCP Publishers** (8/10) - Platform plug-in
4. **IME Providers** (8/10) - CPD/CME standard
5. **Biotech Pre-Launch** (7/10) - Some custom needed

**Deprioritized (Too Custom):**
- Platform Foundation (4/10) - Want custom builds
- JV/Co-creation (3/10) - MVP needs
- Non-tech Startups (3/10) - Unclear buyers

### Tools Built: 5/5 ✓

1. **Apollo Automation** (`apollo_icp_search.py`)
   - Searches 12 ICPs
   - Auto-loads credentials
   - Saves results to JSON

2. **Landing Page Generator** (`landing_page_generator.py`)
   - WordPress ACF integration
   - ICP-specific content
   - Preview + create modes

3. **Research Engine** (`research_engine.py`)
   - Pain monitoring (Reddit, Twitter, G2)
   - Launch monitoring (framework)
   - Conference monitoring (framework)
   - Hiring signals (framework)
   - Funding rounds (framework)

4. **WordPress Client** (`wordpress_client.py`)
   - REST API + ACF panels
   - Connected to yokehealth.com

5. **Document Converter** (`convert_docs_to_text.py`)
   - Batch .docx/.pptx → .txt
   - For knowledge ingestion

---

## 🧠 INGESTED INTELLIGENCE

### 2026-02-03: ICP Targeting Model
**Source:** `icp targeting model handover (competitor gap - no custom - hypothesis loop .txt`

**Key Principles Extracted:**
- ✅ No custom development (30-day value with standard rollout)
- ✅ Competitor gap focus (where existing tools fail)
- ✅ Failure moment (specific workflow breakdown)
- ✅ Deadline triggers (audit, launch, quarterly, event)
- ✅ Ruthless scoring (0-2 on 5 criteria = max 10)
- ✅ Weekly hypothesis loop (pick → test → validate → pivot)

**Impact:** Complete re-scoring of all 12 ICPs, deprioritized custom-heavy ICPs

---

## 📂 SYSTEM STRUCTURE

```
claude code creator/
├── MASTER_INDEX.md              ← YOU ARE HERE
├── SYSTEM_STATE.json            ← Machine-readable state
├── INGESTION_LOG.md             ← Processing history
│
├── intelligence_queue/          ← DROP NEW FILES HERE
├── intelligence_processed/      ← Already processed
│
├── knowledge/
│   └── client_acquisition/
│       ├── icps/                ← 12 ICP JSON files
│       ├── apollo/              ← Search results
│       ├── landing_pages/       ← Generated pages
│       └── clients/             ← Active prospects
│
├── research_config/             ← Signal configs per ICP
├── research_output/             ← Research results
├── monitors/                    ← Pain/launch/conference monitors
│
├── apollo_client.py
├── apollo_icp_search.py
├── wordpress_client.py
├── landing_page_generator.py
├── research_engine.py
│
└── CREDENTIALS_STORE.json       ← API keys (Apollo, WordPress, etc.)
```

---

## 🔄 CONTINUOUS IMPROVEMENT WORKFLOW

**To add new intelligence:**

1. **Drop file** → `intelligence_queue/`
2. **Next session:** Claude Code automatically:
   - Checks queue
   - Processes new files
   - Updates relevant configs (ICPs, signals, targeting)
   - Logs changes in `INGESTION_LOG.md`
   - Moves file → `intelligence_processed/`

**Supported formats:**
- .txt, .md (best)
- .docx, .pptx (auto-converted)
- .json (structured)

---

## 🎬 STARTUP ROUTINE (Every Session)

1. **Read this file** - Get full context
2. **Check `intelligence_queue/`** - Process new intelligence
3. **Read `SYSTEM_STATE.json`** - Get current priorities
4. **Check `INGESTION_LOG.md`** - See recent updates
5. **Ready to work** - Context loaded, no repetition

---

## 🚀 QUICK COMMANDS

### Search Apollo for ICP:
```bash
python apollo_icp_search.py <icp_name> [limit]
```

### Research ICP signals:
```bash
python research_engine.py <icp_name> [monitors]
```

### Generate landing page:
```bash
python landing_page_generator.py preview <icp_name>
python landing_page_generator.py create <icp_name> draft
```

### List available ICPs:
```bash
python apollo_icp_search.py
python research_engine.py
```

---

## 📋 ACTIVE EXPERIMENTS

**Experiment #2: Medical Societies CPD - UK Specialty Societies**
- **Hypothesis:** UK medical societies (100-500 members) need outcomes-based CPD to satisfy GMC revalidation requirements and accreditation audits
- **Test:** Outreach to 5-10 small specialty societies (CEO/Education Director)
- **Success metric:** 2+ discovery calls in 7 days, validate deal size and buyer urgency
- **Status:** Setup required (research + landing page + outreach)
- **Next:** Research target societies + create landing page + draft outreach

---

## 🎯 STRATEGIC FRAMEWORK

**Core Rule:** No custom development in first 30 days

**ICP Scoring (0-2 each, max 10):**
1. Felt pain intensity (failure moment + consequence)
2. Deadline trigger (audit, launch, event, quarterly)
3. Standard rollout fit (no bespoke build)
4. Buyer reachable + budget owner
5. Evidence validated in 7 days

**Positioning:**
- Pain → Platform → Outcome
- Two-lever: Increase engagement/revenue OR Reduce time/cost
- Lead with failure moment, not features
- Competitor gap focus

**Proof Points:**
- 3 major awards
- Medscape partnership (iCases in-room)
- 10+ programmes across 6+ markets
- 48-hour deployment

---

## 📞 CREDENTIALS

All stored in `CREDENTIALS_STORE.json`:
- ✅ Apollo.io API
- ✅ WordPress (yokehealth.com)
- ✅ DigitalOcean Droplet
- ✅ Todoist API
- ✅ Trello API

---

## 🔮 NEXT PRIORITIES

**Immediate (This week):**
1. Research 5-10 UK medical specialty societies (websites, Education Directors, member counts)
2. Create Medical Societies landing page (outcomes for GMC revalidation angle)
3. Draft outreach email (lead with accreditation audit pain, not features)
4. Update Apollo search for medical societies + CPD keywords
5. Launch 7-day outreach test

**Short-term (This month):**
1. Validate Medical Societies hypothesis (deal size, buyer, urgency)
2. Get 2-3 discovery calls
3. Close first society deal (£10-20k)
4. Build society case study

**Long-term (3-6 months):**
1. Scale to 10+ small societies
2. Use as proof for mid-size bodies (£20-50k deals)
3. Approach Royal Colleges (enterprise £50-150k)
4. Build referral engine within medical education community

---

## 📚 KEY DOCUMENTS

- `ICP_DECISION_HISTORY.md` - **ALL ICP analysis & decisions** ⭐
- `APOLLO_AUTOMATION_README.md` - Apollo usage
- `RESEARCH_AUTOMATION_README.md` - Research usage
- `CONFIRMED_WORKFLOWS.md` - Approved automations
- `CREDENTIALS_README.md` - API setup

---

## 🚨 MAJOR DECISIONS

**Decision #1: Strategic Pivot to Medical Societies CPD (2026-02-04)**
- **From:** KOL Series (event-based, 9/10)
- **To:** Medical Societies CPD (portal-based, 10/10)
- **Rationale:** True SaaS scale (portal vs event logistics), 10x larger market, regulatory pain validated, standard product
- **Full Analysis:** See `ICP_DECISION_HISTORY.md`

---

**Last Action:** Strategic pivot decision + Medical Societies ICP build
**Next Session:** Read this file first → Check intelligence_queue/ → Continue with Medical Societies research

---

*This file is your perpetual context. Update it after major changes.*
