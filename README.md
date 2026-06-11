# Chess Bot Project

This project creates a selfbot that plays chess at 3200 rating against other bots on chess.com.

## Project Structure

```
chess-bot/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── api_client.py
│   └── chess_engine.py
├── tests/
│   ├── test_main.py
├── README.md
├── requirements.txt
├── example.py
└── .gitignore
```

## How to Upload to GitHub

1. **Create a GitHub repository**
   - Go to [GitHub](https://github.com)
   - Click "New repository"
   - Give it a name (e.g., "chess-bot")
   - Choose visibility (public/private)
   - Do NOT initialize with README (we'll add it)

2. **Push your code**
   ```bash
   # From your local machine (not in the PowerShell environment)
   cd chess-bot
   git init
   git add .
   git commit -m "Initial commit: Chess.com selfbot for playing at 3200 rating"
   git remote add origin https://github.com/your-username/chess-bot.git
   git push -u origin master
   ```

## Project Features

- **Login System**: Authenticates with chess.com using username/password
- **Game Finding**: Searches for games within rating range (3000-3400)
- **Chess Engine**: Uses python-chess library to evaluate positions and find best moves
- **Move Execution**: Makes moves in games
- **Game Loop**: Continuously plays games to maintain rating

## Requirements

- Python 3.7+
- python-chess>=1.9.0
- aiohttp>=3.8.0

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from src.main import ChessBot

async def main():
    bot = ChessBot("your_username", "your_password")
    await bot.start()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Notes

- This bot is for educational purposes only
- Please respect chess.com's terms of service
- Consider using rate limiting to avoid being blocked
- The 3200 rating target may require tuning of the chess engine parameters

## Author

Created by Satyam
