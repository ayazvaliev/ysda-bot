# Bebra Cinemabot

**Cinemabot** is a simple, low-latency asynchronius Telegram bot written on `aiogram` that responds to movie name requests by returning the poster, rating, description, and links where the movie can be watched. It tracks user activity and request history, enabling lightweight analytics and usage statistics via a local SQLite database.

## Features

- Responds to movie queries with:
  - Poster image
  - Rating
  - Description / synopsis
  - Links where the movie can be watched (via search)
- Persistent storage of requests and user activity using `sqlite3`
- Statistics and history per user
- Low-latency design: minimal hops, caching-friendly patterns, and graceful degradation on downstream failures
- Command-based interface in Telegram:
  - `/start` – initialize interaction with the bot
  - `/help` – list available commands and usage guidance
  - `/stats` – show aggregated statistics about the user’s activity
  - `/history` – retrieve the user’s past movie requests

## Architecture & Dependencies

- **Kinopoisk Dev API**: used to fetch movie metadata such as title, poster URL, rating, description, year, etc.
- **Google Search API**: used to search for URLs where the movie can be watched (streaming/availability links).
- **SQLite3**: local embedded database for:
  - Logging each user request
  - Storing timestamps, query terms, success/failure status
  - Aggregating statistics such as request count, most requested titles, error rates
- **Telegram Bot API**: interaction layer for receiving commands and replying to users.

## Installation / Testing

1. Clone the repository:

    ```bash
    git clone https://your.repo.url/cinemabot.git
    cd cinemabot
    ```

2. Create a Python virtual environment and install dependencies (Version **>=Python 3.10.12** is required):
    ```bash
    python -m venv venv
    source venv/bin/activate        # or `venv\Scripts\activate` on Windows
    pip install -r requirements.txt
    ```

3. Prepare API tokens in `tokens.env`.

## Usage
Run the bot:
```bash
python bot.py
```