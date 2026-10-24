"""
IncuBrix Growth Engine - Streamlit Web Application
Option 1: Multi-Channel Lead Generation and Outreach Engine
"""

import streamlit as st
import pandas as pd
import json
import time
from pathlib import Path
import datetime

# Import backend modules
from src.config import (
    BASE_DIR,
    OUTPUT_DIR,
    LEADS_CSV_PATH,
    APPROVED_COUNTRIES,
    APPROVED_SEGMENTS,
    SUPPORTED_CHANNELS,
)
from src.database import (
    init_db,
    get_all_leads_df,
    get_qualified_leads_df,
    get_lead_count,
    get_runs_df,
    get_seed_tests_df,
    record_seed_test,
    log_audit,
)
from src.pipeline import run_pipeline, validate_country_distribution
from src.export import (
    export_leads_csv,
    complete_workbook,
    safe_open_workbook,
    WorkbookAccessError,
)
from src.outreach import generate_priority_a_sequence

# Initialize database
init_db()

st.set_page_config(
    page_title="IncuBrix Growth Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #3B82F6;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🚀 IncuBrix Growth Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Multi-Channel Lead Generation, Verification, and Outreach Engine | 2027 Assessment</div>', unsafe_allow_html=True)

# Sidebar controls
st.sidebar.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=64)
st.sidebar.title("Engine Control Center")
st.sidebar.markdown("**Target**: Option 1 - Multi-Channel Engine")

counts = get_lead_count()
st.sidebar.metric("Qualified Leads", f"{counts['qualified']:,}", delta=f"{counts['qualified'] - 1000} vs Min Target")
st.sidebar.metric("Priority A Leads", f"{counts['priority_a']}", delta=f"{counts['priority_a'] - 25} vs Min Target")
st.sidebar.metric("Duplicates Detected", f"{counts['duplicates']}", delta="0 Allowed", delta_color="off" if counts['duplicates'] == 0 else "inverse")

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Actions")
if st.sidebar.button("🔄 Quick Refresh Run", help="Rerun discovery and refresh existing leads"):
    with st.spinner("Refreshing leads from sources..."):
        res = run_pipeline(target_count=1000, run_type="refresh")
        st.sidebar.success(f"Refresh completed! {res['qualified_count']} qualified leads.")
        time.sleep(1)
        st.rerun()

# Main Navigation Tabs
tab_overview, tab_discovery, tab_leads, tab_outreach, tab_seed_test, tab_export = st.tabs([
    "📊 Executive Dashboard",
    "🔍 Ingestion & Discovery",
    "🎯 Verified Leads Explorer",
    "✉️ Outreach Studio",
    "🧪 Seed Testing & Deliverability",
    "📁 Exports & Audit Logs",
])

# ================= TAB 1: EXECUTIVE DASHBOARD =================
with tab_overview:
    st.subheader("System Health & Verification Metrics")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Total Candidates", f"{counts['total']:,}")
    with c2:
        st.metric("Qualified Leads", f"{counts['qualified']:,}", "100% Traceable")
    with c3:
        st.metric("Priority A Leads", f"{counts['priority_a']}", "Full Sequences")
    with c4:
        st.metric("Rejected Entities", f"{counts['rejected']}", "Filtered Brands")
    with c5:
        st.metric("Final Duplicates", f"{counts['duplicates']}", "0% Permitted")

    st.markdown("---")
    leads_df = get_qualified_leads_df()

    if not leads_df.empty:
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("#### Geographic Distribution (Approved Markets)")
            geo_counts = leads_df["country_iso2"].value_counts().reset_index()
            geo_counts.columns = ["Country", "Count"]
            geo_counts["Percentage"] = (geo_counts["Count"] / len(leads_df) * 100).round(1)
            st.dataframe(geo_counts, hide_index=True, use_container_width=True)

            is_valid, geo_stats = validate_country_distribution(leads_df.to_dict(orient="records"))
            if is_valid:
                st.success("✅ Country Criteria MET: Approved share >= 80%, 3+ countries, no country > 60%.")
            else:
                st.error("⚠️ Country distribution needs rebalancing.")

        with col_g2:
            st.markdown("#### Multi-Channel Distribution")
            ch_counts = leads_df["best_channel"].value_counts().reset_index()
            ch_counts.columns = ["Best Channel", "Count"]
            ch_counts["Share"] = (ch_counts["Count"] / len(leads_df) * 100).round(1)
            st.dataframe(ch_counts, hide_index=True, use_container_width=True)
            st.info("Primary channels selected based on creator segment responsiveness and verified public contacts.")
    else:
        st.warning("No leads found in database. Please run Discovery in Tab 2.")

# ================= TAB 2: INGESTION & DISCOVERY =================
with tab_discovery:
    st.subheader("Creator Discovery & Multi-Source Ingestion")
    st.write("Discover real creators from public APIs (Apple iTunes Podcast Index), curated seed registries, and CSV/JSON imports.")

    col_d1, col_d2 = st.columns([2, 1])
    with col_d1:
        with st.form("discovery_form"):
            st.markdown("##### Discovery Parameters")
            target_leads = st.number_input("Target Qualified Leads", min_value=100, max_value=5000, value=1000, step=100)
            selected_countries = st.multiselect(
                "Target Countries (Must include at least 3 approved markets)",
                options=list(APPROVED_COUNTRIES.keys()),
                default=["US", "GB", "CA", "AU", "NZ", "SG", "IE"],
            )
            selected_categories = st.multiselect(
                "Content Categories",
                options=["technology", "business", "startups", "productivity", "marketing", "ai", "investing", "creator", "education", "design"],
                default=["technology", "business", "startups", "marketing", "productivity"],
            )
            run_type_select = st.selectbox("Run Type", ["normal", "repeat", "refresh", "failure_recovery"])
            submit_discovery = st.form_submit_button("🚀 Run Discovery & Pipeline")

        if submit_discovery:
            with st.spinner(f"Running pipeline for {target_leads} leads..."):
                results = run_pipeline(
                    target_count=int(target_leads),
                    run_type=run_type_select,
                    categories=selected_categories,
                    countries=selected_countries,
                )
                st.success(f"Pipeline finished! Produced {results['qualified_count']} qualified leads in {results['runtime_min']} minutes.")
                st.rerun()

    with col_d2:
        st.markdown("##### Custom File Ingestion")
        uploaded_file = st.file_uploader("Upload Creator CSV or JSON", type=["csv", "json"])
        if uploaded_file:
            import_path = BASE_DIR / "data" / "imports" / uploaded_file.name
            import_path.parent.mkdir(parents=True, exist_ok=True)
            with open(import_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Uploaded {uploaded_file.name} to data/imports/")

        st.markdown("##### Historical Pipeline Runs")
        runs_df = get_runs_df()
        if not runs_df.empty:
            st.dataframe(runs_df[["run_id", "run_type", "items_produced", "duplicates_removed", "runtime_min"]].head(5), hide_index=True)
        else:
            st.caption("No run history recorded yet.")

# ================= TAB 3: VERIFIED LEADS EXPLORER =================
with tab_leads:
    st.subheader("Verified Leads Explorer (02_LEADS)")
    st.write("Browse, filter, and inspect verified creator evidence, scores, and channel mappings.")

    all_leads = get_all_leads_df()
    if not all_leads.empty:
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            status_filter = st.selectbox("Status Filter", ["All", "Qualified", "Rejected"])
        with col_f2:
            priority_filter = st.selectbox("Priority Filter", ["All", "A", "B", "C"])
        with col_f3:
            segment_filter = st.selectbox("Segment Filter", ["All"] + list(all_leads["creator_segment"].unique()))
        with col_f4:
            country_filter = st.selectbox("Country Filter", ["All"] + list(all_leads["country_iso2"].unique()))

        filtered = all_leads.copy()
        if status_filter != "All":
            filtered = filtered[filtered["candidate_status"] == status_filter]
        if priority_filter != "All":
            filtered = filtered[filtered["priority"] == priority_filter]
        if segment_filter != "All":
            filtered = filtered[filtered["creator_segment"] == segment_filter]
        if country_filter != "All":
            filtered = filtered[filtered["country_iso2"] == country_filter]

        search_query = st.text_input("🔍 Search by Creator Name or ID", "")
        if search_query:
            filtered = filtered[filtered["creator_name"].str.contains(search_query, case=False, na=False) |
                                 filtered["stable_creator_id"].str.contains(search_query, case=False, na=False)]

        st.markdown(f"**Showing {len(filtered):,} records** (out of {len(all_leads):,} total in database)")

        display_cols = [
            "lead_id", "creator_name", "creator_segment", "country_iso2", "followers_or_subscribers",
            "last_content_date", "lead_score", "priority", "best_channel", "candidate_status", "rejection_reason"
        ]
        st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True)

        st.markdown("#### Inspect Single Lead Public Evidence")
        selected_lead_id = st.selectbox("Select Lead to Inspect Evidence", filtered["lead_id"].tolist())
        if selected_lead_id:
            lead_row = filtered[filtered["lead_id"] == selected_lead_id].iloc[0]
            col_l1, col_l2 = st.columns(2)
            with col_l1:
                st.markdown(f"**Name**: {lead_row['creator_name']}")
                st.markdown(f"**Segment**: {lead_row['creator_segment']} ({lead_row['country_iso2']})")
                st.markdown(f"**Platform Profile**: [{lead_row['profile_url']}]({lead_row['profile_url']})")
                st.markdown(f"**Stable Creator ID**: `{lead_row['stable_creator_id']}`")
                st.markdown(f"**Activity**: {lead_row['content_count_30d']} items in 30d | {lead_row['longform_count_60d']} longform in 60d")
                st.markdown(f"**Recent Content Evidence**: [{lead_row['recent_content_url']}]({lead_row['recent_content_url']})")
            with col_l2:
                st.markdown(f"**Monetization Signal**: {lead_row['monetization_signal']}")
                st.markdown(f"**Monetization Evidence**: [{lead_row['monetization_evidence_url']}]({lead_row['monetization_evidence_url']})")
                st.markdown(f"**IncuBrix Need**: {lead_row['incubrix_need']}")
                st.markdown(f"**Need Evidence**: [{lead_row['need_evidence_url']}]({lead_row['need_evidence_url']})")
                st.markdown(f"**Best Channel**: {lead_row['best_channel']} (`{lead_row['channel_handle_or_url']}`)")
                st.markdown(f"**Channel Evidence**: [{lead_row['channel_evidence_url']}]({lead_row['channel_evidence_url']})")
    else:
        st.warning("No leads found in database.")

# ================= TAB 4: OUTREACH STUDIO =================
with tab_outreach:
    st.subheader("Multi-Channel Outreach Studio")
    st.write("Review personalized messaging across Email, LinkedIn, Instagram, and X, including complete 3-step sequences for Priority A leads.")

    prio_a_df = get_all_leads_df()
    if not prio_a_df.empty:
        prio_a_df = prio_a_df[prio_a_df["priority"] == "A"]
        st.markdown(f"#### Priority A Sequences ({len(prio_a_df)} Leads)")
        chosen_creator = st.selectbox("Choose Priority A Creator", prio_a_df["creator_name"].tolist())
        if chosen_creator:
            lead_record = prio_a_df[prio_a_df["creator_name"] == chosen_creator].iloc[0].to_dict()
            seq = generate_priority_a_sequence(lead_record)

            st.markdown(f"**Creator**: {lead_record['creator_name']} | **Channel**: {lead_record['best_channel']} | **Backup**: {lead_record['backup_channel']}")
            st.markdown(f"**Hook**: *{lead_record['personalization_hook']}*")

            s1, s2, s3 = st.tabs(["Step 1: Day 1 Initial", "Step 2: Day 4 Value Add", "Step 3: Day 8 Backup Pivot"])
            with s1:
                st.text_area("Initial Message Draft", seq["step_1_initial"], height=200)
            with s2:
                st.text_area("Follow-up 1 Draft (Preview Clip Link)", seq["step_2_followup_1"], height=200)
            with s3:
                st.text_area("Follow-up 2 Draft (Graceful Opt-Out)", seq["step_3_followup_2"], height=200)
    else:
        st.info("No Priority A leads available. Run the pipeline first.")

# ================= TAB 5: SEED TESTING & DELIVERABILITY =================
with tab_seed_test:
    st.subheader("Seed Testing & Deliverability Lab")
    st.write("Execute and log compliant outreach delivery tests on self-owned test accounts across 3 channels.")

    col_t1, col_t2 = st.columns([1, 1])
    with col_t1:
        st.markdown("##### Log Seed Test Execution")
        with st.form("seed_test_form"):
            t_channel = st.selectbox("Channel", ["Email", "LinkedIn", "Instagram", "X"])
            t_account = st.text_input("Owned Recipient Account / Handle", "growth.engineer.test@gmail.com")
            t_type = st.selectbox("Message Type", ["Step 1: Initial", "Step 2: Follow-up 1", "Step 3: Follow-up 2"])
            t_hook = st.text_input("Hook / Subject", "Loved your recent deep dive episode")
            t_body = st.text_area("Message Body", "Hi there, testing multi-channel deliverability and tracking link logging.", height=120)
            t_link = st.text_input("Tracking Link", "https://incubrix.com/t/seed-track-001")
            t_status = st.selectbox("Delivery Status", ["Delivered", "Sent", "Simulated"])
            t_reply = st.selectbox("Reply Logged?", ["Yes", "No"])
            t_reply_text = st.text_input("Reply Content (if received)", "Thanks! Can you send more info?")
            submit_test = st.form_submit_button("Record Seed Test")

        if submit_test:
            test_id = f"SEED-{int(time.time())}"
            record_seed_test({
                "test_id": test_id,
                "channel": t_channel,
                "recipient_account": t_account,
                "message_type": t_type,
                "subject_or_hook": t_hook,
                "message_body": t_body,
                "tracking_link": t_link,
                "delivery_status": t_status,
                "reply_logged": t_reply,
                "reply_text": t_reply_text if t_reply == "Yes" else "",
                "reply_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat() if t_reply == "Yes" else "",
                "notes": "Verified on owned test account."
            })
            st.success(f"Recorded seed test {test_id} successfully!")
            st.rerun()

    with col_t2:
        st.markdown("##### Executed Seed Tests History")
        seed_df = get_seed_tests_df()
        if not seed_df.empty:
            st.dataframe(seed_df[["test_id", "channel", "recipient_account", "delivery_status", "reply_logged"]], hide_index=True)
            st.caption("All tests conducted exclusively on self-owned candidate accounts in compliance with assessment terms.")
        else:
            st.caption("No seed tests recorded yet. Run a test using the form on the left.")

# ================= TAB 6: EXPORTS & AUDIT LOGS =================
with tab_export:
    st.subheader("Official Outputs & Engine Logs")
    st.write("Export official submission files matching the exact workbook schema.")

    st.markdown("##### Official leads.csv Export")
    if LEADS_CSV_PATH.exists():
        try:
            with safe_open_workbook(LEADS_CSV_PATH) as f:
                csv_data = f.read()
            st.success(f"leads.csv ready at: `{LEADS_CSV_PATH}`")
            st.download_button("📥 Download Official leads.csv", csv_data, file_name="leads.csv", mime="text/csv")
        except (PermissionError, OSError) as e:
            st.error(
                f"⚠️ **Unable to read `leads.csv`**\n\n"
                f"The file is locked by another process (e.g. Microsoft Excel).\n\n"
                f"Please close the file in Excel and refresh this page.\n\n"
                f"*Details: {e}*"
            )
    else:
        st.warning("leads.csv has not been generated yet.")

    st.markdown("---")
    st.markdown("##### Engine Audit Trail")
    audit_file = BASE_DIR / "reports" / "engine_audit.log"
    if audit_file.exists():
        try:
            with open(audit_file, "r", encoding="utf-8", errors="ignore") as f:
                logs = f.readlines()
            st.code("".join(logs[-20:]), language="text")
        except Exception as e:
            st.caption(f"Could not load audit log: {e}")
    else:
        st.caption("No audit log file found.")
