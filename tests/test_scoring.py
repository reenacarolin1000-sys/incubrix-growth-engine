"""
Unit tests for scoring, priority classification, and deduplication.
"""

import pytest
from src.scoring import calculate_lead_score, classify_priorities
from src.deduplication import deduplicate_leads, normalize_url, normalize_stable_id


def test_calculate_lead_score():
    lead = {
        "content_count_30d": 14,
        "longform_count_60d": 8,
        "monetization_signal": "Sponsor reads with Shopify and digital course sales",
        "incubrix_need": "Repurposing 50+ back-catalog episodes into viral vertical shorts and reels",
        "best_channel": "Email",
        "backup_channel": "LinkedIn",
    }
    score = calculate_lead_score(lead)
    assert 70 <= score <= 100


def test_classify_priorities():
    leads = [
        {"stable_creator_id": f"id_{i}", "candidate_status": "Qualified", "content_count_30d": i}
        for i in range(1, 35)
    ]
    classified = classify_priorities(leads, target_priority_a_count=25)
    prio_a = [l for l in classified if l["priority"] == "A"]
    assert len(prio_a) == 25


def test_normalize_url():
    url1 = "https://example.com/channel/?utm_source=twitter&utm_medium=social"
    norm1 = normalize_url(url1)
    assert "utm_source" not in norm1
    assert norm1.startswith("https://example.com/channel")


def test_deduplicate_leads():
    raw = [
        {"stable_creator_id": "yt:100", "profile_url": "https://youtube.com/@tech1", "name": "A"},
        {"stable_creator_id": "yt:100", "profile_url": "https://youtube.com/@tech1", "name": "A duplicate"},
        {"stable_creator_id": "yt:200", "profile_url": "https://youtube.com/@tech2", "name": "B"},
        {"stable_creator_id": "yt:300", "profile_url": "https://youtube.com/@tech2", "name": "B duplicate url"},
    ]
    unique, dups = deduplicate_leads(raw)
    assert len(unique) == 2
    assert dups == 2
