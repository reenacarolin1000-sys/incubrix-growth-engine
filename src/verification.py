"""
Verification module for the IncuBrix Growth Engine.
Validates creator legitimacy, activity cadence, monetization signals, workflow needs,
country eligibility, English-language compliance, and reachability.
"""

import re
from typing import Dict, Any, Tuple
from urllib.parse import urlparse
from src.config import (
    APPROVED_COUNTRIES,
    APPROVED_SEGMENTS,
    DISALLOWED_SEGMENTS,
    MIN_CONTENT_ITEMS_30D,
    MIN_LONGFORM_ITEMS_60D,
)

# Comprehensive list of media networks, generic brands, agencies, and publications
KNOWN_MEDIA_AND_CORPORATE_BRANDS = [
    "bloomberg", "bbc", "cnn", "new york times", "nytimes", "the new york times",
    "wall street journal", "wsj", "the wall street journal", "espn", "npr",
    "iheartpodcasts", "iheart", "iheartradio", "wondery", "abc news", "fox news",
    "cbs", "nbc", "the economist", "economist", "financial times", "reuters",
    "associated press", "audible", "ted", "ted tech", "ted talks", "vox", "slate",
    "the verge", "condé nast", "conde nast", "hearst", "parcast", "spotify studios",
    "apple", "google", "microsoft", "amazon", "the guardian", "forbes", "fortune",
    "inc. magazine", "fast company", "business insider", "huffpost", "daily wire",
    "barstool", "the ringer", "gimlet", "pushkin", "crooked media", "lemonada",
    "cumulus", "siriusxm", "stitcher", "new york magazine", "cool zone media",
    "management firm", "talent agency", "marketing agency", "pr agency",
    "y combinator", "marketplace", "stanford", "harvard", "mit sloan", "goldman sachs",
    "mckinsey", "bain & company", "bcg", "deloitte", "accenture", "kpmg", "fidelity",
    "rnz", "radio new zealand", "cbc", "radio-canada", "pbs", "rte", "rté",
    "ramsey network", "podcast network", "media network", "news network",
    "seeking alpha", "9to5mac", "irish independent", "business post", "macrumors", "techmeme"
]

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')



def is_valid_url(url: str) -> bool:
    """Validates that a string is a well-formed HTTP/HTTPS URL."""
    if not url or not isinstance(url, str):
        return False
    try:
        parsed = urlparse(url.strip())
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


def verify_creator(creator_data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Evaluates a creator record against all IncuBrix qualification criteria.
    Returns:
        (is_qualified: bool, rejection_reason: str)
    """
    # 1. Real and Relevant: Creator Name & Profile
    name = str(creator_data.get("creator_name", "")).strip()
    if not name or len(name) < 2:
        return False, "Missing or invalid creator name"

    # Check for corporate networks, media brands, or publications
    name_lower = name.lower()
    if any(brand in name_lower for brand in KNOWN_MEDIA_AND_CORPORATE_BRANDS) or name_lower.endswith(" network"):
        return False, f"Disallowed entity: '{name}' is a corporate media publication or broadcasting network"

    stable_id = str(creator_data.get("stable_creator_id", "")).strip()
    if not stable_id:
        return False, "Missing stable platform identifier (stable_creator_id)"

    profile_url = str(creator_data.get("profile_url", "")).strip()
    if not is_valid_url(profile_url):
        return False, f"Invalid or missing profile URL: {profile_url}"

    # 2. Segment Eligibility
    segment = str(creator_data.get("creator_segment", "")).strip()
    if not segment:
        return False, "Missing creator segment"

    if any(disallowed.lower() in segment.lower() for disallowed in DISALLOWED_SEGMENTS):
        return False, f"Disallowed segment '{segment}' (agencies, generic brands, media publications excluded)"

    if not any(approved.lower() in segment.lower() for approved in APPROVED_SEGMENTS):
        return False, f"Unapproved segment '{segment}' (must be Podcaster, Video-First Creator, or Expert-Led Creator)"

    # 3. Country Eligibility & English Language
    country = str(creator_data.get("country_iso2", "")).strip().upper()
    if not country:
        return False, "Missing country ISO-2 code"

    language = str(creator_data.get("primary_language", "en")).strip().lower()
    if language != "en":
        return False, f"Non-English content language '{language}' (English required)"

    # Script and foreign language detection on creator name
    has_non_latin = any(
        '\u4e00' <= char <= '\u9fff' or  # CJK
        '\u3040' <= char <= '\u30ff' or  # Japanese
        '\uac00' <= char <= '\ud7af' or  # Korean
        '\u0400' <= char <= '\u04ff' or  # Cyrillic
        '\u0600' <= char <= '\u06ff'     # Arabic
        for char in name
    )
    if has_non_latin:
        return False, f"Non-English content: creator name '{name}' contains non-Latin characters"

    foreign_keywords = ["abogados", "noticias", "español", "espanol", "podcast en español", "francais", "deutsch", "italiano"]
    if any(fk in name.lower() for fk in foreign_keywords):
        return False, f"Non-English content: creator name '{name}' indicates non-English programming"

    # 4. Activity Threshold
    try:
        content_count_30d = int(creator_data.get("content_count_30d", 0))
    except (ValueError, TypeError):
        content_count_30d = 0

    try:
        longform_count_60d = int(creator_data.get("longform_count_60d", 0))
    except (ValueError, TypeError):
        longform_count_60d = 0

    has_active_volume = content_count_30d >= MIN_CONTENT_ITEMS_30D
    has_active_longform = longform_count_60d >= MIN_LONGFORM_ITEMS_60D

    if not (has_active_volume or has_active_longform):
        return False, (
            f"Fails activity threshold: {content_count_30d} items in 30d (req >= {MIN_CONTENT_ITEMS_30D}) "
            f"and {longform_count_60d} longform in 60d (req >= {MIN_LONGFORM_ITEMS_60D})"
        )

    recent_content_url = str(creator_data.get("recent_content_url", "")).strip()
    if not is_valid_url(recent_content_url):
        return False, "Missing or invalid recent content evidence URL"

    # 5. Monetization Evidence
    monetization_signal = str(creator_data.get("monetization_signal", "")).strip()
    if not monetization_signal or len(monetization_signal) < 5:
        return False, "Missing clear monetization signal description"

    monetization_evidence_url = str(creator_data.get("monetization_evidence_url", "")).strip()
    if not is_valid_url(monetization_evidence_url):
        return False, "Missing or invalid monetization evidence URL"

    # 6. IncuBrix Need Evidence
    incubrix_need = str(creator_data.get("incubrix_need", "")).strip()
    if not incubrix_need or len(incubrix_need) < 5:
        return False, "Missing clear IncuBrix workflow need description"

    need_evidence_url = str(creator_data.get("need_evidence_url", "")).strip()
    if not is_valid_url(need_evidence_url):
        return False, "Missing or invalid IncuBrix need evidence URL"

    # 7. Reachability: Best & Backup Channels
    best_channel = str(creator_data.get("best_channel", "")).strip()
    if not best_channel:
        return False, "Missing best contact channel"

    channel_handle_or_url = str(creator_data.get("channel_handle_or_url", "")).strip()
    if not channel_handle_or_url:
        return False, "Missing business contact handle or destination URL"

    if best_channel == "Email" and not EMAIL_REGEX.match(channel_handle_or_url):
        return False, f"Invalid email address format for Email channel: '{channel_handle_or_url}'"

    channel_evidence_url = str(creator_data.get("channel_evidence_url", "")).strip()
    if not is_valid_url(channel_evidence_url):
        return False, "Missing or invalid business channel evidence URL"

    # 8. Personalization Hook & First Message
    hook = str(creator_data.get("personalization_hook", "")).strip()
    if not hook or len(hook) < 5:
        return False, "Missing specific content personalization hook"

    first_message = str(creator_data.get("first_message", "")).strip()
    if not first_message or len(first_message) < 20:
        return False, "Missing complete first message draft"

    # If all checks pass:
    return True, ""
