# IncuBrix 2027 Growth Engineer Assessment - Option 1
## Multi-Channel Lead Generation and Outreach Engine: Requirements Checklist & Specification

---

### 1. Executive Summary & Core Mission
- **Role**: Growth Engineer (2027 Graduate Hiring)
- **Track**: Option 1 - Multi-Channel Lead Generation and Outreach Engine
- **Goal**: Build a launch-ready, automated system that discovers creators who need IncuBrix, verifies their real public evidence, selects the optimal outreach channel, drafts personalized outreach sequences across at least three distinct channels, exports a CRM-ready dataset, and supports periodic refreshing with zero duplicate generation.
- **Scale Target**:
  - Minimum requirement: **1,000 unique, qualified creators** (with at least 25 Priority A leads).
  - Exceptional target: **5,000 unique, qualified creators** (with at least 250 Priority A leads).
- **Core Product Context**:
  - **IncuBrix** is an AI content engine & workflow platform designed for content creators, podcasters, and educators.
  - It solves acute workflow bottlenecks: video repurposing (transforming long-form video/podcast into vertical clips/shorts/reels), AI-driven transcription & stylized captions, automated show-notes & newsletters, multi-platform publishing consistency, and content backlog clearance.

---

### 2. Candidate Persona & Target Criteria Checklist

| Requirement | Specification | Enforcement Mechanism |
| :--- | :--- | :--- |
| **Creator Segments Only** | Podcasters / Video Podcasters, YouTubers / Video-First Creators, Expert-Led Creators (coaches, consultants, educators). Exclude agencies, management firms, media companies, generic brands, directories, and fan accounts. | Strict regex/tag filter + keyword heuristic rejection rules in `verification.py`. |
| **Approved Geographic Focus** | At least 80% from developed English-speaking markets: United States (`US`), Canada (`CA`), United Kingdom (`GB`), Ireland (`IE`), Australia (`AU`), New Zealand (`NZ`), or Singapore (`SG`). | Validated against country ISO-2 codes in `src/verification.py`. Distribution checks ensure >= 3 countries and no single country exceeds 60%. |
| **Language** | Recent content predominantly in English. | Explicit language check field (`primary_language == 'en'`). |
| **Activity Threshold** | Either **8 content items in the last 30 days** OR **2 long-form items in the last 60 days**. | Checked against timestamp of recent items: `content_count_30d >= 8` OR `longform_count_60d >= 2`. |
| **Monetization Evidence** | Public evidence of sponsorship, digital products, coaching, courses, memberships, subscriptions, affiliate links, or paid newsletters. | `monetization_signal` + traceable `monetization_evidence_url`. No assumptions without public proof. |
| **IncuBrix Need Evidence** | Traceable evidence of content creation backlog, lack of vertical shorts/reels, inconsistent publishing, manual editing, or caption bottlenecks. | `incubrix_need` + traceable `need_evidence_url`. |
| **Reachable Business Channel** | Must be real, public, used for business inquiries, and active within the last 60 days. No guessed or brute-forced emails/handles. | Best channel + backup channel selection with `channel_evidence_url`. |
| **Compliance & Opt-Out** | Outreach messages must include sender identity, reference specific recent creator content, provide clear opt-out language, and adhere to platform terms (no bulk unauthorized automated DMs). | Template generator enforces personalization hook, opt-out clause, and sender signature. |
| **Data Integrity & Recency** | Verified within the last 30 days (`checked_date`). Every lead has a stable platform ID (`stable_creator_id`) and unique profile URL. | Deduplication on `stable_creator_id` and normalized profile/channel URLs. 0 duplicates permitted. |

---

### 3. Submission Workbook Schema (`02_LEADS`)

Every row in the full `leads.csv` and workbook `02_LEADS` conforms to the 30-column specification:

1. `lead_id`: Unique identifier (e.g., `LEAD-0001` to `LEAD-1000+`).
2. `creator_name`: Full creator or host name.
3. `creator_segment`: Segment (`Podcaster`, `Video-First Creator`, `Expert-Led Creator`).
4. `country_iso2`: ISO-2 country code (`US`, `CA`, `GB`, `AU`, `NZ`, `SG`, `IE`).
5. `primary_language`: Primary content language (`en`).
6. `primary_platform`: Primary publishing platform (`YouTube`, `Apple Podcasts`, `Spotify`, `Substack`, etc.).
7. `profile_url`: Canonical public profile or channel URL.
8. `stable_creator_id`: Stable unique platform ID (e.g., YouTube Channel ID, Apple Podcast ID, RSS GUID).
9. `followers_or_subscribers`: Subscriber / follower / listener count or bracket.
10. `last_content_date`: ISO format date (`YYYY-MM-DD`) of the latest published item.
11. `recent_content_url`: Working URL to a specific recent episode or video.
12. `content_count_30d`: Count of published items in the last 30 days.
13. `longform_count_60d`: Count of long-form episodes (>15 min) in the last 60 days.
14. `monetization_signal`: Description of the commercial model (e.g., "Patreon membership + sponsor read for AG1").
15. `monetization_evidence_url`: Working URL proving commercialization.
16. `incubrix_need`: Specific workflow bottleneck (e.g., "Produces 60-min podcast with no shorts/reels repurposing").
17. `need_evidence_url`: Working URL displaying the bottleneck or content gap.
18. `best_channel`: Recommended primary business contact channel (`Email`, `LinkedIn`, `Instagram`, `X`).
19. `channel_handle_or_url`: Exact public business contact handle, profile, or email.
20. `channel_evidence_url`: Working URL where the contact information is publicly displayed.
21. `backup_channel`: Secondary verified outreach channel.
22. `personalization_hook`: Specific reference to creator's recent episode topic, quote, or guest.
23. `first_message`: Full personalized outreach message drafted for `best_channel`.
24. `checked_date`: Date verification was conducted (`YYYY-MM-DD`, within 30 days).
25. `priority`: Qualification tier (`A`, `B`, or `C`). Top 25 leads must be Priority A.
26. `lead_score`: Composite numerical score (0-100).
27. `candidate_status`: `Qualified` or `Rejected`.
28. `rejection_reason`: Mandatory if `Rejected`, empty if `Qualified`.
29. `duplicate_check`: Workbook formula: `=IF(A5="","",IF(COUNTIF($H$5:$H$1004,H5)>1,"DUPLICATE","UNIQUE"))`.
30. `completeness_check`: Workbook formula ensuring all 20 required fields are non-empty for `Qualified` leads.

---

### 4. Excel Workbook Tabs & Formulas

- **`00_START`**:
  - Yellow input cells for candidate details, URLs, AI & manual tool disclosure, and declaration acceptance (`B21 = "Yes"`).
  - Calculated status: `=IF(AND(COUNTIF(04_SELF_CHECK!F6:F12,"MET")=7,B21="Yes",COUNTIF(F5:F10,"Yes")=6),"YES","NOT YET - check tabs 00 and 04")`.
- **`01_INSIGHT`**:
  - Section A: 5 detailed product observations backed by evidence and tied to growth impact.
  - Section B: 3 biggest growth opportunities with evidence, expected impact, metric, and 30-day targets.
- **`02_LEADS`**:
  - First 1,000 rows of official `leads.csv` populated, preserving formulas in columns `AC` (`duplicate_check`) and `AD` (`completeness_check`).
- **`03_ENGINE_LAUNCH`**:
  - Section A: Engine proof matrix (9 operational requirements verified).
  - Section B: Run summary table (Normal run, Repeat run, Refresh run, Failure & recovery run).
  - Section C: 30-day launch kit summary.
- **`04_SELF_CHECK`**:
  - Minimum Results table (Rows 6-12) evaluating:
    - Unique qualified creators >= 1,000
    - Country constraints met (>=80% approved, 3+ countries, <=60% single country)
    - 0 duplicates
    - Outreach channels >= 3
    - Priority A leads >= 25 with full sequences (1st message + 2 follow-ups)
    - Seed test on owned accounts passed on 3 channels
    - Engine reruns cleanly from README
  - Exceptional Results (5,000 leads, 250 Priority A, automated 5k refresh, channel-mix analysis).
  - Self-score calculation (`SUM(C24:C28)` out of 100).

---

### 5. Architectural Components of the Engine

1. **`src/config.py`**: Configuration constants, approved country sets, scoring weights, API settings, and file paths.
2. **`src/database.py`**: SQLite database persistence layer (`data/database/incubrix_growth.db`), tables for `leads`, `runs`, `audit_logs`, and `seed_tests`.
3. **`src/discovery.py`**: Automated search and ingestion from public feeds, iTunes Podcast Search API, RSS metadata, JSON/CSV imports, and web scraping.
4. **`src/verification.py`**: Rules engine validating profile legitimacy, stable ID, activity frequency, commercial presence, IncuBrix need, and country/language constraints.
5. **`src/scoring.py`**: Mathematical scoring model evaluating audience scale, publishing frequency, monetization maturity, and repurposing need to assign scores (0-100) and Priority A/B/C.
6. **`src/deduplication.py`**: Normalization and deduplication pipeline preventing duplicate creators across runs and refreshes.
7. **`src/channel_selection.py`**: Logic determining primary and fallback communication channels based on creator platform, verified handles, and platform responsiveness.
8. **`src/outreach.py`**: Multi-channel copywriting engine generating customized first messages and two sequential follow-up messages for all Priority A leads across Email, LinkedIn, and Instagram/X.
9. **`src/export.py`**: High-fidelity exporter creating `output/leads.csv` (UTF-8) and populating the completed Excel submission workbook while preserving styles, formulas, and data validations.
10. **`app.py`**: Interactive Streamlit GUI allowing users to run discovery, inspect lead tables, view audit logs, trigger refreshes, preview outreach sequences, and export files.
11. **`tests/`**: Pytest automated test suite covering all modules, regression testing, edge cases, and seed test delivery verification.

---

### 6. Deliverable Inventory Checklist

- [x] Separate clean directory: `C:\Users\carolin\OneDrive\Desktop\IncuBrix_Growth_Engine_Submission`
- [ ] Source code modules in `src/`
- [ ] Comprehensive unit & integration tests in `tests/`
- [ ] Interactive Streamlit application (`app.py`)
- [ ] Official `output/leads.csv` containing >= 1,000 qualified creators
- [ ] Outreach sequences folder `outreach/` with multi-channel sequences & 2 follow-ups for Priority A leads
- [ ] Seed test execution report and instructions (`reports/seed_test_report.md`)
- [ ] Engine run summary report (`reports/engine_run_summary.md`)
- [ ] Audit report (`reports/audit_report.md`)
- [ ] Requirements checklist (`REQUIREMENTS.md`)
- [ ] Product & Market Insights (`PRODUCT_MARKET_INSIGHTS.md`)
- [ ] 30-Day Launch Plan (`LAUNCH_PLAN.md`)
- [ ] AI & Manual Work Disclosure (`AI_AND_MANUAL_WORK_DISCLOSURE.md`)
- [ ] Completed Submission Workbook copy (`IncuBrix_2027_Growth_Engineer_Option_1_Submission_Workbook_Completed.xlsx`)
- [ ] 5-minute Product Walkthrough Script (`scripts/product_walkthrough_script.md`)
- [ ] 8-minute Technical Demo Script (`scripts/technical_demo_script.md`)
- [ ] Dependencies (`requirements.txt`), `.env.example`, `.gitignore`
- [ ] Comprehensive `README.md` with one clear run command and PowerShell instructions
