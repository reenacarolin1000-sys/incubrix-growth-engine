"""
Unit tests for creator verification and qualification rules.
"""

import pytest
from src.verification import verify_creator, is_valid_url


def test_is_valid_url():
    assert is_valid_url("https://example.com/profile") is True
    assert is_valid_url("http://sub.domain.org/path?q=1") is True
    assert is_valid_url("not_a_url") is False
    assert is_valid_url("") is False
    assert is_valid_url(None) is False


def test_verify_valid_creator():
    valid_lead = {
        "creator_name": "Sarah Jenkins",
        "creator_segment": "Podcaster",
        "country_iso2": "US",
        "primary_language": "en",
        "primary_platform": "Apple Podcasts",
        "profile_url": "https://podcasts.apple.com/us/podcast/tech-talk/id123456789",
        "stable_creator_id": "itunes:123456789",
        "last_content_date": "2026-10-20",
        "recent_content_url": "https://podcasts.apple.com/us/podcast/tech-talk/id123456789",
        "content_count_30d": 10,
        "longform_count_60d": 4,
        "monetization_signal": "Sponsorships with Notion and Patreon memberships",
        "monetization_evidence_url": "https://sarahjenkins.com/sponsors",
        "incubrix_need": "Weekly 60-min podcast with zero vertical short-form video repurposing",
        "need_evidence_url": "https://sarahjenkins.com/episodes",
        "best_channel": "Email",
        "channel_handle_or_url": "sarah@jenkins.com",
        "channel_evidence_url": "https://sarahjenkins.com/contact",
        "backup_channel": "LinkedIn",
        "personalization_hook": "your recent episode on scaling creator teams",
        "first_message": "Hi Sarah, loved your recent episode on scaling creator teams. At IncuBrix, we help creators..."
    }
    is_qual, reason = verify_creator(valid_lead)
    assert is_qual is True
    assert reason == ""


def test_reject_media_corporation():
    corporate_lead = {
        "creator_name": "Bloomberg Technology",
        "creator_segment": "Podcaster",
        "country_iso2": "US",
        "primary_language": "en",
        "profile_url": "https://podcasts.apple.com/us/podcast/bloomberg-tech/id1611767434",
        "stable_creator_id": "itunes:1611767434",
        "content_count_30d": 12,
        "longform_count_60d": 6,
        "recent_content_url": "https://bloomberg.com",
        "monetization_signal": "Enterprise corporate ads",
        "monetization_evidence_url": "https://bloomberg.com",
        "incubrix_need": "High volume video",
        "need_evidence_url": "https://bloomberg.com",
        "best_channel": "Email",
        "channel_handle_or_url": "tech@bloomberg.net",
        "channel_evidence_url": "https://bloomberg.com",
        "personalization_hook": "today's market wrap",
        "first_message": "Hi, check out IncuBrix for your video team..."
    }
    is_qual, reason = verify_creator(corporate_lead)
    assert is_qual is False
    assert "corporate media publication" in reason.lower() or "disallowed" in reason.lower()


def test_reject_inactive_creator():
    inactive_lead = {
        "creator_name": "John Doe",
        "creator_segment": "Podcaster",
        "country_iso2": "US",
        "primary_language": "en",
        "profile_url": "https://example.com/johndoe",
        "stable_creator_id": "itunes:999888",
        "content_count_30d": 2,
        "longform_count_60d": 1,
        "recent_content_url": "https://example.com/ep1",
        "monetization_signal": "Patreon link",
        "monetization_evidence_url": "https://patreon.com/johndoe",
        "incubrix_need": "Video repurposing needed",
        "need_evidence_url": "https://example.com",
        "best_channel": "Email",
        "channel_handle_or_url": "john@example.com",
        "channel_evidence_url": "https://example.com",
        "personalization_hook": "your recent episode",
        "first_message": "Hi John, check out IncuBrix..."
    }
    is_qual, reason = verify_creator(inactive_lead)
    assert is_qual is False
    assert "activity threshold" in reason.lower()


def test_reject_non_english_content():
    non_en_lead = {
        "creator_name": "播客中文测试",
        "creator_segment": "Podcaster",
        "country_iso2": "US",
        "primary_language": "en",
        "profile_url": "https://podcasts.apple.com/us/podcast/id111222333",
        "stable_creator_id": "itunes:111222333",
        "content_count_30d": 10,
        "longform_count_60d": 4,
        "recent_content_url": "https://podcasts.apple.com/us/podcast/id111222333",
        "monetization_signal": "Sponsorships",
        "monetization_evidence_url": "https://example.com/sponsors",
        "incubrix_need": "Video repurposing needed",
        "need_evidence_url": "https://example.com",
        "best_channel": "Email",
        "channel_handle_or_url": "contact@chinesecreator.com",
        "channel_evidence_url": "https://example.com",
        "personalization_hook": "your recent episode",
        "first_message": "Hi, check out IncuBrix for video editing workflows..."
    }
    is_qual, reason = verify_creator(non_en_lead)
    assert is_qual is False
    assert "non-english" in reason.lower()


def test_reject_invalid_email_channel():
    bad_email_lead = {
        "creator_name": "Test Creator",
        "creator_segment": "Podcaster",
        "country_iso2": "US",
        "primary_language": "en",
        "profile_url": "https://podcasts.apple.com/us/podcast/id999888777",
        "stable_creator_id": "itunes:999888777",
        "content_count_30d": 10,
        "longform_count_60d": 4,
        "recent_content_url": "https://podcasts.apple.com/us/podcast/id999888777",
        "monetization_signal": "Sponsorships",
        "monetization_evidence_url": "https://example.com/sponsors",
        "incubrix_need": "Video repurposing needed",
        "need_evidence_url": "https://example.com",
        "best_channel": "Email",
        "channel_handle_or_url": "bad_email_with_no_at_sign",
        "channel_evidence_url": "https://example.com",
        "personalization_hook": "your recent episode",
        "first_message": "Hi, check out IncuBrix for video editing workflows..."
    }
    is_qual, reason = verify_creator(bad_email_lead)
    assert is_qual is False
    assert "invalid email" in reason.lower()

