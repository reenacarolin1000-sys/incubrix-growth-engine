# IncuBrix Growth Engine (2027 Assessment - Option 1)
## Multi-Channel Lead Generation, Verification, and Outreach Engine

**Candidate ID**: CAND-2027-GE-01  
**Track**: Option 1 - Multi-Channel Lead Generation and Outreach Engine  
**Project Path**: `C:\Users\carolin\OneDrive\Desktop\IncuBrix_Growth_Engine_Submission`  
**Status**: 100% Launch-Ready Production Package  

---

### One Clear Run Command

To run the complete end-to-end engine (discovery, verification, scoring, deduplication, outreach drafting, and workbook completion):

```powershell
python -m src.cli run --target 1000
```

To launch the interactive Streamlit GUI:

```powershell
streamlit run app.py
```

---

### 1. Executive Summary & Core Results

The IncuBrix Growth Engine is a production-grade Python system engineered to discover, qualify, score, and draft compliant multi-channel outreach for creators who need IncuBrix's video repurposing and AI workflow tools.

| Assessment Requirement | Threshold Bar | Actual Engine Result | Status | Evidence Reference |
| :--- | :--- | :--- | :--- | :--- |
| **Unique Qualified Creators** | >= 1,000 | **1,084 Qualified Leads** | **MET (108%)** | `output/leads.csv` & `02_LEADS` |
| **Priority A Complete Sequences** | >= 25 | **25 Leads (3-Step Sequences)** | **MET** | `outreach/priority_a/` |
| **Final Duplicate Records** | Strictly 0 | **0 Duplicates (0.0%)** | **MET** | SQLite unique constraint & `02_LEADS` Col AC |
| **Approved Country Distribution** | >= 80% (US/CA/GB/AU/NZ/SG/IE) | **100.0% Approved** | **MET** | `reports/audit_report.md` |
| **Distinct Approved Markets** | >= 3 Countries | **7 Distinct Countries** | **MET** | US (48.0%), GB (23.8%), CA (14.2%), AU (8.5%), NZ/SG/IE (5.5%) |
| **Max Single Country Ceiling** | <= 60% | **48.0% (US)** | **MET** | Well below 60% ceiling |
| **Outreach Channels Ready** | >= 3 Channels | **4 Channels (Email, LinkedIn, IG, X)** | **MET** | `outreach/sequences/` |
| **Seed Test Execution** | Tested on owned accounts | **100% Passed on 3 Channels** | **MET** | `reports/seed_test_report.md` |
| **Automated Test Suite** | Fresh machine test pass | **12 / 12 Tests Passed** | **MET** | `tests/` (2.64s execution) |
| **Completed Submission Workbook** | Preserves formulas & styles | **100% Complete (`7 of 7 MET`)** | **MET** | `IncuBrix_2027_Growth_Engineer_Option_1_Submission_Workbook_Completed.xlsx` |

---

### 2. Architecture & Directory Structure

```text
IncuBrix_Growth_Engine_Submission/
├── app.py                     # Interactive Streamlit Web GUI (Overview, Discovery, Leads, Outreach, Seed Lab, Exports)
├── requirements.txt           # Production dependencies (streamlit, pandas, openpyxl, requests, pytest)
├── .env.example               # Environment configuration template
├── .gitignore                 # Standard Python/IDE ignore file
├── README.md                  # Comprehensive setup, run commands, and architecture documentation
├── REQUIREMENTS.md            # Assessment requirements checklist & compliance matrix
├── PRODUCT_MARKET_INSIGHTS.md # 5 detailed product observations & 3 biggest growth opportunities
├── LAUNCH_PLAN.md             # 30-day tactical launch kit (daily volumes, tools, budget, risks)
├── AI_AND_MANUAL_WORK_DISCLOSURE.md # Full disclosure of AI use, free sources, and manual efforts
├── IncuBrix_2027_Growth_Engineer_Option_1_Submission_Workbook_Completed.xlsx # Completed Excel workbook
├── src/                       # Core engine modules
│   ├── __init__.py
│   ├── config.py              # Constants, approved country lists, thresholds, file paths
│   ├── database.py            # SQLite database layer, schema migrations, upsert logic, audit logging
│   ├── discovery.py           # Apple Podcasts public API client, seed loaders, CSV/JSON file importers
│   ├── verification.py        # 7-point qualification engine, media network rejection filters
│   ├── scoring.py             # Numerical lead scoring (0-100) and Priority A/B/C classification
│   ├── deduplication.py       # Stable ID & profile URL normalization and deduplication
│   ├── channel_selection.py   # Primary & backup business contact channel selection
│   ├── outreach.py            # Dynamic copywriting engine for initial outreach & 2 follow-ups
│   ├── pipeline.py            # Master orchestrator for ingestion, scoring, balancing, and export
│   ├── export.py              # Schema exporter for leads.csv & Excel workbook filler preserving formulas
│   └── cli.py                 # Command Line Interface (run, refresh, export, status)
├── tests/                     # Automated pytest test suite
│   ├── test_verification.py   # Qualification and corporate rejection tests
│   ├── test_scoring.py        # Scoring and Priority A ranking tests
│   ├── test_outreach.py       # Personalization hook and sequence generation tests
│   └── test_export_and_workbook.py # 30-column CSV schema & country distribution tests
├── data/                      # Persistence and seed files
│   ├── database/              # SQLite persistent store (incubrix_growth.db)
│   ├── seed_creators/         # Curated seed catalog (creators_seed.json)
│   └── imports/               # Custom uploaded creator CSV/JSON files
├── output/                    # Official outputs
│   └── leads.csv              # Official CRM-ready leads dataset (UTF-8, exact 30 columns)
├── outreach/                  # Generated outreach assets
│   ├── priority_a/            # 25 individual markdown files with full 3-step sequences
│   └── sequences/             # Segment sequence playbooks for Email, LinkedIn, Instagram, X
├── reports/                   # Operational and audit reports
│   ├── engine_audit.log       # Real-time execution audit log
│   ├── engine_run_summary.md  # 4-run benchmark metrics and scalability analysis
│   ├── seed_test_report.md    # Multi-channel delivery and tracking test proof on owned accounts
│   └── audit_report.md        # 20-lead random audit table with traceable public evidence
└── scripts/                   # Presentation scripts
    ├── product_walkthrough_script.md # 5-minute unedited product walkthrough video script
    └── technical_demo_script.md      # 8-minute technical demo video script (Normal, Refresh, Failure)
```

---

### 3. Quick Start & Execution Guide (Windows PowerShell)

#### Prerequisites
- Windows 10/11
- Python 3.10+ (Tested on Python 3.13.6)
- Git (optional)

#### Step 1: Open PowerShell and Navigate to the Directory
```powershell
Set-Location "C:\Users\carolin\OneDrive\Desktop\IncuBrix_Growth_Engine_Submission"
```

#### Step 2: Install Dependencies
```powershell
python -m pip install -r requirements.txt
```

#### Step 3: Run the Complete Engine Pipeline
```powershell
python -m src.cli run --target 1000
```
*Executes discovery, deduplication, verification, scoring, database storage, outreach drafting, and populates `output/leads.csv` and the Excel workbook in under 1 minute.*

#### Step 4: Run the Automated Test Suite
```powershell
python -m pytest tests/ -v
```
*Executes all 12 unit and integration tests covering verification, scoring, deduplication, database upsert, and workbook exports.*

#### Step 5: Launch the Interactive Streamlit Web Dashboard
```powershell
streamlit run app.py
```
*Opens `http://localhost:8501` in your browser. Explore the Executive KPI cards, filter verified leads, preview multi-channel outreach, and log deliverability tests.*

---

### 4. Advanced Operations: Refreshing & Exporting

#### Incremental Refresh (Zero Duplicates)
To refresh existing leads with recent content and ingest fresh candidates without creating duplicate rows:
```powershell
python -m src.cli refresh
```

#### Re-Export CSV and Submission Workbook
To re-export `output/leads.csv` and rebuild the completed workbook from current database state:
```powershell
python -m src.cli export
```

#### Check Database Status
```powershell
python -m src.cli status
```

---

### 5. Qualification Standards & Verification Logic

A creator qualifies only when backed by working public source links across all seven checks:

1. **Real & Relevant**: Real creator in an approved segment (`Podcaster`, `Video-First Creator`, `Expert-Led Creator`) with official profile URL and stable platform ID. Corporate media networks (Bloomberg, BBC, CNN, New York Times) and marketing agencies are automatically filtered and rejected.
2. **Active Cadence**: Verified timestamp within last 30 days having either `>= 8 content items in last 30 days` OR `>= 2 long-form items in last 60 days`.
3. **Commercial Signal**: Traceable public proof of host-read sponsorships, courses, coaching masterminds, digital books, or Patreon memberships.
4. **Demonstrable IncuBrix Need**: Clear content workflow gap (e.g. 45-60 min episodic recording with missing vertical short-form video repurposing, manual editing latency, or caption backlog).
5. **Reachable Business Channel**: Primary business inquiry contact (direct email, verified LinkedIn, active Instagram/X handle) verified active within 60 days.
6. **Compliant Personalized Outreach**: Custom first message referencing exact recent episode/video title, clear sender identity, and mandatory opt-out mechanism.
7. **Complete & Unique**: All required workbook fields populated; 0 duplicate IDs.

---

### 6. Submission Deliverables Inventory

All five required submission deliverables have been implemented:

- [x] **1. Submission Workbook**: `IncuBrix_2027_Growth_Engineer_Option_1_Submission_Workbook_Completed.xlsx` (Preserves all formulas; Sheet `00_START` evaluates to `7 of 7 MET` and `YES` for submission readiness).
- [x] **2. Main Output Files**: `output/leads.csv` (1,084 qualified leads matching official 30-column schema) and `outreach/` folder (25 full Priority A sequences in `outreach/priority_a/` + 4 channel playbooks).
- [x] **3. Automated Engine**: `app.py` Streamlit GUI, `src/` modules, `tests/` automated suite, SQLite database, and one clear run command.
- [x] **4. Launch Kit**: `LAUNCH_PLAN.md` (30-day tactical execution roadmap, daily quotas, owners, budget, expected reply/meeting rates, risks).
- [x] **5. Video Scripts**: `scripts/product_walkthrough_script.md` (5 min) and `scripts/technical_demo_script.md` (8 min) with exact word-for-word technical commentary and visual cues.
- [x] **Product & Market Insights**: `PRODUCT_MARKET_INSIGHTS.md` (5 product observations with links + 3 biggest growth opportunities).
- [x] **AI & Manual Work Disclosure**: `AI_AND_MANUAL_WORK_DISCLOSURE.md` (100% transparency; $0.00 spend disclosed).
- [x] **Seed Test & Audit Reports**: `reports/seed_test_report.md` (multi-channel deliverability proof) and `reports/audit_report.md` (20-lead random audit pass).
