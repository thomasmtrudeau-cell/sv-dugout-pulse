"""
SV Dugout Pulse — Slack Alerts

Sends notifications to Slack when trigger conditions are met.
"""

import json
import logging
import os
from typing import Optional

import requests

logger = logging.getLogger(__name__)

# Webhook URL — set via environment variable or replace default
SLACK_WEBHOOK_URL = os.environ.get(
    "SLACK_WEBHOOK_URL",
    "https://hooks.slack.com/services/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",
)

# Track alerts already sent this run to avoid duplicates
_sent_alerts: set[str] = set()


def send_slack_message(text: str, blocks: Optional[list] = None) -> bool:
    """Send a message to the configured Slack webhook."""
    if not SLACK_WEBHOOK_URL or "YOUR_WEBHOOK" in SLACK_WEBHOOK_URL:
        logger.warning("Slack webhook not configured — skipping alert")
        return False

    payload = {"text": text}
    if blocks:
        payload["blocks"] = blocks

    try:
        resp = requests.post(
            SLACK_WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        if resp.status_code == 200:
            logger.info("Slack alert sent: %s", text[:50])
            return True
        else:
            logger.error("Slack webhook failed: %s %s", resp.status_code, resp.text)
            return False
    except Exception:
        logger.exception("Failed to send Slack alert")
        return False


def _alert_key(player_name: str, alert_type: str) -> str:
    """Generate a unique key to track sent alerts."""
    return f"{player_name}:{alert_type}"


def _already_sent(player_name: str, alert_type: str) -> bool:
    """Check if this alert was already sent this run."""
    return _alert_key(player_name, alert_type) in _sent_alerts


def _mark_sent(player_name: str, alert_type: str):
    """Mark an alert as sent."""
    _sent_alerts.add(_alert_key(player_name, alert_type))


def check_and_send_alerts(player: dict, stats: dict):
    """
    Check if the player's stats trigger any alert conditions.
    Sends Slack notifications for:
    - Any player hits a home run (any tier)
    - Any pitcher enters the game (any tier)
    - Any pitcher gets 5+ Ks (any tier)
    - T1/T2 hitter reaches base 3+ times
    """
    name = player.get("player_name", "Unknown")
    team = player.get("team", "")
    tier = player.get("roster_priority", 99)
    position = player.get("position", "Hitter")
    game_context = stats.get("game_context", "")
    game_status = stats.get("game_status", "N/A")

    # Skip if no game data
    if game_status == "N/A":
        return

    tier_label = f"T{tier}" if tier <= 4 else "T?"

    # --- Alert: Home Run (any player, any tier) ---
    hr = stats.get("home_runs", 0)
    if hr > 0 and not _already_sent(name, "hr"):
        hr_text = f"{hr} HRs" if hr > 1 else "a HR"
        send_slack_message(
            f"⚾ *{name}* ({tier_label}) just hit {hr_text}!\n"
            f"_{team}_ — {game_context}"
        )
        _mark_sent(name, "hr")

    # --- Alert: Pitcher enters game (any pitcher, any tier) ---
    is_pitching = stats.get("is_pitcher_line", False) or position == "Pitcher"
    ip = stats.get("ip", 0.0)

    if is_pitching and ip > 0 and not _already_sent(name, "entered"):
        # Only alert once when they first appear (IP > 0)
        send_slack_message(
            f"🔥 *{name}* ({tier_label}) is pitching!\n"
            f"_{team}_ — {game_context}"
        )
        _mark_sent(name, "entered")

    # --- Alert: Pitcher 5+ strikeouts (any pitcher, any tier) ---
    strikeouts = stats.get("strikeouts", 0)
    if is_pitching and strikeouts >= 5 and not _already_sent(name, "5k"):
        send_slack_message(
            f"🎯 *{name}* ({tier_label}) has {strikeouts} K's!\n"
            f"_{team}_ — {game_context}"
        )
        _mark_sent(name, "5k")

    # --- Alert: T1/T2 hitter reaches base 3+ times ---
    if tier <= 2 and position in ("Hitter", "Two-Way") and not stats.get("is_pitcher_line"):
        hits = stats.get("hits", 0)
        # Estimate times on base: hits + walks (walks not always available, so approximate)
        # For now, use hits + rough estimate. If we had BB data we'd add it.
        # Using 3+ hits as proxy for "reached base 3+ times"
        walks = stats.get("walks", 0)  # May not be populated
        times_on_base = hits + walks

        # If walks aren't tracked, check if 3+ hits as a conservative proxy
        if times_on_base >= 3 or hits >= 3:
            if not _already_sent(name, "3ob"):
                send_slack_message(
                    f"💪 *{name}* ({tier_label}) has reached base {times_on_base if times_on_base >= 3 else hits}+ times!\n"
                    f"_{team}_ — {stats.get('stats_summary', '')} — {game_context}"
                )
                _mark_sent(name, "3ob")


def reset_sent_alerts():
    """Clear the sent alerts tracker (call at start of each run)."""
    _sent_alerts.clear()
