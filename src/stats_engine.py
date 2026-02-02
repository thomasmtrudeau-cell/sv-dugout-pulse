"""
SV Dugout Pulse — Stats Engine

Two ecosystems:
  1. Pro (MLB/MiLB) — via the MLB-StatsAPI library
  2. NCAA — fault-tolerant framework with pluggable school scrapers
"""

from __future__ import annotations

import abc
import logging
from datetime import date
from typing import Optional

import requests
import statsapi
from bs4 import BeautifulSoup

from .config import ROSTER_URL

logger = logging.getLogger(__name__)


# ===== Shared data structures =====

def empty_stats() -> dict:
    """Return a blank stats dict (no data available)."""
    return {
        "stats_summary": "No game data",
        "game_context": "",
        "game_status": "N/A",
        "is_pitcher_line": False,
        # Raw fields used by the analyzer
        "hits": 0,
        "at_bats": 0,
        "home_runs": 0,
        "rbi": 0,
        "runs": 0,
        "stolen_bases": 0,
        "ip": 0.0,
        "earned_runs": 0,
        "strikeouts": 0,
        "walks_allowed": 0,
        "hits_allowed": 0,
        "saves": 0,
        "win": False,
        "loss": False,
        "quality_start": False,
        "is_debut": False,
        "milestone_label": None,
    }


# =========================================================================
# PRO (MLB / MiLB)
# =========================================================================

# Map common org display names to the franchise search names used by statsapi
TEAM_NAME_MAP = {
    "Athletics": "Oakland Athletics",
    "Unsigned": None,
}


class ProStatsFetcher:
    """Fetch game/stats data for MLB and MiLB players via MLB-StatsAPI."""

    def __init__(self):
        self._games_cache: dict[str, list] = {}
        self._today = date.today().strftime("%m/%d/%Y")

    # ----- public API -----

    def fetch(self, player: dict) -> dict:
        """
        Given a normalized player dict, attempt to find today's game
        and return a stats dict.
        """
        team = player.get("team", "")
        name = player.get("player_name", "")

        if not team or team == "Unsigned":
            logger.debug("Skipping %s — unsigned / no team", name)
            return empty_stats()

        try:
            player_id = self._lookup_player(name)
            if player_id is None:
                logger.info("Player not found in MLB lookup: %s", name)
                return empty_stats()

            game = self._find_todays_game(player_id)
            if game is None:
                logger.debug("No game today for %s", name)
                return empty_stats()

            return self._extract_stats(player, player_id, game)

        except Exception:
            logger.exception("Error fetching pro stats for %s", name)
            return empty_stats()

    # ----- internal helpers -----

    def _lookup_player(self, name: str) -> Optional[int]:
        """Search MLB for a player ID by name."""
        try:
            results = statsapi.lookup_player(name)
            if results:
                return results[0]["id"]
        except Exception:
            logger.exception("MLB player lookup failed for %s", name)
        return None

    def _find_todays_game(self, player_id: int) -> Optional[dict]:
        """Find a game today that involves the player's team."""
        try:
            schedule = statsapi.schedule(date=self._today)
            # Check if the player is in any of today's games
            for game in schedule:
                boxscore = statsapi.boxscore_data(game["game_id"])
                # Search both teams' rosters
                for side in ("home", "away"):
                    players = boxscore.get(f"{side}Batters", []) + boxscore.get(
                        f"{side}Pitchers", []
                    )
                    if player_id in players:
                        return {
                            "game_id": game["game_id"],
                            "boxscore": boxscore,
                            "schedule": game,
                            "side": side,
                        }
        except Exception:
            logger.exception("Error searching today's games for player %d", player_id)
        return None

    def _extract_stats(self, player: dict, player_id: int, game: dict) -> dict:
        """Pull the player's line from the boxscore."""
        result = empty_stats()
        sched = game["schedule"]
        box = game["boxscore"]

        # Game context
        status = sched.get("status", "Unknown")
        home = sched.get("home_name", "")
        away = sched.get("away_name", "")
        home_score = sched.get("home_score", 0)
        away_score = sched.get("away_score", 0)
        inning = sched.get("current_inning", "")

        if status == "Final":
            result["game_context"] = f"{away} {away_score}, {home} {home_score} | Final"
            result["game_status"] = "Final"
        elif status in ("In Progress", "Live"):
            half = sched.get("inning_state", "")
            result["game_context"] = (
                f"{away} {away_score}, {home} {home_score} | {half} {inning}"
            )
            result["game_status"] = "Live"
        else:
            result["game_context"] = f"{away} vs {home} | {status}"
            result["game_status"] = status

        # Find the player's stats line in the boxscore
        pid_str = f"ID{player_id}"
        position = player.get("position", "Hitter")

        if position == "Pitcher":
            result["is_pitcher_line"] = True
            pitchers = box.get(f"{game['side']}Pitchers", [])
            for entry in pitchers:
                if isinstance(entry, dict) and str(player_id) in str(
                    entry.get("personId", "")
                ):
                    result.update(self._parse_pitcher_line(entry))
                    break
        else:
            batters = box.get(f"{game['side']}Batters", [])
            for entry in batters:
                if isinstance(entry, dict) and str(player_id) in str(
                    entry.get("personId", "")
                ):
                    result.update(self._parse_batter_line(entry))
                    break

        return result

    @staticmethod
    def _parse_batter_line(entry: dict) -> dict:
        """Parse a batter's boxscore entry into our stats dict."""
        stats = entry.get("stats", {})
        h = int(stats.get("hits", 0))
        ab = int(stats.get("atBats", 0))
        hr = int(stats.get("homeRuns", 0))
        rbi = int(stats.get("rbi", 0))
        r = int(stats.get("runs", 0))
        sb = int(stats.get("stolenBases", 0))

        parts = [f"{h}-{ab}"]
        if hr:
            parts.append(f"{hr} HR" if hr > 1 else "HR")
        if rbi:
            parts.append(f"{rbi} RBI")
        if r:
            parts.append(f"{r} R")
        if sb:
            parts.append(f"{sb} SB")

        return {
            "stats_summary": ", ".join(parts),
            "hits": h,
            "at_bats": ab,
            "home_runs": hr,
            "rbi": rbi,
            "runs": r,
            "stolen_bases": sb,
        }

    @staticmethod
    def _parse_pitcher_line(entry: dict) -> dict:
        """Parse a pitcher's boxscore entry into our stats dict."""
        stats = entry.get("stats", {})
        ip_str = stats.get("inningsPitched", "0")
        ip = float(ip_str) if ip_str else 0.0
        er = int(stats.get("earnedRuns", 0))
        k = int(stats.get("strikeOuts", 0))
        bb = int(stats.get("baseOnBalls", 0))
        ha = int(stats.get("hits", 0))
        sv = int(stats.get("saves", 0))
        w = stats.get("wins", 0)
        l = stats.get("losses", 0)

        parts = [f"{ip_str} IP"]
        if ha:
            parts.append(f"{ha} H")
        if er:
            parts.append(f"{er} ER")
        parts.append(f"{k} K")
        if bb:
            parts.append(f"{bb} BB")
        if sv:
            parts.append("SV")
        if w:
            parts.append("W")
        if l:
            parts.append("L")

        qs = ip >= 6.0 and er <= 3

        return {
            "stats_summary": ", ".join(parts),
            "is_pitcher_line": True,
            "ip": ip,
            "earned_runs": er,
            "strikeouts": k,
            "walks_allowed": bb,
            "hits_allowed": ha,
            "saves": sv,
            "win": bool(w),
            "loss": bool(l),
            "quality_start": qs,
        }


# =========================================================================
# NCAA — Fault-Tolerant Framework
# =========================================================================


class BaseSchoolScraper(abc.ABC):
    """
    Base class for school-specific NCAA stat scrapers.
    Subclass this and register in SCHOOL_SCRAPERS to add support for a school.
    """

    @abc.abstractmethod
    def fetch_stats(self, player_name: str, team: str) -> Optional[dict]:
        """
        Return a stats dict for the player, or None if unavailable.
        Must not raise — catch and log internally.
        """
        ...


class SidearmScraper(BaseSchoolScraper):
    """
    Scraper for schools using the Sidearm Sports platform.
    Many D1 programs use this (e.g., Florida, Texas, Alabama).
    """

    # Override per school — map school name to its Sidearm base URL
    SIDEARM_URLS: dict[str, str] = {
        # "Florida": "https://floridagators.com/sports/baseball/stats",
        # Add URLs as you discover them
    }

    def fetch_stats(self, player_name: str, team: str) -> Optional[dict]:
        base_url = self.SIDEARM_URLS.get(team)
        if not base_url:
            logger.debug("No Sidearm URL configured for %s", team)
            return None

        try:
            # Sidearm exposes a JSON schedule/stats feed at predictable paths
            resp = requests.get(f"{base_url}?format=json", timeout=15)
            resp.raise_for_status()
            data = resp.json()
            return self._find_player_in_feed(player_name, data)
        except Exception:
            logger.info("Sidearm fetch failed for %s @ %s", player_name, team)
            return None

    def _find_player_in_feed(self, player_name: str, data: dict) -> Optional[dict]:
        """Parse the Sidearm JSON feed for a specific player. Override as needed."""
        # Sidearm feed structures vary — this is a starting point
        logger.debug("Sidearm feed parsing not yet implemented for this school")
        return None


class StatBroadcastScraper(BaseSchoolScraper):
    """
    Scraper for schools using the StatBroadcast live stats platform.
    """

    STATBROADCAST_URLS: dict[str, str] = {
        # "Coastal Carolina": "https://statbroadcast.com/events/statmonitr.php?gid=ccu",
        # Add URLs as you discover them
    }

    def fetch_stats(self, player_name: str, team: str) -> Optional[dict]:
        url = self.STATBROADCAST_URLS.get(team)
        if not url:
            logger.debug("No StatBroadcast URL configured for %s", team)
            return None

        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            return self._parse_statbroadcast(player_name, resp.text)
        except Exception:
            logger.info("StatBroadcast fetch failed for %s @ %s", player_name, team)
            return None

    def _parse_statbroadcast(self, player_name: str, html: str) -> Optional[dict]:
        logger.debug("StatBroadcast parsing not yet implemented")
        return None


class NCAAOrgScraper(BaseSchoolScraper):
    """
    Fallback scraper: stats.ncaa.org box scores.
    This is the least reliable but widest-coverage option.
    """

    BASE_URL = "https://stats.ncaa.org"

    def fetch_stats(self, player_name: str, team: str) -> Optional[dict]:
        try:
            # stats.ncaa.org requires team lookup -> schedule -> boxscore
            # This is a structural placeholder — the site changes frequently
            logger.info(
                "NCAA.org scraper called for %s @ %s — not yet fully implemented",
                player_name,
                team,
            )
            return None
        except Exception:
            logger.info("NCAA.org fetch failed for %s @ %s", player_name, team)
            return None


class NCAAStatsFetcher:
    """
    Fault-tolerant NCAA stats fetcher.
    Tries registered school scrapers in order, falls back gracefully.
    """

    def __init__(self):
        self._sidearm = SidearmScraper()
        self._statbroadcast = StatBroadcastScraper()
        self._ncaa_org = NCAAOrgScraper()

        # Registry: school name -> list of scrapers to try in order.
        # Add school-specific overrides here.
        self._school_scrapers: dict[str, list[BaseSchoolScraper]] = {
            # Example:
            # "Coastal Carolina": [self._statbroadcast, self._ncaa_org],
        }

        # Default fallback chain for schools without a specific entry
        self._default_chain: list[BaseSchoolScraper] = [
            self._sidearm,
            self._statbroadcast,
            self._ncaa_org,
        ]

    def fetch(self, player: dict) -> dict:
        """
        Attempt to fetch stats for an NCAA player.
        Tries school-specific scrapers first, then the default chain.
        Never raises — returns empty_stats() on total failure.
        """
        name = player.get("player_name", "")
        team = player.get("team", "")

        scrapers = self._school_scrapers.get(team, self._default_chain)

        for scraper in scrapers:
            try:
                result = scraper.fetch_stats(name, team)
                if result is not None:
                    return result
            except Exception:
                logger.exception(
                    "Scraper %s crashed for %s @ %s",
                    scraper.__class__.__name__,
                    name,
                    team,
                )
                continue

        logger.info("No NCAA stats found for %s @ %s", name, team)
        return empty_stats()


# =========================================================================
# Unified fetcher
# =========================================================================


class StatsFetcher:
    """
    Unified interface: routes a player to the correct fetcher based on level.
    """

    def __init__(self):
        self.pro = ProStatsFetcher()
        self.ncaa = NCAAStatsFetcher()

    def fetch(self, player: dict) -> dict:
        level = player.get("level", "")
        if level == "Pro":
            return self.pro.fetch(player)
        elif level == "NCAA":
            return self.ncaa.fetch(player)
        else:
            logger.warning("Unknown level '%s' for %s", level, player.get("player_name"))
            return empty_stats()
