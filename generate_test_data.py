"""
SV Dugout Pulse — Test Data Generator

Generates realistic test data for all dashboard views:
- current_pulse.json: Today's live stats
- window_7d.json: 7-day rolling stats
- window_30d.json: 30-day rolling stats
- window_season.json: Season-to-date stats

Usage:
    python generate_test_data.py
"""

import json
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
OUTPUT_PATH = os.path.join(DATA_DIR, "current_pulse.json")
WINDOW_7D_PATH = os.path.join(DATA_DIR, "window_7d.json")
WINDOW_30D_PATH = os.path.join(DATA_DIR, "window_30d.json")
WINDOW_SEASON_PATH = os.path.join(DATA_DIR, "window_season.json")

# Uses real player names from the roster for realism
TEST_PULSE = [
    # --- 💎 Milestone (Pro, Client) ---
    {
        "player_name": "Aaron Watson",
        "team": "Cincinnati Reds",
        "level": "Pro",
        "stats_summary": "5.0 IP, 3 H, 0 ER, 6 K, 1 BB, W",
        "game_context": "CIN 4, PIT 1 | Final",
        "game_status": "Final",
        "performance_grade": "\U0001f48e Milestone",
        "social_search_url": 'https://x.com/search?q=%22Aaron%20Watson%22%20Reds&f=live',
        "is_client": True,
        "tags": {
            "draft_class": "N/A",
            "position": "Pitcher",
            "roster_priority": 2,
        },
    },
    # --- 🔥 Standout Hitter (Pro, Final, Win) ---
    {
        "player_name": "Dax Kilby",
        "team": "New York Yankees",
        "level": "Pro",
        "stats_summary": "2-4, HR, 3 RBI",
        "game_context": "NYY 6, BOS 3 | Final",
        "game_status": "Final",
        "performance_grade": "\U0001f525 Standout",
        "social_search_url": 'https://x.com/search?q=%22Dax%20Kilby%22%20Yankees&f=live',
        "is_client": True,
        "tags": {
            "draft_class": "N/A",
            "position": "Hitter",
            "roster_priority": 1,
        },
    },
    # --- 🔥 Standout Pitcher (Pro, Final) ---
    {
        "player_name": "Garrett Whitlock",
        "team": "Boston Red Sox",
        "level": "Pro",
        "stats_summary": "7.0 IP, 4 H, 1 ER, 8 K, 0 BB, W",
        "game_context": "BOS 5, TB 2 | Final",
        "game_status": "Final",
        "performance_grade": "\U0001f525 Standout",
        "social_search_url": 'https://x.com/search?q=%22Garrett%20Whitlock%22%20Sox&f=live',
        "is_client": True,
        "tags": {
            "draft_class": "N/A",
            "position": "Pitcher",
            "roster_priority": 1,
        },
    },
    # --- 🔥 Standout Hitter (NCAA, Final) ---
    {
        "player_name": "Kyle Jones",
        "team": "Florida",
        "level": "NCAA",
        "stats_summary": "3-4, 2B, 2 RBI, 2 R",
        "game_context": "UF 9, UGA 3 | Final",
        "game_status": "Final",
        "performance_grade": "\U0001f525 Standout",
        "social_search_url": 'https://x.com/search?q=%22Kyle%20Jones%22%20Florida&f=live',
        "is_client": True,
        "tags": {
            "draft_class": "2026",
            "position": "Hitter",
            "roster_priority": 1,
        },
    },
    # --- ✅ Good (Pro, Live game) ---
    {
        "player_name": "Kellon Lindsey",
        "team": "Los Angeles Dodgers",
        "level": "Pro",
        "stats_summary": "2-3, RBI, R",
        "game_context": "LAD 3, SF 2 | Bot 6th",
        "game_status": "Live",
        "performance_grade": "\u2705 Good",
        "social_search_url": 'https://x.com/search?q=%22Kellon%20Lindsey%22%20Dodgers&f=live',
        "is_client": True,
        "tags": {
            "draft_class": "N/A",
            "position": "Hitter",
            "roster_priority": 1,
        },
    },
    # --- ✅ Good (NCAA) ---
    {
        "player_name": "Myles Bailey",
        "team": "Florida State",
        "level": "NCAA",
        "stats_summary": "2-4, R",
        "game_context": "FSU 5, MIA 4 | Final",
        "game_status": "Final",
        "performance_grade": "\u2705 Good",
        "social_search_url": 'https://x.com/search?q=%22Myles%20Bailey%22%20Florida%20State&f=live',
        "is_client": True,
        "tags": {
            "draft_class": "2026",
            "position": "Hitter",
            "roster_priority": 1,
        },
    },
    # --- 😐 Routine (Pro) ---
    {
        "player_name": "Sterlin Thompson",
        "team": "Colorado Rockies",
        "level": "Pro",
        "stats_summary": "1-4",
        "game_context": "COL 3, ARI 7 | Final",
        "game_status": "Final",
        "performance_grade": "\U0001f610 Routine",
        "social_search_url": 'https://x.com/search?q=%22Sterlin%20Thompson%22%20Rockies&f=live',
        "is_client": True,
        "tags": {
            "draft_class": "N/A",
            "position": "Hitter",
            "roster_priority": 2,
        },
    },
    # --- 😐 Routine Pitcher (NCAA) ---
    {
        "player_name": "Cam Flukey",
        "team": "Coastal Carolina",
        "level": "NCAA",
        "stats_summary": "2.0 IP, 2 H, 1 ER, 2 K, 1 BB",
        "game_context": "CCU 6, JMU 5 | Final",
        "game_status": "Final",
        "performance_grade": "\U0001f610 Routine",
        "social_search_url": 'https://x.com/search?q=%22Cam%20Flukey%22%20Coastal&f=live',
        "is_client": True,
        "tags": {
            "draft_class": "2026",
            "position": "Pitcher",
            "roster_priority": 1,
        },
    },
    # --- 🚩 Soft Flag (Pro, cold bat) ---
    {
        "player_name": "Cade Doughty",
        "team": "Toronto Blue Jays",
        "level": "Pro",
        "stats_summary": "0-4",
        "game_context": "TOR 2, BAL 5 | Final",
        "game_status": "Final",
        "performance_grade": "\U0001f6a9 Soft Flag",
        "social_search_url": 'https://x.com/search?q=%22Cade%20Doughty%22%20Jays&f=live',
        "is_client": True,
        "tags": {
            "draft_class": "N/A",
            "position": "Hitter",
            "roster_priority": 2,
        },
    },
    # --- 🚩 Soft Flag Pitcher (Pro, rough outing) ---
    {
        "player_name": "Tanner Gordon",
        "team": "Colorado Rockies",
        "level": "Pro",
        "stats_summary": "3.1 IP, 7 H, 5 ER, 2 K, 3 BB, L",
        "game_context": "COL 3, ARI 7 | Final",
        "game_status": "Final",
        "performance_grade": "\U0001f6a9 Soft Flag",
        "social_search_url": 'https://x.com/search?q=%22Tanner%20Gordon%22%20Rockies&f=live',
        "is_client": True,
        "tags": {
            "draft_class": "N/A",
            "position": "Pitcher",
            "roster_priority": 2,
        },
    },
    # --- Live game (NCAA, in progress) ---
    {
        "player_name": "Joe Tiroly",
        "team": "Virginia",
        "level": "NCAA",
        "stats_summary": "1-2, BB",
        "game_context": "UVA 2, VT 1 | Top 5th",
        "game_status": "Live",
        "performance_grade": "\U0001f610 Routine",
        "social_search_url": 'https://x.com/search?q=%22Joe%20Tiroly%22%20Virginia&f=live',
        "is_client": True,
        "tags": {
            "draft_class": "2026",
            "position": "Hitter",
            "roster_priority": 2,
        },
    },
    # --- No data (player with no game today) ---
    {
        "player_name": "Aiden Robbins",
        "team": "Texas",
        "level": "NCAA",
        "stats_summary": "No game data",
        "game_context": "",
        "game_status": "N/A",
        "performance_grade": "\u2014 No Data",
        "social_search_url": 'https://x.com/search?q=%22Aiden%20Robbins%22%20Texas&f=live',
        "is_client": True,
        "tags": {
            "draft_class": "2026",
            "position": "Hitter",
            "roster_priority": 1,
        },
    },
    # =========== RECRUITS (Following) ===========
    # --- 🔥 Standout (Following, NCAA) ---
    {
        "player_name": "Chase Burns",
        "team": "Tennessee",
        "level": "NCAA",
        "stats_summary": "7.0 IP, 2 H, 0 ER, 12 K, 1 BB",
        "game_context": "TENN 5, BAMA 0 | Final",
        "game_status": "Final",
        "performance_grade": "\U0001f525 Standout",
        "social_search_url": 'https://x.com/search?q=%22Chase%20Burns%22%20Tennessee&f=live',
        "is_client": False,
        "tags": {
            "draft_class": "2025",
            "position": "Pitcher",
            "roster_priority": 1,
        },
    },
    # --- ✅ Good (Following, NCAA) ---
    {
        "player_name": "Jac Caglianone",
        "team": "Florida",
        "level": "NCAA",
        "stats_summary": "2-4, HR, 2 RBI",
        "game_context": "UF 7, LSU 4 | Final",
        "game_status": "Final",
        "performance_grade": "\U0001f525 Standout",
        "social_search_url": 'https://x.com/search?q=%22Jac%20Caglianone%22%20Florida&f=live',
        "is_client": False,
        "tags": {
            "draft_class": "2025",
            "position": "Two-Way",
            "roster_priority": 1,
        },
    },
    # --- 😐 Routine (Following, Pro) ---
    {
        "player_name": "Dylan Crews",
        "team": "Washington Nationals",
        "level": "Pro",
        "stats_summary": "1-4, R",
        "game_context": "WSH 4, NYM 5 | Final",
        "game_status": "Final",
        "performance_grade": "\U0001f610 Routine",
        "social_search_url": 'https://x.com/search?q=%22Dylan%20Crews%22%20Nationals&f=live',
        "is_client": False,
        "tags": {
            "draft_class": "2023",
            "position": "Hitter",
            "roster_priority": 2,
        },
    },
]


# =========== WINDOW TEST DATA ===========
# Test data for 7D/30D/Season views with various grades

def make_window_entry(name, team, level, is_client, position, priority, window, grade, stats, games):
    """Helper to create window test entries."""
    return {
        "player_name": name,
        "team": team,
        "level": level,
        "is_client": is_client,
        "tags": {
            "position": position,
            "draft_class": "N/A" if level == "Pro" else "2026",
            "roster_priority": priority,
        },
        "window": window,
        "window_grade": grade,
        "stats": stats,
        "games_played": games,
        "last_updated": datetime.utcnow().isoformat() + "Z",
    }


def generate_window_data(window):
    """Generate test data for a specific time window."""
    return [
        # Hot hitter (Pro, Client)
        make_window_entry(
            "Dax Kilby", "New York Yankees", "Pro", True, "Hitter", 1, window,
            "🔥 Hot",
            {"pa": 28, "ab": 25, "h": 12, "hr": 4, "avg": ".480", "obp": ".536", "slg": ".920", "ops": "1.456"},
            7 if window == "7d" else (25 if window == "30d" else 45)
        ),
        # Solid hitter (Pro, Client)
        make_window_entry(
            "Kellon Lindsey", "Los Angeles Dodgers", "Pro", True, "Hitter", 1, window,
            "✅ Solid",
            {"pa": 30, "ab": 27, "h": 9, "hr": 1, "avg": ".333", "obp": ".400", "slg": ".481", "ops": ".881"},
            7 if window == "7d" else (28 if window == "30d" else 50)
        ),
        # Quiet hitter (Pro, Client)
        make_window_entry(
            "Sterlin Thompson", "Colorado Rockies", "Pro", True, "Hitter", 2, window,
            "😐 Quiet",
            {"pa": 25, "ab": 23, "h": 5, "hr": 0, "avg": ".217", "obp": ".280", "slg": ".261", "ops": ".541"},
            6 if window == "7d" else (22 if window == "30d" else 40)
        ),
        # Cold hitter (Pro, Client)
        make_window_entry(
            "Cade Doughty", "Toronto Blue Jays", "Pro", True, "Hitter", 2, window,
            "🥶 Cold",
            {"pa": 22, "ab": 20, "h": 3, "hr": 0, "avg": ".150", "obp": ".227", "slg": ".150", "ops": ".377"},
            5 if window == "7d" else (20 if window == "30d" else 38)
        ),
        # Hot pitcher (Pro, Client)
        make_window_entry(
            "Garrett Whitlock", "Boston Red Sox", "Pro", True, "Pitcher", 1, window,
            "🔥 Hot",
            {"ip": "14.0", "k": 18, "bb": 2, "era": "1.29", "whip": "0.79"},
            2 if window == "7d" else (5 if window == "30d" else 12)
        ),
        # Solid pitcher (Pro, Client)
        make_window_entry(
            "Aaron Watson", "Cincinnati Reds", "Pro", True, "Pitcher", 2, window,
            "✅ Solid",
            {"ip": "12.1", "k": 14, "bb": 4, "era": "2.92", "whip": "1.14"},
            2 if window == "7d" else (4 if window == "30d" else 10)
        ),
        # Cold pitcher (Pro, Client)
        make_window_entry(
            "Tanner Gordon", "Colorado Rockies", "Pro", True, "Pitcher", 2, window,
            "🥶 Cold",
            {"ip": "8.2", "k": 6, "bb": 5, "era": "6.23", "whip": "1.85"},
            2 if window == "7d" else (4 if window == "30d" else 8)
        ),
        # NCAA hitter (Client)
        make_window_entry(
            "Kyle Jones", "Florida", "NCAA", True, "Hitter", 1, window,
            "🔥 Hot",
            {"pa": 32, "ab": 28, "h": 14, "hr": 3, "avg": ".500", "obp": ".563", "slg": ".857", "ops": "1.420"},
            8 if window == "7d" else (30 if window == "30d" else 55)
        ),
        # NCAA pitcher (Client)
        make_window_entry(
            "Cam Flukey", "Coastal Carolina", "NCAA", True, "Pitcher", 1, window,
            "✅ Solid",
            {"ip": "10.0", "k": 12, "bb": 3, "era": "2.70", "whip": "1.10"},
            3 if window == "7d" else (8 if window == "30d" else 15)
        ),
        # Following (recruit) - Hot
        make_window_entry(
            "Chase Burns", "Tennessee", "NCAA", False, "Pitcher", 1, window,
            "🔥 Hot",
            {"ip": "16.0", "k": 24, "bb": 3, "era": "0.56", "whip": "0.56"},
            2 if window == "7d" else (6 if window == "30d" else 14)
        ),
        # Following (recruit) - Solid
        make_window_entry(
            "Jac Caglianone", "Florida", "NCAA", False, "Hitter", 1, window,
            "✅ Solid",
            {"pa": 35, "ab": 30, "h": 11, "hr": 5, "avg": ".367", "obp": ".457", "slg": ".767", "ops": "1.224"},
            9 if window == "7d" else (32 if window == "30d" else 58)
        ),
        # Insufficient data example
        make_window_entry(
            "Aiden Robbins", "Texas", "NCAA", True, "Hitter", 1, window,
            "— Insufficient",
            {"pa": "--", "ab": "--", "h": "--", "hr": "--", "avg": "--", "obp": "--", "slg": "--", "ops": "--"},
            2 if window == "7d" else (8 if window == "30d" else 15)
        ),
    ]


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    # Write today's pulse data
    with open(OUTPUT_PATH, "w") as f:
        json.dump(TEST_PULSE, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(TEST_PULSE)} test entries to {OUTPUT_PATH}")

    # Write window data
    for window, path in [("7d", WINDOW_7D_PATH), ("30d", WINDOW_30D_PATH), ("season", WINDOW_SEASON_PATH)]:
        data = generate_window_data(window)
        with open(path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Wrote {len(data)} test entries to {path}")


if __name__ == "__main__":
    main()
