"""
Configuration and constants for the IncuBrix Growth Engine.
Option 1: Multi-Channel Lead Generation and Outreach Engine.
"""

from pathlib import Path
import os

# Base directory for the submission package
BASE_DIR = Path(__file__).resolve().parent.parent

# Data and output directories
DATA_DIR = BASE_DIR / "data"
DATABASE_DIR = DATA_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "incubrix_growth.db"
IMPORTS_DIR = DATA_DIR / "imports"
SEED_CREATORS_DIR = DATA_DIR / "seed_creators"

OUTPUT_DIR = BASE_DIR / "output"
LEADS_CSV_PATH = OUTPUT_DIR / "leads.csv"

OUTREACH_DIR = BASE_DIR / "outreach"
OUTREACH_SEQUENCES_DIR = OUTREACH_DIR / "sequences"
OUTREACH_PRIORITY_A_DIR = OUTREACH_DIR / "priority_a"

REPORTS_DIR = BASE_DIR / "reports"
AUDIT_LOG_PATH = REPORTS_DIR / "engine_audit.log"

# Approved developed English-speaking countries
# At least 80% of leads must come from these countries.
APPROVED_COUNTRIES = {
    "US": "United States",
    "CA": "Canada",
    "GB": "United Kingdom",
    "IE": "Ireland",
    "AU": "Australia",
    "NZ": "New Zealand",
    "SG": "Singapore",
}

# Country distribution constraints
MIN_APPROVED_COUNTRY_SHARE = 0.80  # >= 80%
MIN_DISTINCT_COUNTRIES = 3         # >= 3 countries
MAX_SINGLE_COUNTRY_SHARE = 0.60    # <= 60%

# Target creator segments
APPROVED_SEGMENTS = [
    "Podcaster",
    "Video-First Creator",
    "Expert-Led Creator",
]

# Disallowed segments (immediate rejection)
DISALLOWED_SEGMENTS = [
    "Agency",
    "Management Firm",
    "Generic Brand",
    "Media Company",
    "Publication",
    "Directory",
    "Fan Account",
]

# Qualification activity thresholds
# Creator must have EITHER >= 8 content items in last 30 days OR >= 2 longform items in last 60 days
MIN_CONTENT_ITEMS_30D = 8
MIN_LONGFORM_ITEMS_60D = 2

# Supported outreach channels
SUPPORTED_CHANNELS = [
    "Email",
    "LinkedIn",
    "Instagram",
    "X",
    "YouTube",
    "Podcast Guest Pitch",
]

# Scoring and Priority thresholds
PRIORITY_A_MIN_SCORE = 85
PRIORITY_B_MIN_SCORE = 70
PRIORITY_C_MIN_SCORE = 50

# Target numbers
TARGET_LEADS_MINIMUM = 1000
TARGET_LEADS_EXCEPTIONAL = 5000
MIN_PRIORITY_A_COUNT = 25
EXCEPTIONAL_PRIORITY_A_COUNT = 250

# Candidate & assessment metadata defaults
CANDIDATE_METADATA = {
    "candidate_id": "CAND-2027-GE-01",
    "full_name": "Senior Growth Engineer Candidate",
    "registered_email": "candidate@growth-engineer.com",
    "college_degree": "B.Tech / M.S. Computer Science & Growth Engineering",
    "assessment_start": "2026-10-18 09:00:00",
    "submission_time": "2026-10-24 14:00:00",
}
