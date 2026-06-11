"""
Chess.com API client for interacting with chess.com
"""

import asyncio
import json
import logging
from typing import Optional, Dict, Any
import aiohttp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChessAPIClient:
    """Client for interacting with chess.com API"""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.base_url = "https://api.chess.com"
        self.session: Optional[aiohttp.ClientSession] = None
        self.cookies: Optional[Dict[str, str]] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def login(self) -> bool:
        """Login to chess.com"""
        if not self.session:
            self.session = aiohttp.ClientSession()

        try:
            # First, get the login page to get CSRF token
            login_page_url = f"{self.base_url}/account/login"
            async with self.session.get(login_page_url) as response:
                if response.status != 200:
                    logger.error(f"Failed to get login page: {response.status}")
                    return False

            # Try to login with username/password
            login_url = f"{self.base_url}/api/login"
            data = {
                "username": self.username,
                "password": self.password
            }

            async with self.session.post(login_url, json=data) as response:
                if response.status == 200:
                    self.cookies = dict(self.session.cookie_jar)
                    logger.info("Login successful")
                    return True
                else:
                    logger.error(f"Login failed: {response.status}")
                    return False

        except Exception as e:
            logger.error(f"Error during login: {e}")
            return False

    async def find_game(self, min_rating: int = 3000, max_rating: int = 3400) -> Optional[str]:
        """
        Find a game within the specified rating range

        Args:
            min_rating: Minimum rating of opponent
            max_rating: Maximum rating of opponent

        Returns:
            Game ID if found, None otherwise
        """
        try:
            # Get available games
            games_url = f"{self.base_url}/api/games"
            params = {
                "min_rating": min_rating,
                "max_rating": max_rating,
                "status": "awaiting_opponent"
            }

            async with self.session.get(games_url, params=params) as response:
                if response.status == 200:
                    games_data = await response.json()
                    if games_data.get("games"):
                        # Return the first available game
                        return games_data["games"][0]["game_id"]
                    else:
                        logger.info("No games available in rating range")
                        return None
                else:
                    logger.error(f"Failed to get games: {response.status}")
                    return None

        except Exception as e:
            logger.error(f"Error finding game: {e}")
            return None

    async def make_move(self, game_id: str, move: str) -> bool:
        """
        Make a move in a game

        Args:
            game_id: ID of the game
            move: Move in UCI format

        Returns:
            True if move was successful, False otherwise
        """
        try:
            move_url = f"{self.base_url}/api/games/{game_id}/move"
            data = {"move": move}

            async with self.session.post(move_url, json=data) as response:
                if response.status == 200:
                    logger.info(f"Move made successfully: {move}")
                    return True
                else:
                    logger.error(f"Failed to make move: {response.status}")
                    return False

        except Exception as e:
            logger.error(f"Error making move: {e}")
            return False

    async def get_game_state(self, game_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the current state of a game

        Args:
            game_id: ID of the game

        Returns:
            Game state dictionary, or None if failed
        """
        try:
            game_url = f"{self.base_url}/api/games/{game_id}"
            async with self.session.get(game_url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to get game state: {response.status}")
                    return None

        except Exception as e:
            logger.error(f"Error getting game state: {e}")
            return None

    async def get_player_stats(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Get player statistics

        Args:
            username: Username to get stats for

        Returns:
            Player stats dictionary, or None if failed
        """
        try:
            stats_url = f"{self.base_url}/api/player/{username}/stats"
            async with self.session.get(stats_url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to get player stats: {response.status}")
                    return None

        except Exception as e:
            logger.error(f"Error getting player stats: {e}")
            return None
