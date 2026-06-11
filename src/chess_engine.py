"""
Chess engine for move evaluation and generation
"""

import chess
import chess.engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChessEngine:
    """Chess engine for move evaluation and best move selection"""

    def __init__(self, engine_path: str = None):
        self.engine_path = engine_path
        self.engine = None
        self.setup_engine()

    def setup_engine(self) -> None:
        """Setup the chess engine"""
        try:
            if self.engine_path:
                self.engine = chess.engine.SimpleEngine.popen_engine(self.engine_path)
            else:
                self.engine = chess.engine.SimpleEngine()
            logger.info("Chess engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize chess engine: {e}")
            self.engine = None

    def get_best_move(self, fen: str, is_white: bool, time_limit: float = 1.0) -> Optional[str]:
        """
        Get the best move for the current position

        Args:
            fen: FEN string of the current position
            is_white: Whether it's white's turn
            time_limit: Time limit for search in seconds

        Returns:
            Best move as UCI string, or None if no move found
        """
        if not self.engine:
            logger.error("Chess engine not available")
            return None

        try:
            board = chess.Board(fen)
            result = self.engine.play(board, chess.engine.Limit(time=time_limit))
            return result.move.uci()
        except Exception as e:
            logger.error(f"Error getting best move: {e}")
            return None

    def evaluate_position(self, fen: str) -> float:
        """
        Evaluate the current position

        Args:
            fen: FEN string of the current position

        Returns:
            Evaluation score (positive for white, negative for black)
        """
        if not self.engine:
            logger.error("Chess engine not available")
            return 0.0

        try:
            board = chess.Board(fen)
            result = self.engine.analyse(board, chess.engine.Limit(time=0.5))
            return result.get("score", chess.engine.Mate(0)).score()
        except Exception as e:
            logger.error(f"Error evaluating position: {e}")
            return 0.0

    def __del__(self):
        """Cleanup engine resources"""
        if self.engine:
            self.engine.quit()
