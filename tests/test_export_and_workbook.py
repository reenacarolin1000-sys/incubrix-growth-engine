"""
Tests for export schema fidelity, workbook preservation, and geographic validation.
"""

import sys
import os
import pytest
import pandas as pd
from pathlib import Path
from src.export import (
    export_leads_csv,
    OFFICIAL_WORKBOOK_COLUMNS,
    safe_open_workbook,
    WorkbookAccessError,
)
from src.pipeline import validate_country_distribution
from src.config import BASE_DIR


def test_export_leads_csv_schema(tmp_path):
    out_csv = tmp_path / "test_leads.csv"
    leads = [
        {
            "lead_id": "LEAD-0001",
            "creator_name": "Test Creator",
            "creator_segment": "Podcaster",
            "country_iso2": "US",
            "primary_language": "en",
            "primary_platform": "Apple Podcasts",
            "profile_url": "https://example.com/profile",
            "stable_creator_id": "test:001",
            "followers_or_subscribers": "10,000",
            "last_content_date": "2026-10-20",
            "recent_content_url": "https://example.com/recent",
            "content_count_30d": 12,
            "longform_count_60d": 6,
            "monetization_signal": "Sponsorships",
            "monetization_evidence_url": "https://example.com/sponsor",
            "incubrix_need": "Video repurposing",
            "need_evidence_url": "https://example.com/need",
            "best_channel": "Email",
            "channel_handle_or_url": "test@example.com",
            "channel_evidence_url": "https://example.com/contact",
            "backup_channel": "LinkedIn",
            "personalization_hook": "great show",
            "first_message": "Hello there...",
            "checked_date": "2026-10-24",
            "priority": "A",
            "lead_score": 95,
            "candidate_status": "Qualified",
            "rejection_reason": "",
        }
    ]

    export_leads_csv(leads, out_csv)
    assert out_csv.exists()

    df = pd.read_csv(out_csv)
    assert len(df) == 1
    assert list(df.columns) == OFFICIAL_WORKBOOK_COLUMNS
    assert df.iloc[0]["duplicate_check"] == "UNIQUE"
    assert df.iloc[0]["completeness_check"] == "COMPLETE"


def test_validate_country_distribution():
    valid_leads = (
        [{"country_iso2": "US"}] * 480 +
        [{"country_iso2": "GB"}] * 240 +
        [{"country_iso2": "CA"}] * 140 +
        [{"country_iso2": "AU"}] * 90 +
        [{"country_iso2": "NZ"}] * 25 +
        [{"country_iso2": "SG"}] * 25
    )
    is_valid, stats = validate_country_distribution(valid_leads)
    assert is_valid is True
    assert stats["approved_share"] == 1.0
    assert stats["distinct_countries"] == 6
    assert stats["max_single_country_share"] <= 0.60

    # Test invalid: single country exceeds 60%
    invalid_leads = (
        [{"country_iso2": "US"}] * 700 +
        [{"country_iso2": "GB"}] * 200 +
        [{"country_iso2": "CA"}] * 100
    )
    is_valid_inv, stats_inv = validate_country_distribution(invalid_leads)
    assert is_valid_inv is False
    assert stats_inv["max_single_country_share"] == 0.70


def test_safe_open_workbook_normal(tmp_path):
    """Test reading a standard accessible file using safe_open_workbook."""
    test_file = tmp_path / "sample.xlsx"
    test_file.write_bytes(b"PK\x03\x04test_content_normal")

    handle_ref = None
    with safe_open_workbook(test_file) as f:
        handle_ref = f
        data = f.read()
        assert data == b"PK\x03\x04test_content_normal"
        assert not f.closed

    # Verify handle is closed upon exit
    assert handle_ref.closed


def test_safe_open_workbook_nonexistent():
    """Test that safe_open_workbook raises FileNotFoundError for missing files."""
    missing_path = Path("non_existent_workbook_12345.xlsx")
    with pytest.raises(FileNotFoundError):
        with safe_open_workbook(missing_path) as f:
            pass


def test_safe_open_workbook_preserves_original(tmp_path):
    """Test that original file is not deleted or overwritten."""
    test_file = tmp_path / "original.xlsx"
    original_bytes = b"EXACT_ORIGINAL_CONTENT_PRESERVED"
    test_file.write_bytes(original_bytes)
    mtime_before = test_file.stat().st_mtime

    with safe_open_workbook(test_file) as f:
        assert f.read() == original_bytes

    assert test_file.exists()
    assert test_file.read_bytes() == original_bytes
    assert test_file.stat().st_mtime == mtime_before


@pytest.mark.skipif(sys.platform != "win32", reason="Windows file sharing test")
def test_safe_open_workbook_excel_sharing_lock(tmp_path):
    """Test reading a file held open with Excel-style sharing locks on Windows."""
    import ctypes
    from ctypes import wintypes

    test_file = tmp_path / "locked_by_excel.xlsx"
    content = b"WORKBOOK_CONTENT_SIMULATING_EXCEL_OPEN"
    test_file.write_bytes(content)

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    GENERIC_READ = 0x80000000
    GENERIC_WRITE = 0x40000000
    DELETE = 0x00010000
    FILE_SHARE_READ = 0x00000001
    FILE_SHARE_WRITE = 0x00000002
    FILE_SHARE_DELETE = 0x00000004
    OPEN_EXISTING = 3
    FILE_ATTRIBUTE_NORMAL = 0x80

    # Excel opens files with GENERIC_READ | GENERIC_WRITE | DELETE and full sharing
    handle = kernel32.CreateFileW(
        str(test_file),
        GENERIC_READ | GENERIC_WRITE | DELETE,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
        None,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        None,
    )
    assert handle not in (-1, wintypes.HANDLE(-1).value)

    try:
        # Standard open() fails with PermissionError because CRT doesn't share DELETE
        with pytest.raises(PermissionError):
            open(test_file, "rb")

        # safe_open_workbook succeeds via shared read / temp fallback
        with safe_open_workbook(test_file) as f:
            data = f.read()
            assert data == content
            assert not f.closed
    finally:
        kernel32.CloseHandle(handle)


@pytest.mark.skipif(sys.platform != "win32", reason="Windows file sharing test")
def test_safe_open_workbook_exclusive_lock_raises(tmp_path):
    """Test that safe_open_workbook raises PermissionError/WorkbookAccessError on exclusive lock."""
    import ctypes
    from ctypes import wintypes

    test_file = tmp_path / "exclusively_locked.xlsx"
    test_file.write_bytes(b"EXCLUSIVE_CONTENT")

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    GENERIC_READ = 0x80000000
    GENERIC_WRITE = 0x40000000
    OPEN_EXISTING = 3
    FILE_ATTRIBUTE_NORMAL = 0x80

    # Open with dwShareMode = 0 (exclusive lock)
    handle = kernel32.CreateFileW(
        str(test_file),
        GENERIC_READ | GENERIC_WRITE,
        0,  # No sharing
        None,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        None,
    )
    assert handle not in (-1, wintypes.HANDLE(-1).value)

    try:
        with pytest.raises(PermissionError):
            with safe_open_workbook(test_file) as f:
                f.read()
    finally:
        kernel32.CloseHandle(handle)


def test_safe_open_workbook_completed_submission_workbook():
    """Verify that the completed submission workbook can be read safely right now."""
    completed_wb = BASE_DIR / "IncuBrix_2027_Growth_Engineer_Option_1_Submission_Workbook_Completed.xlsx"
    assert completed_wb.exists(), "Completed workbook must exist"

    with safe_open_workbook(completed_wb) as f:
        data = f.read()
        assert len(data) > 0
        assert data.startswith(b"PK")  # Valid zip/xlsx magic header


def test_app_runs_cleanly_via_apptest():
    """Verify that app.py runs with zero uncaught exceptions, CSV download is active, workbook button removed."""
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(BASE_DIR / "app.py"))
    at.run()
    assert len(at.exception) == 0, f"App execution raised exceptions: {[e.message for e in at.exception]}"

    # Verify CSV download button is present
    labels = [btn.label for btn in at.download_button]
    assert any("leads.csv" in label for label in labels), "Official leads.csv download button must be present"

    # Verify completed workbook download button is removed from app UI
    assert not any("Workbook" in label for label in labels), "Workbook download button must be removed from UI"

    # Verify audit trail code block is visible
    assert len(at.code) >= 1, "Audit log trail must be visible"

