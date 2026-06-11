"""
Chess.com Selfbot for playing at 3200 rating
"""

import asyncio
import logging
from typing import Optional

from .api_client import ChessAPIClient
from .chess_engine import ChessEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChessBot:
    """Main chess bot class that plays games on chess.com"""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.api_client = ChessAPIClient(username, password)
        self.chess_engine = ChessEngine()
        self.current_game_id: Optional[str] = None
        self.is_playing = False

    async def login(self) -> bool:
        """Login to chess.com"""
        return await self.api_client.login()

    async def find_game(self, min_rating: int = 3000, max_rating: int = 3400) -> Optional[str]:
        """Find a game within the specified rating range"""
        game_id = await self.api_client.find_game(min_rating, max_rating)
        if game_id:
            self.current_game_id = game_id
            self.is_playing = True
        return game_id

    async def make_move(self, game_id: str, move: str) -> bool:
        """Make a move in the current game"""
        return await self.api_client.make_move(game_id, move)

    async def play_game(self) -> None:
        """Play a single game"""
        if not await self.login():
            logger.error("Failed to login")
            return

        logger.info("Logged in successfully")

        while self.is_playing:
            game_id = await self.find_game()
            if not game_id:
                logger.info("No game found, waiting...")
                await asyncio.sleep(5)
                continue

            logger.info(f"Found game: {game_id}")
            await self.play_single_game(game_id)

    async def play_single_game(self, game_id: str) -> None:
        """Play a single game to completion"""
        while True:
            game_state = await self.api_client.get_game_state(game_id)
            if not game_state or game_state.get("status") == "finished":
                break

            if game_state.get("my_color") == "white":
                move = self.chess_engine.get_best_move(
                    game_state.get("fen", ""),
                    is_white=True
                )
            else:
                move = self.chess_engine.get_best_move(
                    game_state.get("fen", ""),
                    is_white=False
                )

            if move:
                success = await self.make_move(game_id, move)
                if not success:
                    logger.error(f"Failed to make move: {move}")
                    break
                logger.info(f"Made move: {move}")
            else:
                logger.warning("No move suggested")
                break

    async def start(self) -> None:
        """Start the bot"""
        logger.info("Starting chess bot")
        await self.play_game()
