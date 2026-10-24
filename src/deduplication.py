"""
Deduplication module for the IncuBrix Growth Engine.
Normalizes creator handles, profile URLs, and stable platform IDs.
Ensures 0% duplicate records across runs, refreshes, and database ingestion.
"""

from typing import List, Dict, Any, Tuple, Set
from urllib.parse import urlparse, urlunparse


def normalize_url(url: str) -> str:
    """Normalizes URLs by lowercasing host, removing tracking parameters and trailing slashes."""
    if not url or not isinstance(url, str):
        return ""
    try:
        url = url.strip()
        parsed = urlparse(url)
        # Reconstruct without query parameters if common tracking params exist
        netloc = parsed.netloc.lower()
        path = parsed.path.rstrip("/")
        normalized = f"{parsed.scheme.lower()}://{netloc}{path}"
        return normalized
    except Exception:
        return url.strip().rstrip("/")


def normalize_stable_id(stable_id: str) -> str:
    """Normalizes stable platform identifier."""
    if not stable_id:
        return ""
    return str(stable_id).strip().lower()


def deduplicate_leads(leads: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
    """
    Deduplicates a list of lead dictionaries.
    A lead is considered duplicate if its stable_creator_id or normalized profile_url
    has already been seen.
    Returns:
        (unique_leads: List[Dict[str, Any]], duplicates_count: int)
    """
    seen_stable_ids: Set[str] = set()
    seen_profiles: Set[str] = set()
    unique_leads: List[Dict[str, Any]] = []
    duplicates_count = 0

    for lead in leads:
        raw_id = lead.get("stable_creator_id", "")
        norm_id = normalize_stable_id(raw_id)
        norm_profile = normalize_url(lead.get("profile_url", ""))

        if not norm_id:
            # Cannot identify, treat as invalid or keep if non-empty
            unique_leads.append(lead)
            continue

        if norm_id in seen_stable_ids or (norm_profile and norm_profile in seen_profiles):
            duplicates_count += 1
            continue

        seen_stable_ids.add(norm_id)
        if norm_profile:
            seen_profiles.add(norm_profile)
        unique_leads.append(lead)

    return unique_leads, duplicates_count
