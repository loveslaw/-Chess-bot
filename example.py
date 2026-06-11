"""
Example usage of the chess bot
"""
import asyncio
from src.main import ChessBot


async def main():
    """Example usage of the chess bot"""
    # Replace with your chess.com credentials
    username = "your_username"
    password = "your_password"

    bot = ChessBot(username, password)
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
