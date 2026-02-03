"""
SV Dugout Pulse — Test Data Generator

Generates a realistic current_pulse.json with fake game data
covering every performance grade tier so the dashboard UI can be
tested before the season starts.

Usage:
    python generate_test_data.py
"""

import json
import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "data", "current_pulse.json")

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


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(TEST_PULSE, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(TEST_PULSE)} test entries to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
