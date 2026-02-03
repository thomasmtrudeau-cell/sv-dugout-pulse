"""
SV Dugout Pulse — Configuration
"""

import logging
import os

# ---------------------------------------------------------------------------
# Google Sheet "Publish to Web" CSV URL
# Set via environment variable or replace the default with your URL.
# In Google Sheets: File -> Share -> Publish to Web -> CSV format -> copy link
# ---------------------------------------------------------------------------
ROSTER_URL = os.environ.get(
    "ROSTER_URL",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vROl4fVdpx2LKElwbZ9kqtXsMY2CmiHn5Jsjn7R5NAyJ5rqpt-EG2JiRj5YExQ1Asi47PO8vEXbum-N/pub?output=csv",
)

# Recruits/Following sheet — players we're tracking but not yet clients
RECRUITS_URL = os.environ.get(
    "RECRUITS_URL",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vRz1OQbckLK52-dxY9YqRNL8U-BRS6p6ipVPCVnhe7W-Bpo2v2imyqaV3hoz0HKRjx6dz207LShEg6j/pub?output=csv",
)

# ---------------------------------------------------------------------------
# Column name mapping (Sheet header -> internal key)
# If a column is renamed in the Sheet, update ONLY here.
# ---------------------------------------------------------------------------
COLUMN_MAP = {
    "Player Name": "player_name",
    "Org": "team",
    "Level": "level",
    "Position": "position",
    "Draft Class": "draft_class",
    "X Handle": "x_handle",
    "Tier": "roster_priority",  # 1-4 internal priority — NOT performance grade
    "State (High School)": "state",
    "State": "state",  # Recruits sheet uses "State" instead of "State (High School)"
    "IG Handle": "ig_handle",
    "DOB": "dob",
    "Age": "age",
}

# Levels to include (everything else is excluded)
INCLUDED_LEVELS = {"Pro", "NCAA"}

# ---------------------------------------------------------------------------
# Performance grade thresholds
# ---------------------------------------------------------------------------
HITTER_STANDOUT_HITS = 3
HITTER_GOOD_HITS = 2
PITCHER_STANDOUT_KS = 5
PITCHER_QS_IP = 6.0
PITCHER_QS_MAX_ER = 3
SLUMP_HITLESS_AB = 12  # 0-for-last-N triggers Soft Flag

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "current_pulse.json")

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
