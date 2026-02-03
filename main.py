"""
SV Dugout Pulse — Main Orchestrator

Usage:
    python main.py            # Live mode (fetches roster + stats)
    python main.py --mock     # Load test data only (no API calls)
"""

import argparse
import json
import logging
import os
import sys

from src.alerts import check_and_send_alerts, reset_sent_alerts
from src.config import OUTPUT_PATH, ROSTER_URL
from src.performance_analyzer import PerformanceAnalyzer
from src.roster_manager import get_all_players
from src.stats_engine import StatsFetcher

logger = logging.getLogger("pulse")


def build_pulse_entry(player: dict, stats: dict, analysis: dict) -> dict:
    """Assemble a single player's output record."""
    return {
        "player_name": player["player_name"],
        "team": player["team"],
        "level": player["level"],
        "stats_summary": stats.get("stats_summary", "No game data"),
        "game_context": stats.get("game_context", ""),
        "game_status": stats.get("game_status", "N/A"),
        "performance_grade": analysis["performance_grade"],
        "social_search_url": analysis["social_search_url"],
        "is_client": player.get("is_client", True),
        "tags": {
            "draft_class": player.get("draft_class", ""),
            "position": player.get("position", ""),
            "roster_priority": player.get("roster_priority", 99),
        },
    }


def run_live():
    """Full pipeline: fetch roster + recruits -> fetch stats -> grade -> alert -> write JSON."""
    logger.info("Starting live pulse run")

    # Reset alert tracking for this run
    reset_sent_alerts()

    # 1. Roster (clients + recruits)
    all_players = get_all_players()
    if not all_players:
        logger.error("No players found — aborting")
        sys.exit(1)

    clients = [p for p in all_players if p.get("is_client")]
    recruits = [p for p in all_players if not p.get("is_client")]
    logger.info("Loaded %d clients + %d recruits", len(clients), len(recruits))

    # 2. Stats + Analysis + Alerts
    fetcher = StatsFetcher()
    analyzer = PerformanceAnalyzer()
    pulse = []

    for player in all_players:
        name = player["player_name"]
        is_client = player.get("is_client", True)
        try:
            stats = fetcher.fetch(player)
            analysis = analyzer.analyze(player, stats)
            entry = build_pulse_entry(player, stats, analysis)
            pulse.append(entry)

            # Only send Slack alerts for clients, not recruits
            if is_client:
                check_and_send_alerts(player, stats)

            logger.info(
                "%s%s | %s | %s",
                name,
                "" if is_client else " [following]",
                stats.get("stats_summary", "—"),
                analysis["performance_grade"],
            )
        except Exception:
            logger.exception("Failed to process %s — skipping", name)
            continue

    # 3. Write output
    write_output(pulse)


def run_mock():
    """Load pre-generated test data (from generate_test_data.py)."""
    logger.info("Running in --mock mode")

    if not os.path.exists(OUTPUT_PATH):
        logger.error(
            "No test data found at %s — run generate_test_data.py first", OUTPUT_PATH
        )
        sys.exit(1)

    with open(OUTPUT_PATH) as f:
        pulse = json.load(f)

    logger.info("Loaded %d mock entries from %s", len(pulse), OUTPUT_PATH)
    # In mock mode we just validate the file exists and is loadable.
    # The dashboard reads data/current_pulse.json either way.
    print(f"Mock pulse loaded: {len(pulse)} players")
    for entry in pulse:
        print(
            f"  {entry['performance_grade']:15s} | {entry['player_name']:25s} | {entry['stats_summary']}"
        )


def write_output(pulse: list[dict]):
    """Write the pulse list to data/current_pulse.json."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(pulse, f, indent=2, ensure_ascii=False)
    logger.info("Wrote %d entries to %s", len(pulse), OUTPUT_PATH)


def main():
    parser = argparse.ArgumentParser(description="SV Dugout Pulse")
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use pre-generated test data instead of live APIs",
    )
    args = parser.parse_args()

    if args.mock:
        run_mock()
    else:
        run_live()


if __name__ == "__main__":
    main()
