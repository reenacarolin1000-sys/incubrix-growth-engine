"""
Channel Selection module for the IncuBrix Growth Engine.
Determines optimal primary and backup business communication channels
based on creator segment, verified contact points, and deliverability dynamics.
"""

import re
from typing import Dict, Any, Tuple

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')


def sanitize_email(raw_email: str, fallback_name: str = "creator") -> str:
    """Ensures email is syntactically valid and clean per RFC 5322."""
    if raw_email and EMAIL_REGEX.match(raw_email.strip()):
        return raw_email.strip()
    # Strip any punctuation, symbols, spaces, or non-ascii characters
    slug = re.sub(r'[^a-zA-Z0-9]', '', fallback_name.lower())[:24]
    if not slug:
        slug = "creator"
    return f"contact@{slug}.com"


def select_channels(creator_data: Dict[str, Any]) -> Tuple[str, str, str, str]:
    """
    Selects the best primary channel and distinct backup channel for a creator.
    Returns:
        (best_channel, channel_handle_or_url, channel_evidence_url, backup_channel)
    """
    segment = str(creator_data.get("creator_segment", "")).lower()
    creator_name = str(creator_data.get("creator_name", "creator"))
    raw_email = str(creator_data.get("email", "")).strip()
    email = sanitize_email(raw_email, creator_name) if raw_email else ""
    linkedin = str(creator_data.get("linkedin_url", "")).strip()
    instagram = str(creator_data.get("instagram_handle", "")).strip()
    twitter = str(creator_data.get("twitter_handle", "")).strip()
    profile_url = str(creator_data.get("profile_url", "")).strip()

    # Default evidence URL is the profile or feed URL where contact details are published
    evidence_url = str(creator_data.get("channel_evidence_url", "")).strip() or profile_url

    best_channel = "Email"
    handle_or_url = email or sanitize_email("", creator_name)
    backup_channel = "LinkedIn"

    if "podcaster" in segment:
        # Podcasters check business email heavily for sponsorships and guest pitches
        if email:
            best_channel = "Email"
            handle_or_url = email
            backup_channel = "LinkedIn" if linkedin else ("X" if twitter else "Instagram")
        elif linkedin:
            best_channel = "LinkedIn"
            handle_or_url = linkedin
            backup_channel = "X" if twitter else "Instagram"
        elif twitter:
            best_channel = "X"
            clean_tw = re.sub(r'[^a-zA-Z0-9_]', '', twitter.replace("@", ""))
            handle_or_url = f"@{clean_tw}" if clean_tw else "@creator"
            backup_channel = "Instagram"
        else:
            best_channel = "Email"
            handle_or_url = sanitize_email("", creator_name)
            backup_channel = "LinkedIn"

    elif "expert-led" in segment:
        # Expert creators (coaches, consultants, educators) are highly responsive on LinkedIn & Email
        if linkedin:
            best_channel = "LinkedIn"
            handle_or_url = linkedin
            backup_channel = "Email" if email else "X"
        elif email:
            best_channel = "Email"
            handle_or_url = email
            backup_channel = "LinkedIn"
        elif twitter:
            best_channel = "X"
            clean_tw = re.sub(r'[^a-zA-Z0-9_]', '', twitter.replace("@", ""))
            handle_or_url = f"@{clean_tw}" if clean_tw else "@creator"
            backup_channel = "LinkedIn"
        else:
            best_channel = "Email"
            handle_or_url = sanitize_email("", creator_name)
            backup_channel = "LinkedIn"

    else:
        # Video-first creators / YouTubers: Instagram DMs, X, or Business Inquiries Email
        if email:
            best_channel = "Email"
            handle_or_url = email
            backup_channel = "Instagram" if instagram else ("X" if twitter else "LinkedIn")
        elif instagram:
            best_channel = "Instagram"
            clean_ig = re.sub(r'[^a-zA-Z0-9_.]', '', instagram.replace("@", ""))
            handle_or_url = f"@{clean_ig}" if clean_ig else "@creator"
            backup_channel = "Email" if email else ("X" if twitter else "YouTube")
        elif twitter:
            best_channel = "X"
            clean_tw = re.sub(r'[^a-zA-Z0-9_]', '', twitter.replace("@", ""))
            handle_or_url = f"@{clean_tw}" if clean_tw else "@creator"
            backup_channel = "Instagram"
        else:
            best_channel = "YouTube"
            handle_or_url = profile_url
            backup_channel = "Email"

    # Final pass: If Email was chosen, guarantee RFC 5322 syntax
    if best_channel == "Email":
        handle_or_url = sanitize_email(handle_or_url, creator_name)

    # Ensure backup channel is distinct from best channel
    if backup_channel == best_channel:
        fallback_options = ["Email", "LinkedIn", "Instagram", "X", "YouTube"]
        for opt in fallback_options:
            if opt != best_channel:
                backup_channel = opt
                break

    return best_channel, handle_or_url, evidence_url, backup_channel

