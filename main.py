"""
SV Dugout Pulse — Main Orchestrator

Usage:
    python main.py                # Live mode (fetches roster + today's stats)
    python main.py --mock         # Load test data only (no API calls)
    python main.py --historical   # Aggregate historical stats (7D/30D/Season)
"""

import argparse
import json
import logging
import os
import sys

from src.alerts import check_and_send_alerts, reset_sent_alerts
from src.config import (
    OUTPUT_PATH,
    ROSTER_URL,
    WINDOW_7D_PATH,
    WINDOW_30D_PATH,
    WINDOW_SEASON_PATH,
)
from src.historical_stats import WindowStatsAggregator, write_window_json
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
        "game_time": stats.get("game_time"),
        "next_game": stats.get("next_game"),
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


def run_historical():
    """Aggregate historical stats for all time windows (7D/30D/Season)."""
    logger.info("Starting historical stats aggregation")

    # 1. Fetch roster
    all_players = get_all_players()
    if not all_players:
        logger.error("No players found — aborting")
        sys.exit(1)

    logger.info("Loaded %d total players for historical aggregation", len(all_players))

    # 2. Aggregate stats across all windows
    aggregator = WindowStatsAggregator()
    window_data = aggregator.run_all_windows(all_players)

    # 3. Write separate JSON files
    write_window_json(window_data["7d"], WINDOW_7D_PATH)
    write_window_json(window_data["30d"], WINDOW_30D_PATH)
    write_window_json(window_data["season"], WINDOW_SEASON_PATH)

    logger.info(
        "Historical aggregation complete: 7D=%d, 30D=%d, Season=%d",
        len(window_data["7d"]),
        len(window_data["30d"]),
        len(window_data["season"]),
    )


def main():
    parser = argparse.ArgumentParser(description="SV Dugout Pulse")
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use pre-generated test data instead of live APIs",
    )
    parser.add_argument(
        "--historical",
        action="store_true",
        help="Aggregate historical stats (7D/30D/Season) instead of live stats",
    )
    args = parser.parse_args()

    if args.mock:
        run_mock()
    elif args.historical:
        run_historical()
    else:
        run_live()


if __name__ == "__main__":
    main()
