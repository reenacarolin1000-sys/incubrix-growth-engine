"""
Unit tests for outreach generation, database persistence, and seed testing.
"""

import pytest
from pathlib import Path
from src.outreach import generate_first_message, generate_priority_a_sequence
from src.database import (
    init_db,
    upsert_lead,
    get_lead_count,
    record_seed_test,
    get_seed_tests_df,
    clear_leads_table,
)


def test_outreach_contains_hook_and_opt_out():
    lead = {
        "creator_name": "Marcus Vance",
        "best_channel": "Email",
        "backup_channel": "LinkedIn",
        "personalization_hook": "your recent breakdown on AI coding agents",
        "incubrix_need": "high video editing latency and caption backlog",
        "stable_creator_id": "test:001",
    }
    msg = generate_first_message(lead)
    assert "your recent breakdown on AI coding agents" in msg
    assert "unsubscribe" in msg.lower() or "opt-out" in msg.lower()

    seq = generate_priority_a_sequence(lead)
    assert "step_1_initial" in seq
    assert "step_2_followup_1" in seq
    assert "step_3_followup_2" in seq
    assert "preview" in seq["step_2_followup_1"].lower()


def test_database_and_seed_tests(tmp_path):
    test_db = tmp_path / "test_growth.db"
    init_db(test_db)

    # Insert lead
    lead = {
        "lead_id": "LEAD-0001",
        "creator_name": "Test Host",
        "creator_segment": "Podcaster",
        "country_iso2": "US",
        "primary_language": "en",
        "primary_platform": "Apple Podcasts",
        "profile_url": "https://example.com/test",
        "stable_creator_id": "itunes:999000",
        "last_content_date": "2026-10-20",
        "recent_content_url": "https://example.com/ep",
        "content_count_30d": 10,
        "longform_count_60d": 4,
        "monetization_signal": "Sponsor reads",
        "monetization_evidence_url": "https://example.com/sponsors",
        "incubrix_need": "Shorts clipping",
        "need_evidence_url": "https://example.com/need",
        "best_channel": "Email",
        "channel_handle_or_url": "host@test.com",
        "channel_evidence_url": "https://example.com/contact",
        "backup_channel": "LinkedIn",
        "personalization_hook": "great show",
        "first_message": "Hi Test Host, love your show...",
        "checked_date": "2026-10-24",
        "priority": "A",
        "lead_score": 92,
        "candidate_status": "Qualified",
    }
    inserted = upsert_lead(lead, db_path=test_db)
    assert inserted is True

    # Upsert again (refresh) - should not duplicate
    updated = upsert_lead(lead, db_path=test_db)
    assert updated is False

    counts = get_lead_count(test_db)
    assert counts["total"] == 1
    assert counts["qualified"] == 1
    assert counts["duplicates"] == 0

    # Record Seed Test
    record_seed_test({
        "test_id": "SEED-TEST-001",
        "channel": "Email",
        "recipient_account": "tester@myaccount.com",
        "message_type": "Step 1: Initial",
        "message_body": "Test message body",
        "delivery_status": "Delivered",
        "reply_logged": "Yes",
        "reply_text": "Sounds interesting, let's talk next week.",
    }, db_path=test_db)

    seed_df = get_seed_tests_df(test_db)
    assert len(seed_df) == 1
    assert seed_df.iloc[0]["reply_logged"] == "Yes"
