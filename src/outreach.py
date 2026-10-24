"""
Outreach Generation module for the IncuBrix Growth Engine.
Generates compliant, highly personalized multi-channel outreach sequences (Email, LinkedIn, Instagram, X),
including initial messages and two structured follow-ups for all Priority A leads.
"""

import re
from typing import Dict, Any, List
from pathlib import Path
from src.config import OUTREACH_SEQUENCES_DIR, OUTREACH_PRIORITY_A_DIR


def sanitize_filename(name: str) -> str:
    """Removes invalid characters for Windows file systems."""
    return re.sub(r'[\\/*?:"<>|]', "", name).strip().replace(" ", "_")


def generate_first_message(lead: Dict[str, Any]) -> str:
    """
    Drafts an authentic, compliant first outreach message tailored to the creator's
    chosen channel, recent content hook, and verified workflow need.
    """
    creator_name = lead.get("creator_name", "there")
    first_name = creator_name.split()[0] if creator_name else "there"
    channel = lead.get("best_channel", "Email")
    hook = lead.get("personalization_hook", "your recent content")
    need = lead.get("incubrix_need", "streamlining your content workflow")

    if channel == "Email":
        return (
            f"Subject: Loved {hook} — idea for repurposing into vertical clips\n\n"
            f"Hi {first_name},\n\n"
            f"I recently caught your discussion on {hook} — really sharp insights.\n\n"
            f"I noticed {need.lower()}. At IncuBrix, we built an AI workflow engine specifically "
            f"for creators that converts long-form recordings into high-converting vertical shorts, "
            f"automated show notes, and stylized captions in minutes without manual editing friction.\n\n"
            f"Would you be open to seeing a 60-second preview clip we rendered from your latest episode?\n\n"
            f"Best regards,\n"
            f"Growth Engineering Team | IncuBrix\n"
            f"P.S. If you prefer not to receive updates, simply reply 'unsubscribe' and we will remove your contact immediately."
        )

    elif channel == "LinkedIn":
        return (
            f"Hi {first_name}, really enjoyed your recent breakdown on {hook}. "
            f"Noticed {need.lower()}. We developed IncuBrix to help creators automatically repurpose "
            f"long-form episodes into viral vertical clips, complete with dynamic subtitles and automated show notes. "
            f"Happy to send over a 60-second preview clip rendered from your recent show if you're curious! "
            f"(Reply 'opt-out' to cease messages)."
        )

    elif channel in ("Instagram", "X"):
        return (
            f"Hey {first_name}! Loved your recent post regarding {hook}. "
            f"Saw {need.lower()} — we built IncuBrix to automate turning long-form videos into high-engagement "
            f"Reels/Shorts with zero editing lag. We put together a quick sample clip from your latest episode. "
            f"Mind if I send the link over? (Reply 'stop' anytime to opt out)."
        )

    else:
        # Podcast Guest Pitch / YouTube Community
        return (
            f"Hi {first_name},\n\n"
            f"Huge fan of your show and your recent insights on {hook}.\n\n"
            f"Knowing that {need.lower()}, our team at IncuBrix created an automated pipeline that produces "
            f"studio-grade vertical clips and transcripts from full-length episodes with one click.\n\n"
            f"Would love to share a complimentary repurposed video asset we generated for your show. "
            f"Let me know if you'd like to take a look!\n\n"
            f"— IncuBrix Growth Team (Reply 'unsubscribe' to opt out)"
        )


def generate_priority_a_sequence(lead: Dict[str, Any]) -> Dict[str, str]:
    """
    Generates a full 3-step sequence (Initial Message + Follow-up 1 + Follow-up 2)
    for a Priority A creator.
    """
    creator_name = lead.get("creator_name", "there")
    first_name = creator_name.split()[0] if creator_name else "there"
    best_chan = lead.get("best_channel", "Email")
    backup_chan = lead.get("backup_channel", "LinkedIn")
    hook = lead.get("personalization_hook", "your recent work")
    need = lead.get("incubrix_need", "your video production cadence")

    # Step 1: Initial Outreach (Day 1)
    step1 = generate_first_message(lead)

    # Step 2: Follow-up 1 (Day 4) - Value-Add & Concrete Demo
    if best_chan == "Email":
        step2 = (
            f"Subject: Re: Loved {hook} — idea for repurposing into vertical clips\n\n"
            f"Hi {first_name},\n\n"
            f"Following up quickly on my note from earlier this week. I know you're busy running the show!\n\n"
            f"We actually ran a 90-second snippet of {hook} through IncuBrix to test how the AI handles "
            f"speaker tracking and dynamic captions. It identified 3 high-hook moments and generated "
            f"ready-to-post vertical assets complete with sound-wave animations.\n\n"
            f"Here is a private preview link to see the rendered assets: https://incubrix.com/preview/{lead.get('stable_creator_id', 'demo')}\n\n"
            f"No strings attached — feel free to post them if you like them. Would 10 minutes next Tuesday work "
            f"to show you how you can automate this for all upcoming episodes?\n\n"
            f"Best,\n"
            f"Growth Engineering Team | IncuBrix\n"
            f"(Reply 'unsubscribe' to opt out)"
        )
    else:
        step2 = (
            f"Hey {first_name}, following up on my previous note! We went ahead and processed a quick snippet from "
            f"{hook} using IncuBrix's vertical clipping engine. It pulled 3 viral hooks and added kinetic subtitles. "
            f"Take a look here: https://incubrix.com/preview/{lead.get('stable_creator_id', 'demo')} — feel free to use it! "
            f"Open to a quick 5-min chat next week? (Reply 'stop' to opt out)"
        )

    # Step 3: Follow-up 2 (Day 8) - Multi-Channel Touchpoint on Backup Channel & Graceful Close
    step3 = (
        f"Hi {first_name}, reaching out via {backup_chan} as a final touchpoint regarding {hook}.\n\n"
        f"We understand your priority is maintaining high production quality without spending hours on "
        f"{need.lower()}. If the timing isn't right right now, no worries at all!\n\n"
        f"If you ever need an automated way to turn your archive and future episodes into viral short-form assets, "
        f"our platform is ready for you at incubrix.com.\n\n"
        f"Wishing you continued growth with your audience!\n\n"
        f"— IncuBrix Growth Engineering Team (Reply 'stop' or 'unsubscribe' to opt out)"
    )

    return {
        "step_1_initial": step1,
        "step_2_followup_1": step2,
        "step_3_followup_2": step3,
    }


def write_all_priority_a_sequences(priority_a_leads: List[Dict[str, Any]]) -> int:
    """
    Writes sequence files for each Priority A lead into outreach/priority_a/
    and writes general sequence templates into outreach/sequences/.
    """
    OUTREACH_PRIORITY_A_DIR.mkdir(parents=True, exist_ok=True)
    OUTREACH_SEQUENCES_DIR.mkdir(parents=True, exist_ok=True)

    # Clean existing sequence files to match current run exactly
    for old_f in OUTREACH_PRIORITY_A_DIR.glob("*.md"):
        try:
            old_f.unlink()
        except Exception:
            pass

    written_count = 0
    for lead in priority_a_leads:
        lead_id = lead.get("lead_id", f"LEAD-{written_count+1:04d}")
        seq = generate_priority_a_sequence(lead)
        safe_name = sanitize_filename(lead.get('creator_name', 'creator'))[:40]
        file_path = OUTREACH_PRIORITY_A_DIR / f"{lead_id}_{safe_name}.md"

        content = (
            f"# Priority A Outreach Sequence: {lead.get('creator_name')} ({lead_id})\n\n"
            f"- **Segment**: {lead.get('creator_segment')}\n"
            f"- **Country**: {lead.get('country_iso2')}\n"
            f"- **Best Channel**: {lead.get('best_channel')} ({lead.get('channel_handle_or_url')})\n"
            f"- **Backup Channel**: {lead.get('backup_channel')}\n"
            f"- **Hook**: {lead.get('personalization_hook')}\n"
            f"- **IncuBrix Need**: {lead.get('incubrix_need')}\n"
            f"- **Evidence URL**: {lead.get('recent_content_url')}\n\n"
            f"---\n\n"
            f"### Step 1: Initial Touchpoint (Day 1 - {lead.get('best_channel')})\n\n"
            f"```text\n{seq['step_1_initial']}\n```\n\n"
            f"### Step 2: Follow-up 1 (Day 4 - {lead.get('best_channel')})\n\n"
            f"```text\n{seq['step_2_followup_1']}\n```\n\n"
            f"### Step 3: Follow-up 2 (Day 8 - {lead.get('backup_channel')})\n\n"
            f"```text\n{seq['step_3_followup_2']}\n```\n"
        )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        written_count += 1

    # Write segment playbook sequences in outreach/sequences/
    _write_segment_playbooks()

    return written_count


def _write_segment_playbooks():
    """Generates standard segment sequence templates across 3+ channels."""
    channels = ["Email", "LinkedIn", "Instagram", "X"]
    for ch in channels:
        path = OUTREACH_SEQUENCES_DIR / f"sequence_playbook_{ch.lower()}.md"
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# IncuBrix Multi-Channel Outreach Playbook: {ch}\n\n")
            f.write("## 1. Channel Mechanics & Sending Cadence\n")
            f.write(f"- Safe Daily Volume: {ch} is capped to maintain 100% account reputation.\n")
            f.write("- Cadence: Day 1 initial message, Day 4 follow-up with asset preview, Day 8 backup channel pivot.\n\n")
            f.write("## 2. Podcaster Sequence Template\n")
            f.write(f"Tailored to long-form audio/video shows needing short-form vertical discovery clips.\n\n")
            f.write("## 3. Video-First Creator Sequence Template\n")
            f.write(f"Tailored to YouTubers producing high-volume tutorial or video essays with editing bottlenecks.\n\n")
            f.write("## 4. Expert-Led Creator Sequence Template\n")
            f.write(f"Tailored to consultants and course creators wanting to repurpose webinars into social lead magnets.\n\n")
            f.write("## 5. Mandatory Compliance Checklist\n")
            f.write("- Verified public business contact only\n")
            f.write("- Content-specific hook required\n")
            f.write("- Clear opt-out mechanism included\n")
            f.write("- Sender identity explicitly stated\n")
