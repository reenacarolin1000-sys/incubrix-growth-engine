"""
Command Line Interface (CLI) for the IncuBrix Growth Engine.
Provides clean commands for running the pipeline, refreshing leads, exporting files, and running diagnostics.
"""

import argparse
import sys
from pathlib import Path
from src.pipeline import run_pipeline
from src.database import get_lead_count, get_all_leads_df
from src.export import export_leads_csv, complete_workbook
from src.config import BASE_DIR, LEADS_CSV_PATH


def main():
    parser = argparse.ArgumentParser(
        description="IncuBrix Growth Engine - Option 1: Multi-Channel Lead Generation and Outreach Engine"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available engine commands")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run full discovery, verification, scoring, and outreach pipeline")
    run_parser.add_argument("--target", type=int, default=1000, help="Target minimum qualified leads (default: 1000)")
    run_parser.add_argument("--type", type=str, default="normal", choices=["normal", "repeat", "refresh", "failure_recovery"], help="Run type")

    # Refresh command
    subparsers.add_parser("refresh", help="Refresh existing leads with updated content and ingest new candidates")

    # Export command
    subparsers.add_parser("export", help="Export CRM-ready leads.csv and complete the Excel submission workbook")

    # Status command
    subparsers.add_parser("status", help="Print current database metrics and qualification health")

    args = parser.parse_args()

    if args.command == "run":
        print(f"[*] Starting IncuBrix Growth Engine pipeline (target={args.target}, type={args.type})...")
        results = run_pipeline(target_count=args.target, run_type=args.type)
        print("\n[+] Pipeline Run Completed Successfully!")
        print(f"    - Input candidates: {results['input_size']}")
        print(f"    - Qualified leads: {results['qualified_count']}")
        print(f"    - Priority A leads: {results['priority_a_count']}")
        print(f"    - Rejected leads: {results['rejected_count']}")
        print(f"    - Duplicates removed: {results['duplicates_removed']}")
        print(f"    - Runtime: {results['runtime_min']} minutes")
        print(f"    - Official CSV: {results['csv_path']}")
        print(f"    - Submission Workbook: {results['workbook_path']}")
        print("\nGeographic Validation:")
        geo = results.get("geo_stats", {})
        print(f"    - Approved country share: {geo.get('approved_share', 0)*100:.1f}% (Required: >=80%)")
        print(f"    - Distinct countries: {geo.get('distinct_countries', 0)} (Required: >=3)")
        print(f"    - Max single country share: {geo.get('max_single_country_share', 0)*100:.1f}% (Required: <=60%)")
        print(f"    - Country check status: {'PASSED' if geo.get('is_valid') else 'FAILED'}")

    elif args.command == "refresh":
        print("[*] Running engine refresh...")
        results = run_pipeline(target_count=1000, run_type="refresh")
        print("[+] Refresh completed successfully!")

    elif args.command == "export":
        print("[*] Exporting official CSV and completing workbook...")
        leads_df = get_all_leads_df()
        leads = leads_df.to_dict(orient="records")
        csv_path = export_leads_csv(leads, LEADS_CSV_PATH)
        print(f"[+] Exported leads to {csv_path}")

        ref_wb = Path(r"C:\Users\carolin\OneDrive\Desktop\Incubrix_growth_engineer\reference_files") / "IncuBrix_2027_Growth_Engineer_Option_1_Lead_Generation_and_Outreach_Submission_Workbook.xlsx"
        out_wb = BASE_DIR / "IncuBrix_2027_Growth_Engineer_Option_1_Submission_Workbook_Completed.xlsx"
        if ref_wb.exists():
            complete_workbook(leads, out_wb, ref_wb)
            print(f"[+] Completed submission workbook saved at {out_wb}")

    elif args.command == "status":
        counts = get_lead_count()
        print("\n=== IncuBrix Growth Engine Database Status ===")
        print(f"Total Leads: {counts['total']}")
        print(f"Qualified Leads: {counts['qualified']}")
        print(f"Priority A Leads: {counts['priority_a']}")
        print(f"Priority B Leads: {counts['priority_b']}")
        print(f"Priority C Leads: {counts['priority_c']}")
        print(f"Rejected Leads: {counts['rejected']}")
        print(f"Duplicates: {counts['duplicates']}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
