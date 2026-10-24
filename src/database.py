"""
Database module for the IncuBrix Growth Engine.
Manages SQLite storage, migrations, lead persistence, run logs, audit trails, and seed tests.
"""

import sqlite3
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd
from src.config import DATABASE_PATH, DATABASE_DIR, AUDIT_LOG_PATH


def get_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """Returns a connection to the SQLite database."""
    target_path = db_path or DATABASE_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(target_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Optional[Path] = None) -> None:
    """Initializes the database schema."""
    conn = get_connection(db_path)
    cur = conn.cursor()

    # Leads table - matches official workbook columns
    cur.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        lead_id TEXT PRIMARY KEY,
        creator_name TEXT NOT NULL,
        creator_segment TEXT NOT NULL,
        country_iso2 TEXT NOT NULL,
        primary_language TEXT NOT NULL,
        primary_platform TEXT NOT NULL,
        profile_url TEXT NOT NULL,
        stable_creator_id TEXT UNIQUE NOT NULL,
        followers_or_subscribers TEXT,
        last_content_date TEXT NOT NULL,
        recent_content_url TEXT NOT NULL,
        content_count_30d INTEGER NOT NULL,
        longform_count_60d INTEGER NOT NULL,
        monetization_signal TEXT NOT NULL,
        monetization_evidence_url TEXT NOT NULL,
        incubrix_need TEXT NOT NULL,
        need_evidence_url TEXT NOT NULL,
        best_channel TEXT NOT NULL,
        channel_handle_or_url TEXT NOT NULL,
        channel_evidence_url TEXT NOT NULL,
        backup_channel TEXT NOT NULL,
        personalization_hook TEXT NOT NULL,
        first_message TEXT NOT NULL,
        checked_date TEXT NOT NULL,
        priority TEXT NOT NULL,
        lead_score INTEGER NOT NULL,
        candidate_status TEXT NOT NULL,
        rejection_reason TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        run_id TEXT
    );
    """)

    # Index for fast deduplication checks and priority queries
    cur.execute("CREATE INDEX IF NOT EXISTS idx_leads_stable_id ON leads(stable_creator_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_leads_priority ON leads(priority);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(candidate_status);")

    # Runs table - tracks normal, repeat, refresh, and failure recovery runs
    cur.execute("""
    CREATE TABLE IF NOT EXISTS runs (
        run_id TEXT PRIMARY KEY,
        run_type TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        input_size INTEGER NOT NULL,
        items_produced INTEGER NOT NULL,
        items_rejected INTEGER NOT NULL,
        duplicates_removed INTEGER NOT NULL,
        runtime_min REAL NOT NULL,
        direct_cost REAL NOT NULL,
        notes TEXT
    );
    """)

    # Seed tests table - logs multi-channel delivery on owned test accounts
    cur.execute("""
    CREATE TABLE IF NOT EXISTS seed_tests (
        test_id TEXT PRIMARY KEY,
        channel TEXT NOT NULL,
        recipient_account TEXT NOT NULL,
        message_type TEXT NOT NULL,
        subject_or_hook TEXT NOT NULL,
        message_body TEXT NOT NULL,
        tracking_link TEXT,
        sent_timestamp TEXT NOT NULL,
        delivery_status TEXT NOT NULL,
        reply_logged TEXT NOT NULL,
        reply_text TEXT,
        reply_timestamp TEXT,
        notes TEXT
    );
    """)

    # Audit logs table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        level TEXT NOT NULL,
        action TEXT NOT NULL,
        message TEXT NOT NULL,
        details TEXT
    );
    """)

    conn.commit()
    conn.close()


def clear_leads_table(db_path: Optional[Path] = None) -> None:
    """Clears leads table for clean reset runs while preserving audit logs and runs history."""
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("DELETE FROM leads;")
    conn.commit()
    conn.close()


def log_audit(action: str, message: str, level: str = "INFO", details: str = "", db_path: Optional[Path] = None) -> None:
    """Logs an action to both SQLite database and file."""
    now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        conn = get_connection(db_path)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO audit_logs (timestamp, level, action, message, details) VALUES (?, ?, ?, ?, ?)",
            (now_str, level, action, message, details)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging to DB: {e}")

    try:
        AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{now_str}] [{level}] [{action}] {message} | {details}\n")
    except Exception as e:
        print(f"Error writing to audit file: {e}")


def upsert_lead(lead_dict: Dict[str, Any], run_id: Optional[str] = None, db_path: Optional[Path] = None) -> bool:
    """
    Inserts or updates a lead based on stable_creator_id and lead_id.
    Prevents duplicate primary key collisions and guarantees clean storage.
    """
    conn = get_connection(db_path)
    cur = conn.cursor()
    now_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    # Check if stable_creator_id exists
    cur.execute("SELECT lead_id FROM leads WHERE stable_creator_id = ?", (lead_dict["stable_creator_id"],))
    existing_by_stable = cur.fetchone()

    if existing_by_stable:
        lead_id = existing_by_stable["lead_id"]
        # Update existing record
        cur.execute("""
        UPDATE leads SET
            creator_name = ?,
            creator_segment = ?,
            country_iso2 = ?,
            primary_language = ?,
            primary_platform = ?,
            profile_url = ?,
            followers_or_subscribers = ?,
            last_content_date = ?,
            recent_content_url = ?,
            content_count_30d = ?,
            longform_count_60d = ?,
            monetization_signal = ?,
            monetization_evidence_url = ?,
            incubrix_need = ?,
            need_evidence_url = ?,
            best_channel = ?,
            channel_handle_or_url = ?,
            channel_evidence_url = ?,
            backup_channel = ?,
            personalization_hook = ?,
            first_message = ?,
            checked_date = ?,
            priority = ?,
            lead_score = ?,
            candidate_status = ?,
            rejection_reason = ?,
            updated_at = ?,
            run_id = ?
        WHERE lead_id = ?
        """, (
            lead_dict.get("creator_name", ""),
            lead_dict.get("creator_segment", ""),
            lead_dict.get("country_iso2", ""),
            lead_dict.get("primary_language", "en"),
            lead_dict.get("primary_platform", ""),
            lead_dict.get("profile_url", ""),
            str(lead_dict.get("followers_or_subscribers", "")),
            lead_dict.get("last_content_date", ""),
            lead_dict.get("recent_content_url", ""),
            int(lead_dict.get("content_count_30d", 0)),
            int(lead_dict.get("longform_count_60d", 0)),
            lead_dict.get("monetization_signal", ""),
            lead_dict.get("monetization_evidence_url", ""),
            lead_dict.get("incubrix_need", ""),
            lead_dict.get("need_evidence_url", ""),
            lead_dict.get("best_channel", ""),
            lead_dict.get("channel_handle_or_url", ""),
            lead_dict.get("channel_evidence_url", ""),
            lead_dict.get("backup_channel", ""),
            lead_dict.get("personalization_hook", ""),
            lead_dict.get("first_message", ""),
            lead_dict.get("checked_date", ""),
            lead_dict.get("priority", "C"),
            int(lead_dict.get("lead_score", 0)),
            lead_dict.get("candidate_status", "Qualified"),
            lead_dict.get("rejection_reason", ""),
            now_str,
            run_id,
            lead_id
        ))
        conn.commit()
        conn.close()
        return False
    else:
        lead_id = lead_dict.get("lead_id")
        # Check if lead_id collides with another creator
        if lead_id:
            cur.execute("SELECT 1 FROM leads WHERE lead_id = ?", (lead_id,))
            if cur.fetchone():
                cur.execute("DELETE FROM leads WHERE lead_id = ?", (lead_id,))

        cur.execute("""
        INSERT OR REPLACE INTO leads (
            lead_id, creator_name, creator_segment, country_iso2, primary_language,
            primary_platform, profile_url, stable_creator_id, followers_or_subscribers,
            last_content_date, recent_content_url, content_count_30d, longform_count_60d,
            monetization_signal, monetization_evidence_url, incubrix_need, need_evidence_url,
            best_channel, channel_handle_or_url, channel_evidence_url, backup_channel,
            personalization_hook, first_message, checked_date, priority, lead_score,
            candidate_status, rejection_reason, created_at, updated_at, run_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            lead_id,
            lead_dict.get("creator_name", ""),
            lead_dict.get("creator_segment", ""),
            lead_dict.get("country_iso2", ""),
            lead_dict.get("primary_language", "en"),
            lead_dict.get("primary_platform", ""),
            lead_dict.get("profile_url", ""),
            lead_dict["stable_creator_id"],
            str(lead_dict.get("followers_or_subscribers", "")),
            lead_dict.get("last_content_date", ""),
            lead_dict.get("recent_content_url", ""),
            int(lead_dict.get("content_count_30d", 0)),
            int(lead_dict.get("longform_count_60d", 0)),
            lead_dict.get("monetization_signal", ""),
            lead_dict.get("monetization_evidence_url", ""),
            lead_dict.get("incubrix_need", ""),
            lead_dict.get("need_evidence_url", ""),
            lead_dict.get("best_channel", ""),
            lead_dict.get("channel_handle_or_url", ""),
            lead_dict.get("channel_evidence_url", ""),
            lead_dict.get("backup_channel", ""),
            lead_dict.get("personalization_hook", ""),
            lead_dict.get("first_message", ""),
            lead_dict.get("checked_date", ""),
            lead_dict.get("priority", "C"),
            int(lead_dict.get("lead_score", 0)),
            lead_dict.get("candidate_status", "Qualified"),
            lead_dict.get("rejection_reason", ""),
            now_str,
            now_str,
            run_id
        ))
        conn.commit()
        conn.close()
        return True


def get_all_leads_df(db_path: Optional[Path] = None) -> pd.DataFrame:
    """Returns all leads as a Pandas DataFrame sorted by lead_id."""
    conn = get_connection(db_path)
    df = pd.read_sql_query("SELECT * FROM leads ORDER BY lead_id ASC", conn)
    conn.close()
    return df


def get_qualified_leads_df(db_path: Optional[Path] = None) -> pd.DataFrame:
    """Returns only qualified leads sorted by lead_score descending."""
    conn = get_connection(db_path)
    df = pd.read_sql_query("SELECT * FROM leads WHERE candidate_status = 'Qualified' ORDER BY lead_score DESC, lead_id ASC", conn)
    conn.close()
    return df


def get_lead_count(db_path: Optional[Path] = None) -> Dict[str, int]:
    """Returns count metrics for dashboard and self-checks."""
    conn = get_connection(db_path)
    cur = conn.cursor()
    total = cur.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
    qualified = cur.execute("SELECT COUNT(*) FROM leads WHERE candidate_status = 'Qualified'").fetchone()[0]
    rejected = cur.execute("SELECT COUNT(*) FROM leads WHERE candidate_status = 'Rejected'").fetchone()[0]
    priority_a = cur.execute("SELECT COUNT(*) FROM leads WHERE priority = 'A' AND candidate_status = 'Qualified'").fetchone()[0]
    priority_b = cur.execute("SELECT COUNT(*) FROM leads WHERE priority = 'B' AND candidate_status = 'Qualified'").fetchone()[0]
    priority_c = cur.execute("SELECT COUNT(*) FROM leads WHERE priority = 'C' AND candidate_status = 'Qualified'").fetchone()[0]
    duplicates = cur.execute("SELECT COUNT(*) - COUNT(DISTINCT stable_creator_id) FROM leads").fetchone()[0]
    conn.close()
    return {
        "total": total,
        "qualified": qualified,
        "rejected": rejected,
        "priority_a": priority_a,
        "priority_b": priority_b,
        "priority_c": priority_c,
        "duplicates": duplicates
    }


def record_run(run_data: Dict[str, Any], db_path: Optional[Path] = None) -> None:
    """Saves run metrics to the runs table."""
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO runs (
        run_id, run_type, timestamp, input_size, items_produced,
        items_rejected, duplicates_removed, runtime_min, direct_cost, notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        run_data["run_id"],
        run_data["run_type"],
        run_data.get("timestamp", datetime.datetime.now(datetime.timezone.utc).isoformat()),
        int(run_data.get("input_size", 0)),
        int(run_data.get("items_produced", 0)),
        int(run_data.get("items_rejected", 0)),
        int(run_data.get("duplicates_removed", 0)),
        float(run_data.get("runtime_min", 0.0)),
        float(run_data.get("direct_cost", 0.0)),
        run_data.get("notes", "")
    ))
    conn.commit()
    conn.close()


def get_runs_df(db_path: Optional[Path] = None) -> pd.DataFrame:
    """Returns runs as a DataFrame."""
    conn = get_connection(db_path)
    df = pd.read_sql_query("SELECT * FROM runs ORDER BY timestamp DESC", conn)
    conn.close()
    return df


def record_seed_test(test_data: Dict[str, Any], db_path: Optional[Path] = None) -> None:
    """Records a seed test execution on owned accounts."""
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("""
    INSERT OR REPLACE INTO seed_tests (
        test_id, channel, recipient_account, message_type, subject_or_hook,
        message_body, tracking_link, sent_timestamp, delivery_status,
        reply_logged, reply_text, reply_timestamp, notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        test_data["test_id"],
        test_data["channel"],
        test_data["recipient_account"],
        test_data["message_type"],
        test_data.get("subject_or_hook", ""),
        test_data["message_body"],
        test_data.get("tracking_link", ""),
        test_data.get("sent_timestamp", datetime.datetime.now(datetime.timezone.utc).isoformat()),
        test_data.get("delivery_status", "Delivered"),
        test_data.get("reply_logged", "No"),
        test_data.get("reply_text", ""),
        test_data.get("reply_timestamp", ""),
        test_data.get("notes", "")
    ))
    conn.commit()
    conn.close()


def get_seed_tests_df(db_path: Optional[Path] = None) -> pd.DataFrame:
    """Returns seed tests as a DataFrame."""
    conn = get_connection(db_path)
    df = pd.read_sql_query("SELECT * FROM seed_tests ORDER BY sent_timestamp ASC", conn)
    conn.close()
    return df
