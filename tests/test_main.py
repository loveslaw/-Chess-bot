"""
Tests for the chess bot
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from src.main import ChessBot
from src.chess_engine import ChessEngine
from src.api_client import ChessAPIClient


class TestChessEngine:
    """Test the chess engine"""

    def test_init(self):
        """Test engine initialization"""
        engine = ChessEngine()
        assert engine is not None

    def test_get_best_move_without_engine(self):
        """Test getting best move without engine"""
        engine = ChessEngine()
        engine.engine = None
        move = engine.get_best_move("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", True)
        assert move is None

    @patch('chess.engine.SimpleEngine')
    def test_get_best_move_with_mock(self, mock_engine):
        """Test getting best move with mocked engine"""
        mock_instance = MagicMock()
        mock_result = MagicMock()
        mock_move = MagicMock()
        mock_move.uci.return_value = "e2e4"
        mock_result.move = mock_move
        mock_instance.play.return_value = mock_result

        mock_engine.return_value = mock_instance

        engine = ChessEngine()
        move = engine.get_best_move("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", True)
        assert move == "e2e4"


class TestChessAPIClient:
    """Test the API client"""

    @pytest.mark.asyncio
    async def test_login_success(self):
        """Test successful login"""
        with patch('aiohttp.ClientSession') as mock_session:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_session.return_value.get.return_value.__aenter__.return_value = mock_response
            mock_session.return_value.post.return_value.__aenter__.return_value = mock_response

            client = ChessAPIClient("test_user", "test_pass")
            result = await client.login()
            assert result is True

    @pytest.mark.asyncio
    async def test_login_failure(self):
        """Test failed login"""
        with patch('aiohttp.ClientSession') as mock_session:
            mock_response = AsyncMock()
            mock_response.status = 401
            mock_session.return_value.get.return_value.__aenter__.return_value = mock_response

            client = ChessAPIClient("test_user", "test_pass")
            result = await client.login()
            assert result is False

    @pytest.mark.asyncio
    async def test_find_game(self):
        """Test finding a game"""
        with patch('aiohttp.ClientSession') as mock_session:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_games_data = {
                "games": [
                    {"game_id": "game123", "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"}
                ]
            }
            mock_response.json.return_value = mock_games_data
            mock_session.return_value.get.return_value.__aenter__.return_value = mock_response

            client = ChessAPIClient("test_user", "test_pass")
            game_id = await client.find_game()
            assert game_id == "game123"

    @pytest.mark.asyncio
    async def test_make_move(self):
        """Test making a move"""
        with patch('aiohttp.ClientSession') as mock_session:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_session.return_value.post.return_value.__aenter__.return_value = mock_response

            client = ChessAPIClient("test_user", "test_pass")
            result = await client.make_move("game123", "e2e4")
            assert result is True

    @pytest.mark.asyncio
    async def test_get_game_state(self):
        """Test getting game state"""
        with patch('aiohttp.ClientSession') as mock_session:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_game_data = {
                "game_id": "game123",
                "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                "my_color": "white"
            }
            mock_response.json.return_value = mock_game_data
            mock_session.return_value.get.return_value.__aenter__.return_value = mock_response

            client = ChessAPIClient("test_user", "test_pass")
            game_state = await client.get_game_state("game123")
            assert game_state["game_id"] == "game123"
            assert game_state["my_color"] == "white"


class TestChessBot:
    """Test the main chess bot"""

    @pytest.mark.asyncio
    async def test_init(self):
        """Test bot initialization"""
        bot = ChessBot("test_user", "test_pass")
        assert bot.username == "test_user"
        assert bot.password == "test_pass"
        assert bot.current_game_id is None
        assert bot.is_playing is False

    @pytest.mark.asyncio
    async def test_login(self):
        """Test bot login"""
        with patch.object(ChessAPIClient, 'login', new_callable=AsyncMock) as mock_login:
            mock_login.return_value = True

            bot = ChessBot("test_user", "test_pass")
            result = await bot.login()
            assert result is True

    @pytest.mark.asyncio
    async def test_find_game(self):
        """Test finding a game"""
        with patch.object(ChessAPIClient, 'find_game', new_callable=AsyncMock) as mock_find:
            mock_find.return_value = "game123"

            bot = ChessBot("test_user", "test_pass")
            game_id = await bot.find_game()
            assert game_id == "game123"
            assert bot.current_game_id == "game123"
            assert bot.is_playing is True
