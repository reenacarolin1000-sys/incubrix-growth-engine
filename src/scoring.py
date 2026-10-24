"""
Scoring and Priority Classification module for the IncuBrix Growth Engine.
Evaluates creator activity cadence, commercial maturity, IncuBrix need intensity,
and reachability to compute a composite score (0-100) and Priority A/B/C tier.
"""

from typing import Dict, Any, List
from src.config import PRIORITY_A_MIN_SCORE, PRIORITY_B_MIN_SCORE


def calculate_lead_score(creator_data: Dict[str, Any]) -> int:
    """
    Computes a composite numerical score from 0 to 100 based on four objective dimensions:
    1. Activity Cadence (0-25)
    2. Commercial Maturity (0-25)
    3. IncuBrix Need Intensity (0-30)
    4. Reachability & Channel Strength (0-20)
    """
    # 1. Activity Cadence (0 - 25 pts)
    activity_score = 0
    try:
        count_30d = int(creator_data.get("content_count_30d", 0))
    except (ValueError, TypeError):
        count_30d = 0

    try:
        longform_60d = int(creator_data.get("longform_count_60d", 0))
    except (ValueError, TypeError):
        longform_60d = 0

    if count_30d >= 20:
        activity_score += 15
    elif count_30d >= 12:
        activity_score += 12
    elif count_30d >= 8:
        activity_score += 9
    else:
        activity_score += min(count_30d, 8)

    if longform_60d >= 8:
        activity_score += 10
    elif longform_60d >= 4:
        activity_score += 8
    elif longform_60d >= 2:
        activity_score += 6
    else:
        activity_score += min(longform_60d * 2, 5)

    activity_score = min(25, activity_score)

    # 2. Commercial Maturity (0 - 25 pts)
    monetization = str(creator_data.get("monetization_signal", "")).lower()
    comm_score = 10  # Baseline for having verified commercial signal
    if any(k in monetization for k in ["sponsor", "advertiser", "brand deal", "partner"]):
        comm_score += 8
    if any(k in monetization for k in ["course", "mastermind", "coaching", "consulting"]):
        comm_score += 7
    if any(k in monetization for k in ["patreon", "membership", "subscription", "community"]):
        comm_score += 5
    if any(k in monetization for k in ["affiliate", "merch", "book"]):
        comm_score += 3
    comm_score = min(25, comm_score)

    # 3. IncuBrix Need Intensity (0 - 30 pts)
    need_desc = str(creator_data.get("incubrix_need", "")).lower()
    need_score = 12  # Baseline for verified need
    if any(k in need_desc for k in ["repurpose", "repurposing", "clip", "shorts", "reels", "tiktok"]):
        need_score += 8
    if any(k in need_desc for k in ["backlog", "archive", "library", "unrepurposed", "100+", "50+"]):
        need_score += 5
    if any(k in need_desc for k in ["caption", "subtitle", "transcribe", "transcript"]):
        need_score += 3
    if any(k in need_desc for k in ["editor", "editing bottleneck", "turnaround", "team", "consistency"]):
        need_score += 4
    need_score = min(30, need_score)

    # 4. Reachability & Channel Strength (0 - 20 pts)
    channel = str(creator_data.get("best_channel", "")).lower()
    reach_score = 10
    if "email" in channel:
        reach_score += 8
    elif "linkedin" in channel:
        reach_score += 7
    elif "instagram" in channel or "x" in channel:
        reach_score += 6
    else:
        reach_score += 4

    backup = str(creator_data.get("backup_channel", "")).strip()
    if backup and backup != channel:
        reach_score += 2

    reach_score = min(20, reach_score)

    total_score = activity_score + comm_score + need_score + reach_score
    return max(0, min(100, total_score))


def classify_priorities(leads: List[Dict[str, Any]], target_priority_a_count: int = 25) -> List[Dict[str, Any]]:
    """
    Ranks leads and assigns Priority A, B, or C.
    Guarantees that at least target_priority_a_count top qualified leads are marked as Priority 'A'.
    """
    for lead in leads:
        lead["lead_score"] = calculate_lead_score(lead)

    qualified_leads = [l for l in leads if l.get("candidate_status") == "Qualified"]
    rejected_leads = [l for l in leads if l.get("candidate_status") == "Rejected"]

    # Sort qualified leads by lead_score descending
    qualified_leads.sort(key=lambda x: (x.get("lead_score", 0), int(x.get("content_count_30d", 0))), reverse=True)

    for i, lead in enumerate(qualified_leads):
        if i < target_priority_a_count:
            lead["priority"] = "A"
        elif lead.get("lead_score", 0) >= PRIORITY_B_MIN_SCORE:
            lead["priority"] = "B"
        else:
            lead["priority"] = "C"

    for lead in rejected_leads:
        lead["priority"] = "C"

    return qualified_leads + rejected_leads
